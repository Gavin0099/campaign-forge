# Task Godot spike 02 A8: one more AI pass for Thoma swing/00–04, driven by the commission brief, as one shared sheet

Authorized by Gavin on 2026-10-24 15:09 (Asia/Taipei), after reviewing the artist commission brief: 「再用AI畫一次看看」 ("try drawing it with AI once more").

## Owner decisions (unchanged)
- campaign-forge uses **Godot directly** (P010 accepted on branch `decision/p010-godot`). The React web version and Phase B are **CANCELLED**. Do not touch `ui-prototype/`, do not add React to-dos, do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**: dark iron flanged head, worn oak haft, small brass collar. Do not change its status or design.
- One consistent dark-fantasy hand-painted style. AI image generation is allowed. Do not adopt the on-hold Ferry Dusk palette.
- The commission brief (`docs/art-briefs/thoma-swing-commission.md`, `fdc796b`) stays valid as the fallback for a human artist. **Do not edit it or anything under `docs/art-briefs/`**; this segment only *uses* it.

This is a **small art segment** on top of spike-02 A7 (`042810a`) and the commission brief (`fdc796b`).

## Why
A5, A6 and A7 all ended **REJECT for art, 0/5 frames pass** (A7: Codex self-audit; the GPT review could not run).

| Round | Method | What broke |
| --- | --- | --- |
| A4/A5 | cutout rig from anchor pixels | seams, detached shoes, fragments (A5 `swing/01` passed once) |
| A6 | independent full-body `image_gen` per frame | face/hair, embroidery, tassels drift frame to frame; sequence jumps; `swing/04` mace +19 px |
| A7 | appearance spec + per-frame fix/inpaint | face/hair, stole, embroidery, tassels, cuffs still drift; sequence still jumps; even `swing/01` failed |

The common failure: **each frame was generated or fixed on its own**, so the model re-invents the character every time. A8 changes the method, not the polish:

1. **The commission brief is the single spec.** Its canvas rules, per-frame target table, guide overlays, appearance table, palette and 13-item checklist (section 6) are what an artist would get; A8 must meet the same bar.
2. **Generate all 5 middle frames together in ONE multi-panel sheet image**, with `idle/01` and `swing/05` placed in the same image as fixed panels, so the model paints one character once and shares face, costume and brush across every panel.
3. **Per-frame-independent regeneration is NOT the main method.** It is allowed only as a fallback, and then only as an *edit* that uses the best sheet panel as the identity reference.

Read first:
- `docs/art-briefs/thoma-swing-commission.md` (the whole file; sections 2, 3 and 6 are binding) and everything in `docs/art-briefs/thoma-swing/` (`refs/`, `guides/swing-00..04-guide.png`)
- `shared-anim/thoma-appearance-spec.md` and `.json` (A7 W1; the numeric source the brief summarises)
- the **"spike-02 A7"** and **"spike-02 A6"** sections of `godot-spike/docs/HANDOFF.md` and `godot-spike/docs/VERIFICATION.md`
- `godot-spike/docs/evidence/spike02-a7/`: `METHOD.md`, `W2-OPERATIONS.md`, `spec-check.*`, `landmark-deltas.*`, `sequence-check.json`, `playback-check.json`, `frame-status-table.md`, `attempts/`
- `godot-spike/tools/prepare_a7_frames.py`, the A6/A7 check, contact-sheet, packaging and capture tools (`capture_a7.gd` etc.); reuse them where they fit
- under `shared-anim/`: `frame-audit.json`, `manifest.json`, `SOURCES.md`, `a6-swing-prompts.json`, `a7-swing-prompts.json`, `README.md`
- `godot-spike/tests/*`, especially `test_a7_contract.gd` and how `test_a3`–`test_a6` contracts were re-pointed at archived baselines in earlier segments
- `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `fdc796b`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Nothing under `ui-prototype/` or `docs/art-briefs/` changes.** Never edit or move original PNGs or earlier evidence/candidates/attempts.
- Godot 4.7.2 standard build, **GDScript only** for the game. Python is allowed for offline art tools. No C#, no GDExtension, no new addons beyond the vendored GUT.
- Don't change the rules, the HUD, the timing, the knights, the battlefield or props. Do not generate any other character or the environment. G005 is untouched.
- **`thoma/idle/01.png` and `thoma/swing/05.png` stay byte-identical.** They are the anchors and the only source of truth for appearance.
- **Mechanics stay exactly as in A7** (tested): canvas **512×512 RGBA, straight alpha, transparent**, registration pivot **[256,464]**, ground **y = 464** (lowest opaque pixel y 463–465, at least one foot on the line), height ≈ 360 px (head top ≈ y 103), faces **screen-right**, drawn in place; mace-head centres **00 (192,85) · 01 (259,87) · 02 (449,110) · 03 (455,196) opaque contact · 04 (421,376)** within ±4 px; same `contact_frame_index` (3); **same manifest timing** (180 / 70 / 40 / 80 (+80 hitstop) / 100 / 150 ms); normal attack within the 1.7 s budget; Reduced Motion shows 00 / 03 / 05.
- Appearance per the brief section 3: grey short hair and squared grey beard, heavy brow, no smile; dark-teal over-robe on ivory under-robe; **two stole panels with ONE leaf-sprig embroidery each (2 total)**; short uneven fringes **L ≈ 10, R ≈ 8 (±1)** plus **exactly one** long knotted waist cord; **exactly one** brown satchel at screen-left hip with a cloth roll; ivory flared undersleeves; small bronze medallion; two worn brown boots attached to the legs; canon mace in the right hand; thin broken dark-brown contour, mottled low-contrast shading, no black vector lines, no cel shading.
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Build the generation inputs from the commission brief
- Write `godot-spike/tools/prepare_a8_sheet.py` that builds **one multi-panel sheet canvas**: 7 panels in a row (or a documented 4+3 grid if the image tool's aspect limits require it), each panel exactly 512×512 at the same scale, with a known panel layout recorded in JSON:
  - **panel 1 = `idle/01`** (exact pixels), **panel 7 = `swing/05`** (exact pixels);
  - **panels 2–6 = `swing/00`–`04`**, each containing that frame's guide (`docs/art-briefs/thoma-swing/guides/swing-NN-guide.png`: ground line, pivot, joint targets, mace arc and mace-head target) drawn as a light pose scaffold; optionally a faint A7 silhouette for pose only (never its face or costume details).
  - Flat neutral background that is easy to key out, or transparent if the tool keeps alpha; record which.
- Also prepare: an edit **mask** that leaves panels 1 and 7 untouched and opens panels 2–6; an identity reference image (`refs/anchors-2x.png`, `refs/spec-crops.png`); and a **sheet prompt** condensed from brief sections 2–4 (per-panel pose description, appearance table, palette notes, brush rules, "same character, same painting, panels 1 and 7 are fixed").
- Save inputs under `godot-spike/docs/evidence/spike02-a8/inputs/` (`sheet-canvas.png`, `sheet-mask.png`, `sheet-layout.json`, `sheet-prompt.txt`) with SHA-256 for each.
- Archive the five A7 live frames as byte copies under `godot-spike/docs/evidence/spike02-a8/baseline-a7/` with recorded hashes (they must not be referenced by the manifest).
- Commit.

### W2. Generate the five middle frames together, then slice and normalize
**Primary method (required first):** use built-in `image_gen` in **edit mode** on the W1 sheet canvas (anchors included as fixed panels, mask opening only panels 2–6) so all five frames are painted **in one image** and share identity and costume.
- **Up to ~4 sheet attempts.** Between attempts adjust only the prompt, mask or scaffold strength; record why. Save every attempt whole under `godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-<n>.png` with its inputs.
- Pick the best attempt for **cross-panel consistency first** (same face, same stole/embroidery/tassels, same bag), pose accuracy second. Record the choice and reasons in `METHOD.md`.
- **Slice** panels 2–6 by the recorded layout. **Normalize with scale/translate only** (uniform scale so height matches idle/01 ≈ 360 px; translate so feet sit on y = 464 and the pivot is [256,464]); then check each mace-head centre against its target. If a mace head is off by > 4 px after normalization, a **local** fix of the mace/forearm only is allowed (redraw or move that region with a seamless blend); record it. **Clean alpha**: key out the background, no halos or stray pixels, straight alpha, no guide remnants.
- Verify that panels 1 and 7 of the chosen attempt still resemble the anchors (a drift there means the model repainted the anchors; note it). The runtime anchors are always the original files, never the sheet's panels 1/7.
- **Fallback (only if no sheet attempt can hold the poses):** take the best sheet panel as the **identity reference** and do per-frame `image_gen` *edits* (not independent generation) of the failing frames, at most ~2 per frame, each with the identity panel + anchors as references. State clearly in `METHOD.md` and the handoff that the fallback was used and for which frames.
- Record every attempt, prompt, input/reference with SHA-256, tool, seed/settings (or "not exposed"), every local fix (input hash, output hash, mask, what changed), and raw/runtime SHA-256 in `shared-anim/SOURCES.md` and a new `shared-anim/a8-swing-prompts.json`. Install the chosen frames as `shared-anim/thoma/swing/00.png`–`04.png`.
- Commit.

### W3. Check against the commission brief
- **13-item acceptance checklist** from brief section 6 (`face_hair, stole, embroidery, tassels, cuffs, hem, palette, seams, bag_count, feet, mace, landmarks, sequence`) for each of `swing/00`–`04`, PASS/FAIL with a one-line reason per failure, crops next to the matching anchor crops: `checklist.png` + `checklist.json`. Plus the technical check (512×512, RGBA, transparent, no guide remnants, filenames).
- **Landmark / mace-target delta table**: measured vs brief target for head centre, both hands, elbows, knees, both feet, mace head, plus character height and lowest opaque y; and frame-to-frame deltas for every adjacent pair (idle/01 → 00 → … → 04 → 05). Flag anything outside ±4 px or any jump: `landmark-deltas.md` + `.json`.
- **Sequence strip** (idle/01 → 00 → 01 → 02 → 03 → 04 → 05, equal scale, transparent) and an **A7-vs-A8 contact sheet** (A7 baseline row over the A8 row, same scale): `sequence-strip.png`, `contact-sheet-a7-vs-a8.png`. Regenerate `shared-anim/thoma-weapon-style-check.png`; keep the A7 version as `godot-spike/docs/evidence/spike02-a8/style-check-a7.png`.
- **Real 720p flicker check** from a rendered Godot run (frame captures): no face/hair change, no embroidery or tassel appearing/vanishing/shifting, no cuff, hem, outline or shoe jumps, no bag changes, no colour flicker. Record a measurable proxy per adjacent pair (mean-colour delta inside region masks, silhouette IoU, height delta): `playback-check.json`.
- Write the results into `shared-anim/frame-audit.json` (`region_review`, all 13 items per frame, with the new SHA-256).
- **Mark a frame non-PLACEHOLDER only if it honestly passes all 13 items and the technical check.** An honest PLACEHOLDER beats a false PASS. Model inspection is not Owner art approval.
- Commit.

### W4. A8 swap-in test work, sync, import, tests
This is the "A8 swap-in" from brief section 7:
1. Re-point `godot-spike/tests/test_a7_contract.gd` at the archived `godot-spike/docs/evidence/spike02-a8/baseline-a7/` frames (same approach the A3–A6 contracts already use), so the A7 history stays tested without pinning the live frames.
2. Update `shared-anim/frame-audit.json` with the A8 hashes and 13-item results (W3).
3. Add `godot-spike/tests/test_a8_contract.gd` covering at least:
   - idle/01 and swing/05 byte-unchanged
   - 00–04 are 512×512 RGBA, lowest opaque pixel y 463–465, at least one foot on y = 464
   - mace-head centres within ±4 px of the brief targets; pixel (455,196) of `swing/03` opaque
   - canvas, pivot, contact index, contact anchor and manifest timing unchanged
   - no baseline-a7/a6/a5/a4/a3/a2 frame referenced by the manifest
   - PLACEHOLDER flags in `frame-audit.json` match the handoff table; every PASS frame has all 13 items PASS with bag_count == 1
   - every adopted A8 frame has recorded inputs, prompts and raw/runtime SHA-256 in `a8-swing-prompts.json`, with ≤ 4 sheet attempts (and ≤ 2 fallback edits per frame if used)
- Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte, then regenerate `shared-anim/contact-sheet.png`.
- Headless import, then GUT. All tests green: **≥ 63** tests (A7 plus new). Save the log as `godot-spike/docs/evidence/spike02-a8/test-run.log`.
- Commit.

### W5. Evidence and verification
In `godot-spike/docs/evidence/spike02-a8/`, from a rendered run with a `CAPTURE_COMPLETE … pass=true` marker (add `capture_a8.gd` or reuse `capture_a7.gd` with a new output dir):
- the checklist, landmark table, sequence strip, A7-vs-A8 contact sheet and playback check from W3; the sheet inputs and attempts from W1/W2.
- `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png` and `idle.png`, each at **1280×720 and 1920×1080** (`-1080p` suffix).
- A `--write-movie` capture at `--fixed-fps 60` of the open attack, strike to input-ready. Subsample if over about 8 MB and document it in `MOVIE.md`.
- `timing.json` (normal and Reduced Motion) and `source-hashes.json`.

Add a **"spike-02 A8"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes. Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A8"** to `godot-spike/docs/HANDOFF.md` covering:
- how to run it (sync, import, play)
- the method in a few sentences (brief-driven single sheet, anchors as fixed panels), linking `inputs/`, `sheet-attempts/`, `METHOD.md` and `a8-swing-prompts.json`; whether the fallback was used and for which frames
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER, all 13 items per frame and reasons, linking `checklist.png`, `landmark-deltas.md`, `sequence-strip.png`, the style check and the A7-vs-A8 contact sheet
- sheet attempts used, which one was chosen and why, and any local fixes
- mace-head measured vs target per frame
- timing (unchanged, measured) against the 1.7 s budget
- a short honest comparison with A7: what improved, what still fails
- what stays open: the human hit-feel playtest (**HUMAN_PENDING**), any remaining PLACEHOLDER frames, Owner art approval, and whether the commission brief is still needed
- limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`

Make this the handoff commit, then **stop**.

## Acceptance
- Sheet inputs built from the commission brief (anchors as fixed panels, guides for 00–04), with hashes.
- The five frames generated together in one sheet image (≤ ~4 attempts, all saved and recorded); fallback per-frame edits only if needed, documented, and identity-referenced to the best sheet panel.
- Frames sliced and normalized by scale/translate only (plus documented local mace fixes), alpha clean, on the brief's pivot, ground and mace targets.
- 13-item checklist, landmark/mace delta table, sequence strip, A7-vs-A8 contact sheet and real 720p flicker check committed; results in `frame-audit.json`. PLACEHOLDER removed only on frames that pass everything.
- Mechanics and timing unchanged (tested); idle/01 and swing/05 byte-unchanged; A7 frames only as an evidence baseline with hashes; `test_a7_contract` reads the baseline; `test_a8_contract` added.
- 60 FPS clip and 720p + 1080p screenshots committed.
- GUT exits 0 with ≥ 63 tests; log committed.
- `git diff --stat fdc796b..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` or `docs/art-briefs/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
