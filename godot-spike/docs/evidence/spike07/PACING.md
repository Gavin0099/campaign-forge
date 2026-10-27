# Pacing and stratified40-seed results

Distinct traces are not independent samples; Wilson intervals describe probe counts, not human win probability.
Seeds24018,1001–1039. Seed varies coordinate AI tie-break and policy ordering only; fixed stats/damage. All default reports have no illegal commands. Bypass is a stagedT5 partial-start probe, never a full-route win or minutes estimate.

| Policy/version | Wins [95% Wilson] | Bypass wins | Win turns | Loss turns | Wave all / wins | First wave turn | M/B/S mean deaths | True idle | Distinct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| road/before06 | 50.0% [35.2%–64.8%] | 0/40 | 14 [10–15] | 16 [7–16] | 100.0% / 1.0 | 7.5 [6–9] | 0.62/0.65/1.50 | 27.5% | 40/40 |
| road/after07 | 60.0% [44.6%–73.7%] | 0/40 | 14 [12–15] | 16 [6–16] | 100.0% / 1.0 | 6 [5–7] | 0.45/0.33/1.32 | 29.2% | 40/40 |
| flank/before06 | 62.5% [47.0%–75.8%] | 1/40 | 13 [7–15] | 16 [7–16] | 95.0% / 0.96 | 7 [6–8] | 0.50/0.53/1.32 | 28.7% | 40/40 |
| flank/after07 | 67.5% [52.0%–79.9%] | 0/40 | 14 [11–15] | 9 [6–16] | 100.0% / 1.0 | 6 [5–7] | 0.50/0.35/1.40 | 29.1% | 39/40 |
| turtle/before06 | 12.5% [5.5%–26.1%] | 0/40 | 14 [13–15] | 12 [9–16] | 100.0% / 1.0 | 8 [7–9] | 1.02/1.18/1.27 | 30.0% | 28/40 |
| turtle/after07 | 10.0% [4.0%–23.1%] | 0/40 | 14 [14–15] | 10 [7–16] | 100.0% / 1.0 | 6 [5–6] | 0.93/0.57/1.30 | 33.2% | 27/40 |
| scout-retreat/before06 | 0.0% [-0.0%–8.8%] | 0/40 | — | 8 [4–11] | 72.5% / — | 7 [7–9] | 1.77/0.28/0.00 | 32.3% | 24/40 |
| scout-retreat/after07 | 5.0% [1.4%–16.5%] | 0/40 | 13 [13–13] | 8 [4–9] | 77.5% / 1.0 | 6 [6–8] | 1.60/0.07/0.35 | 31.1% | 27/40 |
| leader-dash/before06 | 85.0% [70.9%–92.9%] | 33/40 | 6 [5–7] | 6 [5–7] | 12.5% / 0.029411764705882353 | 6 [6–6] | 0.53/1.77/0.68 | 31.4% | 40/40 |
| leader-dash/after07 | 10.0% [4.0%–23.1%] | 0/40 | 6 [6–7] | 6 [5–8] | 100.0% / 1.0 | 4 [4–5] | 1.60/1.77/1.73 | 23.9% | 39/40 |
| bypass/before06 | 95.0% [83.5%–98.6%] | 3/40 | 7 [6–10] | 7 [7–7] | 92.5% / 0.9210526315789473 | 6 [5–6] | 0.10/0.45/0.23 | 6.5% | 20/40 |
| bypass/after07 | 27.5% [16.1%–42.8%] | 0/40 | 10 [9–14] | 7 [6–14] | 100.0% / 1.0 | 5 [5–5] | 1.05/0.35/1.07 | 5.3% | 28/40 |

## Policy × outcome strata

| Policy/version/outcome | n | Rate [95%] | Turns | M/B/S deaths median[range] | Wave n; first turn | Scout death turn | Distinct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| road/before06/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| road/before06/engaged-win | 20 | 50.0% [35.2%–64.8%] | 14 [10–15] | 0 [0–1] / 0 [0–2] / 1 [0–2] | 20; 7.5 [6–8] | 8 [3–11] | 20 |
| road/before06/loss-Thoma | 8 | 20.0% [10.5%–34.8%] | 8 [7–15] | 1 [1–2] / 0 [0–1] / 1 [0–2] | 8; 7.5 [7–8] | 7 [3–13] | 8 |
| road/before06/loss-timeout | 12 | 30.0% [18.1%–45.4%] | 16 [16–16] | 1 [0–1] / 2 [0–2] / 2 [2–2] | 12; 7.5 [7–9] | 9 [3–15] | 12 |
| road/after07/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| road/after07/engaged-win | 24 | 60.0% [44.6%–73.7%] | 14 [12–15] | 0 [0–1] / 0 [0–1] / 1 [0–2] | 24; 6 [6–7] | 7 [4–13] | 24 |
| road/after07/loss-Thoma | 7 | 17.5% [8.7%–32.0%] | 7 [6–15] | 1 [1–2] / 0 [0–1] / 1 [0–2] | 7; 6 [5–6] | 6 [4–10] | 7 |
| road/after07/loss-timeout | 9 | 22.5% [12.3%–37.5%] | 16 [16–16] | 1 [0–1] / 0 [0–2] / 1 [0–2] | 9; 6 [5–6] | 7 [4–15] | 9 |
| flank/before06/bypass-win | 1 | 2.5% [0.4%–12.9%] | 7 [7–7] | 0 [0–0] / 0 [0–0] / 1 [1–1] | 0; — | 5 [5–5] | 1 |
| flank/before06/engaged-win | 24 | 60.0% [44.6%–73.7%] | 13.5 [7–15] | 0 [0–1] / 0 [0–2] / 1 [0–2] | 24; 7 [6–8] | 8 [3–14] | 24 |
| flank/before06/loss-Thoma | 4 | 10.0% [4.0%–23.1%] | 7 [7–8] | 1 [1–1] / 0 [0–0] / 0.5 [0–1] | 3; 7 [7–7] | 5 [3–7] | 4 |
| flank/before06/loss-timeout | 11 | 27.5% [16.1%–42.8%] | 16 [16–16] | 1 [0–1] / 1 [0–2] / 2 [0–2] | 11; 8 [7–8] | 10 [3–14] | 11 |
| flank/after07/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| flank/after07/engaged-win | 27 | 67.5% [52.0%–79.9%] | 14 [11–15] | 0 [0–1] / 0 [0–1] / 2 [0–2] | 27; 6 [5–7] | 7 [4–12] | 27 |
| flank/after07/loss-Thoma | 7 | 17.5% [8.7%–32.0%] | 9 [6–9] | 1 [1–2] / 0 [0–0] / 1 [0–2] | 7; 6 [6–6] | 6 [4–7] | 6 |
| flank/after07/loss-timeout | 6 | 15.0% [7.1%–29.1%] | 16 [16–16] | 1 [0–1] / 1 [0–2] / 2 [1–2] | 6; 6 [5–6] | 7 [6–11] | 6 |
| turtle/before06/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| turtle/before06/engaged-win | 5 | 12.5% [5.5%–26.1%] | 14 [13–15] | 0 [0–1] / 1 [0–2] / 1 [0–1] | 5; 8 [8–9] | 10 [8–10] | 5 |
| turtle/before06/loss-Thoma | 21 | 52.5% [37.5%–67.1%] | 11 [9–13] | 2 [1–2] / 1 [0–2] / 1 [1–2] | 21; 8 [7–8] | 6 [3–11] | 12 |
| turtle/before06/loss-timeout | 14 | 35.0% [22.1%–50.5%] | 16 [16–16] | 1 [0–1] / 1 [1–2] / 1.5 [1–2] | 14; 8 [7–9] | 4 [3–13] | 11 |
| turtle/after07/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| turtle/after07/engaged-win | 4 | 10.0% [4.0%–23.1%] | 14 [14–15] | 0 [0–0] / 0 [0–1] / 2 [1–2] | 4; 6 [6–6] | 7 [3–10] | 4 |
| turtle/after07/loss-Thoma | 28 | 70.0% [54.6%–81.9%] | 7 [7–13] | 1 [1–2] / 0 [0–2] / 1 [0–2] | 28; 6 [5–6] | 6 [3–9] | 17 |
| turtle/after07/loss-timeout | 8 | 20.0% [10.5%–34.8%] | 16 [16–16] | 0 [0–1] / 1 [1–2] / 2 [2–2] | 8; 5 [5–6] | 6 [4–13] | 6 |
| scout-retreat/before06/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| scout-retreat/before06/engaged-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| scout-retreat/before06/loss-Thoma | 40 | 100.0% [91.2%–100.0%] | 8 [4–11] | 2 [1–2] / 0 [0–1] / 0 [0–0] | 29; 7 [7–9] | — | 24 |
| scout-retreat/before06/loss-timeout | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| scout-retreat/after07/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| scout-retreat/after07/engaged-win | 2 | 5.0% [1.4%–16.5%] | 13 [13–13] | 0 [0–0] / 0 [0–0] / 1 [1–1] | 2; 8 [8–8] | 9 [9–9] | 2 |
| scout-retreat/after07/loss-Thoma | 38 | 95.0% [83.5%–98.6%] | 8 [4–9] | 2 [1–2] / 0 [0–1] / 0 [0–1] | 29; 6 [6–6] | 6 [6–6] | 25 |
| scout-retreat/after07/loss-timeout | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| leader-dash/before06/bypass-win | 33 | 82.5% [68.0%–91.3%] | 6 [5–6] | 0 [0–1] / 2 [1–2] / 0 [0–2] | 0; — | 2 [2–4] | 33 |
| leader-dash/before06/engaged-win | 1 | 2.5% [0.4%–12.9%] | 7 [7–7] | 1 [1–1] / 2 [2–2] / 2 [2–2] | 1; 6 [6–6] | 5 [4–6] | 1 |
| leader-dash/before06/loss-Thoma | 6 | 15.0% [7.1%–29.1%] | 6 [5–7] | 2 [1–2] / 2 [2–2] / 1.5 [0–2] | 4; 6 [6–6] | 4 [2–4] | 6 |
| leader-dash/before06/loss-timeout | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| leader-dash/after07/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| leader-dash/after07/engaged-win | 4 | 10.0% [4.0%–23.1%] | 6 [6–7] | 0 [0–1] / 1 [1–1] / 1 [0–1] | 4; 4 [4–4] | 5 [5–5] | 4 |
| leader-dash/after07/loss-Thoma | 36 | 90.0% [76.9%–96.0%] | 6 [5–8] | 2 [1–2] / 2 [1–2] / 2 [1–2] | 36; 4 [4–5] | 4 [2–6] | 35 |
| leader-dash/after07/loss-timeout | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| bypass/before06/bypass-win | 3 | 7.5% [2.6%–19.9%] | 6 [6–6] | 0 [0–0] / 0 [0–0] / 0 [0–0] | 0; — | — | 2 |
| bypass/before06/engaged-win | 35 | 87.5% [73.9%–94.5%] | 7 [7–10] | 0 [0–1] / 0 [0–2] / 0 [0–2] | 35; 6 [5–6] | 7 [6–8] | 17 |
| bypass/before06/loss-Thoma | 2 | 5.0% [1.4%–16.5%] | 7 [7–7] | 1 [1–1] / 2 [2–2] / 1 [1–1] | 2; 6 [6–6] | 7 [7–7] | 1 |
| bypass/before06/loss-timeout | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| bypass/after07/bypass-win | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |
| bypass/after07/engaged-win | 11 | 27.5% [16.1%–42.8%] | 10 [9–14] | 0 [0–1] / 0 [0–2] / 1 [1–2] | 11; 5 [5–5] | 7 [6–10] | 11 |
| bypass/after07/loss-Thoma | 29 | 72.5% [57.2%–83.9%] | 7 [6–14] | 1 [1–2] / 0 [0–2] / 1 [0–2] | 29; 5 [5–5] | 7 [6–10] | 17 |
| bypass/after07/loss-timeout | 0 | 0.0% [-0.0%–8.8%] | — | — / — / — | 0; — | — | 0 |

## Class contribution and survival

| Policy/version/class | Damage share | Kills/share | Finishes | Intercepts | Death turn | Scout early-death run share |
| --- | --- | --- | --- | --- | --- | --- |
| road/before06/melee | 772.0 / 38.8% | 72.0 / 24.5% | 72.0 | 0.0 | 9 [7–15] | 6/40 |
| road/before06/ranged | 757.0 / 38.0% | 89.0 / 30.3% | 89.0 | 0.0 | 11 [7–14] | 6/40 |
| road/before06/mobile | 462.0 / 23.2% | 133.0 / 45.2% | 133.0 | 198.0 | 8 [3–15] | 6/40 |
| road/after07/melee | 834 / 40.5% | 94 / 29.9% | 94 | 0 | 9 [6–15] | 0/40 |
| road/after07/ranged | 772 / 37.5% | 98 / 31.2% | 98 | 0 | 8 [6–11] | 0/40 |
| road/after07/mobile | 454 / 22.0% | 122 / 38.9% | 122 | 188 | 7 [4–15] | 0/40 |
| flank/before06/melee | 788.0 / 40.1% | 79.0 / 27.0% | 79.0 | 0.0 | 9.5 [6–11] | 5/40 |
| flank/before06/ranged | 713.0 / 36.3% | 105.0 / 35.8% | 105.0 | 0.0 | 9 [7–13] | 5/40 |
| flank/before06/mobile | 463.0 / 23.6% | 109.0 / 37.2% | 109.0 | 192.0 | 8 [3–14] | 5/40 |
| flank/after07/melee | 879 / 42.8% | 99 / 31.5% | 99 | 0 | 8 [6–12] | 0/40 |
| flank/after07/ranged | 784 / 38.2% | 126 / 40.1% | 126 | 0 | 10.5 [6–15] | 0/40 |
| flank/after07/mobile | 392 / 19.1% | 89 / 28.3% | 89 | 190 | 7 [4–12] | 0/40 |
| turtle/before06/melee | 768 / 42.4% | 93 / 35.1% | 93 | 0 | 11 [7–13] | 19/40 |
| turtle/before06/ranged | 603 / 33.3% | 85 / 32.1% | 85 | 0 | 8 [4–11] | 19/40 |
| turtle/before06/mobile | 440 / 24.3% | 87 / 32.8% | 87 | 183 | 6 [3–13] | 19/40 |
| turtle/after07/melee | 700 / 45.7% | 94 / 41.2% | 94 | 0 | 7 [6–13] | 17/40 |
| turtle/after07/ranged | 489 / 31.9% | 67 / 29.4% | 67 | 0 | 8 [4–13] | 17/40 |
| turtle/after07/mobile | 343 / 22.4% | 67 / 29.4% | 67 | 179 | 6 [3–13] | 17/40 |
| scout-retreat/before06/melee | 610 / 49.7% | 68 / 43.0% | 68 | 0 | 7 [4–11] | 0/40 |
| scout-retreat/before06/ranged | 480 / 39.1% | 72 / 45.6% | 72 | 0 | 8 [8–9] | 0/40 |
| scout-retreat/before06/mobile | 138 / 11.2% | 18 / 11.4% | 18 | 88 | — | 0/40 |
| scout-retreat/after07/melee | 616 / 50.2% | 73 / 44.8% | 73 | 0 | 6 [4–9] | 0/40 |
| scout-retreat/after07/ranged | 468 / 38.2% | 72 / 44.2% | 72 | 0 | 7 [7–7] | 0/40 |
| scout-retreat/after07/mobile | 142 / 11.6% | 18 / 11.0% | 18 | 114 | 6 [6–9] | 0/40 |
| leader-dash/before06/melee | 141 / 36.5% | 20 / 58.8% | 20 | 0 | 5 [4–7] | 15/40 |
| leader-dash/before06/ranged | 4 / 1.0% | 2 / 5.9% | 2 | 0 | 4 [3–5] | 15/40 |
| leader-dash/before06/mobile | 241 / 62.4% | 12 / 35.3% | 12 | 95 | 2 [2–6] | 15/40 |
| leader-dash/after07/melee | 85 / 43.4% | 2 / 50.0% | 2 | 0 | 6 [5–8] | 15/40 |
| leader-dash/after07/ranged | 2 / 1.0% | 1 / 25.0% | 1 | 0 | 4 [3–6] | 15/40 |
| leader-dash/after07/mobile | 109 / 55.6% | 1 / 25.0% | 1 | 194 | 5 [2–6] | 15/40 |
| bypass/before06/melee | 447 / 33.1% | 30 / 21.7% | 30 | 0 | 7 [7–7] | 0/40 |
| bypass/before06/ranged | 455 / 33.7% | 71 / 51.4% | 71 | 0 | 6.5 [6–8] | 0/40 |
| bypass/before06/mobile | 450 / 33.3% | 37 / 26.8% | 37 | 99 | 7 [6–8] | 0/40 |
| bypass/after07/melee | 544 / 33.7% | 56 / 30.4% | 56 | 0 | 7 [6–14] | 0/40 |
| bypass/after07/ranged | 580 / 36.0% | 87 / 47.3% | 87 | 0 | 8 [7–10] | 0/40 |
| bypass/after07/mobile | 488 / 30.3% | 41 / 22.3% | 41 | 125 | 7 [6–10] | 0/40 |

## Enemy idle by group / estimated minutes

| Policy/version | front/flank/south/reserve/rear/leader/wave idle | Eligible observed | LOS blocked actual / opportunities | Estimated median minutes / full span | Inside15–25min |
| --- | --- | --- | --- | --- | --- |
| road/before06 | 80.0/195.0/40.0/116.0/0.0/153.0/0.0 | 2127 | 0.0 / 130.0 | [17.7966437333333, 29.04664373333335] / [9.90321913333333, 35.9216437333333] | 0/40 |
| road/after07 | 80/197/40/121/0/195/0 | 2171 | 0 / 119 | [18.34447845833335, 30.34447845833335] / [9.147633625, 37.8936896666667] | 0/40 |
| flank/before06 | 80.0/184.0/40.0/122.0/0.0/156.0/0.0 | 2027 | 0.0 / 109.0 | [17.72003416666665, 29.0533675] / [9.90321913333333, 36.3383104] | 0/40 |
| flank/after07 | 80/191/40/132/0/187/0 | 2167 | 0 / 97 | [17.0944784583333, 28.261145125] / [9.147633625, 34.5603563333333] | 0/40 |
| turtle/before06 | 60/200/40/181/0/182/0 | 2211 | 0 / 253 | [15.1912328, 24.8578994666667] / [12.5184246, 33.364041] | 4/40 |
| turtle/after07 | 60/198/40/183/0/190/0 | 2019 | 0 / 227 | [13.1210560416667, 21.704389375] / [9.67223922916667, 30.761145125] | 0/40 |
| scout-retreat/before06 | 80/122/40/74/0/153/0 | 1453 | 0 / 94 | [11.7108218666667, 19.2108218666667] / [6.23041093333333, 27.3002967333333] | 1/40 |
| scout-retreat/after07 | 80/122/40/74/0/188/0 | 1623 | 0 / 88 | [11.1968448333333, 18.5301781666667] / [6.09842241666667, 31.1532061875] | 0/40 |
| leader-dash/before06 | 80/105/41/80/0/80/0 | 1231 | 0 / 69 | [7.7494177666666655, 12.66608443333335] / [7.0956164, 14.0956164] | 0/40 |
| leader-dash/after07 | 80/113/41/80/0/97/0 | 1717 | 0 / 77 | [7.647633625, 12.647633625] / [6.37302802083333, 15.1722392291667] | 0/40 |
| bypass/before06 | 0/1/40/0/0/0/0 | 633 | 0 / 103 | [4.90321913333333, 7.90321913333333] / [3.3456164, 14.3260273333333] | 0/40 |
| bypass/after07 | 0/9/40/0/0/0/0 | 925 | 0 / 95 | [5.69684483333333, 9.3635115] / [3.147633625, 14.8786005833333] | 0/40 |

Minutes are arithmetic only: living ally unit-turns ×15–25s + result turn × supplied enemy mean, /60. Read each run estimate_enemy_mean/source; after uses frozen spike06 reference1.47633625s for comparability, NOT a fresh human-time claim. No tuning toward minutes; HUMAN_PENDING. True idle retains spike06 definition; birth rest/unprocessed terminal tails excluded. LOS opportunities are phase-start in-range blocked pairs, not attempted illegal shots.

## Targets (definitions locked before tuning)

- PASS: full-route bypass0/200; partial probe has no wave-free zero-deathT6 win. Empirical probe closure, not proof against all human strategies.
- PASS: road60% within40–60%, flank67.5% within52.5–72.5%; W1 road50%,flank62.5%. Original20W1 road50%,flank70% reproduced. Naive turtle/retreat still mostly lose.
- PASS: intended-route scouts no death<T4 in80/80 (>=90%); no top damage class. FAIL: conditional scout death median7<8, flank finishing kills89<ranged126. Road scoutfinishes122 lead; scoutintercepts188/190 lead.
- PASS minimum native mean20.7/23.5ms; FAIL strict16.67ms all / worst33ms. See PERFORMANCE.md; no stable60FPS claim.
- PASS: 240 frozen06 recheck traces/commands/outcomes/deaths/class/turn metrics exactly match W1;80 W3 traces match after optimized rules. Distinct does not imply independent samples.
- Human timing, clarity, fairness, art/feel approval remain HUMAN_PENDING.

Actual uncaptured final flank1006 winT14:13normal enemy phases mean1.416251s
[0.064966–3.178392];43attacks0.606045–0.934332s,readbacks0. Dedicated crit/reduced
checks remain infield-timing.json. All are actual wall time, not AVI clock. The
40-seed estimates keep reference1.47633625s for comparability; human minutes
stillpending, no tune to this arithmetic. Strict60FPS/worst33 fails even though
minimum means pass: AI-inclusive normal16.85/worst64.28,2x17.03/worst66.80ms.
