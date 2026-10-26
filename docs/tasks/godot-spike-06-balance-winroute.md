# Task Godot spike 06: balance + deployment, a winning route, reinforcements that matter, multi-seed testing, high-mobility role, flash 0.5 (24×18 field)

Authorized by Gavin on 2026-10-26 19:17 (Asia/Taipei), answering the spike-05 review question 「下一步怎麼做？」:
- 「開始 spike-06：先調平衡和佈陣、確定有路線打得贏、讓增援進場、多種子測試，閃白降到 0.5」 ("start spike-06: tune balance and deployment first, make sure there is a route that can win, make the reinforcements enter the fight, multi-seed testing, flash down to 0.5");
- 「高機動當繞側、攔截、收割殘血」 ("high-mobility units are flankers, interceptors and finishers of wounded enemies");
- 「其他問題先照預設值」 ("the other questions keep their defaults for now").

## Owner decisions
Unchanged:
- campaign-forge uses **Godot directly** (P010 on branch `decision/p010-godot`). React and Phase B are **CANCELLED**. `ui-prototype/` is read-only reference; do not edit P010 or other decision records.
- Thoma's **short one-handed flanged mace** is **APPROVED canon**.
- One consistent **dark-fantasy hand-painted** style. Do not adopt the on-hold Ferry Dusk palette.
- **A9 swing frames are development PLACEHOLDER.** No art work on them. **No new art** this segment.
- Big map is **Option C** (160 × 94.5 px diamond tiles, ≈ 96 px figures), **staged at 24×18**. **Do not build 32×24.** No fog of war.
- The 11×9 Skirmish/L03 stays the small tutorial map, untouched.

Answered defaults (Owner, 2026-10-26 19:17: "other questions keep their defaults"). Treat these as **decided for this segment**, not open:
1. win = **defeat the enemy leader**; lose = Thoma falls or turn > 15;
2. move **4 / 3 / 6** (melee / ranged / high-mobility) kept;
3. edge scroll **OFF** by default;
4. enemy phase **normal** speed by default (2× stays a toggle);
5. reinforcements **pursue/intercept**; do not change the objective to force engagement. If W3 finds that engagement cannot be made likely without a design lever (e.g. timing/entry point/leader position), use the smallest lever and document why;
6. 24×18 only; 32×24 still not authorised;
7. LOS rule kept (supercover; cliffs `^`, deep-water banks `~` and living units block; forest −1 cover, min 1; diagonal corner checks both sides).

New in this segment, in this priority order (GPT review of spike-05 + Owner):
1. **Balance + deployment so that at least one intended route wins reliably** with competent automated play, while weaker routes stay risky. Find the root cause of "all policies lose" first.
2. **Reinforcements that matter:** most winning runs must actually fight the reinforcement wave (still announced ≥ 1 turn ahead).
3. **Multi-seed testing** instead of the single seed 24018.
4. **High-mobility role = flank, intercept, finish off wounded (收割殘血)**, not top damage dealer; scouts should survive more than turn 4–5.
5. **Hit feel:** flash_mix **0.5**. Keep hitstop, directional shake, recoil, dust and current number sizes.
6. Visual/HUD polish **last** and only if cheap (threat overlay colour legend, overview label readability at 720p).
**Do not pad HP or stretch battles artificially to reach 15–25 minutes** (GPT review): more attrition is not more decisions.

This segment builds on spike-05 (`6ee5cb7`, GUT 147/147, 11,492 assertions).

## spike-05 findings that drive this segment
From `godot-spike/docs/evidence/spike05/PACING.md`, `PERFORMANCE.md` and HANDOFF "spike-05":
- New AI: activation radius 6 / group hit / chained alert ≤5 / all at turn 4; shared reverse-Dijkstra advance; regroup; leader with 2 bodyguards (radius 3, intercept ≤ 6); leader counter/step-back; reinforcements warn T4, arrive T5 at (23,4)/(23,5)/(23,6), rest on birth turn, then intercept.
- Results from the **original deployment, seed 24018**: road **lose T8** (was win T12 in spike-04), flank lose T7, turtle lose T6, scripted bypass lose T7, scout-retreat lose T9. **No winning policy.** Codex self-audit: level-design and winnability **FAIL**.
- True idle down a lot (road 68 % → 26 %), first contact still turn 2.
- Reinforcement wave **never** engaged in the three western fights (they end before it arrives).
- Road class shares after: melee 42.9 % dmg / 66.7 % kills, ranged 23.8 % / 16.7 %, high-mobility 33.3 % / 16.7 % but **both scouts die T4–5**; scout-retreat keeps them alive with 4.5 % damage and 0 kills.
- Estimates 9.3–21.8 min; enemy phase mean 3.456 s; 15–25 min **not established**.
- Perf 720p: scroll 20.7 / 30.6 ms, normal enemy 23.5 / 34.0 ms (mean / worst).
- The only RNG-like input is `level.seed`, used as a tiny tie-break term in `field_rules.gd` (~l.270, ~l.367). Damage is fixed (no hit/crit chance), so **seeds alone may barely change outcomes** (see W1).
- spike-05 default profile: flash_mix 0.6, hold 0, fade 60 ms, crit flash ×1.2 (field max .72), sparks 18 / spokes 6, numbers 21 / crit 26 px; hitstop 110/170/80 ms, shake 8/12 px, recoil 9 px, streak 22 px, bias .8, dust/zoom/knockback/SFX as spike-04.

GPT review of spike-05 (`git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-05.md`, CONDITIONAL ACCEPT; technical pass, gameplay not):
- AI pressure clearly better but maybe **too strong**; check the player's counter-play space before strengthening AI further.
- Reinforcements still bypassable in practice; the isolated pursuit test doesn't prove the level forces them into play.
- LOS direction is right; confirm across seeds.
- High-mobility: flank assault, pursuit of archers/retreating enemies, finishing wounded; needs survival/escape, not raw damage.
- Flash still slightly strong: flash_mix 0.5–0.55 or fade 45–50 ms. Keep hitstop/shake unchanged.
- Threat overlay needs a colour legend; O-overview labels small/crowded at 720p.
- Priorities: balance + winning route → reinforcement/objective design → multi-seed → class differentiation and battle length → visual polish last.

## Read first
- `godot-spike/docs/HANDOFF.md` ("spike-05" section, ~line 2687) and `godot-spike/docs/VERIFICATION.md` ("spike-05")
- `docs/tasks/godot-spike-05-ai-los-polish.md` (previous brief)
- `godot-spike/docs/evidence/spike05/PACING.md`, `PERFORMANCE.md`, `README.md`, `WORK.md`, `baseline/`, `autoplay/*.json`, `w2/`
- `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-05.md` (read-only)
- `godot-spike/scripts/rules/field_rules.gd`, `scripts/rules/field_sight.gd`, `data/levels/field_24x18.gd`, `scripts/levels/field_*.gd`, `scripts/impact/impact_profile.gd`, `config/*.tres`, `tools/autoplay_field.gd`, `tools/field_policy.gd`, `tools/capture_field05.gd`, `tools/capture_spike05.gd`, `tools/package_spike05_*.py`, `tools/audit_spike05.py`
- `godot-spike/tests/*`. Know which tests pin field data (deployment, roster, AI radii), profile values, camera and UI.
- `docs/SCOPE.md`, `docs/review/RESOURCE-CHECKLIST.md` (level-design, game-ai, game-ui-ux, game-feel, prototype-fast)

## Hard boundaries
- **Worktree:** work only in `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `6ee5cb7`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- **What you may change:** only `godot-spike/` (code, config, data, tests, tools, evidence, docs) and this segment's handoff/verification sections.
- **Protected paths:** nothing under `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/`, `shared-anim/` or `main` changes. No swing/idle/knight frame PNG changes. **No new art** (small marker/legend/label/HUD tweaks are fine).
- **Skirmish / L03 stays exactly as it is:** `grid_rules.gd`, the 11×9 map and its three setups, damage 2, HP, knockback cells, walkability, G005, the Skirmish HUD layout and the swing frame timing (180/70/40/80/100/150 ms, contact 3, anchor (455,196)). Only the shared impact profile value changes (W5). Do not edit `grid_rules.gd` unless strictly needed; if you must, justify it in the handoff and keep every Skirmish test byte-for-byte green.
- **Field rules** stay in `scripts/rules/field_rules.gd`, `field_sight.gd` and `data/levels/field_24x18.gd` (pure functions, inputs never mutated, results as events, deterministic, no global RNG). All numbers are **spike test values, not canon**; mark them so in data and docs.
- **Fixed this segment:** map size 24×18, objective type (defeat leader), turn limit 15, move 4/3/6, LOS rule, base damage per class. **Allowed balance levers** (W2–W4), each listed with before → after and reason: ally deployment cells, enemy count / group membership / placement, activation thresholds and timing, regroup/focus/bodyguard/leader parameters, reinforcement timing / entry cells / pursuit target, a small number of terrain cell edits (routes, chokepoints, retreat lanes), and a scout kit (W4). **Do not raise HP** on either side to lengthen battles; lowering enemy HP or count is allowed only if listed and justified. Keep every spike-05 data set reproducible (e.g. keep the spike-05 level data as a named variant so the W1 baseline can always be re-run).
- **Toolchain:** Godot 4.7.2 standard, **GDScript only** for the game. Python allowed for offline evidence tools (Pillow present). `PYTHON` = `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe` (full path; may not be on PATH in your sandbox). No C#, no GDExtension, no new addons beyond the vendored GUT. ffmpeg is **not** installed: PNG strips + `--write-movie` AVI (optional Pillow GIF). `rg` is not installed: use `Select-String` or `git grep`.
- **Attack timing:** normal attack strike-to-input-ready ≤ 1.7 s (hard), target ≤ 1.2 s, in Skirmish and the field. Reduced Motion ≤ normal.
- **Tests:** GUT must end with **≥ 147 tests, all green**. Earlier tests may only be re-pointed with a recorded reason (e.g. field-data tests pinned to the spike-05 deployment move to the `spike05` variant; profile-value tests move to `impact_profile_spike05.tres`), never deleted or weakened.

## Godot
`GODOT` = `C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`
- import: `GODOT --headless --path godot-spike --import`
- GUT: `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`
- field: `GODOT --path godot-spike res://scenes/levels/Field24x18.tscn`
- autoplay: `GODOT --headless --path godot-spike -s res://tools/autoplay_field.gd -- <flags>`
- movie: `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/<dir>/<name>.avi -s res://tools/<capture>.gd -- <flags>`
If the first command cannot find Godot or Python (PATH/sandbox), retry with the full path / escalation before giving up, and record it.

## Do
Work in order. **Commit after each W step** (`git -c user.name=Gavin0099 -c user.email=Gavin0099@users.noreply.github.com commit ...`).

### W1. Multi-seed baseline ("before")
- Extend `tools/autoplay_field.gd` (and `field_policy.gd`) into a **multi-seed harness** without changing game behaviour at the default seed: `--seeds=<list|range>`, `--policies=<list>`, `--variant=<level variant>`, writing one JSON per run plus an aggregate.
- Use a **fixed, committed seed list of ≥ 20 seeds** (include 24018). Because damage is fixed and the seed only breaks ties, **define and document what a seed varies**. At minimum: AI tie-breaks (existing `level.seed` term) **and** policy-side choices (seeded tie-breaks/ordering among equally good moves, e.g. which ally acts first, which equal target/cell). Optionally a separate, clearly labelled "deployment jitter" mode (±1 cell on legal cells). If ≥ 90 % of seeds give identical traces, say so and add the policy-side variation until results actually differ; record the distinctness count.
- Run **all policies** (road, flank, turtle, scout-retreat, and bypass as the scripted mid-battle probe, labelled as such) on the unchanged spike-05 data.
- Per run record the spike-05 metrics: win/loss + turn, first contact turn, **reinforcement first-engage turn** (either side attacks / enemy wave attacks, separately) or never, true idle by group (spike-05 definition), per-class damage/kill share, ally deaths per class + turn, LOS-blocked opportunities/shots, living-ally turns, battle-length estimate (`turns × (enemy-phase mean + living allies/turn × 15–25 s)`, using the spike-05 measured 3.456 s until W6 re-measures).
- Aggregate per policy: **win rate**, loss/win turn median + range, mean casualties, reinforcement engagement rate, idle share, class shares, length estimate range.
- Save under `godot-spike/docs/evidence/spike06/baseline/` (`runs/*.json`, `aggregate.json`, `BASELINE.md`). Confirm seed 24018 reproduces spike-05 (road lose 8, flank lose 7, turtle lose 6, scout-retreat lose 9); if not, explain why.
- Add tests: harness determinism (same seed → identical trace), seed list stable, default-seed behaviour unchanged.
- Commit.

### W2. Root cause, balance and deployment: one route that wins reliably
- First write a short **root-cause analysis** in `docs/evidence/spike06/WORK.md`: why do all policies lose (e.g. focus fire on Thoma, turn-4 global activation stacking groups, bodyguard intercept radius, scouts exposed at deployment, ally deployment geometry, policy weaknesses)? Separate "AI too strong / map unfair" from "auto-policy plays badly" with evidence (e.g. a stronger policy probe, a single-lever ablation table).
- Improve policies where they are just naive (e.g. road with flank support, focus fire, retreat wounded, protect Thoma) **before** nerfing the enemy. Name the intended winning route(s) explicitly (e.g. "road push with scouts screening the north flank").
- Then tune with the allowed levers (see Hard boundaries). Prefer, in order: ally deployment → enemy placement/group membership → activation timing/thresholds → bodyguard/leader parameters → enemy count → small terrain edits. **No HP padding, no move changes, no damage changes.**
- Targets over the W1 seed list (state the exact thresholds in WORK.md before tuning and keep them):
  - at least **one intended policy wins ≥ 60 %** of seeds, ideally ≥ 70 %;
  - a weaker/naive policy (e.g. turtle or a reckless rush) still loses most seeds — **not every approach should win**;
  - wins should not all end before turn 8 (aim for decisive turns ~9–14);
  - first contact may stay early, but enemy pressure must stay real (true idle must not climb back above ~35 % on the winning policy).
- Keep the spike-05 data as variant `spike05` (selectable via `--variant`) and put the tuned data in the default variant. Every changed value/cell gets a before → after → reason line in `WORK.md` and the handoff.
- Tests: tuned data loads, all walkability/reachability tests still pass (leader reachable, reinforcement entry reachable, no unit spawned on a blocked cell), AI determinism, inputs not mutated.
- Commit.

### W3. Reinforcements that matter (objective unchanged)
- Goal: in **most winning runs (target ≥ 70 % of winning seeds of the intended policy)** the reinforcement wave actually fights (enemy wave attacks at least once or is attacked), and bypassing it is not a free optimum.
- Levers: arrival turn (still **announced ≥ 1 turn ahead**, the warning stays visible), entry cells (closer to where the fight happens, still map-edge or a clearly signposted entry), pursuit target choice (e.g. head for the leader's attackers or Thoma), and leader position/behaviour. Do not change the defeat-leader objective, and do not add forced-engagement rules unless strictly needed; if needed, document why as an Owner question.
- Keep the bypass probe and report whether bypass is still possible and at what cost (casualties/turn).
- Tests: warning turn < arrival turn, warning visible in HUD state, wave engages in a fixture that mirrors the intended route, entry cells legal, deterministic.
- Commit.

### W4. High-mobility role: flank, intercept, finish off wounded
- Give the high-mobility class a small, explainable kit (spike test values), for example — choose and document:
  - **finisher:** bonus damage (e.g. +1) vs targets at ≤ 50 % HP, or a guaranteed kill-confirm on targets at 1–2 HP;
  - **flank:** bonus when attacking a target that is adjacent to another ally or from the target's rear/side relative to its last move;
  - **intercept / zone of control:** enemies entering a cell adjacent to a scout stop there or pay extra movement, letting scouts screen archers or block reinforcement lanes;
  - **escape:** e.g. move after attacking with remaining move (hit-and-run), or a free disengage, so scouts survive past turn 4–5.
- Constraint: high-mobility must **not** become the top damage class on the intended winning policy; it should lead or co-lead in **finishing kills / intercepts** and survive longer than in spike-05. Melee 4 / ranged 3 / mobile 6 moves unchanged; no HP increase.
- Reflect the kit in preview, hover and the V threat overlay where relevant (e.g. ZoC cells), in AI evaluation (enemies account for ZoC) and in auto-play policies (road/flank use scouts as flankers/interceptors/finishers; keep scout-retreat as a probe).
- Tests: each kit rule as pure-rule tests (bonus applies/does not apply, ZoC stop, hit-and-run move budget), inputs not mutated, Skirmish unaffected.
- Commit.

### W5. Hit feel: flash 0.5 (+ cheap HUD fixes)
- First save the current default **byte-for-byte** as `config/impact_profile_spike05.tres` and make `--impact-profile=spike05` select it (keep `a9_baseline`, `spike03`, `spike04`).
- Default: **flash_mix 0.5**; keep hold 0 and fade 60 ms (if 0.5 still reads as a white silhouette in the strip, you may also try fade 45–50 ms as an extra comparison but keep the default fade 60 ms and note it). Crit flash multiplier/max scaled consistently (state the new field max). Keep hitstop, directional shake, recoil, streak, bias, dust, zoom punch, knockback, SFX, sparks/spokes and number sizes (21 / 26 px) unchanged.
- Evidence (`docs/evidence/spike06/hitfeel/`): spike05 vs spike06 normal and crit contact stills, one stacked strip `impact-strip-spike05-vs-spike06.png` (contact ±8 frames, same layout as spike-05), AVIs, `timing.json` (normal/crit/Reduced Motion × 3 Skirmish setups), one field hit still.
- Tests: re-point spike-05 profile-value tests to `impact_profile_spike05.tres` (recorded reason); default flash 0.5; everything else equal to spike05; all five profiles load and select.
- **Only if cheap**: a small colour legend for the V threat overlay (what each colour means: move, attack, LOS-blocked, cover, ZoC), and larger/declutted O-overview labels at 720p. No new art.
- Commit.

### W6. Measurements and evidence ("after")
- Re-run the **same seed list** and all policies on the tuned default; also re-run the `spike05` variant to show the harness still reproduces W1.
- `docs/evidence/spike06/PACING.md`: **before/after table (W1 vs W6) per policy**: win rate, win/loss turn median+range, casualties per class, reinforcement engagement rate and first-engage turn, true idle share by group, per-class damage/kill share (plus finishing kills / intercepts for high-mobility), LOS-blocked shots, battle-length estimate vs the 15–25 min target. Re-measure the enemy-phase mean on the tuned data and use it.
- State clearly whether the targets were met: ≥ 1 intended policy ≥ 60 % win rate; its battle-length estimate inside 15–25 min (or how far off, honestly — do not pad); reinforcements engaged in ≥ 70 % of its wins; high-mobility not top damage, survives longer. If a target is missed, say so; don't relax the definition.
- Class role note: melee / ranged / high-mobility contribution and survival, LOS effect across seeds.
- Performance: average and worst frame time at 720p during scrolling and the enemy phase (normal and 2×), measured on this PC, compared with spike-05 (20.7 / 23.5 ms means).
- Captures at 1280×720 (plus one 1080p still) under `docs/evidence/spike06/`: tuned deployment, intended route mid-battle, reinforcement wave engaging, scout flank/finisher hit, ZoC/intercept preview, threat overlay with legend (if done), O overview, win screen from a real continuous auto-play run (not a staged fixture), lose screen. PNG strips and 60 FPS AVIs of one enemy phase with the wave engaging and one scout flank → finish → retreat sequence. `MOVIE.md` explains ffmpeg missing → AVI + PNG strips.
- Commit.

### W7. Verification and scope audit
- Headless import, then full GUT: **≥ 147 tests, all green**, with the new count and assertions. Save to `docs/evidence/spike06/test-run.log`.
- Skirmish/L03 regression: all three setups give identical rules results (HP, cells); timings ≤ 1.7 s for default / crit / Reduced Motion; a9_baseline, spike03, spike04, spike05 profiles still reproduce their values.
- Add a **"spike-06"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- `git diff --stat 6ee5cb7..HEAD` must show changes only under `godot-spike/` and this brief. Confirm no changes to frame PNGs, `shared-anim/`, `ui-prototype/`, `docs/art-briefs/`, `docs/proposals/` or (unless justified) `grid_rules.gd`. Record `docs/evidence/spike06/source-hashes.json` and a `README.md` index.
- Commit.

### W8. Handoff, then stop
Add a section **"spike-06"** to `godot-spike/docs/HANDOFF.md` (Traditional Chinese main text, like spike-05) covering:
- how to run (Field24x18, controls incl. any new keys/legend, F1, Reduced Motion, profile switch `a9_baseline` / `spike03` / `spike04` / `spike05` / default, level variant `spike05` vs default, the multi-seed harness command);
- root cause of spike-05's all-lose result, and the list of every balance/deployment/terrain/AI change (before → after → reason), all marked spike test values;
- the intended winning route(s) in plain words, and why the weaker routes stay risky;
- reinforcement design: when/where they warn and arrive, how they pursue, engagement rate, whether bypass is still possible and at what cost;
- the high-mobility kit and its measured role (finishing kills, intercepts, survival);
- the hit-feel table (spike-05 → spike-06) with strip links;
- the multi-seed before/after table, battle-length estimate vs 15–25 min, honest auto-play caveats;
- performance vs spike-05;
- PLACEHOLDER lists (terrain/props, unit stand-ins, A9 swing frames, SFX);
- **HUMAN_PENDING**: Gavin blind-plays the tuned field once each with **road / flank / turtle** (without reading the intended-route section first), recording real minutes, casualties, confusion points, why he won/lost, and whether the scouts' role and the reinforcements were understandable; judges the 0.5 flash and the threat legend;
- risks;
- **numbered open questions for Gavin**, each answerable in one line (e.g. difficulty target / win-rate goal, the scout kit choice, whether forced engagement is ever wanted, whether 24×18 passes and 32×24 may be considered later — still not authorised); do **not** re-ask the questions he already answered with defaults unless the data now argues against a default;
- a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`;
- the commit table.

Make this the handoff commit, then **stop**.

## Acceptance
- W1 multi-seed harness (≥ 20 fixed seeds, documented variation sources, distinctness count) + baseline committed; seed 24018 reproduces spike-05.
- Root cause written; every tuning change listed with reason; no HP padding; moves 4/3/6, damage, objective, turn limit and LOS rule unchanged; `spike05` variant still runnable.
- At least one intended policy wins ≥ 60 % of seeds (or an honest FAIL with evidence of why); at least one naive policy still mostly loses.
- Reinforcements engage in ≥ 70 % of the intended policy's wins (or honest FAIL); still announced ≥ 1 turn ahead; bypass cost documented.
- High-mobility kit implemented in pure rules, previews, AI and policies; scouts survive longer and lead finishing kills/intercepts without being the top damage class; tested.
- Default flash_mix 0.5; spike05/spike04/spike03/a9_baseline selectable; strip + timing committed; hitstop/shake/recoil/dust unchanged.
- Before/after multi-seed PACING table, class-role note, performance vs spike-05, 720p captures + 60 FPS AVIs, a real continuous win capture committed.
- 24×18 only; Skirmish/L03 rules, swing frames, frame timing, `shared-anim/`, `docs/art-briefs/`, `docs/proposals/`, `ui-prototype/` and `main` unchanged; `grid_rules.gd` unchanged unless justified; all attacks ≤ 1.7 s.
- GUT exits 0 with ≥ 147 tests (plus new harness/balance/reinforcement/scout/profile tests); log committed.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. If something is ambiguous, choose the safest option inside this brief, record it in the handoff, and continue. Stop after the W8 handoff commit and wait for review.
