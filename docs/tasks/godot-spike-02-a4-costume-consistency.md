# Task Godot spike 02 A4: make Thoma's 5 swing frames match the costume by building from the reference frames

Authorized by Gavin on 2026-10-24 (Asia/Taipei): 「先再修一次 5 格揮擊的衣服細節」 ("Fix the costume details on the 5 swing frames one more time first").

This is a **small art-fix segment** on top of spike-02 A3 (`bd80c5e`). It runs **before** Phase B. **Do not start Phase B** (`docs/tasks/godot-spike-02-swing-and-ab.md`) and **do not touch React** (`ui-prototype/`). The engine decision (P010) stays **PROPOSED**. Thoma's short one-handed flanged mace is already **APPROVED (Owner, 2026-10-24)**; do not change its status or design.

## Why
The GPT review of A3 (`docs/review/gpt-godot-spike-02a3.md` on `origin/review/gpt-godot-spike`) returned **CONDITIONAL ACCEPT**, no P0. W2 was **PARTIAL**: geometry and the contact position were kept, but the **costume seams, embroidery, cuffs and hem still do not match**. All five frames `thoma/swing/00`–`04` are still **PLACEHOLDER**. Only `thoma/idle/01` and `thoma/swing/05` (recover) pass. Remaining failures, from `godot-spike/docs/evidence/spike02-a3/frame-status-table.md`:

| Frame | A3 failure |
| --- | --- |
| `swing/00` | doubled border/leaf density at patch edges; raised cuff transition and broad fan hem differ from idle/recover |
| `swing/01` | stole border blending and raised cuff folds differ; bell-shaped hem retained from A2 |
| `swing/02` | compressed leaf detail, cuff patch boundary and swept underskirt contour drift |
| `swing/03` | stole seam/leaf density and broad underskirt hem inconsistent at detail scale |
| `swing/04` | stretched diagonal embroidery, front cuff transition and trailing hem visibly different |

## Change the method, not just retry
A2 regenerated whole frames, and A3 generated new figures and adopted generated cuff/hem cloth patches plus sprigs transplanted from the original. The costume still drifted, and A3 explicitly **left the old A2 hem contour unresolved**. **A4 must not be a fourth round of "generate, then patch".**

**Required method: reference-anchored costume transfer.**
- The costume pixels of `thoma/idle/01.png` and `thoma/swing/05.png` are the **source of truth**. That covers the stole/cape band and its embroidery (leaf sprigs, border lines, seams), the cuffs, the hem and underskirt silhouette, the satchel, the medallion, the robe and stole colors, and the face, beard and hair.
- For each swing frame, **carry those regions across from the reference**: cut the matching region from idle/01 or swing/05 (whichever pose is closer), then fit it onto the swing pose by paint-over, compositing and warping. Use moves such as affine or perspective warps, mesh or piecewise warps along the stole and hem curves, and rotation of cuff segments with the forearm. The embroidery must come out at the **same density, spacing and stroke** as the reference. Keep scale changes moderate so motifs don't stretch, and **never double or overlap** a border or leaf row at a seam.
- **Generate or freshly paint only regions that must change for the motion**: arms and hands, the mace, the torso twist, and where the cloth sweeps in the swing direction. Repaint the **hem contour** so its shape matches the reference hem; the A2/A3 fan or bell shapes must go. Deformation for motion is fine, but the hem and edge treatment must read as the same garment. You may change the alpha/silhouette in the hem region to do this. The feet, the pivot and the mace stay exactly where they are.
- If you think another method anchors better to the reference pixels, you may use it, for example a scripted layered or cutout rig built from idle/swing05 parts. You must **justify it in W1** with a small proof on one frame. Any method that invents costume detail from scratch through image generation is **not** acceptable as the main method.
- Everything must be **reproducible from scripts** (for example a new `godot-spike/tools/prepare_a4_frames.py`), with the masks, warp control points and source regions committed. A human-like manual paint-over pass is allowed if it is recorded: the inputs, the output hash and what was touched.
- Image generation is allowed only for motion-only regions of `swing/00`–`04`, with at most **3 attempts per frame**. Record every attempt as in A3: tool, full prompt, references, raw and runtime SHA-256, cleanup. Use `shared-anim/SOURCES.md` and a new `shared-anim/a4-swing-prompts.json`. Rejected attempts go to `shared-anim/rejected/` (listed).

Read first:
- the A3 review: `git fetch origin review/gpt-godot-spike`, then `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a3.md`
- the **"spike-02 A3"** section of `godot-spike/docs/HANDOFF.md`
- `godot-spike/docs/VERIFICATION.md#spike-02-a3`
- under `shared-anim/`: `frame-audit.json`, `a3-swing-prompts.json`, `SOURCES.md`, `manifest.json`, `thoma-weapon-style-check.png`
- the tools `godot-spike/tools/prepare_a3_frames.py` and `a3_style_check.py`
- under `godot-spike/docs/evidence/spike02-a3/`: `repaint-masks/` and `baseline-a2/`, and `frame-status-table.md`
- `godot-spike/tests/*`
- `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `bd80c5e`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Do not change anything under `ui-prototype/`.** Reading it, and copying bytes out of it, is fine. Never edit or move original PNGs.
- Godot 4.7.2 standard build, **GDScript only** for the game. Python is allowed for offline art tools, as in A2/A3. No C#, no GDExtension, and no new addons beyond the vendored GUT.
- Don't change the rules, the HUD, the timing, the knights, the battlefield or props. G005 is untouched. Don't adopt the on-hold Ferry Dusk palette.
- **Do not change `thoma/idle/01.png` or `thoma/swing/05.png`.** They are the reference.
- **Mechanics stay exactly as in A3** (tested):
  - canvas **512×512**, foot pivot **[256,464]**
  - mace length, head size and grip
  - pose intent per frame: 00 anticipation, 01 raise/start, 02 swing with the hand-painted smear (hidden under Reduced Motion as before), 03 contact with the head on the contact anchor **[455,196]**, 04 follow-through
  - same `contact_frame_index`
  - **same manifest timing**: **180 ms** wind-up hold, **40 ms** swing, all other durations unchanged; the normal attack stays within the 1.7 s budget
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Method and reference extraction
- Write `godot-spike/docs/evidence/spike02-a4/METHOD.md`. It must cover the chosen method (reference-anchored transfer, or a justified alternative) and, for each of `swing/00`–`04`, which reference (idle/01 or swing/05) supplies which region and why. It must list the regions that will be newly painted or generated (motion-only), and explain how this avoids the A3 failure modes: doubled borders at patch edges, stretched embroidery, cuff patch boundaries and the A2 hem contour.
- Extract a **reference region library** from idle/01 and swing/05 into `godot-spike/docs/evidence/spike02-a4/reference-regions/`: the stole band (left and right), the embroidery motif tile or strip, the cuffs (each arm), the hem/underskirt edge, the satchel, the medallion, and the face/hair. Include a reference **palette** with the measured key colors of the robe, stole, embroidery, cuff, hem shadow, skin and hair. Record the masks and coordinates as JSON.
- Prove the method on **one** frame (your choice) as a draft, and include a before/after crop.
- Commit.

### W2. Build `swing/00`–`04`
- Apply the method to all five frames. Keep **A3's live frames as a baseline** under `godot-spike/docs/evidence/spike02-a4/baseline-a3/` as byte copies with recorded hashes. They must not be in the live set or referenced by the manifest. The A2 baseline under `spike02-a3/` stays where it is.
- Clean up as in A3 (alpha, halo, registration to the pivot). Map to the reference palette only where needed, and record the palette distance before and after.
- Commit.

### W3. Per-region check
- Make a **per-region comparison sheet**, `godot-spike/docs/evidence/spike02-a4/region-check.png`. For each swing frame, put same-scale crops of **stole, embroidery, cuffs, hem, face/hair, palette swatch** next to the matching crops from idle/01 and swing/05, on a neutral dark background. Add a row at native 720p in-game size. Regenerate `shared-anim/thoma-weapon-style-check.png` with all 7 frames, and keep the A3 version as `godot-spike/docs/evidence/spike02-a4/style-check-a3.png`.
- **Sequence-consistency check:** make an onion-skin or flip strip of idle/01 → 00 → 01 → 02 → 03 → 04 → 05, `godot-spike/docs/evidence/spike02-a4/sequence-strip.png`. Check that the costume does not "pop" between neighbouring frames: no embroidery appearing or vanishing, no cuff or hem shape jumps, no colour flicker. Where you can, record a measurable proxy per adjacent pair, such as a palette or mean-colour delta inside each region mask.
- For each frame `swing/00`–`04`, record PASS/FAIL per region (stole, embroidery, cuffs, hem, face/hair, palette) and the sequence-pop result in `shared-anim/frame-audit.json`, with a one-line reason per failure.
- **Remove PLACEHOLDER only on frames that pass every region and the sequence check.** A frame that still fails stays PLACEHOLDER with the specific reason. An honest PLACEHOLDER beats a false PASS.
- Commit.

### W4. Sync, import, tests
- Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte, then regenerate `shared-anim/contact-sheet.png`.
- Run the headless import, then GUT. All tests must be green: **≥ 37** tests, the A3 ones plus the new ones. Add or extend tests for:
  - idle/01 and swing/05 are byte-unchanged from A3
  - canvas, pivot, contact index, contact anchor and manifest timing are unchanged from A3
  - no baseline-a3 or baseline-a2 frame is referenced by the manifest
  - the PLACEHOLDER flags in `frame-audit.json` match the handoff table
  - every frame marked PASS has PASS on all six regions and the sequence check
- Save the log as `godot-spike/docs/evidence/spike02-a4/test-run.log`.
- Commit.

### W5. Evidence and verification
In `godot-spike/docs/evidence/spike02-a4/`, from a rendered run with a `CAPTURE_COMPLETE … pass=true` marker:
- `contact-sheet-a3-vs-a4.png`: the A3 baseline row against the new row, at the same scale.
- `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png` and `idle.png`, each at **1280×720 and 1920×1080** (suffix `-1080p` for the 1080p set). 1080p was a P2 gap in the A3 review.
- A `--write-movie` capture at `--fixed-fps 60` of the open attack, from strike to input-ready. Subsample if it's over about 8 MB, and document what was kept in `MOVIE.md`.
- `timing.json` (normal and Reduced Motion, all three setups) and `source-hashes.json`.

Then add a **"spike-02 A4"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes. Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A4"** to `godot-spike/docs/HANDOFF.md` covering:
- how to run it (sync, import, play)
- the method used, in a few sentences, with links to `METHOD.md` and the reference-region library
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER, the per-region results and reasons, and links to `region-check.png`, `sequence-strip.png`, the style check and the A3-vs-A4 contact sheet
- timing (unchanged, measured) against the 1.7 s budget
- what stays open for Phase B: the human hit-feel playtest (**HUMAN_PENDING**) and the shared React/Godot asset-and-timing rule
- limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`. P010 stays **PROPOSED**.

Make this the handoff commit, then **stop**. Phase B remains unstarted.

## Acceptance
- The method anchors costume detail to idle/01 and swing/05 pixels; it is not whole-frame regeneration. It is documented and reproducible (script, masks, control points).
- `swing/00`–`04` are rebuilt. Canvas, pivot, mace geometry, contact frame and anchor, and timing are unchanged from A3 (tested). idle/01 and swing/05 are byte-unchanged.
- The region-check sheet and sequence strip are committed. Per-region PASS/FAIL is in `frame-audit.json`. PLACEHOLDER is removed only on frames that pass everything.
- The A3 frames exist only as an evidence baseline, with hashes.
- The 60 FPS clip and the 720p and 1080p screenshots are committed.
- GUT exits 0 with ≥ 37 tests, and the log is committed.
- `git diff --stat bd80c5e..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
