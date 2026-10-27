# Stratified deterministic probes

Distinct traces are not independent samples; Wilson intervals describe probe counts, not human win probability.

| Policy | Wins (95% Wilson) | Bypass wins | No scout death <T4 | Distinct traces |
| --- | --- | --- | --- | --- |
| road | 60.0% [44.6%, 73.7%] | 0/40 | 100.0% | 40/40 |
| flank | 67.5% [52.0%, 79.9%] | 0/40 | 100.0% | 39/40 |
| turtle | 10.0% [4.0%, 23.1%] | 0/40 | 57.5% | 27/40 |
| scout-retreat | 5.0% [1.4%, 16.5%] | 0/40 | 100.0% | 27/40 |
| leader-dash | 10.0% [4.0%, 23.1%] | 0/40 | 62.5% | 39/40 |
| bypass | 27.5% [16.1%, 42.8%] | 0/40 | 100.0% | 28/40 |

| Policy × outcome | n | Rate [95%] | Turn median [range] | Wave engaged | Scout death turns |
| --- | --- | --- | --- | --- | --- |
| road / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| road / engaged-win | 24 | 60.0% [44.6%, 73.7%] | {'median': 14.0, 'min': 12, 'max': 15} | 24 | {'median': 7, 'min': 4, 'max': 13} |
| road / loss-Thoma | 7 | 17.5% [8.7%, 32.0%] | {'median': 7, 'min': 6, 'max': 15} | 7 | {'median': 6.0, 'min': 4, 'max': 10} |
| road / loss-timeout | 9 | 22.5% [12.3%, 37.5%] | {'median': 16, 'min': 16, 'max': 16} | 9 | {'median': 7.0, 'min': 4, 'max': 15} |
| flank / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| flank / engaged-win | 27 | 67.5% [52.0%, 79.9%] | {'median': 14, 'min': 11, 'max': 15} | 27 | {'median': 7, 'min': 4, 'max': 12} |
| flank / loss-Thoma | 7 | 17.5% [8.7%, 32.0%] | {'median': 9, 'min': 6, 'max': 9} | 7 | {'median': 6.0, 'min': 4, 'max': 7} |
| flank / loss-timeout | 6 | 15.0% [7.1%, 29.1%] | {'median': 16.0, 'min': 16, 'max': 16} | 6 | {'median': 7, 'min': 6, 'max': 11} |
| turtle / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| turtle / engaged-win | 4 | 10.0% [4.0%, 23.1%] | {'median': 14.0, 'min': 14, 'max': 15} | 4 | {'median': 7, 'min': 3, 'max': 10} |
| turtle / loss-Thoma | 28 | 70.0% [54.6%, 81.9%] | {'median': 7.0, 'min': 7, 'max': 13} | 28 | {'median': 6, 'min': 3, 'max': 9} |
| turtle / loss-timeout | 8 | 20.0% [10.5%, 34.8%] | {'median': 16.0, 'min': 16, 'max': 16} | 8 | {'median': 6.0, 'min': 4, 'max': 13} |
| scout-retreat / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| scout-retreat / engaged-win | 2 | 5.0% [1.4%, 16.5%] | {'median': 13.0, 'min': 13, 'max': 13} | 2 | {'median': 9.0, 'min': 9, 'max': 9} |
| scout-retreat / loss-Thoma | 38 | 95.0% [83.5%, 98.6%] | {'median': 8.0, 'min': 4, 'max': 9} | 29 | {'median': 6.0, 'min': 6, 'max': 6} |
| scout-retreat / loss-timeout | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| leader-dash / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| leader-dash / engaged-win | 4 | 10.0% [4.0%, 23.1%] | {'median': 6.0, 'min': 6, 'max': 7} | 4 | {'median': 5, 'min': 5, 'max': 5} |
| leader-dash / loss-Thoma | 36 | 90.0% [76.9%, 96.0%] | {'median': 6.0, 'min': 5, 'max': 8} | 36 | {'median': 4.0, 'min': 2, 'max': 6} |
| leader-dash / loss-timeout | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| bypass / bypass-win | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
| bypass / engaged-win | 11 | 27.5% [16.1%, 42.8%] | {'median': 10, 'min': 9, 'max': 14} | 11 | {'median': 7.0, 'min': 6, 'max': 10} |
| bypass / loss-Thoma | 29 | 72.5% [57.2%, 83.9%] | {'median': 7, 'min': 6, 'max': 14} | 29 | {'median': 7, 'min': 6, 'max': 10} |
| bypass / loss-timeout | 0 | 0.0% [-0.0%, 8.8%] | None | 0 | None |
