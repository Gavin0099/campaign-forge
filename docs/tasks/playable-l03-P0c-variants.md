# Task P0c: compare win-condition variants A / B / C / B+ (verification only, 45 min timebox)

Authorized by Gavin on 2026-10-22, 15:30 (Asia/Taipei). The source is the GPT review of P0b (`docs/review/gpt-playable-l03-p0b.md` on `origin/review/gpt-playable-l03-research`), decision 2.
This authorizes **only P0c**. P1 is NOT authorized.

## Goal
Find out which win-condition variant turns the open-gate hold from CHEESE into a real decision. This is **verification only**: keep the default rules exactly as they are now. Each variant must be a config option that is off by default, so the existing P0 and P0b tests and traces stay byte-identical. Don't add attack, push, HP, animation, UI, art, or story. Don't adopt any variant as the default.

Variants:
- **Baseline**: current rules.
- **A**: the survival limit is 6 turns instead of 5.
- **B**: on victory, at least one companion must be adjacent to the winch (2,1).
- **C**: Toma's starting position is (0,4).
- **B+**: in each of the last 2 turns, at least one companion must be adjacent to the winch at end of turn, and progress must be below the threshold. Make the number of turns (N) a parameter and also report N=3.

## Before you start
1. Work in `D:\campaign-forge` on `codex/playable-l03-research`. Run `git fetch origin` and `git pull --ff-only`. Stop if that isn't a fast-forward.
2. Read the GPT P0b review with `git show origin/review/gpt-playable-l03-research:docs/review/gpt-playable-l03-p0b.md`.
3. The Owner has confirmed that any Claude desktop helper process is not working in this worktree. If `git status` is clean, proceed.
4. Record the baseline SHA and your start time.

## Do
For each variant, run the **same search spaces as P0b**:
- all turn-1 placements followed by waiting
- at most one move across the whole battle
- solo and duo lineups

Then fill in this table:

| Variant | Turn-1-then-wait W/L | Max-one-move W/L | Min-cost win (units/moves/tiles) | Original P0 success trace still wins? | Lace (0,3) cheese still wins? | Solo wins? | Duo wins? |
|---|---|---|---|---|---|---|---|

Also add a **bounded multi-move search** for B and B+, with at most 2 moves per turn and 5 or 6 turns. In it, look for new cheap wins such as "rush to the winch on the last turn". Report the cheapest win you find and the search bounds you used.

## Acceptance
- Results come out identical when the search is run twice. Record the exit codes.
- The P0 and P0b tests still pass unchanged, which proves the defaults didn't change.
- The handoff gets a "P0c variant comparison" section. It contains the table, a verdict per variant (CHEESE, THIN, OK or UNSOLVABLE), and one recommended variant with its reason.
  - "No win found" is UNSOLVABLE, not fixed.
  - If no variant reaches THIN or OK, say so plainly. You may list at most 2 new candidate ideas, as proposals only.
- Update the resource self-check.

## Stop and hand off
Commit, then try `git push`. If the push fails, leave the commits local and say so. Don't start P1, don't touch main, don't open a PR, and don't use git stash.
