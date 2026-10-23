"""Opaque-silhouette overlap from rendered-run sprite transforms (not screenshots).
Counts include weapons, exclude UI/rings/flash. Conservative mask threshold 128.
Camera zoom is common to all actors; world-space overlap is the comparison.
"""
from pathlib import Path
from PIL import Image,ImageChops
import json
root=Path(__file__).resolve().parents[1]
folder=root/'docs/evidence/spike02'
shots=json.loads((folder/'readability.json').read_text(encoding='utf-8-sig'))
out=[]
for shot in shots:
    masks={}
    for b in shot['bodies']:
        im=Image.open(root/b['texture'].removeprefix('res://')).convert('RGBA')
        sx,sy=b['scale']; x,y=b['origin']
        # A negative global X means reflection about the fixed foot pivot.
        if sx<0: im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);x+=im.width*sx
        im=im.resize((round(im.width*abs(sx)),round(im.height*abs(sy))),Image.Resampling.LANCZOS)
        canvas=Image.new('L',(1280,720));canvas.paste(im.getchannel('A').point(lambda a:255 if a>=128 else 0),(round(x),round(y)))
        masks[b['id']]=canvas
    pairs={}
    keys=list(masks)
    for i,a in enumerate(keys):
        for b in keys[i+1:]: pairs[a+'/'+b]=ImageChops.multiply(masks[a],masks[b]).histogram()[255]
    out.append(dict(file=shot['file'],option=shot['option'],setup=shot['setup'],phase=shot['phase'],opaque_overlap_px=pairs))
(folder/'readability-overlap.json').write_text(json.dumps(out,indent=2)+'\n')
for row in out:print(row)
