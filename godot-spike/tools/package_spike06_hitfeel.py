"""Offline layouts from native runtime PNGs. No game/source art modification."""
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / 'docs/evidence/spike06/hitfeel'

def main():
    strips = []
    for name in ('spike05-normal', 'spike06-normal', 'spike05-crit', 'spike06-crit'):
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
        shutil.copyfile(PROJECT/'.godot'/('spike06-'+name)/'attack.avi',folder/'attack-60fps.avi')
        strips.append(strip)
    stacked = Image.new('RGB',(1600,sum(s.height for s in strips)),'#101a19')
    y = 0
    for strip in strips:
        stacked.paste(strip,(0,y))
        y += strip.height
    stacked.save(OUT/'impact-strip-spike05-vs-spike06.png')
    timing = json.loads((OUT/'timing.json').read_text(encoding='utf-8'))
    assert timing['pass'] and len(timing['runs'])==9
    runtime = json.loads((OUT/'timing-runtime.json').read_text(encoding='utf-8'))
    assert runtime['pass'] and len(runtime['runs']) == 9
    assert all(r['wall_seconds'] <= 1.7 for r in runtime['runs'])
    timing['runtime_runs'] = runtime['runs']
    timing['wall_note'] = 'Fixed60 run uses a simulation clock; wall normal/crit exceeded1.7s even alone on this PC. Independent uncaptured real-time run verifies gameplay wall duration.'
    (OUT/'timing.json').write_text(json.dumps(timing,indent=2)+'\n',encoding='utf-8')
    print('SPIKE06_HITFEEL pass=true four AVIs, four native contact stills, contact +/-8 strips, nine timing runs')

if __name__ == '__main__':
    main()
