# spike-04 evidence index

Option C: separate playable24×18 scene;160×94.5px diamonds,96px figures.
Art/numbers are PLACEHOLDER / spike test values. Automated engineering evidence
is separate from Gavin's HUMAN_PENDING full-battle/feel/art judgment.

| Evidence | Files |
| --- | --- |
| Hit-feel03→04 | [normal/crit stacked contact±8 strip](hitfeel/impact-strip-spike03-vs-spike04.png), [nine setup timings](hitfeel/timing.json); native frames/stills/AVIs in `hitfeel/spike03-normal`, `spike04-normal`, `spike03-crit`, `spike04-crit` |
| Deployment | [720p](deployment.png), [native1080p](deployment-1080.png), [move confirmed](move-confirmed.png), [F1](debug-overlay.png) |
| Combat | [first contact](first-contact.png), [ranged](ranged-attack.png), [melee](melee-hit.png), [enemy phase](enemy-phase.png), [win12](win.png) |
| Navigation | [scroll](scroll.png), [overview](overview.png), [mid-battle overview](mid-battle-overview.png), [camera strip](camera-follow-return-strip.png), [samples](camera-sequence.json) |
| Wave | [warning4](reinforcement-warning.png), [arrival5](reinforcement-arrival.png); first eligible enemy action6 |
| Movies | [MOVIE.md](MOVIE.md), [operating AVI](scroll-select-move-attack-60fps.avi), [enemy AVI](enemy-phase-60fps.avi), [header/hash index](movie-index.json) |
| Pacing | [PACING.md](PACING.md), [road](autoplay/road.json), [flank](autoplay/flank.json), [turtle](autoplay/turtle.json), [initial layout](autoplay/initial/), [continuous scene telemetry](runtime-battle.json) |
| Performance | [PERFORMANCE.md](PERFORMANCE.md), [raw samples](performance.json), [unrecorded attacks](runtime-attack-timings.json) |
| Verification | [GUT123/123,10,310 assertions](test-run.log), [exits](w7-exit-codes.json), [audit](audit.json), [source hashes](source-hashes.json), [Git scope](git-scope.json), [changed paths](changed-paths.txt), [stat](diff-stat.txt) |
| Decisions/failures | [WORK.md](WORK.md), `attempts/`, historical `w1`–`w6` logs; final logs listed by audit tool |
| Art provenance | [SOURCES.md](../../../art/bigmap/SOURCES.md), [generator](../../../tools/make_field_art.py); original source frames untouched |

Capture JSON records engine, renderer, actual dimensions and individual checks.
`stills` is a continuous automated battle. The operating sequence explicitly
stages combat from a reachable road trace; it is not a continuous playthrough.
Rejected logs remain visible even when an earlier process exited0 with errors.
PowerShell logs normalize UTF8/terminal noise/trailing whitespace; error content
and outcomes remain. No human playtest is claimed.

Five skills read only, no installation/code/asset copying, at
`gamedev-skills/awesome-gamedev-agent-skills` commit
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`:
[prototype-fast](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/workflows/prototype-fast/SKILL.md),
[level-design](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/level-design/SKILL.md),
[game-ai](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ai/SKILL.md),
[game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md),
[game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md).
Methods applied: keep/discard test, route/objective visibility, understandable
deterministic AI, preview/confirm feedback, restrained readable impact. Owner's
15–25min target supersedes the generic checklist3–5min bar.
