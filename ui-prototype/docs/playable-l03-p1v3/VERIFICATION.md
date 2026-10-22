# P1v3 visual pass — verification

The screen now uses the existing painted material and character atlases in a
consistent moss/slate/brass frame. The original board had pale flat tiles,
26-unit figures and text-only side lists. The new view adds visible banks,
deeper projection, 50-unit figures, portrait cards, gauges and movement/phase
feedback. These changes improve visual structure; passing tests does not
establish commercial art quality or human recognition. **HUMAN_PENDING**.

Base: `codex/playable-l03-research@7319ef03923a6838375e95a6a16f1de4c42c9d11`.
Owner-confirmed clean/exclusive worktree. First recorded clock:
2026-10-22 19:05:58 Asia/Taipei. Budget: 90 minutes maximum, not a claim of
90 minutes spent. Final actual time and Git outcomes are in the handoff.

## Commands and results

Run from the repo root. The existing Vite server was launched locally with
`node ui-prototype/node_modules/vite/bin/vite.js ui-prototype --host 127.0.0.1 --port 5183 --strictPort`.
Chrome executable identity was verified against the existing repo binding;
profiles live in this worktree's scratch directories. Browser requests outside
the local origin are blocked. No dependencies were installed.

| Command | Exit | Evidence |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 checks, committed traces byte-identical |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v3 --before` | 0 | 26 baseline checks; real Before captures before source changes |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v3` | 0 | 26 checks; [report](p1v-regression/browser-results.json) |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v3` | 0 | 9 checks; [report](p1v2-regression/after-results.json) |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v3-browser.mjs` | 0 | 9 checks; [report](visual-results.json) |
| `npm run build --prefix ui-prototype` | 0 | TypeScript + Vite, 50 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | 0 | 13 planning files protected; approved sandbox retry |
| `git diff --check` | 0 | No whitespace errors |
| `git diff --quiet 7319ef0 -- <protected paths>` | 0 | Rules, source PNGs, old screens, dependencies, fixtures and story unchanged |

Full executed output and exit codes: [command-results.json](command-results.json).
Browser reports include source SHA-256, capture SHA-256, exact states and errors.
The final checks total 70 (26 pure + 44 browser), excluding the baseline run.
P1v2 retains every assertion, including nonoverlapping figure viewports, foot
anchors, depth order and 100 actual pointer checks. Only the P1v winch text
selector was adjusted for the deliberately hidden coordinates; a new test
also verifies the coordinate toggle. No behavioral assertion was removed.

The original P1v regression still covers both old story choices, absent/solo
deployment, dialogue log, movement/skill preview/confirm/Esc, result to campaign,
animated/skipped wins and losses, repeated input, mid-animation skip/reduced
motion, unmount, Retry focus, keyboard, 200% text and the 390px fallback.

New checks confirm the preview equals the unchanged command's exact path,
mouse and keyboard both produce it, Esc removes it, the landing feedback
fires and disappears, turn banners follow real playback, gauges match state,
debug mode is presentation-only, and Reduced Motion disables all new effects.

## Screenshot index

Open [comparison.html](comparison.html) to compare seven states at either size.
All PNGs were captured from the running app, never generated or composited.

For each `SIZE` = `1280x720` and `1920x1080`:

| State | Before | After |
| --- | --- | --- |
| Start | `before/SIZE-start.png` | `p1v-regression/SIZE-start.png` |
| Selected move range | `before/SIZE-move-range.png` | `p1v-regression/SIZE-move-range.png` |
| Enemy intent | `before/SIZE-intent.png` | `p1v-regression/SIZE-intent.png` |
| Mid-animation | `before/SIZE-mid-animation.png` | `p1v-regression/SIZE-mid-animation.png` |
| Turn transition | `before/SIZE-turn-banner.png` | `p1v-regression/SIZE-turn-banner.png` |
| Victory | `before/SIZE-victory.png` | `p1v-regression/SIZE-victory.png` |
| Defeat | `before/SIZE-defeat.png` | `p1v-regression/SIZE-defeat.png` |

There was no banner in the baseline; its transition capture honestly shows
that absence. Dynamic captures use the same logical replay point, not a claim
of identical animation timing. Additional `after-SIZE-path-preview.png`,
`after-SIZE-enemy-turn-banner.png` and `after-SIZE-ally-turn-banner.png` show
the new feedback. `p1v2-regression/` contains the winch cluster, column and
200% name captures. The model inspected real screenshots at both sizes,
including selected/path, clustered figures, phase, success and failure.

## Failed attempts preserved

- First P1v run exit 1: 720p sidebar pushed the controls below the viewport.
  Reduced portrait/panel padding; preserved [report](attempts/01-layout-failure.json).
- Second P1v run exit 1: 1080p controls extended 10px below the viewport.
  Corrected large-screen board height; preserved [report](attempts/02-1080-layout-failure.json).
- First new P1v3 run exit 1: selector polling missed the 180ms arrival effect.
  Started frame-by-frame observation before the keyboard move. The actual
  effect was not lengthened to satisfy the harness; preserved
  [report](attempts/03-arrival-observer-timeout.json).
- Initial sandbox fetch could not write `.git/FETCH_HEAD`; approved fetch
  exited 0, without pull. Initial Python invocation was inaccessible in the
  sandbox (exit 1); the same existing validator outside that boundary exited 0.

## Known limits and scope

- Literal 1.2–1.5 full diamond-height figures conflict with the retained zero
  overlap assertion. Kept 50-unit figures / 52-unit nearest vertical spacing;
  see [STYLE](STYLE.md). Portraits improve face reading, but human recognition
  and commercial art acceptance remain pending.
- Single-frame standing artwork still slides/bobs during movement. No new
  skeletal animation, attacks, sound, hit-stop, 3D engine or lighting system.
- Winch/bridge/wagon chassis are geometric supporting props. The provided
  `landmarks-v3.png` contains different objects, so it was not misrepresented
  as a winch. Tree/cargo art comes from `props-v2.png`.
- Repeated terrain texture and the symmetric board edges remain visible.
  No custom map painting or newly generated assets were authorized.
- P0c A remains THIN and scoped to this screen. P2 is untouched. No deeper AI,
  rules, narrative, formal story selection or S4 claim. Existing original
  assets remain proposals, with no new license or commercial clearance claim.
- No human playtest, gamepad or screen-reader trial, GPU/FPS benchmark, full
  WCAG certification, Owner art approval or natural lifecycle callback claimed.
- Shared edits: `ui-prototype/PLAN.md`, `memory/01_active_task.md`, both under
  Codex-owned locks. User's no-pull instruction overrides the shared-file
  default pull step. No daily memory edit; delivery is not SessionEnd.
