"""Retain A6 assertions against byte-copy archive; A7 tests cover live files."""
from build_a7_spec import ROOT
path=ROOT/'godot-spike/tests/test_a6_contract.gd'
text=path.read_text(encoding='utf-8-sig')
assert 'const A6_ARCHIVE' not in text
text=text.replace('const REPO = "res://../"','''const REPO = "res://../"
const A6_ARCHIVE = "res://docs/evidence/spike02-a7/baseline-a6/"

# A7 changes current art; preserve all historical A6 byte/provenance checks.
func a6_frame(path: String) -> String:
	return A6_ARCHIVE + ("idle-01.png" if path.contains("/idle/") else path.get_file())''')
for var in ['row.frame','record.path']:
    text=text.replace('FileAccess.get_sha256(SHARED+'+var+')','FileAccess.get_sha256(a6_frame('+var+'))')
text=text.replace('json(SHARED+"frame-audit.json")','json(A6_ARCHIVE+"frame-audit.json")')
text=text.replace('image(SHARED+row.frame)','image(a6_frame(row.frame))')
text=text.replace('image(SHARED+"thoma/swing/03.png")','image(a6_frame("thoma/swing/03.png"))')
text=text.replace('FileAccess.get_sha256(SHARED+"thoma/swing/"+file)','FileAccess.get_sha256(a6_frame("thoma/swing/"+file))')
path.write_text(text,encoding='utf-8',newline='\n')
print('A7_HISTORICAL A6 assertion coverage retained against archive; live A7 checked separately')
