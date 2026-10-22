# Task P0d — complete A's search + enemy counter-pressure (verification only, 45–60 min timebox)

Authorized by Gavin 2026-10-22 16:30 Asia/Taipei. Source: GPT P0c review (`docs/review/gpt-playable-l03-p0c.md` on `origin/review/gpt-playable-l03-research`), decision 3. Owner decisions: P0c accepted; A stays a candidate, NOT the default.
This authorizes ONLY P0d, and it is the last P0 rules-verification round. P1 is NOT authorized.

## Goal
Find out whether any rule variant gives L03 real tactical choice, meaning that the best strategies are not all "deploy on T1, then wait".
Verification only: new variants are opt-in config, OFF by default. The P0, P0b and P0c tests and outputs stay byte-identical. Do not add attacks, HP, UI, animation, art, story or new dependencies.

## Do
1. **Complete A.** Run the same cross-turn bounded multi-move search on A that P0c ran on B/B+: at most 2 moves per turn, at most 2 moves total. Extend it to at most 3 moves total if that is feasible within the timebox, and report the bounds. Re-check whether solo and duo lineups can win under A, with at most 2–3 commands per turn (bounded). Report the cheapest win.
2. **New variant D: enemy counter-pressure.** When an enemy has been blocked for 2 consecutive turns, it switches its target or takes one simple breakout action. Keep it minimal and deterministic, and document the exact rule. A breakout action is something like retargeting to another approach lane or the winch from another side, or a forced shove/swap. Do NOT add damage or HP. Make the 2-turn threshold a parameter.
3. Compare **A**, **D** (5 turns) and **A+D** (6 turns) on the same search spaces as P0c:
   - T1-then-wait
   - at most one move
   - bounded multi-move
   - solo and duo

   Use the same table columns as P0c, plus these two:
   - **Distinct winning strategy families**: group the wins by which units hold which lane and whether they re-position after T1.
   - **All best wins are T1-then-wait?** (yes/no)
4. Verdict per variant: CHEESE, THIN, OK or UNSOLVABLE. **OK** requires all of the following:
   - no T1-then-wait win, or only costly ones
   - at least 2 distinct winning strategy families
   - wins exist but are a minority of the search space
   - the original P0 trace either still wins or fails for an understandable reason (explain which)

## Acceptance
- Run the searches twice and confirm the output is byte-identical. Record the exit codes.
- The P0, P0b and P0c tests still pass unchanged.
- Add a "P0d" section to the handoff with the table, the verdicts, and one recommendation. If nothing reaches OK, say plainly that "P0 rule tweaks are exhausted; core combat design needs rethinking" and list at most 2 directions as proposals only.
- Update the resource self-check.

## Stop
Commit, then try `git push`. If the push fails, leave the commits local and say so. Do not start P1, touch main, open a PR or use git stash.
