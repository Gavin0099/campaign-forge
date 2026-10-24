"""Offline evidence layout only. Never reads or writes animation source PNGs."""
import json
import hashlib
import shutil
import struct
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / 'docs/evidence/spike03'

def chunks(raw, start, end):
    while start+8 <= end:
        key = raw[start:start+4]
        length = struct.unpack_from('<I',raw,start+4)[0]
        if key in (b'RIFF',b'LIST'):
            yield from chunks(raw,start+12,min(end,start+8+length))
        else:
            yield key,raw[start+8:start+8+length]
        start += 8+length+(length % 2)

def package(name):
    folder = ROOT / name
    data = json.loads((folder / 'timeline.json').read_text(encoding='utf-8'))
    contact = data['contact_row']
    strip = Image.new('RGB', (5 * 320, 4 * 342), '#101a19')
    draw = ImageDraw.Draw(strip)
    for n, row in enumerate(data['frames'][contact-8:contact+9]):
        im = Image.open(folder / row['png']).convert('RGB').crop((260,150,580,470))
        x, y = n % 5 * 320, n // 5 * 342
        strip.paste(im,(x,y+22))
        draw.text((x+5,y+4), f"{name} F{row['process_frame']} ({row['ms_from_strike']:.0f}ms) {row['phase']}", fill='#eee7d6')
    strip.save(folder / 'impact-strip.png')
    lines = [f'# {name} — actual 60 FPS post-draw timeline', '',
             'Every frame from contact −8 (includes required −6) through input-ready has its native PNG in `frames/`.',
             'All strike frames are in JSON. Times below are process frames / 60. Wall times include readback cost.',
             data['particle_note'], '',
             '| F | ms | phase / swing | pause | offset | zoom | flash | target Δ | number scale | emitter capacity | SFX |',
             '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in data['frames']:
        lines.append(f"| {r['process_frame']} | {r['ms_from_strike']:.1f} | {r['phase']} / {r['swing_frame_index']} | {r['paused']} | {r['camera_offset']} | {r['camera_zoom']} | {r['target_flash']:.3f} | {r['target_delta']} | {[n['scale'] for n in r['damage_numbers']]} | {r['live_particle_count_upper_bound']} | {r['sfx_triggers']} |")
    (folder / 'timeline.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    hit = data['frames'][contact]
    Image.open(folder/hit['png']).save(folder/'contact.png')
    movie = ROOT.parents[2] / '.godot' / ('spike03-'+name) / 'attack.avi'
    if movie.exists():
        shutil.copyfile(movie,folder/'attack-60fps.avi')
        raw = movie.read_bytes()
        frames = [Image.open(BytesIO(value)).convert('RGB') for key,value in chunks(raw,12,len(raw)) if key in (b'00dc',b'00db')]
        assert all(im.size == (1280,720) for im in frames)
        (folder/'movie-index.json').write_text(json.dumps({'fps':60,'frames':len(frames),'bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest(),'timeline_run':data['runs'][0]},indent=2)+'\n',encoding='utf-8')
    return data

def comparisons():
    a, b = [Image.open(ROOT/name/'impact-strip.png').convert('RGB') for name in ('before','after')]
    out = Image.new('RGB',(a.width,a.height+b.height),'#101a19')
    out.paste(a,(0,0)); out.paste(b,(0,a.height))
    out.save(ROOT/'impact-strip-before-vs-after.png')
    frames = []
    data = [json.loads((ROOT/n/'timeline.json').read_text(encoding='utf-8')) for n in ('before','after')]
    # Contact-aligned, 30 FPS, native readbacks resized only for review GIF.
    # Last available ready frame is held when the shorter sequence has ended.
    start = -8
    stop = max(len(d['frames'])-d['contact_row'] for d in data)
    for i in range(start,stop,2):
        canvas = Image.new('RGB',(720,382),'#101a19')
        draw = ImageDraw.Draw(canvas)
        for col,name in enumerate(('before','after')):
            d = data[col]
            row = d['frames'][min(d['contact_row']+i,len(d['frames'])-1)]
            im = Image.open(ROOT/name/row['png']).convert('RGB').crop((260,150,620,510))
            canvas.paste(im,(360*col,22))
            draw.text((360*col+8,5),f'{name} contact {i:+d}f; {row["phase"]}',fill='#eee7d6')
        frames.append(canvas)
    frames[0].save(ROOT/'before-vs-after.gif',save_all=True,append_images=frames[1:],duration=round(1000/30),loop=0,optimize=True)
    for name,filename in [('after','contact.png'),('after-crit','contact-crit.png')]:
        shutil.copyfile(ROOT/name/'contact.png',ROOT/filename)
    d = data[1]
    row = next(r for r in d['frames'][d['contact_row']:] if not r['hitstop'] and r['damage_numbers'])
    shutil.copyfile(ROOT/'after'/row['png'],ROOT/'number-pop.png')

def archive_trials():
    # Keep the rejected contact + complete AVI/timeline. Intermediate full PNGs
    # are local scratch, while final before/after keep every required native PNG.
    for name in ('after','after-crit'):
        trial = ROOT/'pre-number-placement'/name
        if not (trial/'frames').exists(): continue
        data = json.loads((trial/'timeline.json').read_text(encoding='utf-8'))
        Image.open(trial/data['frames'][data['contact_row']]['png']).save(trial/'contact.png')
        destination = ROOT.parents[2]/'.godot'/'spike03-rejected-number-placement'/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        assert trial.resolve().is_relative_to(ROOT.resolve())
        assert destination.resolve().is_relative_to(ROOT.parents[2].resolve())
        assert not destination.exists()
        shutil.move(str(trial/'frames'),str(destination))
    trial_root = ROOT/'pre-number-placement'
    if trial_root.exists():
        (trial_root/'README.md').write_text('# Rejected damage-number placement\n\n'
            'First W3 render: the 28/34 px punched number on a dark backing covered the hit. '
            'Final config moves it from −88 to −112 world px and removes the tuned backing. '
            'These original contact PNGs, complete 60 FPS AVIs, raw timelines and logs retain the trial. '
            'Its per-frame PNGs are local .godot scratch only; their paths in these raw timelines are historical, '
            'not links to delivered files. All required final per-frame PNGs are in ../../before, ../../after and ../../after-crit.\n',encoding='utf-8')

if __name__ == '__main__':
    archive_trials()
    for name in ['before','after','after-crit']:
        if (ROOT/name/'timeline.json').exists(): package(name)
    if all((ROOT/n/'timeline.json').exists() for n in ('before','after','after-crit')):
        comparisons()
