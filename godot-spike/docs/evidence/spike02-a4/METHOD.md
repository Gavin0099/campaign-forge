# A4 W1 — reference-anchored cutout rig

Authority: Gavin, 2026-10-24. A4 only; no Phase B, React edits or push.
Starting commit 8197026, A3 bd80c5e. The fetched GPT A3 review is
CONDITIONAL ACCEPT with incomplete final paragraph; its suggestion about B
does not override this brief. Weapon identity remains APPROVED.

## Chosen method and proof

Use Pillow to transfer one continuous reference torso/skirt, rather than
generate a figure and repair its decorations. The body includes stole bands,
their existing motifs, bag, medallion, robe and underskirt edge. Reference
face/hair and cuffs are separate articulated parts. The A3 pose supplies only
the motion silhouette of arms/torso twist, fixed hands/mace and planted feet.
No image generation is used, so there are zero generation attempts.

`godot-spike/tools/prepare_a4_frames.py --proof` extracts the library and
renders contact frame 03 to `proof-03.png`, without changing the live frame.
`proof-before-after.png` compares the full 512 canvases at identical scale.
`proof.json` records the input/output SHA-256. This is an asset proof, not a
game screenshot or an art approval.

The first rigid proof (`proof-rejected-rigid.png`) is explicitly rejected:
transparent cuff bounding boxes made holes and the narrow reference body
disconnected from the wide stance. The revised proof uses the four actual
cloth corners and 1.15 horizontal garment scale, with unit vertical scale.
It demonstrates a reference-derived, narrower layered hem instead of the
old fan. Shoulder/waist joins and the reconstructed area behind the idle mace
remain visible limitations. W3 must judge them; provenance alone is not PASS.

## Per-frame source map

| Swing | Continuous body, both stoles, embroidery, hem, bag, medallion | Face/hair and both cuffs | Reason |
| --- | --- | --- | --- |
| 00 | idle/01 | idle/01 | Upright anticipation closest to idle; small shear fits the wide stance |
| 01 | idle/01 | idle/01 | Upright raised pose; smallest torso shear |
| 02 | swing/05 | swing/05 | Forward shoulder and lower head; negative cloth sweep |
| 03 | swing/05 | swing/05 | Forward contact shoulder; negative shear, exact A3 weapon overlay |
| 04 | swing/05 | swing/05 | Lower forward head and trailing cloth; strongest negative shear |

All source polygons and destination cuff quadrilaterals, head offsets and
affine controls are in `reference-regions/regions.json` and `rig-controls.json`.
The library contains 24 masked full-canvas reference regions, corresponding
mask PNGs, and measured palette samples with source rectangles and hashes.
The left stole is split above/below the bag for inspection; reconstruction
uses the continuous body, not separately overlapped strips.

## Motion-only work and seams

- Existing A3 arms, torso twist, hand/weapon and feet are retained as motion
  layers; no new anatomy or mace is generated. The two cuff surfaces are
  replaced with reference pixels at recorded corners, feathered 0.55 px.
- Only the small area occluded by the *idle reference's mace* is reconstructed
  by cloning neighboring plain reference bag/cloth. The source/destination
  quads are recorded. No new embroidery is painted. This reconstruction is
  subject to visible-seam review, not silently treated as exact source art.
- The old skirt alpha below y=270 is removed completely, then the continuous
  reference body/hem is composited over unchanged feet. This explicitly fixes
  the prior method's refusal to change the A2 fan/bell contour. There is no
  global resize/re-registration, and no frame auto-fit.
- The body has 1.15 horizontal scale, unit vertical scale and small per-pose
  shear. Motif spacing along the stole stays fixed; lateral motif widening
  and shoulder joins remain reviewable risks. Continuous bands prevent the
  doubled motif/border rows created by separate patches. No extra sprigs added.
- Transparent RGB is zeroed; reference edge alpha is retained through bicubic
  RGBA transformation. Palette distance before/after is recorded; no mapping
  is applied unless evidence shows it is necessary. Palette numbers are
  supporting proxies, not perceptual quality scores.

## Verification plan

W2 archives A3 bytes before rebuilding five frames. W3 compares all six
regions and adjacent poses, retaining PLACEHOLDER for any failure. W4 tests
immutable references, manifest equality, protected weapon/feet, provenance,
sync and honest status. Historical A3 assertions must target the archived A3
frames, since A4 explicitly changes the old garment alpha. W5 uses a rendered
run for 720p/1080p, an actual 60 FPS movie and separate no-readback timing.
W6 embeds the audited table and stops. Human hit-feel remains HUMAN_PENDING;
P010 remains PROPOSED. No claim of commercial art approval.
