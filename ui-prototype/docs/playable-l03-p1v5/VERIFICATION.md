# P1v5 battlefield interaction feedback

Owner brief: `docs/tasks/playable-l03-P1v5-feedback.md`. Started 2026-10-23
00:57:41 Asia/Taipei, with a 60-minute cap, from clean
`codex/playable-l03-research@3c95f0e`. No pull. Final delivery time and SHAs
are recorded in the branch handoff and final reply.

All four priorities are implemented and separately checkpointed:

| Step | Checkpoint | Visible result |
| --- | --- | --- |
| 1 | `f3aba38` | 500ms winch jerk/wheel turn and taut rope shake, 700ms new-pip flash and numeric pop, static red warning plus optional pulse at 2/3, 450ms defeat fade |
| 2 | `0483147` | Existing blocked-intent event: 300ms enemy recoil, 450ms dust, 240ms visual-layer shake (3 scene px maximum), 600ms status pop; adjacent ally gets a 350ms clash spark |
| 3 | `c3a65ea` | Flowing intent arrow and pulsing exact predicted destination; a contributor already beside the winch points to the winch |
| 4 | `435c886` | Pointer/keyboard hover glow, 280ms move confirmation and 180ms arrival dust; impact-time phase banner moves above the action |

Every timer owns presentation only. No extra input lock, extra resolution,
damage, push, or cell displacement. Static intent outlines and the 2/3 warning
remain available with Reduced Motion or Skip Animation; transient feedback
does not mount. Toggling either during feedback cancels it without replay.
At the failure threshold the existing modal and Retry focus activate immediately;
its visual fade adds no gameplay delay. The original rules can increment 2→4;
the view retains the actual number and original `>=3` defeat condition.

There are **no hit/shove events or HP in this ruleset**. The implemented impact
is a presentation of a real blocked intent, with a status pop rather than an
invented damage number. Physical shove and damage feedback therefore remain
N/A until such mechanics receive separate authorization. No new bitmap,
image generation, engine, dependency, sound, story, or final art decision.

## Executed verification

Exact commands, exit codes, and failed attempts: [command-results.json](command-results.json).

| Check | Exit | Count / evidence |
| --- | --- | --- |
| P0 / P0b / P0c | 0 / 0 / 0 | 8 / 9 / 9; original traces byte-identical |
| P1v / P1v2 / P1v3 / P1v4 browser regressions | 0 / 0 / 0 / 0 | 26 / 9 / 9 / 9; original behavioural assertions retained |
| P1v5 browser | 0 | 14; actual state compared to pure commands on every move/turn |
| `npm run build --prefix ui-prototype` | 0 | TypeScript and Vite |
| `scripts/validate_ui_scope.py` via installed Python | 0 | 13 protected planning files |
| `node ui-prototype/tests/verify-p1v5-evidence.mjs` | 0 | 67 browser checks, 41 screenshot hashes, 52 current source bindings |
| Protected-path diff / whitespace diff | 0 / 0 | rules, original art, dependencies, story, root PLAN/SLICES unchanged |
| `scripts/record_governance_checks.py` via installed Python | 0 | lifecycle-tests, scope, typecheck, Vite all exit 0; current receipt in `artifacts/governance-native-acceptance.json` |

**93 game checks** = 26 pure + 53 existing browser + 14 new browser.
The old harness changes only add a `--p1v5` evidence destination, preserving
earlier evidence and all behavioural assertions. Both 1280×720 and 1920×1080,
200% text, 390px fallback, keyboard/Esc/Retry, both legacy story branches and
absence flow, animated/skipped victory/defeat, invalid/duplicate input and
animation interruption remain covered. New feedback-specific captures are 720p.

`attempts/step4-initial-results.json` preserves an exit-1 test. Dust and the
arrival group originally shared a sibling React key, leaving stale dust DOM
after timeout; separate keys fixed it. The diagnostic rerun also exited 1;
its screenshot is `attempts/step4-diagnosis-failure.png`. Final cleanup and
mid-feedback preference assertions pass. This was fixed before step 4 commit.

No human playtest was performed: **HUMAN_PENDING**. Browser execution and model
inspection do not establish comfort, readability for a human, commercial art
approval, or native governance lifecycle completion.
The existing governance recorder was run after the milestone to keep its
source-bound receipt current. This is local isolated command replay, not a
natural platform callback or a request to end the session. No governance code
or global trust setting was changed.

## Actual execution screenshots

These are unmodified browser captures, not image-generation mockups. Short
effects were sampled during ordinary playback, without slowing production
timers or injecting game state. Source and capture hashes are in the reports.

- [Winch interference](1280x720-winch-interference.png)
- [Single-contributor 1/3 pop](1280x720-winch-1-of-3.png)
- [Persistent 2/3 warning](1280x720-warning-2-of-3.png)
- [Body block and spark](1280x720-body-block.png)
- [Enemy intent pulse](1280x720-intent-pulse.png)
- [Hover glow](1280x720-hover-glow.png)
- [Move confirmation](1280x720-move-confirm.png)
- [Defeat transition](1280x720-defeat.png)

Regression captures and reports are in `p1v-regression/`, `p1v2-regression/`,
`p1v3-regression/`, and `p1v4-regression/`. Their screenshots include both
resolutions. Full-screen model inspection confirmed that moving the phase
banner above the impact leaves the body-block spark visible; Owner judgement
of the strength and readability of these effects is still pending.
