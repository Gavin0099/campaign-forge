# A8 method and claim ceiling

The commission brief is the binding art spec. W1 builds a 2048×1024 transparent
4+3 grid, each panel512×512. Panels1/7 contain exact original idle01/recover05
RGBA pixels; middle panels contain38% brief guides. A7 is archived as byte
copies. Appearance inputs are only the two anchors and their crop reference.

Three built-in image_gen EDIT calls painted all five middle frames TOGETHER.
All whole-sheet returns, exact prompts, references, input hashes and settings
are preserved in sheet-attempts/ and shared-anim/a8-swing-prompts.json.
The interface exposes no explicit mask parameter: the W1 mask was submitted as
an image with prompt constraints, not an enforced inpainting mask. Seed/model/
quality are not exposed. All returned1774×887 sheets repainted/rescaled the
anchors. They resemble them but are NOT byte-identical. Runtime endpoints
always use originals; neither generated endpoint was adopted.

Attempt1 broadly shares costume but puts02 too horizontally and over-enlarges
the cast. Attempt2 adds22% flat A7 alpha silhouettes, without ANY appearance
texture; it improves the02/04 arc but widens/simplifies stole details and has a
less coherent02 grip. Attempt3 keeps that scaffold and emphasizes narrow
asymmetric stole, tiny sprigs, short irregular fringe and close grey hair.
It is selected for the most coherent five-panel surface treatment and face,
then pose readability. It still does NOT match the anchors exactly. This is
an honest model preference between three failed candidates, not art approval.
No per-frame imagegen fallback was used: the sheet held all five broad poses.

Attempt3 is uniformly resized to the recorded grid, then panels2–6 are sliced.
Each body is normalized only by uniform scale and translation: head-to-ground
361px, opaque foot at464, registration origin remains[256,464]. Manual head
top/centre picks and all matrices are recorded. No limb rig, body warp,
independent generated face or costume collage is used. Generated alpha is
preserved above24, small detached islands<80px removed, transparent RGB zeroed;
visible RGB is straight, not multiplied by alpha.

All five normalized mace heads miss their brief targets. Local mace-only fixes
erase the exposed weapon, retain hand/forearm/body, redraw the oak haft/brass
collar to the target and rigidly rotate a masked original idle01 iron head.
Every pre-fix/output/mask/donor hash and centroid is recorded. First local fixes
left old shaft slivers on01/04: those failed intermediates are preserved;
second masked cleanup outputs remove the slivers. The reconstructed short
weapons meet contact location but projection/brush joins need the full art
audit. Target centroids are checked independently against final PNG opacity;
correct target placement does not certify the weapon design or pose.

W1 commit6ab7061. Initial sandbox commands could not access installed Python,
Godot or linked Git metadata; approved scoped escalations run those operations.
An exploratory import found numpy absent (exit1); tools use Pillow/stdlib,
no install. A read requested nonexistent check_a7_frames.py (exit1); existing
audit tools were then read instead. No push, merge, PR, stash, addon, gameplay,
timing, HUD, story, ui-prototype or art-brief changes. Task completion is not
session end; memory/PLAN writes are outside this explicitly scoped segment.

W2 correction: initial residual cleanup exited1 (missing pathlib.Path import), before changing any pixels. W2 commit2a355a0 therefore retained those slivers. Import fixed and cleanup rerun exit0 in a separate corrective commit before W3; both pre-cleanup runtime images preserved. No generation repeated.
