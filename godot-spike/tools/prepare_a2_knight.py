"""Consistent offline knight-B identity edit, requested scripted approach.
Reconstruct from immutable knight-A frames, so repeated runs never layer edits.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,random
root=Path(__file__).resolve().parents[2]/'shared-anim'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Manual shield ellipse and helmet crest attachment coordinates for each pose.
poses={'idle/00.png':(371,272,28,43,298,109), 'hit/00.png':(319,244,33,50,330,107),
 'hit/01.png':(276,229,30,52,353,117), 'hit/02.png':(313,270,30,44,211,108),
 'stagger/00.png':(204,219,25,51,311,137), 'stagger/01.png':(335,296,30,46,192,160),
 'stagger/02.png':(364,275,28,47,243,137)}
audit=json.loads((root/'frame-audit.json').read_text(encoding='utf-8'))
audit=[r for r in audit if not r['path'].startswith('knight-b/')]
entries=[]
for p,(cx,cy,rx,ry,hx,hy) in poses.items():
 source=root/'knight-a'/p;im=Image.open(source).convert('RGBA');pixels=[]
 for i,(r,g,b,a) in enumerate(im.getdata()):
  x,y=i%512,i//512
  if a>0 and ((x-cx)/rx)**2+((y-cy)/ry)**2<1 and (x-cx)**2+(y-cy)**2>150:
   v=min(232,round(135+(r+g+b)/3*.5));r,g,b=v,v-5,v-20
  pixels.append((r,g,b,a))
 im.putdata(pixels)
 # Short horsehair crest, broad hooked silhouette; muted bone with worn dark roots.
 crest=Image.new('RGBA',(512,512));d=ImageDraw.Draw(crest)
 outline=[(hx-8,hy+7),(hx-13,hy-12),(hx-9,hy-32),(hx+2,hy-45),(hx+17,hy-45),(hx+30,hy-32),(hx+37,hy-9),(hx+25,hy-14),(hx+14,hy-29),(hx+5,hy-28),(hx+4,hy+7)]
 d.polygon(outline,fill='#c8bea4',outline='#3c3b33')
 mask=crest.getchannel('A');rgen=random.Random(23)
 for _ in range(260):
  x,y=rgen.randrange(hx-13,hx+38),rgen.randrange(hy-45,hy+8)
  if mask.getpixel((x,y)):
   d.line((x,y,x+1,y+2),fill=rgen.choice(['#a99c80','#ded4bb','#867c65']),width=1)
 crest.putalpha(mask)
 im.alpha_composite(crest)
 target=root/'knight-b'/p;im.save(target,optimize=True)
 rec=dict(path='knight-b/'+p,source='knight-a/'+p,source_sha256=sha(source),sha256=sha(target),status='SOURCE_DERIVED',tool='Python/Pillow deterministic scripted edit',attempt=1,cleanup='bone shield remap and textured short crest; fixed canvas/pivot, no body geometry changes',helmet_anchor=[hx,hy],shield_mask=[cx,cy,rx,ry],palette='existing bone/brass/moss; no Ferry Dusk',prompt='Scripted edit, no generative prompt: retain knight-A body pixels; remap shield field to bone and attach the same textured short bone crest to manually registered helmet top.')
 audit.append(rec);entries.append(rec)
(root/'frame-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(root/'knight-a2-edits.json').write_text(json.dumps(entries,indent=2)+'\n')
text=(root/'SOURCES.md').read_text(encoding='utf-8').split('\n## A2 knight B')[0]
text+='\n## A2 knight B\n\nScripted edit preferred by the brief, one pass per frame, no image generation. Reproducible script: godot-spike/tools/prepare_a2_knight.py. Identical short bone horsehair crest and light shield field across idle/hit/stagger. Original atlases and knight A unchanged. Detailed anchors, input/output SHA-256 and exact edit instruction: knight-a2-edits.json. Model inspection is not Owner art approval.\n\n| Frame | Input SHA-256 | Output SHA-256 |\n| --- | --- | --- |\n'
for e in entries:text+=f"| {e['path']} | `{e['source_sha256']}` | `{e['sha256']}` |\n"
(root/'SOURCES.md').write_text(text,encoding='utf-8')
# Refresh contact sheet only; never rerun historical Phase A cleanup.
m=json.loads((root/'manifest.json').read_text());sheet=Image.new('RGB',(2048,900),(34,40,38));d=ImageDraw.Draw(sheet)
for row,c in enumerate(m['characters']):
 paths=[f['path'] for seq in m['sequences'].values() if seq['character']==c for f in seq['frames']]
 for col,p in enumerate(paths):
  im=Image.open(root/p).resize((256,256),Image.Resampling.LANCZOS);sheet.paste(im,(col*256,row*300+30),im);d.text((col*256+5,row*300+8),p,fill='#eee7d6')
sheet.save(root/'contact-sheet.png',optimize=True)
print('KNIGHT_B_EDIT frames=7 identity=bone-crest-and-shield')
