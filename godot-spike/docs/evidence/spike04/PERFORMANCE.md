# Measured 720p performance

AMD Radeon 780M; Godot4.7.2 GL Compatibility.
GL Compatibility, native720p, no fixed FPS/movie/readbacks; inter-process-frame wall times incl UI/rules, excludes startup; capped60FPS pacing is included.

| Operation | Samples | Mean ms | Worst ms |
| --- | ---: | ---: | ---: |
| scroll | 59 | 19.666 | 42.897 |
| enemy-normal | 86 | 22.776 | 30.366 |
| enemy-fast | 54 | 22.521 | 32.135 |

Enemy turn2 wall duration: normal 2.188s, 2× 1.433s.

Inter-frame samples include pacing/UI/rules and OS scheduling; this is a short local
run, not a GPU benchmark or steady-60 guarantee. Worst frames exceed16.67ms.
Raw samples: [performance.json](performance.json); clean exit0: `w6-performance-clean.log`.
Earlier probes/logs remain; the verbose probe identified an unfinished placeholder
audio playback at shutdown. Final capture waits for it and frees streams.

| Unrecorded normal attack | n | Mean wall s | Max wall s | Max process s |
| --- | ---: | ---: | ---: | ---: |
| melee | 17 | 0.869 | 0.893 | 0.987 |
| ranged | 10 | 0.770 | 0.801 | 0.906 |
| mobile | 5 | 0.854 | 0.877 | 0.980 |
| knight | 14 | 0.630 | 0.653 | 0.661 |
| leader | 2 | 0.655 | 0.662 | 0.644 |

Strike-to-input-ready includes presentation and return; hard ceiling1.7s, target1.2s.
GUT separately checks crit/Reduced Motion and all Skirmish setups. Movie wall time
includes encoding, so use process seconds there and these unrecorded wall samples.
