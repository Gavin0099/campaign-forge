# P1v6 feedback and winch — execution verification

2026-10-23, Asia/Taipei. Presentation proposal; **HUMAN_PENDING** for human
playtest and Owner art acceptance. Work is on `codex/playable-l03-research`,
starting at Owner-named `fc266cb`. Latest instruction is **commit only**.

The five priorities are implemented. Feedback now consumes the original event
order on the same 230ms path-step clock as movement. A move's dust starts at
its final step, a block at its intent, and winch feedback at positive progress.
`finish()` still commits the rule state exactly once. The final landing shares
the finish boundary; it is not postponed until after settlement, and no extra
frame or effect lifetime is added to the input lock. Earlier landings occur
while the original turn state is still committed. This boundary detail matters
when interpreting the request that dust appear before the turn finishes.

## Commands and results

Run from the repository root. Existing verified Node, Python and Chrome were
used, without installing packages. The local Vite server ran on
`http://127.0.0.1:5183/`; browser traffic to other origins was blocked.

| Command | Exit | Result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 original pure-rule checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 original checks; trace/witness replay |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 original checks; opt-in variants |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v6-feedback.mjs` | 0 | 2 assertion groups: timeline and counterfactual contact |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v4 --p1v5 --p1v6` | 0 | 26 browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v4 --p1v5 --p1v6` | 0 | 9 browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v3-browser.mjs --p1v5 --p1v6` | 0 | 9 browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v4-browser.mjs --p1v5 --p1v6` | 0 | 9 browser checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v5-browser.mjs --p1v6` | 0 | All 14 original feedback checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v6-browser.mjs` | 0 | 12 new browser checks |
| `npm run build --prefix ui-prototype` | 0 | TypeScript + Vite; 51 modules |
| `python scripts/validate_ui_scope.py` | 0 | 13 protected planning files; no Actions or root LICENSE |
| `python scripts/record_governance_checks.py` | 0 | 13 isolated lifecycle replay tests; scope/typecheck/Vite all 0 |
| `node ui-prototype/tests/verify-p1v6-evidence.mjs` | 0 | 79 browser checks, 50 capture hashes, 66 source bindings |
| `git diff --check` | 0 | No whitespace errors |
| `git diff fc266cb --exit-code -- ui-prototype/src/playable-l03/rules.ts ui-prototype/package.json ui-prototype/package-lock.json docs/story README.md PLAN.md SLICES.md docs/DECISIONS.md docs/EXECUTION.md` | 0 | Rules, dependencies and protected story unchanged |

107 game checks = 26 original pure checks + 2 new pure assertion groups +
79 browser checks. The 13 governance replay tests are separate. Replay is
not a native platform callback or complete automatic-governance acceptance.
No governing script, hook trust or global configuration was changed.

`command-results.json` and the seven `.log` files record real command exits
and output. PowerShell logs were losslessly transcoded to UTF-8/LF; JSON source
manifests and the exported governance receipt use Git's required LF before
source binding. The two browser suites that bind those manifests were rerun.
`evidence-audit.json` binds the command record, logs and governance receipt.

Old browser harness edits only add a P1v6 evidence destination and the imported
presentation module to source bindings. No selector or behavioral assertion
was weakened. Existing P1v5 evidence and all original asset PNGs remain intact.

## New behavior verified

- Timeline tests cover stable order at shared boundaries, one landing per move,
  positive progress after preceding movement, empty/zero-step handling and
  input purity. Browser MutationObserver records show two distinct enemy
  landings at their actual destination cells. First landing retains turn 1's
  original rule state; final landing is on the commit boundary.
- At each blocked intent, preceding move endpoints are reconstructed without
  committing rule state. The queried enemy is placed first in a copy for the
  pure resolver, so earlier enemies do not move twice. Removing Thoma opens
  the real blocked knight's route. An incidental adjacent ally across the
  disconnected river does not open a route and earns no spark. Contact must
  be adjacent to the stationary enemy and uniquely confirmed; distant or
  ambiguous obstructions receive no invented contact spark/recoil.
- Each arrival has its own cell and expiry, rather than replacing one global
  last mover. Dust has no pointer input. Static broken-chain markers stay at
  enemy feet in preview, resolution, rest, skip and Reduced Motion.
- Four painted winch frames and two rope states load from the new atlases;
  the geometric wheel, rope path and warning ellipse are absent. Ember paint
  on the fourth frame supplies the persistent 2/3 warning. Every transient
  effect is suppressed in skip/reduced mode; changing the preference between
  landings cancels future cues and commits only the original result once.
- Original regressions cover 1280×720, 1920×1080, 200% text, the 390px fallback,
  keyboard/Space/arrows/Esc/Enter, invalid/duplicate input, interruption,
  Retry, both legacy story choices, absence/deployment, move/skill preview,
  cancel/confirm and return to campaign. They remain automated evidence.

## Actual execution captures

These are unmodified browser PNGs at **1280×720**, not generated mockups:

- `1280x720-landing-1-knight-1.png`
- `1280x720-landing-2-knight-2.png`
- `1280x720-winch-turn-00.png` through `1280x720-winch-turn-03.png`
- `1280x720-warning-2-of-3.png`
- `1280x720-blocked-marker-preview.png`
- `1280x720-confirmed-block-spark.png`

The four winch images are a short continuous live compositor sequence. Chrome
streams PNGs while requestAnimationFrame records the actual CSS frame intervals
and painted taut-rope source. Each selected PNG's frame-swap timestamp lies
inside its recorded interval for index 0, 1, 2 or 3; the PNG bytes are unchanged.
Production timing was not slowed. Each dust screenshot uses a separate real replay so screenshot
encoding cannot obscure observation of the next 180ms event. The complete
two-mover timing assertion uses one uninterrupted enemy phase, independently
of screenshot timing. Both-size regression captures are in the five
`p1v*-regression/` directories.

Rendered review inspected the complete frame sequence, both dust captures,
warning and block views. The chain sign is distinct from an X, has a dark
outline plus light broken links and a redundant 受阻 label, and receives no
input. Typography review was scoped to the new board label: it uses the
existing system Chinese sans fallback, avoids case/transformation issues,
and is a diagram annotation rather than body copy. Main UI remains rem-sized
and original 200% text checks pass. No new typeface or font download.

## Assets, failed attempts and limits

Built-in **image_gen** produced two accepted original transparent atlases:
`public/art/l03-p1v6/winch-frames.png` (2172×724) and
`public/art/l03-p1v6/rope-states.png` (1159×1358). Exact prompts, references,
date, dimensions and SHA-256 are in `art-prompts.json` / `art-manifest.json`.
Only the existing original P1v4 props and battlefield were supplied as visual
references. Non-destructive SVG crops align generated padding and footings.
No generated art was rejected for style; no `*-attempt-NN.png` art is omitted.

Three verification attempts are deliberately retained:

1. `attempts/attempt-01/`: test exit 1, missed second short dust while parallel
   browser suites were capturing. The original report, first screenshot and
   timeout screenshot remain. The fix records mount order continuously and
   captures dust on independent replays; it does not slow effects or weaken
   the per-phase order/state assertions.
2. `attempts/attempt-02/`: automated report exit 0, but visual inspection
   **FAIL** found the SVG viewport's warning drop-shadow exposing adjacent
   atlas frames. Original report and defective warning/turn screenshots stay
   here. `eefce15` moves the filter to the image inside an explicitly clipped
   viewport. New assertions cover clip overflow and filter placement; actual
   replacement screenshots show one winch. All affected suites were rerun.
3. `attempts/attempt-03/`: browser report exit 0, stricter evidence verifier
   exit **1** because sequential screenshot encoding crossed from turn-B to
   jerk before its metadata read. `6d87c20` was mistakenly committed after
   that failed check and is **superseded as verification evidence** by the
   following correction commit. The original report, mismatched turn image,
   stale audit and actual verifier exit/log are preserved. The harness now
   streams compositor PNGs continuously and selects by frame-swap timestamps
   inside measured live CSS intervals. The frame-index assertion stays strict;
   no animation speed or rule code was changed. The corrected audit passes.

Early shell probes also encountered sandbox Python lookup and PowerShell
native-string quoting failures; the final file-based recorder used the
verified installed interpreter and produced the successful exits above.

The small 64×58 scene-unit prop and painterly four-frame motion still need
Owner judgment for readability and weight. The ember warning is restrained;
the header also retains the clear 2/3 warning. No skeletal animation, sound,
new hit/shove rule, full engine, commercial art approval, human playtest,
S4/story decision, PR, merge, deployment, Actions or push is claimed.
