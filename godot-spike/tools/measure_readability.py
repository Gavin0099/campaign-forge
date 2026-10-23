"""Opaque-silhouette overlap from rendered-run sprite transforms (not screenshots).
Counts include weapons, exclude UI/rings/flash. Conservative mask threshold 128.
Full viewport transforms include reflection, rotation and camera zoom.
"""
from pathlib import Path
from PIL import Image,ImageChops
import json,sys
root=Path(__file__).resolve().parents[1]
folder=root/'docs/evidence'/('spike02-a2' if '--a2' in sys.argv else 'spike02')
shots=json.loads((folder/'readability.json').read_text(encoding='utf-8-sig'))
out=[]
for shot in shots:
    masks={}
    for b in shot['bodies']:
        im=Image.open(root/b['texture'].removeprefix('res://')).convert('RGBA')
        a,basis_y,c,d,tx,ty=b['screen_transform']
        determinant=a*d-basis_y*c
        assert abs(determinant)>1e-9
        inverse=(d/determinant,-c/determinant,(c*ty-d*tx)/determinant,
                 -basis_y/determinant,a/determinant,(basis_y*tx-a*ty)/determinant)
        alpha=im.getchannel('A').transform((1280,720),Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC)
        masks[b['id']]=alpha.point(lambda value:255 if value>=128 else 0)
    pairs={}
    keys=list(masks)
    for i,a in enumerate(keys):
        for b in keys[i+1:]: pairs[a+'/'+b]=ImageChops.multiply(masks[a],masks[b]).histogram()[255]
    out.append(dict(file=shot['file'],option=shot['option'],setup=shot['setup'],phase=shot['phase'],opaque_overlap_px=pairs))
(folder/'readability-overlap.json').write_text(json.dumps(out,indent=2)+'\n')
for row in out:print(row)
