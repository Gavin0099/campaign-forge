# Task Godot spike 04: hit-feel tone-down + first PLAYABLE 24×18 big-map battlefield (Option C)

Authorized by Gavin on 2026-10-24 21:26 (Asia/Taipei), answering the spike-03 review question 「大地圖和打擊感要怎麼往下走？」:
「照 GPT 建議走：方案 C，先做 24×18 可玩戰場，打擊感照建議調淡」 ("follow GPT's advice: Option C, first build a playable 24×18 battlefield, tone the hit feel down as suggested").

## Owner decisions
Unchanged from spike-03:
- campaign-forge uses **Godot directly** (P010 on branch `decision/p010-godot`). React and Phase B are **CANCELLED**. `ui-prototype/` is read-only reference; no React to-dos; do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**.
- One consistent **dark-fantasy hand-painted** style; the game must read as a real tactics RPG, not a tool UI. AI image generation is allowed. Do not adopt the on-hold Ferry Dusk palette.
- **A9 swing frames are development PLACEHOLDER** (Owner, 2026-10-24 18:27). No art work on them: `shared-anim/**`, `godot-spike/art/anim-shared/**` PNGs and everything under `docs/art-briefs/` stay byte-identical; `frame-audit.json` flags unchanged.

New in this segment (Owner, 2026-10-24 21:26), answering the spike-03 handoff questions:
1. Big map = **Option C**: keep the current isometric diamond projection, tiles **160 × 94.5 px** on the 1280×720 reference canvas (half-width 80, 44:26 aspect), figures about **96 px** tall.
2. **Staged**: first a **playable 24×18** battlefield. Do **not** build 32×24 in this segment. That comes later, only if 24×18 passes.
3. Figures **96 px**.
4. **The existing 11×9 Skirmish/L03 stays the small tutorial map, untouched.** The big map is a **new, separate level**.
5. First version has **no fog of war**; the whole map is visible via scrolling and overview.
6. Controls: **WASD/arrow keys + middle-mouse drag + O for overview**. Edge scroll is optional and **off by default**.
7. Target battle length **15–25 minutes** (to be measured, not promised).
8. **Hybrid landscape** accepted: tile terrain + painted chunks + separate props. Graybox/placeholder art is fine if one style is kept and it is labelled PLACEHOLDER.
9. **Tone down the hit feel** per the GPT review (`docs/review/gpt-godot-spike-03.md` on `review/gpt-godot-spike`, summarised below).

This segment builds on spike-03 (`a0ae42c`, GUT 89/89, 8958 assertions).

## GPT review of spike-03 (CONDITIONAL ACCEPT), the parts that drive this segment
- **Flash** over-exposes the figure, so character detail disappears. Lower the mix to about **0.8**.
- **Sparks** are too dense and hide the figures. Reduce them, keeping the **directional** sparks first.
- **Damage numbers** are too heavy. Make them **10–15 % smaller**.
- **Shake (8/12 px), hitstop, recoil and dust stay** for now and get tuned after a human playtest. SFX are still PLACEHOLDER.
- **Big map:** C at 160 px / 96 px is sensible. The main risk is that a bigger map does not mean deeper tactics. Long walks delay contact, and ranged or high-mobility units may gain outsized advantage. Validate 24×18 first, then 32×24.
- **Next:** a controllable 24×18 battlefield that proves the camera, scrolling, finding enemies and engagement pacing; test melee vs ranged vs high-mobility balance. Two images do not prove the real operating experience.

## Current state (verify yourself from `a0ae42c`)
- Main scene `res://scenes/Skirmish.tscn` → `scripts/skirmish.gd`: one-attack spike on the 11×9 map, fixed Camera2D (640,360), attack zoom 1.4, layered impact read from `config/impact_profile.tres` (`ImpactProfile`), baseline `config/impact_profile_a9_baseline.tres`, `-- --impact-profile=a9_baseline`, crit presentation `C` / `--crit`, Reduced Motion `M`.
- Rules `scripts/rules/grid_rules.gd`: 11×9 `ROWS`, `SPIKE` damage 2, 4-neighbour BFS move (no per-turn move limit), adjacent attack with 1-cell knockback / blocked events. No turns, no enemy AI, no ranged attack, no objectives.
- Units available: Thoma (idle + A9 swing PLACEHOLDER), knight-a and knight-b (idle / hit / stagger). There is no ranged or mounted art.
- Mockup `scenes/mockups/BigMapMockup.tscn` + `scripts/mockups/big_map_mockup.gd` (32×24, 160 px option, WASD/drag/edge/wheel/O/F, display-only minimap), capture `tools/capture_big_map.gd`, smoke test `tests/test_big_map_mockup.gd`. It is throwaway: you may read and copy ideas from it, but do not wire it into the game.
- L03 reference data (move ≤ 3 steps via path length ≤ 4, enemy intent/approach turn) is in `ui-prototype/src/playable-l03/rules.ts` (read-only).
- spike-03 tuned profile values: flash_mix 1.0, flash_ms 80, spoke_count 11, spoke_width 2, streak 22 px, spark_count 36, crit_particle_multiplier 1.5, number_font_px 28 / crit 34, number_scale 1.6 × crit multiplier 1.125, hitstop 110 / crit ×1.545, shake 8 px / crit ×1.5, recoil 9 px, dust on contact, zoom punch 0.06.

## Read first
- `godot-spike/docs/HANDOFF.md` ("spike-03" section) and `godot-spike/docs/VERIFICATION.md` ("spike-03")
- `docs/tasks/godot-spike-03-hitfeel-bigmap.md` (previous brief), `docs/proposals/big-map-proposal.md` and `docs/proposals/big-map/README.md`
- `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-03.md` (the review, read-only)
- `godot-spike/scripts/skirmish.gd`, `battle_hud.gd`, `scripts/impact/impact_profile.gd`, `config/*.tres`, `scripts/anim/*`, `scripts/rules/grid_rules.gd`, `scripts/mockups/big_map_mockup.gd`, `tools/capture_spike03.gd`, `tools/capture_big_map.gd`
- `godot-spike/tests/*` (all 15 scripts). Know which tests pin profile values, the main scene, Skirmish timing and the mockup.
- `docs/SCOPE.md`, `docs/review/RESOURCE-CHECKLIST.md` (level-design, game-ai, game-ui-ux, game-feel, prototype-fast), `ui-prototype/src/playable-l03/rules.ts` (read-only)

## Hard boundaries
- **Worktree:** work only in `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `a0ae42c`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- **What you may change:** only `godot-spike/` (code, config, tests, tools, evidence, docs) and this segment's handoff/verification sections.
- **Protected paths:** nothing under `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/` (read-only this time) or `main` changes. No `shared-anim/` changes. No swing/idle/knight frame PNG changes.
- **New art:** new terrain/prop/marker art for the new level is allowed under `godot-spike/art/bigmap/`. It may be programmatic, placeholder or AI-generated, in one dark-fantasy hand-painted direction, and must be labelled PLACEHOLDER in a `SOURCES.md`. No external downloads of third-party assets.
- **Skirmish / L03 stays exactly as it is:**
  - `grid_rules.gd`, the 11×9 map and its three setups;
  - damage 2, HP, knockback cells, walkability and G005;
  - the Skirmish HUD layout and the swing frame timing (180/70/40/80/100/150 ms, contact 3, anchor (455,196)).
  - Only the impact profile values change (W1).
  - `Skirmish.tscn` stays the main scene, unless you add a small, documented launcher. Prefer a command-line scene path or a key on a title-free start, and keep every existing test passing unchanged.
- **New level rules go in a NEW pure rules module** (e.g. `scripts/rules/field_rules.gd`) plus level data (e.g. `data/levels/field_24x18.json` or a `.gd` const):
  - Never edit `grid_rules.gd`.
  - New numbers (move ranges, HP, ranged range, AI) are **spike test values, not canon**. Mark them as such in data and docs.
  - Melee attacks in the new level reuse the Skirmish semantics (damage 2, 1-cell knockback / blocked), unless a test value below says otherwise.
- **Toolchain:** Godot 4.7.2 standard, **GDScript only** for the game. Python allowed for offline evidence tools (Pillow is present). No C#, no GDExtension, no new addons beyond the vendored GUT. ffmpeg is **not** installed: produce PNG strips + `--write-movie` AVI (and a GIF via Pillow if useful) and say so. `rg` is not installed: use `Select-String` or `git grep`.
- **Attack timing:** normal attack strike-to-input-ready ≤ 1.7 s (hard), target ≤ 1.2 s, in both Skirmish and the new level. Reduced Motion ≤ normal.
- **Tests:** GUT must end with **≥ 89 tests, all green**. Earlier tests may only be re-pointed with a recorded reason (e.g. W1 profile values), never deleted or weakened.

## Godot
`GODOT` = `C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`
- import: `GODOT --headless --path godot-spike --import`
- GUT: `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`
- movie: `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/<dir>/<name>.avi -s res://tools/<capture>.gd -- <flags>`
If the first command cannot find Godot or Python (PATH/sandbox), retry with the full path / escalation before giving up, and record it.

## Do
Work in order. **Commit after each W step** (`git -c user.name=Gavin0099 -c user.email=Gavin0099@users.noreply.github.com commit ...`).

### W1. Hit-feel tone-down (Skirmish, presentation only)
- Copy the current tuned profile byte-for-byte to `godot-spike/config/impact_profile_spike03.tres`, so it can be selected with `-- --impact-profile=spike03`. Keep `impact_profile_a9_baseline.tres` unchanged.
- Edit `godot-spike/config/impact_profile.tres` (the new default, "spike04 toned"):
  - **flash:** `flash_mix` **0.8**. Keep flash_ms/hold, or shorten slightly if the strip shows the figure still blown out; record the choice. Crit flash must stay ≤ 1.0 effective mix and readable.
  - **sparks:** cut the radial/random spray clearly (suggested `spark_count` 36 → about 20–24, `spoke_count` 11 → about 6–8, crit multiplier ≤ 1.35). **Keep the directional streak** and bias the remaining sparks along the hit direction, so the figure's silhouette is not covered. If biasing needs a new field, add it to `ImpactProfile` with range + comment (baseline default reproduces A9).
  - **damage numbers:** **10–15 % smaller** for normal and crit (suggested font 28 → 24, crit 34 → 29–30, or the equivalent via scale). Keep the pop but don't let it cover the figure's head.
  - **unchanged:** hitstop, shake, recoil, dust, zoom punch, knockback, SFX.
- Capture with `tools/capture_spike03.gd` (or a `capture_spike04.gd` copy), all at 1280×720 `--fixed-fps 60`:
  - spike03 vs spike04 **normal** and **crit** contact stills;
  - one stacked strip `godot-spike/docs/evidence/spike04/hitfeel/impact-strip-spike03-vs-spike04.png` (contact ±8 frames, same layout);
  - AVIs;
  - timing for normal/crit/Reduced Motion × 3 setups in `hitfeel/timing.json`.
- Tests: re-point the spike-03 profile-value tests to `impact_profile_spike03.tres` (recorded reason). Add tests that the default profile has flash_mix 0.8 (±0.02), fewer sparks/spokes than spike03, numbers 10–15 % smaller (normal and crit), hitstop/shake/recoil/dust equal to spike03, and that the a9_baseline/spike03/default profiles all load and select via the user arg.
- Commit.

### W2. Pure rules + level data for the 24×18 field (no presentation)
- New `scripts/rules/field_rules.gd` (pure functions, inputs never mutated, results as events like `grid_rules.gd`), driven by level data. **Map 24×18**, 4-neighbour grid, terrain types with walkability and move cost:
  - at least plain, road, forest (cost 2), shallow ford (cost 2), deep water / cliff (impassable);
  - one optional raised or defensive tile type if cheap.
- **Turn loop:** player phase (each unit may move once, then act once: attack or wait), then enemy phase, then reinforcement/objective checks, then the next turn. There is a turn counter and win/lose results.
- **Spike test archetypes** (data, not canon; reuse existing art, see W3):
  - **Melee** (Thoma-type): move 4, HP 8, adjacent attack 2 dmg + knockback.
  - **Ranged** (archer test): move 3, HP 6, attack at range 2–3 (Manhattan), 2 dmg, no knockback, cannot attack adjacent. Either no line of sight, or a simple documented rule.
  - **High-mobility** (skirmisher/rider test): move 6, HP 6, adjacent attack 2 dmg, extra cost in forest.
  - **Enemy knights** reuse melee stats (HP 6). **Enemy leader:** HP 10, holds a position until threatened.
  - Tune only in data. Record all values in a table in the handoff.
- **Party / opposition:** about **5–6 allies** (at least 2 melee, 1–2 ranged, 1–2 high-mobility) vs. about **10–14 enemies** at start, plus **one reinforcement wave**. Deploy allies on one side. Place the first meaningful contact about **8–15 steps** from deployment (per the proposal). Provide a main road and at least one side path with a different cost (e.g. ford or forest flank).
- **Objective (not rout):**
  - Primary win: **defeat the enemy leader** (or **hold** a marked point for N turns; pick one, document it, the other may be secondary).
  - Lose: Thoma falls, or a turn limit (e.g. 15) is exceeded.
  - Objective, win/lose and turn limit must be readable at battle start.
- **Reinforcements:** spawn from a map-edge entry at a fixed turn or trigger. They must be **announced at least one full turn before** they arrive (event `reinforcement_warning` with turn, entry cell(s), unit kinds). Arrivals never act on the turn they appear. If an entry cell is occupied, use a documented fallback.
- **Simple, explainable enemy AI:** groups with states idle/guard → alert (an ally enters an alert radius or a group member is attacked) → approach → attack.
  - Leader holds unless attacked or the hold point is contested.
  - Path cost via Dijkstra/BFS with a shared distance map, invalidated when occupancy changes.
  - Deterministic (seeded tie-breaks), so tests and the auto-playtest are reproducible.
- **Tests** (`tests/test_field_rules.gd`): map size 24×18 and terrain data; move ranges per archetype with terrain cost; ranged min/max range; melee knockback/blocked parity with Skirmish semantics; turn order; win by objective; lose conditions; reinforcement warning ≥ 1 turn ahead, with arrival on the announced turn at the announced entry; AI determinism; inputs not mutated.
- Commit.

### W3. Battlefield scene at Option C scale
- New scene `scenes/levels/Field24x18.tscn` + `scripts/levels/field_battle.gd` (+ small helper scripts as needed). **Not** the Skirmish scene. Do not reference the mockup scene.
- Launch with `GODOT --path godot-spike res://scenes/levels/Field24x18.tscn`. Optionally add a documented key/arg to open it from Skirmish without changing Skirmish's default behaviour or tests.
- **Projection:** isometric diamond, tile **160 × 94.5 px** at zoom 1.0 on the 1280×720 canvas. Figures **≈ 96 px** tall (reference_height 360 scaled). Feet pivot as in Skirmish. 1080p uses the existing canvas_items stretch.
- **Hybrid landscape** under `godot-spike/art/bigmap/` (PLACEHOLDER, one dark-fantasy hand-painted direction, consistent light direction and perspective):
  - ground tiles via `TileMapLayer` or a batched draw, from the rules data — never infer terrain from the painting;
  - a few painted chunks (river bank/ford, road crossing);
  - separate y-sorted props (trees, rocks, a banner/marker for the objective) with occlusion fade when a unit is behind them.
  - A clear but subtle grid overlay that can be toggled.
- **Units:** reuse existing art, no new figure art.
  - Allies use Thoma idle frames.
  - Melee can use the **A9 PLACEHOLDER swing frames as-is** for attacks. Ranged and high-mobility test units reuse Thoma or knight frames with a distinct, readable, non-colour-only badge/silhouette marker (e.g. bow / boot icon plus label). The leader uses a knight with a banner/crown marker.
  - Mark all of these as PLACEHOLDER.
  - A ranged attack can be a simple projectile/arc using the impact profile (no new frames).
- **Interaction:** click/keyboard select → move-range highlight (cost-aware) → move → attack-target highlight (melee adjacent, ranged band) → attack or wait. Also: end-turn button/key, cancel (Esc / right-click, without colliding with camera drag), hover info (HP, archetype, move/range), enemy threat overlay toggle, and a turn/phase banner.
  - **Enemy phase:** visible, with a fast-forward (e.g. hold Shift / 2× toggle) and skip-movement option.
  - **Reduced Motion** works here too.
- **Impact:** the hit-feel layers on melee contact use the same `ImpactProfile` (default = W1 toned). Reuse the Skirmish implementation by extracting a shared presentation helper **only if** Skirmish behaviour, evidence and all existing tests stay identical. Otherwise keep a small adapter and record why.
- Commit.

### W4. Scrolling camera
- Camera has three layers (per the proposal): **base position** (pan/follow, clamped) + **attack focus** (save before, return to the **pre-attack** position afterwards, never to (640,360)) + **impact offset** (shake only via offset, limited so it never reveals beyond the bounds).
- **Controls:**
  - pan: WASD / arrow keys, with speed scaled by zoom; middle-mouse drag;
  - **O** toggles an overview zoom that shows the whole 24×18 map. Reading mode; selecting from overview may centre the camera;
  - wheel zoom steps 0.8 / 1.0 / 1.2 (1.5 optional), anchored at the cursor;
  - **F / Home** centres on the selected unit;
  - edge scroll implemented but **off by default** (setting toggle).
- **Follow:** smooth follow of the active/selected ally. During the enemy phase, pan to visible relevant actions (attacks, arrivals) with a short announce. Reduced Motion snaps instead of panning. No drift without an event.
- **Clamping:** the camera is clamped to the map's world bounds at every zoom, including after zoom changes and during shake. HUD-safe margins keep edge tiles reachable/selectable.
- **Tests** (`tests/test_field_camera.gd`):
  - clamp at all four edges and every zoom step;
  - WASD/arrow pan moves the base by the expected amount (simulated input events);
  - middle-drag pan;
  - O overview fits the full map and toggles back to the previous position/zoom;
  - the attack returns to the pre-attack base position;
  - shake never pushes the view outside the bounds;
  - Reduced Motion: no shake/zoom punch, snap follow.
- Commit.

### W5. Minimap, off-screen indicators, objective and reinforcement UI
- **Minimap** (corner, collapsible): terrain thumbnail, ally/enemy/leader dots with **shape as well as colour**, the objective marker, reinforcement entries, the viewport rectangle. **Click to move the camera.** It must not cover the core tactical area at 720p.
- **Off-screen indicators:** labelled edge arrows for enemies near/threatening allies, the leader/objective and announced reinforcement entries. Clamped to the screen edge, inside the HUD-safe area. Clicking one centres the camera.
- **Objective panel:** goal, lose conditions, turn x / limit. On a reinforcement warning, show a banner + marker one turn ahead ("增援：第 N 回合，從東北渡口，3 名騎士" style text; Traditional Chinese UI text with English debug is fine). The camera may briefly show the entry (snap in Reduced Motion).
- No fog of war.
- **Tests** (`tests/test_field_ui.gd`):
  - minimap world↔map transform and click → camera;
  - viewport rect matches the camera;
  - indicators appear only for off-screen targets, point in the right direction and stay inside the screen;
  - the objective panel shows the correct state;
  - the reinforcement warning shows ≥ 1 turn before arrival and its marker matches the entry cell;
  - win/lose screens trigger from rules results.
- Commit.

### W6. Instrumentation, auto-playtest and evidence
- **Telemetry** in the new level (debug overlay `F1` + JSON log): turn of first contact (first attack by either side), per-unit move distance per turn and the average per archetype, attacks by archetype, damage dealt/taken per archetype, idle turns (units that could not reach anything), enemy-phase duration in seconds (normal and fast-forward), turns to win/lose.
- **Deterministic auto-playtest** (`tools/autoplay_field.gd`, headless): scripted ally policies, e.g.:
  - (a) push the main road;
  - (b) flank via the side path;
  - (c) turtle and use ranged.
  - Each runs to a result and writes `docs/evidence/spike04/autoplay/<policy>.json`. Summarise in `docs/evidence/spike04/PACING.md`:
    - turns to first contact (target: contact by turn 2–3, about 8–15 steps);
    - average move distance;
    - battle-length estimate = turns × (measured enemy-phase time + an assumed player think time per unit, stated explicitly, e.g. 15–25 s), compared with the 15–25 min target;
    - per-archetype share of damage/kills, flagging if ranged or high-mobility dominates (e.g. > 50 % of damage) or melee rarely engages.
  - If pacing is clearly off (e.g. no contact before turn 4, or an estimate over 35 min), adjust **level data only** (deployment/positions/reinforcement turn), rerun, and keep both runs in the log.
- **Captures** at 1280×720 (plus one native 1080p still):
  - deployment view, first contact, ranged attack, melee hit with the toned impact on the big map, O overview, minimap + off-screen arrows, reinforcement warning, enemy phase, win screen;
  - a 60 FPS `--write-movie` AVI of a scroll → select → move → attack sequence, and one of an enemy phase;
  - PNG strips of the camera follow/return;
  - everything goes under `godot-spike/docs/evidence/spike04/`, with `MOVIE.md` (ffmpeg missing → AVI + PNG strips (+ optional Pillow GIF, under ~8 MB)).
- **Performance note:** average and worst frame time at 720p during scroll + enemy phase on this PC (AMD 780M, GL Compatibility), measured not assumed.
- Commit.

### W7. Verification and scope audit
- Headless import, then full GUT: **≥ 89 tests, all green**, with the new count and assertions. Save to `godot-spike/docs/evidence/spike04/test-run.log`.
- Skirmish regression:
  - all three setups still give identical rules results (HP, cells);
  - timings ≤ 1.7 s for spike04-default / crit / Reduced Motion;
  - a9_baseline and spike03 profiles still reproduce their values.
- Add a **"spike-04"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- `git diff --stat a0ae42c..HEAD` must show changes only under `godot-spike/` and this brief. Confirm there are no changes to frame PNGs, `shared-anim/`, `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/` or `grid_rules.gd`. Record source hashes (`docs/evidence/spike04/source-hashes.json`) and add a `README.md` index.
- Commit.

### W8. Handoff, then stop
Add a section **"spike-04"** to `godot-spike/docs/HANDOFF.md` (Traditional Chinese main text, like spike-03) covering:
- how to run (Field24x18 scene, controls, F1, Reduced Motion, profile switch `a9_baseline` / `spike03` / default);
- the hit-feel changes as a table (spike-03 → spike-04) with strip links;
- the field level: map, terrain, archetype table (test values), party/enemies, objective, reinforcement schedule, AI behaviour;
- camera/minimap/indicator behaviour;
- the pacing results (first contact, move distance, battle-length estimate vs 15–25 min, archetype balance), with honest caveats that the auto-playtest is not a human;
- performance numbers;
- PLACEHOLDER lists (terrain/props, unit stand-ins, A9 swing frames, SFX);
- what is **HUMAN_PENDING**: Gavin plays a full battle, judges camera comfort, readability at 96 px, the toned hit feel, pacing and balance;
- risks;
- **numbered open questions for Gavin**, each answerable in one line (e.g. objective type, move ranges, whether to proceed to 32×24, whether to keep edge scroll off, fast-forward default);
- a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`;
- the commit table.

Make this the handoff commit, then **stop**.

## Acceptance
- W1: the default profile is toned (flash ≈ 0.8, fewer sparks with the directional streak kept, numbers 10–15 % smaller); the spike03 and a9_baseline profiles are selectable; before/after strip + timing are committed.
- A new, separate 24×18 Field level at 160 × 94.5 px tiles and ≈ 96 px figures is **playable from deployment to a win or lose** by a human with mouse + keyboard, with a non-rout objective and a reinforcement wave announced ≥ 1 turn ahead.
- Camera: WASD/arrows, middle-drag, O overview, wheel steps, follow, pre-attack return and bounds clamp all work. Minimap (clickable) and off-screen indicators work. No fog.
- Telemetry + auto-playtest pacing report with a battle-length estimate and an archetype balance note; 720p captures + 60 FPS AVIs committed.
- Skirmish/L03 rules, swing frames, frame timing, `grid_rules.gd`, `shared-anim/`, `docs/art-briefs/`, `docs/proposals/`, `ui-prototype/` and `main` unchanged; all attacks ≤ 1.7 s.
- GUT exits 0 with ≥ 89 tests (plus the new rules/camera/UI/profile tests); log committed.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. If something is ambiguous, choose the safest option inside this brief, record it in the handoff, and continue. Stop after the W8 handoff commit and wait for review.
