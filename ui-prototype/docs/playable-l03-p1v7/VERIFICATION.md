# P1v7 — execution verification

2026-10-23, Asia/Taipei. Owner-named base `67c4dd8` on
`codex/playable-l03-research`. Presentation only; commit only, no push.

## Accepted last-landing boundary (step 3)

Gavin accepted the final landing sharing `finish()`. Earlier landings can
appear during playback; the last landing starts at the same boundary as the
single rule-state commit. Its 180 ms dust lifetime does not extend the input
lock. No pause, turn wait, or extra animation frame is added. This is an
accepted known limit, not a claim that every landing precedes settlement.

Zero-step cues instead have an independent 750 ms lifetime after `finish()`;
they do not own `pending` or `busy`. Normal move timing stays 230 ms per step.
Reduced Motion and skip commit directly with only static prediction markers.

## Commands and real results

Run from the repo root, except Vite, which runs from `ui-prototype/`:
`node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5183 --strictPort`.
URL: `http://127.0.0.1:5183/?scene=playable-l03`. The existing Chrome binding
is verified before launch; profiles stay in this repo and remote requests
are blocked. No dependencies, art, rules, or event order were changed.

| Command | Exit | Result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 original pure checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 original pure checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 original pure checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v6-feedback.mjs` | 0 | 2 original feedback groups |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v7-feedback.mjs` | 0 | 3 new helper groups |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v4 --p1v5 --p1v6 --p1v7` | 0 | 26 original browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v4 --p1v5 --p1v6 --p1v7` | 0 | 9 original browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v3-browser.mjs --p1v5 --p1v6 --p1v7` | 0 | 9 original browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v4-browser.mjs --p1v5 --p1v6 --p1v7` | 0 | 9 original browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v5-browser.mjs --p1v6 --p1v7` | 0 | 14 original browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v6-browser.mjs --p1v7` | 0 | 12 original browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v7-browser.mjs` | 0 | 15 new browser checks |
| `npm run build --prefix ui-prototype` | 0 | TypeScript + Vite, 51 modules |
| `python scripts/validate_ui_scope.py` (repo-bound Python 3.12) | 0 | 13 protected planning files; no Actions/root LICENSE |
| `node ui-prototype/tests/verify-p1v7-evidence.mjs` | 0 | 125 game checks, 55 capture hashes, 73 source bindings |
| `git diff --check` | 0 | No whitespace errors |
| `git diff 67c4dd8 --exit-code -- ui-prototype/src/playable-l03/rules.ts ui-prototype/package.json ui-prototype/package-lock.json docs/story README.md PLAN.md SLICES.md docs/DECISIONS.md docs/EXECUTION.md` | 0 | Rules, dependencies and protected story unchanged |

125 = all 107 existing checks (26 rule + 2 feedback + 79 browser), plus
3 helper groups and 15 new browser checks. Command receipts and logs are here;
the first browser command's actual exit is also in its source-bound report.
The first build ran after step 1; the recorded final build includes step 3.
No governing program or hook changed, so governance replay is not rerun or
claimed as new native callback evidence.

All existing behavioural assertions remain. One P1v6 marker-count assertion
was moved from immediately after End Turn to immediately before it: its old
placement required the premature marker this brief explicitly removes.
The preview count, busy phase, confirmed Thoma clash, final marker and exact
state/outcome assertions are retained. P1v7 adds strict absence through the
earlier move and appearance at the reached event. The other legacy harness
edits only add `--p1v7` evidence routing, preserving historical evidence.

## Measured feedback and input

For the same six-step enemy phase, the actual P1v6 component at `c980e5a`
and the current component each ran three times in the same browser/server:

| Version | Lock duration samples (ms) | Mean (ms) |
| --- | --- | --- |
| P1v6 | 1412.9, 1398.0, 1393.0 | 1401.3 |
| P1v7 | 1407.8, 1425.7, 1387.4 | 1407.0 |

Both use six 230 ms steps, plus real RAF scheduling. The measured mean
difference is 5.7 ms; no timer or wait was added to normal turns.
For reproduction, export the baseline first in PowerShell:
`git show c980e5a:ui-prototype/src/playable-l03/PlayableL03.tsx | Set-Content -Encoding utf8 scratch/p1v7-baseline-component.tsx`.
The harness serves that component through a temporary sibling module with
unchanged relative imports, records its SHA-256, and removes it after closing
the browser. No old production files or rules are checked out or restored.

The zero-step winch and block labels had opacity 1 at **366.0 ms** and
**355.7 ms** after their state commits. Both committed with `busy=false`
and End Turn enabled. A real selection dispatched **0.1 ms** after the
committed DOM was observed became selected **4.7 ms** after commit.
The cue's independent 750 ms expiry leaves the settled state unchanged.
New selection clears it, new resolution replaces its serial, and Retry
clears it with no delayed commit or stale effect. Skip/Reduced Motion both
before resolution and toggled during a cue mount no future transient effects.

The late-block witness has a knight move before the other knight's blocked
intent. Its marker stays absent through that move; the block is at the final
movement boundary, so the after-event screenshot also shows the committed
next turn, with no invented pause. The converse witness has knight 1 block
first while knight 2 moves later: the marker is visible **during playback**
at the enemy's visual cell, then disappears when the new state's prediction
changes to approach. Pure tests cover inclusive event indexing, multiple
blocked enemies and input/set purity.

## Actual 1280×720 screenshots

- `1280x720-zero-step-winch-after-commit.png`: painted cue, 2/3 and enabled input.
- `1280x720-zero-step-block-after-commit.png`: block label, broken chain, enabled input.
- `1280x720-synced-marker-before-event.png`: earlier enemy moving, marker absent.
- `1280x720-synced-marker-after-event.png`: reached block at (2,3), new turn settled.
- `1280x720-synced-marker-during-later-move.png`: reached block at (1,5) while input is still locked for the later mover.

All are unmodified Chrome execution screenshots, visually inspected at native
size. Capture metadata, exact rule states and SHA-256 are in
`feedback-results.json`. The six regression subdirectories retain all 50
legacy captures, including 1080p, 720p, keyboard, text zoom and actual winch
compositor frames. The source/capture audit checks all 55 images and verifies
the four existing winch frames against their measured live CSS intervals.

## Attempts and acceptance limits

`attempts/attempt-01/` retains browser exit 1 from starting Vite at the repo
root rather than the UI directory (HTTP navigation failure). The server was
stopped and restarted at the correct root. `attempts/attempt-02/` retains
browser exit 1 from deleting the baseline module during a run, which caused
Vite to reload the page. Cleanup now happens after closing the browser.
Both fixes affect verification setup only; production timing was not slowed.
An initial shell probe could not access Python inside the sandbox and did
not execute the validator. The final scope command used the verified bound
interpreter outside the sandbox and actually exited 0.

No requested implementation is skipped. The final landing boundary above is
Owner-accepted; no added wait is proposed. Human playtest, weight/readability
judgment and commercial art acceptance remain **HUMAN_PENDING**. No new art,
story, game outcome, dependency, engine, S4, push, merge, PR, Actions or
deployment. Task DONE is not SessionEnd.
