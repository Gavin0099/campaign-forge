# Task Godot spike 01: hit feel for one attack (isolated PoC, 90 min timebox)

Authorized by Gavin on 2026-10-23 17:26 (Asia/Taipei): 「開 Godot 試做版，讓 Codex 做 Thoma 打騎士這一下」 ("Start the Godot spike; have Codex build Thoma hitting the knight"). `docs/review/RESOURCE-CHECKLIST.md` requires an isolated PoC plus Owner approval before adding a new engine. This is that approval, but **only for an isolated PoC**. The engine choice itself stays PROPOSED until Gavin accepts it.

Why: after P1v7, Gavin reported that hits still don't feel impactful (「打擊感還是不夠」). The web prototype (React + TS + DOM/SVG) has no animation system, particles, camera shake or hitstop. Its rules (`ui-prototype/src/playable-l03/rules.ts`) only emit `move`, `intent`, `progress`, `turn`, `result` and `retry` events. They have no attack, damage or knockback. This spike tests whether Godot 4 delivers convincing hit feel on our existing art.

## Hard boundaries
- Work only inside a new folder `godot-spike/`, plus the brief-mandated `docs/DECISIONS.md` entry. Do **not** touch `ui-prototype/`, its rules, its tests or its art. Copy the PNGs you need; never move or edit the originals.
- Godot 4.7, standard build (not .NET), **GDScript only**. No C#, no GDExtension, no editor plugins beyond the test framework.
- Do not touch other worktrees (`scratch/*`) or the main checkout `D:\campaign-forge`.
- This spike may invent provisional numbers (HP and damage). Label them as spike-only, not game rules or G005.

## Verified engine command (Windows, PowerShell)
- `godot --version` prints `4.7.2.stable.official.ed1daf0bf`.
- `godot` is `godot.cmd` on PATH (winget). It wraps `Godot_v4.7.2-stable_win64_console.exe`, so stdout, stderr and exit codes reach the shell.
- Typical invocations, run from the worktree root:
  - Import once after adding assets: `godot --headless --path godot-spike --import`
  - Headless tests (GUT example): `godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`
  - Rendered capture (not headless, because headless uses a dummy renderer that cannot produce screenshots): `godot --path godot-spike --resolution 1280x720 -- --capture`
  - Movie: `godot --path godot-spike --resolution 1280x720 --fixed-fps 60 --write-movie godot-spike/docs/evidence/hit/frame.png --quit-after <frames>`
- Record the exact commands you actually used, with their real exit codes, in `godot-spike/docs/VERIFICATION.md`.

## Context to read first
- `ui-prototype/src/playable-l03/rules.ts`: the 11×9 grid, `walkable()` (water columns 4–5 and the destroyed crossing at (4,4)/(5,4) are impassable on the open route), the 4-neighbour order and `DEPLOYMENT` (Thoma at (1,4), knights at (1,8) and (3,8)).
- `ui-prototype/src/l03Scene.ts`: `sceneRows`.
- `ui-prototype/src/playable-l03/presentation.tsx`: the camera `project(x,y) = (550 + 44(x−y), 70 + 26(x+y))` in a 1100-wide scene, tiles of 88×52 scene units, and the battlefield image rectangle x=130, y=13.666667, w=940, h=626.666667. It also has the sprite crops for Thoma (from `l03-party-v1.png`), the knights (from `l03-enemies-v1.png`) and the winch frames.
- `ui-prototype/docs/playable-l03-p1v4/STYLE.md`, `ui-prototype/docs/playable-l03-p1v3/STYLE.md` and `ui-prototype/docs/ART-DIRECTION.md` for the dark-fantasy hand-painted palette.
- `docs/tasks/playable-l03-P1v4-art.md` and `docs/tasks/playable-l03-P1v6-feedback-winch.md` for the art conventions.

## Do
Work in order. Commit after each step so partial progress survives a quota cutoff.

1. **Project skeleton.**
   - Create `godot-spike/project.godot` (Godot 4.7) with:
     - a 1280×720 viewport;
     - stretch mode `canvas_items` and aspect `keep`;
     - the main scene `res://scenes/Skirmish.tscn`.
   - Add a `godot-spike/.gitignore` that ignores `.godot/` and other import caches. Commit `*.import` files only if Godot needs them for headless loading, and say so in the handoff.
   - Copy into `godot-spike/art/` the PNGs you need:
     - `ui-prototype/public/art/l03-p1v4/battlefield.png`
     - `ui-prototype/public/art/l03-p1v4/props.png`
     - `ui-prototype/public/art/l03-party-v1.png`
     - `ui-prototype/public/art/l03-enemies-v1.png`
     - optionally `ui-prototype/public/art/l03-p1v6/winch-frames.png`
   - Add `godot-spike/art/SOURCES.md`, listing each copied file's original path.
2. **Minimal rules model in GDScript**, pure and with no nodes (for example `scripts/rules/grid_rules.gd`, extending `RefCounted`).
   - **Grid.** The same 11×9 rows as `sceneRows`, and the same walkability as `rules.ts` on the open route.
   - **Units.** Each unit has an id, a side, a cell, hp and max_hp.
   - **`move(unit, to)`.** A simple BFS. No passing through units.
   - **`attack(attacker, target)`.** Requires adjacency. It returns an ordered event list: `attack`, then `damage {unit, amount, hp_after}`, then either `knockback {unit, from, to}` or `knockback_blocked {unit, from, into, blocker: "terrain"|"unit", blocker_id?}`.
   - **Knockback direction.** One tile, directly away from the attacker. It never passes through walls, water, the map edge or units. A blocked knockback leaves the target in place and emits `knockback_blocked`. It may deal +1 spike-only impact damage, as long as that is documented.
   - Use spike-only numbers, for example Thoma deals 2 and a knight has 6 HP (from `sceneUnits`). Keep them in one constants block.
3. **Skirmish scene.**
   - **Battlefield.** `Skirmish.tscn` shows the painted battlefield.
   - **Grid alignment.** Map the web camera into Godot coordinates, so the grid overlay matches the web version's layout as closely as practical. A uniform scale and offset from the 1100-wide scene to 1280×720 is fine. Add a diagnostic toggle that shows the grid, which is off by default.
   - **Placement.** Place Thoma and both knights using their existing sprite crops (`AtlasTexture` regions). Units are about 1.0 tile tall, matching P1v4.
   - **Showcase setups.** Stage three of them, selectable with keys or buttons in a small painted-style HUD. No admin-style UI.
     - (a) **Normal knockback:** Thoma at (1,4), knight-1 at (1,5). Knockback goes to (1,6).
     - (b) **Blocked by a unit:** as in (a), plus knight-2 at (1,6).
     - (c) **Blocked by terrain:** Thoma at (2,4), a knight at (3,4). The knockback goes into the destroyed crossing at (4,4).
     - You may use different cells if these are illegal under your model. Document why.
4. **The showcase attack: Thoma hits a knight.** Play the events from step 2 in this order:
   1. **Wind-up:** a short anticipation, about 150–250 ms. Pull back or lean, maybe with a squash.
   2. **Lunge and contact.**
   3. **Hitstop of about 80 ms** at contact. Use `Engine.time_scale` near 0 restored with a real-time `SceneTreeTimer` (`process_always`, `ignore_time_scale`), or a local freeze of the two actors. Document which one you chose.
   4. **Camera2D shake:** decaying, about 150–250 ms, small amplitude.
   5. **White hit-flash** on the target, from a `CanvasItem` shader with a `flash` uniform, lasting about 100 ms.
   6. **Knockback** of one tile, with an ease-out tween of about 180–250 ms. For a blocked knockback, play a short shove-and-recoil toward the blocker instead, with a strong impact cue (an extra shake or dust burst). Never cross the blocker visually.
   7. **Damage number:** it floats up and fades, in the bone/brass palette with a dark outline.
   8. **Impact particles:** `GPUParticles2D` or `CPUParticles2D` sparks or dust at the contact point.
   9. **Hit sound.** Placeholder SFX are fine if you generate them procedurally (for example a WAV synthesized by a script you commit) or take them from CC0. Record the source and license in `godot-spike/audio/SOURCES.md`.

   Then do the following:
   - **Replay:** a key or button replays the current setup from a clean state.
   - **Reduced motion:** a toggle that removes the shake and flash, keeps the knockback but makes it instant or very short, and keeps the damage number. Hitstop may stay because it is not motion.
   - **Timing:** measure the total attack sequence time, from the start of the wind-up until input is available again. The target is **1.7 s or less** for setups (a) to (c). Print or log the measured value.
   - **VFX art:** image generation is allowed for small missing art (spark, dust or impact sprites) in the existing dark-fantasy hand-painted style. Save it under `godot-spike/art/vfx/`, and record each prompt and output in `art/SOURCES.md`. Do not regenerate characters or the battlefield.
5. **Tests**, headless.
   - Vendor GUT (a Godot 4.x compatible release) or gdUnit4 inside `godot-spike/addons/`. Record its version, source URL and license (both are MIT) in `godot-spike/addons/README.md`.
   - If the download is impossible, write a minimal self-contained GDScript test runner (`tests/run_tests.gd`, run with `-s`, exiting non-zero on failure) and document why.
   - The tests must at least cover:
     - an attack between adjacent units produces `attack`, `damage` and `knockback` events, in that order;
     - HP is reduced by exactly the damage amount, and a non-adjacent attack is rejected;
     - knockback into a wall or water emits `knockback_blocked`, and the target stays in its cell;
     - knockback into another unit emits `knockback_blocked` with `blocker: "unit"`, and neither unit passes through or overlaps;
     - knockback off the map edge is blocked;
     - optionally, a scene-level test that the attack sequence finishes within 1.7 s of game time. Note in the test how hitstop is counted.
   - Save the headless test log to `godot-spike/docs/evidence/test-run.log`.
6. **Evidence** in `godot-spike/docs/evidence/`.
   - Save these screenshots at 1280×720, captured by a rendered run with a capture mode (for example `-- --capture`) that saves `get_viewport().get_texture().get_image()` at the chosen moments and then quits:
     - `hit-frame.png`: the contact, hitstop and flash frame;
     - `knockback-end.png`;
     - `knockback-blocked.png`;
     - optionally `reduced-motion.png`.
   - Save a short capture of setup (a), if feasible: a `--write-movie` PNG frame sequence or AVI, or failing that a handful of timed frames. Keep it small, a few MB at most. If the size gets too big, commit a subsampled sequence and say so.
   - Write `godot-spike/docs/VERIFICATION.md` with:
     - the commands you ran, with their real exit codes;
     - the test counts;
     - the measured sequence times per setup;
     - which hitstop method you chose.
   - Make this the verification commit.
7. **Handoff and decision proposal.**
   - Write `godot-spike/docs/HANDOFF.md` covering:
     - how to run it (the editor, and the exact CLI);
     - what was verified, with evidence links;
     - what is placeholder (SFX, spike numbers, VFX);
     - its limits, for example the single body sprite per knight and no animation frames;
     - an honest comparison with the web version's feel;
     - a recommendation on full migration: what would move (rules, art, tests), a rough effort, and the risks, including Ink support in Godot 4 and the Codex/GPT review loop under Godot.
     - a resource self-check: game-feel PASS or FAIL with evidence, while human playtest stays HUMAN_PENDING.
   - Add a row to `docs/DECISIONS.md` under 提案與工作假設. Use the next free P-number, marked **PROPOSED** (not accepted): "Godot 4 (GDScript) as the battle presentation engine". Its condition is the Owner playtest of this spike plus a decision. Do not change any confirmed D-row.
   - Commit this as the handoff commit.

## Acceptance
- `godot --headless --path godot-spike ...` tests exit 0, and the log is committed.
- The scene opens and plays all three setups with replay and reduced motion, as shown in the screenshots.
- The attack sequence takes 1.7 s or less, measured and recorded.
- `git diff --stat` against the base branch shows changes only under `godot-spike/` and to `docs/DECISIONS.md`.

## Stop
Commit only. Don't push, because the Owner's agent pushes afterwards. Don't merge to main, open a PR or use git stash. Stop after the handoff commit and wait for review.
