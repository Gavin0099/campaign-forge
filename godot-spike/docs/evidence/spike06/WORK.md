# spike-06 work record (SPIKE TEST VALUES, not canon)

Owner authorization: 2026-10-26 19:17 Asia/Taipei; brief HEAD
8010bde2047bc9a5b268bedf03de64a2c1ef5873. Worktree starts
clean on codex/godot-spike. Scope is godot-spike/ only. No push/PR/merge/stash.
The Owner explicitly assigned this worktree; process listing found desktop and
CLI processes but does not prove their CWD. No additional agent is launched;
no concurrent file modifications observed. No claim of inspecting other worktrees.

## Fixed acceptance thresholds (set before W2 tuning)

- At least one intended policy >=60% wins on the committed 20 seeds; aim >=70%.
- A naive policy still loses >50%; wins must not all finish before T8,
  desired decisive turns 9–14. Winning policy true idle <=35%.
- Wave attacks or is attacked in >=70% of intended-policy winning seeds.
- Scouts outlive spike05 T4–5, lead/co-lead finishing kills/intercepts and do
  not lead damage. No HP padding, base damage/move/LOS/objective/limit changes.
- Enemy-phase estimate 15–25 minutes is reported honestly, never manufactured.
- Every new rule stays pure and has tests; all historical tests retained.

Keep/rework criterion: preserve the prototype if evidence shows an accessible
winning route with meaningful reinforcement/scout decisions. Rework if this
requires hidden forced engagement or arbitrary HP inflation. Human enjoyment,
blind plays and art approval are separate HUMAN_PENDING gates. The Owner's
W1–W8 scope supersedes the generic prototype-fast timebox; no art investment.

## W1

Preserved byte-for-byte field data as field_24x18_spike05.gd. Harness seeds:
24018,1001..1019. Seed24018 retains historical policy ordering; others hash
seed+turn+unit ID only among equal-class action choices and equal-HP targets.
AI retains its existing tiny coordinate tie-break. No RNG, deployment jitter,
damage variance or hidden game-rule adjustment. Trace distinctness excludes
report metadata. Bypass remains a labelled scripted mid-battle probe.

External executables: Owner-specified full Godot/Python paths fail resolution
inside sandbox; identical paths succeed with escalation (4.7.2/Python3.12.10).
Existing Git login/remote only, fetch succeeded. This is local offline tool use,
not complete trust-root hardening: inherited environment/DLL/Git resolution
are not adversarially verified. Evidence tools add no subprocess/network.
Shared PLAN/memory are outside this segment's writable scope; milestones are
recorded here and in the final project handoff. Task DONE is not SessionEnd.

W1 completed: baseline100/100 terminal, no illegal commands; all policies0% wins.
Distinct traces per20: road10,flank9,turtle14,scout-retreat9,bypass8 (none has90%
identical traces). Road loss median6[5–8],flank5[5–7],turtle8[6–10],retreat5[5–9],
bypass6[5–7]. W1 tests4/4,18 assertions,exit0. Commit5cff31f.

## W2 — root cause and counter-play contract

The original policy spends each unit's full move minimizing distance to ANY
attack slot, without danger, screen cohesion or Thoma protection. Scouts move6
ahead of move4 melee, then suffer concentrated attacks. Target priority always
favours leader even over an available kill. Same-class action order changes
collapse time substantially, so all-loss alone does not prove an unfair map.
All11 knights plus leader join/hold around a single T4 global march/latched
chain. All fifteen possible enemies have94 total HP versus40 allied HP
(2×8+2×6+2×6), equal base damage2; player needs local numerical advantage,
not simultaneous global attrition. Wave is too far east for western collapses.
These are mechanisms to probe, not isolated causal claims. Ablations run a
stronger supported-road operator on unchanged spike05 first, then deployment,
then march timing, then enemy count. No HP/base damage/move/terrain edits.

Intended route: disciplined main-road push with melee screening two bows,
scouts staying near the screen until a flank/finisher opportunity. Thoma pulls
back when wounded. The original turtle and scout-retreat remain weak probes;
the scripted bypass is not a complete route. These operators are not optimal
human play and do not prove difficulty distribution.

W2 ablation evidence: w2/ (first stronger-policy candidate), w2-second/
(wounded retreat/kill priority correction), raw logs retained. Initial parse
failure was an untyped Vector2i ternary; stopped only that task's process,
fixed explicit type, reran exit0. Failed log retained, not acceptance evidence.
Policy-only first candidate lost T14/9/13; after retreat fix lost T4/15/15
(24018/1001/1007), showing the heuristic is imperfect, not an optimal solver.
Forward deployment (6–7 columns) failed all three; rejected. Compact western
screen, delayed march and eight-knight candidates still mostly lost. Six-knight
candidate across20 seeds:45% road winsT13–15, turtle0%; idle27.33% road,
wave engaged100% of wins. One remaining bodyguard is tested next.

Selected W2 changes (all spike test values):
| Lever | Before -> after | Reason |
| --- | --- | --- |
| thoma | (3,9) -> (3,10) | behind durable screen rather than spearhead |
| guard | (3,10) -> (4,9) | first road screen |
| bow-1 / bow-2 | (2,8)/(2,11) -> (3,8)/(3,11) | support screen without wasting one advance |
| scout-1 / scout-2 | (3,7)/(3,12) -> (2,8)/(2,11) | rear flank support, no isolated initial sprint |
| march_turn | 4 -> 6 | allow local opening before remaining groups converge; sight/chained alert still immediate |
| knight-4 (12,15) south | present -> omitted | fewer simultaneous southern attackers |
| knight-6 (19,4), knight-7 (20,4) flank | present -> omitted | one northern interceptor rather than three-unit pileup |
| knight-10 (22,14), knight-11 (23,15) rear | present -> omitted | avoid another full attrition wave on top of announced reinforcement wave |
| knight-9 (19,10) reserve | present -> omitted | single bodyguard after six-knight45% candidate missed60% |
| initial knights / leader / wave | 11/1/3 -> 5/1/3 | local numerical counter-play, all survivors retain original HP/damage |
| policy | nearest-target rush -> supported road/flank, kill priority, wounded retreat, scout cohesion | correct obvious operator mistakes first |

No authored terrain/enemy placement/group membership, alert6, chain5, support3,
bodyguard radius3, intercept6, leader behaviour, wave timing/entries, stats or
objective/limit changed. Entry fallback/LOS and all Skirmish rules untouched.

Historical test migrations: old roster-count/map assertions now explicitly use
spike05 data; original18-actor battle/visibility fixtures restored from spike05;
T4 AI fixture uses spike05. Historical autoplay test uses preserved spike05
operator+data. No assertion deleted, weakened or moved onto fabricated results;
new tuned-data legality/reachability/determinism tests run independently.

W2 final 20-seed validation: road17/20=85% wins, median12[9–14], true
idle31.08%, mean2.15 casualties. Turtle8/20=40% wins (loses60%), win14–15.
All17 road wins engage the original east wave. Therefore the locked W2 win,
weak-route, decisive-turn and idle thresholds pass without stat inflation.
Estimates range14.0–35.8min; 15–25min is NOT a universal pass. W2 pure tests
3/3,38 assertions exit0. JSON and failed/intermediate candidates retained.

## W3 — reinforcement entry adjustment

W2's continuous road wins all fought the wave, but the scripted infiltration
probe bypassed it in10/20 seeds:100% win,T7–9,mean0.65 casualties. That is a
counterexample to meaningful pursuit on the fast approach, despite being an
artificial mid-battle placement, not an optimal full route. Smallest lever:
entries (23,4)/(23,5)/(23,6) -> (23,8)/(23,9)/(23,10), all map-edge/passable,
near the leader's east approach. Label now says east crossing rather than NE.
WarningT4,arrivalT5,birth rest,three original knights,closest-to-leader attacker
pursuit,leader/objective all unchanged. No forced-engagement gate.

Final20-seed road14/20=70% wins,T10–15(median12),idle30.02%,wave engagement
100% in runs/wins. Scripted bypass18/20=90% wins,T7–10(median8),mean1.95
casualties vs0.65 before;100% attacked/attacking wave. Bypass is possible but
not free/no-wave. It remains an artificially advanced start, so its higher win
rate does not establish a superior initial-deployment strategy. W6 rechecks
with final kit. Two GUT tests/19 assertions pass on both initial/final entries:
visible warning before legal rested arrivals; full continuous road has enemy
wave attack and ally wave attack, not only a pursuit isolation fixture.

## W4 — scout kit and operator experiments

Final spike test kit (allies/mobile, default only; spike05 kit absent):
- finisher +1 vs current HP <=50% max HP; base damage remains2, so a3HP
  knight can be finished. No bonus at >half, no raw stat/HP change.
- four orthogonal adjacent cells are control zones. An enemy entering one
  stops its movement there and may still attack; it can leave a controlled
  starting cell. No reaction damage/forced objective. AI uses the same reach.
- after one attack, one optional disengage of min(2,6-movement_cost_spent).
  Full6 before strike leaves0; strike before moving permits2, no second attack,
  no repeated retreat. Wait ends it, next turn resets. Weighted terrain counts.
- preview/hover display actual +1; action state exposes remaining retreat,
  cancel preserves state; V draws purple control. Ground threat uses the same
  controlled reach. Events distinguish intercept/disengage from damage.

Operator mistakes exposed by experiments: first cap2 policy was too passive
+ used only4 travel;20% road wins. Full travel6, healthy flank attacks and
advance-aware retreat improved it; leader-aware hold/knockback evaluation then
reached50% road,70% flank. A full-remaining-move escape trial was not retained;
final cap2 keeps the smaller kit. Experiments retained in w4-* folders/logs.
Final intended route is supported main-road advance with scouts screening
north (flank policy's y7 preference), not the old unsupported north sprint.
Its20 seeds:14 wins=70%, win median13[7–15],idle29.97%,wave100% of wins.
Melee39.39% damage,ranged35.56%,mobile25.05%; mobile61 finishing kills vs
42/46,87 intercepts,median deathT8 vs spike05'sT4–5 (some still dieT3).
Scouts are not highest damage; mobile living-unit-turns364, not invulnerable.
Road50% remains riskier; W6 repeats every policy rather than claiming all pass.

Six new pure/UI tests44 assertions pass. Initial test failures were fixture
errors (a blocked full-move route and an alternate legal route around control)
and autofree while signal emitter was locked; corrected fixtures/unwind frame,
failed log retained. Full regression found one historical NE-label pin after
entry changed east; preserved original fixture/NE assertion, added east-label
assertion to new test. Final focused15/15,125 assertions exit0. Full W4 run
on the intermediate full-remaining trial is retained and not final acceptance;
W7 runs the final entire suite. grid_rules.gd untouched.
