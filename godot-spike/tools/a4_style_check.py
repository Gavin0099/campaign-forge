"""Same-scale region sheets and explicit model observations; never auto-approve art."""
from PIL import Image, ImageDraw, ImageChops, ImageStat
from prepare_a4_frames import SHARED, OUT, LIB, REFS, POSES, REGIONS, ref_poly, mask, rect, sha, write
import json, math

PATHS=[REFS['idle']]+[f'thoma/swing/{i:02}.png' for i in range(6)]
REGION_NAMES=['stole','embroidery','cuffs','hem','face_hair','palette']
BACKGROUND=(34,40,38)
REASONS={
 '00': {'stole':'FAIL: shoulder band meets retained raised-arm paint abruptly; bag/plain-cloth clone has a visible horizontal seam.',
        'embroidery':'PASS: same source lower-end sprig, one row with no doubled motif; lateral 15 percent ease is documented.',
        'cuffs':'FAIL: cloth grain is reference-derived but the raised cuff changes fold direction abruptly at the sleeve join.',
        'hem':'FAIL: fan contour replaced with reference edge, but left boot/hem connection is too narrow and near-idle drape lacks coil.',
        'face_hair':'PASS: reference face and hair translated as one unit; recognizable grey beard and facial identity.',
        'palette':'PASS: muted reference teal/ivory/brown retained; no new palette mapping.',
        'sequence':'FAIL: idle-to-raised sleeve/shoulder joins pop; narrow hem against spread feet is discontinuous.'},
 '01': {'stole':'FAIL: upper band/arm seam and horizontal bag clone edge remain visible.',
        'embroidery':'PASS: intact source sprig and border spacing along the band; no added leaf row.',
        'cuffs':'FAIL: raised cuff texture reads as a separate patch despite correct reference color.',
        'hem':'FAIL: reference scalloped edge retained but transition from preceding wide stance is abrupt.',
        'face_hair':'PASS: same source facial identity and grey hair; moderate positional change.',
        'palette':'PASS: no visible color-family flicker or Ferry Dusk palette.',
        'sequence':'FAIL: raised-to-swing torso occlusion and cuff silhouette jump remain.'},
 '02': {'stole':'FAIL: squared shoulder cut and waist overlay boundary expose the cutout construction.',
        'embroidery':'PASS: lower motif remains the same source sprig at unit vertical scale.',
        'cuffs':'FAIL: off-hand cuff has an abrupt triangular edge and fold transition.',
        'hem':'FAIL: old swept fan removed, but reference hem bridges the fixed stance awkwardly.',
        'face_hair':'PASS: recover reference face/hair remains identifiable through forward motion.',
        'palette':'PASS: reference palette retained; numeric delta includes changing occlusion.',
        'sequence':'FAIL: torso/cuff boundaries and cloth-to-boot junction change visibly from raised pose.'},
 '03': {'stole':'FAIL: waist/shoulder joins and cloned bag occlusion remain visible even though full source bands are used.',
        'embroidery':'PASS: original sprig/line weight survives the small shear with no doubled rows.',
        'cuffs':'FAIL: primary cuff retains a visible composite boundary against the extended sleeve.',
        'hem':'FAIL: reference-shaped edge replaces broad fan; wide planted stance still reads disconnected at the left ankle.',
        'face_hair':'PASS: unchanged reference facial pixels translated to contact head position.',
        'palette':'PASS: original muted color family with no independent color remapping.',
        'sequence':'FAIL: contact-to-follow-through changes shoulder occlusion and hem attachment abruptly.'},
 '04': {'stole':'FAIL: torso twist retains an A3 shoulder seam; reference-band/body junction and bag clone remain apparent.',
        'embroidery':'PASS: source lower sprig persists with fixed vertical spacing; shear follows cloth direction.',
        'cuffs':'FAIL: front cuff is reference cloth but edge/fold transition still reads pasted.',
        'hem':'FAIL: trailing contour now derives from reference, but floor/boot overlap and recovery shape jump remain.',
        'face_hair':'PASS: source recover face and hair transferred together; no regenerated identity.',
        'palette':'PASS: no visible independent palette change.',
        'sequence':'FAIL: trailing garment snaps back to unwarped recovery; this is not a continuous finished costume rig.'},
}

def region_mask(path,name):
    moving='/swing/' in path and not path.endswith('05.png')
    ref='idle' if path==REFS['idle'] else 'recover'
    p=POSES[path[-6:-4]] if moving else None
    if moving: ref=p['ref']
    keys={'stole':['stole-left','stole-left-lower','stole-right'],'embroidery':['embroidery'],
          'cuffs':['cuff-left','cuff-right'],'hem':['hem'],'face_hair':['face-hair'],'palette':['body']}[name]
    m=Image.new('L',(512,512))
    for key in keys:m=ImageChops.lighter(m,mask(ref_poly(ref,key)))
    if p:
        if name=='face_hair':
            new=Image.new('L',(512,512));new.paste(m,tuple(p['head']));m=new
        elif name=='cuffs':
            m=Image.new('L',(512,512))
            for dst in p['cuffs']:m=ImageChops.lighter(m,mask(dst))
        else:
            s,dx,dy=p['shear'],p['dx'],p['dy'];scale=1.15
            m=m.transform((512,512),Image.Transform.AFFINE,(1/scale,-s/scale,(s*(dy+250)-dx+245*(scale-1))/scale,0,1,-dy),Image.Resampling.BICUBIC)
    im=Image.open(SHARED/path).convert('RGBA')
    return ImageChops.multiply(m,im.getchannel('A'))

def crop_region(im,m):
    box=m.getbbox()
    # Include 4 px context so joins are visible; do not mask away defects.
    box=(max(0,box[0]-4),max(0,box[1]-4),min(512,box[2]+5),min(512,box[3]+5))
    return im.crop(box),box

def main():
    sheet=Image.new('RGB',(5040,1680),BACKGROUND);d=ImageDraw.Draw(sheet)
    d.text((10,8),'A4 MODEL REGION CHECK | all crops 1:1 source pixels, no per-cell resizing | idle / recover / swing | NOT runtime screenshots',fill='white')
    crops=[];means={};masks=OUT/'region-masks';masks.mkdir(exist_ok=True)
    for row,path in enumerate(PATHS[1:6]):
        top=40+row*300
        d.text((8,top),path+' | PLACEHOLDER',fill='#ffb58a')
        for col,name in enumerate(REGION_NAMES):
            x=col*840;d.text((x+8,top+18),name,fill='#d2b777')
            for j,src in enumerate([REFS['idle'],REFS['recover'],path]):
                im=Image.open(SHARED/src).convert('RGBA');m=region_mask(src,name)
                crop,box=crop_region(im,m)
                # 240 px columns fit all explicit regions; entire palette body is
                # shown as measured swatch, not resized to impersonate a crop.
                if name=='palette':
                    rgb=tuple(round(c) for c in ImageStat.Stat(im.convert('RGB'),m).mean)
                    d.rectangle((x+j*280+8,top+65,x+j*280+220,top+180),fill=rgb)
                    d.text((x+j*280+8,top+190),str(rgb),fill='white')
                else:
                    assert crop.width<=280 and crop.height<=260,(src,name,crop.size)
                    sheet.paste(crop,(x+j*280+(280-crop.width)//2,top+38),crop)
                d.text((x+j*280+8,top+280),['idle/01','swing/05',path[-12:]][j],fill='white')
                crops.append({'frame':src,'region':name,'box':box,'scale':1})
    for i,path in enumerate(PATHS):
        im=Image.open(SHARED/path).convert('RGBA');native=im.resize((68,68),Image.Resampling.LANCZOS)
        x=15+i*250;sheet.paste(native,(x,1590),native);d.text((x+72,1620),path,fill='white')
        means[path]={}
        for name in REGION_NAMES:
            m=region_mask(path,name);m.save(masks/(path.replace('/','-').replace('.png','')+'-'+name+'.png'))
            means[path][name]=[round(v,4) for v in ImageStat.Stat(im.convert('RGB'),m).mean]
    d.text((10,1568),'Native 720p asset size approximation: 68px canvas / ~48px body. Rendered verification is separate.',fill='white')
    sheet.save(OUT/'region-check.png',optimize=True);write(OUT/'region-crops.json',crops)
    strip=Image.new('RGB',(1792,490),BACKGROUND);draw=ImageDraw.Draw(strip)
    for i,path in enumerate(PATHS):
        im=Image.open(SHARED/path).convert('RGBA');small=im.resize((256,256),Image.Resampling.LANCZOS)
        draw.text((i*256+8,8),path,fill='white');strip.paste(small,(i*256,30),small)
        native=im.resize((68,68),Image.Resampling.LANCZOS);strip.paste(native,(i*256+94,310),native)
        if i:
            prior=Image.open(SHARED/PATHS[i-1]).convert('RGBA');prior.putalpha(prior.getchannel('A').point(lambda a:a//3))
            onion=Image.alpha_composite(prior,im);onion.thumbnail((96,96));strip.paste(onion,(i*256+80,390),onion)
    draw.text((8,290),'Flip-strip + native-size row + adjacent onion overlay | no costume continuity PASS inferred from palette metrics',fill='white')
    strip.save(OUT/'sequence-strip.png',optimize=True);strip.save(SHARED/'thoma-weapon-style-check.png',optimize=True)
    sequence=[]
    for prev,cur in zip(PATHS,PATHS[1:]):
        sequence.append({'from':prev,'to':cur,'region_mean_rgb_delta':{name:round(math.dist(means[prev][name],means[cur][name]),4) for name in REGION_NAMES},'visual_result':'FAIL','reason':'Sleeve/torso joins or hem-to-stance attachment change abruptly; palette mean does not detect spatial seams.'})
    write(OUT/'sequence-check.json',{'authority':'model inspection, not human playtest','metric':'Euclidean distance of mask-weighted mean RGB, unaligned poses; occlusion affects sample composition','pairs':sequence})
    audit=json.loads((SHARED/'frame-audit.json').read_text(encoding='utf-8'))
    provenance={r['frame']:r for r in json.loads((SHARED/'a4-swing-prompts.json').read_text())}
    lines=['| Frame | Status | Stole | Embroidery | Cuffs | Hem | Face/hair | Palette | Sequence | Reason |','| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for path in PATHS:
        record=next(r for r in audit if r['path']==path)
        moving=path in provenance
        results=REASONS[path[-6:-4]] if moving else {name:'PASS: unchanged accepted A3 reference region.' for name in REGION_NAMES+['sequence']}
        if not moving:results['sequence']='PASS: unchanged reference endpoint; incoming/outgoing motion-transition defects are assigned to motion frames in sequence-check.json.'
        reason=('Reference pixel method fixes the old fan contour and duplicate motif rows, but '+REASONS[path[-6:-4]]['stole'][6:]+' '+REASONS[path[-6:-4]]['hem'][6:]) if moving else 'Byte-unchanged A3 reference; model PASS retained, not Owner art approval.'
        record.update(sha256=sha(SHARED/path),review_segment='spike-02 A4',status='PLACEHOLDER' if moving else 'PASS',reason=reason,
            review_authority='model visual inspection; Owner art approval not claimed',region_review=results)
        if moving:record.update(source='reference pixel rig: idle/01 + swing/05',raw_sha256=None,cleanup=provenance[path]['cleanup'],palette_distance=provenance[path]['palette_distance'])
        record['style_review']={
            'face':results['face_hair'],'stole_cape_embroidery':results['stole'],'cuffs':results['cuffs'],
            'hem_silhouette':results['hem'],'palette':results['palette'],'proportions':'PASS: canvas/pivot fixed; exact pose weapon retained.',
            'light_direction':'PASS: source top-left paint retained.','stroke':'FAIL: visible composite joins remain.' if moving else 'PASS: unchanged reference.',
            'satchel_medallion':'FAIL: bag clone boundary visible; reference medallion preserved.' if moving else 'PASS: unchanged reference.'}
        flags=[results[k].split(':')[0] for k in REGION_NAMES+['sequence']]
        lines.append('| `'+path+'` | '+record['status']+' | '+' | '.join(flags)+' | '+reason+' |')
    write(SHARED/'frame-audit.json',audit)
    (OUT/'frame-status-table.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    source=(SHARED/'SOURCES.md').read_text(encoding='utf-8').split('\n### A4 W3 model verdict')[0]
    source=source.split('\n| Frame | Reference hashes | A4 runtime SHA-256')[0]
    source+='\n| Frame | A4 runtime SHA-256 | Palette distance before / after |\n| --- | --- | --- |\n'
    for item in provenance.values():
        source+=f"| {item['frame']} | {item['runtime_sha256']} | {item['palette_distance']['before']} / {item['palette_distance']['after']} |\n"
    with (SHARED/'SOURCES.md').open('w',encoding='utf-8',newline='\n') as f:
        f.write(source)
        f.write('\n### A4 W3 model verdict\n\nFive motion frames remain PLACEHOLDER. Reference transfer fixes provenance and replaces the old contour, but shoulder/cuff/bag seams and hem-to-feet continuity fail. See frame-audit.json region_review and spike02-a4/sequence-check.json. Two immutable references retain PASS. No human or Owner art approval is claimed.\n')
    print('A4_STYLE_CHECK region_results=42 motion_placeholder=5 reference_pass=2 sequence_pairs_failed=6')

if __name__=='__main__':main()
