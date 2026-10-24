"""A5 unscaled diagnostic crops and explicit human-readable model verdicts."""
from PIL import Image, ImageDraw, ImageChops, ImageStat
from prepare_a5_frames import *
import a4_style_check as a4style

PATHS=[a4.REFS['idle']]+[f'thoma/swing/{i:02}.png' for i in range(6)]
NAMES=['stole','embroidery','cuffs','hem','face_hair','palette','seams','waist_seam','bag','feet']
CHECKS=['stole','embroidery','cuffs','hem','face_hair','palette','seams','bag_count','feet','sequence']
BG=(34,40,38)

def region(im,path,name,baseline=False):
    moving='/swing/' in path and not path.endswith('05.png')
    index=path[-6:-4];p=POSES[index] if moving else None
    ref=p['ref'] if moving else ('idle' if '/idle/' in path else 'recover')
    extra={'seams':(190,145,337,235),'waist_seam':(180,227,322,286),
           'bag':(175,242,250,345),'feet':(100,375,420,470)}
    if name in extra:
        box=extra[name]
        # Broad context crops reveal joins rather than masking them away.
        return im.crop(box),box,mask(rect(*box))
    keys={'stole':['stole-left','stole-left-lower','stole-right'],'embroidery':['embroidery'],
          'cuffs':['cuff-left','cuff-right'],'hem':['hem'],'face_hair':['face-hair'],'palette':['body']}[name]
    m=Image.new('L',SIZE)
    for key in keys:m=ImageChops.lighter(m,mask(a4.ref_poly(ref,key)))
    if moving:
        if name=='face_hair':
            new=Image.new('L',SIZE);new.paste(m,tuple(p['head']));m=new
        elif name=='cuffs':
            m=Image.new('L',SIZE)
            for dst in p['cuffs']:m=ImageChops.lighter(m,mask(dst))
        elif baseline:
            s,dx,dy=p['shear'],p['dx'],p['dy'];scale=1.15
            m=m.transform(SIZE,Image.Transform.AFFINE,(1/scale,-s/scale,(s*(dy+250)-dx+245*(scale-1))/scale,0,1,-dy),Image.Resampling.BICUBIC)
        else:
            # Actual body now uses recover reference for every pose.
            m=Image.new('L',SIZE)
            for key in keys:m=ImageChops.lighter(m,mask(a4.ref_poly('recover',key)))
            m=transform_body(m,dict(p,index=index))
    m=ImageChops.multiply(m,im.getchannel('A'))
    b=m.getbbox();box=(max(0,b[0]-4),max(0,b[1]-4),min(512,b[2]+5),min(512,b[3]+5))
    return im.crop(box),box,m

def main():
    sheet=Image.new('RGB',(13600,1690),BG);d=ImageDraw.Draw(sheet)
    d.text((10,8),'A5 MODEL CHECK | 1:1 source-pixel crops: idle / recover / A4 / A5 | not runtime screenshots',fill='white')
    crops=[]
    for row,path in enumerate(PATHS[1:6]):
        y=35+row*300
        for col,name in enumerate(NAMES):
            x=col*1360;d.text((x+8,y),f'{path} {name}',fill='#d2b777')
            for j,src in enumerate([a4.REFS['idle'],a4.REFS['recover'],path,path]):
                file=BASE/f'{path[-6:-4]}.png' if j==2 else SHARED/src
                im=Image.open(file).convert('RGBA');crop,box,m=region(im,src,name,j==2)
                if name=='palette':
                    rgb=tuple(round(v) for v in ImageStat.Stat(im.convert('RGB'),m).mean)
                    d.rectangle((x+j*340+8,y+35,x+j*340+200,y+150),fill=rgb)
                    d.text((x+j*340+8,y+165),str(rgb),fill='white')
                else:
                    assert crop.width<=340 and crop.height<=260,(src,name,crop.size)
                    sheet.paste(crop,(x+j*340+8,y+25),crop)
                d.text((x+j*340+8,y+280),['idle/01','swing/05','A4 '+path[-6:-4],'A5 '+path[-6:-4]][j],fill='white')
                crops.append({'frame':src,'source':file.relative_to(REPO).as_posix(),'region':name,'crop':box,'scale':1})
    d.text((10,1550),'Native 720p rest-canvas scale 68px (zoomed attack is 1.4x). Rendered evidence is separate in W5.',fill='white')
    for i,path in enumerate(PATHS):
        im=Image.open(SHARED/path).convert('RGBA').resize((68,68),Image.Resampling.LANCZOS)
        sheet.paste(im,(i*250+15,1590),im);d.text((i*250+90,1610),path,fill='white')
    sheet.save(OUT/'region-check.png',optimize=True);write(OUT/'region-crops.json',crops)
    strip=Image.new('RGB',(1792,490),BG);d=ImageDraw.Draw(strip)
    for i,path in enumerate(PATHS):
        im=Image.open(SHARED/path).convert('RGBA');small=im.resize((256,256),Image.Resampling.LANCZOS)
        d.text((i*256+8,8),path,fill='white');strip.paste(small,(i*256,30),small)
        native=im.resize((68,68),Image.Resampling.LANCZOS);strip.paste(native,(i*256+94,310),native)
        if i:
            prior=Image.open(SHARED/PATHS[i-1]).convert('RGBA');prior.putalpha(prior.getchannel('A').point(lambda a:a//3))
            onion=Image.alpha_composite(prior,im);onion.thumbnail((96,96));strip.paste(onion,(i*256+80,390),onion)
    d.text((8,290),'Seven-frame flip strip / native rest size / adjacent onion skin. Model inspection; no human approval.',fill='white')
    strip.save(OUT/'sequence-strip.png',optimize=True);strip.save(SHARED/'thoma-weapon-style-check.png',optimize=True)
    pairs=[]
    for prev,cur in zip(PATHS,PATHS[1:]):
        ims=[Image.open(SHARED/p).convert('RGBA') for p in [prev,cur]]
        means={}
        for name in NAMES[:6]:
            values=[ImageStat.Stat(im.convert('RGB'),region(im,p,name)[2]).mean for im,p in zip(ims,[prev,cur])]
            means[name]=round(math.dist(*values),4)
        # Fixed garment-only comparison box, excluding head/mace/most arms.
        silhouettes=[im.getchannel('A').crop((100,275,420,440)).point(lambda a:255 if a>127 else 0) for im in ims]
        intersection=sum(v>0 for v in ImageChops.darker(*silhouettes).getdata())
        union=sum(v>0 for v in ImageChops.lighter(*silhouettes).getdata())
        pairs.append({'from':prev,'to':cur,'region_mean_rgb_delta':means,'garment_silhouette_iou':round(intersection/union,6),
            'silhouette_crop':[100,275,420,440],'visual_result':'FAIL',
            'reason':'Pose-specific sleeve/shoulder fold orientation and lower-hem sweep still pop; numerical proxies do not establish continuity.'})
    write(OUT/'sequence-check.json',{'authority':'model inspection; not human playtest','pairs':pairs,
        'limits':'Mean RGB includes changing occlusion. IoU is fixed-canvas garment crop, not registered perceptual similarity; no threshold used to approve art.'})
    print('A5_SHEETS crops=200 sequence_pairs=6; visual verdicts added separately after inspection')

if __name__=='__main__':main()
