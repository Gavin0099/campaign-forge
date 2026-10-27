# Stratified deterministic probes

Distinct traces are not independent samples; Wilson intervals describe probe counts, not human win probability.

| Policy | Wins (95% Wilson) | Bypass wins | No scout death <T4 | Distinct traces |
| --- | --- | --- | --- | --- |
| road | 50.0% [35.2%, 64.8%] | 0/40 | 85.0% | 40/40 |
| flank | 62.5% [47.0%, 75.8%] | 1/40 | 87.5% | 40/40 |
| turtle | 12.5% [5.5%, 26.1%] | 0/40 | 52.5% | 28/40 |
| scout-retreat | 0.0% [-0.0%, 8.8%] | 0/40 | 100.0% | 24/40 |
| leader-dash | 85.0% [70.9%, 92.9%] | 33/40 | 62.5% | 40/40 |
| bypass | 95.0% [83.5%, 98.6%] | 3/40 | 100.0% | 20/40 |

| Policy × outcome | n | Rate [95%] | Turn median [range] | Wave engaged | Scout death turns |
| --- | --- | --- | --- | --- | --- |
| road / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| road / engaged-win | 20 | 50.0% [35.2%, 64.8%] | {'median': 14.0, 'min': 10.0, 'max': 15.0} | 20 | {'median': 8.0, 'min': 3.0, 'max': 11.0} |
| road / loss-Thoma | 8 | 20.0% [10.5%, 34.8%] | {'median': 8.0, 'min': 7.0, 'max': 15.0} | 8 | {'median': 7.0, 'min': 3.0, 'max': 13.0} |
| road / loss-timeout | 12 | 30.0% [18.1%, 45.4%] | {'median': 16.0, 'min': 16.0, 'max': 16.0} | 12 | {'median': 9.0, 'min': 3.0, 'max': 15.0} |
| flank / bypass-win | 1 | 2.5% [0.4%, 12.9%] | {'median': 7, 'min': 7, 'max': 7} | 0 | {'median': 5, 'min': 5, 'max': 5} |
| flank / engaged-win | 24 | 60.0% [44.6%, 73.7%] | {'median': 13.5, 'min': 7.0, 'max': 15.0} | 24 | {'median': 8, 'min': 3, 'max': 14.0} |
| flank / loss-Thoma | 4 | 10.0% [4.0%, 23.1%] | {'median': 7.0, 'min': 7, 'max': 8} | 3 | {'median': 5.0, 'min': 3, 'max': 7} |
| flank / loss-timeout | 11 | 27.5% [16.1%, 42.8%] | {'median': 16, 'min': 16.0, 'max': 16.0} | 11 | {'median': 10.0, 'min': 3, 'max': 14} |
| turtle / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| turtle / engaged-win | 5 | 12.5% [5.5%, 26.1%] | {'median': 14, 'min': 13, 'max': 15} | 5 | {'median': 10, 'min': 8, 'max': 10} |
| turtle / loss-Thoma | 21 | 52.5% [37.5%, 67.1%] | {'median': 11, 'min': 9, 'max': 13} | 21 | {'median': 6, 'min': 3, 'max': 11} |
| turtle / loss-timeout | 14 | 35.0% [22.1%, 50.5%] | {'median': 16.0, 'min': 16, 'max': 16} | 14 | {'median': 4, 'min': 3, 'max': 13} |
| scout-retreat / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| scout-retreat / engaged-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| scout-retreat / loss-Thoma | 40 | 100.0% [91.2%, 100.0%] | {'median': 8.0, 'min': 4, 'max': 11} | 29 | None |
| scout-retreat / loss-timeout | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| leader-dash / bypass-win | 33 | 82.5% [68.0%, 91.3%] | {'median': 6, 'min': 5, 'max': 6} | 0 | {'median': 2, 'min': 2, 'max': 4} |
| leader-dash / engaged-win | 1 | 2.5% [0.4%, 12.9%] | {'median': 7, 'min': 7, 'max': 7} | 1 | {'median': 5.0, 'min': 4, 'max': 6} |
| leader-dash / loss-Thoma | 6 | 15.0% [7.1%, 29.1%] | {'median': 6.0, 'min': 5, 'max': 7} | 4 | {'median': 4.0, 'min': 2, 'max': 4} |
| leader-dash / loss-timeout | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| bypass / bypass-win | 3 | 7.5% [2.6%, 19.9%] | {'median': 6, 'min': 6, 'max': 6} | 0 | None |
| bypass / engaged-win | 35 | 87.5% [73.9%, 94.5%] | {'median': 7, 'min': 7, 'max': 10} | 35 | {'median': 7, 'min': 6, 'max': 8} |
| bypass / loss-Thoma | 2 | 5.0% [1.4%, 16.5%] | {'median': 7.0, 'min': 7, 'max': 7} | 2 | {'median': 7.0, 'min': 7, 'max': 7} |
| bypass / loss-timeout | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
