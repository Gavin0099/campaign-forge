"""A6 full-frame normalization only; no rig, costume patches or region warps.

Raw candidates are immutable. Uniform scale/translate, low-alpha cleanup and
an optional recorded nearest idle-palette remap are the only output operations.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageStat
import argparse, hashlib, json, math, shutil

REPO = Path(__file__).resolve().parents[2]
SHARED = REPO/'shared-anim'
OUT = REPO/'godot-spike/docs/evidence/spike02-a6'
BASE = OUT/'baseline-a5'
SIZE = (512,512)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def load(path): return json.loads(path.read_text(encoding='utf-8-sig'))

def archive():
    BASE.mkdir(parents=True,exist_ok=True)
    pairs=[(SHARED/f'thoma/swing/{i:02}.png',BASE/f'{i:02}.png') for i in range(6)]
    pairs += [(SHARED/'thoma/idle/01.png',BASE/'idle-01.png')]
    pairs += [(SHARED/n,BASE/n) for n in ['manifest.json','frame-audit.json']]
    for source,dest in pairs:
        if not dest.exists(): shutil.copyfile(source,dest)
    if not (OUT/'style-check-a5.png').exists():
        shutil.copyfile(SHARED/'thoma-weapon-style-check.png',OUT/'style-check-a5.png')
    write(BASE/'hashes.json',[{'path':p.relative_to(REPO).as_posix(),'sha256':sha(p)} for _,p in pairs])

def palette():
    im=Image.open(SHARED/'thoma/idle/01.png').convert('RGBA')
    pixels=[rgb[:3] for rgb in im.getdata() if rgb[3]>240]
    row=Image.new('RGB',(len(pixels),1));row.putdata(pixels)
    return row.quantize(colors=128,method=Image.Quantize.MEDIANCUT)

def distance(im,pal):
    rgb=im.convert('RGB');matched=rgb.quantize(palette=pal,dither=Image.Dither.NONE).convert('RGB')
    values=[math.dist(a,b) for a,b,alpha in zip(rgb.getdata(),matched.getdata(),im.getchannel('A').getdata()) if alpha>240]
    return round(sum(values)/len(values),6)

def normalize(raw, settings, destination):
    im=Image.open(raw).convert('RGBA')
    # All coordinates are manually inspected landmarks on the raw candidate.
    # Only ONE similarity transform acts on the entire figure, including weapon.
    scale=settings['scale']; tx,ty=settings['translate']
    out=im.transform(SIZE,Image.Transform.AFFINE,(1/scale,0,-tx/scale,0,1/scale,-ty/scale),Image.Resampling.BICUBIC)
    before=out.copy(); alpha=out.getchannel('A')
    alpha=alpha.point(lambda a:0 if a<24 else a);out.putalpha(alpha)
    pal=palette(); before_dist=distance(out,pal)
    if settings.get('palette_remap',True):
        rgb=out.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA')
        rgb.putalpha(alpha);out=rgb
    pixels=[(0,0,0,0) if p[3]==0 else p for p in out.getdata()];out.putdata(pixels)
    destination.parent.mkdir(parents=True,exist_ok=True);out.save(destination,optimize=True)
    diff=ImageChops.difference(before,out)
    mask=Image.new('L',SIZE);mask.putdata([255 if any(p) else 0 for p in diff.getdata()])
    mask_path=destination.with_name(destination.stem+'-cleanup-mask.png');mask.save(mask_path)
    return {'raw_sha256':sha(raw),'normalized_sha256':sha(destination),
            'settings':settings,'palette_distance':{'before':before_dist,'after':distance(out,pal),
                'metric':'mean nearest idle/01 128-color Euclidean RGB, alpha>240'},
            'cleanup_mask':mask_path.relative_to(REPO).as_posix(),'cleanup_mask_sha256':sha(mask_path),
            'operations':'single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing',
            'runtime_sha256':None,'adopted':False}

def proof(candidate):
    paths=[SHARED/'thoma/swing/02.png',candidate,SHARED/'thoma/idle/01.png',SHARED/'thoma/swing/05.png']
    labels=['A5 swing/02','A6 best proof (not live)','idle/01 immutable','swing/05 immutable']
    sheet=Image.new('RGB',(2080,1350),(34,40,38));d=ImageDraw.Draw(sheet)
    d.text((10,8),'A6 W1: equal 512px canvases, source-pixel crops; NOT runtime screenshots or Owner approval',fill='white')
    regions={'stole':(175,145,335,395),'embroidery':(175,305,335,395),'cuffs/sleeves':(155,145,395,285),
             'hem':(100,345,420,440),'legs/shoes':(95,395,425,470),'face/hair':(215,85,335,195),'mace':(150,60,485,350)}
    boxes={}
    for col,(path,label) in enumerate(zip(paths,labels)):
        im=Image.open(path).convert('RGBA');x=col*520
        d.text((x+8,30),label,fill='white');sheet.paste(im,(x,50),im)
        y=570;boxes[label]={}
        for name,box in regions.items():
            crop=im.crop(box)
            # Two columns below each whole-frame panel, no region rescaling.
            if name in ['stole','embroidery','face/hair']: px=x+8; py={'stole':600,'embroidery':860,'face/hair':970}[name]
            else: px=x+180;py={'cuffs/sleeves':600,'hem':760,'legs/shoes':875,'mace':990}[name]
            # Mace crop is wide; uses full panel width lower down.
            if name=='mace':px=x+8;py=1100;crop=im.crop((145,60,490,285));box=(145,60,490,285)
            d.text((px,py-14),name,fill='#d2b777');sheet.paste(crop,(px,py),crop);boxes[label][name]=box
    sheet.save(OUT/'proof-02.png',optimize=True);write(OUT/'proof-crops.json',boxes)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',action='store_true');p.add_argument('--frame');p.add_argument('--attempt',type=int,default=1)
    p.add_argument('--scale',type=float);p.add_argument('--tx',type=float,default=0);p.add_argument('--ty',type=float,default=0);p.add_argument('--proof',action='store_true')
    args=p.parse_args()
    if args.archive:archive()
    if args.frame:
        raw=OUT/f'candidates/{args.frame}/attempt-{args.attempt}.png';dest=OUT/f'normalized/{args.frame}-attempt-{args.attempt}.png'
        result=normalize(raw,{'scale':args.scale,'translate':[args.tx,args.ty],'palette_remap':True},dest)
        write(dest.with_suffix('.json'),result)
        if args.proof:proof(dest)
        print(json.dumps(result))
