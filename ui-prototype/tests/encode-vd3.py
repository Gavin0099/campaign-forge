"""Encode live CDP captures only. Generated artwork is never modified."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
output = root / 'ui-prototype/screenshots/vd3'
for width in (1280, 1920):
    for kind in ('melee', 'missile'):
        key = f'{kind}-{width}'
        manifest_path = output / f'recording-{key}.json'
        manifest = json.loads(manifest_path.read_text())
        records = manifest['frames']
        frame_directory = (root / manifest['capture_directory']).resolve()
        assert frame_directory.is_relative_to(root / 'scratch/vd3-browser')
        assert len(records) > 30
        frames, durations = [], []
        for i, record in enumerate(records):
            assert Path(record['file']).name == record['file']
            source = frame_directory / record['file']
            assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256']
            with Image.open(source) as image:
                assert image.size == (width, manifest['viewport']['height'])
                frames.append(image.convert('RGB'))
            delta = records[i+1]['timestamp']-record['timestamp'] if i+1 < len(records) else .3
            durations.append(max(10, round(delta*100)*10))
        strip = Image.new('RGB', (256, 144*len(frames[::8])))
        for i, frame in enumerate(frames[::8]):
            thumb = frame.copy()
            thumb.thumbnail((256, 144))
            strip.paste(thumb, (0, i*144))
        palette = strip.quantize(colors=256)
        indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
        target = output / f'{key}.gif'
        indexed[0].save(target, save_all=True, append_images=indexed[1:], duration=durations,
                        loop=0, optimize=True, disposal=1)
        with Image.open(target) as encoded:
            actual_duration = sum(encoded.seek(i) or encoded.info['duration'] for i in range(encoded.n_frames))
            assert actual_duration == sum(durations)
        manifest['gif'] = dict(file=target.name, sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                               bytes=target.stat().st_size, duration_ms=actual_duration,
                               encoder='Pillow; actual live frames only; timestamp durations and shared palette; silent GIF; no synthetic frames')
        manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
        sheet = Image.new('RGB', (640*3, 384*3), '#162225')
        draw = ImageDraw.Draw(sheet)
        for i in range(9):
            index = min(len(frames)-1, round(i*(len(frames)-1)/8))
            frame = frames[index].copy()
            frame.thumbnail((640, 360))
            x, y = (i % 3)*640, (i // 3)*384
            sheet.paste(frame, (x, y))
            draw.text((x+8, y+362), f"{kind} {records[index]['timestamp']-records[0]['timestamp']:.3f}s", fill='white')
        sheet.save(root / f'scratch/vd3-browser/contact-{key}.jpg')
        print(json.dumps(dict(frames=len(frames), **manifest['gif'])))
