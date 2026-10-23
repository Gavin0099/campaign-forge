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

## Verification status

Step 1 build: `npm run build --prefix ui-prototype`, exit 0.
Step 2 pure checks: P1v6 feedback (2 groups), P1v7 helper (3 groups), exit 0.
Full regression, measured browser checks and 1280×720 evidence pending the
verification commit. Human playtest and Owner art acceptance: HUMAN_PENDING.
