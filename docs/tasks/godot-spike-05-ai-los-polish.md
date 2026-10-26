# Task Godot spike 05: enemy AI pressure + ranged line of sight + hit-feel/camera/HUD polish (24×18 field)

Authorized by Gavin on 2026-10-26 10:19 (Asia/Taipei), answering the spike-04 review question 「下一步要怎麼做？」:
「開始 spike-05：修敵人 AI、加遠程視線檢查、閃白和數字再調淡、修鏡頭和標籤」 ("start spike-05: fix the enemy AI, add a ranged line-of-sight check, tone the flash and numbers down further, fix the camera and labels").

## Owner decisions
Unchanged from spike-04:
- campaign-forge uses **Godot directly** (P010 on branch `decision/p010-godot`). React and Phase B are **CANCELLED**. `ui-prototype/` is read-only reference; do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**.
- One consistent **dark-fantasy hand-painted** style. AI image generation is allowed. Do not adopt the on-hold Ferry Dusk palette.
- **A9 swing frames are development PLACEHOLDER.** No art work on them.
- Big map is **Option C** (160 × 94.5 px diamond tiles, ≈ 96 px figures), **staged at 24×18**. **Do not build 32×24** in this segment. No fog of war.
- The 11×9 Skirmish/L03 stays the small tutorial map, untouched.

New in this segment (Owner, 2026-10-26 10:19), in this priority order (from the GPT review of spike-04):
1. **Enemy AI**: no idle knights, real pressure, a defended leader, reinforcements that are hard to bypass.
2. **Rules credibility**: a ranged **line-of-sight** check, terrain blocking/cover, threat range that matches the rules.
3. **Hit feel**: the white contact flash and the damage numbers are still too strong. Lower them further. **Keep hitstop, directional shake, recoil and dust.**
4. **Camera/HUD**: no figures clipped at the edge of the scrolled view, readable figures/markers in O overview, no label overlap.
5. **No map growth and no art investment** this round.

**Gavin has NOT answered the spike-04 open questions.** Keep the current defaults and carry the questions over unchanged:
- win = **defeat the enemy leader** (lose: Thoma falls or turn > 15);
- move **4 / 3 / 6** (melee / ranged / high-mobility);
- edge scroll **OFF** by default;
- enemy phase at **normal** speed by default (2× stays a toggle);
- whether reinforcements **must** engage is open; this segment makes them actively pursue/intercept (Owner priority 1), but do not change the objective type to force it.

This segment builds on spike-04 (`905c0ce`, GUT 123/123, 10,310 assertions).

## spike-04 findings that drive this segment
From `godot-spike/docs/evidence/spike04/PACING.md`, `PERFORMANCE.md` and the HANDOFF "spike-04" section:
- Road policy won on turn 12 (estimate 12.9–21.2 min). Flank lost on turn 7. Turtle lost on turn 3. All first contact on turn 2.
- Road enemy knights had **72 no-target unit-phases**. Rear guards and the reinforcement wave **can be bypassed** (leader-kill objective).
- Road: melee 53.1 % damage / 40 % kills; **ranged 31.2 % damage but 60 % kills** (no LOS, last-hit bias); **high-mobility 15.6 % damage, 0 kills, dies early**.
- 720p frame time: scroll avg 19.7 ms (worst 42.9), enemy phase avg 22.8 ms (worst 30.4). No stable 60 FPS guarantee.
- spike-04 default profile: flash_mix 0.8 (hold 16.67 ms / 80 ms), sparks 22 / spokes 7, crit particle ×1.3, directional bias 0.8, streak 22 px, numbers 24 / crit 30 px; hitstop/shake/recoil/dust/zoom/SFX as spike-03.

GPT review of spike-04 (`git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-04.md`, CONDITIONAL ACCEPT):
- Contact flash still too prominent: hides the figure and the weapon contact. Damage numbers too prominent. Lower flash coverage and particle density; keep hitstop and directional shake.
- O overview: figures too small to operate from, only fit for reading.
- Scrolled view: some figures clipped, labels overlap; enemy group text overlaps scene props; the three reinforcement markers are too loud.
- Pacing only partly in 15–25 min; flank/turtle failing suggests low strategic tolerance. 72 idle knights + bypassable reinforcements = enemies don't apply sustained pressure.
- Ranged may dominate kills without LOS. High-mobility needs better entry routes, escape and role, **not more damage**.
- Next: AI → rules (LOS, terrain, threat, reinforcement triggers) → flash/numbers → camera/HUD → human blind tests of road/flank/turtle.

## Read first
- `godot-spike/docs/HANDOFF.md` ("spike-04" section) and `godot-spike/docs/VERIFICATION.md` ("spike-04")
- `docs/tasks/godot-spike-04-bigmap-24x18.md` (previous brief)
- `godot-spike/docs/evidence/spike04/PACING.md`, `PERFORMANCE.md`, `README.md`, `autoplay/*.json`
- `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-04.md` (read-only)
- `godot-spike/scripts/rules/field_rules.gd`, `data/levels/field_24x18.gd`, `scripts/levels/field_*.gd`, `scripts/impact/impact_profile.gd`, `config/*.tres`, `tools/autoplay_field.gd`, `tools/field_policy.gd`, `tools/capture_field*.gd`, `tools/capture_spike04.gd`
- `godot-spike/tests/*` (all 21 scripts). Know which tests pin profile values, field AI behaviour, the field data, camera clamps and UI.
- `docs/SCOPE.md`, `docs/review/RESOURCE-CHECKLIST.md` (level-design, game-ai, game-ui-ux, game-feel, prototype-fast)

## Hard boundaries
- **Worktree:** work only in `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `905c0ce`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- **What you may change:** only `godot-spike/` (code, config, data, tests, tools, evidence, docs) and this segment's handoff/verification sections.
- **Protected paths:** nothing under `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/`, `shared-anim/` or `main` changes. No swing/idle/knight frame PNG changes. No new figure art; no new art investment (small marker/label/HUD tweaks are fine).
- **Skirmish / L03 stays exactly as it is:** `grid_rules.gd`, the 11×9 map and its three setups, damage 2, HP, knockback cells, walkability, G005, the Skirmish HUD layout and the swing frame timing (180/70/40/80/100/150 ms, contact 3, anchor (455,196)). Only the impact profile values change (W4). Do not edit `grid_rules.gd` unless strictly needed; if you must, justify it in the handoff and keep every Skirmish test byte-for-byte green.
- **Field rules** stay in `scripts/rules/field_rules.gd` + `data/levels/field_24x18.gd` (pure functions, inputs never mutated, results as events). All numbers (AI radii, LOS/cover, terrain tweaks) are **spike test values, not canon**. Mark them as such in data and docs.
- **Map size stays 24×18.** No 32×24. No fog. Objective type, turn limit, move ranges, HP, damage and reinforcement count stay as in spike-04 (the open questions are Gavin's to answer). Small **terrain/position** tweaks are allowed only for W3 (routes/retreat for high-mobility) and must be listed.
- **Toolchain:** Godot 4.7.2 standard, **GDScript only** for the game. Python allowed for offline evidence tools (Pillow is present). `PYTHON` = `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe` (use the full path; it may not be on PATH in your sandbox). No C#, no GDExtension, no new addons beyond the vendored GUT. ffmpeg is **not** installed: produce PNG strips + `--write-movie` AVI (and a GIF via Pillow if useful) and say so. `rg` is not installed: use `Select-String` or `git grep`.
- **Attack timing:** normal attack strike-to-input-ready ≤ 1.7 s (hard), target ≤ 1.2 s, in both Skirmish and the field. Reduced Motion ≤ normal.
- **Tests:** GUT must end with **≥ 123 tests, all green**. Earlier tests may only be re-pointed with a recorded reason (e.g. W4 profile values, W2 AI behaviour that was pinned on purpose), never deleted or weakened.

## Godot
`GODOT` = `C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`
- import: `GODOT --headless --path godot-spike --import`
- GUT: `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`
- field: `GODOT --path godot-spike res://scenes/levels/Field24x18.tscn`
- movie: `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/<dir>/<name>.avi -s res://tools/<capture>.gd -- <flags>`
If the first command cannot find Godot or Python (PATH/sandbox), retry with the full path / escalation before giving up, and record it.

## Do
Work in order. **Commit after each W step** (`git -c user.name=Gavin0099 -c user.email=Gavin0099@users.noreply.github.com commit ...`).

### W1. Baseline ("before") metrics
- Re-run the spike-04 auto-play (`tools/autoplay_field.gd`) for **road / flank / turtle** at seed 24018 on the unchanged `905c0ce` code and data. Confirm it reproduces spike-04's results (road win 12, flank lose 7, turtle lose 3); if not, record why.
- Extend telemetry/autoplay output **without changing game behaviour** so each run records at least:
  - enemy **idle unit-turns** (no target reachable and no meaningful move), split by group (front / flank / rear / leader / reinforcement);
  - turns to first contact; turn the reinforcement wave first engages (or "never");
  - per-class damage share and kill share (melee / ranged / high-mobility), including ranged shots that would be **blocked by the W3 LOS rule** (count only, no behaviour change yet);
  - ally deaths per class and the turn each died;
  - win/loss and turn; battle-length estimate with the spike-04 formula (`turns × (measured enemy-phase mean + living allies/turn × assumed 15–25 s)`).
- Save to `godot-spike/docs/evidence/spike05/baseline/<policy>.json` and a short `baseline/BASELINE.md` table.
- Commit.

### W2. Enemy AI: pressure, no idling, defended leader, reinforcements that intercept
- Keep the AI **simple, explainable and deterministic** (seeded tie-breaks, no global RNG). Document every state and trigger in the handoff.
- **Activation triggers** for guard groups (any one is enough): an ally enters a sight radius (test value, e.g. 6–7 cells, path or Manhattan, document which); a member of the group or a neighbouring group is attacked; a turn timer (e.g. rear guards march from turn 3–4). Once active a group does not go back to idle.
- **No idling:** an active unit that cannot attack this turn must still advance toward the best target cell or regroup point; "stand still" only if it is a deliberate role (leader guard, holding a choke) and is logged as such, not as idle.
- **Pressure:** groups advance as a loose front (don't string out single-file), regroup with nearby allies before charging when outnumbered, and **focus** (low HP → threat to leader → closest, with a documented order). Prefer attacking exposed ranged/high-mobility units when reachable, but do not ignore melee in the way.
- **Leader protection:** the leader holds its point, but 1–2 bodyguards stay within a short radius and intercept allies approaching the leader; the leader may step back to a safer adjacent cell or counter when threatened (document the rule).
- **Reinforcements:** still announced **≥ 1 full turn ahead** (unchanged warning event, entry cells, kinds) and never act on their arrival turn. After arrival they **actively pursue/intercept**: target the allied group nearest the leader or the leader's approach path, so a rush past them is contested. They must be hard to fully bypass. If the arrival turn/entry needs to change for this, keep the announcement rule and record the change.
- Path cost stays Dijkstra/BFS with shared distance maps, invalidated on occupancy changes. Watch the enemy-phase cost (spike-04: avg 22.8 ms/frame); no per-unit full-map recomputation if avoidable.
- **Tests** (`tests/test_field_ai.gd` or extend `test_field_rules.gd`): each activation trigger; no idle active unit when a path exists; group cohesion/regroup; focus order; bodyguard interception; leader step-back/counter rule; reinforcements pursue and engage within N turns in a scripted bypass scenario; determinism (same seed → same events); inputs not mutated. Re-point any spike-04 test that pinned the old idle behaviour, with a recorded reason.
- Commit.

### W3. Ranged line of sight + terrain credibility
- Add a **line-of-sight** rule on the diamond grid for ranged attacks (range 2–3 unchanged, still cannot shoot adjacent). Choose and document one simple rule, e.g. a supercover/Bresenham line through cell centres in grid space:
  - **cliffs / deep-water banks you choose** and **forest** cells along the line (not the target cell) block, or forest gives **cover** instead (pick one; if cover, define it as a simple deterministic effect such as −1 damage, minimum 1; never random);
  - **units** in between block or give cover (pick one and document);
  - corner/diagonal tie cases resolved deterministically (document).
- Enemy AI and the auto-play policies must respect LOS too (enemy ranged units if any; otherwise just the player side).
- **Threat overlay (V), target highlight and attack preview reflect LOS** (blocked targets are not offered; cover shown in the preview). Hover info states the LOS/cover reason.
- **High-mobility routes (optional, small):** if the data shows scouts have no useful flanking or retreat options, make **small terrain/position tweaks** (e.g. a second ford cell, a gap in the south forest, a safe pocket behind the line) so they get entry routes and escape space. **No damage or HP buff.** List every changed cell in the handoff and keep the road/ford layout recognisable.
- **Tests:** LOS clear/blocked/cover cases incl. forest, cliff, unit in between, diagonal ties, min/max range; overlay/preview consistent with rules; any terrain tweak covered by the field data tests.
- Commit.

### W4. Hit feel: flash and numbers down again (presentation only)
- Copy the current default profile byte-for-byte to `godot-spike/config/impact_profile_spike04.tres` (selectable with `-- --impact-profile=spike04`). Keep `impact_profile_a9_baseline.tres` and `impact_profile_spike03.tres` unchanged.
- Edit `godot-spike/config/impact_profile.tres` (new default, "spike05 toned"):
  - **flash:** lower `flash_mix` to about **0.6** and/or shorten the flash so the figure and the mace contact stay readable (no blown-out silhouette). Record the choice and the strip frames that justify it. Crit effective mix ≤ 0.8.
  - **sparks:** optionally trim density a little more if the strip still hides the figure; keep the directional streak and bias.
  - **damage numbers:** another **10–15 % smaller** than spike-04 (e.g. 24 → ~21, crit 30 → ~26) or the equivalent via scale; keep the pop short and keep it off the figure's head.
  - **unchanged:** hitstop, directional shake, recoil, dust, zoom punch, knockback, SFX.
- Apply the same profile to the field level's impact adapter.
- Captures at 1280×720 `--fixed-fps 60`: spike04 vs spike05 **normal** and **crit** contact stills; one stacked strip `godot-spike/docs/evidence/spike05/hitfeel/impact-strip-spike04-vs-spike05.png` (contact ±8 frames, same layout as spike-04); AVIs; timing for normal/crit/Reduced Motion × 3 Skirmish setups in `hitfeel/timing.json`; one field melee hit still.
- **Tests:** re-point the spike-04 profile-value tests to `impact_profile_spike04.tres` (recorded reason). Add tests that the default has the lower flash (value/duration), numbers 10–15 % smaller than spike04 (normal and crit), hitstop/shake/recoil/dust equal to spike04, and that a9_baseline/spike03/spike04/default all load and select via the user arg.
- Commit.

### W5. Camera and HUD: no clipped figures, readable overview, no label overlap
- **Clipping:** in the scrolled view no unit (full 96 px figure incl. head, HP bar and badge) may be cut by the screen edge or hidden under HUD panels when it is the selected/acting unit or an attack target. Add HUD-aware safe margins to follow/focus logic (and to the pre-attack/enemy-action pans) so actors are brought fully inside. Keep the camera clamp to the world bounds at every zoom.
- **Overview (O):** make figures readable at overview scale, e.g. scaled-up unit markers/icons with shape + colour (ally square / enemy triangle / leader diamond like the minimap), HP pips, and group labels; overview stays a reading mode.
- **Labels:** nameplates, group labels, reinforcement markers and banners must not overlap each other or important props. Add simple deterministic overlap avoidance (stacking/offset/priority/declutter by zoom). Make the three reinforcement entry markers quieter (one grouped marker or a smaller style) while the warning stays clear.
- **Minimap:** verify icons are distinguishable at actual size and click-to-centre is reliable (a test for the transform already exists; extend if needed).
- **Tests:** actor-inside-safe-rect for follow/focus/enemy-action pans at each zoom step and near all four map edges; camera clamp tests still pass; overview marker scale; label overlap checker (no two label rects intersect in the scripted capture states); reinforcement marker count/style.
- Commit.

### W6. Measurements and evidence ("after")
- Re-run the auto-play with **road / flank / turtle** plus any new probe policies (e.g. a "rush the leader past reinforcements" bypass probe and a "scout flank + retreat" probe). Same seed; record everything W1 records.
- `godot-spike/docs/evidence/spike05/PACING.md`: a **before/after table** (W1 vs W6): idle unit-turns (by group), first contact turn, reinforcement first-engage turn, per-class damage/kill share, ally deaths per class, LOS-blocked shots, win/loss turn, battle-length estimate vs the 15–25 min target. Add a short class-balance note (ranged kill share after LOS, high-mobility contribution and survival) and honest caveats that auto-play is not a human.
- If flank or turtle still collapse by turn 3–7 because of AI rather than policy quality, say so; do **not** relax stats or objectives to fix it. Level-data position tweaks are allowed only if listed and both runs are kept.
- **Performance:** average and worst frame time at 720p during scrolling and during the enemy phase (normal and 2×) on this PC, measured not assumed, compared with spike-04 (19.7 / 22.8 ms). Flag any regression from the new AI or label avoidance.
- **Captures** at 1280×720 (plus one 1080p still) under `godot-spike/docs/evidence/spike05/`: enemy phase showing an advancing front, reinforcement interception, a LOS-blocked target + a cover preview, threat overlay with LOS, O overview with the new markers, a scrolled view near a map edge with no clipping, a dense-label scene, field melee hit with the spike05 profile, win/lose screen. PNG strips and 60 FPS AVIs of one enemy phase and one select → move → ranged-attack sequence. `MOVIE.md` explains ffmpeg missing → AVI + PNG strips (+ optional Pillow GIF under ~8 MB).
- Commit.

### W7. Verification and scope audit
- Headless import, then full GUT: **≥ 123 tests, all green**, with the new count and assertions. Save to `godot-spike/docs/evidence/spike05/test-run.log`.
- Skirmish/L03 regression: all three setups give identical rules results (HP, cells); timings ≤ 1.7 s for spike05-default / crit / Reduced Motion; a9_baseline, spike03 and spike04 profiles still reproduce their values.
- Add a **"spike-05"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- `git diff --stat 905c0ce..HEAD` must show changes only under `godot-spike/` and this brief. Confirm no changes to frame PNGs, `shared-anim/`, `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/` or (unless justified) `grid_rules.gd`. Record source hashes (`docs/evidence/spike05/source-hashes.json`) and a `README.md` index.
- Commit.

### W8. Handoff, then stop
Add a section **"spike-05"** to `godot-spike/docs/HANDOFF.md` (Traditional Chinese main text, like spike-04) covering:
- how to run (Field24x18, controls incl. any new keys, F1, Reduced Motion, profile switch `a9_baseline` / `spike03` / `spike04` / default);
- the enemy AI: states, triggers, focus order, leader/bodyguard rule, reinforcement pursuit; all values marked spike test values;
- the LOS/cover rule with diagrams or examples, and any terrain/position tweaks (cell list);
- the hit-feel table (spike-04 → spike-05) with strip links;
- camera/HUD changes (safe margins, overview markers, label avoidance, reinforcement marker);
- the before/after pacing and balance table, battle-length estimate vs 15–25 min, with honest auto-play caveats;
- performance numbers vs spike-04;
- PLACEHOLDER lists (terrain/props, unit stand-ins, A9 swing frames, SFX);
- **HUMAN_PENDING**: Gavin plays the field, ideally once each with road / flank / turtle (blind test per the GPT review), recording time, casualties, confusion points and why he won/lost; judges camera comfort, overview readability, label clarity and the toned hit feel;
- risks;
- **numbered open questions for Gavin**, each answerable in one line, **including the carried-over spike-04 questions**: objective (defeat leader vs hold point), move 4/3/6, edge scroll off, enemy phase speed default, whether reinforcements must engage, whether 24×18 passes and 32×24 may be considered later (still not authorised), plus any new ones (e.g. LOS block vs cover, high-mobility role);
- a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`;
- the commit table.

Make this the handoff commit, then **stop**.

## Acceptance
- W1 baseline JSON + table committed and reproducing spike-04.
- Enemy AI: active groups never idle without a logged role reason; idle unit-turns clearly down vs W1; reinforcements engage in the bypass probe; leader is defended; deterministic; tests green.
- Ranged LOS (+ cover if chosen) implemented in pure rules, reflected in overlay/preview/AI/policies, documented and tested.
- Default profile: flash clearly lower than spike-04 (≈ 0.6 and/or shorter), numbers another 10–15 % smaller; hitstop/shake/recoil/dust unchanged; spike04/spike03/a9_baseline selectable; strip + timing committed.
- No clipped actor in scrolled view at any zoom near any edge; readable overview markers; no overlapping labels in the capture states; quieter reinforcement markers.
- Before/after PACING table, class-balance note, performance vs spike-04, 720p captures + 60 FPS AVIs committed.
- 24×18 only; Skirmish/L03 rules, swing frames, frame timing, `shared-anim/`, `docs/art-briefs/`, `docs/proposals/`, `ui-prototype/` and `main` unchanged; `grid_rules.gd` unchanged unless justified; all attacks ≤ 1.7 s.
- GUT exits 0 with ≥ 123 tests (plus new AI/LOS/profile/camera/HUD tests); log committed.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. If something is ambiguous, choose the safest option inside this brief, record it in the handoff, and continue. Stop after the W8 handoff commit and wait for review.
