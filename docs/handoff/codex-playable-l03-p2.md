# Handoff: codex/playable-l03-p2

**P2 creates a causal re-decision on one tested defense line, but the encounter
is still CHEESE.** Telegraphs and exact/cancelled swaps work at the rules layer.
The original A/A+D rear delay still wins, and a cheaper one-ally/two-command
delay now wins without responding to a telegraph. This is evidence for review,
not a recommendation to adopt P2 as the default or a claim of tactical depth.

| Field | Value |
| --- | --- |
| Branch / worktree | `codex/playable-l03-p2` / `D:\campaign-forge\scratch\p2` |
| Owner-named base | `ce45ad2b29ddbfd9e975e4f894b4001faa63d378` |
| Implementation commit / delivery | `48652a6feb3707f748262c389883932692573e0b`; normal commit **0**, `git push -u origin codex/playable-l03-p2` **0**, pushed **yes** |
| Handoff delivery | This file follows in a separate commit on the same branch. Final handoff SHA and remote-head verification are reported in the final response rather than a self-referential SHA. |
| Owner instruction | Only `docs/tasks/playable-l03-P2-enemy.md`, 90 minutes; read-only node_modules; do not touch P1v TSX/CSS, main checkout/branch or P1v2; commit then try push, leave local on failure |
| Time window, Asia/Taipei | Started approximately 2026-10-22 18:15:14; first clock 18:15:17. Final delivery time/elapsed reported with the actual SHAs. |
| Parallel coordination | Owner identifies the other session in the main checkout; this process uses only the separately assigned P2 worktree. No additional model agents started. |

Implementation delivery used a fresh `git fetch origin` (0); the remote P2 ref
was still the known base `ce45ad2`, with no unknown commits. Normal push advanced
only `codex/playable-l03-p2` to `48652a6`. The existing pre-commit advisory reported
`missing_canonical_memory` with `completion_claim_allowed=True`; no daily record
was manufactured because task completion is not SessionEnd. The shared pre-push
JSON inventory guard passed (`updates=1`, `json_blobs=3`). Its inherited smoke
named `D:/campaign-forge/ai-governance-framework` as framework/smoke root and
this P2 worktree as target, and printed advisory scope diagnostics; overall push
exit was 0. That shared hook invocation is distinct from this session's source
work. No hook/global trust or main-checkout source was manually changed, and
this does not prove P2-native callbacks or complete governance adoption.

## 1. What changed

- `ui-prototype/src/playable-l03/rules.ts`: opt-in `enemyBehaviour: 'p2'`,
  parameter `detourThreshold` (default 1), enemy pressure/telegraph memory,
  two behaviours emitting intent + reason + exact action. Default events/states
  and P0c/P1v configuration remain unchanged.
- Pressure compares the open route with the route ignoring allies but retaining
  enemy obstacles. First pressure approaches/stops before its named blocker;
  following phase prepares an exact swap and waits; next phase executes only
  that saved swap. Moving or replacing the target cancels/replans, never swaps
  a replacement ally without a fresh warning. No damage or new battle system.
- P2 tests/search and `ui-prototype/docs/playable-l03-p2/` retain the results,
  four full replays and actual unchanged P1v browser regression captures.
- P0d reference was read via `git show` at
  `2dc92b6d5ec22e9e4e48bb82db995adeb111e58a`; copied its bounded search harness
  and adapted the pressure cache key and witness checks. No branch merge.
- **Shared files edited: NONE.** This dedicated handoff carries the milestone.
  Shared PLAN/memory locks are outside the assigned write boundary; coordinator
  reconciliation is an open question, not silently performed during parallel work.

### Metrics

A's six-turn horizon; full party. Cost is **moved allies / commands / path
tiles**, ranked by commands, allies, tiles. Counts are command/placement spaces,
not human win rates. Overlapping spaces are not summed.

| Search | W / L | Min-cost win | Cheapest wins requiring telegraph reaction |
| --- | ---: | --- | ---: |
| T1 then wait | 88 / 6,708 | 2 / 2 / 5 | 0 of 1 |
| <=1 total move | 0 / 210 | None | N/A |
| <=2 total moves, <=2/turn | 80 / 24,705 | 1 / 2 / 2 | 0 of 1 |
| <=3 total moves, <=2/turn | 14,220 / 1,905,088 | 1 / 2 / 2 | 0 of 1 |

No beam/state/transition cap in the required bounded searches. The wait-tail
cache limit is not a search cap. T1 uses deduplicated placements; the two/three
move spaces enumerate command sequences. All three bodies remain present.

Cheapest win: T1 Karen `(2,5)->(3,5)`; T2 Karen `->(2,5)`; wait T3–T6,
progress 1. Original A/A+D cheapest rear delay also still wins: T1 Karen
`(2,5)->(1,5)`, Lace `(1,3)->(3,4)`; T2 Karen `->(2,5)`; wait, progress 2.
Neither needs a reaction to a preparation telegraph.

### Key-gate witness: achieved locally

1. T1: Lace `(1,3)->(1,1)`; Thoma `(1,4)->(2,2)`;
   Karen `(2,5)->(3,3)`.
2. T2: Karen `(3,3)->(3,1)`.
3. T3: wait. Knight-1 prepares Lace `(1,1)->(1,2)`;
   knight-2 prepares Karen `(3,1)->(3,2)`. Neither swap happens yet.
4. T4: Karen `(3,1)->(1,0)`, then Lace `(1,1)->(3,1)`.
   Both original telegraphs cancel. Knight-1 approaches the vacated west cell;
   knight-2 must start a fresh blocked/prepare sequence against Lace.
5. T5–T6: wait. The replacement-blocker swap finally happens at T6, too late
   to contribute that phase; win at progress 2.

| Replay | Outcome | Final progress |
| --- | --- | ---: |
| P2, take the T4 reaction | Win | 2 |
| P2, omit T4 reaction | Lose; exact advertised swaps execute at T4 | 4 |
| A alone (P2 off), omit T4 reaction | Win | 2 |

Cost: **3 allies / 6 commands / 15 tiles**, including **two extra commands /
five tiles** to react. This is a re-decision caused by the enemy reaction on the
same defense prefix, not merely a later-turn move. It does not establish that
reacting is globally necessary. The directed probe tried 24 single-command
responses and six ordered pairs, stopping at its first witness. It is separate
from the exhaustive <=3 table and makes no six-command optimality claim.

Full replay: `ui-prototype/docs/playable-l03-p2/witnesses.jsonl`;
inputs, counts and probe bounds: `search-results.json`; contract: `README.md`.
**Verdict: CHEESE**, even though the key gate is achieved. No THIN/OK claim.

## 2. How to verify

Run from this worktree root. No install needed.

| Command | Result / native exit |
| --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p2-search.mjs` twice | 0 / 0; report and witness bytes identical |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p2.mjs` | 11 PASS, 0 |
| Original `playable-l03-p0.mjs`, `-p0b.mjs`, `-p0c.mjs` with same Node flags | 8 / 9 / 9 PASS; each 0 |
| Original `playable-l03-p0b-search.mjs`, `-p0c-search.mjs` | Each 0; original output unchanged |
| `npm run build --prefix ui-prototype` | 0 |
| Existing Python 3.12 + `scripts/validate_ui_scope.py` | 0 after existing pinned submodule checkout; initial missing-module exit 1 retained |
| Unchanged `playable-l03-p1v-browser.mjs`, `P1V_URL=http://127.0.0.1:5184/` | 26 PASS, 0 |
| Byte/hash assertion batch; legacy protected diff; whitespace | Each 0 |

Exact command receipts, source digests and environment failures are in
`ui-prototype/docs/playable-l03-p2/command-results.json` and `VERIFICATION.md`.
Report SHA-256: `c51d862a9c1e3060643773ce4bac655db9bdccea30c2e8f0bd996ffc70b92d86`.
Witness SHA-256: `81f5ff28141dd74707f7d4f4014a84c87535081b89b674230fa027e3aab42c79`.

`p1v-regression/` contains actual running-build 720p/1080p/text captures and
the unchanged browser harness's raw report. Its capture paths retain original
names; resolve by basename in the relocated folder. All capture/source hashes
were checked, and the original P1v evidence restored byte-for-byte. These show
the old UI with P2 disabled, not P2 UI integration or human playtest results.

## 3. Not done / known limits

- No P1v2 edits, P3+, new UI, art, story, HP, attacks, skills, engine or dependency.
- No exhaustive >3-command search, optional-party balance or human playtest.
- Extra telegraph waiting introduces cheap delays; the new AI is not necessarily
  harder or better. One causal witness does not remove the cheaper exploit.
- The rule-adaptation contract named by the checklist is absent in this branch;
  no formal SRD/G005 adaptation is undertaken or inferred from that absence.
- No shared PLAN/memory edit or daily canonical closeout. Task DONE is not
  SessionEnd. No native callback/full governance-adoption claim.

## 4. Risks

- A future UI must distinguish the immediate `plannedPath` (wait during prepare)
  from the stored `plan.path`/`plan.to` telegraph, and show cancellation reasons.
- The pressure threshold and mandatory waiting can reward manipulating enemy
  routes. The CHEESE result is an actual limitation, not an unexplained PASS.
- Tests prove stated deterministic rules and bounded evidence; they do not
  prove player understanding, fun or commercial quality.

## 5. Open questions

- For Claude/GPT, when Owner requests review: audit the causal counterfactual,
  phase separation, cache key, cheapest-win definition and restored legacy bytes.
- For Gavin: decide whether to retain this opt-in mechanism given the cheap win.
  No tuning or later slice is automatically authorized by this recommendation.
- For the coordinator: reconcile the branch-specific milestone into shared
  PLAN/memory under the normal lock after parallel tasks, if desired.

## 6. Not claimed

Owner acceptance, human playtest, commercial art approval, adopted story/rules,
P2 UI readiness, complete tactical depth, unrestricted balance, full executable
trust audit, native hook callbacks, canonical closeout, main merge, PR, deploy
or Actions. Push success is claimed only from the real command result.

## Resource self-check

Source: `docs/review/RESOURCE-CHECKLIST.md`. The three relevant public SKILL.md
files were fully read at fixed `gamedev-skills/awesome-gamedev-agent-skills`
commit `0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`: `prototype-fast`,
`level-design`, `game-ai`. Method only; no installation or copied external code.
The local external-executable-trust-audit skill/checklist was read for the
unchanged browser harness. Ordinary shell/Node/npm/Git trust roots remain;
Chrome's pre-launch binding is not a full toolchain security attestation.

### A. Skills

- PASS — prototype-fast: one mechanic, explicit causal keep gate, 90-minute
  timebox, opt-in experiment, negative CHEESE result preserved. Human fun test
  N/A under this rules-only task.
- PASS bounded — level-design: terrain/deployment unchanged, default reachability
  tests pass, all reported witnesses legally replay with explicit costs.
  Sealed-route play and full encounter quality are outside P2.
- PASS rules layer — game-ai: small state machine, named blocker, deterministic
  paths/actions, delayed exact swap and player-driven cancellation; 11 tests.
- N/A — game-ui-ux: P2 UI explicitly prohibited; P1v regression separately passes.
- N/A — game-feel: no animation/hit/pacing changes authorized.

### B. Reference repos

- PASS architecture / N/A reuse — Grid-Tactics: pure rules return state/events;
  no view import or animation-owned resolution. No code/assets copied; its
  previously recorded license remains unconfirmed.
- N/A reuse — HopeMetal/2DTacticalRPGDemo: no code/assets borrowed; previous
  research distinguishes MIT code and CC-BY-SA 3.0 images, not blanket MIT.
- PASS — no new engine/dependency; package/lock unchanged, no npm install;
  only the already-pinned governance submodule checked out for validation.

### C. Playable acceptance bar

- N/A — full uncoached 3–5 minute P2 battle: rules-only task; not claimed.
- PASS program layer — understandable state-based enemy actions: target/reason/
  action/telegraph tests and saved traces. Human comprehension remains pending.
- PASS — win/lose: table and causal replays prove both outcomes.
- PASS local differing choices / FAIL encounter depth, explained: reacting to
  the T3 telegraph changes loss to win, but cheaper two-command waiting wins
  remain. This explains the CHEESE verdict and prevents adoption/quality claims.
- PASS — restart/change strategy: P2 retry reset plus unchanged P0/P1v tests.
- PASS tested rules — no duplicate/stale resolution, invalid movement or overlap;
  frozen inputs, placement sample and witness checks. Animation N/A for P2;
  old P1v animation cancellation regression passes.
- PASS regression / N/A P2 presentation — 720p/1080p, text and keyboard: 26 old
  P1v browser checks. New P2 intent presentation not implemented.
- PASS — automated vs human evidence separate; actual exits/captures; no human
  or model-review approval fabricated.

### D. Project rules

- N/A formal SRD adaptation / PASS no copied IP: original provisional occupancy
  rule only; no WotC content or external art/code. Missing adaptation contract
  is disclosed rather than treated as authority.
- PASS — assigned worktree/branch/scope only; no other checkout/branch edits,
  no shared-file writes, main, PR, stash, force, bypass, deployment, Actions or
  story change. Scope validator 0. Delivery status is recorded above.

## Review

Claude/GPT review is separate and only initiated when Owner requests it.
This self-check is not Owner approval.
