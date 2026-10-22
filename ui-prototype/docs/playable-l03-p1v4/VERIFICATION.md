# P1v4 art pass — verification

The repeated ground diamonds are replaced by one hand-painted ferry landscape.
The winch, broken bridge ends and wagon use a transparent painted atlas, and
the second knight has a distinct portrait. Idle grid lines are hidden; range,
hover, focus, selected cells and the existing intent arrows remain readable.

The requested 1.3-tile height **failed the retained overlap test**. The final
common figure viewport is 52 / 52 = **1.00 tile**, the geometric maximum for
the same-screen-column winch cluster. Actual opaque figure height is
**0.960–0.979 tile**. This exception is explicit; automated checks do not
constitute Owner art approval or a human playtest.

## Scope and time

- Owner-named baseline: `codex/playable-l03-research@f1e0ab627e92e68c726c3cdef47c08735cd70831`.
- Status was clean; Owner confirmed no other session in this worktree.
- First clock: **2026-10-22 20:34:40 Asia/Taipei**. Budget: 120 minutes maximum.
  Evidence/documentation checkpoint: **21:03:24**, 28m44s elapsed.
  Final Git SHAs, push outcomes and total elapsed are in the handoff/final report.
- No pull, main write/merge, PR, stash, forced push, dependency installation,
  or access to `scratch/p2` / `scratch/p0d`. No sub-agents spawned.
- Shared edits: `ui-prototype/PLAN.md` and `memory/01_active_task.md`,
  under Codex-owned locks and with required commit trailers. No-pull instruction
  overrides the shared-file default pull step. Task DONE is not SessionEnd.

## Generated assets

All are built-in image_gen originals, saved under `public/art/l03-p1v4/`.
Original PNG bytes are retained. Full prompts and dates are in
[art-prompts.json](../art-prompts.json); full SHA-256 and dimensions in
[art-manifest.json](../art-manifest.json).

| File | Result | SHA-256 |
| --- | --- | --- |
| `battlefield-attempt-01.png` | **REJECTED**: river too wide, bridge layout shifted | `dceaf33a86eda498f3a44c82be53bc5c1d1347c8a7e69bfcc3bd6bf792f4530b` |
| `battlefield.png` | Used: guide-constrained continuous landscape | `8c42a5e46952a85db4bce232ac8b3463090a1ddc0f3bf65b25bcea6031e713c5` |
| `props.png` | Used: alpha winch / bridge end / wagon atlas | `8f9e678bd048cffe67c9d1f384b6cb0a3ae53cf4d306fa5262019787ac0d16cf` |
| `knight-2-portrait.png` | Used: distinct open-face knight portrait | `419984a8c18c6a25341857a61ca29e3cc15137c88a0eae2368bc7717dde58019` |

The source-authored `layout-guide.svg/png` is a geometry diagram used as an
image-generation reference, not a game screenshot. Its framing is inverted
in the SVG image rectangle so the existing rule-grid projection stays exact.
The rejected original is retained for audit; it is not referenced by runtime.

Existing `l03-party-v1.png` and `l03-enemies-v1.png` supply the figures.
All original art paths are unchanged against the baseline. No commercial game
imagery or third-party art/code was copied.

## Commands

From the repo root, with Node 24's built-in TypeScript stripping:

| Command | Exit | Evidence |
| --- | --- | --- |
| `node ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 checks, original traces byte-identical |
| `node ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 checks |
| `node ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 checks |
| `node ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v4` | 0 | 26 checks; [report](p1v-regression/browser-results.json) |
| `node ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v4` | 0 | 9 checks; [report](p1v2-regression/after-results.json) |
| `node ui-prototype/tests/playable-l03-p1v3-browser.mjs --p1v4` | 0 | 9 checks; [report](p1v3-regression/visual-results.json) |
| `node ui-prototype/tests/playable-l03-p1v4-browser.mjs` | 0 | 9 art/geometry checks; [report](art-results.json) |
| `npm run build --prefix ui-prototype` | 0 | TypeScript / Vite, 50 modules |
| Existing Python: `scripts/validate_ui_scope.py` | 0 | 13 protected planning files; approved sandbox escalation |
| `git diff --check` | 0 | No whitespace errors |
| Baseline protected-path and original-art diff checks | 0 | Rules, old screens, dependencies, fixtures, original art and story unchanged |

79 final checks = 26 pure + 53 browser. [Command ledger](command-results.json)
records actual results, the scale failure and setup failures. The server used
`node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5183 --strictPort`
from `ui-prototype/`. Browser tests verify the existing Chrome absolute path,
byte length and SHA before launching, use repository-local profiles and an
allowlisted environment, and block non-local browser requests. No claim is
made that ambient npm/Git shell launches form a hardened security boundary.

Existing browser assertions and selectors were retained. The only changes
to the three earlier runners route their evidence into P1v4 and include the
presentation source hash; prior evidence is not overwritten.

P1v regression still covers both old story choices, absent/solo deployment,
dialogue log, move/skill previews, Esc, confirmation, result to campaign,
animated/skipped wins/losses, repeated inputs, mid-animation interruptions,
Retry focus, keyboard, 200% text and the 390px fallback. P1v2 retains its 100
real pointer hits, overlap, foot anchoring and depth-order checks. P1v3 retains
path parity, arrival, phase/gauges, debug and Reduced Motion assertions.

New checks verify one ground image/no texture patterns, four painted prop
instances, five unique portrait signatures, hidden idle grid, all 99 exact
cell-centre hits, all 18 impassable river cells, actual alpha-based figure
height, transparent prop background samples and every generated image hash.

## Screenshot index

[Comparison viewer](comparison.html) pairs archived P1v3 Before captures with
new P1v4 captures. Every screenshot below comes from the running browser;
generated art originals and the geometry guide are kept separate.

For each `SIZE` = `1280x720` or `1920x1080`:

| State | Path relative to this directory |
| --- | --- |
| Start | `after-SIZE-start.png` |
| Selected / exact path preview | `after-SIZE-selected-path-preview.png` |
| Enemy inspection / intent | `after-SIZE-enemy-intent.png` |
| Enemy turn banner | `p1v3-regression/after-SIZE-enemy-turn-banner.png` |
| Ally turn banner | `p1v3-regression/after-SIZE-ally-turn-banner.png` |
| Victory | `p1v-regression/SIZE-victory.png` |
| Defeat | `p1v-regression/SIZE-defeat.png` |
| Cluster / column / enlarged text | `p1v2-regression/after-SIZE-{winch,column,text-200}.png` |
| Grid alignment diagnostic | `after-SIZE-DIAGNOSTIC-grid-alignment.png` |

Diagnostic images deliberately reveal all cell polygons via test-only CSS;
normal gameplay hides the idle grid. Capture reports store hashes, exact
states and viewport sizes. Model visual inspection is not human playtest.

## Rejected attempts and limits

- First battlefield generation rejected: wide river did not fit the logical
  two-column channel. Second generation uses a precise layout reference.
- 67.6-unit figures (1.3 tiles) failed P1v2 with `lace/thoma` overlap,
  exit 1. Original [failure report](rejected-scale-1.3/after-results.json)
  and [screenshot](rejected-scale-1.3/failure.png) retained.
  The diagonal winch cluster's 52-unit foot spacing independently limits
  zero-overlap height. No numeric tolerance was enlarged to fake compliance.
- Final viewport ratio 1.00; opaque art 0.960–0.979. Party art is 4% taller;
  tighter knight crops make their visible art about 24.7% taller. See
  [STYLE](STYLE.md) and exact measurements in [art-results](art-results.json).
- Both knight battlefield bodies still share the original closed-helmet
  figure. The second portrait is distinct but its open helmet does not yet
  have a matching body variant.
- Painterly bank edges and foliage are approximate decoration, not pixel-perfect
  navigation meshes. The exact polygons/rules still control all input and movement.
- Optional extra idle/attack frames skipped. Existing single-frame movement
  bob/slide, 180ms landing and 900ms phase feedback remain. No new attacks,
  damage, sound, full animation system or engine.
- Human playtest, 3–5 minute pacing, 720p recognition and Owner art approval:
  **HUMAN_PENDING**. The earlier A experiment remains THIN.
- No screen-reader/gamepad trial, formal accessibility certification, GPU
  performance benchmark, formal story/rules or native governance completion
  claimed. Governance code and trust configuration were not changed.
