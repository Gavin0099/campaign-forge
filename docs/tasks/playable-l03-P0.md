# Task P0: L03 west-bank winch, pure-rules PoC (60 min timebox)

Authorized by Gavin on 2026-10-22, 10:44 (Asia/Taipei). This authorizes **only P0**. P1 to P6 each need separate authorization after review.
Consensus source: Claude (review/quality-gameplay-audit, QR-11, QR-12, L03-PLAYABLE-SPEC.md), Codex (this branch, IMPLEMENTATION-SLICES.md), and the GPT review on 2026-10-22.

## Before you start
1. Work in `D:\campaign-forge` on branch `codex/playable-l03-research`. Run `git fetch origin`, then `git pull --ff-only` to get this task file. If that isn't a fast-forward, or the remote has any other commit you don't recognize, stop and report.
2. Run `git merge origin/main` (main only has docs and rules: AGENTS.md, CLAUDE.md, docs/review/RESOURCE-CHECKLIST.md). Don't use stash.
3. Read the following:
   - `AGENTS.md`, the Multi-Agent Coordination section
   - `docs/review/RESOURCE-CHECKLIST.md`
   - `docs/handoff/TEMPLATE.md`
   - Claude's `ui-prototype/docs/quality-review/L03-PLAYABLE-SPEC.md` on `origin/review/quality-gameplay-audit`, read-only through `git show`
4. Record the baseline SHA and your start time (with time zone).

## Decisions already made (don't reopen them)
- **Winch:** move it from (8,1) to the **west bank at (2,1)**. Player deployment stays on the west (left) bank. Don't move the party to the east bank.
- **Architecture:** use your pure rules state machine, command validation, and event-based presentation, in the standalone module `ui-prototype/src/playable-l03/`. Don't touch `L03Preview.tsx` or `ArtGate.tsx`.
- **Route intent:**
  - Open the gate: hold the west bank and keep the knight off the winch.
  - Seal the gate: escort the wagon across the bridge.

  P0 only needs to prove the **open-gate hold** loop. The seal route only needs to be reachable on the map.
- **Passing through allies:** not decided yet. Default to **no passing through any living unit**. Make it a single flag in the rules config, and add one test showing the open-gate route is still solvable with it on.
- Don't change rewards, story, or the K1 cost for QR-11 (open gate being the dominant choice). Just note it as a known issue.

## Build (60 minutes, nothing more)
A pure TypeScript module with no React, animation, or timers that resolves:

legal move -> simple enemy interference -> winch progress -> success or failure -> retry

Use one fixed MapDef and one fixed deployment.

## Not in scope
- No UI
- No new art
- No story changes
- No full Attack/Support system: a minimal enemy push or block that affects winch progress is enough
- No new npm dependency without Owner approval. Run tests with what already exists, e.g. `node --experimental-strip-types` or the esbuild already in node_modules.

## Acceptance (stop as soon as these are done, or at 60 min, whichever is first)
1. The winch at (2,1), both deployments, and the objective tiles are reachable. There is no overlap, no walking on water, and no crossing a broken bridge.
2. Legal and illegal moves are reproducible. When a move is rejected, the state is unchanged (deep-equal).
3. `resolve()` settles a turn without React, animation, or timers.
4. Simple enemy interference changes winch progress. Standing still must **not** win.
5. There is at least one success trace, one failure trace, and one retry trace, each written to a file. Re-running produces identical results.
6. Record: baseline SHA, implementation SHA, actual time spent, each test command with its exit code, and the RESOURCE-CHECKLIST filled in.

If you are stuck at 60 minutes, stop. Narrow the question and report what failed. Don't add features to hide it, and don't remove the failure condition.

## Stop and hand off
1. Commit and push `codex/playable-l03-research`. Don't open a PR and don't touch main.
2. Write `docs/handoff/codex-playable-l03-research.md` from the template, including the resource self-check.
3. **Stop.** Don't start P1. Claude and GPT will review this, and Gavin will decide next.
