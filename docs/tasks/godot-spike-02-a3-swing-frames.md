# Task Godot spike 02 A3: finish Thoma's mace swing frames, approve the mace, re-check knight B

Authorized by Gavin on 2026-10-24 (Asia/Taipei): 「就用單手短釘頭錘，開始補 5 格揮擊」 ("Use the short one-handed mace; start finishing the 5 swing frames").

This is a **small art-fix segment** on top of spike-02 A2 (`98c735e`). It runs **before** Phase B. **Do not start Phase B** (the React vs Godot A/B in `docs/tasks/godot-spike-02-swing-and-ab.md`) and **do not touch React** (`ui-prototype/`). The engine decision (P010) stays **PROPOSED**.

## Why
The GPT review of A2 (`docs/review/gpt-godot-spike-02a2.md` on `origin/review/gpt-godot-spike`, commit `a2e1fa2`) returned **CONDITIONAL ACCEPT**, no P0, no P2. Its open P1 items, of which this segment fixes the art and readability ones:
1. **P1-01 Swing frames are placeholders.** `thoma/swing/00`–`04` are PLACEHOLDER because the stole/cape embroidery, cuff folds and hem silhouette drift from the original Thoma. Only the weapon idle (`thoma/idle/01`) and `thoma/swing/05` pass the style check. The weapon itself needed Owner approval.
2. **Knight B readability.** "0 px overlap" does not prove a player can tell the two knights apart. Check at native 720p, without name labels, in grayscale, in all three setups. If they cannot be told apart at a glance, change the helm or shield silhouette; do not scale the characters up.
3. (Not in this segment) human hit-feel playtest and the shared React/Godot asset-and-timing rule. Those belong to Phase B and stay open.

Read first: that review (`git fetch origin review/gpt-godot-spike` then `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a2.md`), the **"spike-02 A2"** section of `godot-spike/docs/HANDOFF.md`, `shared-anim/README.md`, `shared-anim/SOURCES.md`, `shared-anim/frame-audit.json`, `shared-anim/manifest.json`, `shared-anim/generation-prompts.json` / `a2-swing-prompts.json` / `a2-retry-prompt.json`, `shared-anim/thoma-weapon-style-check.png`, `godot-spike/tools/prepare_a2_frames.py`, `godot-spike/tools/sync_shared_anim.gd`, `godot-spike/tests/*` (especially `test_a2_hud.gd`), `godot-spike/docs/evidence/spike02-a2/` and `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux).

## Owner decision: Thoma's weapon is canon
**Decision (Gavin, 2026-10-24): Thoma's canon weapon is the short one-handed flanged mace** — dark iron flanged head, worn oak haft, small brass collar echoing his medallion, about forearm length, carried in his right hand. The brass medallion stays his **holy symbol (聖徽)**, not a weapon. No staff, no blade, no book, no magic glow (unchanged from `ui-prototype/docs/l03/character-prompt.txt`).

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `98c735e`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/`, the P010-unrelated weapon note described in W1 below, and this segment's handoff section. **Do not change anything under `ui-prototype/`** (reading and copying bytes out of it is fine). Never edit or move original PNGs.
- Godot 4.7.2 standard build, **GDScript only**. No C#, no GDExtension, no new addons beyond the vendored GUT.
- No rules changes, no HUD redesign, no timing changes. G005 is untouched.
- Do not adopt the on-hold Ferry Dusk palette. Do not regenerate the battlefield, props, the knights (except a W4 *proposal*, not an edit) or any Thoma frame other than `swing/00`–`swing/04` (plus `swing/05` / `idle/01` only if W3 shows they no longer match the new set; then say why).
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Mace APPROVED (Owner decision)
- Everywhere the mace is marked `PROPOSED` / "Owner confirmation pending" — at least `shared-anim/README.md`, `shared-anim/SOURCES.md`, `shared-anim/frame-audit.json` (`weapon_status`), `shared-anim/generation-prompts.json` (and the A2 prompt files if they carry the flag), the synced copies under `godot-spike/art/anim-shared/`, and the A2 section of `godot-spike/docs/HANDOFF.md` — change it to **APPROVED (Owner, 2026-10-24)**. Do not rewrite the historical A2 text beyond the status; add a short "superseded by Owner decision 2026-10-24" note where the A2 handoff says PROPOSED.
- Add an **Owner decision** note to `shared-anim/README.md` (replace the weapon-proposal paragraph's status line): the decision, date, the Owner's words above, and the weapon description. Also add one line to `docs/DECISIONS.md` only if it already has a section for confirmed art/equipment decisions; otherwise record it only in `shared-anim/README.md` and the handoff (do not invent a new D-row, and do not touch P010).
- Update the test that asserts `weapon_status == "PROPOSED"` (`godot-spike/tests/test_a2_hud.gd`) to expect `APPROVED`.
- `P010` stays **PROPOSED**; only the weapon status changes. Use `git grep -n -i "proposed"` afterwards and list in the commit message what was intentionally left PROPOSED (P010, history).
- Commit.

### W2. Redo `thoma/swing/00`–`04`
- Goal: costume details match the passing frames (`thoma/idle/01`, `thoma/swing/05`) and the original Thoma reference (`shared-anim/references/thoma.png`): **stole/cape embroidery motif, cuff folds, hem silhouette, robe and stole colors, satchel, medallion, face/beard, proportions, light direction and stroke**.
- Keep the motion and the mechanics exactly as in A2: same canvas **512×512**, same foot pivot **[256,464]**, same mace length, head size and grip, same pose intent per frame (00 anticipation, 01 raise/start, 02 swing with hand-painted smear — hidden under Reduced Motion as before, 03 contact with the head on the contact anchor `[455,196]`, 04 follow-through), same `contact_frame_index`, and **same manifest timing** (180 ms wind-up hold, 40 ms swing, all other durations unchanged). The total normal attack must stay as measured in A2 (≤ 1.7 s budget).
- Image generation is allowed for these 5 frames only, using `references/thoma.png`, `thoma/idle/01.png` and `thoma/swing/05.png` as references (costume ground truth) and the current A2 frame of the same index as the pose reference. Prefer an approach that copies costume detail rather than reinventing it (for example generating with strong references and then compositing/repainting the stole band, cuffs and hem from the passing frames; palette-map from the source crop as in A2). At most **3 attempts per frame**. Clean each as in A2 (alpha, halo, registration to the pivot, palette mapping).
- Record every attempt in `shared-anim/SOURCES.md` and a new `shared-anim/a3-swing-prompts.json`: tool, full prompt, references, raw and runtime SHA-256, cleanup. Rejected attempts go to `shared-anim/rejected/` (listed), not the runtime folder.
- **Keep the old A2 frames as a comparison baseline** under `godot-spike/docs/evidence/spike02-a3/baseline-a2/` (byte copies, hashes recorded). They must not be in the live set or referenced by the manifest.
- Commit.

### W3. Per-frame style check (all 7 frames)
- Make `shared-anim/thoma-weapon-style-check.png` anew (keep the A2 one as `godot-spike/docs/evidence/spike02-a3/style-check-a2.png`): the original crop, `idle/01` and all 6 swing frames side by side at the same scale on a neutral dark background, a zoomed detail row of the stole band, cuffs and hem for each frame, and one row at 720p in-game size.
- For each of the 7 Thoma runtime frames (`idle/01`, `swing/00`–`05`), check face, stole/cape embroidery, cuffs, hem silhouette, palette, proportions, light direction and stroke against `idle/01`/`swing/05` and the original. Write the result per frame in `shared-anim/frame-audit.json` (pass/fail per criterion, plus a palette distance number if you can measure it).
- **Remove PLACEHOLDER only on frames that pass.** Any frame that still fails stays PLACEHOLDER with the specific reason. Be honest: an unchanged PLACEHOLDER is better than a false PASS.
- Commit.

### W4. Knight B readability check (no art change unless clearly needed)
- Rendered runs at **native 1280×720**, with **all name/role labels and HUD tags hidden**, captured in **color and grayscale**, for **setups 1, 2 and 3**, both at rest (default view) and at the zoomed attack. Save as `godot-spike/docs/evidence/spike02-a3/knights-720p-setup{1,2,3}-{rest,zoom}-{color,gray}.png`.
- Judge for each: can a player tell knight A from knight B at a glance without labels? Write PASS / FAIL with a one-line reason per image in `godot-spike/docs/evidence/spike02-a3/knight-readability.json`. Also record a simple measurable proxy (for example grayscale mean-luminance and silhouette-area difference of the distinguishing helm/shield region between the two knights).
- **Only if it clearly fails:** write a proposal (do **not** implement) in the handoff for a helm or shield silhouette change, with a rough mock-up image if useful. Do not scale the characters up.
- Commit.

### W5. Sync, import, tests and evidence
- Run `godot-spike/tools/sync_shared_anim.gd` so `godot-spike/art/anim-shared/` matches `shared-anim/` byte for byte; regenerate `shared-anim/contact-sheet.png`.
- Headless import, then GUT: all tests green (expect **≥ 33** tests; the old ones plus any new ones). Add or extend tests for: weapon status APPROVED in the manifest/audit; the PLACEHOLDER flags in `frame-audit.json` match what the handoff table says; no baseline-a2 frame is referenced by the manifest; pivot, canvas, contact index and timing unchanged from A2. Save the log to `godot-spike/docs/evidence/spike02-a3/test-run.log`.
- In `godot-spike/docs/evidence/spike02-a3/`, from a rendered 1280×720 run with a `CAPTURE_COMPLETE … pass=true` marker: `contact-sheet-old-vs-new.png` (A2 baseline row vs new row, same scale), `swing-anticipation.png`, `swing-smear.png`, `contact.png` (during hitstop), `follow-through.png`, `idle.png`, plus a `--write-movie` capture at `--fixed-fps 60` of the open attack from strike to input-ready (subsample if over about 8 MB; document what was kept), `timing.json` (normal and Reduced Motion, all three setups) and `source-hashes.json`.
- Add a **"spike-02 A3"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A3"** to `godot-spike/docs/HANDOFF.md`:
- how to run it (sync, import, play);
- **Thoma's weapon: APPROVED (Owner, 2026-10-24)** with the description;
- the frame table (`idle/01`, `swing/00`–`05`) with PASS / PLACEHOLDER and the reason, and links to the new style check and the old-vs-new contact sheet;
- knight B readability result per setup (color and grayscale), and the silhouette proposal only if it failed;
- timing (unchanged, measured) against the 1.7 s budget;
- what stays open for Phase B: human hit-feel playtest (**HUMAN_PENDING**) and the shared React/Godot asset-and-timing rule;
- limits and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`. P010 stays **PROPOSED**.
- Make this the handoff commit, then **stop**. Phase B remains unstarted.

## Acceptance
- The mace is APPROVED (Owner 2026-10-24) everywhere it was PROPOSED; P010 is still PROPOSED.
- `swing/00`–`04` are repainted with costume details matching `idle/01`/`swing/05` and the original; canvas, pivot, mace geometry, contact frame and timing are unchanged from A2 (tested).
- The A2 frames exist only as an evidence baseline, with hashes; the manifest does not reference them.
- The new style-check sheet is committed and the PLACEHOLDER flags are honest per frame.
- Knight B readability is reported PASS/FAIL per setup at native 720p, unlabeled, in color and grayscale, with screenshots.
- GUT exits 0 with ≥ 33 tests and the log committed.
- `git diff --stat 98c735e..HEAD` shows changes only under `shared-anim/`, `godot-spike/`, this brief and (if allowed by W1) one line in `docs/DECISIONS.md`. Nothing under `ui-prototype/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
