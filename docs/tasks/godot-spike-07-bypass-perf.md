# Task Godot spike 07: close the T6 wave-bypass, fix the frame-time regression, scout early survival, ≥40-seed testing (24×18 field)

Authorized by Gavin on 2026-10-27 09:54 (Asia/Taipei), answering the spike-06 review question 「Spike-06 之後怎麼走」:
- 「開始 spike-07：先修第 6 回合繞過增援的漏洞、查每幀 34 ms 的退步」 ("start spike-07: first fix the turn-6 reinforcement-bypass hole and investigate the 34 ms per-frame regression");
- 「難度就用現在這樣」 ("keep the difficulty as it is now": flank ≈14/20 winnable, naive policies mostly lose);
- 「偵察兵能力保留，照 GPT 改善早期站位和後撤」 ("keep the scout kit; improve early positioning and retreat as GPT suggests");
- 「閃白 0.5 和 V/O 先接受」 ("flash 0.5 and the V legend / O labels are accepted").

## Owner decisions
Unchanged:
- campaign-forge uses **Godot directly** (P010 on branch `decision/p010-godot`). React and Phase B are **CANCELLED**. `ui-prototype/` is read-only reference; do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**.
- One consistent **dark-fantasy hand-painted** style. Do not adopt the on-hold Ferry Dusk palette.
- **A9 swing frames are development PLACEHOLDER.** No art work on them. **No new art** this segment.
- Big map is **Option C** (160 × 94.5 px diamond tiles, ≈ 96 px figures), **staged at 24×18**. **Do not build 32×24.** No fog of war.
- The 11×9 Skirmish/L03 stays the small tutorial map, untouched.
- Win = **defeat the enemy leader**; lose = Thoma falls or turn > 15. Move **4 / 3 / 6** (melee / ranged / high-mobility). Edge scroll OFF. Enemy phase normal speed by default (2× toggle). LOS rule kept (supercover; cliffs `^`, deep-water banks `~` and living units block; forest −1 cover, min 1; diagonal corner checks both sides). Base damage per class and attack ranges unchanged.
- **Scout kit is kept** as in spike-06: +1 damage vs targets at ≤ 50 % HP; enemies entering a cell adjacent to a scout stop (may still attack); after attacking, retreat up to 2 movement cost.
- **Difficulty baseline = spike-06 default** (flank ≈ 70 % / road ≈ 50 % on the 20-seed list; turtle and scout-retreat 0 %). Do not make the field easier or harder beyond what the bypass fix strictly requires.
- **Hit feel is frozen:** flash_mix 0.5 (and the rest of the spike-06 default profile), V six-colour threat legend and O-overview labels are **accepted**. Do not change any impact-profile value, hitstop, shake, recoil, dust, numbers, legend colours or overview labels (a perf fix may change *how* they are drawn only if the pixels/timings stay equivalent; prove it).

New in this segment, in this priority order (GPT review of spike-06 + Owner):
1. **P0 — close the T6 wave-bypass.** Seeds **1014 / 1015 / 1017** of the scripted bypass probe win on **turn 6 with zero deaths without ever touching the reinforcement wave**. Bypassing the wave must no longer be a free optimum. Allowed design levers (choose the **minimal** one, justify it with an ablation, keep the **defeat-leader** win): leader reachability/position/behaviour (e.g. leader steps back toward the wave once the wave is announced, bodyguard/guard-post changes), wave timing/entry/pursuit relative to the leader, a small terrain edit around the leader, or a win-condition refinement that still reads as "defeat the leader" (e.g. the leader only becomes attackable/exposed after X — only if the smaller levers fail; record as an Owner question if used). No HP padding, no damage changes, no move changes.
2. **P0 — profile and fix the frame-time regression.** Native 720p on this PC (AMD Radeon 780M, GL Compatibility): scroll **20.7 / 30.6 → 34.0 / 46.4 ms** (mean / worst, spike-05 → spike-06), enemy-phase normal **23.5 / 34.0 → 34.1 / 47.0 ms**, 2× **23.1 / 29.6 → 34.6 / 45.6 ms**. Budget **16.67 ms** (60 FPS). Find the **measured** cause (not a guess), fix it, and show before/after under identical workloads.
3. **P1 — scout early survival** (GPT): scouts still sometimes die on turn 3. Improve exposure scoring, early positioning, retreat-cell choice (AI/policy side) and, if needed, ally deployment — **not** more damage, HP or move.
4. **P1 — expand multi-seed testing to ≥ 40 seeds**, stratified by policy and outcome; report distinct traces and state clearly that distinct traces are not independent samples.
5. Keep everything else stable. **Do not pad HP or stretch battles artificially.**

This segment builds on spike-06 (`1cff2db`, GUT 165/165).

## spike-06 findings that drive this segment
From `godot-spike/docs/evidence/spike06/PACING.md`, `PERFORMANCE.md`, `WORK.md` and HANDOFF "spike-06" (~line 2960):
- Tuned default: initial enemies cut 11 knights + leader → 5 knights + leader; wave of 3 enters from the east ford near the leader; global push delayed T4 → T6; ally deployment tweaked; alert 6 / chain 5 / support 3 / bodyguard 3 / intercept 6, leader contest 2 / counter.
- 20 seeds: flank 0 % → **70 %** (win T13 median), road 0 % → **50 %**, turtle and scout-retreat 0 %. Wave engaged in 100 % of wins. Distinct traces: road 20/20, flank 20/20, turtle 12/20, scout-retreat 14/20, scripted bypass 10/20.
- Scripted bypass probe (pre-placed east at T5, **not** a full route): 20/20 wins, T7 [6–9]; seeds **1014 / 1015 / 1017 win T6 with zero deaths and never touch the wave**. Codex's own note: 「繞過仍可能，免費繞後反例未消除」. W7 must also check whether a **full-battle** policy from the real deployment can reproduce the bypass (a "dash for the leader" policy), not only the scripted probe.
- Scout after: 25.1 % damage, 40.9 % kills, 61 finishing kills, 87 intercepts, death turn median 8 [3–14] — **still dies T3 in some seeds**.
- Enemy phase mean 3.456 s → 1.476 s. Battle-length estimate 0/20 fully inside 15–25 min (flank ≈ 17.2–28.4 min); human minutes pending — **do not tune toward the estimate** this segment.
- Performance table above. spike-06's PERFORMANCE.md itself notes workloads differ (spike-05 sampled T2, spike-06 sampled the wave state) — so part of the delta may be workload, not code. W4 must separate the two.

GPT review of spike-06 (`git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-06.md`, CONDITIONAL ACCEPT): P0 close the bypass (win condition, leader reachability, wave involvement); P0 profile 23 → 34 ms; P1 ≥ more seeds stratified by deployment/policy/outcome; P1 scout T3 deaths: exposure + retreat path choice, not more output; P2 real pacing/hit-feel check (human, not this segment).

## Read first
- `godot-spike/docs/HANDOFF.md` ("spike-06" section) and `godot-spike/docs/VERIFICATION.md` ("spike-06")
- `docs/tasks/godot-spike-06-balance-winroute.md` (previous brief)
- `godot-spike/docs/evidence/spike06/PACING.md`, `PERFORMANCE.md`, `performance.json`, `WORK.md`, `README.md`, `baseline/`, `after/`, `w3-bypass/`, `targets.json`, `metrics-summary.json`
- `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-06.md` (read-only)
- `godot-spike/scripts/rules/field_rules.gd`, `field_sight.gd`, `data/levels/field_24x18.gd`, `field_24x18_spike05.gd`, `scripts/levels/field_*.gd`, `tools/autoplay_field.gd`, `tools/field_harness.gd`, `tools/field_policy.gd`, `tools/field_policy_spike05.gd`, `tools/probe_balance06.gd`, `tools/capture_field06.gd`, `tools/capture_spike06.gd`, `tools/package_spike06_*.py`, `tools/summarize_spike06.py`, `tools/audit_spike06.py`
- `godot-spike/tests/*`. Know which tests pin field data, the scout kit, profile values, camera and UI.
- `docs/SCOPE.md`, `docs/review/RESOURCE-CHECKLIST.md` (level-design, game-ai, game-ui-ux, game-feel, performance, prototype-fast)

## Hard boundaries
- **Worktree:** work only in `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `1cff2db`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- **What you may change:** only `godot-spike/` (code, config, data, tests, tools, evidence, docs) and this segment's handoff/verification sections.
- **Protected paths:** nothing under `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/`, `shared-anim/` or `main` changes. No swing/idle/knight frame PNG changes. **No new art.**
- **Skirmish / L03 stays exactly as it is:** `grid_rules.gd`, the 11×9 map and its three setups, damage 2, HP, knockback cells, walkability, G005, the Skirmish HUD layout and the swing frame timing (180/70/40/80/100/150 ms, contact 3, anchor (455,196)). Do not edit `grid_rules.gd` unless strictly needed; if you must, justify it in the handoff and keep every Skirmish test byte-for-byte green.
- **Impact profiles frozen:** `config/*.tres` impact profiles (default = spike-06, flash_mix 0.5; `spike05`, `spike04`, `spike03`, `a9_baseline`) keep their values byte-for-byte.
- **Field rules** stay in `scripts/rules/field_rules.gd`, `field_sight.gd` and `data/levels/field_24x18.gd` (pure functions, inputs never mutated, results as events, deterministic, no global RNG). All numbers are **spike test values, not canon**; mark them so in data and docs.
- **Fixed this segment:** map size 24×18, objective type (defeat leader), turn limit 15, move 4/3/6, LOS rule, ranges, base damage per class, HP, scout kit rules. **Allowed levers** for W2/W3, each listed with before → after → reason: leader position/behaviour/guard parameters, wave timing (still **announced ≥ 1 turn ahead**) / entry cells / pursuit target, a small number of terrain cell edits, ally deployment cells, AI exposure/retreat scoring, auto-policy logic. Keep the **spike-06 default data reproducible as a named variant `spike06`** (and keep `spike05`), selectable via `--variant`.
- **Toolchain:** Godot 4.7.2 standard, **GDScript only** for the game. Python allowed for offline evidence tools (Pillow present). `PYTHON` = `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe` (full path; may not be on PATH in your sandbox). No C#, no GDExtension, no new addons beyond the vendored GUT. ffmpeg is **not** installed: PNG strips + `--write-movie` AVI. `rg` is not installed: use `Select-String` or `git grep`.
- **Attack timing:** normal attack strike-to-input-ready ≤ 1.7 s (hard), target ≤ 1.2 s, in Skirmish and the field. Reduced Motion ≤ normal.
- **Tests:** GUT must end with **≥ 165 tests, all green**. Earlier tests may only be re-pointed with a recorded reason (e.g. field-data tests pinned to the spike-06 data move to the `spike06` variant), never deleted or weakened.

## Godot
`GODOT` = `C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`
- import: `GODOT --headless --path godot-spike --import`
- GUT: `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`
- field: `GODOT --path godot-spike res://scenes/levels/Field24x18.tscn`
- autoplay: `GODOT --headless --path godot-spike -s res://tools/autoplay_field.gd -- <flags>`
- movie: `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/<dir>/<name>.avi -s res://tools/<capture>.gd -- <flags>`
- profiling: Godot's built-in `Performance` monitors (`TIME_PROCESS`, `TIME_PHYSICS_PROCESS`, `RENDER_TOTAL_DRAW_CALLS_IN_FRAME`, `RENDER_TOTAL_OBJECTS_IN_FRAME`, `OBJECT_NODE_COUNT`, etc.), `Time.get_ticks_usec()` scoped timers, and `--print-fps`; a headless run cannot measure rendering, so render timings must come from a windowed native 720p run.
If the first command cannot find Godot or Python (PATH/sandbox), retry with the full path / escalation before giving up, and record it.

## Do
Work in order. **Commit after each W step** (`git -c user.name=Gavin0099 -c user.email=Gavin0099@users.noreply.github.com commit ...`).

### W1. ≥ 40-seed baseline on spike-06 data ("before")
- Freeze the current default data as variant `spike06` (byte-equivalent behaviour) and keep `spike05`.
- Extend the committed seed list to **≥ 40 fixed seeds** (keep the 20 spike-06 seeds incl. 24018, 1014, 1015, 1017; add ≥ 20 new). Keep the spike-06 definition of what a seed varies (AI tie-breaks + policy-side ordering); do not change it silently.
- Add a **full-battle "leader-dash" policy** that starts from the real deployment and tries to reach and kill the leader as fast as possible while avoiding the wave (this is the realistic version of the bypass; keep the scripted T5 bypass probe too, clearly labelled as a partial-start probe).
- Run all policies (road, flank, turtle, scout-retreat, leader-dash, scripted bypass probe) on `spike06`. Per run, keep the spike-06 metrics and add: `bypass_win` flag (= win with zero wave engagement by either side), win turn, deaths per class, scout death turn and cause (who killed it, from where, how exposed it was at the start of that enemy phase).
- Aggregate **stratified by policy × outcome** (win / loss-Thoma / loss-timeout; bypass-win vs engaged-win): counts, rates with a simple 95 % interval (e.g. Wilson), median/range turns, casualties, wave engagement, scout death turns. Report **distinct traces per policy** and state that distinct traces ≠ independent samples.
- Confirm the original 20 seeds reproduce spike-06 numbers (flank 14/20, road 10/20, bypass seeds 1014/1015/1017 T6 zero-death); if not, explain why.
- Save under `godot-spike/docs/evidence/spike07/baseline/` (`runs/*.json`, `aggregate.json`, `BASELINE.md`).
- Tests: seed list stable (≥ 40, contains the spike-06 20), `spike06` variant reproduces spike-06 data, leader-dash policy deterministic per seed.
- Commit.

### W2. Close the T6 wave-bypass (minimal design change)
- In `docs/evidence/spike07/WORK.md` first write: **why** the bypass works (trace analysis of 1014/1015/1017 and any leader-dash bypass wins: where the leader is, which cells/turns, why the wave never contacts, which bodyguard/guard rules fail), and **state the target before tuning**: on the W1 seed list, `bypass_win` rate = **0 %** for leader-dash and for any full-battle policy, and the scripted probe no longer produces zero-death T6 wave-free wins (or, if a cheap bypass remains, it costs clearly more than the intended route — define the cost metric, e.g. deaths and turn — and say so honestly).
- Try levers in order of smallness, with a **single-lever ablation table** (each lever alone on the full seed list, plus the chosen combination): (a) leader behaviour/position — e.g. once the wave is announced the leader falls back toward the wave entry, or the leader's guard post sits where the wave arrives; (b) wave timing/entry/pursuit relative to the leader; (c) a small terrain edit around the leader's approach; (d) only if a–c fail: a win-condition refinement that still reads as "defeat the leader" (document as an Owner question in the handoff).
- **Keep the difficulty band:** after the fix, flank and road win rates on the ≥ 40-seed list must stay within roughly ±10 percentage points of their W1 values (state exact W1 numbers and the band before tuning); turtle and scout-retreat must still mostly lose; wins should keep engaging the wave. If the fix pushes win rates outside the band, re-balance only with the allowed levers and report it.
- Every changed value/cell: before → after → reason in WORK.md and the handoff. Warning still ≥ 1 turn ahead and visible.
- Tests: bypass fixture (e.g. seed 1014 scripted probe and a leader-dash run) no longer yields a wave-free zero-death win; leader reachable; wave entry legal and reachable; warning turn < arrival turn; determinism; inputs not mutated.
- Commit.

### W3. Scout early survival (no more damage)
- Analyse the W1/W2 scout deaths before T5: exposure at the start of the enemy phase (how many enemies could reach/attack it), whether the retreat budget was used and where it went, deployment cell, policy choice.
- Fix with, in order: auto-policy positioning (don't end the turn in ≥ N enemy threat cells early, prefer retreat cells out of reach/behind allies or LOS blockers), retreat-cell choice in the hit-and-run budget, a ZoC-aware screening position, then ally deployment of the scouts. The kit's rules and numbers stay unchanged. Show the AI side too if enemy focus logic is the cause (document; do not make the AI dumber than spike-06 just to save the scout).
- Target (state before tuning): no scout death before T4 in ≥ 90 % of intended-route runs, scout death-turn median not lower than spike-06's 8, scouts still lead or co-lead finishing kills/intercepts and are **not** the top damage class.
- Tests: exposure/retreat scoring pure tests (prefers safe cell, respects the 2-cost budget), deployment legal, determinism.
- Commit.

### W4. Profile the frame-time regression (measure first)
- Build a repeatable **native 720p windowed** perf harness (no movie writing, no readbacks, no concurrent Godot) with **identical workloads** for both builds: (1) scroll path across the full field at T2, (2) scroll at the wave state, (3) one normal and one 2× enemy phase at the same reached state. Run each ≥ 3 times; report mean / p95 / worst ms.
- Measure **`spike05` code+data at 6ee5cb7 vs spike-06 at 1cff2db** (e.g. via a temporary `git worktree` *outside* this repo's tracked files, removed afterwards; never stash, never touch other worktrees) on the same workloads to separate **code regression vs workload difference**.
- Break the frame down: process vs render time, draw calls, object/node counts, per-system scoped timers (threat/V overlay recompute, ZoC/LOS previews, scout retreat preview, HUD/labels, overview markers, legend, AI evaluation per frame vs per action, pathfinding, `_draw()`/queue_redraw frequency). Identify the **measured** top cause(s) with numbers.
- Save to `docs/evidence/spike07/perf/` (`profile-before.json`, notes) and the "Cause" section of `PERFORMANCE.md`.
- Commit (measurement only, no fixes yet — unless a fix is a one-line obvious bug, still measured).

### W5. Fix the regression
- Fix the measured causes (e.g. cache and recompute overlays/previews only on state change, avoid per-frame Dijkstra/LOS, batch draws, reduce redundant nodes/labels, throttle HUD updates). **No visual change**: impact profile, legend colours, overview labels, figure sizes and the map must look the same — prove with same-frame before/after stills (pixel diff or side-by-side) for deployment, V overlay and O overview.
- Targets: scroll and enemy phase mean **≤ spike-05 values (20.7 / 23.5 ms)** at minimum; aim for **≤ 16.67 ms** mean with worst < 33 ms. If 16.67 ms is not reachable without art/renderer changes, say exactly what remains (e.g. GPU fill on 780M, GL Compatibility) with the numbers — do not claim 60 FPS without data.
- `docs/evidence/spike07/PERFORMANCE.md`: **cause → fix → before/after** table under identical workloads (spike-05 / spike-06 / spike-07), plus attack-timing re-check (all ≤ 1.7 s).
- Tests: cache invalidation correctness (overlay/preview equals a fresh recompute after moves/attacks/turn change), rules results unchanged, Skirmish unaffected.
- Commit.

### W6. Measurements and evidence ("after")
- Re-run the **same ≥ 40 seeds** and all policies on the new default; re-run `spike06` (and spot-check `spike05` 24018) to show the harness still reproduces W1.
- `docs/evidence/spike07/PACING.md`: **before/after table (W1 vs W6) stratified by policy × outcome**: win rate with interval, win/loss turn median+range, `bypass_win` rate, wave engagement rate and first-engage turn, casualties per class, scout death turn (median, share dying before T4), per-class damage/kill share, finishing kills / intercepts, true idle share, distinct traces (+ the "not independent samples" note). Battle-length estimate: report it but do **not** tune toward it; human minutes pending.
- State clearly whether each target was met: bypass closed; flank/road inside the ±10 pp band; naive policies still mostly lose; scout early-death target; frame-time targets. If a target is missed, say so; don't relax the definition.
- Captures at 1280×720 (plus one 1080p still) under `docs/evidence/spike07/`: the leader/wave situation that used to allow the bypass (before vs after, same seed/turn), the bypass probe's new outcome, a scout retreat to a safe cell, a real continuous auto-play win from the real deployment (not a staged fixture), a lose screen, V overlay and O overview after the perf fix. PNG strips and 60 FPS AVIs of one enemy phase where the leader/wave respond to an attempted dash. `MOVIE.md` explains ffmpeg missing → AVI + PNG strips.
- Commit.

### W7. Verification and scope audit
- Headless import, then full GUT: **≥ 165 tests, all green**, with the new count and assertions. Save to `docs/evidence/spike07/test-run.log`.
- Skirmish/L03 regression: all three setups give identical rules results; timings ≤ 1.7 s for default / crit / Reduced Motion; all five impact profiles still reproduce their values byte-for-byte.
- Add a **"spike-07"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- `git diff --stat 1cff2db..HEAD` must show changes only under `godot-spike/` and this brief. Confirm no changes to frame PNGs, impact-profile `.tres`, `shared-anim/`, `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/` or (unless justified) `grid_rules.gd`. Record `docs/evidence/spike07/source-hashes.json` and a `README.md` index.
- Commit.

### W8. Handoff, then stop
Add a section **"spike-07"** to `godot-spike/docs/HANDOFF.md` (Traditional Chinese main text, like spike-06). Start it with a short subsection **「先給盲玩者」** (how to launch, controls incl. V/O/F1/2×, what wins and loses — **without** revealing the intended route or the bypass analysis), then:
- how to run (Field24x18, profile and level variants `spike05` / `spike06` / default, the ≥ 40-seed harness command, the perf harness command);
- the bypass: root cause, the ablation table, the chosen minimal change (before → after → reason), whether any bypass remains and at what cost;
- scout early survival: cause of T3 deaths, what changed, measured result;
- performance: measured cause(s), fixes, spike-05 / spike-06 / spike-07 table, what still stands between this and 60 FPS on the 780M;
- the ≥ 40-seed before/after table stratified by policy × outcome, distinct traces, Wilson intervals, honest auto-play caveats;
- PLACEHOLDER lists (terrain/props, unit stand-ins, A9 swing frames, SFX);
- **HUMAN_PENDING**: Gavin blind-plays road / flank / turtle once each (reading only 「先給盲玩者」 first), recording real minutes, casualties, confusion points, why he won/lost, whether the leader/wave behaviour reads as fair, and frame smoothness when scrolling;
- risks;
- **numbered open questions for Gavin**, each answerable in one line; do **not** re-ask already-answered questions (difficulty, scout kit, flash 0.5, V/O, defaults) unless the data now argues against them;
- a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`;
- the commit table.

Make this the handoff commit, then **stop**.

## Acceptance
- ≥ 40-seed harness with leader-dash policy + `spike06` variant; original 20 seeds reproduce spike-06; stratified baseline committed.
- Bypass root cause and ablation written; chosen change is minimal and justified; defeat-leader win kept; `bypass_win` = 0 % for full-battle policies and the scripted probe no longer wins wave-free at zero deaths on T6 (or an honest FAIL with evidence); warning ≥ 1 turn ahead.
- Flank/road win rates within ≈ ±10 pp of W1; naive policies still mostly lose; no HP padding; move 4/3/6, damage, ranges, objective, turn limit, LOS rule and scout kit rules unchanged.
- Scout early-death target met (or honest FAIL); scouts not top damage; still lead finishing/intercepts.
- Frame-time cause measured under identical workloads; fix committed; before/after table; mean ≤ spike-05 values at minimum, 16.67 ms target reported honestly; no visual change proven.
- Hit feel / impact profiles / V legend / O labels unchanged.
- 24×18 only; Skirmish/L03, swing frames, frame timing, `shared-anim/`, `docs/art-briefs/`, `docs/proposals/`, `ui-prototype/` and `main` unchanged; `grid_rules.gd` unchanged unless justified; all attacks ≤ 1.7 s.
- GUT exits 0 with ≥ 165 tests (plus new seed/bypass/scout/perf-cache tests); log committed.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. If something is ambiguous, choose the safest option inside this brief, record it in the handoff, and continue. Stop after the W8 handoff commit and wait for review.
