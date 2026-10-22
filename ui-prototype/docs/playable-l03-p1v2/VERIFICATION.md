# P1v2 readability verification

Baseline: `63a1f112cc7a331aee20bf37e82b935e57cbd2e8`, on
`codex/playable-l03-research`. Owner requested only P1v2, a 60-minute cap,
no pull, unchanged rules, and A on this screen only. Work began
2026-10-22 18:09:04 Asia/Taipei; delivery time is recorded in the handoff.

The original large silhouettes and inline names obscured the winch cluster.
Sprites now use a 26-unit clipped viewport, feet anchored at tile centres,
with animated foot-position depth sorting and a stable horizontal tie-break.
Only tile polygons receive input. A full name, side, coordinate and action
status appear in an HTML strip on hover, keyboard focus or inspection; its
reserved text footprint prevents hover from moving the board at 200% text.
Allied circular bases and enemy diamond bases also differ in colour.

Inspecting an enemy or an already-used ally selects it for inspection only;
it cannot move or Wait. `data-p1v-inspected` records this separately from the
actionable `data-p1v-selected`. No rule result is changed by inspection.
No source art was modified or created; no new dependencies or animation rigs.

## Actual checks

Commands ran at the repository root. `command-results.json` retains real
command output and individual exit codes. Browser reports bind source/art
SHA-256, screenshots, exact rule states, browser binding and capture times.

| Command | Exit | Result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 checks, original traces byte-identical |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 stance/bounds/absence checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 opt-in/default/witness checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v2` | 0 | 26 browser checks; outputs isolated in `p1v-regression/` |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs` | 0 | 9 readability checks, `after-results.json` |
| `npm run build --prefix ui-prototype` | 0 | TypeScript and Vite, 49 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | 0 | 13 protected planning files, no Actions/root LICENSE |
| `git diff --check` | 0 | No whitespace errors |

The new browser cases recreate the initial map-column pair, Lace (1,3) /
Thoma (1,4), and the actual first three P0 success-trace moves yielding the
winch cluster (1,1)/(2,2)/(3,3). At both sizes they click all five units at
five interior tile points (100 pointer checks). They assert the hit element,
inspection identity, action availability and unchanged rule state. They also
check visible names, bounding-box separation from every clipped sprite,
topmost label hit tests, all sprite pairs, exact foot anchors and draw order.
Further cases cover keyboard/Esc, hover exit, 200% text without layout shift,
and actual interpolated foot sorting during an animated legal move.

Nested SVG `getBoundingClientRect()` includes the underlying **unclipped atlas**.
The test therefore transforms the actual nested SVG viewport into screen
coordinates. This bounds all visible sprite pixels rather than counting
invisible neighbouring atlas columns as overlap.

P1v assertions were retained. Four obsolete sprite-click selectors now target
their owning tiles, matching the explicitly requested input contract. The
26-case suite still checks full animated/skipped wins and losses, Retry,
legal ranges, waiting, keyboard, repeated inputs, Reduced Motion, exit during
animation, 200% text, 390px fallback, original L03 and both legacy story flows.

Protected diff against baseline is empty for `rules.ts`, `AnimatedActor.tsx`,
`L03Preview.tsx`, `ArtGate.tsx`, package/lockfile, source art, all P0/P0b/P0c
fixtures and `docs/story/`. A remains opt-in through the existing screen's
`survivalTurns: 6`; no P2 or story changes.

## Running-screen captures

Before captures were made before editing source, using `--before` (exit 0).
After captures use the same rule states; inspection UI differs as expected.
All are real browser screenshots, not generated images. No older evidence
was overwritten. `before-results.json` / `after-results.json` retain hashes.

| Size / state | Before | After |
| --- | --- | --- |
| 1280×720, winch | [before](before-1280x720-winch.png) | [after](after-1280x720-winch.png) |
| 1920×1080, winch | [before](before-1920x1080-winch.png) | [after](after-1920x1080-winch.png) |
| 1280×720, column | [before](before-1280x720-column.png) | [after](after-1280x720-column.png) |
| 1920×1080, column | [before](before-1920x1080-column.png) | [after](after-1920x1080-column.png) |
| 200% text | — | [720p](after-1280x720-text-200.png), [1080p](after-1920x1080-text-200.png) |

Agent visually inspected the 720p column/winch/200% and 1080p winch captures.
Human playtesting remains **HUMAN_PENDING**. The smaller figures trade detail
for separation, especially at 720p. A remains **THIN**; no claim of commercial
art quality, tactical depth, 3–5 minute human completion, screen-reader or
gamepad acceptance. Names are intentionally shown for one inspected/hovered
unit at a time. At 200% text the page uses vertical scrolling.

## Failed attempts and corrections

- Initial new browser run: exit 1, false sprite overlap from unclipped SVG
  atlas bounds; corrected the measurement to the clipped viewport.
- Expanded 200% case: exit 1, changing placeholder/name wrapping moved the
  board under the pointer. Fixed the reserved text footprint; a new assertion
  now checks identical board bounds and the correct inspected unit.
- Both failed reports remain locally in
  `scratch/playable-l03-p1v2-browser/attempt-{1,2}-results.json`.
- Initial `git fetch origin`: exit 1, sandbox could not write FETCH_HEAD;
  approved retry exit 0, no unexpected commits on this task branch. No pull.
- Local Python alpha-bound probe: exit 1 in sandbox; approved same-interpreter
  retry exit 0. Ally alpha bottoms are 710/710/711, enemy 871; used to crop
  transparent padding, without editing PNGs.

## Scoped implementation review

`ui-design` and `typography-audit` were applied to these changed controls and
labels only. Keyboard-operable tiles retain visible focus and Space/arrows;
decorative sprites are aria-hidden and unit/side names live on the tile.
Labels use the existing font at 1rem, unitless inherited line-height 1.5,
and actual 200% checks. Existing landmarker typography and page type scale
were not redesigned. No full accessibility compliance is claimed.

Browser launch inventory: test-only Chrome, verified canonical absolute path,
byte count and SHA-256 before importing Playwright or creating a profile;
allowlisted environment, repo-local profile, only loopback page traffic.
The existing outer Node/npm/Git launch remains ambient; no whole-toolchain
trust claim or new trust settings. Existing hooks are exercised by actual
commits/push, not substituted with hook-installation evidence.
