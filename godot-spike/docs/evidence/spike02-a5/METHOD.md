# A5 W1 — seams and feet, reference rig refinement

Owner: Gavin, 2026-10-24. Start cc164b2, A4 handoff 8592fbb.
Fetched and read origin/review/gpt-godot-spike A4 review (art REJECT,
engineering accepted). This is five-frame repair, not costume redesign.
Godot chosen by Owner; Phase B CANCELLED. Weapon is APPROVED canon.

## Retained base and reproducibility

`../../../tools/prepare_a5_frames.py` imports A4's unmodified cutout helpers,
region polygons, pose controls, cuff quadrilaterals, head offsets and weapon
protection polygons. The committed A4 reference library remains unchanged.
Both reference PNGs remain byte-identical. Run `--proof` for the W1 draft;
`--build` archives A4 then reconstructs five live frames. No generation calls,
manual unrecorded paint, extra dependency or new costume element.

## Repairs and explicit rejection conditions

| A4 defect | Concrete change | Reject if still visible |
| --- | --- | --- |
| Shoulder / torso twist | Retain A4 cape silhouette above y=248, use a continuous reference body, feather arm polygon joins inward; final 0.75px smoothing at half strength only inside declared narrow seam bands and opaque interior | Cut corner, brightness step, fabric direction discontinuity |
| Waist | Single continuous body and satchel, no separate waist overlay; narrow waist band smooths retained sleeve/body intersection | Horizontal splice or mismatched fold |
| Cuffs | Original A4 four-corner reference transfers with inward 1px blend; 6px perimeter seam band | Separate pasted patch, broken fold, hole |
| Cloned bag | Remove both A4 CLONES, retain upper cape only above bag, one recover-reference body; fill recovery mace occlusion with a plain teal reference-robe patch, never a bag patch | More than one bag or repair scar |
| Hem / feet | Keep A4 feet as raw RGBA; continuous lower-body mesh below y=382 brings scalloped underskirt toward fixed ankles; body over boots, final foot protection restores actual planted soles | Thin neck, floating ankle, boot/cloth overlap or lost scallops |
| 1.15 stretch | Remove globally: horizontal upper-garment scale exactly 1.0; ease confined below source y=382 (last motif ROI ends y=376) | Motif/border width or spacing differs by more than 5% locally |
| Outline | Same body topology across all poses, A4 shear and indexed lower-hem ease; compare all six neighbours and contour/colour proxies | Snapping cape, cuff, bag, hem, flicker; metrics alone cannot approve art |

The plain-cloth occlusion patch is a reference pixel transfer, not seam paint.
Its source/target quad is in rig-controls.json. Hem mesh and source transfers
are structural cutout operations explicitly allowed by the brief. All final
paint-over smoothing is limited to seam-masks; no motif is synthesized.

## Committed seam bands

[coordinates.json](seam-masks/coordinates.json) specifies every polyline,
width, per-frame mask SHA-256 and area. Widths are 6px cuffs / 8px torso and
waist. Maximum union area 10,000 pixels, 3.815% of the 512x512 canvas.
Actual areas: 00 7,608; 01 5,450; 02 5,939; 03 6,004; 04 5,687 pixels.
Masks follow actual cutout perimeters; no whole stole or motif row is covered.
No smoothing is applied in transparent/antialiased outline pixels.
An initial 6,500-pixel total budget rejected 00 (exit 1); revised total budget
retains the same narrow width, no band was enlarged to evade the check.

## Scale measurement

[scale-measurement.json](scale-measurement.json) measures the A4 reference
embroidery ROI's horizontal map at a fixed source y: x=226..251 is 25px,
A4 1.15x maps to 28.75px, A5 1.0 maps to 25px. The same source-row horizontal
spacing maps at 1:1, independent of shear translation. Tolerance <=5%,
analytical deviation 0%. This is a local transform measurement, not a claim
that a sheared motif's axis-aligned bounding box or raster antialiasing is
unchanged. The hem ease starts below all these motif pixels, so it cannot
stretch their horizontal geometry. No global 1.15 scale remains.

## Per-frame controls and risks

| Frame | Kept intent | Refinement / remaining risk to inspect |
| --- | --- | --- |
| 00 | Anticipation, overhead mace | Recover body underneath original idle-derived face/cuffs; .70 lower-hem ease for wide left stance; raised shoulder join |
| 01 | Raise | .48 lower-hem ease; shoulder occlusion and transition from 00 |
| 02 | Fast swing, existing smear | .98 lower-hem ease; squared shoulder and offhand cuff transition |
| 03 | Contact at [455,196] | .82 lower-hem ease; chosen one-frame proof, inspect left ankle / waist / single bag |
| 04 | Follow-through | .48 lower-hem ease, original -.32 shear; torso twist and return to immutable recover |

Proof: [before/after crops](proof-before-after.png), [draft 03](proof-03.png),
[input/output hashes](proof.json). Crops are unscaled source pixels, not game
screenshots. This proves construction, not acceptance; W3 must explicitly
retain PLACEHOLDER for any failed region/sequence. The draft may still have
fold/hem inconsistencies. Each such failure will be recorded, not inferred
away from hashes or numeric proxies.

## Verification contract

W2 immutable A4 baseline + provenance/palette distances. W3 ten region crops,
six pair metrics and honest audit. W4 exact reference/manifest/protected mace
and foot bytes, seam mask support/area, no archive references and status/table
agreement. Historical A4 tests use the A4 archive; live A5 tests stay live.
W5 rendered 720p/1080p, six no-readback normal/reduced setups per size and a
real fixed-60fps movie. W6 handoff then stop. Human hit-feel HUMAN_PENDING.
No ui-prototype, rules, HUD, story, P010, push or other worktree edits.
