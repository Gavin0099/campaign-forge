# A6 W3 — observed relative improvement, incomplete final fidelity

Five complete new frames, no cutout repaint. 6 raw candidates, 5 picks, every
frame <=4 attempts. Equal-scale sequence-strip.png and 200 region crops in
region-check.png were inspected alongside the two immutable references and A5.
Per-frame PASS/FAIL is in shared-anim/frame-audit.json and frame-status-table.md.

Observed improvements: no floating A5 offhand sleeve scrap in02/03, no detached
right boot in00/02/03/04, continuous painted robe/underskirt. Exactly one
satchel in each whole frame/crop. New01 removes the A5 inserted cuff/body join.

Remaining FAILs: all five generated botanical sprigs/fringes have different
stroke/width/spacing; face/hair remain recognizable but cheek/hair rendering
drifts from fixed references. Head-height range348.369–356.224px is within the
declared360+/-18px tolerance. No costume part was independently transformed.
Palette remapping uses only idle01 colours, but that does not ensure constant
shading/grain or identical garment mean colour during pose changes.

Weapon design remains the approved short flanged iron mace/oak/brass. 03's
single whole-frame transform maps manually inspected raw head-center[1170,424]
exactly to[455,196]; no weapon patch/warp. However 04's head is around[421,357]
instead of A5[421,376], grip differs too: mace FAIL, exact pose-geometry
requirement NOT fully met. Newly generated hands/mace pixels are not raw-A5
byte protection. geometry-check.json preserves manual landmarks and3px raw
selection uncertainty; fixed manifest geometry is a separate test contract.

Actual non-headless Godot4.7.2 1280x720 --write-movie --fixed-fps60 run exited0:
CAPTURE_COMPLETE A6 movie=true runs=1 shots=0 pass=true. Decoded59 consecutive
native rendered frames in playback-every-frame.png, seven traced key poses in
playback-keyframes.png; full native selected screenshots in sequence-runtime/.
playback-crop.gif is only a looping preview, with GIF time quantization.
Movie/trace process frame is the timing authority; encoding wall time is not.

The first decoder exited1 on59 movie frames vs58 post-draw records. Failure
retained in attempt-playback-trace-count.log. Final decoder keeps58 real records
and labels the untraced terminal frame; requires full decoded RGB equality to
the preceding actual ready frame. No trace entry is invented. Rerun exit0.

Observed through all consecutive actual rendered crops: no duplicate bag or
detached sleeve/shoe flashes; new01 no longer flashes a cutout waist/shoulder
seam. Hem/stance width changes and endpoint motif/style changes still pop.
Native-size detail cannot prove exact embroidery consistency; source crops
show remaining drift. Overall sequence FAIL, not waived by small render scale.
Six pairs have alpha-intersected rectangular region RGB deltas, garment IoU
and head-to-ground height delta in sequence-check.json. These proxies include
occlusion and pose changes and do not approve folds, continuity or human feel.

All five motion frames remain PLACEHOLDER. Both byte-identical endpoints retain
reference PASS; adjacent defects are assigned to the generated motion frames.
No Owner art approval. Human hit-feel/playtest remains HUMAN_PENDING.

W3 sync/import were prerequisites for this actual-playback check; W4 performs
final sync/import/tests against final audit. No gameplay, HUD, manifest timing,
knight, battlefield, prop, story, decision or ui-prototype change.
