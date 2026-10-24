"""Copy the verified A6 observer with evidence paths only; no game changes."""
from build_a7_spec import *
source=(ROOT/'godot-spike/tools/capture_a6.gd').read_text(encoding='utf-8-sig')
source=source.replace('A6','A7').replace('a6','a7').replace('baseline-a5','baseline-a6')
(ROOT/'godot-spike/tools/capture_a7.gd').write_text(source,encoding='utf-8',newline='\n')
print('A7_CAPTURE generated from A6; only segment/evidence/baseline paths changed')
