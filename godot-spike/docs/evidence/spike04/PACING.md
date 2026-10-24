# Pacing and balance — automated evidence, HUMAN_PENDING

Seed24018; rules-only policies have no presentation time. The road policy was also
played continuously through the real scene to win on turn12. The other two policies
are deliberately simple probes; their losses are not proof those routes are unwinnable.
Road: melee-first nearest legal attack / approach leader. Flank: mobile goes via north
ford(16,5). Turtle: stage at(10,9/10), then hold melee unless an attack is reachable.
Targets prefer leader, then lowestHP/id; neither policy is an expert tactics solver.

| Policy | Initial result/turn | Retuned result/turn | First contact | Living ally unit-turns | Estimated min |
| --- | --- | --- | ---: | ---: | --- |
| road | lose/7 | win/12 | 2 | 50 | 12.9–21.2 |
| flank | lose/6 | lose/7 | 2 | 34 | 8.7–14.4 |
| turtle | lose/3 | lose/3 | 2 | 18 | 4.6–7.6 |

Initial front/side groups overwhelmed every policy. Only authored enemy positions
were retuned: two front, south/flank farther back, rear beyond leader. No stats,
terrain, wave, turn limit or policy were relaxed. Both runs are retained in autoplay/.
First front is 11–12 Manhattan cells from deployment; all policies contact on turn2
(target2–3), so no four-turn empty opening. Northern forest/ford has higher move cost.

Measured normal enemy mean = 1.999s over 11 real phases,
max = 4.719s. Estimate formula:
`turns × (measured enemy mean + mean living allies/turn × assumed 15–25s think/unit)`.
Equivalently sum living ally unit-turns ×15–25s plus turns × enemy mean. It includes
a conservative extra enemy phase on the winning turn and omits menu/reading breaks.
Road has50 unit-turns /12 =4.17 living allies/turn: about12.9–21.2min. A fixed
six-unit assumption gives18.4–30.4min. The15–25min goal is plausible but not verified;
flank/turtle terminate too soon. Human pacing/balance remains pending.

| Policy / ally kind | Mean actual steps/unit-turn | Attacks | Damage dealt/taken | Damage share | Kills/share | No reachable target phases |
| --- | ---: | ---: | --- | ---: | --- | ---: |
| road/melee | 2.65 | 17 | 34/10 | 53.1% | 4/40.0% | 5 |
| road/ranged | 2.25 | 10 | 20/10 | 31.2% | 6/60.0% | 7 |
| road/mobile | 4.86 | 5 | 10/12 | 15.6% | 0/0.0% | 2 |
| flank/melee | 2.42 | 8 | 16/16 | 44.4% | 3/60.0% | 4 |
| flank/ranged | 2.29 | 9 | 18/6 | 50.0% | 2/40.0% | 5 |
| flank/mobile | 4.25 | 1 | 2/12 | 5.6% | 0/0.0% | 2 |
| turtle/melee | 2.33 | 1 | 2/8 | 50.0% | 0/0.0% | 4 |
| turtle/ranged | 2.67 | 1 | 2/0 | 50.0% | 0/0.0% | 4 |
| turtle/mobile | 2.67 | 0 | 0/0 | 0.0% | 0/0.0% | 2 |

Movement averages include zero-move living phases, not just moves; per-unit per-turn
steps and weighted cost are in JSON. Idle means no target can be attacked from any
cost-legal destination at phase start, even if the unit moves toward contact.

Road melee supplies53.1% damage and17 attacks: it does engage. Ranged supplies31.3%
damage but60% of kills (last-hit/order bias): flag for human review. Mobile supplies
15.6% damage and dies early, so speed is not dominating this policy. Flank ranged
is50% damage, not >50%; turtle is50% of only4 total damage. These tiny samples do
not establish balance. No LOS benefits ranged; simple leader pursuit exposes scouts.
Road enemy knights have72 no-target unit-phases; rear/wave guards can be bypassed
because the objective is leader defeat, not rout. Reinforcements visibly arrive but
may never engage: a design risk to assess before any larger map. No32×24 built.
