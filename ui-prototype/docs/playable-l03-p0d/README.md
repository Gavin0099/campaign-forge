# P0d: final bounded pressure experiment

Owner authorized only `docs/tasks/playable-l03-P0d-pressure.md`, in the separate
`codex/playable-l03-p0d` worktree starting at `13a6e17`, for at most 60 minutes.
The parallel P1v session and its worktree are outside this task. Nothing imports
these experiments into the UI. This is a rules-verification result, not a
playable battle, adopted combat design, story decision or human playtest.

## Pre-implementation question and stop criteria

Can any tested option avoid having every cheapest strategy be first-turn
deployment followed by waiting? Keep the measurements and reproducible
witnesses, not a new default. CHEESE means a full-party win with at most two
commands. A solvable option is THIN unless it meets all the OK gates:

- No T1-only win, or its minimum costs at least three commands, three moved
  allies and eight path tiles (an explicit operational definition of costly).
- At least two lane/reposition strategy groups.
- Winning sequences are below 50% of each exact search space containing wins.
- Some minimum-cost tested win requires a command after T1.
- The original P0 trace legally wins or has an understandable documented loss.

UNSOLVABLE means no win found in the reported bounds, never a proof over all
legal play. If no option is OK, stop P0 tweaks and report that core combat
design needs rethinking. No next phase is authorized by these criteria.

## Exact D rule (opt-in only)

`config.p0d = { blockedTurnsBeforeBreakout: 2 }` enables D; omitting it preserves
every original state/event byte. The threshold accepts positive safe integers.
A keeps the existing six-turn `p0c` option. D uses five turns; A+D uses six.

1. At enemy phase start, determine progress contributors exactly as before:
   living enemies already orthogonally adjacent to the winch. They contribute
   this phase and reset their blocked streak. Arrival never contributes early.
2. Process enemies in their existing unit-array order. Attempt the unchanged
   shortest reachable winch-neighbor path, using N/W/E/S target and BFS ties.
   A normal positive-length movement resets that enemy's blocked streak.
3. No reachable target path, or no legal positive step, counts as one blocked
   phase. On the Nth consecutive blocked phase, perform one breakout action.
4. Replan to the same winch-neighbor targets, ignoring living allies **only for
   path planning**. Other enemies remain impassable even if allied-transit is
   enabled. Choose shortest path with the same deterministic ties.
5. Travel at most three orthogonal cells. On encountering the first living
   ally, stop immediately on its cell and move that ally into the preceding
   path cell. That cell is now empty, so no overlap or chained shove occurs.
   If no ally is encountered within three cells, advance those cells normally.
   This is a forced swap, not a player command, attack, HP loss or teleport.
6. A performed breakout resets the streak to zero. If even that planning graph
   has no path (e.g. other enemies occupy all targets), wait and saturate the
   streak at N. A later unblocked phase resets it; a later blocked phase may
   retry the breakout. Resolve remains finite and atomic.

The `breakout` event records path, threshold streak and optional displaced
ally/from/to. Retry keeps the experiment config and clears the counters.
No existing movement range, map, deployment, objective threshold or default
rule changed. D's new pressure state is included in search state keys.

## Searches and interpretation

All commands pass through the real `command`/`resolve` API. No second simulator
or copied third-party implementation. Absent allies are removed for solo/duo.

- T1-only: all legal 0–3-command orders, deduplicated by labeled endpoints,
  cheapest representative retained, then wait. This matches P0c.
- At most one move: all legal actor/destination/turn combinations on the idle
  timeline, plus idle once. Commands after terminal failure are excluded.
- Exact bounded multi: at most two commands per turn, first at most two total,
  then extended to at most three total. Every sequence, including command
  order, is counted; no state/transition truncation. A deterministic wait-tail
  cache affects speed only, not enumeration. Three-on-T1 placements remain in
  the separate T1 space rather than being smuggled into this two-per-turn bound.
- Wider solo/duo: at most two commands per turn, no total command cap. At most
  10,000 retained turn-boundary states and 250,000 examined transitions per
  turn. Retain cheapest representative per state AND previously moved-unit
  set. Counter history is part of the state; cap flags and layer sizes are in
  JSON. A capped result supplies existence/cheapest-found evidence only.

Cost order is commands, distinct voluntarily moved allies, then total path
tiles, matching P0b/P0c. Tables display allies/commands/tiles. Forced swaps are
not voluntary commands. Best-win ties are tracked, so the T1 question is not
answered by an arbitrarily chosen witness. Full-party bests combine the four
exact spaces; reduced lineups are reported separately. Overlapping search
spaces must not be summed into a purported win rate.

Family grouping uses each living ally's final lane and whether any voluntary
command occurred after T1: y>3 rear; otherwise y=0 north; x<=1 west; x=2 south;
x>=3 east. Within-lane tile and timing differences are merged. Forced swaps
alone do not count as player repositioning. These are operational spatial
groups, not independent evidence that human players face meaningful choices.

## Reproduce

From this worktree root, with existing Node and the read-only node_modules:

```powershell
node --experimental-strip-types ui-prototype/tests/playable-l03-p0d-search.mjs
node --experimental-strip-types ui-prototype/tests/playable-l03-p0d.mjs
```

Normal runs compare evidence bytes without overwriting fixtures. Only new P0d
files can be generated with `--write-results` / `--write-traces`; no such flag
was used on P0/P0b/P0c. Complete results, cap flags, family witnesses and cheapest
wins are in `search-results.json`; replayed states/events in `witnesses.jsonl`.
Commands/exits and the final decision are in the P0d-specific handoff.
