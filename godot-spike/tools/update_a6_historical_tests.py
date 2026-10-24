"""Route historical A5 art assertions to immutable A5, retaining assertions."""
from prepare_a6_frames import *
import sys
p=REPO/'godot-spike/tests/test_a5_contract.gd';text=p.read_text(encoding='utf-8-sig')
if 'const A5_ARCHIVE' in text:
    print('A5 historical test routing already migrated; no changes')
    sys.exit(0)
text=text.replace('const CHECKS =','const A5_ARCHIVE = "res://docs/evidence/spike02-a6/baseline-a5/"\nconst CHECKS =',1)
text=text.replace('func json(path: String):','''# A6 replaces generated art. A5 raw cutout-protection proofs remain against
# the immutable A5 archive; all current contracts live in test_a6_contract.gd.
func a5_frame(path: String) -> String:
	return A5_ARCHIVE + ("idle-01.png" if path.contains("/idle/") else path.get_file())

func json(path: String):''',1)
text=text.replace('SHARED+"thoma/swing/"+name','a5_frame("thoma/swing/"+name)')
text=text.replace('png(SHARED+"thoma/swing/03.png")','png(a5_frame("thoma/swing/03.png"))')
text=text.replace('json(SHARED+"frame-audit.json")','json(A5_ARCHIVE+"frame-audit.json")')
text=text.replace('FileAccess.get_sha256(SHARED+record.path)','FileAccess.get_sha256(a5_frame(record.path))')
text=text.replace('FileAccess.get_sha256(SHARED+record.frame)','FileAccess.get_sha256(a5_frame(record.frame))')
p.write_text(text,encoding='utf-8',newline='\n')
p=REPO/'godot-spike/tools/a6_contact_sheet.py'
text=(REPO/'godot-spike/tools/a5_contact_sheet.py').read_text(encoding='utf-8-sig').replace('prepare_a5_frames','prepare_a6_frames').replace('A5','A6')
p.write_text(text,encoding='utf-8',newline='\n')
