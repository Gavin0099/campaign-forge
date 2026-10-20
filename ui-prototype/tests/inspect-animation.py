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
    left = right = start % width; top = bottom = start // width; count = 0
    while queue:
        value = queue.popleft(); x = value % width; y = value // width; count += 1
        left = min(left,x); right = max(right,x); top = min(top,y); bottom = max(bottom,y)
        for neighbor in (value-1 if x else -1, value+1 if x<width-1 else -1, value-width, value+width):
            if 0 <= neighbor < len(mask) and mask[neighbor]:
                mask[neighbor] = 0; queue.append(neighbor)
    if count > 1000:
        components.append(dict(x=left,y=top,width=right-left+1,height=bottom-top+1,pixels=count))
assert len(components)==30, f'Expected 30 separated full-body components; got {len(components)}'
frames=[]
for row in range(5):
    for col in range(6):
        matches=[c for c in components if int((c['x']+c['width']/2)/width*6)==col and int((c['y']+c['height']/2)/height*5)==row]
        assert len(matches)==1, (row,col,matches)
        box=matches[0]
        frames.append(dict(row=row,column=col,**box,anchorX=round((col+.5)*width/6,2),anchorY=box['y']+box['height']))
record=dict(source=asset.name,sha256=hashlib.sha256(asset.read_bytes()).hexdigest(),width=width,height=height,columns=6,rows=['idle','move','physical','hit-recovery','cast'],frames=frames,note='Full connected silhouette bounds avoid cutting sword poses at nominal cell borders. Pixels unchanged. Foot anchor measured per frame; manual visual review still required.')
metadata = root/'src/shienFrames.json'
if '--check' in sys.argv:
    assert json.loads(metadata.read_text(encoding='utf-8')) == record, 'Animation metadata stale'
else:
    metadata.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(size=image.size,frames=len(frames),maximum_width=max(c['width'] for c in frames),maximum_height=max(c['height'] for c in frames))))
