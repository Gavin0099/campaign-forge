# Stratified deterministic probes

Distinct traces are not independent samples; Wilson intervals describe probe counts, not human win probability.

| Policy | Wins (95% Wilson) | Bypass wins | No scout death <T4 | Distinct traces |
| --- | --- | --- | --- | --- |
| road | 60.0% [44.6%, 73.7%] | 0/40 | 100.0% | 40/40 |
| flank | 67.5% [52.0%, 79.9%] | 0/40 | 100.0% | 39/40 |

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
