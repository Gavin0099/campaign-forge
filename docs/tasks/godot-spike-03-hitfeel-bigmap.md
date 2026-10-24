# Task Godot spike 03: stronger hit feel (implement) + big-map proposal (document and mockup only)

Authorized by Gavin on 2026-10-24 18:27 (Asia/Taipei), after the A9 review: 「A9 先暫用，接著做大地圖提案和打擊感」 ("use A9 for now; next do the big-map proposal and the hit feel").

## Owner decisions (unchanged)
- campaign-forge uses **Godot directly** (P010 accepted on branch `decision/p010-godot`). The React web version and Phase B are **CANCELLED**. Do not touch `ui-prototype/` (read-only reference is fine), do not add React to-dos, do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**. Do not change its status or design.
- One consistent **dark-fantasy hand-painted** style; the game must read as a real tactics RPG, not a tool UI. AI image generation is allowed. Do not adopt the on-hold Ferry Dusk palette.
- **A9 swing frames are accepted as development PLACEHOLDER** (Owner, 2026-10-24 18:27). This segment does **no art work on them**: `shared-anim/thoma/**` PNGs, `godot-spike/art/anim-shared/**` PNGs and everything under `docs/art-briefs/` stay byte-identical. Their PLACEHOLDER flags in `frame-audit.json` stay as they are. The commission brief stays the fallback for a human artist.

This segment builds on spike-02 A9 (`b2f460b`, 79 GUT tests).

## Why
- **Hit feel.** The Owner finds 打擊感 still not strong enough. The current impact is thin (measured in A9, see below). Part A layers a proper impact on the contact frame (`swing/03`) without touching the art.
- **Big maps like 曹操傳.** The current battlefield fits the whole 11×9 map on one 1280×720 screen, so tiles and units look small. The Owner wants many more tiles, maps much bigger than the screen, a scrolling camera and large readable tiles and units. This changes level design and balance, so Part B is a **PROPOSAL for Owner approval plus a throwaway mockup — NOT an implementation**. No gameplay, rules or real level changes.

## Current state (measured by the Owner's agent from `b2f460b`, verify yourself)
Hit feel (`godot-spike/scripts/skirmish.gd`, `shared-anim/manifest.json` → `impact`, `camera`, `sequences["thoma.swing"]`):
- Swing frames 180 / 70 / 40 / 80 / 100 / 150 ms, `contact_frame_index` 3, contact anchor (455,196); events on frame 3: `spark`, `sfx`.
- `impact.hitstop_ms` 80 — implemented in `hold_contact()` by pausing the **whole SceneTree** (`get_tree().paused`), world nodes are `PROCESS_MODE_PAUSABLE`.
- `impact.shake` strength 3.4 px, 200 ms, decay 2; `_process()` drives `camera.offset` with a non-directional sin/cos wobble; `shake()` sets a first offset (s, −s/2).
- Hit flash: `shaders/hit_flash.gdshader` mixes to white at `flash * 0.65`; set to 1.0 on contact, faded over `impact.flash_ms` 35 ms after the hold.
- Knockback tween 220 ms (cubic out) to the next cell; blocked: shove 6 px / 60 ms, recoil 160 ms; `settle_ms` 180.
- Camera: one `Camera2D` at (640,360) zoom 1; attack zooms to 1.4 in 240 ms towards the attacker/target midpoint (weight 0.52), back in 180 ms. No zoom punch.
- Damage number: `show_damage()` Label "−N", 18 px brass on a dark box, rises 30 px over 0.38 s, fades from 0.18 s. No scale punch.
- Particles: `emit_particles()` 7 static brass spokes (fade 0.12 s) + 24 CPU sparks (lifetime 0.30); dust (18) only on the blocked recoil.
- SFX: one synthesized hit, `audio/impact_synth.gd` `make_hit()` (0.24 s, −7 dB). No whoosh or knockback thud.
- No crit (rules damage is fixed 2; `grid_rules.gd` `SPIKE`).
- Measured A9 strike-to-input-ready ≈ 0.91–0.95 s normal (720p), movie 0.9167 s; Reduced Motion ≈ 0.68–0.75 s; budget 1.7 s.

Map / camera (`skirmish.gd` `project()`, `MAP_SCALE`, `grid_rules.gd`):
- Isometric diamond projection `MAP_OFFSET + Vector2(550 + 44*(x−y), 70 + 26*(x+y)) * 0.94` → one tile ≈ **82.7 × 48.9 px** on a 1280×720 screen.
- Map **11 × 9** (`ROWS` in `grid_rules.gd`, mirrors `ui-prototype/src/playable-l03/rules.ts`); whole map ≈ 827 × 489 px, fully on screen. Terrain is one painted image `art/battlefield.png` (940×627 × 0.94) plus props, not tiles.
- Unit sprites: 512×512 frames, 360 px reference height × (48.88/360) × 0.98 ≈ **48 px tall** on screen.
- Camera is fixed (no scroll, no follow, no edge/drag, no minimap).

## Read first
- `godot-spike/docs/HANDOFF.md` (spike-01 and the "spike-02 A9" section) and `godot-spike/docs/VERIFICATION.md` (A9 commands)
- `godot-spike/scripts/skirmish.gd`, `battle_hud.gd`, `scripts/anim/*`, `scripts/rules/grid_rules.gd`, `shaders/hit_flash.gdshader`, `audio/impact_synth.gd`, `audio/SOURCES.md`
- `shared-anim/manifest.json`, `godot-spike/tools/capture_a9.gd`, the timing/movie evidence in `godot-spike/docs/evidence/spike02-a9/`
- `godot-spike/tests/*` (all 13 scripts) — know which contracts pin `manifest.impact`, timing, hitstop and Reduced Motion
- `docs/tasks/godot-spike-01-hit-feel.md`, `docs/SCOPE.md`, `docs/DECISIONS.md` (if present), `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux), `ui-prototype/src/playable-l03/rules.ts` and `README.md` (read-only, for L03 data)

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `b2f460b`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `godot-spike/` (code, tests, tools, evidence, docs), add `docs/proposals/big-map-proposal.md` (and images next to it under `docs/proposals/big-map/`), and this segment's handoff section. **Nothing under `ui-prototype/`, `docs/art-briefs/` or `main` changes. No swing/idle/knight frame PNG changes. No `shared-anim/` changes**, except, if truly needed, adding a new non-frame key to `shared-anim/manifest.json` — prefer a separate config file instead (see W2).
- Godot 4.7.2 standard build, **GDScript only** for the game. Python allowed for offline evidence tools (GIF/MP4/strips). No C#, no GDExtension, no new addons beyond the vendored GUT. ffmpeg only if already installed; otherwise produce PNG strips + AVI and say so.
- **Rules stay exactly as they are**: damage, HP, knockback cells, walkability, the 11×9 map, G005 all unchanged. The crit variant is **presentation only** (a debug/capture flag), no rules change.
- Swing **frame durations and contact frame stay as in A9** (180 / 70 / 40 / 80 / 100 / 150 ms, contact index 3, anchor (455,196)). Only the impact layer around contact changes.
- Normal attack **strike-to-input-ready ≤ 1.7 s** (hard), target ≤ 1.2 s; crit ≤ 1.7 s too. Reduced Motion must still be ≤ the normal time.
- **Part B changes no gameplay.** The mockup is a separate scene, not the main scene, not wired into rules, real levels, HUD or tests of real levels.
- `rg` is not installed; use `Select-String` or `git grep`.

## Godot
`GODOT` = `C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`
- import: `GODOT --headless --path godot-spike --import`
- GUT: `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`
- movie: `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/<dir>/attack.avi -s res://tools/<capture>.gd -- <flag>`

## Do — Part A: hit feel (implement)
Work in order. **Commit after each step.**

### W1. Measure the current impact timeline and list gaps
- Add `godot-spike/tools/capture_spike03.gd` (reuse `capture_a9.gd` patterns, its own output dir, `CAPTURE_COMPLETE … pass=true` marker). Capture the **open-ground** hit (setup 1) at **1280×720, `--fixed-fps 60`**, and dump **every frame** from 6 frames before contact to input-ready as PNG.
- Record per frame: process frame, ms from strike start, phase, swing frame index, paused/hitstop, camera offset and zoom, target flash value, target position delta, damage-number scale/position, live particle count, SFX trigger. Save `godot-spike/docs/evidence/spike03/before/timeline.json` + `timeline.md` and a **frame strip** of the impact window (`before/impact-strip.png`, contact ±8 frames, frame numbers labelled).
- Write `godot-spike/docs/evidence/spike03/GAPS.md`: each gap vs. genre-standard impact (hitstop length/feel, shake direction/size, flash visibility/length, no target recoil on the hit frame, weak sparks, no dust on a clean hit, no number punch, no zoom punch, single SFX, no crit read). Each gap with the measured value, why it reads weak, and the planned change. Use the RESOURCE-CHECKLIST game-feel items.
- Commit.

### W2. Layered impact on the contact frame (`swing/03`)
1. **One tunable config.** Create `godot-spike/scripts/impact/impact_profile.gd` (`class_name ImpactProfile extends Resource`, exported fields with ranges and comments) and `godot-spike/config/impact_profile.tres` (tuned) plus `godot-spike/config/impact_profile_a9_baseline.tres` (reproduces the A9 values exactly, for the before capture). All impact numbers live there: hitstop (attacker, target), shake, flash, recoil, knockback, particles, dust, damage number, zoom punch, crit multipliers, SFX hook names/volumes. `skirmish.gd` reads the profile; no new magic numbers in code. Leave `manifest.impact` as the A9 record; if a test pins it, keep it pinned. Select the profile with a user arg (e.g. `-- --impact-profile=a9_baseline`) for before/after.
2. **Layers**, all triggered on the same process frame as contact (keep `same_frame_contact` true):
   - **Hitstop** for attacker + target, tuned (suggested 100–130 ms normal, 150–190 ms crit). Keep the real-time minimum guard. If you replace the global tree pause with per-actor freeze, keep HUD/input responsive and keep the existing pause regression tests meaningful.
   - **Directional screen shake** along the hit direction (attacker → target) with exponential falloff, a short sharp first kick then 2–4 decaying oscillations (suggested 6–10 px normal, 10–14 px crit, 150–250 ms). Uses `camera.offset` only; deterministic (seeded) so captures repeat.
   - **Target hit flash**: stronger, readable white/warm flash (e.g. full white 1–2 frames then fade 60–100 ms), optional 1-frame red/bone tint; extend `hit_flash.gdshader` (keep the `flash` uniform name).
   - **Recoil nudge**: target sprite pushed 6–12 px along the hit direction during/just after hitstop and eased back (separate from the rules knockback tween, which still moves to the next cell); a small attacker follow-through lean is optional.
   - **Impact particles**: brighter spark burst with a short streak/flare at the contact anchor, plus **ground dust** at the target's feet on every hit; one-shot, cleaned up, frozen during hitstop.
   - **Damage number pop**: larger (e.g. 26–32 px), scale punch (1.6 → 1.0 overshoot in ~120 ms), then rise and fade; crit uses a bigger number and a different accent colour from the existing palette.
   - **Optional zoom punch**: brief extra zoom (e.g. +0.04–0.08 for 80–120 ms) on top of the attack zoom, returning smoothly.
   - **Crit variant**: presentation-only flag (debug key `C` toggles "next hit crit", plus a capture arg) — stronger hitstop/shake/flash/number, extra particles, distinct SFX hook. Rules damage unchanged.
   - **SFX hooks**: named hook points `swing_whoosh` (frame 1 or 2), `impact`, `impact_crit`, `knockback_thud` / `blocked_thud`. If no real sound exists, synthesize deterministic placeholders in `audio/` and **mark them PLACEHOLDER** in `audio/SOURCES.md` and the handoff. No external downloads.
3. **Reduced Motion**: no shake, no zoom punch, no recoil nudge, no camera zoom; keep the current Reduced Motion contract (00 / 03 / 05 frames, suppressed spark/flash as today unless you document a better accessible choice); the damage number may pop in scale but must not move the camera. Test it.
4. Keep all three setups working (open, unit-blocked, terrain-blocked) and the HUD unchanged in layout.
- Commit.

### W3. Before/after evidence and tests
- With `capture_spike03.gd`, capture **before** (A9 baseline profile) and **after** (tuned), and **after-crit**, each at 1280×720 `--fixed-fps 60`: per-frame timeline JSON, impact frame strips (contact ±8 frames, same layout for before/after, stacked in one `impact-strip-before-vs-after.png`), the `--write-movie` AVI, and, if tooling allows, a **side-by-side GIF or MP4** (`before-vs-after.gif`/`.mp4`, subsample if over ~8 MB; document in `MOVIE.md`). Also 720p stills: `contact.png` (during hitstop), `contact-crit.png`, `number-pop.png`.
- Timing for normal, crit and Reduced Motion × 3 setups in `timing.json`; all ≤ 1.7 s.
- Add `godot-spike/tests/test_spike03_impact.gd` covering at least: profile loads and every field is in range; baseline profile reproduces the A9 values; contact layers fire on the same process frame; hitstop ≥ the profile minimum for normal and crit; shake is directional (first offset along the hit vector) and decays to zero; Reduced Motion produces zero camera offset/zoom change and no recoil; flash returns to 0; damage number scale returns to 1 and frees itself; particles free themselves; SFX hooks fire once each at the right frame; total time ≤ 1.7 s for normal/crit/reduced; rules results identical to A9 (HP, cells) for all three setups.
- Headless import, then GUT: **≥ 79 tests, all green** (earlier tests may only be re-pointed with a recorded reason, never deleted). Save as `godot-spike/docs/evidence/spike03/test-run.log`.
- Commit.

## Do — Part B: big-map proposal (document + mockup only)

### W4. Proposal document
Write `docs/proposals/big-map-proposal.md` (Traditional Chinese main text with English terms where useful; the Owner reads Chinese). Cover:
- **Goal and reference**: 曹操傳-style campaign maps — many tiles, map much larger than the screen, scrolling, big readable tiles/units. Reference feel only; nothing copied.
- **View**: keep the current isometric diamond vs. switch to a top-down / 3/4 square grid (曹操傳 is square). Pros/cons for readability, art cost (painted terrain vs. tiles), unit size, existing code.
- **On-screen tile size** at 1280×720 with options (e.g. 64 / 80 / 96 px; iso width vs. height), how many tiles are visible at once, unit sprite height for each (current ≈ 48 px), HUD safe area, and 1080p scaling.
- **Map sizes per map type** (e.g. skirmish 16×12, standard 24×18, siege/large 32×24 to 40×30) with typical unit counts.
- **Camera**: keyboard/WASD, edge scroll, mouse drag, wheel zoom steps, follow the active unit and enemy turns, snap to events, bounds, minimap option, "centre on unit" key; how the attack zoom and the new impact shake work on a scrolling camera.
- **Fog / zones**: fog of war or not, zone reveals, objective markers off-screen (edge arrows).
- **Level design changes**: deployment zones, reinforcements (timed/triggered, from map edges), objectives (rout, reach, hold, escort, defeat leader), pacing per turn and per map, side paths.
- **Balance impacts**: movement ranges (current 4-neighbour BFS), attack/threat ranges, AI (pathfinding cost, group behaviour, approach), turn length and enemy-turn speed (skip/fast-forward), unit counts.
- **Terrain art pipeline**: painted single image vs. tile set vs. hybrid (painted chunks + tile logic), keeping one dark-fantasy hand-painted style; AI-generation feasibility.
- **Performance**: draw calls, `TileMapLayer`, culling, particles on big maps, GL Compatibility on the AMD 780M.
- **Migration plan** for existing levels, especially L03 (11×9, winch (2,1), crossing): enlarge, rebuild or keep as a small tutorial map.
- **2–3 options** (e.g. A conservative: same iso, 64 px, 24×18; B 曹操傳-like: square 3/4, 80 px, 32×24; C …) with effort, risk and a **recommendation**.
- **Open questions for Gavin** (numbered, each answerable in one line).
- Commit.

### W5. Throwaway mockup
- A separate scene `godot-spike/scenes/mockups/BigMapMockup.tscn` + `godot-spike/scripts/mockups/big_map_mockup.gd`, **not** the main scene and not referenced by the game: an enlarged test map (e.g. 32×24) at the recommended tile size, using existing art tiled/scaled or quick placeholder tiles clearly labelled MOCKUP, a few unit sprites (existing idle frames) at the proposed size, and a scrolling camera (keyboard + edge + drag, clamped bounds, optional minimap corner).
- Capture at 1280×720: overview of the whole map (scaled down), 2–3 scrolled views, and one view per tile-size option if cheap. Save under `docs/proposals/big-map/` and reference them in the proposal; a short scroll movie is optional.
- One smoke GUT test that the mockup scene loads and the camera clamps to bounds is allowed; it must not touch real levels.
- Commit.

### W6. Evidence and verification
- Everything under `godot-spike/docs/evidence/spike03/` (`before/`, `after/`, `after-crit/`, `timing.json`, `MOVIE.md`, `GAPS.md`, `test-run.log`, `source-hashes.json`), with a `README.md` index.
- Add a **"spike-03"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- Check: `git diff --stat b2f460b..HEAD` shows changes only under `godot-spike/`, `docs/proposals/` and this brief; no frame PNG, `shared-anim/`, `ui-prototype/` or `docs/art-briefs/` change.
- Commit.

### W7. Handoff, then stop
Add a section **"spike-03"** to `godot-spike/docs/HANDOFF.md`: how to run (play, toggle crit `C`, Reduced Motion, switch profile), the impact layers and their values (table: A9 → spike-03), where to tune them (`impact_profile.tres`), before/after strips and movie links, timing vs. the 1.7 s budget, the PLACEHOLDER SFX list, the A9 swing frames still PLACEHOLDER (unchanged), the big-map proposal summary with the recommendation and the open questions, what stays open (**human hit-feel playtest HUMAN_PENDING**, Owner decision on the big-map option), limits, and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`. Make this the handoff commit, then **stop**.

## Acceptance
- W1 timeline + strip + GAPS committed.
- All impact values in one `ImpactProfile` resource with an A9-baseline profile; layered impact (hitstop, directional shake, flash, recoil, sparks + dust, number pop, optional zoom punch, crit variant, SFX hooks) on the contact frame; Reduced Motion has no shake/zoom/recoil.
- Before/after/crit 60 FPS captures and frame strips committed; side-by-side GIF/MP4 if tooling allows (else documented).
- Rules results, swing frames and frame timing unchanged; all attacks ≤ 1.7 s.
- `docs/proposals/big-map-proposal.md` with options, recommendation and open questions; mockup scene + 720p captures; no gameplay change.
- GUT exits 0 with ≥ 79 tests; log committed.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W7 handoff commit and wait for review.
