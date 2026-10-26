# W1 baseline — seed 24018

Unchanged spike04 rules/data at 905c0ce (brief commit db47f3a). All three terminal outcomes reproduced.
Telemetry-only changes; original runs retained in original/. LOS is counterfactual only.

| Policy | Result/turn | Contact | Real idle by group | Wave engages | LOS blocked shots | Estimate min |
| --- | --- | --- | --- | --- | --- | --- |
| road | win/12 | 2 | {"flank":9,"front":2,"leader":7,"rear":22,"reinforcements":18,"reserve":4,"south":4} | -1 | 3 | 12.8998–21.2331333333333 |
| flank | lose/7 | 2 | {"flank":6,"front":2,"leader":7,"rear":14,"reinforcements":6,"reserve":13,"south":4} | -1 | 1 | 8.73321666666667–14.3998833333333 |
| turtle | lose/3 | 2 | {"flank":9,"front":2,"leader":3,"rear":6,"reinforcements":0,"reserve":6,"south":6} | -1 | 1 | 4.59995–7.59995 |

True idle = eligible living enemy has no cost-legal reachable attack, no movement and no attack in its completed phase; explicit role holds are reported separately. Old idle_turns is retained and means no reachable attack even if advancing. South/reserve remain separate authored groups, not silently merged into front/rear.

Estimates use spike04 measured enemy mean 1.999s, actual living ally unit-turns × assumed 15–25s. Not human play time. Death class/turn and damage/kill shares are in each JSON.

Counterfactual W3 LOS: centre supercover, exact corner checks both orthogonal cells (x then y); intermediate cliff/deep water and units block; forest on the line or target gives −1 damage, min1. No behavior changes in W1.

Godot initial sandbox launch exit1 (executable inaccessible); full-path escalated retry exit0. Fetch initially metadata denied; authorized retry exit0. Process listing identifies this CLI in the spike worktree; desktop app processes alone do not prove an active session in this folder. Owner explicitly cleared autonomous work here.
