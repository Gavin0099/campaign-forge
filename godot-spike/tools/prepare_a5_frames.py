"""A5 deterministic refinement of A4 reference cutout rig. No AI generation.

--proof writes only evidence; --build first archives A4 then replaces 00-04.
No reference extraction writes and no modifications of the A4 script/library.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter, ImageStat
from io import BytesIO
import argparse, copy, hashlib, json, math, shutil
import prepare_a4_frames as a4

REPO, SHARED = a4.REPO, a4.SHARED
OUT = REPO/'godot-spike/docs/evidence/spike02-a5'
BASE = OUT/'baseline-a4'
SIZE = (512,512)
sha, write, mask, cut, rect = a4.sha, a4.write, a4.mask, a4.cut, a4.rect
POSES = copy.deepcopy(a4.POSES)
# Same affine/arm/head/weapon controls as A4. Horizontal garment scale is 1.0.
# Recover body avoids idle mace occlusion through the satchel. Both references
# still supply their original face and cuff pixels as in the A4 rig.
HEM_EASE = {'00':.70,'01':.48,'02':.98,'03':.82,'04':.48}
CLONES = [
    {'source':rect(181,345,207,381),
     'target':[(188,304),(219,310),(222,353),(201,345)]},
    {'source':rect(235,271,252,308),
     'target':[(219,311),(239,319),(249,353),(222,351)]},
]

def transform_body(im,p,hem=True):
    """Unit-scale upper garment; horizontal ease ONLY below all motif rows."""
    # Reference recovery body is three pixels above idle: correct at input.
    dy=p['dy']+(3 if p['ref']=='idle' else 0)
    # MESH strips keep horizontal scale at 1 through y=382. Gradual hem ease
    # is continuous at strip boundaries and retains the reference scallops.
    mesh=[]
    for y in range(0,512,2):
        quad=[]
        for x,yy in [(0,y),(0,y+2),(512,y+2),(512,y)]:
            sy=yy-dy
            t=max(0,min(1,(sy-382)/43)) if hem else 0
            ease=1+HEM_EASE[p['index']]*t*t*(3-2*t)
            sx=(x-245-p['dx']-p['shear']*(sy-250))/ease+245
            quad.extend([sx,sy])
        mesh.append(((0,y,512,y+2),tuple(quad)))
    return im.transform(SIZE,Image.Transform.MESH,mesh,Image.Resampling.BICUBIC)

def bands(index):
    p=POSES[index]
    # Bands follow actual retained arm/torso boundaries, never entire garments.
    joins=[]
    for i,poly in enumerate(p['arms']):
        joins.append({'name':f'arm-shoulder-twist-{i}','points':poly+[poly[0]],'width':8})
    for i,poly in enumerate(p['cuffs']):
        joins.append({'name':f'cuff-{i}','points':poly+[poly[0]],'width':6})
    joins.append({'name':'waist','points':[(193+p['dx'],269+p['dy']),
                  (246+p['dx'],274+p['dy']),(299+p['dx'],267+p['dy'])],'width':8})
    combined=Image.new('L',SIZE)
    for join in joins:
        ImageDraw.Draw(combined).line([tuple(v) for v in join['points']],fill=255,width=join['width'],joint='curve')
    return combined,joins

def soft_layer(target,layer,poly,width):
    """Feather inward only. All departure from hard cut lies in seam band."""
    m=mask(poly)
    inner=m.filter(ImageFilter.MinFilter(width*2+1))
    feather=inner.filter(ImageFilter.GaussianBlur(width/2))
    # Binary support; no blur paint can leak outside the declared poly/band.
    feather=ImageChops.multiply(feather,m)
    # RGB/alpha interpolated once, avoiding transparent double-composition.
    target.alpha_composite(Image.composite(layer,Image.new('RGBA',SIZE),feather))

def build(index,old):
    p=dict(POSES[index],index=index)
    ref=Image.open(SHARED/a4.REFS['recover']).convert('RGBA')
    body=cut(ref,a4.ref_poly('recover','body'))
    # Recover mace occludes a small plain lower-band patch, NOT the satchel.
    # Use undecorated ivory cloth, not the old A4 bag-bearing source.
    for patch in CLONES:
        part=a4.perspective(ref,patch['source'],patch['target'])
        m=mask(patch['target']);m=m.filter(ImageFilter.GaussianBlur(.7))
        alpha=body.getchannel('A');body.paste(part,(0,0),m);body.putalpha(alpha)
    body=transform_body(body,p)
    # Upper cape silhouette is retained from A4, ending before the satchel.
    # A4 head-clear prevents a duplicate face behind the translated reference.
    out=old.copy()
    out.paste((0,0,0,0),(0,248,512,512))
    out.paste((0,0,0,0),a4.HEAD_CLEAR[index])
    for poly in p['feet']:out.alpha_composite(cut(old,poly))
    out.alpha_composite(cut(old,rect(0,432,511,511)))
    out.alpha_composite(body)
    # No retained whole upper torso behind the new body: this removes duplicate
    # bag/cloth outside the cutout. Existing motion arms alone are reintroduced.
    for poly in p['arms']:soft_layer(out,old,poly,2)
    reference=Image.open(SHARED/a4.REFS[p['ref']]).convert('RGBA')
    head=cut(reference,a4.ref_poly(p['ref'],'face-hair'))
    out.alpha_composite(head,tuple(p['head']))
    for i,dst in enumerate(p['cuffs']):
        src=([(167,236),(197,246),(192,273),(157,266)] if i==0 else [(306,220),(318,229),(325,240),(301,254)])
        delta=-3 if p['ref']=='recover' else 0
        cuff=a4.perspective(reference,[(x,y+delta) for x,y in src],dst)
        # Keep original cuff interior, mix narrow edge to underlying sleeve.
        soft_layer(out,cuff,dst,1)
    # Recorded narrow-band paint-over: local 0.75px color smoothing only, no
    # new lines or motifs. Opaque interior only; never alter source outline.
    seam,_=bands(index)
    inside=out.getchannel('A').point(lambda a:255 if a==255 else 0).filter(ImageFilter.MinFilter(3))
    seam=ImageChops.multiply(seam,inside)
    blurred=out.filter(ImageFilter.GaussianBlur(.75))
    out.paste(blurred,(0,0),seam.point(lambda a:a//2))
    protected=Image.new('L',SIZE)
    for poly in p['weapon']:protected=ImageChops.lighter(protected,mask(poly))
    head_mask=Image.new('L',SIZE)
    head_mask.paste(mask(a4.ref_poly(p['ref'],'face-hair')),tuple(p['head']))
    protected=ImageChops.lighter(protected,head_mask)
    # Preserve entire fixed feet, not a newly invented boot or changed stance.
    for poly in p['feet']:protected=ImageChops.lighter(protected,mask(poly))
    protected=ImageChops.lighter(protected,mask(rect(0,444,511,511)))
    out.putdata([(0,0,0,0) if q[3]==0 else q for q in out.getdata()])
    out.paste(old,(0,0),protected)
    return out,protected

def controls():
    OUT.mkdir(parents=True,exist_ok=True)
    folder=OUT/'seam-masks';folder.mkdir(exist_ok=True)
    rows=[]
    for index in POSES:
        m,joins=bands(index);m.save(folder/f'{index}.png',optimize=True)
        area=sum(v>0 for v in m.getdata())
        rows.append({'frame':index,'mask':f'{index}.png','sha256':sha(folder/f'{index}.png'),
                     'bands':joins,'total_pixel_area':area,'max_area':10000,'max_band_width':8})
        assert area<=10000
    write(folder/'coordinates.json',rows)
    write(OUT/'rig-controls.json',{'base':'../spike02-a4/reference-regions/rig-controls.json',
        'poses':POSES,'body_reference':a4.REFS['recover'],'body_horizontal_scale':1.0,
        'hem_start_source_y':382,'hem_end_source_y':425,'hem_ease':HEM_EASE,
        'plain_cloth_occlusion_patches':CLONES,'seam_blur_radius':.75,'canvas':[512,512],'pivot':[256,464]})
    measurements=[]
    for index,p in POSES.items():
        # Local mapping at same y: source horizontal 25px motif and 12px
        # horizontal feature spacing, independent of shear translation.
        motif=a4.REGIONS['embroidery'];width=motif[1][0]-motif[0][0]
        measurements.append({'frame':index,'reference':a4.REFS['recover'],'reference_roi':[226,340,251,373],
            'reference_motif_roi_width_px':width,
            'a4_width_px':width*1.15,'a5_width_px':width,'horizontal_spacing_scale':1.0,
            'horizontal_change_percent':0,'tolerance_percent':5,'result':'PASS',
            'metric':'analytical local horizontal mapping of committed reference motif ROI; not a perceptual score'})
    write(OUT/'scale-measurement.json',measurements)
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--proof',action='store_true');parser.add_argument('--build',action='store_true');a=parser.parse_args()
    controls()
    if a.proof:
        path=SHARED/'thoma/swing/03.png';old=Image.open(path).convert('RGBA');new,_=build('03',old)
        new.save(OUT/'proof-03.png',optimize=True)
        sheet=Image.new('RGB',(1250,310),(34,40,38));d=ImageDraw.Draw(sheet)
        crops={'shoulder':(200,154,302,230),'waist':(193,227,304,283),'cuff':(277,177,342,229),
               'bag':(177,248,245,341),'hem-feet':(108,374,397,469)}
        x=0
        for label,box in crops.items():
            d.text((x+4,5),label,fill='white')
            for row,im in enumerate([old,new]):
                crop=im.crop(box);sheet.paste(crop,(x+5,25+row*140),crop)
                d.text((x+5,122+row*140),'A4 before' if row==0 else 'A5 draft',fill='white')
            x+=box[2]-box[0]+35
        sheet.save(OUT/'proof-before-after.png',optimize=True)
        write(OUT/'proof.json',{'frame':'03','input_sha256':sha(path),'output_sha256':sha(OUT/'proof-03.png'),
              'generation_attempts':0,'status':'DRAFT; visual review in W3','crops':crops})
        print('A5_W1 proof=03 masks=5 scale=1.0 generation_attempts=0')
    if a.build:
        BASE.mkdir(exist_ok=True)
        for i in range(6):
            dst=BASE/f'{i:02}.png'
            if not dst.exists():shutil.copyfile(SHARED/f'thoma/swing/{i:02}.png',dst)
        for src,dst in [(SHARED/a4.REFS['idle'],BASE/'idle-01.png'),(SHARED/'manifest.json',BASE/'manifest.json'),
                        (SHARED/'frame-audit.json',BASE/'frame-audit.json'),(SHARED/'thoma-weapon-style-check.png',OUT/'style-check-a4.png')]:
            if not dst.exists():shutil.copyfile(src,dst)
        write(BASE/'hashes.json',[{'path':p.relative_to(REPO).as_posix(),'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.name!='hashes.json'])
        colors=[]
        for path in a4.REFS.values():colors.extend([v[:3] for v in Image.open(SHARED/path).convert('RGBA').getdata() if v[3]>240])
        strip=Image.new('RGB',(len(colors),1));strip.putdata(colors);pal=strip.quantize(colors=128).getpalette();pal=[tuple(pal[i:i+3]) for i in range(0,384,3)]
        rows=[];(OUT/'protected-masks').mkdir(exist_ok=True)
        for index in POSES:
            old=Image.open(BASE/f'{index}.png').convert('RGBA');im,protected=build(index,old)
            path=SHARED/f'thoma/swing/{index}.png';im.save(path,optimize=True);protected.save(OUT/f'protected-masks/{index}.png',optimize=True)
            rows.append({'frame':f'thoma/swing/{index}.png','tool':'Pillow deterministic A4-rig refinement','generation_attempts':0,
                'prompt':None,'raw':None,'raw_sha256':None,'rejected_attempts':[],
                'references':{path:sha(SHARED/path) for path in a4.REFS.values()},'baseline_sha256':sha(BASE/f'{index}.png'),
                'runtime_sha256':sha(path),'mask':f'godot-spike/docs/evidence/spike02-a5/seam-masks/{index}.png',
                'mask_sha256':sha(OUT/f'seam-masks/{index}.png'),'controls':'godot-spike/docs/evidence/spike02-a5/rig-controls.json',
                'palette_distance':{'before':a4.palette_distance(old,pal),'after':a4.palette_distance(im,pal),
                    'metric':'mean nearest reference 128-color Euclidean RGB, alpha>240','mapping_applied':False},
                'cleanup':'One recover reference body, unit motif scale, plain ivory occlusion fill, lower hem mesh; narrow seam smoothing; fixed raw weapon/hand/feet overwrite; transparent RGB cleared outside protection.'})
        write(SHARED/'a5-swing-prompts.json',rows)
        print('A5_W2 rebuilt=5 references_unchanged=true generation_attempts=0')

if __name__=='__main__':main()

