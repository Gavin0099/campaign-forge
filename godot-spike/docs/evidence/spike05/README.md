# spike-05 evidence index

Automated operator evidence, not a human playtest or Owner art approval.
24×18 only; test values, no formal story/rules decision. Local commits only.

| Evidence | Contents / limits |
| --- | --- |
| [WORK](WORK.md) | W1–W8 decisions, keep/discard criteria and historical test-pin migrations |
| [baseline](baseline/BASELINE.md) | Unchanged spike04 road win12 / flank lose7 / turtle lose3 reproduced; original and enhanced JSON retained |
| [PACING](PACING.md) | Before/after idle by group, contact/wave, class damage/kills/deaths, blocked shots and estimates; all measured initial-deployment policies now lose |
| [PERFORMANCE](PERFORMANCE.md) | Unrecorded 720p scroll/normal/2× means and worst frames, small regressions, 40 runtime attack timings |
| [MOVIE](MOVIE.md) | Actual Godot60FPS AVI + native-frame PNG strips; ffmpeg unavailable; movie time is not performance |
| [Hit comparison](hitfeel/impact-strip-spike04-vs-spike05.png) | Normal/crit spike04 vs05, contact±8; four AVI sets and individual contact stills under hitfeel/ |
| [Skirmish timing](hitfeel/timing.json) | Three setups × normal/crit/Reduced Motion; same HP/cells/contact; nine no-readback measurements |
| [Enemy phase strip](enemy-phase-60fps-strip.png) | Actual normal-speed road phase, advancing front |
| [Ranged sequence strip](select-move-ranged-60fps-strip.png) | Parsed select → move/cancel → confirm → ranged preview/confirm → contact/return; isolated fixture, original stats/map |
| [Deployment](deployment.png), [1080p](deployment-1080.png) | Native resolution render, no generated mockup |
| [Overview](overview.png), [dense labels](dense-labels.png), [edge](edge-safe.png) | Deterministic declutter, visible selected complete actor; manual exploration can leave unrelated actors offscreen |
| [Blocked](los-blocked.png), [cover](cover-preview.png), [V threat](threat-los.png) | Actual field terrain, shared LOS/preview/threat rules |
| [Interception](reinforcement-interception.png) | Isolated pursuit fixture, original entry cells/born turn; full-roster bypass JSON separately records first engagement7 |
| [Melee](field-melee-hit.png), [lose](lose.png) | Continuous initial-deployment road runtime, loses8 |
| [Staged terminal win](win-staged-terminal.png) | Lethal adjacent fixture only; **not** evidence of initial-deployment whole-field winnability |
| [Capture checks](capture-qa.json) and capture-*.json | Actual shots/dimensions, parsed interactions, overlaps/safe actors; `capture-source-hashes.json` freezes W6 runtime sources |
| [GUT](test-run.log), [exits](w7-exit-codes.json) | 147/147, 11,492 assertions, import0/GUT0; old123 retained with documented behavior-pin migrations |
| [Scope](git-scope.json), [changed paths](changed-paths.txt), [diff stat](diff-stat.txt) | Base905c0ce through pre-containing-commit working tree; brief is only outside-project change and predates W1 |
| [Audit](audit.json), [sources](source-hashes.json) | Offline audit and SHA256 working bytes / normalized-LF; excludes self-hash and audit stdout log; refreshed with W8 docs |

Failed attempt is preserved at `attempts/capture-intercept-full-probe-failed.json` + log:
exit1 because full probe first contact was an ally shooting the wave, not the requested
enemy wave strike. Final isolated pursuit capture exits0; no failure was silently relabelled.
`w6-exit-codes.json` retains this distinction. W2 intermediate policies live under w2/.
Logs are encoding/ANSI/trailing-whitespace normalized only, preserving errors and results.

Idle table recomputes **both** W1 and W6 using observed actor phases, excluding
unprocessed actors after terminal. W1 original JSON remains unchanged. Old `idle_turns`
meant no reachable target even when moving, so the old72 figure is not true inactivity.
Pacing estimates assume15–25 seconds per living ally; no human time was measured.
Road estimate10.0–16.3min and losses7/6 do not establish the15–25min target.

Read-only skill methods used (pinned source, not installed; no code/art copied):

- [prototype-fast](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/workflows/prototype-fast/SKILL.md): upfront keep/discard, smallest testable change.
- [level-design](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/level-design/SKILL.md): retain map/routes, report failed strategies instead of relaxing stats.
- [game-ai](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ai/SKILL.md): explicit deterministic states and focus, pure rules/events.
- [game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md): shared legality, safe actors and marker/plate readability checks.
- [game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md): preserved contact layers, before/after strips and input-ready timing.

Local external-executable-trust-audit skill: explicit Owner-provided Godot/Python
paths; offline Python tools launch no processes/network. No PATH fallback, global trust
change, or claim of complete executable trust-root hardening. Sandbox Godot resolution
and shared Git metadata required escalation; no alternate worktree was modified.
Human feel/readability, blind road/flank/turtle, overall winnability and commercial art
remain HUMAN_PENDING. See the spike-05 HANDOFF for open questions and resource checks.
