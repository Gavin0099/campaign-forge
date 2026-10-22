# Task P2: two enemy responses (rules domain only, 90 min timebox)

Authorized by Gavin on 2026-10-22 as part of the P1→P6 chain. Source: the GPT P0d review (`docs/review/gpt-playable-l03-p0d.md` on `origin/review/gpt-playable-l03-research`), decision 3.

**Parallel note:** another Codex session is doing P1v2 (screen readability) in the main checkout. You work in the separate worktree `D:\campaign-forge\scratch\p2` on branch `codex/playable-l03-p2`.
- Do NOT edit `PlayableL03.tsx` or its CSS. P2 is rules, tests and evidence only.
- UI integration comes in a later segment.
- Read-only references:
  - P0d's code on `origin/codex/playable-l03-p0d` (rules.ts D breakout, search support).
  - Its handoff, `docs/handoff/codex-playable-l03-p0d.md` on that branch.

## Goal
In the pure rules module, add two enemy behaviours, each emitting **intent + reason + action**. Both are opt-in config (`enemyBehaviour: "p2"`, or similar). The default rules and all P0/P0b/P0c/P1v outputs stay byte-identical. Base turn limit: **A (6 turns)**.

1. **Target interference (目標干擾).** This is the current behaviour: approach the winch and add progress. Formalize its intent output: target tile, planned path, reason.
2. **Hunt the weak point (追弱點).** If a knight's direct approach is blocked or detoured by more than a threshold (parameter), it switches to targeting the specific ally blocking the key lane.
   - **Telegraph turn.** On the following enemy phase, its intent becomes `prepare-breakout` against that ally. Show the target ally and the tile it will be shoved to. This gives the player one full turn to react: move away, swap in another unit, or reposition.
   - **Breakout turn.** If the ally is still there on the next enemy phase, the knight executes the telegraphed shove/swap. It must match the telegraph exactly. It deals no damage.
   - **Player reaction.** If the player reacts, the intent is cancelled or re-planned, with a reason.
   - Use P0d's D swap as reference, but fix the issues GPT found:
     - Detour counts as pressure, not just "fully blocked".
     - The states blocked, prepare-breakout and breakout are distinct and announced in advance.
     - No surprise swaps.
3. Do not add HP, attacks, class skills, more AI types, UI, art, story or dependencies.

## Acceptance
- Unit tests prove every intent matches the actual events for both behaviours, including the telegraph turn followed by a matching breakout, and the telegraph followed by a player reaction that cancels or replans.
- Re-run the P0d search harness (reuse it) with P2 behaviour on 6 turns:
  - T1-then-wait
  - ≤1 move
  - ≤2 and ≤3 total-move bounded search
- Report the metrics:
  - W/L
  - min-cost win
  - whether the A/A+D cheapest rear-delay win (Karen T1 (2,5)→(1,5), Lace (1,3)→(3,4); T2 Karen→(2,5); wait) still wins
  - how many cheapest wins require reacting to a telegraph
- **Key gate (per GPT):** at least one tested winning line must need a re-decision *because of* the enemy reaction. Show it as a replayable witness.
  - Use verdict THIN or OK only with that evidence.
  - Otherwise say plainly that P2 didn't create the re-decision.
- The P0, P0b, P0c and P1v tests still pass unchanged. Run the searches twice and confirm the output is byte-identical.
- Handoff: write `docs/handoff/codex-playable-l03-p2.md` with the table, the witness and the resource self-check.

## Stop
Commit, then try `git push -u origin codex/playable-l03-p2`. If the push fails, leave the commits local. Don't touch main or the main checkout, open a PR, or use git stash.
