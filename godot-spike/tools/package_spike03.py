"""Offline evidence layout only. Never reads or writes animation source PNGs."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / 'docs/evidence/spike03'

def package(name):
    folder = ROOT / name
    data = json.loads((folder / 'timeline.json').read_text(encoding='utf-8'))
    contact = data['contact_row']
    strip = Image.new('RGB', (5 * 320, 4 * 202), '#101a19')
    draw = ImageDraw.Draw(strip)
    for n, row in enumerate(data['frames'][contact-8:contact+9]):
        im = Image.open(folder / row['png']).convert('RGB')
        im.thumbnail((320,180))
        x, y = n % 5 * 320, n // 5 * 202
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
    return data

if __name__ == '__main__':
    for name in ['before','after','after-crit']:
        if (ROOT/name/'timeline.json').exists(): package(name)
