"""Read-only alpha inspection; writes frame metadata, never edits image pixels."""
from collections import deque
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
asset = root / 'public/art/shien-actions-v3.png'
image = Image.open(asset).convert('RGBA')
width, height = image.size
alpha = image.getchannel('A')
mask = bytearray(1 if a > 64 else 0 for a in alpha.tobytes())
components = []
for start in range(len(mask)):
    if not mask[start]:
        continue
    queue = deque([start]); mask[start] = 0
    left = right = start % width; top = bottom = start // width; count = 0; pixels = []
    while queue:
        value = queue.popleft(); x = value % width; y = value // width; count += 1; pixels.append((x,y))
        left = min(left,x); right = max(right,x); top = min(top,y); bottom = max(bottom,y)
        for neighbor in (value-1 if x else -1, value+1 if x<width-1 else -1, value-width, value+width):
            if 0 <= neighbor < len(mask) and mask[neighbor]:
                mask[neighbor] = 0; queue.append(neighbor)
    if count > 1000:
        components.append(dict(x=left,y=top,width=right-left+1,height=bottom-top+1,pixels=count,coordinates=pixels))
assert len(components)==30, f'Expected 30 separated full-body components; got {len(components)}'
frames=[]
for row in range(5):
    for col in range(6):
        matches=[c for c in components if int((c['x']+c['width']/2)/width*6)==col and int((c['y']+c['height']/2)/height*5)==row]
        assert len(matches)==1, (row,col,matches)
        box=matches[0]
        overlaps=any(other is not box and min(box['x']+box['width'],other['x']+other['width'])>max(box['x'],other['x']) and min(box['y']+box['height'],other['y']+other['height'])>max(box['y'],other['y']) for other in components)
        path=[]
        if overlaps:
            # Display-only clipping metadata, not bitmap editing. Rectangles can
            # include another character when long sword poses overlap in bounds.
            for scan_y in range(box['y'],box['y']+box['height']):
                xs=sorted(x for x,y in box['coordinates'] if y==scan_y)
                if not xs:continue
                start_x=previous=xs[0]
                for scan_x in xs[1:]+[xs[-1]+2]:
                    if scan_x>previous+1:
                        length=previous-start_x+1
                        path.append(f'M{start_x} {scan_y}h{length}v1h-{length}z')
                        start_x=scan_x
                    previous=scan_x
        fields={key:value for key,value in box.items() if key!='coordinates'}
        frames.append(dict(row=row,column=col,**fields,clipPath=''.join(path),anchorX=round((col+.5)*width/6,2),anchorY=box['y']+box['height']))
record=dict(source=asset.name,sha256=hashlib.sha256(asset.read_bytes()).hexdigest(),width=width,height=height,columns=6,rows=['idle','move','physical','hit-recovery','cast'],frames=frames,note='Connected silhouette clipping excludes neighboring figures on overlapping sword frames; other frames use padded bounds. Bitmap pixels unchanged. Foot anchor measured per frame; manual visual review still required.')
metadata = root/'src/shienFrames.json'
if '--check' in sys.argv:
    assert json.loads(metadata.read_text(encoding='utf-8')) == record, 'Animation metadata stale'
else:
    metadata.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(size=image.size,frames=len(frames),maximum_width=max(c['width'] for c in frames),maximum_height=max(c['height'] for c in frames))))
