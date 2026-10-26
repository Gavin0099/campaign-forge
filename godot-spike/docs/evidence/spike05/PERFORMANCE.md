# Measured performance — 720p, AMD Radeon 780M

Native720p, GL Compatibility, capped60FPS; inter-process wall time incl pacing/UI/rules. No fixed FPS, movie or readbacks during samples; startup excluded.

| Operation | Before mean/worst ms | After n | After mean/worst ms | Mean delta |
| --- | --- | ---: | --- | ---: |
| scroll | 19.666/42.897 | 90 | 20.703/30.588 | +1.037ms |
| enemy-normal | 22.776/30.366 | 46 | 23.509/33.983 | +0.733ms |
| enemy-fast | 22.521/32.135 | 30 | 23.124/29.606 | +0.603ms |

Positive deltas are measured regressions in these short samples; scheduling, camera
safety and label work are included. This does not isolate AI cost or prove causation.
No steady60FPS claim. Captured movies are separate and are NOT performance samples.

Enemy turn2 presentation: normal 1.336s, 2× 0.951s.
Continuous road run normal enemy mean 3.456164s across 8 phases; includes terminal partial phase.

| Unrecorded runtime attacks | n | Mean / max wall s | Max process s |
| --- | ---: | --- | ---: |
| knight | 17 | 0.651/0.668 | 0.671 |
| melee | 10 | 0.867/0.892 | 0.997 |
| mobile | 7 | 0.864/0.902 | 0.985 |
| ranged | 6 | 0.781/0.823 | 0.898 |

One runtime melee contact PNG readback is included in these attack wall samples;
the perf mode has none. Input readiness≤1.7s verified; target≤1.2s is reported per row.
Dummy audio was driven, not auditioned. HUMAN_PENDING.
