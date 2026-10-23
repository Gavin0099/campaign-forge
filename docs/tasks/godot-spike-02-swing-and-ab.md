# Task Godot spike 02: swing and hit animation, then a fair React vs Godot A/B

Authorized by Gavin on 2026-10-23 (Asia/Taipei): 「先做揮擊和受擊動畫，再用同素材做網頁版和 Godot 的對照」 ("First build the swing and hit-reaction animation, then compare the web version and Godot using the same assets").

This brief has **two phases**. **This run does Phase A only, then stops.** Phase B is described so Phase A's asset format is designed for it. Do not start Phase B.

The engine decision (P010) stays **PROPOSED**. Nothing here adopts Godot.

## Why
The GPT review of spike 01 (`docs/review/gpt-godot-spike-01.md` on `origin/review/gpt-godot-spike`) judged it **needs Owner**. Its scores were rules/presentation split 9/10, tests 8/10, hit motion 4/10 and art integration 5/10. Its P1 findings were:
1. **No weapon swing.** `scripts/skirmish.gd:216–235`: wind-up and lunge only translate or rotate the whole `Node2D`. There is no weapon arc, no holding pose and no contact deformation, so units read as "sliding paper".
2. **Hitstop is local.** `scripts/skirmish.gd:236–250`: the 80 ms hold only pauses the actors' tweens. Particles, sound and HUD continue, and the camera shake starts after the hold.
3. **Unreadable units.** `scripts/skirmish.gd:162–170`: both knights use the same atlas region and are told apart only by I/II labels. Figures are small at 720p.
4. **Test-tool UI.** `scripts/skirmish.gd:109–150`: a fixed rectangular panel, three setup buttons, a diagnostic toggle and a lot of text.

Its key point: **spike 01 was not a fair engine comparison**, because the React prototype has no attack event at all. The weak hit feel comes mainly from the missing swing and hit-reaction animation, not from the engine. So this spike first builds that animation **once, as engine-neutral assets**. Phase B then plays the exact same assets and timing in both engines.

## Art rules (Owner)
- One consistent dark-fantasy hand-painted style. The references are the P1v4 battlefield (`godot-spike/art/battlefield.png`), the existing sprites in `godot-spike/art/l03-party-v1.png` and `l03-enemies-v1.png`, `ui-prototype/docs/playable-l03-p1v4/STYLE.md`, `ui-prototype/docs/playable-l03-p1v3/STYLE.md` and `ui-prototype/docs/ART-DIRECTION.md`.
- Gavin wants a unified color identity **before** any mass image generation. The Ferry Dusk palette (Draft PR #1) is **on hold**. Do not adopt it and do not regrade anything to it.
- So the new frames must **match the existing Thoma and knight sprites exactly**: the same palette (sample colors from the existing crops), the same light direction, the same stroke and edge treatment, and the same proportions and costume. They must read as the same characters, not as redesigns.
- **Keep the frame count small**, and use only the counts below.
- Image generation is **allowed for these frames only**. Prefer editing or deriving from the existing crops, with the existing crop as the reference image, over generating from scratch. Do **not** regenerate the battlefield, props or any other character.
- For every generated or edited frame, record the following in `shared-anim/SOURCES.md`:
  - the tool;
  - the full prompt;
  - the reference image(s) used;
  - the output's SHA-256;
  - any manual cleanup, such as background removal, recolor or crop.
  Keep rejected attempts out of the runtime folder. A few small ones may go in `shared-anim/rejected/`, listed in SOURCES.md.
- Never edit or move the original PNGs under `ui-prototype/` or `godot-spike/art/`.

## Phase A (this run): shared animation assets plus Godot integration

### Hard boundaries for Phase A
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, on branch `codex/godot-spike`. Do not touch the main checkout `D:\campaign-forge` or other `scratch/*` worktrees.
- You may change only:
  - `shared-anim/` (new, at the repo root);
  - `godot-spike/`;
  - this brief's handoff section in `godot-spike/docs/HANDOFF.md`;
  - optionally, a one-line note on the P010 row in `docs/DECISIONS.md`. It must stay PROPOSED.
- **Do not change anything under `ui-prototype/` in Phase A.**
- Godot 4.7.2 standard build, **GDScript only**. No C#, no GDExtension, and no new addons beyond the vendored GUT.
- The spike-only combat numbers stay spike-only. No new rules, and no G005 changes.

### Asset location decision: `shared-anim/` at the repo root
Use **`shared-anim/`** at the repository root, **not** `ui-prototype/public/art/anim-shared/`. The reasons:
- Phase A may not touch `ui-prototype/`.
- The set must be engine-neutral, with neither engine owning it.
- Godot cannot `load()` `res://` paths outside its project folder, and Vite serves only its own `public/`.

**Each engine gets a byte-identical copy through a committed sync step:**
- **Godot (now).** Add `godot-spike/tools/sync_shared_anim.gd` (run with `godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd`) or a small PowerShell script. It copies `shared-anim/` into `godot-spike/art/anim-shared/`. Add a GUT test that fails if any copied file's SHA-256 differs from the source in `shared-anim/`.
- **React (Phase B).** It will copy into `ui-prototype/public/art/anim-shared/` with the same hash check.

Record this decision in the handoff. If you find a hard blocker with this layout, document it, pick the closest alternative and justify it. Do not silently change it.

### Context to read first
- `godot-spike/docs/HANDOFF.md`, `godot-spike/docs/VERIFICATION.md` and `docs/tasks/godot-spike-01-hit-feel.md`: what spike 01 built.
- `godot-spike/scripts/skirmish.gd`, `godot-spike/scripts/rules/grid_rules.gd` and `godot-spike/tests/*`.
  - The atlas regions are Thoma `Rect2(1558, 0, 520, 711)` in `l03-party-v1.png` and the knight `Rect2(15, 8, 745, 863)` in `l03-enemies-v1.png`.
  - The projection is the web camera × 0.94, offset (−20, 42). The body height is 48.88 px at 720p.
- The style docs listed under Art rules.
- `docs/review/RESOURCE-CHECKLIST.md` (the game-feel and game-ui-ux items).
- Optionally, the GPT review `docs/review/gpt-godot-spike-01.md`. It is on `origin/review/gpt-godot-spike`; read it with `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-01.md` after `git fetch origin review/gpt-godot-spike`. If the fetch fails, the summary under "Why" is enough.

### Do
Work in order. **Commit after each step**, so partial progress survives a quota cutoff.

**A1. Animation spec and manifest schema.**
- Write `shared-anim/README.md`, covering:
  - the sequences;
  - the frame naming (`<character>/<sequence>/<nn>.png`);
  - the canvas size;
  - the pivot convention: one fixed pivot per character, at the feet on the ground-contact point, identical across all of that character's frames, in frame-pixel coordinates;
  - the facing convention, plus how the other direction is produced (mirroring) if needed;
  - the scale relationship to the existing crops.
- Write `shared-anim/manifest.json`, the **single source of truth** that both engines read. Add a JSON Schema at `shared-anim/manifest.schema.json`. At minimum the manifest has:
  - `version`, `characters` (each with the canvas size and pivot);
  - `sequences`, each holding:
    - `frames` (a path, a `duration_ms` and an optional per-frame `offset`);
    - `loop: false`;
    - `contact_frame_index` (swing only);
    - optional `events`, such as `{frame, type: "sfx"|"spark"|"dust", anchor}`, where `anchor` is a contact point in frame pixels;
  - `impact`:
    - `hitstop_ms` (default 80);
    - `shake` (`strength_px`, `duration_ms`, `decay`);
    - `flash_ms`;
    - `knockback_ms`;
    - `blocked_shove_ms`;
    - `blocked_recoil_ms`;
  - `scenarios`: the three setups from spike 01 (open, unit-blocked, terrain-blocked). Each maps to the target's reaction sequence: `hit` then a knockback move, or `stagger` for a blocked case.
- Durations are in milliseconds, as integers. No engine-specific fields. Anything engine-specific goes in an engine-side adapter.
- The total normal-attack time from swing start to input-ready must stay **≤ 1.7 s** (spike 01 was about 0.93–0.97 s). Keep it close to that, and do not make attacks slower without a stated reason.
- Commit.

**A2. Frames.** Hand-painted-style PNGs on transparent backgrounds, all with a consistent pivot and canvas per character.
- **Thoma: a sword swing**, about **5–7 frames**:
  1. anticipation or wind-up;
  2. swing (one or two frames, with a readable weapon arc; a painted smear on the swing frame is fine);
  3. contact;
  4. follow-through;
  5. recover, ending on a pose compatible with the existing idle crop.

  The weapon must be visibly the one Thoma carries in `l03-party-v1.png`.
- **Knight A: a hit reaction**, about **3–4 frames**: flinch, recoil and settle. **Knight A: a blocked stagger**, about **3–4 frames**: an impact against the obstacle, a buckle or stumble, then recovery.
- **Knight B: a visually distinct variant.** Change the helm crest or plume, the tabard or shield color, or the silhouette (for example a different helm shape or a spear instead of a sword). It must stay the same faction and style. Give it an idle frame. Its hit and stagger frames may be the A frames with the same variant edit applied, if that stays consistent. Both knights must be distinguishable **without labels** at 720p and in grayscale. Verify that with a grayscale screenshot.
- Produce frames by deriving from the existing crops where possible, plus image generation with the crop as reference. Clean every frame by hand or by script: transparent background, no halo, consistent scale and pivot alignment, and a palette checked against the source crop. Record each one in `shared-anim/SOURCES.md` as required by Art rules.
- Add a contact-sheet PNG, `shared-anim/contact-sheet.png`. Put every runtime frame in sequence order on a neutral dark background, next to the original idle crop, with the pivot marked. Use it for self-review of style consistency.
- If a frame fails to match the style after **3 attempts**, keep the best one, label it **PLACEHOLDER** in SOURCES.md and in the handoff, and move on. Do not loop on generation.
- Commit.

**A3. The Godot manifest player.**
- Add the sync step and hash test (see "Asset location decision").
- Write a GDScript loader for `manifest.json` (for example `scripts/anim/anim_manifest.gd`, a `RefCounted` with no nodes). It validates the required fields and fails loudly on a bad manifest.
- Write a frame player that plays a sequence frame by frame from the manifest durations, using `Sprite2D` texture swaps or `AnimatedSprite2D` with per-frame durations. It positions frames by the manifest pivot so the feet don't jitter. It also fires the manifest `events` at the right frame (contact → spark, sfx).
- Replace spike 01's whole-body translate and rotate in `play_attack()` with the manifest-driven swing on Thoma. Keep a small lunge only if it reads better, with its timing in the manifest. On the target, play `hit` + knockback, or `stagger` for blocked cases, from the manifest.
- **Make the playback a generic event player.** Spike 01 indexed `result.events[0..2]` directly, so dispatch on the event `type` instead. Order and timing come from the event list plus the manifest.
- Keep the existing rules model untouched, except for what is needed to support knight B's identity. Keep the hit flash, damage number, particles and procedural SFX, but time them from the manifest.
- Commit.

**A4. Whole-frame hitstop.**
- At the contact frame, freeze **all world motion** for `impact.hitstop_ms`. That includes:
  - every unit sprite and frame player;
  - all world tweens;
  - particles;
  - the camera;
  - any world-space damage number.

  The **UI layer is excluded**: HUD and input focus stay responsive, but attack input remains locked as before.
- Recommended approach: put all world nodes under one `World` node with `process_mode` pausable, and the HUD in a `CanvasLayer` with `PROCESS_MODE_ALWAYS`. Use `get_tree().paused = true` for the hold, restored by a `SceneTreeTimer` created with `process_always = true` and `ignore_time_scale = true`. Bind world tweens to world nodes (`node.create_tween()`), so they pause with the tree. Setting `Engine.time_scale` to 0 is acceptable only if you prove that the UI and timer behave. Document which approach you chose and why.
- The contact frame, flash onset, spark burst and SFX all fire on the **same frame**, at the start of the hold. The shake starts **with** the impact; a held shake offset during the freeze is fine. It does not start after the hold.
- Reduced Motion keeps working: no shake, no flash and no swing smear, minimal displacement, the damage number kept. Hitstop may stay. Show the swing in reduced form (key poses only, or shorter); document which.
- Commit.

**A5. Unit readability at 720p.**
- Make units clearly readable at 1280×720. Two candidates; prototype both, and keep one or a combination:
  - (a) **An attack camera:** a short `Camera2D` zoom toward the attacker–target midpoint during the attack, for example 1.0 → 1.35–1.6 → 1.0, with its timing in the manifest (`camera`).
  - (b) **A larger unit scale** on the board, for example 1.2–1.4 tiles tall.
- **Decide by evidence.** Option (b) failed in P1v4 at 1.3 tiles because neighbouring units overlapped, so check overlap in all three setups (adjacent units, and setup (b)'s three-in-a-row). Capture both options at 720p, at the contact moment and at rest. Pick the one that reads better without overlap, and justify it in the handoff with the screenshots. Knight A and knight B must be distinguishable without labels.
- Commit.

**A6. Minimal in-game UI.**
- Trim the HUD to a minimal in-game style that matches the painted look. It shows the selected scenario name, a small key hint line (1/2/3, Space, R, M), and HP pips or bars for the two or three units in the bone/brass palette already used. There are no admin panels and no big text blocks.
- Move every debug element (the setup buttons if you keep them as buttons, the grid toggle, phase text, timing readout and diagnostic labels) behind a **debug toggle (F1 or `)**, which is off by default.
- Keyboard control and focus behaviour stay as in spike 01 (Space strikes, R replays, M toggles Reduced Motion, Esc exits).
- Commit.

**A7. Tests (GUT, headless).**
- Keep all existing tests passing. Add tests for:
  - **Manifest parsing:** a valid manifest loads; every referenced frame exists; durations are positive integers; `contact_frame_index` is in range; a missing required field is rejected.
  - **Hash parity:** each `godot-spike/art/anim-shared/` file is byte-identical (SHA-256) to `shared-anim/`.
  - **Whole-frame hitstop:** during the hold, world nodes do not advance. A world tween's progress, the frame player's frame and time, a particle node's processing and the camera offset are all unchanged across real time ≥ the hold. A UI node marked always-process does advance. After the hold the world resumes.
  - **Contact sync:** flash, spark and SFX triggers fire on the contact frame.
  - **Generic event player:** an event list with a different order or an extra unknown event plays without index assumptions.
  - **Timing:** each scenario completes within 1.7 s of game time. State how hitstop is counted.
  - **Knight identity:** knight A and knight B use different textures or regions.
- Save the log to `godot-spike/docs/evidence/spike02/test-run.log`.
- Commit.

**A8. Evidence and verification commit.** Put everything in `godot-spike/docs/evidence/spike02/`.
- 1280×720 screenshots from a rendered capture run, for scenario (a):
  - `anticipation.png`;
  - `contact.png` (during hitstop);
  - `recoil.png`.
- Also capture:
  - `blocked-unit-stagger.png`, `blocked-terrain-stagger.png` and `reduced-motion-contact.png`;
  - `readability-option-a.png` and `readability-option-b.png`;
  - `knights-grayscale.png`;
  - `hud-minimal.png` and `hud-debug.png`.
- **A `--write-movie` capture** of scenario (a), from strike to input-ready, at `--fixed-fps 60`. If the full PNG sequence is too big (over about 8 MB), commit a subsampled set plus an AVI if it is small. Document what was kept.
- **Timing measurements** per scenario, in normal and reduced modes, in `timing.json`. Also check the measured hitstop duration against the manifest, and the frame-accurate contact sync.
- Update `godot-spike/docs/VERIFICATION.md` with a "spike-02 Phase A" section listing the commands actually run, with their real exit codes. The capture must still print a `CAPTURE_COMPLETE … pass=true` style marker. Exit 0 alone is not acceptance.
- Make this the verification commit.

**A9. Handoff, then stop.**
- Add a section **"spike-02 Phase A"** to `godot-spike/docs/HANDOFF.md`, covering:
  - how to run it, including the sync step and the debug toggle;
  - what changed against each of the four spike-01 P1 findings, with evidence links;
  - the asset-location decision;
  - the frame list with PLACEHOLDER flags;
  - the readability decision and why;
  - the hitstop method;
  - an honest style-consistency self-assessment against the existing sprites, with a contact-sheet link;
  - limits;
  - what Phase B needs (manifest fields the web side must honor, frame formats, and the expected React approach).
- Include a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`. Human playtest stays **HUMAN_PENDING**. P010 stays **PROPOSED**.
- Make this the handoff commit, then **stop**. Do not start Phase B.

### Phase A acceptance
- The headless GUT suite exits 0, with the log committed.
- Thoma visibly swings a weapon, and the target visibly reacts with distinct hit and stagger frames, from `shared-anim/manifest.json`.
- The hitstop freezes the whole world, not the UI, and this is proven by a test and the contact screenshot.
- The two knights are distinguishable without labels, including in grayscale.
- The default HUD is minimal, with debug behind a toggle.
- Every scenario takes 1.7 s or less, as measured.
- `git diff --stat be9a398..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and (optionally) a one-line P010 note in `docs/DECISIONS.md`. Nothing under `ui-prototype/` changes.

## Phase B (a later run; do NOT do it now): a React vs Godot A/B with the same assets
Described here so Phase A's formats support it. A separate Owner go-ahead and run will start it.
- **An isolated React demo scene** at a new route `?scene=anim-ab` in `ui-prototype/`.
  - **No changes to `ui-prototype/src/playable-l03/rules.ts`** or the existing scenes.
  - It has its own small event fixture: the same attack → damage → knockback / knockback_blocked events and the same three scenarios as the Godot spike. Ideally the same JSON fixture is shared with Godot.
  - It reads the **same** `manifest.json` and frames, synced into `ui-prototype/public/art/anim-shared/` with a hash check.
  - It plays them with the same timing: frame swaps plus the Web Animations API or a `<canvas>`, a whole-scene hitstop (pausing all animations and particles while the UI stays live), the same shake, flash, damage number, sparks and SFX, and Reduced Motion.
  - It uses the same battlefield crop, unit scale and readability choice as Godot, at 1280×720.
- **Evidence:**
  - side-by-side captures of both engines at the same moments (anticipation, contact, recoil and the blocked cases);
  - frame-timed recordings;
  - a timing comparison table, measured against the manifest, with jitter and drift;
  - an effort note (lines of code and time per engine for the same result).
- **An A/B report for Gavin**, `docs/review/anim-ab-report.md`:
  - how to launch both;
  - a short blind-ish protocol: play both for 3–5 minutes and score hit weight, readability and responsiveness;
  - what differs and why;
  - no recommendation presented as an Owner decision.
- Its tests are Vitest or Playwright for the web scene. The web suite and Godot GUT must both stay green.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. **Stop after the Phase A handoff commit** and wait for review.
