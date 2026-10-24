# Task Godot spike 02 A7: one appearance spec for Thoma, then fix swing/00–04 frame by frame

Authorized by Gavin on 2026-10-24 13:12 (Asia/Taipei): 「照 GPT 的建議再做一輪，先寫統一外觀規格」 ("follow GPT's suggestion for one more round; write the unified appearance spec first").

## Owner decisions (unchanged)
- campaign-forge uses **Godot directly** (P010 accepted on branch `decision/p010-godot`). The React web version and Phase B are **CANCELLED**. Do not touch `ui-prototype/`, do not add React to-dos, do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**: dark iron flanged head, worn oak haft, small brass collar. Do not change its status or design.
- One consistent dark-fantasy hand-painted style. AI image generation is allowed. Do not adopt the on-hold Ferry Dusk palette.

This is a **small art segment** on top of spike-02 A6 (`e233171`).

## Why
The GPT review of A6 (`docs/review/gpt-godot-spike-02a6.md` on `origin/review/gpt-godot-spike`, `3f29156`) is **REJECT for art**, 0/5 frames pass. Engineering and verification were accepted (55 GUT tests, 2772 asserts).

| Region | A6 verdict |
| --- | --- |
| stole/sash | PARTIAL: shape and colour consistent, local folds and position drift |
| embroidery + tassels | FAIL: motif shape, position and tassels not consistent across frames |
| cuffs | PARTIAL: structure fine, folds and edges unstable |
| hem | PARTIAL: no fragments, but spread width and inner cloth outline jump |
| face/hair | FAIL: facial features and grey hair shape not stable across the five frames |
| palette, seams, bag count, feet | PASS |
| mace | PARTIAL: `swing/04` mace head ~19 px too high vs A5 |
| sequence | FAIL: hands, costume outline and details jump |

History in one line each:
- **A4/A5** (cutout rig from reference pixels): costume correct, structure broke (seams, detached shoes, fragments). A5 `swing/01` passed.
- **A6** (independent full-body `image_gen` per frame): structure fixed (seams, single bag, feet, palette), but identity and costume details drift frame to frame.

GPT's A7 recommendation, approved by the Owner:
1. **Stop regenerating frames independently.**
2. Lock `idle/01` and `swing/05` as immutable anchors.
3. Constrain all five frames with **one character appearance spec**; stabilise face/hair, embroidery, tassels and stole first.
4. Fix 00–04 **one frame at a time**, especially the `swing/04` mace head; do not break the feet and overall structure that already pass.
5. Re-check the asset sheet, per-region crops and real 720p playback; remove PLACEHOLDER only when a frame passes art acceptance.

Key principle (from the review): what needs fixing is **the same character staying consistent through a continuous motion**, not making single images prettier.

Read first:
- the A6 review: `git fetch origin review/gpt-godot-spike`, then `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a6.md` (and `...-02a5.md` for context)
- the **"spike-02 A6"** and **"spike-02 A5"** sections of `godot-spike/docs/HANDOFF.md` and `godot-spike/docs/VERIFICATION.md`
- `godot-spike/docs/evidence/spike02-a6/`: `METHOD.md`, `frame-status-table.md`, `region-check.png`, `region-crops.json`, `sequence-strip.png`, `sequence-check.json`, `playback-check.json`, `geometry-check.json`, `candidates/`, `baseline-a5/`, `normalized/`, `W3-OBSERVATIONS.md`
- `godot-spike/tools/prepare_a6_frames.py`, `prepare_a5_frames.py` and the A5/A6 check, contact-sheet, packaging and capture tools (reuse them where they fit)
- under `shared-anim/`: `frame-audit.json`, `manifest.json`, `SOURCES.md`, `a5-swing-prompts.json`, `a6-swing-prompts.json`, `thoma-weapon-style-check.png`
- `godot-spike/tests/*`
- `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `e233171`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Nothing under `ui-prototype/` changes.** Never edit or move original PNGs or earlier evidence/candidates.
- Godot 4.7.2 standard build, **GDScript only** for the game. Python is allowed for offline art tools. No C#, no GDExtension, no new addons beyond the vendored GUT.
- Don't change the rules, the HUD, the timing, the knights, the battlefield or props. Do not generate any other character or the environment. G005 is untouched.
- **`thoma/idle/01.png` and `thoma/swing/05.png` stay byte-identical.** They are the anchors and the only source of truth for appearance.
- **Mechanics stay exactly as in A6** (tested): canvas **512×512**, foot pivot **[256,464]**, mace length/head/grip, pose intent per frame (00 anticipation, 01 raise, 02 swing with smear hidden under Reduced Motion, 03 contact with the head on the contact anchor **[455,196]**, 04 follow-through), same `contact_frame_index`, **same manifest timing** (**180 ms** wind-up hold, **40 ms** swing, others unchanged), normal attack within the 1.7 s budget.
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Unified appearance spec + per-frame pose targets
Write `shared-anim/thoma-appearance-spec.md` plus a machine-readable `shared-anim/thoma-appearance-spec.json`, derived **only** from the pixels of `idle/01` and `swing/05` (measure, don't invent). Where the two anchors disagree, say so and pick one with the reason.
- **Face:** shape, features, eye/brow treatment, mouth, skin tones as hex (light/mid/shadow).
- **Hair:** silhouette, colour hex values, parting, length relative to ears/collar.
- **Each costume element:** robe, stole/sash (width, fall, fold lines), **embroidery motif** (exact pattern, repeat count and spacing in px, colours as hex), **tassels** (count, length, position, colour), cuffs, hem shape and layers, bag (exactly one, position), belt, shoes.
- **Mace:** dimensions in px (haft length, head size, collar), head/flange shape, colours, grip position in hand.
- **Body proportions in px:** head height, shoulder width, torso length, leg length, character height from pivot.
- **Palette list** (hex, with which region uses each) and **outline/brush style** (outline colour/width, shading treatment).
- **Annotated reference crops** from both anchors for every item: `godot-spike/docs/evidence/spike02-a7/spec-crops.png` (+ `spec-crops.json` with crop boxes).
- **Per-frame pose targets for `swing/00`–`04`**: landmark positions (head centre, eyes, both shoulders, elbows, hands, hips, knees, both feet, mace head, mace grip) so consecutive frames move smoothly from idle/01 to swing/05. The mace head positions must lie on one consistent swing arc, with `swing/03` exactly on the contact anchor **[455,196]** and feet on the pivot **[256,464]**. **Correct the `swing/04` mace head height against that arc** (A6 was ~19 px too high). Put the targets in the JSON and draw them as an overlay: `pose-targets.png`.
- Commit.

### W2. Fix the frames one at a time against the spec
Order: **`swing/01`, `swing/02`, `swing/00`, `swing/03`, `swing/04`** (01 first because A5's 01 had passed). Finish and record one frame before starting the next; already-fixed neighbours are a consistency check, never an appearance source.
- **Pick the best base per frame, per region,** from existing candidates: A5 frames (`baseline-a5/`), A6 adopted frames, and A6 raw candidates (`candidates/`). Record why. Combine **A6's correct structure** (single bag, connected feet, no seams) with the **anchors' exact face and embroidery**.
- **Fix the base to conform to the spec**, e.g. `image_gen` edit/inpaint constrained by the spec text and the two anchors as references (not independent full regeneration), plus targeted touch-up of face/hair/embroidery/tassels copied or redrawn from the anchors where the spec requires an exact match, and pose correction toward the W1 landmark targets. Do not break feet, seams or bag count that already pass. Any copied region must be blended so no seam is visible at 1× and 720p.
- **Max ~4 attempts per frame.** Save every attempt under `godot-spike/docs/evidence/spike02-a7/attempts/<frame>/attempt-<n>.png` with the inputs. If a frame cannot pass, keep PLACEHOLDER with the reason; do not burn more attempts.
- Keep **A6's live frames as a baseline** under `godot-spike/docs/evidence/spike02-a7/baseline-a6/` as byte copies with recorded hashes; they must not be referenced by the manifest.
- Normalize (canvas, scale, pivot, contact anchor, palette) with scale/translate only.
- Record every attempt, prompt, input/reference with SHA-256, tool, seed/settings (or "not exposed"), every touch-up (input hash, output hash, mask, what changed), and raw/runtime SHA-256 in `shared-anim/SOURCES.md` and a new `shared-anim/a7-swing-prompts.json`. Tools in e.g. `godot-spike/tools/prepare_a7_frames.py`.
- Commit.

### W3. Spec compliance, sheet, landmarks, real playback
- **Spec-compliance check per frame:** every spec item PASS/FAIL with crops next to the matching anchor crops: `spec-check.png` + `spec-check.json`.
- **Equal-scale transparent sheet** of all 7 frames and a **sequence strip** (idle/01 → 00 → 01 → 02 → 03 → 04 → 05). Regenerate `shared-anim/thoma-weapon-style-check.png`; keep the A6 version as `godot-spike/docs/evidence/spike02-a7/style-check-a6.png`.
- **Frame-to-frame landmark delta table** (face centre, both hands, mace head, both feet; plus character height) for every adjacent pair, against the W1 targets: `landmark-deltas.md` + `.json`. Flag jumps.
- **Real 720p playback flicker check** from a rendered Godot run (frame captures): no face/hair change, no embroidery or tassel appearing/vanishing/shifting, no cuff, hem, outline or shoe jumps, no bag changes, no colour flicker. Record a measurable proxy per adjacent pair (mean-colour delta inside region masks, silhouette IoU, height delta).
- For each frame `swing/00`–`04`, record PASS/FAIL in `shared-anim/frame-audit.json` for **face/hair, stole, embroidery, tassels, cuffs, hem, palette, seams, bag_count (== 1), feet, mace, landmarks, sequence**, with a one-line reason per failure.
- **Remove PLACEHOLDER only on frames that pass everything.** An honest PLACEHOLDER beats a false PASS. Model inspection is not Owner art approval.
- Commit.

### W4. Sync, import, tests
- Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte, then regenerate `shared-anim/contact-sheet.png`.
- Headless import, then GUT. All tests green: **≥ 55** tests (A6 plus new). Add or extend tests for:
  - idle/01 and swing/05 byte-unchanged
  - canvas, pivot, contact index, contact anchor and manifest timing (180 ms / 40 ms) unchanged
  - no baseline-a6/a5/a4/a3/a2 frame referenced by the manifest
  - appearance spec JSON exists and has every required section; pose targets exist for 00–04 with 03's mace head == [455,196]
  - PLACEHOLDER flags in `frame-audit.json` match the handoff table; every PASS frame passes all checks with bag_count == 1
  - every adopted A7 frame has recorded inputs, prompts and raw/runtime SHA-256 in `a7-swing-prompts.json`, with ≤ 4 attempts per frame
- Save the log as `godot-spike/docs/evidence/spike02-a7/test-run.log`.
- Commit.

### W5. Evidence and verification
In `godot-spike/docs/evidence/spike02-a7/`, from a rendered run with a `CAPTURE_COMPLETE … pass=true` marker:
- `contact-sheet-a6-vs-a7.png`: the A6 baseline row against the new row, same scale.
- the spec check, landmark table and playback check from W3.
- `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png` and `idle.png`, each at **1280×720 and 1920×1080** (`-1080p` suffix).
- A `--write-movie` capture at `--fixed-fps 60` of the open attack, strike to input-ready. Subsample if over about 8 MB and document it in `MOVIE.md`.
- `timing.json` (normal and Reduced Motion) and `source-hashes.json`.

Add a **"spike-02 A7"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes. Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A7"** to `godot-spike/docs/HANDOFF.md` covering:
- how to run it (sync, import, play)
- the spec and method in a few sentences, linking `thoma-appearance-spec.md`, `pose-targets.png`, the attempts folder and `a7-swing-prompts.json`
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER, per-check results and reasons, linking `spec-check.png`, `landmark-deltas.md`, `sequence-strip.png`, the style check and the A6-vs-A7 contact sheet
- attempts used per frame, which base was picked and what was changed
- the `swing/04` mace head before/after against the arc
- timing (unchanged, measured) against the 1.7 s budget
- what stays open: the human hit-feel playtest (**HUMAN_PENDING**), any remaining PLACEHOLDER frames, Owner art approval
- limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`

Make this the handoff commit, then **stop**.

## Acceptance
- One appearance spec (md + json) derived from the two anchors, with annotated crops and per-frame pose targets; `swing/04` mace head corrected against the arc.
- Frames fixed one at a time in order 01, 02, 00, 03, 04 against the spec; ≤ ~4 attempts per frame, every attempt saved and recorded.
- No regression on feet, seams, bag count or palette.
- Spec check, sheet, sequence strip, landmark delta table and real-playback flicker check committed; per-check results in `frame-audit.json`. PLACEHOLDER removed only on frames that pass everything.
- Mechanics and timing unchanged (tested); idle/01 and swing/05 byte-unchanged.
- A6 frames exist only as an evidence baseline, with hashes.
- 60 FPS clip and 720p + 1080p screenshots committed.
- GUT exits 0 with ≥ 55 tests; log committed.
- `git diff --stat e233171..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
