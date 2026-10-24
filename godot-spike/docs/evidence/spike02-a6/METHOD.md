# A6 W1 — full-frame anchored regeneration

Start: clean codex/godot-spike at 438e801 above A5 78bb38a. Gavin confirmed
single-session use and this worktree exception on 2026-10-24. Fetched the
specified GPT review (exit 0); A5 art REJECT, swing/01 single-frame PASS but
playback seam check still pending. Godot selected; Phase B/React CANCELLED.
Short one-handed flanged mace APPROVED canon. No decision record edits.

## Tool and references

Built-in image_gen, transparent_background=true. Exact prompts/settings and
reference SHA-256 values are in ../../../../../shared-anim/a6-swing-prompts.json.
Model, quality and seed are not exposed. Each returned raw PNG is retained
unchanged in candidates/<frame>/attempt-<n>.png; maximum FOUR calls per frame.
One frame is finished and recorded before another is started.

Every call has exactly three images: idle/01 and swing/05 are costume, face,
hair, palette, painting and mace authorities; the A5 same-index frame is ONLY
a pose/silhouette guide. Prompts explicitly prohibit reproducing its cutout
fragments. No prior generated neighbour is a costume source.

Prompt template: create ONE complete full-body transparent sprite; preserve
the first two reference identities/costume/mace; use the third only for pose;
list head/hand/head-of-mace/ground coordinates and pose intent; require natural
shoulder/cuffs, continuous hem/legs/boots, exactly one satchel, two ivory bands
with small botanical sprigs; forbid extra objects and disconnected fragments.
Full exact prompt text, including iteration corrections, is retained per call.

## Normalization and allowed touch-up

prepare_a6_frames.py applies one uniform scale/translation to the WHOLE image,
including mace: no costume warps or independent body/weapon transforms.
512x512 canvas, pivot metadata [256,464], head-to-ground 360px +/- 18px
(5%, permitting a braced attack), opaque planted sole y=464 +/- 1px.
Contact 03 must retain head anchor [455,196]. Mace head/haft/grip landmarks
are compared against A5 after normalization; canvas/pivot alone do not prove it.

Allowed cleanup: clear alpha<24 and hidden transparent RGB; recorded nearest
idle/01 128-colour RGB remap, no dithering. Record raw/normalized/runtime hashes,
single transform, per-pixel cleanup mask and before/after mean nearest-colour
distance. No retouch currently beyond these operations. No costume parts,
face, boots, sleeve or weapon pixels are pasted from another source.

A4/A5 reconstructed garments by rig/mesh/patch transfers. A6 generates the
complete figure in one pass and uses only the allowed uniform transform and
small-defect cleanup. Original/raw/reference PNGs are never edited or moved.

## W1 proof gate result

Two attempts on 02; candidate 1 is the best. proof-02.png places A5 / candidate
1 / idle/01 / swing/05 on equal 512px canvases with unscaled region crops.
Both candidates improve anatomy; candidate 1 clearly removes A5's floating
offhand sleeve pieces, triangular lower-hem scrap and disconnected right boot.
Two ivory botanical stole bands, wide ivory cuffs, teal robe, single satchel,
pendant and brown boots remain consistent with both reference designs.
Gate PASS: proceed to W2. This is relative structural improvement, NOT full art
acceptance: motif stroke/scale, fringe, face detail and inter-frame style may
still fail W3. No live frame replaced in W1, no PLACEHOLDER removed.

Candidate 2 is retained: less faithful shoulder/stole drape and altered wrist;
not chosen. 2/4 attempts used; no reason to spend remaining attempts once the
bounded structural proof is clear. W2 must record each remaining frame; W3
must retain explicit failures and test actual playback. HUMAN_PENDING remains.

Initial sandbox Python lookup denied access; existing absolute installation
worked with approved tool escalation. Python 3.12.10, Pillow 12.2.0; no install.
Exact Python SHA-256 matches A5: 4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a.
This is tool identification, not hardened subprocess/trust-root verification.
Root PLAN/memory and ui-prototype are outside the authorized write scope;
this method and the segment handoff are the scoped milestone record.
