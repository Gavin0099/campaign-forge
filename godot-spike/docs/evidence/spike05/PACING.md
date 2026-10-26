# Before/after pacing — seed24018, automated policies

Same original 24×18 terrain/deployment, HP/damage/move4/3/6, leader objective, limit15, warning4/arrival5.
W1 reproduced road win12, flank lose7, turtle lose3; W2-only intermediates retained in w2/.

| Policy/version | Result/turn | Contact | Wave first engaged | LOS-blocked actual shots | Living ally turns | Estimate min |
| --- | --- | ---: | --- | ---: | ---: | --- |
| road/before | win/12 | 2 | never | 3 | 50 | 12.9–21.2 |
| road/after | lose/8 | 2 | never | 0 | 38 | 10.0–16.3 |
| flank/before | lose/7 | 2 | never | 1 | 34 | 8.7–14.4 |
| flank/after | lose/7 | 2 | never | 0 | 38 | 9.9–16.2 |
| turtle/before | lose/3 | 2 | never | 1 | 18 | 4.6–7.6 |
| turtle/after | lose/6 | 2 | never | 0 | 36 | 9.3–15.3 |
| bypass/after | lose/7 | 5 | 7 | 0 | 16 | 4.4–7.1 |
| scout-retreat/after | lose/9 | 2 | never | 0 | 51 | 13.3–21.8 |

Formula: turns × (measured enemy mean + mean living allies/turn × assumed15–25s). Before mean1.999s; after mean3.456164s from actual road scene.
Menu/reading breaks omitted; extra conservative phase counted on a winning turn. Bypass begins at scripted turn5, so its estimate uses only observed ally turns plus the absolute result turn; it is NOT full-battle pacing.
15–25min target is not established: all three fixed simple policies lose, road victory regresses.
Flank7 and turtle6 still collapse. AI adds pressure and LOS removes some shots; policy mistakes
and difficulty are confounded. No stat/objective/terrain relaxation was made to manufacture wins.

| Policy/version | front | flank | south | reserve | rear | leader | wave | Total true idle / observed enemy turns |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| road/before | 2 | 9 | 4 | 4 | 22 | 7 | 18 | 66/97 (68.0%) |
| road/after | 0 | 6 | 2 | 4 | 6 | 2 | 0 | 20/77 (26.0%) |
| flank/before | 2 | 6 | 4 | 12 | 12 | 6 | 3 | 45/68 (66.2%) |
| flank/after | 0 | 9 | 2 | 4 | 6 | 3 | 0 | 24/69 (34.8%) |
| turtle/before | 2 | 6 | 4 | 4 | 4 | 2 | 0 | 22/26 (84.6%) |
| turtle/after | 0 | 9 | 2 | 6 | 6 | 3 | 0 | 26/55 (47.3%) |
| bypass/after | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/29 (0.0%) |
| scout-retreat/after | 0 | 9 | 2 | 6 | 6 | 3 | 0 | 26/88 (29.5%) |

True idle = eligible enemy with observed actor phase, no reachable attack, no move, no attack, and no explicit deliberate hold. Inactive guard phases count idle. Born-turn and unprocessed actors after terminal do not.
W1 raw enemy_idle_by_group predates the terminal-tail correction; this table recomputes BOTH versions
from their preserved trace/rows. Original JSON untouched; raw historical idle_turns still includes advancing enemies.
Bodyguard at the radius boundary is now explicitly logged as a protection hold, not silent idle.

| Policy/version/class | Damage/share | Kills/share | Ally deaths (id@turn) |
| --- | --- | --- | --- |
| road/before/melee | 34/53.1% | 4/40.0% | guard@11 |
| road/before/ranged | 20/31.2% | 6/60.0% | bow-2@8 |
| road/before/mobile | 10/15.6% | 0/0.0% | scout-1@3, scout-2@4 |
| road/after/melee | 18/42.9% | 4/66.7% | guard@7, thoma@8 |
| road/after/ranged | 10/23.8% | 1/16.7% | bow-2@6 |
| road/after/mobile | 14/33.3% | 1/16.7% | scout-1@4, scout-2@5 |
| flank/before/melee | 16/44.4% | 3/60.0% | guard@5, thoma@7 |
| flank/before/ranged | 18/50.0% | 2/40.0% | none |
| flank/before/mobile | 2/5.6% | 0/0.0% | scout-1@4, scout-2@4 |
| flank/after/melee | 20/57.1% | 2/50.0% | guard@7, thoma@7 |
| flank/after/ranged | 11/31.4% | 2/50.0% | none |
| flank/after/mobile | 4/11.4% | 0/0.0% | scout-2@5, scout-1@5 |
| turtle/before/melee | 2/50.0% | 0/0.0% | thoma@3 |
| turtle/before/ranged | 2/50.0% | 0/0.0% | none |
| turtle/before/mobile | 0/0.0% | 0/0.0% | none |
| turtle/after/melee | 15/53.6% | 2/50.0% | thoma@6 |
| turtle/after/ranged | 5/17.9% | 1/25.0% | none |
| turtle/after/mobile | 8/28.6% | 1/25.0% | none |
| bypass/after/melee | 12/37.5% | 1/50.0% | thoma@7 |
| bypass/after/ranged | 12/37.5% | 1/50.0% | none |
| bypass/after/mobile | 8/25.0% | 0/0.0% | scout-1@6, scout-2@6 |
| scout-retreat/after/melee | 24/54.5% | 2/33.3% | guard@7, thoma@9 |
| scout-retreat/after/ranged | 18/40.9% | 4/66.7% | bow-2@8, bow-1@9 |
| scout-retreat/after/mobile | 2/4.5% | 0/0.0% | none |

Road ranged kill share60% before →16.7% after, damage31.25%→23.8%; cover/LOS and AI both changed, so this is not isolated LOS causality.
Road mobile damage15.6%→33.3% but both still die early. Scout-retreat preserves scouts longer at the cost of very little damage; noHP/damage buff, no route edits. Mobility role remains an Owner question.
Wave never engages the three short western fights. Full-roster scripted bypass is first contested on turn7
(either side attacking counts engagement); isolated pursuit test/capture separately proves wave actively attacks
within two eligible turns. Neither proves the wave cannot ever be bypassed; leader-kill objective stays.
No initial-deployment winning policy was established after the AI change. The staged terminal win capture
only proves the objective/result screen, not whole-map winnability. Human blind road/flank/turtle tests pending.
No terrain or position changes to authored level data. All values are spike tests, not canon.
