"""Reference-pixel cutout rig; no generation, no edits to reference PNGs.

Coordinates are in the fixed 512 canvas. Run --proof for W1; --build for W2.
Only Pillow is required. All controls/masks and provenance are exported.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter, ImageStat
import argparse, hashlib, json, shutil, math
from collections import Counter

REPO = Path(__file__).resolve().parents[2]
SHARED = REPO / 'shared-anim'
OUT = REPO / 'godot-spike/docs/evidence/spike02-a4'
LIB = OUT / 'reference-regions'
SIZE = (512, 512)
REFS = {'idle': 'thoma/idle/01.png', 'recover': 'thoma/swing/05.png'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, obj): p.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
def rect(x0,y0,x1,y1): return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
def mask(poly):
    im=Image.new('L',SIZE); ImageDraw.Draw(im).polygon(poly,fill=255); return im
def cut(im,poly):
    result=im.copy(); result.putalpha(ImageChops.multiply(im.getchannel('A'),mask(poly))); return result

# Library includes complete contiguous body, plus independently inspectable regions.
REGIONS = {
 'body': [(192,158),(215,150),(279,153),(290,180),(299,239),(307,301),(329,354),(319,398),(281,420),(235,429),(173,417),(162,383),(182,331),(187,294),(193,240),(203,216)],
 'stole-left': [(192,159),(207,157),(230,182),(245,239),(231,248),(220,199),(208,177)],
 'stole-left-lower': [(230,257),(251,252),(256,379),(219,386),(221,340)],
 'stole-right': [(278,157),(287,165),(292,228),(311,348),(292,360),(282,308),(280,233)],
 'embroidery': rect(226,343,251,376),
 'cuff-left': [(167,234),(188,243),(199,245),(193,274),(174,278),(156,267)],
 'cuff-right': [(308,215),(319,228),(328,239),(313,252),(300,259),(298,241)],
 'hem': [(165,355),(324,350),(321,397),(279,421),(235,427),(172,417),(162,384)],
 'satchel': [(199,248),(237,248),(232,290),(220,315),(187,305),(180,284)],
 'medallion': rect(250,196,271,221),
 'face-hair': [(226,120),(234,106),(253,101),(273,107),(287,118),(287,146),(278,164),(258,171),(241,158),(232,143)],
}
# Recover is 8 px higher at the head, 3 px higher on the garment.
def ref_poly(name, region):
    dy = (-8 if region=='face-hair' else -3) if name=='recover' else 0
    return [(x,y+dy) for x,y in REGIONS[region]]

# Reference mace occludes a small part of satchel/plain stole. Remove only that
# motion object on an intermediate layer using nearby *plain* reference cloth.
# No motif, border or hem is synthesized. Source/destination are recorded.
CLONES = [
 {'source':rect(193,260,218,288),'target':[(181,288),(200,288),(229,319),(204,323)]},
 {'source':rect(231,270,250,309),'target':rect(214,306,253,347)},
]

# Affine torso: x'=x+shear*(y-250)+dx, y'=y+dy. Motifs retain unit scale.
# Every pose uses the same body topology; changing shear is cloth sweep only.
POSES = {
 '00': {'ref':'idle','dx':22,'dy':2,'shear':0.09,'head':[20,8],
        'arms':[[(106,129),(135,126),(172,145),(200,140),(222,174),(218,221),(190,238),(164,213),(138,198),(112,191)],[(290,171),(327,187),(360,214),(382,244),(392,269),(367,273),(346,252),(322,264),(297,234)]],
        'weapon':[rect(95,65,213,140)], 'feet':[[(141,399),(166,412),(158,446),(143,463),(123,463),(126,435)],[(327,399),(361,402),(382,423),(369,434),(335,431),(320,417)]],
        'cuffs': [[(117,145),(135,143),(156,175),(121,184)],[(338,211),(357,224),(342,262),(319,246)]]},
 '01': {'ref':'idle','dx':13,'dy':1,'shear':0.04,'head':[17,8],
        'arms':[[(144,125),(166,119),(196,143),(213,155),(228,188),(207,220),(183,207),(158,180)],[(284,172),(311,182),(331,203),(326,251),(301,253),(289,224)]],
        'weapon':[rect(143,65,225,143)], 'feet':[[(169,398),(194,412),(187,454),(171,464),(154,459)],[(316,393),(345,398),(361,414),(350,425),(320,422)]],
        'cuffs': [[(152,153),(173,145),(186,171),(160,178)],[(306,212),(330,215),(319,249),(302,238)]]},
 '02': {'ref':'recover','dx':19,'dy':7,'shear':-0.13,'head':[32,16],
        'arms':[[(232,170),(264,174),(287,181),(329,165),(358,157),(369,175),(343,193),(332,226),(295,228),(261,222),(237,221)],[(298,233),(325,232),(348,247),(367,270),(359,285),(337,269),(319,277),(303,259)]],
        'weapon':[[(337,142),(379,108),(424,72),(454,82),(457,114),(400,147),(361,174)]],
        'feet':[[(115,404),(146,403),(155,425),(138,457),(118,466),(102,456)],[(330,400),(365,409),(391,431),(379,446),(341,435),(326,420)]],
        'cuffs': [[(309,185),(333,174),(339,213),(293,213)],[(335,239),(354,249),(338,273),(323,258)]]},
 '03': {'ref':'recover','dx':15,'dy':8,'shear':-0.13,'head':[28,19],
        'arms':[[(222,171),(245,173),(272,175),(303,179),(335,177),(345,184),(376,184),(380,207),(337,213),(328,229),(301,220),(276,220),(245,231),(220,216)],[(291,232),(318,233),(339,249),(344,269),(330,273),(316,260),(305,269),(294,257)]],
        'weapon':[rect(340,170,480,225)],
        'feet':[[(124,399),(155,405),(157,426),(141,458),(123,465),(111,454)],[(322,395),(353,402),(391,424),(394,441),(372,447),(327,435)]],
        'cuffs': [[(303,183),(330,183),(321,218),(280,211)],[(315,242),(329,250),(317,268),(303,258)]]},
 '04': {'ref':'recover','dx':9,'dy':11,'shear':-0.16,'head':[36,20],
        'arms':[[(181,187),(201,195),(214,219),(198,232),(178,219),(165,228),(154,231),(151,219)],[(258,187),(278,190),(290,212),(307,242),(332,275),(350,293),(345,310),(330,302),(302,299),(278,276),(263,249),(248,218)]],
        'weapon':[[(328,286),(355,297),(405,340),(421,371),(402,382),(370,347),(336,314)]],
        'feet':[[(125,397),(150,396),(154,420),(141,451),(122,460),(111,451)],[(292,392),(320,393),(337,427),(352,441),(345,454),(323,448),(298,425)]],
        'cuffs': [[(282,253),(302,255),(330,278),(296,298)],[(177,202),(199,206),(204,223),(185,220)]]},
}

def perspective(source, src, dst):
    # Local solver, no external runner/dependency.
    from prepare_a3_frames import solve
    a,b=[],[]
    for (x,y),(u,v) in zip(dst,src):
        a += [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; b += [u,v]
    return source.transform(SIZE,Image.Transform.PERSPECTIVE,solve(a,b),Image.Resampling.BICUBIC)

def extract():
    LIB.mkdir(parents=True,exist_ok=True)
    records=[]
    for name,path in REFS.items():
        im=Image.open(SHARED/path).convert('RGBA')
        for region in REGIONS:
            poly=ref_poly(name,region); region_mask=mask(poly)
            cut(im,poly).save(LIB/f'{name}-{region}.png',optimize=True)
            region_mask.save(LIB/f'{name}-{region}-mask.png',optimize=True)
            records.append({'reference':path,'reference_sha256':sha(SHARED/path),'region':region,'polygon':poly,
                            'bbox':region_mask.getbbox(),'pixels':f'{name}-{region}.png','mask':f'{name}-{region}-mask.png'})
    write(LIB/'regions.json',records)
    write(LIB/'rig-controls.json',{'poses':POSES,'motion_occlusion_clone_patches':CLONES,'canvas':[512,512],'pivot':[256,464]})
    samples={'robe':[271,278,280,293],'stole':[236,276,245,293],'embroidery':[233,349,245,371],
             'cuff':[170,249,185,264],'hem-shadow':[185,392,199,409],'skin':[258,130,273,145],'hair':[242,109,260,118]}
    im=Image.open(SHARED/REFS['idle']).convert('RGB')
    measured={k:{'bbox':v,'median_rgb':[round(x) for x in ImageStat.Stat(im.crop(v)).median]} for k,v in samples.items()}
    write(LIB/'palette.json',{'source':REFS['idle'],'sha256':sha(SHARED/REFS['idle']),'samples':measured})
    swatch=Image.new('RGB',(700,100),(34,40,38)); d=ImageDraw.Draw(swatch)
    for i,(k,v) in enumerate(measured.items()):
        d.rectangle((i*100,25,i*100+95,90),fill=tuple(v['median_rgb'])); d.text((i*100,5),k,fill='white')
    swatch.save(LIB/'palette.png')

def build(index,old):
    p=POSES[index]; ref=Image.open(SHARED/REFS[p['ref']]).convert('RGBA')
    body=cut(ref,ref_poly(p['ref'],'body'))
    for patch in CLONES:
        part=perspective(ref,patch['source'],patch['target']); m=mask(patch['target']).filter(ImageFilter.GaussianBlur(.65))
        a=body.getchannel('A');body.paste(part,(0,0),m);body.putalpha(a)
    s,dx,dy=p['shear'],p['dx'],p['dy']
    # Modest 15% horizontal garment ease accommodates the fixed wide stance.
    # 1.0 vertical scale preserves motif spacing along the stole.
    scale=1.15
    body=body.transform(SIZE,Image.Transform.AFFINE,(1/scale,-s/scale,(s*(dy+250)-dx+245*(scale-1))/scale,0,1,-dy),Image.Resampling.BICUBIC)
    out=old.copy()
    # Old torso twist is retained only above the waist; remove the entire old
    # skirt/hem alpha rather than putting reference rectangles over the fan.
    out.paste((0,0,0,0),(0,270,512,512))
    out.paste((0,0,0,0),(252,105,315,177))
    # Exact untransformed legs behind replacement garment; fixed pivot.
    for poly in p['feet']: out.alpha_composite(cut(old,poly))
    out.alpha_composite(body)
    # Torso twist and arms retain pose-specific A3 paint; costume sleeve ends replaced below.
    for poly in p['arms']: out.alpha_composite(cut(old,poly))
    head=cut(ref,ref_poly(p['ref'],'face-hair')); out.alpha_composite(head,tuple(p['head']))
    for i,dst in enumerate(p['cuffs']):
        region='cuff-left' if i==0 else 'cuff-right'
        delta=-3 if p['ref']=='recover' else 0
        # Four actual cloth corners, not the transparent bounding rectangle.
        src=([(167,236),(197,246),(192,273),(157,266)] if i==0 else [(306,220),(318,229),(325,240),(301,254)])
        src=[(x,y+delta) for x,y in src]
        cuff=perspective(ref,src,dst)
        m=mask(dst).filter(ImageFilter.GaussianBlur(.55))
        out.paste(cuff,(0,0),m)
    # Mace and hand restored last, with every pixel (including alpha) exact.
    protected=Image.new('L',SIZE)
    for poly in p['weapon']: protected=ImageChops.lighter(protected,mask(poly))
    out.paste(old,(0,0),protected)
    # Remove RGB under transparent pixels; retain antialiased reference edges.
    pixels=[(0,0,0,0) if q[3]==0 else q for q in out.getdata()];out.putdata(pixels)
    return out, protected

def palette_distance(im,palette):
    counts=Counter(p[:3] for p in im.getdata() if p[3]>240)
    return round(sum(n*min(math.dist(c,p) for p in palette) for c,n in counts.items())/sum(counts.values()),6)

def main():
    args=argparse.ArgumentParser();args.add_argument('--proof',action='store_true');args.add_argument('--build',action='store_true');a=args.parse_args()
    extract()
    if a.proof:
        old=Image.open(SHARED/'thoma/swing/03.png').convert('RGBA');new,_=build('03',old)
        new.save(OUT/'proof-03.png',optimize=True)
        sheet=Image.new('RGB',(1024,550),(34,40,38));d=ImageDraw.Draw(sheet)
        for i,(label,im) in enumerate([('A3 contact - before',old),('A4 cutout proof - NOT art acceptance',new)]):
            d.text((i*512+10,10),label,fill='white');sheet.paste(im,(i*512,30),im)
        sheet.save(OUT/'proof-before-after.png',optimize=True)
        write(OUT/'proof.json',{'input_sha256':sha(SHARED/'thoma/swing/03.png'),'output_sha256':sha(OUT/'proof-03.png'),'frame':'03','status':'DRAFT','generation_attempts':0})
        print('A4_W1 proof=03 reference_regions=24 generation_attempts=0')
    if a.build:
        baseline=OUT/'baseline-a3';baseline.mkdir(exist_ok=True)
        for i in range(6):
            dest=baseline/f'{i:02}.png'
            if not dest.exists():shutil.copyfile(SHARED/f'thoma/swing/{i:02}.png',dest)
        for src,dest in [(SHARED/REFS['idle'],baseline/'idle-01.png'),(SHARED/'manifest.json',baseline/'manifest.json'),(SHARED/'frame-audit.json',baseline/'frame-audit.json'),(SHARED/'thoma-weapon-style-check.png',OUT/'style-check-a3.png')]:
            if not dest.exists():shutil.copyfile(src,dest)
        write(baseline/'hashes.json',[{'path':p.relative_to(REPO).as_posix(),'sha256':sha(p)} for p in sorted(baseline.iterdir()) if p.name!='hashes.json'])
        allcolors=[]
        for path in REFS.values(): allcolors += [p[:3] for p in Image.open(SHARED/path).convert('RGBA').getdata() if p[3]>240]
        strip=Image.new('RGB',(len(allcolors),1));strip.putdata(allcolors)
        pal=strip.quantize(colors=128).getpalette();pal=[tuple(pal[i:i+3]) for i in range(0,384,3)]
        records=[];(OUT/'protected-masks').mkdir(exist_ok=True)
        for index in POSES:
            old=Image.open(baseline/f'{index}.png').convert('RGBA');im,protected=build(index,old)
            path=SHARED/f'thoma/swing/{index}.png';im.save(path,optimize=True)
            protected.save(OUT/f'protected-masks/{index}.png',optimize=True)
            records.append({'frame':f'thoma/swing/{index}.png','tool':'Pillow reference cutout rig','generation_attempts':0,'prompt':None,'raw':None,
              'references':{path:sha(SHARED/path) for path in REFS.values()},'baseline_sha256':sha(baseline/f'{index}.png'),
              'runtime_sha256':sha(path),'controls':POSES[index],'palette_distance':{'before':palette_distance(old,pal),'after':palette_distance(im,pal),'metric':'mean nearest reference 128-color Euclidean RGB, alpha>240','mapping_applied':False},
              'cleanup':'Reference alpha preserved on cutouts; transformed with bicubic premultiplied RGBA; no silhouette inherited from A2/A3 garment. Transparent RGB cleared. Motion weapon exact.'})
        write(SHARED/'a4-swing-prompts.json',records)
        print('A4_W2 rebuilt=5 generation_attempts=0 references_unchanged=true')

if __name__=='__main__':main()
