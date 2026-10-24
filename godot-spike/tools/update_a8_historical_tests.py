"""Keep every A7 assertion but bind historical frame/audit reads to archive."""
from prepare_a8_sheet import ROOT
path=ROOT/'godot-spike/tests/test_a7_contract.gd'
text=path.read_text(encoding='utf-8-sig')
assert 'const A7_ARCHIVE' not in text
text=text.replace('const REPO = "res://../"','''const REPO = "res://../"
const A7_ARCHIVE = "res://docs/evidence/spike02-a8/baseline-a7/"

# A8 only replaces current art. Keep all A7 byte/pixel/provenance assertions.
func a7_frame(path: String) -> String:
	return A7_ARCHIVE + ("idle-01.png" if path.contains("/idle/") else path.get_file())''')
text=text.replace('FileAccess.get_sha256(SHARED+record.frame)','FileAccess.get_sha256(a7_frame(record.frame))')
text=text.replace('FileAccess.get_sha256(SHARED+record.path)','FileAccess.get_sha256(a7_frame(record.path))')
text=text.replace('json(SHARED+"frame-audit.json")','json(A7_ARCHIVE+"frame-audit.json")')
text=text.replace('image(SHARED+"thoma/swing/"+name)','image(a7_frame("thoma/swing/"+name))')
for name in ['03','04']:
    text=text.replace('image(SHARED+"thoma/swing/'+name+'.png")','image(a7_frame("thoma/swing/'+name+'.png"))')
path.write_text(text,encoding='utf-8',newline='\n')
print('A8 historical A7 assertions retained; archived frames/audit now authoritative')
