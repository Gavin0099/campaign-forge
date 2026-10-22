# Task P0b: L03 stance validation (verification only, 45 min timebox)

Authorized by Gavin on 2026-10-22, 13:50 (Asia/Taipei). The source is the GPT review of P0 (`docs/review/gpt-playable-l03-p0.md` on `origin/review/gpt-playable-l03-research`), decision 2.
This authorizes **only P0b**. P1 is NOT authorized.

## Goal
Find out whether the P0 open-gate hold is a real tactical decision or a trivial cheese. **Verify only.** Don't add attack, push, HP, animation, UI, new art, or story. Don't change the rules in `rules.ts` unless a test proves a plain bug. If you fix a bug, keep it minimal, explain it in the handoff, and record the before/after behaviour.

## Before you start
1. Work in `D:\campaign-forge` on `codex/playable-l03-research`. Run `git fetch origin` and `git pull --ff-only`. Stop if it isn't a fast-forward.
2. Read the GPT P0 review with `git show origin/review/gpt-playable-l03-research:docs/review/gpt-playable-l03-p0.md`.
3. Record the baseline SHA and your start time.

## Do
1. **Exhaustive or bounded search.** Write a headless script that enumerates player strategies within the 5-turn limit. Cover at least all end-turn-1 placements of the 3 party members within move range; a bounded search over later turns is fine. Report:
   - the number of winning vs losing strategies
   - the **minimum-cost win** (fewest total moves, fewest units moved)
   - whether 1 or 2 units alone can win
   - whether any win needs no movement after turn 1
2. **At least 3 different blocking stances**, written as tests with traces. Include the current success stance and at least 2 others (for example north-side block, chokepoint block away from the winch, partial block). For each, record the final progress, the outcome, and what the enemies did once blocked.
3. **Blocked-enemy behaviour matrix.** Cover both enemies contesting the same tile, equal-length path ties, and move-order effects. State the current tie-break rule explicitly and add a deterministic test for it.
4. Add the `walkable()` bounds check and update the stale SHA and push state in the handoff. Both were P1/P2 findings in the GPT review.

## Acceptance
- The search script and tests run with existing tooling (`node --experimental-strip-types`), with no new dependencies, and give identical results on re-run. Record the exit codes.
- The results table is in `docs/handoff/codex-playable-l03-research.md` under a new "P0b stance validation" section. Write a plain verdict:
  - **CHEESE**: a trivial win exists, such as one unit or no meaningful decision.
  - **THIN**: few wins, each needing a deliberate setup.
  - **OK**: multiple distinct wins with real trade-offs.
- Update the resource self-check (RESOURCE-CHECKLIST) for this chunk.
- If the verdict is CHEESE, list at most 3 candidate rule or map tweaks as **proposals only**. Don't implement them.

## Stop and hand off
Commit, then push `codex/playable-l03-research`. If the push fails, leave the commits local and say so. Don't start P1, don't touch main, don't open a PR, and don't use git stash.
