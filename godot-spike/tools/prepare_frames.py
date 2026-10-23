"""Reproducible offline cleanup; never modifies source atlases or raw outputs.
Manual registration points were selected from the raw contact sheets. Palette
quantization uses the original character crop, with no new battlefield grading.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, json, math

ROOT = Path(__file__).resolve().parents[2] / 'shared-anim'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cleaned(im):
    im=im.convert('RGBA'); a=im.getchannel('A')
    # Remove almost-transparent generated debris, retain antialiasing above 24.
    a=a.point(lambda v: 0 if v<24 else v)
    im.putalpha(a)
    return im
def palette_for(ref):
    pixels=[p[:3] for p in ref.getdata() if p[3]>200]
    strip=Image.new('RGB',(len(pixels),1)); strip.putdata(pixels)
    return strip.quantize(colors=128,method=Image.Quantize.MEDIANCUT)
def match_palette(im,pal):
    a=im.getchannel('A'); rgb=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(a)
    return rgb
def register(im,foot_x,ground_y,head_y,height=360):
    scale=height/(ground_y-head_y)
    resized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(512,512))
    out.alpha_composite(resized,(round(256-foot_x*scale),round(464-ground_y*scale)))
    return out
def save(im,rel):
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p,optimize=True)
    return dict(path=rel,sha256=sha(p))
refs={c:cleaned(Image.open(ROOT/f'references/{c}.png')) for c in ['thoma','knight-a']}
pals={c:palette_for(im) for c,im in refs.items()}
records=[]
for c,im in refs.items():
    record=save(register(im,im.width/2,im.height,0),f'{c}/idle/00.png')
    record.update(source=f'references/{c}.png',cleanup='original crop uniformly scaled, alpha debris threshold 24, fixed pivot',status='SOURCE_DERIVED')
    records.append(record)
# x ground, y ground, head y, pose body height. Lower crouched poses retain
# their intended compression rather than being auto-stretched back upright.
registration={
 'thoma-swing-00':(690,1196,150,360),
 'thoma-swing-01':(735,1216,302,320),
 'thoma-swing-02':(615,1177,163,348),
 'thoma-swing-03':(550,1192,78,360),
 'thoma-swing-04':(635,1200,85,352),
 'thoma-swing-05':(640,1221,35,360),
 'knight-a-hit-00':(775,1206,68,360),
 'knight-a-hit-01':(775,1168,70,350),
 'knight-a-hit-02':(795,1221,33,360),
 'knight-a-stagger-00':(785,1138,151,332),
 'knight-a-stagger-01':(795,1149,136,310),
 'knight-a-stagger-02':(795,1147,128,335),
}
prompts=json.loads((ROOT/'generation-prompts.json').read_text())+json.loads((ROOT/'knight-generation-prompts.json').read_text())
for entry in prompts:
    p=ROOT/entry['output'];stem=p.stem
    c='thoma' if stem.startswith('thoma') else 'knight-a'
    seq,n=stem.removeprefix(c+'-').rsplit('-',1)
    im=cleaned(Image.open(p));im=register(im,*registration[stem]);im=match_palette(im,pals[c])
    record=save(im,f'{c}/{seq}/{n}.png')
    record.update(source=entry['output'],raw_sha256=sha(p),registration=registration[stem],status='PLACEHOLDER' if c=='thoma' else 'CANDIDATE',reason='weapon absent in original Thoma crop; generated sleeve/hem detail differs' if c=='thoma' else 'automated palette match; Owner art review pending')
    records.append(record)
# Deterministic variant: recolor only mauve cloth/paint pixels to a light bone
# value while preserving local texture and alpha. Same transform on every pose.
shield_masks={'idle/00.png':(371,272,28,43), 'hit/00.png':(319,244,33,50),
 'hit/01.png':(276,229,30,52), 'hit/02.png':(313,270,30,44),
 'stagger/00.png':(204,219,25,51), 'stagger/01.png':(335,296,30,46),
 'stagger/02.png':(364,275,28,47)}
for rec in list(records):
    if not rec['path'].startswith('knight-a/'):continue
    im=Image.open(ROOT/rec['path']).convert('RGBA'); px=[]; count=0
    cx,cy,rx,ry=shield_masks[rec['path'].removeprefix('knight-a/')]
    for idx,(r,g,b,a) in enumerate(im.getdata()):
        x,y=idx%512,idx//512
        radius=((x-cx)/rx)**2+((y-cy)/ry)**2
        mauve=a>0 and radius<1 and ((x-cx)**2+(y-cy)**2)>150
        if mauve:
            v=round((r+g+b)/3);v=min(224,round(120+v*.55));px.append((v,min(255,v-5),max(0,v-20),a));count+=1
        else:px.append((r,g,b,a))
    im.putdata(px)
    variant=save(im,rec['path'].replace('knight-a/','knight-b/'))
    variant.update(source=rec['path'],status='SOURCE_DERIVED',cleanup='manual shield-field ellipse mask, bone value remap; preserve alpha, texture, armor, boss and pivot',recolored_pixels=count)
    records.append(variant)

# Contact sheet in sequence order with original crops alongside idle.
m=json.loads((ROOT/'manifest.json').read_text())
rows=[]
for c in m['characters']:
    items=[(f'{c} ORIGINAL',refs['knight-a' if c=='knight-b' else c])]
    for key,seq in m['sequences'].items():
        if seq['character']==c:
            items += [(f['path'],Image.open(ROOT/f['path'])) for f in seq['frames']]
    rows.append(items)
sheet=Image.new('RGB',(240*8,285*3),(34,40,38));d=ImageDraw.Draw(sheet)
for row,items in enumerate(rows):
    for col,(label,im) in enumerate(items):
        pos=(col*240,row*285);im=im.copy();im.thumbnail((230,245))
        sheet.paste(im,(pos[0]+5,pos[1]+25),im)
        d.text((pos[0]+5,pos[1]+5),label,fill=(238,231,214))
        if 'ORIGINAL' not in label:
            x=pos[0]+5+256*im.width/512;y=pos[1]+25+464*im.height/512
            d.line((x-5,y,x+5,y),fill=(245,100,75),width=1);d.line((x,y-5,x,y+5),fill=(245,100,75),width=1)
sheet.save(ROOT/'contact-sheet.png',optimize=True)
(ROOT/'frame-audit.json').write_text(json.dumps(records,indent=2)+'\n')
text=['# Animation sources — spike 02 Phase A','',
 'Original atlases remain unchanged. All generated frames: built-in `image_gen`, one attempt per frame. No rejected attempt. No commercial art or Ferry Dusk grading.',
 '','## Original reference crops','',
 '| Reference | Original | SHA-256 |','| --- | --- | --- |']
for name,source in [('thoma','godot-spike/art/l03-party-v1.png rect(1558,0,520,711)'),('sword-reference','godot-spike/art/l03-party-v1.png rect(175,0,475,711)'),('knight-a','godot-spike/art/l03-enemies-v1.png rect(15,8,745,863)')]:
    text.append(f'| references/{name}.png | {source} | `{sha(ROOT/f"references/{name}.png")}` |')
text+=['','## Full generation prompts and raw outputs','']
for e in prompts:
    text += [f'### {e["output"]}',f'Tool: {e["tool"]}; attempt {e["attempt"]}/3. References: '+', '.join(e['references']),f'Raw SHA-256: `{sha(ROOT/e["output"])}`','',e['prompt'],'']
text+=['## Cleanup and runtime frames','',
 'Tool: Python 3.12 / Pillow 12.2, `godot-spike/tools/prepare_frames.py`. Per-frame manual registration coordinates are in frame-audit.json. Clear alpha below 24; Lanczos resize to fixed 512px canvas and [256,464] pivot; map generated RGB to 128 colors sampled from its original crop. This removes stray colored edge pixels. Original idles are scaled source crops. Knight B uses manually located shield-field ellipse masks and the same texture-preserving bone-value remap across all seven frames. Armor and shield boss are excluded. No geometric redraw of armor or source originals.',
 '','PLACEHOLDER: all six Thoma swing frames have an equipment-reference gap (the specified original crop is empty-handed), and generated hems/sleeves have small deviations. They are functional motion candidates, not exact costume/weapon approval. Knight frames are candidates with head/armor contour variation; same source palette is measurable, exact stroke identity is not proven. No claim of commercial or Owner art acceptance.',
 '','| Runtime frame | Status | Input | Output SHA-256 |','| --- | --- | --- | --- |']
for r in records:text.append(f'| {r["path"]} | {r["status"]} | {r["source"]} | `{r["sha256"]}` |')
text+=['',f'Contact sheet: `contact-sheet.png`, SHA-256 `{sha(ROOT/"contact-sheet.png")}`. Generated by Pillow from every runtime frame plus original crops; red crosses mark pivots. It is an asset review sheet, not a game screenshot.']
(ROOT/'SOURCES.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
print(f'Prepared {len(records)} runtime frames; originals unchanged.')
