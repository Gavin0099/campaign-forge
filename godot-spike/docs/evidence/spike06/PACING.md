# spike-06 multi-seed before/after

20 fixed seeds per policy. Before: unchanged spike05 data/operator. After: tuned default plus supported road/flank and scout kit. Bypass is a scripted turn5 start, not full-battle pacing.

| Policy/version | Win | Win turn median[range] | Loss turn | Mean casualties M/R/S | Wave all / wins | First engage | True idle | Estimate median; full range min |
| --- | ---: | --- | --- | --- | --- | --- | ---: | --- |
| road/before | 0% | — | 6 [5–8] | 1.60/0.45/1.85 | 0%/— | — | 37.1% | 7.3–12.0; 6.8–16.3 |
| road/after | 50% | 14 [10–15] | 14.5 [7–16] | 0.70/0.65/1.50 | 100%/100% | 7 [6–8] | 26.9% | 17.5–28.9; 10.7–35.0 |
| flank/before | 0% | — | 5 [5–7] | 1.95/0.00/1.05 | 0%/— | — | 43.2% | 6.8–11.1; 6.8–16.2 |
| flank/after | 70% | 13 [7–15] | 16 [7–16] | 0.45/0.50/1.15 | 95%/100% | 7 [6–8] | 30.0% | 17.2–28.4; 9.9–33.7 |
| turtle/before | 0% | — | 8 [6–10] | 1.15/0.20/1.80 | 30%/— | 9 [7–10] | 32.6% | 10.7–17.5; 9.3–22.2 |
| turtle/after | 0% | — | 12 [9–16] | 1.10/1.05/1.45 | 100%/— | 8 [7–9] | 31.7% | 14.8–24.5; 12.2–29.6 |
| scout-retreat/before | 0% | — | 5 [5–9] | 2.00/0.30/0.90 | 0%/— | — | 40.0% | 6.8–11.1; 6.8–21.8 |
| scout-retreat/after | 0% | — | 8 [6–10] | 1.85/0.10/0.00 | 80%/— | 7 [7–8] | 28.6% | 12.2–20.2; 8.6–24.4 |
| bypass/before | 0% | — | 6 [5–7] | 1.00/0.50/0.90 | 20%/— | 6.5 [6–7] | 0.0% | 3.3–5.3; 1.8–7.1 |
| bypass/after | 100% | 7 [6–9] | — | 0.05/0.50/0.15 | 85%/85% | 6 [5–6] | 6.9% | 4.7–7.7; 3.1–11.5 |

Estimate = (result turn × enemy mean + living ally unit-turns × assumed15–25 seconds)/60. Before mean3.456164s; after1.476336s from12 actual normal phases of the uncaptured flank seed24018 win13. A conservative result-turn phase is included even for a player-turn win. Bypass uses observed ally turns from its scripted start, so never compare its minutes as a full route.
No15–25min acceptance from model arithmetic: intervals span outside target; no HP padding. Actual human minutes pending.

## Pressure and wave details

| Policy/version | front | flank | south | reserve | rear | leader | wave | Observed enemy turns | Wave attacks / attacked median[range] | LOS blocked actual shots / phase-start opportunities |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| road/before | 38 | 177 | 40 | 42 | 120 | 40 | 0 | 1232 | — / — | 0 / 18 |
| road/after | 40 | 98 | 20 | 55 | 0 | 74 | 0 | 1066 | 7 [6–9] / 8 [7–9] | 0 / 62 |
| flank/before | 38 | 123 | 40 | 48 | 120 | 60 | 0 | 993 | — / — | 0 / 30 |
| flank/after | 40 | 93 | 20 | 58 | 0 | 77 | 0 | 961 | 7 [6–9] / 8 [7–9] | 0 / 43 |
| turtle/before | 0 | 180 | 40 | 120 | 120 | 60 | 0 | 1596 | 9 [7–10] / 9 [9–10] | 0 / 115 |
| turtle/after | 40 | 100 | 20 | 97 | 0 | 97 | 0 | 1116 | 8 [7–9] / 9 [8–10] | 0 / 121 |
| scout-retreat/before | 38 | 132 | 40 | 50 | 120 | 60 | 0 | 1099 | — / — | 0 / 35 |
| scout-retreat/after | 40 | 55 | 20 | 26 | 0 | 79 | 0 | 768 | 7 [7–8] / 8 [7–8] | 0 / 33 |
| bypass/before | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 367 | 6 [6–6] / 7 [7–7] | 0 / 100 |
| bypass/after | 0 | 0 | 20 | 0 | 0 | 0 | 0 | 290 | 6 [6–6] / 7 [5–7] | 0 / 44 |

True idle: eligible observed enemy actor, no reachable attack at registration, no move/attack, no explicit role hold. Inactive guards count; birth rest and unprocessed terminal tails do not. Legal actual shots must remain unblocked; opportunity counts are in-range blocked pairs at phase registration, not all hypothetical moves.

## Class contribution / survival

| Policy/version/class | Damage/share | Kills/share | Finishing kills | Intercepts | Mean deaths | Death turn median[range] | Living unit-turns |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| road/before/melee | 250/41.1% | 23/28.4% | 23 | 0 | 1.60 | 6 [4–8] | 234 |
| road/before/ranged | 224/36.8% | 49/60.5% | 49 | 0 | 0.45 | 7 [6–7] | 249 |
| road/before/mobile | 134/22.0% | 9/11.1% | 9 | 0 | 1.85 | 2 [2–5] | 126 |
| road/after/melee | 389/39.2% | 35/24.1% | 35 | 0 | 0.70 | 9.5 [7–15] | 486 |
| road/after/ranged | 368/37.1% | 40/27.6% | 40 | 0 | 0.65 | 11 [7–13] | 474 |
| road/after/mobile | 235/23.7% | 70/48.3% | 70 | 100 | 1.50 | 8 [3–13] | 354 |
| flank/before/melee | 175/39.6% | 9/20.9% | 9 | 0 | 1.95 | 5 [4–7] | 186 |
| flank/before/ranged | 155/35.1% | 34/79.1% | 34 | 0 | 0.00 | — | 204 |
| flank/before/mobile | 112/25.3% | 0/0.0% | 0 | 0 | 1.05 | 2 [2–5] | 146 |
| flank/after/melee | 390/39.4% | 42/28.2% | 42 | 0 | 0.45 | 9 [6–10] | 468 |
| flank/after/ranged | 352/35.6% | 46/30.9% | 46 | 0 | 0.50 | 9 [7–13] | 452 |
| flank/after/mobile | 248/25.1% | 61/40.9% | 61 | 87 | 1.15 | 8 [3–14] | 364 |
| turtle/before/melee | 379/44.6% | 57/48.3% | 57 | 0 | 1.15 | 9 [6–10] | 331 |
| turtle/before/ranged | 272/32.0% | 38/32.2% | 38 | 0 | 0.20 | 7 [7–7] | 324 |
| turtle/before/mobile | 198/23.3% | 23/19.5% | 23 | 0 | 1.80 | 4 [3–10] | 208 |
| turtle/after/melee | 382/45.3% | 41/35.3% | 41 | 0 | 1.10 | 11 [9–13] | 460 |
| turtle/after/ranged | 280/33.2% | 33/28.4% | 33 | 0 | 1.05 | 8 [4–11] | 388 |
| turtle/after/mobile | 181/21.5% | 42/36.2% | 42 | 94 | 1.45 | 4 [3–11] | 299 |
| scout-retreat/before/melee | 190/43.7% | 15/30.0% | 15 | 0 | 2.00 | 5 [4–9] | 195 |
| scout-retreat/before/ranged | 173/39.8% | 34/68.0% | 34 | 0 | 0.30 | 6 [4–9] | 212 |
| scout-retreat/before/mobile | 72/16.6% | 1/2.0% | 1 | 0 | 0.90 | 2 [2–5] | 170 |
| scout-retreat/after/melee | 370/57.6% | 53/61.6% | 53 | 0 | 1.85 | 8 [4–10] | 303 |
| scout-retreat/after/ranged | 208/32.4% | 27/31.4% | 27 | 0 | 0.10 | 9 [9–9] | 318 |
| scout-retreat/after/mobile | 64/10.0% | 6/7.0% | 6 | 47 | 0.00 | — | 320 |
| bypass/before/melee | 156/34.5% | 5/13.2% | 5 | 0 | 1.00 | 6 [5–7] | 78 |
| bypass/before/ranged | 150/33.2% | 15/39.5% | 15 | 0 | 0.50 | 6 [6–6] | 75 |
| bypass/before/mobile | 146/32.3% | 18/47.4% | 18 | 0 | 0.90 | 6 [6–7] | 73 |
| bypass/after/melee | 207/31.5% | 11/14.9% | 11 | 0 | 0.05 | 7 [7–7] | 128 |
| bypass/after/ranged | 227/34.5% | 38/51.4% | 38 | 0 | 0.50 | 7 [6–8] | 116 |
| bypass/after/mobile | 224/34.0% | 25/33.8% | 25 | 40 | 0.15 | 7 [6–8] | 125 |

## Locked targets

- intended_flank_win_ge_60: PASS
- wave_ge_70_of_wins: PASS
- idle_le_35: PASS
- not_all_wins_before8: PASS
- scout_not_top_damage: PASS
- scout_leads_finishers: PASS
- scout_death_median_later: PASS
- naive_policy_loses_majority: PASS
- all_intended_estimate_intervals_inside_15_25: FAIL

Only0/20 intended-policy full estimate intervals fit15–25min; median interval is17.2–28.4min.
Melee supplies the durable screen and the highest aggregate damage; ranged supplies LOS-constrained support; scouts lead finishing/interception rather than damage. Death medians are conditional on dying, with survivors censored; longer battles and deployment/count changes confound isolation of kit effects. Some scouts still die early. Finishing kill = last hit against an already wounded target; baseline counts recomputed from unchanged damage events using the same definition. Intercept = a movement ended on scout control (one source credited if several), not a guaranteed prevented attack.
All100 spike05 recheck traces, commands, outcomes, casualties, classes and unit-turns match W1. No jitter or random damage. Distinct traces per20 after: road 20, flank 20, turtle 12, scout-retreat 14, bypass 10.
BOTH policies and level changed between versions; this is not isolated LOS/AI causality, optimal strategy proof, human blind play or commercial quality acceptance.

## Scripted bypass counterexamples

The probe starts atT5 with pre-positioned allies. Its100% win rate and low average casualties are not evidence of an obtainable optimal full route. The wave is still avoidable; no forced objective was introduced. These no-wave wins remain explicit design risks:

| Seed | Win turn | Casualties |
| --- | ---: | ---: |
| 1014 | 6 | 0 |
| 1015 | 6 | 0 |
| 1017 | 6 | 0 |
