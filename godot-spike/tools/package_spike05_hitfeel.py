"""Offline layouts from native runtime PNGs. No game/source art modification."""
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / 'docs/evidence/spike05/hitfeel'

def main():
    strips = []
    for name in ('spike04-normal', 'spike05-normal', 'spike04-crit', 'spike05-crit'):
        folder = OUT / name
        data = json.loads((folder/'timeline.json').read_text(encoding='utf-8'))
        assert data['pass'] and data['resolution'] == [1280,720]
        contact = data['contact_row']
        strip = Image.new('RGB',(5*320,4*342),'#101a19')
        draw = ImageDraw.Draw(strip)
        for n,row in enumerate(data['frames'][contact-8:contact+9]):
            im = Image.open(folder/row['png']).convert('RGB')
            assert im.size == (1280,720)
            x,y = n%5*320,n//5*342
            strip.paste(im.crop((260,150,580,470)),(x,y+22))
            draw.text((x+4,y+4),f'{name} contact {n-8:+d}f {row["phase"]}',fill='#eee7d6')
        strip.save(folder/'impact-strip.png')
        Image.open(folder/data['frames'][contact]['png']).save(folder/'contact.png')
        shutil.copyfile(PROJECT/'.godot'/('spike05-'+name)/'attack.avi',folder/'attack-60fps.avi')
        strips.append(strip)
    stacked = Image.new('RGB',(1600,sum(s.height for s in strips)),'#101a19')
    y = 0
    for strip in strips:
        stacked.paste(strip,(0,y))
        y += strip.height
    stacked.save(OUT/'impact-strip-spike04-vs-spike05.png')
    timing = json.loads((OUT/'timing.json').read_text(encoding='utf-8'))
    assert timing['pass'] and len(timing['runs'])==9
    print('SPIKE05_HITFEEL pass=true four AVIs, four native contact stills, contact +/-8 strips, nine timing runs')

if __name__ == '__main__':
    main()
