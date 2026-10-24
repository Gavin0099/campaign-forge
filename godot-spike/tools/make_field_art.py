"""Original deterministic PLACEHOLDER terrain/props, no downloads or figure edits."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'art/bigmap'
OUT.mkdir(parents=True,exist_ok=True)
rng = random.Random(24018)
palette = {'plain':(91,85,64),'road':(135,116,82),'forest':(64,74,50),
           'ford':(78,99,94),'water':(40,61,64),'cliff':(58,59,54),'defense':(115,106,77)}
for name,color in palette.items():
    # Our existing original painting supplies brush texture only, never terrain.
    patch = Image.open(ROOT/'art/battlefield.png').convert('RGB').crop((310,180,390,235)).resize((160,96),Image.Resampling.LANCZOS)
    im = Image.blend(patch,Image.new('RGB',(160,96),color),.68).convert('RGBA')
    d = ImageDraw.Draw(im)
    diamond = [(80,0),(159,48),(80,95),(0,48)]
    for _ in range(100):
        x,y=rng.randrange(160),rng.randrange(96)
        if abs(x-80)/80+abs(y-48)/48>0.96: continue
        v=rng.randint(-9,9)
        c=tuple(max(0,min(255,k+v)) for k in color)+(255,)
        d.line((x,y,x+rng.randrange(2,8),y+rng.randrange(-1,2)),fill=c,width=rng.choice([1,1,2]))
    im = im.filter(ImageFilter.GaussianBlur(.5))
    mask = Image.new('L',(160,96))
    ImageDraw.Draw(mask).polygon(diamond,fill=255)
    im.putalpha(mask)
    im.save(OUT/(name+'.png'))

# Small painted brush chunks: bank stones and worn crossing ruts. Decorative only.
for name in ('bank','crossing'):
    im=Image.new('RGBA',(320,160))
    d=ImageDraw.Draw(im)
    for i in range(95):
        x,y=rng.randrange(320),rng.randrange(35,125)
        r=rng.randrange(3,13)
        c=rng.choice([(110,103,79,130),(65,65,54,150),(162,143,103,90)])
        if name=='crossing': y=70+(x%21)//3+rng.randrange(12)
        d.ellipse((x,y,x+r*2,y+r),fill=c)
    im.filter(ImageFilter.GaussianBlur(.5)).save(OUT/(name+'.png'))

for name in ('tree','rock','banner'):
    im=Image.new('RGBA',(160,210))
    d=ImageDraw.Draw(im)
    if name=='tree':
        d.polygon([(70,195),(82,191),(91,76),(77,66)],fill='#403c2d')
        for i in range(65):
            y=rng.randrange(15,155)
            spread=int((y+25)*.4)
            x=80+rng.randrange(-spread,spread+1)
            r=rng.randrange(8,22)
            d.polygon([(x,y-r),(x+r,y+r),(x-r,y+r//2)],fill=rng.choice(['#424d32','#56603c','#66704b','#343f2c','#727452']))
    elif name=='rock':
        d.polygon([(25,190),(33,161),(72,140),(120,158),(140,187),(90,202)],fill='#55564b')
        d.polygon([(33,161),(72,140),(120,158),(86,176)],fill='#8a8973')
        d.line([(72,142),(86,176),(90,200)],fill='#b0a68a',width=2)
    else:
        d.line((65,198,65,18),fill='#b6a47b',width=4)
        d.polygon([(68,23),(135,35),(115,65),(134,94),(68,78)],fill='#73483c')
        d.line((72,28,122,39),fill='#c1a66c',width=3)
        d.ellipse((61,12,70,22),fill='#d0b67b')
    im.save(OUT/(name+'.png'))
print('FIELD_ART: seven diamond textures, two painted brush chunks, three props; PLACEHOLDER')
