"""Read-only verification of preserved originals and generated sprite separation."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'ui-prototype/public/art'
DOCS = ROOT / 'ui-prototype/docs'

def check(record):
    image_path = (ART / record['file']).resolve()
    if not image_path.is_relative_to(ART.resolve()):
        raise ValueError('Asset escapes project art directory')
    if hashlib.sha256(image_path.read_bytes()).hexdigest() != record['sha256']:
        raise ValueError(f'Asset digest changed: {record["file"]}')
    image = Image.open(image_path)
    if image.size != (record['width'], record['height']) or image.mode != record['mode']:
        raise ValueError(f'Image metadata changed: {record["file"]}')
    if record['file'] in ('party-v2.png', 'units-v2.png'):
        count = 4 if record['file'].startswith('party') else 5
        alpha = image.getchannel('A')
        values = [alpha.crop((round(image.width*i/count)-1, 0, round(image.width*i/count)+1, image.height)).getextrema()[1] for i in range(1,count)]
        if any(value >= 16 for value in values):
            raise ValueError(f'Visible art crosses sprite column: {values}')

originals = json.loads((DOCS / 'art-manifest.json').read_text(encoding='utf-8'))
for name, record in originals.items():
    if hashlib.sha256((ART/name).read_bytes()).hexdigest() != record['sha256']:
        raise ValueError(f'Original v1 asset changed: {name}')
manifest = json.loads((DOCS / 'visual-sprint/art-manifest.json').read_text(encoding='utf-8'))
for record in manifest['assets']:
    check(record)
print(f'PASS: {len(originals)} original assets preserved; {len(manifest["assets"])} v2 assets match digests/dimensions; 4/5-column sprite boundaries below alpha 16.')
