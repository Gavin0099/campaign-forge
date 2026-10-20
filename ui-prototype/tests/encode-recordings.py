"""Encode actual Chromium screencast frames. Never modifies generated artwork."""
from pathlib import Path
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parents[2]
output = root / 'ui-prototype/screenshots/vd2/after'
for width in (1280, 1920):
    manifest_path = output / f'recording-{width}.json'
    manifest = json.loads(manifest_path.read_text())
    records = manifest['frames']
    assert len(records) > 40
    frames = []
    durations = []
    for i, record in enumerate(records):
        source = root / f'scratch/vd2-browser/frames-{width}' / record['file']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256']
        frame = Image.open(source).convert('RGB')
        assert frame.size == (width, manifest['viewport']['height'])
        frames.append(frame)
        delta = records[i+1]['timestamp']-record['timestamp'] if i+1 < len(records) else .3
        durations.append(max(20, round(delta*100)*10))
    # Shared palette samples the complete capture, including both live spells.
    strip = Image.new('RGB', (256, 144*len(frames[::8])))
    for i, frame in enumerate(frames[::8]):
        thumb = frame.copy(); thumb.thumbnail((256,144)); strip.paste(thumb,(0,i*144))
    palette = strip.quantize(colors=256)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    target = output / f'combat-live-{width}.gif'
    indexed[0].save(target,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=1)
    manifest['gif'] = dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size,duration_ms=sum(durations),encoder='Pillow; actual captured frames only, timestamp-based durations, shared palette; no synthetic frames')
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    # Review-only contact sheet of real captures, not a generated battle movie.
    sheet = Image.new('RGB',(640*3,360*3))
    for i in range(9):
        frame=frames[min(len(frames)-1,round(i*(len(frames)-1)/8))].copy()
        frame.thumbnail((640,360));sheet.paste(frame,((i%3)*640,(i//3)*360))
    sheet.save(root / f'scratch/vd2-browser/contact-{width}.jpg')
    print(json.dumps(dict(frames=len(frames),**manifest['gif'])))
