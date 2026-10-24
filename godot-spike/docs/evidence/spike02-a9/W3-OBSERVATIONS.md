# A9 W3 source and actual-playback observations

Complete art gate: **0/5**, all middle frames PLACEHOLDER. Model source review
finds same-anchor face/hair improvement on00,02,03,04 (individual identity PASS)
and rigid uncompressed mace improvement on00/01 (integration still FAIL).
01 head stays A8 after three failed trials. Narrower donor costume patches and
foot shifts did not integrate; exact A8 cloth/legs remain. All previously
passing cuffs/hem/palette/one-bag/attached-feet items remain PASS. All five
stole/embroidery/fringe/seams/mace/full-landmark/sequence checks still FAIL.
No model inspection or small game display constitutes Owner art approval.

checklist.json/.png include both anchor crops,13 items and an A8->A9 column.
checklist-changes.md lists every item with its reason. Comparison/sequence
images are SOURCE sheets at identical scale, not game screenshots. Original
A8 style sheet is preserved as style-check-a8.png.

landmark-deltas.json/.md use exact unchanged A8 anatomy observations outside
the kept masks. Transformed anchor head centres use the recorded matrix and
source manual picks; this is not independent automatic face detection. Native
headtop is alpha-scanned within the head ROI. Mace centres independently scan
the final37x37 opaque ROI. Hidden joints remain +/-12px estimates, visible
manual joints +/-2px, so no full4px compliance is certified. Original boots
remain grounded but03 stance and04 foot placement remain out of tolerance.

Godot4.7.2 rendered59 native1280x720 frames at fixed60FPS,58 post-draw traces.
CAPTURE_COMPLETE A9 movie=true runs=1 shots=0 pass=true; process exit0; no
writer/script errors. AVI is reused for W5 because the same exact asset state
was captured. Seven actual pose samples and six adjacent-pair analyses live
in playback-check.json, sequence-check.json, sequence-runtime/ and the full
playback-every-frame.png. Region RGB means come from ACTUAL decoded movie
pixels under source-alpha-intersected W1 masks transformed into viewport
coordinates. Garment IoU is SOURCE-alpha occupancy, explicitly labelled; it is
not segmentation of rendered RGB. Height deltas come from source anatomy.
These proxies include camera/occlusion/flash effects and cannot prove no flicker.
Actual sequence still jumps at01 identity and broad cloth/stance endpoints.

W3 Python source audit0; capture preparation0; sync0; headless import0; native
movie0; movie decode/region metrics0. Pillow getdata deprecation warning is
retained. No game script, timing, rules, HUD, environment or original anchor
changed. HUMAN_PENDING; Owner art approval pending; commission fallback needed.
