# P0 west-bank hold proof

Question: can legal repositioning change enemy interference at the west-bank
winch enough to turn a reproducible loss into a win?

Keep this isolated rules module if P0 acceptance 1–6 pass. Stop and report if
it is unsolvable or the 60-minute timebox expires. This is a small module to
evaluate further, not production combat. Human fun/keep remains untested.

`initialState()` creates the fixed five-unit deployment. `command()` validates
one move per ally per turn (orthogonal, up to three steps), `resolve(state,
expectedTurn)` atomically settles the enemy phase and objective, and retry is
allowed only after a result. Pass the displayed turn to reject stale commands.
Only events describe presentation; consumers must adopt the returned state.
Inputs are never mutated. The rules have no React, timers, RNG or I/O.

One MapDef reuses the existing 11×9 terrain rows. The winch is (2,1). Both
route modes use the same fixed PoC deployment; all allies stay west. Open
breaks bridge cells (4,4)/(5,4); sealed allows the wagon-to-exit corridor.
Sealed is **map reachability only**, with no escort resolution or branch win.

Minimal original PoC rules, all provisional: two initial knights advance at
most three cells toward an empty winch-adjacent tile, using shortest paths
with fixed north/west/east/south ties. Each knight already adjacent at enemy
phase start adds one progress; arrival gives the player a reaction turn.
Three progress loses; surviving five turns wins, with failure checked first.
The player interferes by occupying approach tiles; there is no attack, damage,
support, reinforcement, boat simulation or official rules implementation.
`blockAlliedPassage: true` is the default: every living unit blocks passage.
False permits allied transit only; occupied destinations and enemy transit
remain forbidden. This flag does not settle the future passing rule.

The reviewed spec is a design input; P0 deliberately proves only its starting
hold loop with minimal blocking, rather than implementing the full encounter.
QR-11 (open gate's dominant reward/cost) remains unresolved. No rewards,
K1 costs, narrative, original L03Preview or ArtGate were changed.

Run from repository root:

```powershell
node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs
```

The test checks committed success/failure/retry traces byte for byte. To
explicitly regenerate fixtures after an authorized rules change, append
`--write-traces`. Tests record machine evidence only, not human playtest.

## P0c opt-in verification

No experiment is enabled by default. Pass `p0c` alongside the existing
`blockAlliedPassage` flag to `initialState('open', config)`:

| Experiment | `p0c` options |
| --- | --- |
| A | `{ survivalTurns: 6 }` |
| B | `{ requiredHoldTurns: 1 }` |
| C | `{ thomaStartsWest: true }` |
| B+ | `{ requiredHoldTurns: 2 }` or `{ requiredHoldTurns: 3 }` |

Hold means a living ally is orthogonally adjacent to (2,1) at the end of
enemy resolution, with progress below 3. At the deadline the last N ends
must all qualify; a gap resets the streak. The ally may change between
turns. Missing the hold requirement loses at the deadline; progress 3
still loses immediately. Hold history is serialized only when requested.
Retry retains the experiment and resets its history. Horizons are 5 or 6;
hold N is an integer from 0 (off) to the selected horizon.

Question: which option removes cheap waiting wins? Keep the experiment
and evidence isolated, never adopt it as default. For this 45-minute P0c,
CHEESE means a full-party win with at most one command, or a two-command
hold/rush witness; THIN means another verified win without that cheap
witness in the tested spaces, with depth still unproved. OK needs further
tactical evidence. No win found is UNSOLVABLE within the tested bounds,
never a successful fix or a proof of global impossibility.

Run `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c-search.mjs`
to recompute and byte-check the comparison JSON, and
`node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs`
for objective boundary tests and witness replay. Search uses the real
`command`/`resolve` API. See the report for exact counting, caps and
multi-move bounds; these are machine experiments, not human win rates.
