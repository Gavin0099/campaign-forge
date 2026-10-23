"""Original deterministic nine-slice frame, no generated or third-party artwork."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, random
root=Path(__file__).resolve().parents[1]
out=root/'art/ui';out.mkdir(exist_ok=True)
im=Image.new('RGB',(64,64),'#1b2421');d=ImageDraw.Draw(im)
d.rectangle((0,0,63,63),outline='#776746',width=2)
d.line((2,61,2,2,61,2),fill='#d2b777',width=1)
d.rectangle((4,4,59,59),outline='#101a19',width=2)
r=random.Random(22023)
for _ in range(100):
 x,y=r.randrange(64),r.choice([1,2,3,60,61,62]);d.point((x,y),fill=r.choice(['#776746','#9a895d','#d2b777']))
for x,y in [(7,7),(56,7),(7,56),(56,56)]:
 d.line((x-3,y,x+3,y),fill='#d2b777');d.line((x,y-3,x,y+3),fill='#d2b777')
im.save(out/'field-frame.png')
def luminance(hex):
 rgb=[int(hex[i:i+2],16)/255 for i in (0,2,4)]
 return sum(c*k for c,k in zip([v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb],[.2126,.7152,.0722]))
rows=[]
for role,fg in [('primary','eee7d6'),('secondary','b9bbab'),('heading/action','d2b777'),('ally','98c9be'),('enemy','dd9c7e'),('disabled','b9bbab')]:
 for bg in ['1b2421','30372c','101a19']:
  a,b=sorted([luminance(fg),luminance(bg)]);ratio=(b+.05)/(a+.05)
  rows.append(dict(role=role,foreground='#'+fg,background='#'+bg,ratio=round(ratio,3),normal_AA=ratio>=4.5,large_AA=ratio>=3))
folder=root/'docs/evidence/spike02-a2';folder.mkdir(parents=True,exist_ok=True)
(folder/'contrast.json').write_text(json.dumps({'method':'WCAG relative sRGB luminance; all HUD labels backed by opaque panel colors; world numbers use opaque dark backplate. No alpha text colors. CJK normal text >=16px.','pairs':rows,'all_normal_AA':all(r['normal_AA'] for r in rows)},indent=2)+'\n')
print('UI_ASSET sha256='+hashlib.sha256((out/'field-frame.png').read_bytes()).hexdigest()+' min_text_contrast='+str(min(r['ratio'] for r in rows)))
