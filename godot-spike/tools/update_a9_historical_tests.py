"""Retain every A8 assertion while binding its historical art to archive."""
from prepare_a9_regions import ROOT

p=ROOT/'godot-spike/tests/test_a8_contract.gd';text=p.read_text(encoding='utf-8-sig')
assert 'const A8_ARCHIVE' not in text
text=text.replace('const REPO = "res://../"','''const REPO = "res://../"
const A8_ARCHIVE = "res://docs/evidence/spike02-a9/baseline-a8/"

func a8_frame(path: String) -> String:
	return A8_ARCHIVE + ("idle-01.png" if path.contains("/idle/") else path.get_file())''')
text=text.replace('func image(path: String) -> Image:\n','func image(path: String) -> Image:\n\tif path.begins_with(SHARED+"thoma/"): path = a8_frame(path)\n')
text=text.replace('json(SHARED+"frame-audit.json")','json(A8_ARCHIVE+"frame-audit.json")')
text=text.replace('FileAccess.get_sha256(SHARED+record.path)','FileAccess.get_sha256(a8_frame(record.path))')
text=text.replace('FileAccess.get_sha256(SHARED+record.frame)','FileAccess.get_sha256(a8_frame(record.frame))')
p.write_text(text,encoding='utf-8',newline='\n')
print('A9 historical A8: all8 original tests retained, archived PNG/audit reads')
