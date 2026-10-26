# Native720p performance on this PC

Native720p GL Compatibility max60FPS, no fixed clock/movie/readbacks or concurrent Godot. Wall frame intervals incl UI/rules/pacing. Wave-engaging reached phase; spike05 sampled T2 so workloads differ.

| Operation | spike05 mean/worst ms | spike06 n | mean/worst ms | Mean delta |
| --- | --- | ---: | --- | --- |
| scroll | 20.703/30.588 | 54 | 34.007/46.443 | +13.304 |
| enemy-normal | 23.509/33.983 | 70 | 34.053/47.043 | +10.544 |
| enemy-fast | 23.124/29.606 | 43 | 34.585/45.572 | +11.461 |

Uncaptured continuous flank normal enemy mean1.476336s across12 phases. Normal and2× phase samples use the same reached wave state. Positive frame deltas are observed regressions, not isolated causation; scene workload differs from spike05 T2. No steady60FPS claim.

| Real-time uncaptured attack | n | mean / max wall s | max process s |
| --- | ---: | --- | ---: |
| knight | 12 | 0.637/0.673 | 0.661 |
| melee | 14 | 0.906/0.944 | 1.011 |
| mobile | 3 | 0.909/0.914 | 1.010 |
| ranged | 12 | 0.783/0.839 | 0.931 |

Separate screenshot/AVI proof runs are not performance measurements. Fixed60 movie-clock wall duration can exceed gameplay timings; hitfeel/timing.json retains both clocks. Dummy audio driven, not auditioned. Human comfort/pacing pending.
