"""Reuse proven rendered capture, changing evidence destination/labels only."""
from prepare_a9_regions import ROOT

source=ROOT/'godot-spike/tools/capture_a8.gd'
output=ROOT/'godot-spike/tools/capture_a9.gd'
assert not output.exists(),'Do not overwrite capture source'
text=source.read_text(encoding='utf-8-sig').replace('spike02-a8','spike02-a9').replace('baseline-a7','baseline-a8').replace('A8','A9').replace('movie-a8','movie-a9')
output.write_text(text,encoding='utf-8',newline='\n')
(ROOT/'godot-spike/.godot/spike02-a9-movie').mkdir(parents=True,exist_ok=True)
print('A9_CAPTURE prepared; same post-draw/hold/frame gates, A8 rendered comparison')
