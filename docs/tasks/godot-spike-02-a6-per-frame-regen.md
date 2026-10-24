# Task Godot spike 02 A6: regenerate Thoma's failing swing frames one frame at a time

Authorized by Gavin on 2026-10-24 12:13 (Asia/Taipei): 「一格一格重新生成，以待機和收勢為準」 ("regenerate frame by frame, anchored to idle and recover").

## Owner decisions (unchanged)
- campaign-forge uses **Godot directly** (P010 accepted on branch `decision/p010-godot`). The React web version and Phase B are **CANCELLED**. Do not touch `ui-prototype/`, do not add React to-dos, do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**: dark iron flanged head, worn oak haft, small brass collar. Do not change its status or design.
- One consistent dark-fantasy hand-painted style. Do not adopt the on-hold Ferry Dusk palette.

This is a **small art segment** on top of spike-02 A5 (`78bb38a`).

## Why
The GPT review of A5 (`docs/review/gpt-godot-spike-02a5.md` on `origin/review/gpt-godot-spike`, `d590e91`) is **REJECT for art**: only `swing/01` passes (it still needs a playback seam-flicker check). Engineering and verification were accepted (48 GUT tests, 2126 asserts). Stole, embroidery and bag (exactly one) pass.

| Frame | A5 failure |
| --- | --- |
| `swing/00` | detached right shoe; broken hem/leg outline |
| `swing/01` | passes; needs a seam-flicker check in real playback |
| `swing/02` | sleeve fragments; triangular hem fragment; legs separated from shoes |
| `swing/03` | unnatural sleeve piece; seam under the swinging arm |
| `swing/04` | floating hem fragment; bad leg/shoe join |

A2–A5 tried whole-frame generation without anchoring (A2/A3: costume drift), then patch repaint and a cutout rig (A4/A5: seams, fragments, detached feet). GPT's recommendation: **stop patching the cutout rig.** Generate each failing frame as a **complete new full-body frame**, anchored to `idle/01` and `swing/05`, touch up by hand, check each at equal scale on a transparent background, then accept only in real playback.

## Method: one frame at a time, anchored generation
- For each target frame, generate a **complete full-body frame** (not patches, not a re-composite of rig pieces) with the built-in image generation tool that earlier segments used (see `shared-anim/SOURCES.md`; A2–A5 used `image_gen (built-in)`).
- **Image references for every attempt:** `thoma/idle/01.png` and `thoma/swing/05.png` (costume, face/hair, palette, brush and ink treatment, mace design), plus the **A5 frame of the same index only as a pose/silhouette guide** (pose, mace position and angle, contact geometry, stance). The prompt must say explicitly that the A5 frame defines pose only and that all costume detail comes from idle/01 and swing/05. No other references.
- **At most 4 attempts per frame.** Save every candidate (raw output, unchanged) under `godot-spike/docs/evidence/spike02-a6/candidates/<frame>/attempt-<n>.png`, with the pick and the reason.
- **Touch-up is limited** to small defects: background/alpha cleanup, alpha edge and halo fixes, stray pixels, and palette matching to idle/01 (a recorded palette remap). Do **not** re-composite costume pieces from idle/01, swing/05 or the A5 rig into the generated frame; that is what failed in A4/A5. Any manual or scripted touch-up must be recorded (input hash, output hash, mask, what changed).
- **Normalize** every adopted frame to the same 512×512 canvas, the same character scale as idle/01 (head-to-ground height within a stated tolerance), foot pivot **[256,464]**, contact anchor **[455,196]** on `swing/03`, and the idle/01 palette. Normalization is scale/translate only; no warping of costume regions.
- Everything recorded and reproducible: exact prompts, references with SHA-256, tool, any seed/settings the tool exposes (write "not exposed" if none), raw and runtime SHA-256, cleanup steps, in `shared-anim/SOURCES.md` and a new `shared-anim/a6-swing-prompts.json`. Scripts for normalization and cleanup in e.g. `godot-spike/tools/prepare_a6_frames.py`.

Read first:
- the A5 review: `git fetch origin review/gpt-godot-spike`, then `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a5.md` (and `...-02a4.md` for context)
- the **"spike-02 A5"** section of `godot-spike/docs/HANDOFF.md` and `godot-spike/docs/VERIFICATION.md#spike-02-a5`, plus the A2–A4 sections for which image-generation tooling worked here
- `godot-spike/docs/evidence/spike02-a5/`: `METHOD.md`, `frame-status-table.md`, `region-check.png`, `sequence-strip.png`, `sequence-check.json`, `region-crops.json`
- `godot-spike/tools/prepare_a5_frames.py` and the A4/A5 check, contact-sheet, packaging and capture tools (reuse them where they fit)
- under `shared-anim/`: `frame-audit.json`, `manifest.json`, `SOURCES.md`, `a5-swing-prompts.json`, `thoma-weapon-style-check.png`
- `godot-spike/tests/*`
- `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `78bb38a`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Nothing under `ui-prototype/` changes.** Never edit or move original PNGs.
- Godot 4.7.2 standard build, **GDScript only** for the game. Python is allowed for offline art tools. No C#, no GDExtension, no new addons beyond the vendored GUT.
- Don't change the rules, the HUD, the timing, the knights, the battlefield or props. Do not generate any other character or the environment. G005 is untouched.
- **`thoma/idle/01.png` and `thoma/swing/05.png` stay byte-identical.**
- **Mechanics stay exactly as in A5** (tested): canvas **512×512**, foot pivot **[256,464]**, mace length/head/grip, pose intent per frame (00 anticipation, 01 raise, 02 swing with smear hidden under Reduced Motion, 03 contact with the head on the contact anchor **[455,196]**, 04 follow-through), same `contact_frame_index`, **same manifest timing** (**180 ms** wind-up hold, **40 ms** swing, others unchanged), normal attack within the 1.7 s budget.
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Method, tooling and proof on `swing/02`
- Write `godot-spike/docs/evidence/spike02-a6/METHOD.md`: tool used, the reference set, the prompt template, the attempt limit, allowed touch-up, normalization, and how this differs from A4/A5.
- **Prove the method on `swing/02` first** (the worst A5 frame). Up to 4 attempts, all saved. Produce `proof-02.png`: A5 `swing/02` vs the best A6 candidate vs idle/01 and swing/05, at equal scale on a transparent/neutral background, with crops of stole, embroidery, cuffs/sleeves, hem, legs/shoes, face/hair, mace.
- **Gate:** if no `swing/02` candidate clearly beats A5 (no sleeve fragments, no hem fragment, legs connected to shoes, costume consistent with idle/01 and swing/05), **stop after the W1 commit** and write the reason into a short "spike-02 A6 (stopped at W1)" section in `godot-spike/docs/HANDOFF.md`. Do not burn attempts on the other frames.
- Commit.

### W2. Regenerate `swing/00`, `02`, `03`, `04`, one at a time
- One frame at a time, same method, up to 4 attempts each; finish and record one frame before starting the next. Use already-adopted A6 neighbours only as an extra consistency check, never as a costume source.
- **Keep `swing/01`** (A5 pass) unless it visibly pops against the new neighbours; if so, regenerate it too and record why with a side-by-side.
- Keep **A5's live frames as a baseline** under `godot-spike/docs/evidence/spike02-a6/baseline-a5/` as byte copies with recorded hashes; they must not be in the live set or referenced by the manifest. Earlier baselines stay where they are.
- Normalize (canvas, scale, pivot, contact anchor, palette) and clean up. Record palette distance to idle/01 before and after.
- Commit.

### W3. Per-frame and sequence check
- `godot-spike/docs/evidence/spike02-a6/region-check.png`: each swing frame at equal scale on a transparent/neutral background, with per-region crops of **stole, embroidery, cuffs, hem, seams, bag (count), feet/shoes connected to legs, face/hair, palette swatch, mace shape**, next to the matching crops from idle/01, swing/05 and the A5 baseline. Add a row at native 720p in-game size.
- Regenerate `shared-anim/thoma-weapon-style-check.png` with all 7 frames; keep the A5 version as `godot-spike/docs/evidence/spike02-a6/style-check-a5.png`.
- `sequence-strip.png` (idle/01 → 00 → 01 → 02 → 03 → 04 → 05) plus a popping/flicker check **in actual Godot playback** (frame captures from a rendered run): no embroidery appearing/vanishing, no cuff, hem, outline or shoe jumps, no bag appearing/duplicating, no colour flicker, no seam flicker on `swing/01`. Record a measurable proxy per adjacent pair (mean-colour delta inside region masks, robe silhouette IoU or contour distance, character height delta).
- For each frame `swing/00`–`04`, record PASS/FAIL in `shared-anim/frame-audit.json` for **stole, embroidery, cuffs, hem, face/hair, palette, seams, bag_count (== 1), feet, mace, sequence**, with a one-line reason per failure.
- **Remove PLACEHOLDER only on frames that pass every check.** An honest PLACEHOLDER beats a false PASS. Model inspection is not Owner art approval.
- Commit.

### W4. Sync, import, tests
- Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte, then regenerate `shared-anim/contact-sheet.png`.
- Headless import, then GUT. All tests green: **≥ 48** tests (A5 plus new). Add or extend tests for:
  - idle/01 and swing/05 byte-unchanged
  - canvas, pivot, contact index, contact anchor and manifest timing unchanged
  - no baseline-a5/a4/a3/a2 frame referenced by the manifest
  - PLACEHOLDER flags in `frame-audit.json` match the handoff table
  - every PASS frame has PASS on all checks, bag_count == 1
  - every adopted A6 frame has a recorded prompt, references and raw/runtime SHA-256 in `a6-swing-prompts.json`, with ≤ 4 attempts per frame
- Save the log as `godot-spike/docs/evidence/spike02-a6/test-run.log`.
- Commit.

### W5. Evidence and verification
In `godot-spike/docs/evidence/spike02-a6/`, from a rendered run with a `CAPTURE_COMPLETE … pass=true` marker:
- `contact-sheet-a5-vs-a6.png`: the A5 baseline row against the new row, same scale.
- `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png` and `idle.png`, each at **1280×720 and 1920×1080** (`-1080p` suffix).
- A `--write-movie` capture at `--fixed-fps 60` of the open attack, strike to input-ready. Subsample if over about 8 MB and document it in `MOVIE.md`.
- `timing.json` (normal and Reduced Motion, all three setups) and `source-hashes.json`.

Add a **"spike-02 A6"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes. Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A6"** to `godot-spike/docs/HANDOFF.md` covering:
- how to run it (sync, import, play)
- the method in a few sentences, linking `METHOD.md`, the candidates folder and `a6-swing-prompts.json`
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER, per-check results and reasons, linking `region-check.png`, `sequence-strip.png`, the style check and the A5-vs-A6 contact sheet
- attempts used per frame and which candidate was adopted
- timing (unchanged, measured) against the 1.7 s budget
- what stays open: the human hit-feel playtest (**HUMAN_PENDING**), any remaining PLACEHOLDER frames, Owner art approval
- limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`

Make this the handoff commit, then **stop**.

## Acceptance
- Failing frames regenerated as complete frames, one at a time, anchored to idle/01 and swing/05; no costume re-compositing; ≤ 4 attempts per frame, all candidates saved; prompts and references recorded.
- The `swing/02` proof gate was applied honestly.
- Mechanics and timing unchanged (tested); idle/01 and swing/05 byte-unchanged.
- Region check, sequence strip with real-playback flicker check, and per-check results in `frame-audit.json` committed. PLACEHOLDER removed only on frames that pass everything.
- A5 frames exist only as an evidence baseline, with hashes.
- 60 FPS clip and 720p + 1080p screenshots committed.
- GUT exits 0 with ≥ 48 tests; log committed.
- `git diff --stat 78bb38a..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit (or the W1 gate stop) and wait for review.
