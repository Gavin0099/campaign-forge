# P2: enemy responses (opt-in rules experiment)

This is a rules/test/evidence slice only. No UI, formal rule adoption, HP,
attack, story, art, dependency, P1v edit or other-worktree change.

The mechanism passes its causal re-decision witness, but the encounter remains
**CHEESE**: a cheaper two-command rear delay wins without reacting to a
telegraph. The default rules stay unchanged. Do not promote P2 on this result.

## Contract

Use `initialState('open', { blockAlliedPassage: true,
p0c: { survivalTurns: 6 }, enemyBehaviour: 'p2', detourThreshold: 1 })`.
The test config explicitly selects A's six-turn horizon. Omitting P2 retains
the original five-turn default (or the caller's existing P0c configuration).
The threshold is a nonnegative safe integer; the comparison is strictly `>`.

Both behaviours emit `enemy-intent` with `behaviour`, `intent`, `reason`,
`targetTile`, `plannedPath`, and `action`. This new event type avoids changing
the old `intent` union consumed by P1v. UI integration is a later slice.

- Target interference uses the existing shortest open approach to a winch
  neighbor. Its target is the winch; its path is the exact movement this phase.
  Only enemies adjacent at phase start contribute progress. No open step means
  an explicit wait. Movement/path ties remain N/W/E/S.
- Hunt the weak point compares that path with a shortest path ignoring living
  allies, while other enemies remain obstacles. No open route, or a route more
  than the threshold longer than the relaxed route, is pressure. The first ally
  on the relaxed route is the named blocker. This copies the geometry idea of
  this repo's P0d swap; it does not import P0d's immediate execution rule.
- First pressure phase: emit `blocked`, remember blocker identity and tile,
  and approach up to three cells, stopping before that blocker. No forced move.
- Following phase: if pressure and that blocker persist within three steps,
  emit `prepare-breakout` and wait. Store the exact enemy path, ally identity,
  ally origin, ally destination (the preceding path cell), and preparation turn.
  If still farther away, continue approaching and remain `blocked`.
- Next phase: swap only if the saved target, origin, path occupancy, knight
  origin, and immediately preceding preparation turn still match. Emit a
  `breakout` with exactly that saved plan. No damage; alive flags are unchanged.
- If the player moves/removes the target, changes the blocking ally, or blocks
  the advertised path, emit cancellation with a reason. A new threat must start
  at `blocked` again. There is no same-phase re-plan-and-swap. A disappeared
  pre-telegraph pressure emits `pressure-cleared` and resumes interference.

For `prepare-breakout`, `plannedPath` is the current phase's one-cell wait;
`plan.path` is the advertised next-phase path. `plan.to` is the ally's advertised
landing tile. Cancellation is an informational wait event followed by the new
decision; it does not consume an extra hidden action or skip the normal decision.
Knights act in existing unit order against the current occupancy; objective
contribution is still sampled at phase start. Loss wins ties at the deadline.

## Search and verdict

The full-party search harness was copied from this project's
`origin/codex/playable-l03-p0d` at
`2dc92b6d5ec22e9e4e48bb82db995adeb111e58a`, with the P2 config, memory-aware cache
key and causal witness checks added. No merge. Unneeded solo/duo probing was
removed. The old P0b legal-command enumeration and P0c replay code are unchanged.

Costs below are **voluntarily moved allies / commands / path tiles**. Ranking
is commands, then allies, then tiles. All three allies remain on the board.
W/L counts candidate placements or command sequences, not human win rates.
Spaces overlap and must not be summed.

| A+P2, six turns | Wins | Losses | Minimum cost | Cheapest ties requiring a telegraph reaction |
| --- | ---: | ---: | --- | ---: |
| T1 placement then wait | 88 | 6,708 | 2 / 2 / 5 | 0 / 1 |
| At most one total command | 0 | 210 | None | N/A |
| At most two total commands, at most two/turn | 80 | 24,705 | 1 / 2 / 2 | 0 / 1 |
| At most three total commands, at most two/turn | 14,220 | 1,905,088 | 1 / 2 / 2 | 0 / 1 |

The multi-command enumerations have no beam, state or transition cap. The
100,000-entry wait-tail cache limits memory only; uncached tails are computed,
never discarded. Its key includes turn, positions, status, progress, hold and
P2 pressure/telegraph memory. Only wait tails are cached, so per-turn moved flags
cannot affect a cached continuation. T1 enumeration deduplicates placements and
retains their lowest-cost command order; it can include all three T1 commands.

Cheapest overall: T1 Karen `(2,5) -> (3,5)`; T2 Karen `(3,5) -> (2,5)`;
wait through T6. It wins at progress 1. This is not a response to a preparation
telegraph. It is cheaper than the original A/A+D rear delay.

Original cheapest A/A+D rear delay still wins: T1 Karen `(2,5) -> (1,5)`,
Lace `(1,3) -> (3,4)`; T2 Karen `-> (2,5)`; wait. Cost 2/3/5, progress 2.

The extra preparation wait weakens pressure in some routes. Increasing the
number of enemy states has not fixed the inexpensive wait exploit. The verdict
is therefore **CHEESE**, despite the local causal gate below. No THIN/OK claim.

## Key-gate witness

This separate directed probe starts with the existing four-command P0 defense.
It checks the 24 legal single-command responses on its telegraphed turn (none
pass the causal gate), then ordered two-command responses, stopping at the sixth
pair. It is not a complete six-command search; do not add it to the table.

| Turn | Player command / information |
| --- | --- |
| T1 | Lace `(1,3) -> (1,1)`; Thoma `(1,4) -> (2,2)`; Karen `(2,5) -> (3,3)` |
| T2 | Karen `(3,3) -> (3,1)` |
| T3 | Wait. Knight-1 prepares to swap Lace `(1,1) -> (1,2)`; knight-2 prepares to swap Karen `(3,1) -> (3,2)`. No swap yet. |
| T4 | React in this order: Karen `(3,1) -> (1,0)`, then Lace `(1,1) -> (3,1)`. Both old telegraphs cancel because their targets left. |
| T5–T6 | Wait. Win at progress 2. |

Actual cost is **3 allies / 6 commands / 15 path tiles**; the T4 reaction adds
two commands and five tiles. The three comparisons all replay legally:

| Counterfactual | Outcome at T6 | Progress |
| --- | --- | ---: |
| P2 enabled, perform the T4 reaction | Win | 2 |
| P2 enabled, omit the T4 reaction | Lose; both exact advertised swaps execute at T4 | 4 |
| P2 disabled (A only), omit the T4 reaction | Win | 2 |

This establishes a tested re-decision caused by P2 on this prefix, rather than
merely an action after T1. It does not make reacting globally necessary: the
cheapest overall win still avoids it. Full states, commands, events and the
baseline counterfactual are in `witnesses.jsonl`; `search-results.json` contains
the replayable inputs and all table metrics.

## Verification and limits

See `VERIFICATION.md` and `command-results.json` for actual exits and hashes.
Run the P2 search before P2 tests. Search output has no timestamps and is checked
byte-for-byte on two final runs. The P2 tests also compare its <=2 enumerator
with the independent existing P0c enumerator, validate intent/action equality,
freeze inputs, and cover blocking, detour threshold, preparation, exact swap,
vacating/replacing/absent targets, progress, retry, and a deterministic placement
sample. Default P0/P0b/P0c/P1v source/evidence remain unchanged.

`p1v-regression/` captures the unchanged P1v page running this rules module
with P2 disabled, including 720p/1080p and text/keyboard checks. They are real
browser captures, not P2 UI evidence. The original P1v fixtures were restored
byte-for-byte after the unchanged harness ran. No full P2 UI or human playtest
was performed; no unrestricted battle search or party-size balance is claimed.
