# A8 W3 observations

Model inspection, not Owner art approval:0/5 middle frames pass the complete
13-item checklist. Common sheet surfaces are less patchy than A7's interior
face/stole transfers. However the broader crown/softened beard, wider stole,
larger leaf shapes, denser regular fringes and wide stance remain inconsistent
with the immutable anchors. All five remain PLACEHOLDER. Cuffs, continuous
hem, muted material families, one satchel/roll and attached grounded boots pass
their individual checks; that does not grant a frame PASS. The reconstructed
mace centres pass their location constraint but weapon integration still FAILS.

checklist.png contains each item next to BOTH matching anchor crops.
checklist.json records all13 reasoned results and technical checks. The source
sequence-strip.png is transparent/equal-scale; contact-sheet-a7-vs-a8.png uses
archived A7 above current A8 at equal native scale. Neither is a game screenshot.
style-check-a7.png retains the original style sheet unchanged.

landmark-deltas.md/.json list all requested visible landmarks plus cloth-hidden
elbow/knee estimates and every adjacent-pair delta. Visible uncertainty±2px,
hidden±12px: estimates cannot certify strict4px joint compliance. Character
height is361px by the normalization's manually identified head top; endpoints
retain the documented361/371px disagreement. Full pose compliance FAILS.

Real720p flicker evidence is decoded from a native Godot fixed60FPS movie:
59 frames,58 post-draw traces, seven sampled poses, six adjacent pairs. All
frames are inspectable in playback-every-frame.png; playback-crop.gif is only
a quantized preview. Region RGB differences come from actual rendered pixels
under registered source-alpha masks. Silhouette IoU is explicitly source-alpha
occupancy, not RGB segmentation; it removes camera motion. Height differences
are source landmark measurements. These proxies cannot prove no flicker.
Actual playback still changes costume endpoints/stance and anchor identity.
Human hit-feel remains HUMAN_PENDING; Dummy audio is not a hardware audition.

Actual W3 operations: a8_style_check.py exit0; sync0; import0. First movie
process exited0 and printed CAPTURE_COMPLETE but the movie writer emitted
ERR_CANT_OPEN/ERR_UNCONFIGURED because its output directory was missing. That
run is REJECTED as evidence, retained in w3-playback-failed-1.log. Created the
local directory and reran: exit0, marker pass=true, no writer errors and a real
decodable AVI. a8_playback_check.py first exited1 (missing explicit hashlib
import after adapting the old star import); fixed hashlib/Pillow imports and
reran exit0. Existing Pillow getdata deprecation warnings are retained; they
do not affect pixel values. No gameplay/timing/HUD changes.
