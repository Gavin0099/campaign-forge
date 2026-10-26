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
