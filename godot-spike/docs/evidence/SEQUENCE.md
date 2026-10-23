# Setup (a): four timed rendered frames

These are unedited 1280×720 viewport readbacks from one normal attack. Timestamps
are milliseconds after dispatching replay, including dispatch latency and GPU
readback; the attack itself measured **0.926972 s** from wind-up to input unlock.

| Time | Frame |
| ---: | --- |
| 239.552 ms | [Anticipation / lunge begins](sequence-anticipation.png) |
| 356.743 ms | [Contact, white flash and local hitstop](hit-frame.png) |
| 589.626 ms | [Knockback has reached the next cell](knockback-end.png) |
| 1007.102 ms | [Recovered; replay input available](sequence-recovered.png) |

Four PNGs total **3,895,706 bytes** (3.72 MiB). Required contact/end screenshots are
reused here rather than duplicated. This small sampled sequence records staging
and endpoints; it does not substitute for watching the full animation in Godot.
Exact phases, positions, measurements and write results: [capture-report.json](capture-report.json).
