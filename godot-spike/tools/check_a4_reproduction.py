"""Read-only reconstruction check: rig + A3 baseline reproduces live PNG bytes."""
from prepare_a4_frames import SHARED, OUT, REFS, POSES, build, sha
from PIL import Image
from io import BytesIO
import hashlib, json

records=json.loads((SHARED/'a4-swing-prompts.json').read_text())
for record in records:
    index=record['frame'][-6:-4]
    old=Image.open(OUT/f'baseline-a3/{index}.png').convert('RGBA')
    rebuilt,protected=build(index,old)
    encoded=BytesIO();rebuilt.save(encoded,format='PNG',optimize=True)
    assert hashlib.sha256(encoded.getvalue()).hexdigest()==sha(SHARED/record['frame'])==record['runtime_sha256']
    assert protected.tobytes()==Image.open(OUT/f'protected-masks/{index}.png').tobytes()
    assert record['controls']==json.loads(json.dumps(POSES[index]))
    for path in REFS.values():assert sha(SHARED/path)==record['references'][path]
print('A4_REPRODUCTION frames=5 identical_png_bytes=true identical_protected_masks=true references_unchanged=true')
