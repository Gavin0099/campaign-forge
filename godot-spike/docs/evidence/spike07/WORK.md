# spike-07 work ledger

Owner authority: 2026-10-27 09:54 Asia/Taipei; brief fc85094 on top of
1cff2db, clean codex/godot-spike worktree. Only godot-spike/ writes, local
W1–W8 commits, no push/merge/PR/stash. No new agent, art, story or shared-file edit.
All combat values remain spike test values, not canon.

## W1 — freeze and baseline

Keep criterion: original 100 runs reproduce, >=40 fixed seeds and full-route
leader-dash reveal bypasses without changing the seeded variation definition.
Snapshot spike06 data and operator; spike05 retained. Only telemetry gains
phase-start potential threat counts, attacker/source/death cells and spent/left
retreat budgets. Potential exposure is a legal reach/attack upper bound, not a
prediction that every enemy will select that scout. Existing register's boolean
could_attack loop now short-circuits on true; no state/event changes.

40 seeds = original 24018,1001–1019 plus 1020–1039. No deployment jitter or random
damage. Same AI coordinate ties and within-class policy ordering. Leader-dash
starts at real deployment and prioritizes leader attack slots while penalizing
wave threat; bypass remains explicitly SCRIPTED T5 partial start.

Original 100 trace hashes, commands, outcomes, archetypes, unit-turns and wave
engagement reproduce exactly (original20-reproduction.json). Flank14/20,
road10/20; 1014/1015/1017 retain T6 zero-death wave-free scripted wins.
New40: road50%, flank62.5%, turtle12.5%, retreat0%, leader-dash85% with33/40
wave-free wins. Flank also has1 full-route bypass win. See baseline/aggregate.json
for all policy×outcome strata, Wilson intervals, casualty/death spans and traces.
Distinct traces are not independent samples or a human difficulty estimate.

Commands: headless import exit0; test_spike07.gd3/3,8assertions exit0;
six-policy sweep partitioned into disjoint headless routes/naive/dash runs,
each exit0; summarize_spike07.py and check_spike07_baseline.py exit0.
Original unpartitioned sweep was interrupted to short-circuit telemetry and
split independent work. One half-written flank1015 JSON caused resume parse
failure; resume now validates/recomputes incomplete files. Failed/interrupted
logs retained under attempts; final240 outputs validated. No timings from
concurrent headless runs are treated as native performance evidence.

Historical seed assertion now pins SPIKE06_SEEDS; new test pins40 unique seeds
and first20 order, snapshot equality and deterministic real-deployment dash.
No earlier assertion removed or weakened.

Tool boundary: supplied absolute Godot/Python paths initially unavailable inside
sandbox; escalated commands succeeded (Godot4.7.2 ed1daf0bf, Python3.12.10).
Process listing showed only this CLI explicitly targeting this worktree and no
Godot before start; desktop app worktree association cannot be independently
proved from process command lines. No global trust/config changes. Existing
offline Python tools do not launch subprocess/network; ambient DLL/environment
trust is not fully audited and no comprehensive trust-root claim is made.
Resource methods read from fixed awesome-gamedev-agent-skills0a70cfc: prototype-fast,
level-design, game-ai, game-ui-ux, game-feel; no install/copy or new dependency.

## W2 — root cause and targets BEFORE tuning

Trace1014/1015/1017 scripted: leader starts(20,9); allies already atx16–18 onT5.
Wave arrivesx23,y8–10 and restsT5. Leader's adjacent counter/one-cell step-back
keeps it near(20,9), while reserve knight8 only protects radius3 and attacks one
target, not a wall. Melee/scout knockback repeatedly separates leader from its
escort. Allied T6 strikes resolve before wave's first eligible enemy phase.
Leader-dash1014 is a realistic counterexample: scout hitsT4 push leader(20,9)
→(20,10)→(21,10), T5 guard/scout push(21,9)→(21,8), Thoma killsT6 before any
wave contact. It costs4 deaths, but is still85% successful overall, much faster
than intendedT13 routes. Original no-wave fixture is zero-cost, so cannot dismiss.

Locked targets on the SAME40 seeds: all full-route policies bypass_win0%; scripted
probe has no zero-deathT6 wave-free win. Road W1=50%, band40–60%; flank W1=62.5%,
band52.5–72.5%. Turtle/retreat majority losses, all wins engage wave. Objective,
HP, damage, moves, ranges, LOS, scout rules and turn15 frozen. Try leader-only
first, then wave-only if needed; terrain/gating only if those fail. Ablations
use original spike06 operator so W3 policy improvements are not confounded.

Leader-only completed ablations (40 seeds EACH policy):

| Lever alone | road | flank | turtle | retreat | dash wins / bypass | scripted wins / bypass / freeT6 |
| --- | --- | --- | --- | --- | --- | --- |
| baseline |20|25|5|0|34/33|40 (see baseline)/wave-free counterexamples|
| post(20,9)→(22,9), hold follows |18|27|0|2|24/15|15/1/1|
| announced one-step wave fallback |20|16|1|0|36/36|23/2/2|

Post-only retains difficulty but fails bypass; fallback fails both bypass and
flank band. Thus proceed to wave-only timing, before terrain or objective gates.
Trial-only fallback flag absent in defaults/snapshots, so historical rules unchanged.
Compact ablation runner uses identical policy/rules and records terminal/deaths/
wave contacts without idle/LOS sampling; every complete case has240 reports.
Earlier expensive partial sweeps retained in attempts; completed policy partitions
were resumed. Trace hashes for compact trials use their own documented event
collector and are not compared to full telemetry hashes.

Harness override correction: merge candidate level BEFORE initial and scripted
placement, rather than erasing a bypass fixture after placement. Original no-
override results unchanged. T5 partial-start earlier-wave trials now use actual
arrival born_turn, preventing an accidental second birth-rest turn onT5. They
still stage full-HP allies and stationary entry wave; not full-route evidence.

One historical exact-death-array assertion now projects its original id/kind/turn
fields and additionally asserts killer and phase-start HP/threat. The diagnostic
fields added inW1 made raw dictionary equality obsolete; no old expectation lost.

Selected minimal successful combination: post-wave-t3. Full ablation table and
every240-run candidate in ablation/ABLATION.md, summary.json and case/runs.json.
T4-only and both T4+post combinations retain full-route bypasses; T3 alone closes
them but road65%/flank80% exceed the bands. One-cell post+T3 still road65%; two-cell
post+T3 gives road24/40=60%, flank23/40=57.5%, turtle6/40=15%, retreat2/40=5%.
No full-route wave-free wins; scripted probe no wave-free win. No terrain or
objective gate needed. This is an empirical40-seed closure, not a universal proof
against every human policy. Larger position shift was retained only after the
smaller tested shift missed the difficulty band. No HP padding or enemy nerf.

| Changed value | Before → after | Reason |
| --- | --- | --- |
| leader deployment |(20,9)→(22,9)| keep leader beside the east escort, rebalance early-wave route |
| hold_point |(20,9)→(22,9)| guard/counter radius follows leader post; radius itself stays2 |
| reinforcement_turn |5→3| wave can actT4, before earliest real-deployment T5 leader kills |
| warning turn (derived) |4→2| still a full turn of visible notice before arrival |
| wave warning number in O (derived) |T5→T3| same accepted format/width/font/colour; show actual authored arrival |

Accepted V six colours and O group labels/markers/layout remain unchanged. The
timing lever necessarily updates the wave warning's numeric content; safest
interpretation is truthful state text, not a label redesign. Record this explicit
interpretation in handoff. Existing banner/defense art remains at its original
landmark; no art edit. Bodyguard radius3, intercept6, leader counter/step-back,
entries(23,8..10), three knights, birth rest and marchT6 unchanged. Trial-only
leader_wave_fallback remains absent from all default/snapshot data.

Tests: test_spike07.gd6/6,63assertions exit0. Historical T5 wave/leader pins now
explicitly use spike06 data/operator; original assertions intact. New tests pin
the FULL snapshot source SHA256, frozen contracts/deployment of every other
unit, leader/entry reachability, T2 warning<T3 arrival/birth rest/determinism/
immutability, plus1014 full dash and partial bypass without wave-free wins.
Original1014 variant still T6 zero-death wave-free. Commit follows W2 completion.
