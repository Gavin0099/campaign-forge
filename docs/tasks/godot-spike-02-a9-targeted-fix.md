# Task Godot spike 02 A9: targeted, region-limited AI fixes on the A8 swing frames (no regeneration)

Authorized by Gavin on 2026-10-24 17:35 (Asia/Taipei), after the A8 review: 「再用 AI 修一輪」 ("fix it with AI one more round").

## Owner decisions (unchanged)
- campaign-forge uses **Godot directly** (P010 accepted on branch `decision/p010-godot`). The React web version and Phase B are **CANCELLED**. Do not touch `ui-prototype/`, do not add React to-dos, do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**: dark iron flanged head, worn oak haft, small brass collar. Do not change its status or design.
- One consistent dark-fantasy hand-painted style. AI image generation is allowed. Do not adopt the on-hold Ferry Dusk palette.
- The commission brief (`docs/art-briefs/thoma-swing-commission.md`, `fdc796b`) stays valid as the fallback for a human artist and is the **spec** for this segment. **Do not edit it or anything under `docs/art-briefs/`**.

This is a **small art segment** on top of spike-02 A8 (`dcc949c`).

## Why
A8 painted `swing/00`–`04` in one shared sheet. The painted look is more consistent than A7, and all mace heads are within 4 px of the brief targets. The GPT web review (Medium, `docs/review/gpt-godot-spike-02a8.md` on `review/gpt-godot-spike`, `9c14c34`) gave **CONDITIONAL ACCEPT** as a development placeholder, but the Codex self-audit was **0/5**:

| Defect (A8 self-audit) | Frames |
| --- | --- |
| face/hair: broader grey crown, softer beard/cheek, changed brow vs anchors | 00–04 |
| stole wider than anchors; embroidery, tassels, seams differ | 00–04 |
| mace art compressed (head/haft squashed) | 00, 01 |
| stance too wide | 03 |
| front foot lands at the wrong spot | 04 |
| landmarks / sequence FAIL (jumps vs idle/01 and swing/05) | 00–04 |

| Round | Method | What broke |
| --- | --- | --- |
| A4/A5 | cutout rig from anchor pixels | seams, detached shoes, fragments |
| A6 | independent full-body `image_gen` per frame | identity and costume drift per frame |
| A7 | appearance spec + per-frame fix/inpaint | face, stole, embroidery, tassels, cuffs still drift |
| A8 | one shared multi-panel sheet | consistent between middle frames, but face/stole differ from the anchors; pose defects above |

A9 changes the method again: **A8 frames are the base. NO regeneration of whole frames or sheets.** Only **targeted, region-limited fixes**, where the identity regions come from the **anchor pixels themselves** (`idle/01`, `swing/05`) and AI is only used to blend small seams and lighting.

Read first:
- `docs/art-briefs/thoma-swing-commission.md` (whole file; sections 2, 3 and 6 are binding) and `docs/art-briefs/thoma-swing/` (`refs/`, `guides/swing-00..04-guide.png`)
- `shared-anim/thoma-appearance-spec.md` and `.json`
- the **"spike-02 A8"** and **"spike-02 A7"** sections of `godot-spike/docs/HANDOFF.md` and `godot-spike/docs/VERIFICATION.md`
- `godot-spike/docs/evidence/spike02-a8/`: `METHOD.md`, `checklist.json`/`.png`, `landmark-deltas.*`, `sequence-check.json`, `playback-check.json`, `frame-status-table.md`, `W3-OBSERVATIONS.md`, `final-mace-centres.json`, `normalized/`
- `godot-spike/tools/prepare_a8_sheet.py`, `adopt_a8_sheet.py`, `a8_contact_sheet.py`, `a8_playback_check.py`, `a8_style_check.py`, `capture_a8.gd`, `package_a8_evidence.py`, `update_a8_historical_tests.py`; reuse them where they fit
- under `shared-anim/`: `frame-audit.json`, `manifest.json`, `SOURCES.md`, `a8-swing-prompts.json`, `README.md`
- `godot-spike/tests/*`, especially `test_a8_contract.gd` and how `test_a3`–`test_a7` contracts were re-pointed at archived baselines
- `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `dcc949c`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Nothing under `ui-prototype/` or `docs/art-briefs/` changes.** Never edit or move original PNGs or earlier evidence/candidates/attempts.
- Godot 4.7.2 standard build, **GDScript only** for the game. Python is allowed for offline art tools. No C#, no GDExtension, no new addons beyond the vendored GUT.
- Don't change the rules, the HUD, the timing, the knights, the battlefield or props. Do not generate any other character or the environment. G005 is untouched.
- **`thoma/idle/01.png` and `thoma/swing/05.png` stay byte-identical.** They are the anchors and the only source of truth for appearance.
- **No whole-frame or whole-sheet regeneration.** Every change must be confined to a recorded region mask on an A8 frame. `image_gen` may be used only as a **small local edit** inside a mask (seam/edge/lighting blend, or redrawing a mace/foot region), never to repaint the whole figure.
- **Mechanics stay exactly as in A8** (tested): canvas **512×512 RGBA, straight alpha, transparent**, registration pivot **[256,464]**, ground **y = 464** (lowest opaque pixel y 463–465, at least one foot on the line), height ≈ 360 px, faces **screen-right**, drawn in place; mace-head centres **00 (192,85) · 01 (259,87) · 02 (449,110) · 03 (455,196) opaque contact · 04 (421,376)** within ±4 px; same `contact_frame_index` (3); **same manifest timing** (180 / 70 / 40 / 80 (+80 hitstop) / 100 / 150 ms); normal attack within the 1.7 s budget; Reduced Motion shows 00 / 03 / 05.
- Appearance per the brief section 3 (grey short hair, squared grey beard, heavy brow, no smile; dark-teal over-robe on ivory under-robe; two stole panels with ONE leaf-sprig embroidery each; fringes L ≈ 10, R ≈ 8 (±1) plus exactly one long knotted waist cord; exactly one brown satchel at screen-left hip; ivory flared undersleeves; small bronze medallion; two worn brown boots attached to the legs; canon mace in the right hand; thin broken dark-brown contour, mottled low-contrast shading).
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Defect list, region masks and measured targets
- Archive the five A8 live frames as byte copies under `godot-spike/docs/evidence/spike02-a9/baseline-a8/` with SHA-256 (they must not be referenced by the manifest).
- For each of `swing/00`–`04`, write a **per-frame defect list** taken from the A8 audit (`checklist.json`, `landmark-deltas.json`, `W3-OBSERVATIONS.md`), item by item, with the A8 PASS/FAIL state of all 13 items (this is the regression baseline for W2).
- Build **region masks** per frame (PNG, 512×512, one per region): `head` (face/hair/beard), `stole`, `embroidery`, `tassels`, `mace` (head + haft + hand grip), `legs_feet`. Also the matching source regions on `idle/01` and `swing/05`.
- For each region, record a **measured target** from the anchors/brief: head centre, head width/height, brow/beard extents; stole width and panel edges; embroidery count and position; fringe counts L/R; mace head centre, haft length and head size from canon `swing/05`; foot positions and stance width from the brief guides. Save as `godot-spike/docs/evidence/spike02-a9/defects-and-targets.json` + `.md`, masks under `masks/`.
- Write the tool(s) as `godot-spike/tools/prepare_a9_regions.py`.
- Commit.

### W2. Targeted fixes: identity transplant and pose repairs
Fix frames in this order: **03, 02, 04, 00, 01**. **At most ~3 attempts per region per frame.**
1. **Identity transplant.** Take the head/face/hair (and stole/embroidery/tassel patches where the pose allows) **from `idle/01` or `swing/05` pixels**, transform it (rotate/scale/shift only, recorded matrix) onto the A8 frame inside the region mask. Then use a **small local `image_gen` edit inside a narrow seam mask, or manual paint in Python**, only to blend edges and lighting. Do not let the edit repaint the transplanted face.
2. **Pose repairs:**
   - `00`, `01`: redraw/straighten the mace with **no compression**, using the canon mace from `swing/05` (transform its pixels to the frame's grip and the brief mace-head target), keep the hand on the grip.
   - `03`: narrow the stance to the brief guide; keep the mace head opaque at (455,196).
   - `04`: move the front foot to the brief target; feet stay attached, lowest opaque y 463–465.
3. **Regression gate.** After each region fix, re-check the 13 items for that frame. If the fixed version is **worse than A8 on any item that previously passed** (or on the mace target / ground), **keep the A8 pixels for that region** and record why.
- Clean alpha (no halos, stray pixels, guide remnants), straight alpha.
- Save every attempt under `godot-spike/docs/evidence/spike02-a9/attempts/<frame>/<region>-<n>.png` with its mask and transform.
- Record every operation (frame, region, source anchor, transform, mask hash, tool, prompt if `image_gen`, input/output SHA-256, kept or reverted and why) in `shared-anim/SOURCES.md` and a new `godot-spike/docs/evidence/spike02-a9/a9-fix-log.json`. Write the tool(s) as `godot-spike/tools/fix_a9_regions.py`. Describe the method in `METHOD.md`.
- Install the results as `shared-anim/thoma/swing/00.png`–`04.png`.
- Commit.

### W3. Check against the commission brief
- **13-item checklist** from brief section 6 (`face_hair, stole, embroidery, tassels, cuffs, hem, palette, seams, bag_count, feet, mace, landmarks, sequence`) for each of `swing/00`–`04`, PASS/FAIL with a one-line reason per failure and anchor crops: `checklist.png` + `checklist.json`, plus an **A8 → A9 change column** per item (improved / same / worse). Plus the technical check (512×512, RGBA, transparent, no remnants, filenames).
- **Landmark / mace delta table**: measured vs brief target for head centre, hands, elbows, knees, feet, mace head, height, lowest opaque y; frame-to-frame deltas for every adjacent pair (idle/01 → 00 → … → 04 → 05). Flag anything outside ±4 px or any jump: `landmark-deltas.md` + `.json`.
- **A8-vs-A9 contact sheet** (A8 row over A9 row, same scale, with `idle/01` at the left end and `swing/05` at the right end of both rows): `contact-sheet-a8-vs-a9.png`. **Sequence strip** (idle/01 → 00 … 04 → 05): `sequence-strip.png`. Regenerate `shared-anim/thoma-weapon-style-check.png`; keep the A8 version as `style-check-a8.png` in the evidence folder.
- **Real 720p flicker check** from a rendered Godot run (mean-colour delta inside region masks, silhouette IoU, height delta per adjacent pair): `playback-check.json`.
- Update `shared-anim/frame-audit.json` (`region_review`, all 13 items per frame, new SHA-256).
- **Mark a frame non-PLACEHOLDER only if it honestly passes all 13 items and the technical check.** An honest PLACEHOLDER beats a false PASS. Model inspection is not Owner art approval.
- Commit.

### W4. Tests
1. Re-point `godot-spike/tests/test_a8_contract.gd` at `godot-spike/docs/evidence/spike02-a9/baseline-a8/` (same approach as the A3–A7 contracts), so A8 history stays tested without pinning the live frames.
2. Add `godot-spike/tests/test_a9_contract.gd` covering at least:
   - idle/01 and swing/05 byte-unchanged
   - 00–04 are 512×512 RGBA, lowest opaque pixel y 463–465, at least one foot on y = 464
   - mace-head centres within ±4 px of the brief targets; pixel (455,196) of `swing/03` opaque
   - canvas, pivot, contact index, contact anchor and manifest timing unchanged
   - no baseline frame (a8/a7/…/a2) referenced by the manifest
   - PLACEHOLDER flags in `frame-audit.json` match the handoff table; every PASS frame has all 13 items PASS with bag_count == 1
   - every changed region has an entry in `a9-fix-log.json` with mask hash and input/output SHA-256; ≤ 3 attempts per region per frame; no entry is a whole-frame regeneration
3. Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte; regenerate `shared-anim/contact-sheet.png`.
- Headless import, then GUT. All green: **≥ 71** tests. Save the log as `godot-spike/docs/evidence/spike02-a9/test-run.log`.
- Commit.

### W5. Evidence and verification
In `godot-spike/docs/evidence/spike02-a9/`, from a rendered run with a `CAPTURE_COMPLETE … pass=true` marker (add `capture_a9.gd` or reuse `capture_a8.gd` with a new output dir):
- everything from W1–W3;
- `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png`, `idle.png`, each at **1280×720 and 1920×1080** (`-1080p` suffix);
- a `--write-movie` capture at `--fixed-fps 60` of the open attack, strike to input-ready (subsample if over ~8 MB; document in `MOVIE.md`);
- `timing.json` (normal and Reduced Motion) and `source-hashes.json`.

Add a **"spike-02 A9"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes. Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A9"** to `godot-spike/docs/HANDOFF.md` covering:
- how to run it (sync, import, play)
- the method in a few sentences (A8 base, region masks, identity transplant from anchors, local blends, pose repairs, regression gate), linking `defects-and-targets.md`, `masks/`, `attempts/`, `METHOD.md`, `a9-fix-log.json`
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER, all 13 items per frame with reasons and the A8 → A9 change, linking `checklist.png`, `landmark-deltas.md`, `sequence-strip.png`, the style check and the A8-vs-A9 contact sheet
- which regions were kept from A8 by the regression gate and why
- mace-head measured vs target per frame
- timing (unchanged, measured) against the 1.7 s budget
- an honest A8 vs A9 comparison: what improved, what still fails
- what stays open: the human hit-feel playtest (**HUMAN_PENDING**), any remaining PLACEHOLDER frames, Owner art approval, and whether the commission brief is still needed
- limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`

Make this the handoff commit, then **stop**.

## Acceptance
- Defect list, region masks and measured targets committed; A8 frames archived as `baseline-a8/` with hashes.
- Only region-limited fixes on A8 frames (identity transplanted from anchor pixels; local blends; mace/stance/foot repairs), ≤ ~3 attempts per region, all logged in `SOURCES.md` and `a9-fix-log.json`; regression gate applied and documented. No whole-frame or whole-sheet regeneration.
- 13-item checklist with A8 → A9 change column, landmark/mace delta table, A8-vs-A9 contact sheet (anchors at both ends), sequence strip and real 720p flicker check committed; `frame-audit.json` updated. PLACEHOLDER removed only on frames that pass everything.
- Mechanics and timing unchanged (tested); idle/01 and swing/05 byte-unchanged; `test_a8_contract` reads `baseline-a8/`; `test_a9_contract` added.
- 60 FPS clip and 720p + 1080p screenshots committed.
- GUT exits 0 with ≥ 71 tests; log committed.
- `git diff --stat dcc949c..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` or `docs/art-briefs/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
