# Task Godot spike 02 A5: fix the seams, cuffs, bag and feet on Thoma's 5 swing frames

Authorized by Gavin on 2026-10-24 (Asia/Taipei): 「先再修一次 5 格揮擊的衣服細節」, then 「不用網頁版 直接用Godot」 ("No web version; use Godot directly").

## Owner decision: Godot chosen, Phase B cancelled
On 2026-10-24 the Owner decided that campaign-forge uses **Godot directly**. The React web version of the animation scene and the React-vs-Godot comparison (Phase B, `docs/tasks/godot-spike-02-swing-and-ab.md`) are **CANCELLED by the Owner**. Do not start Phase B, do not build `?scene=anim-ab`, and **do not touch `ui-prototype/`**. Do not add React to-dos anywhere. Record the decision in the handoff (see W6). Do not edit P010 or other decision records yourself; just note in the handoff that P010 needs updating by the Owner to reflect the Godot decision.

Thoma's short one-handed flanged mace is **APPROVED canon**; do not change its status or design.

This is a **small art-fix segment** on top of spike-02 A4 (`8592fbb`).

## Why
The GPT review of A4 (`docs/review/gpt-godot-spike-02a4.md` on `origin/review/gpt-godot-spike`, `ba4139b`) is **REJECT for art**: 0/5 frames pass. Engineering and verification were accepted (42 GUT tests, 1583 asserts).

| Region | A4 result |
| --- | --- |
| Embroidery, face/hair, palette | PASS (keep these; do not regress) |
| Stole | FAIL: shoulder seams, waist splice, cloth clone marks |
| Cuffs | FAIL: fold lines do not continue across the cuff/arm join |
| Hem | FAIL: hem does not meet the fixed feet; cloth looks detached from the body |
| Sequence | FAIL: all 6 adjacent pairs fail |

P1 from the review: shoulder and waist seams, cuff joins, the **cloned bag** (the bag/plain cloth clone that fills the area behind the idle mace leaves a duplicated bag and a horizontal seam), and the **hem not connecting to the legs/feet**.
P2: the **1.15× horizontal garment scale** stretches some embroidery; **cloth outlines differ between poses**.

Per-frame failures (from `godot-spike/docs/evidence/spike02-a4/frame-status-table.md` and the review):

| Frame | A4 failure |
| --- | --- |
| `swing/00` | shoulder band strap seam; horizontal bag splice line; hem-to-boot connection too narrow |
| `swing/01` | upper shoulder/arm seam; cloth clone boundary; abrupt transition from the previous pose |
| `swing/02` | obvious squared shoulder cut; visible waist overlay boundary |
| `swing/03` | shoulder/waist seams; bag repair marks; left foot detached from the hem |
| `swing/04` | torso-twist seam; cloth junction; boot overlap; jump into the recover pose |

## Method: keep the A4 rig, fix the joins
A4's reference-anchored cutout rig (`godot-spike/tools/prepare_a4_frames.py`, `reference-regions/`, `rig-controls.json`) is the base. It fixed the fan hem and the duplicated embroidery rows; **keep that**. A5 fixes what the rig left behind. It must **not** be a new costume design, and not a whole-frame regeneration.

- Costume detail stays anchored to `thoma/idle/01.png` and `thoma/swing/05.png`. Both must stay **byte-identical**.
- **Seams (shoulder, waist, torso twist).** Hide every cut edge of the cutout rig. Allowed moves: better cut lines that follow natural fold or shadow lines; overlapping layer order (the stole lying over the arm instead of a hard cut); feathered or blended joins; and **paint-over or inpainting restricted to a committed seam mask**. A seam mask may cover only a narrow band around a join, never a whole stole or motif row. No new embroidery, motifs or costume elements may be painted inside a seam mask.
- **Cuffs.** Fold lines and the cuff edge must continue across the cuff/forearm join, with no box edge, hole or brightness step.
- **Bag: exactly one.** Remove the duplicated bag/clone. Fill the area that was behind the idle mace with plain robe cloth that continues the surrounding folds, or move the bag to its correct place per pose. Each frame must show exactly one satchel, the same design as in the reference.
- **Hem and feet.** The hem must flow into the legs and feet: no gap or thin neck between hem and boot, no hem floating above or detached from a planted foot, no boot drawn over the hem incorrectly, and correct ground contact on the planted feet (feet stay at the pivot, nothing below the ground line). Change hem shape and alpha as needed, but keep the reference edge treatment (scalloped edge, shadow).
- **1.15× stretch.** Remove the 1.15× horizontal garment scale, or keep a smaller scale only where you justify it in W1 with a measurement showing the embroidery motif width/spacing stays within a stated tolerance of the reference (for example ≤ 5%). Prefer widening the stance coverage with cloth fill or a hem warp over stretching the embroidered bands.
- **Consistent cloth outline.** The robe/stole/hem outline should change smoothly across idle/01 → 00 → 01 → 02 → 03 → 04 → 05, following the motion, with no shape jumps between neighbours.
- **AI image generation is allowed** for seam inpainting and for motion-only regions (arms, hands, torso twist, cloth sweep), at most **3 attempts per frame**, always masked and always with idle/01 and swing/05 as references. Generated pixels must not change embroidery, face/hair or palette. Record every attempt (tool, full prompt, references, mask, raw and runtime SHA-256, cleanup) in `shared-anim/SOURCES.md` and a new `shared-anim/a5-swing-prompts.json`. Rejected attempts go to `shared-anim/rejected/` (listed).
- Everything must be **reproducible from scripts** (for example a new `godot-spike/tools/prepare_a5_frames.py` that builds on the A4 rig), with the masks, seam masks and control points committed. A manual paint-over pass is allowed if it is recorded: inputs, output hash, mask and what was touched.

Read first:
- the A4 review: `git fetch origin review/gpt-godot-spike`, then `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a4.md`
- the **"spike-02 A4"** section of `godot-spike/docs/HANDOFF.md` and `godot-spike/docs/VERIFICATION.md#spike-02-a4`
- `godot-spike/docs/evidence/spike02-a4/`: `METHOD.md`, `frame-status-table.md`, `reference-regions/`, `region-masks/`, `protected-masks/`, `region-check.png`, `sequence-strip.png`, `sequence-check.json`, `W4-CORRECTION.md`
- `godot-spike/tools/prepare_a4_frames.py`, `a4_style_check.py`, `a4_contact_sheet.py`, `check_a4_reproduction.py`, `package_a4_evidence.py`, `capture_a4.gd`
- under `shared-anim/`: `frame-audit.json`, `manifest.json`, `SOURCES.md`, `thoma-weapon-style-check.png`
- `godot-spike/tests/*`
- `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `8592fbb`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Do not change anything under `ui-prototype/`.** Never edit or move original PNGs.
- Godot 4.7.2 standard build, **GDScript only** for the game. Python is allowed for offline art tools. No C#, no GDExtension, no new addons beyond the vendored GUT.
- Don't change the rules, the HUD, the timing, the knights, the battlefield or props. G005 is untouched. Don't adopt the on-hold Ferry Dusk palette.
- **Do not change `thoma/idle/01.png` or `thoma/swing/05.png`.**
- **Mechanics stay exactly as in A4** (tested): canvas **512×512**, foot pivot **[256,464]**, mace length/head/grip, pose intent per frame (00 anticipation, 01 raise, 02 swing with smear hidden under Reduced Motion, 03 contact with the head on the contact anchor **[455,196]**, 04 follow-through), same `contact_frame_index`, **same manifest timing** (**180 ms** wind-up hold, **40 ms** swing, others unchanged), normal attack within the 1.7 s budget.
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Method and one-frame proof
- Write `godot-spike/docs/evidence/spike02-a5/METHOD.md`: what is kept from the A4 rig, and for each A4 P1/P2 item (shoulder seam, waist seam, cuff joins, cloned bag, hem/feet, 1.15× stretch, outline consistency) the concrete fix. Include per-frame notes for `swing/00`–`04`.
- Commit the seam masks (narrow bands only) under `godot-spike/docs/evidence/spike02-a5/seam-masks/` with JSON coordinates, and state their total pixel area per frame.
- Record the garment scale decision with an embroidery-motif width/spacing measurement versus the reference.
- Prove the method on **one** frame (pick the worst, e.g. `swing/03` or `swing/04`) as a draft, with a before (A4) / after crop of the shoulder, waist, cuff, bag and hem/feet.
- Commit.

### W2. Build `swing/00`–`04`
- Apply the method to all five frames. Keep **A4's live frames as a baseline** under `godot-spike/docs/evidence/spike02-a5/baseline-a4/` as byte copies with recorded hashes; they must not be in the live set or referenced by the manifest. Earlier baselines stay where they are.
- Clean up as before (alpha, halo, registration to the pivot). Record the palette distance before and after.
- Commit.

### W3. Per-region check
- `godot-spike/docs/evidence/spike02-a5/region-check.png`: for each swing frame, same-scale crops of **stole, embroidery, cuffs, hem, face/hair, palette swatch**, plus new crops of **shoulder seam, waist seam, bag, hem-to-feet/ground contact**, next to the matching crops from idle/01 and swing/05 and the A4 baseline, on a neutral dark background. Add a row at native 720p in-game size.
- Regenerate `shared-anim/thoma-weapon-style-check.png` with all 7 frames; keep the A4 version as `godot-spike/docs/evidence/spike02-a5/style-check-a4.png`.
- `sequence-strip.png` (onion-skin or flip strip idle/01 → 00 → 01 → 02 → 03 → 04 → 05). Check for popping: no embroidery appearing/vanishing, no cuff, hem or outline jumps, no bag appearing/duplicating, no colour flicker. Record a measurable proxy per adjacent pair (for example mean-colour delta inside region masks, and an outline/silhouette IoU or contour distance for the robe).
- For each frame `swing/00`–`04`, record PASS/FAIL in `shared-anim/frame-audit.json` for the six regions (**stole, embroidery, cuffs, hem, face/hair, palette**) **plus** `seams`, `bag_count` (must equal 1), `feet` (hem-to-feet and ground contact) and the sequence result, with a one-line reason per failure.
- **Remove PLACEHOLDER only on frames that pass every check.** An honest PLACEHOLDER beats a false PASS.
- Commit.

### W4. Sync, import, tests
- Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte, then regenerate `shared-anim/contact-sheet.png`.
- Headless import, then GUT. All tests green: **≥ 42** tests (A4 plus new). Add or extend tests for:
  - idle/01 and swing/05 byte-unchanged from A4
  - canvas, pivot, contact index, contact anchor and manifest timing unchanged
  - no baseline-a4/a3/a2 frame referenced by the manifest
  - PLACEHOLDER flags in `frame-audit.json` match the handoff table
  - every PASS frame has PASS on all regions, seams, bag_count == 1, feet and sequence
  - seam masks stay within their declared narrow bands (area limit)
- Save the log as `godot-spike/docs/evidence/spike02-a5/test-run.log`.
- Commit.

### W5. Evidence and verification
In `godot-spike/docs/evidence/spike02-a5/`, from a rendered run with a `CAPTURE_COMPLETE … pass=true` marker:
- `contact-sheet-a4-vs-a5.png`: the A4 baseline row against the new row, same scale.
- `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png` and `idle.png`, each at **1280×720 and 1920×1080** (`-1080p` suffix).
- A `--write-movie` capture at `--fixed-fps 60` of the open attack, strike to input-ready. Subsample if over about 8 MB and document it in `MOVIE.md`.
- `timing.json` (normal and Reduced Motion, all three setups) and `source-hashes.json`.

Add a **"spike-02 A5"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes. Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A5"** to `godot-spike/docs/HANDOFF.md` covering:
- how to run it (sync, import, play)
- the method in a few sentences, linking `METHOD.md` and the seam masks
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER, per-check results and reasons, linking `region-check.png`, `sequence-strip.png`, the style check and the A4-vs-A5 contact sheet
- timing (unchanged, measured) against the 1.7 s budget
- **Phase B: CANCELLED by Owner (2026-10-24, Godot chosen).** No React work remains in this spike. Note that P010 should be updated by the Owner to reflect the decision.
- what stays open: the human hit-feel playtest (**HUMAN_PENDING**), any remaining PLACEHOLDER frames
- limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`

Make this the handoff commit, then **stop**.

## Acceptance
- The A4 rig is the base; costume detail stays anchored to idle/01 and swing/05 pixels. Seam fixes are restricted to committed narrow seam masks; no new costume design.
- Every A4 P1/P2 item is addressed or honestly reported as still failing.
- `swing/00`–`04` rebuilt; mechanics and timing unchanged (tested); idle/01 and swing/05 byte-unchanged.
- Region check, sequence strip and per-check results in `frame-audit.json` committed. PLACEHOLDER removed only on frames that pass everything.
- A4 frames exist only as an evidence baseline, with hashes.
- 60 FPS clip and 720p + 1080p screenshots committed.
- GUT exits 0 with ≥ 42 tests; log committed.
- `git diff --stat 8592fbb..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
