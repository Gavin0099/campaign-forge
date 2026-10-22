# Handoff: codex/playable-l03-research

P0b verdict: **CHEESE**. One tile of movement by Lace on turn two, followed
by waiting, wins with progress 2. The earlier multi-unit hold proves that
occupancy affects outcomes, but is unnecessary to win this reduced encounter.
The bounded searches and replayable traces below replace any implication of
proven tactical depth. This remains a headless rules experiment. The normal
P0b push failed (exit 1); implementation and this updated handoff remain local.

| Field | Value |
| --- | --- |
| Branch | `codex/playable-l03-research` |
| Historical P0 base | Task baseline `d0f400500d60d013d7d95c2bc97c12387d22baaf` after requested fast-forward pull |
| Historical P0 merge from origin/main | `aea2af7e400b446ea84a610fac75edd9664218f9`; merge `f80677d21c2f928d7add7fda81482ad6e1e97cf6`; no merge performed during P0b |
| P0 implementation SHA (historical) | `4e6d0d8a27c02ec04d8e1178310ce472fc0e6ef1`, already included in fetched remote baseline below; the old local-only description is superseded. |
| P0b baseline / last fetched remote head | `097f5a777a3daa551e00dc425d9d96db81f5136d` on `origin/codex/playable-l03-research`; task-required fetch and pull returned 0, already up to date. |
| P0b implementation SHA | `0cf8017ca5750fd359453b72f498bd9dac6d7c1d` (pushed: **no**, normal push exit **1**, github.com:443 connection failure). |
| Head | This handoff is a separate local documentation commit after the P0b implementation SHA; obtain its exact SHA with `git rev-parse HEAD`. No self-referential SHA is asserted. |
| Owner instruction | Finish only `docs/tasks/playable-l03-P0b-stance.md`: save search/tests, explicit bounds, results/verdict/up to 3 proposals, refreshed self-check, test exit codes, commit then normal push attempt; on failure leave local. Owner at 14:51 confirms worktree authorization and no competing work session. No P1, main changes, PR or stash. |
| P0b time window (Asia/Taipei) | Current write-enabled continuation starts `2026-10-22T14:51:57+08:00`; implementation commit `2026-10-22T14:58:34+08:00`; handoff evidence freeze `2026-10-22T15:01:33+08:00` (9m36s). Final documentation commit/check overhead is reported in final response. Earlier read-only run duration was not supplied and is not included or invented. Task timebox: 45 minutes. |
| Review input | P0b: `git show origin/review/gpt-playable-l03-research:docs/review/gpt-playable-l03-p0.md` (exit 0). Historical P0: read-only `origin/review/quality-gameplay-audit` @ `211594279fb48add8fd7cb524122b6e536398812`, `ui-prototype/docs/quality-review/L03-PLAYABLE-SPEC.md` via `git show` |

## P0b stance validation

### Verdict and search boundaries

**CHEESE**: the simplest verified win moves Lace from (1,3) to (0,3)
on turn 2, then waits. Nobody moves on turn 1. Knight-1 has no reachable
winch-adjacent target on turn 2, resumes its approach on turn 3, and arrives
only on turn 5. Knight-2 contributes on turns 4 and 5, so progress ends at 2,
below the failure threshold 3. Temporary delay plus the deadline is enough;
this win does not depend on permanently sealing the winch or a late active
defense. It also does not prove a full encounter or both branches are balanced.

`ui-prototype/tests/playable-l03-p0b-search.mjs` calls the actual rules API,
not a second simulator. T1 enumeration includes all legal orders of 0–3 moves
(each ally at most once), deduplicates by labeled end placement, and retains
the cheapest representative. Cost order is total commands, distinct allies
moved, then path tiles. Later turns only wait. The other enumeration covers
every legal single move on every still-playing turn, plus idle counted once.
Neither table is an exhaustive five-turn search with unrestricted movement,
nor a probability estimate of how humans play. Default allied blocking is ON.

| Search / question | Wins | Losses | Minimum / answer |
| --- | ---: | ---: | --- |
| All T1 placements then wait (6796 distinct placements) | 493 | 6303 | 1 move, 1 ally, 3 path tiles: Lace T1 → (3,4), final progress 2 |
| Of those, move 0 allies | 0 | 1 | Idle loses with progress 4 |
| Of those, move 1 ally | 1 | 46 | Other two allies remain present as blockers |
| Of those, move 2 allies | 59 | 789 | End placements, not command-order counts |
| Of those, move 3 allies | 433 | 5467 | End placements, not command-order counts |
| At most one move during all five turns (217 strategies) | 6 | 211 | 1 move, 1 ally, **1 tile**: Lace T2 → (0,3), final progress 2 |
| Any win without movement after T1? | 493 | — | Yes; the first search's entire winning set |
| True solo / duo (other allies removed) | Witnesses for all 3 solos and all 3 duos | Not a full count | Each replay succeeds at progress 2; none wins in its own at-most-one-move search |

The global cost lower bound is also met: idle loses, a move must use at least
one ally and one tile, and the T2 retreat meets all three minima. Solo/duo
uses a separate deterministic witness search with at most one ally command
per turn, deduplicating by positions and progress, and a 10,000-state cap.
No cap was reached (largest retained frontier 8003); it stops on the first
winning witness and **does not claim lineup win totals or optimal witnesses**.
All six witnesses are independently replayed by the P0b test, with JSONL traces.

| Actual lineup | ≤1 move wins / losses | Winning witness moves / units moved / tiles |
| --- | --- | --- |
| Karen | 0 / 93 | 4 / 1 / 9 |
| Lace | 0 / 89 | 3 / 1 / 6 |
| Thoma | 0 / 89 | 3 / 1 / 7 |
| Karen + Lace | 0 / 167 | 3 / 1 / 7 |
| Karen + Thoma | 0 / 169 | 3 / 2 / 9 |
| Lace + Thoma | 0 / 145 | 3 / 1 / 6 |

### Stances and blocked-enemy matrix

`ui-prototype/tests/playable-l03-p0b.mjs` asserts outcomes and replays each
committed trace byte for byte under `ui-prototype/docs/playable-l03-p0b/`.
Coordinates below are destinations, not new deployment definitions.

| Stance | Commands | Outcome / progress | Enemy response |
| --- | --- | --- | --- |
| Current hold | T1 Lace(1,1), Thoma(2,2), Karen(3,3); T2 Karen(3,1) | success / 1 | Knight-2 blocked T3–T5 at (2,3); knight-1 detours via (0,0), reaches (2,0) T4 and contributes T5 |
| North partial | T1 Lace(1,1), then wait | failure / 3 | Both keep approaching; knight-2 reaches (3,1) T3, knight-1 detours west to (2,2) T4; both contribute T5 |
| South choke away from winch | T1 Karen(3,3), then wait | failure / 3 | Knight-2 detours via (0,5), no blocked wait; knight-1 reaches (2,2) T3 and both contribute T5 |
| One-tile retreat | T2 Lace(0,3), then wait | success / 2 | Knight-1 waits blocked T2, then detours through (3,6), arriving (2,2) T5; knight-2 contributes twice |
| Cheapest T1 placement | T1 Lace(3,4), then wait | success / 2 | Knight-2 waits blocked T2, resumes T3, reaches (2,2) T5; knight-1 contributes twice |

Current tie rules are explicit in these tests, without changing AI policy:
**BFS neighbors N/W/E/S; candidate winch-adjacent targets N/W/E/S; shortest
path first, stable sorting retains that target order on equal lengths; enemy
iteration follows array order (`knight-1`, then `knight-2` in deployment).
Each later enemy recomputes against already-updated occupancy.**

| Matrix case | Deterministic assertion / trace |
| --- | --- |
| Equal routes to one destination | (1,3)→(2,2) goes north to (1,2) before east; `equal-ties.jsonl` |
| Equal target lengths | From (1,3), W target beats S; from (0,0), N target beats W; `equal-ties.jsonl` |
| Two enemies contest only empty S target | Allies occupy N/W/E; enemies (1,3)/(3,3). First reaches (2,2); second emits blocked and stays; progress 0 on arrival, 1 next turn; `contention-order.jsonl` |
| Reverse enemy array order | Same geometry, other enemy takes S, former winner waits. Positions and intent identities reverse predictably; no overlap; same trace file |
| Repeated blocking / recovery | Current hold repeats blocked T3–T5; one-tile retreat shows blocked T2 then approach T3. No attack, push or alternate combat policy exists |

### Minimal bug fix

Only gameplay-source change: one explicit `walkable()` rectangle check after
the integer guard. Out-of-range x/y now return false before indexing rows.
The regression temporarily defines an inherited array property at `-1` and
restores it in `finally`: before the fix `(0,-1)` incorrectly returned true;
test exited **1**. After the fix it returns false, test exits **0**. This is
a constructed robustness case, not a claim that normal map data was polluted.
Both route boundaries, nonintegers, valid corners, water and the route-specific
bridge exclusion are also checked. Original P0 traces remain byte-identical.

### Tweak proposals — not implemented

1. **Extend the survival deadline from 5 to 6 turns.** Hypothesis: the extra
   enemy phase defeats both recorded one-move delays. Cost: longer encounter
   and possible elimination of deliberate hold wins; re-run searches before
   considering it. No threshold or timing change has been made.
2. **Require an ally adjacent to the winch at final success as well as low
   progress.** Hypothesis: force an active defense position instead of the
   recorded retreat/choke wins. Cost: another success condition to communicate
   and potentially a different one-move exploit; needs separate validation.
3. **Move Thoma's initial placement from (1,4) to (0,4).** Hypothesis: open the
   south approach that the retreat temporarily seals with existing occupancy.
   Cost: different initial route pressure and perhaps fewer valid holds;
   requires new reachability/strategy comparisons. No deployment was changed.

These are alternative candidates, not an approved combined design or a P1 plan.

### Verification and delivery ledger

| Command | Observed exit code / result |
| --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs --write-results` | **0**, report saved after correcting the initially too-narrow solo witness search described below |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs` (twice) | **0 / 0**, recomputed report equals committed fixture on both runs |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs --write-traces` | **0**, 9 tests, 13 JSONL fixtures saved |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` (twice) | **0 / 0**, 9 PASS each; byte comparisons include all stances/matrix/lineups |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | **0**, 8 PASS, original traces unchanged |
| `npm run build --prefix ui-prototype` | **0**, TypeScript + Vite, 46 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | **0**, approved execution with existing interpreter, final source/milestone state; 13 planning files protected |
| `git diff --check`; `git diff --cached --check` | **0 / 0** before implementation commit |
| `git diff --check` after handoff update | **0** |
| `git fetch origin`; `git pull --ff-only` | **0 / 0**, already up to date; repeated after own shared locks |
| Pre-push `git fetch origin`; `git log --oneline HEAD..origin/codex/playable-l03-research`; `git merge-base --is-ancestor origin/codex/playable-l03-research HEAD` | **0 / 0 / 0**, empty unknown-commit list, safe ancestor |
| Implementation `git add`; `git commit` | **0 / 0**, `0cf8017ca5750fd359453b72f498bd9dac6d7c1d`; normal hooks, no bypass |
| `git push origin codex/playable-l03-research` | **1**, failed to connect to github.com port 443. Per Owner instruction, **leave local**, no retry/escalation/credential changes |

Both search stdout captures have SHA256
`14d2beed456c76e53119b159c998e6b56b776f9c4fde1a7bf37cc834d0dcc6cb`;
both test stdout captures have
`0ee81138822e187cff8a8c97d6696eaa2f69796e877a0429e5afacfd48c904c3`.
These are PowerShell stdout-capture hashes in ignored scratch, not hashes of
the UTF-8 JSON report. Fixtures themselves are checked as exact UTF-8 bytes.

Failed setup/development checks are preserved: initial sandbox fetch exit
**255** (`.git/FETCH_HEAD` denied), approved fetch **0**; `rg` was unavailable,
so local PowerShell reads were used. Bare `python` was unavailable (command
not found, **no interpreter exit code**); the following `$LASTEXITCODE=0`
was stale from build and is **not** scope evidence. Existing absolute Python
inside sandbox exited **1** (inaccessible), approved runs returned **0**.
The pre-fix bounds test exited **1** as expected. Initial search exited **1**
because it wrongly asserted true solo success inside the ≤1-move search;
that search correctly had none. Added the separately bounded multi-turn
witness search; unchanged three-ally counts and all-six-lineup replays pass.

Shared files edited for P0b: `ui-prototype/PLAN.md`, `memory/01_active_task.md`.
Own locks acquired, fetch/pull completed before edits, SHARED-EDIT output
printed, Shared-file commit trailers present. On failed push, locks are
released at local handoff; no remote delivery or shared-file availability on
another branch is claimed. No `memory/YYYY-MM-DD.md` edit or SessionEnd is
manufactured. Hook advisory `missing_canonical_memory` allowed commit with
`completion_claim_allowed=True`; that is not canonical closeout evidence.

### Resource self-check — P0b (current chunk)

Source: `docs/review/RESOURCE-CHECKLIST.md`; older P0 checklist below is historical.

| Section / item | Result and evidence |
| --- | --- |
| A: prototype-fast | **PASS (verification)** — one question and CHEESE criterion in task/search, isolated rules, current continuation <45m; retain evidence, not production approval. Cached original skill re-read; same fixed commit/hash as historical manifest below. Human fun criterion unmeasured |
| A: level-design | **PASS (open P0b)** — 6796 T1 placements, 5 stance traces and reduced-lineup witnesses; **N/A sealed victory**: deliberately map-only, not claimed |
| A: game-ai | **PASS (behavior verification)** — explicit BFS/target/order matrix, blocked wait and later recovery traces. Tactical depth verdict is CHEESE; passing deterministic tests does not approve AI design |
| A: game-ui-ux / game-feel | **N/A** — P1 UI/animation excluded |
| B: Grid-Tactics | **PASS separation** — search calls existing pure state/event API; no view dependency or copied external implementation; prior pinned reference only, no new external repo execution |
| B: HopeMetal / asset licenses | **N/A reuse / PASS scope** — no borrowed code or art, earlier MIT-vs-image-license distinction remains; no license changes |
| B: no new engine/dependency | **PASS** — package and lockfiles unchanged, existing Node/TypeScript/Vite/Python only |
| C: full 3–5 minute solo battle | **N/A** — headless five-turn rules experiment; no human session duration claimed |
| C: understandable enemy actions | **PASS mechanics** — reason events, five stance traces and deterministic matrix explain approach/blocked/contribute; no human readability evidence |
| C: player can win/lose | **PASS** — search counts and asserted stance outcomes, P0 retry regression |
| C: two tactical choices change outcome | **PASS outcome difference / FAIL depth** — idle fails and one-tile retreat succeeds; FAIL is the measured purpose of P0b, not an unexplained acceptance gap. Existing encounter should not be treated as tactically validated |
| C: retry/change strategy | **PASS (regression)** — original P0 test 7 and unchanged retry fixture, exit 0 |
| C: duplicate/stuck/invalid paths | **PASS tested rules / N/A animation** — P0 guards, P0b bounds and contention tests; blocked units intentionally wait rather than hanging the resolver |
| C: 720p/1080p/keyboard | **N/A** — no UI change or playable UI claim |
| C: automated vs human evidence | **PASS** — all evidence headless/machine; no human playtest or Owner acceptance |
| D: SRD/CC-BY/rule contract | **N/A adaptation / PASS no new IP** — original provisional occupancy only; no copied SRD/WotC text, third-party art or formal-rule change; missing contract remains a historical limitation |
| D: AGENTS authorization | **PASS** — only P0b and explicit bounds fix; own codex branch/worktree; proposals only, no story/Ink, P1, main edits/merge, PR, stash, deploy, Actions or new agents |

Open questions for Gavin: whether to authorize testing any of the three
proposals; none is selected or implemented. For later independent review:
check counting/dedup boundaries and whether the timer-delay explanation
matches JSONL events. No review agent was started in this continuation.

## Historical P0 evidence (superseded where P0b above updates it)

The following original P0 report, tests, time and failed push are historical.
They are not the current P0b delivery status or a claim of tactical depth.

## 1. What changed

- `ui-prototype/src/playable-l03/rules.ts`: isolated pure state machine, one
  MapDef reusing the existing 11×9 terrain, winch (2,1), fixed west deployment,
  legal/rejected move commands, deterministic enemy intents/movement,
  progress, terminal outcomes and retry. Nothing imports this into the UI.
- `ui-prototype/src/playable-l03/README.md`: pre-code question, keep/stop
  criteria, provisional rules and exact scope of the reduced PoC.
- `ui-prototype/tests/playable-l03-p0.mjs`: eight headless checks; freezes
  input, deep-compares rejected commands, verifies reachability, passage,
  turn guards, failure precedence, blocked AI, replay and retry.
- `ui-prototype/docs/playable-l03-p0/{success,failure,retry}.jsonl`: original
  commands, events and states, checked byte for byte on every normal run.
- Shared files edited: `ui-prototype/PLAN.md`, `memory/01_active_task.md`.
  Own locks acquired before editing, required fetch/pull performed, SHARED-EDIT
  output printed, and Shared-file trailers added to implementation commit.
  Own locks released at task handoff after the attempted push. No other
  agent's worktree or lock was edited. No additional model agents were started.
- The requested merge imported upstream coordination/checklist documents;
  local `main` was neither checked out nor advanced.

## 2. How to verify

Run from the repository root in Windows PowerShell, using existing tools only.

| Command | Expected | Observed exit code and result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs --write-traces` | Generate the three fixtures and pass | **0**, 8 PASS |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | Recompute without writing; exact fixture comparison | **0**, 8 PASS; hold success progress 1, idle failure progress 4 |
| `npm run build --prefix ui-prototype` | TypeScript and Vite build | **0**, 46 modules transformed |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | Existing scope protection | **1** in sandbox: interpreter inaccessible; **0** on approved retry using the same existing interpreter; 13 planning files checked |
| `git diff --check` | No whitespace errors | **0** |
| `git diff --cached --check` | Staged whitespace check | **0** |

An initial inline Node smoke probe did not run: PowerShell stripped the inline
JavaScript quotes (`SyntaxError: Unexpected token '.'`, exit **1**). It was
replaced by the checked-in test file, whose generation and read-only replay
commands above both returned **0**. Exact failed probe invocation:

```powershell
node --experimental-strip-types --input-type=module -e 'import {initialState,command,resolve} from "./ui-prototype/src/playable-l03/rules.ts"; let s=initialState(); for(let t=1;t<=5;t++){ for(const [unit,to] of (t===1?[["lace",{x:1,y:1}],["thoma",{x:2,y:2}],["karen",{x:3,y:3}]]:t===2?[["karen",{x:3,y:1}]]:[])){let r=command(s,{type:"move",turn:s.turn,unit,to}); if(!r.ok) throw Error(r.reason);s=r.state;} let r=resolve(s,s.turn);s=r.state; console.log(JSON.stringify({t,s,events:r.events})); if(s.status!=="playing")break;}'
```

Git delivery evidence: `git fetch origin` **0**, initial `git pull --ff-only`
**0** (`704c106` → `d0f4005`); `git merge origin/main` initially **1** because
the sandbox denied `.git/ORIG_HEAD.lock`, then **0** with approved Git write
access (no conflict). Shared-edit fetch/pull **0**, already up to date.
Implementation `git add` **0**, `git commit` **0**, hooks ran normally.
Pre-push fetch **0**, `git log --oneline HEAD..origin/codex/playable-l03-research`
**0**, empty: no unknown remote commits. `git push origin codex/playable-l03-research`
**1**: failed to connect to `github.com` port 443. No force, hook bypass,
credential change, PR, deployment or Actions. Per Owner fallback, retain local
commits rather than escalating the failed network push.

Screenshots / recordings: **N/A**, P0 explicitly has no UI. No browser or human
playtest is claimed. Existing presentation paths were not changed.

### Acceptance 1–6

| # | Result | Evidence and limits |
| --- | --- | --- |
| 1 | **PASS** | Test 1: west winch (2,1), both route modes' identical fixed PoC deployment has no overlap, every spawn walkable/reachable, each ally can reach winch; sealed allies reach wagon and its entire (8,4)→(0,4) corridor is walkable. Open intentionally cannot reach east wagon across broken bridge. Tests/traces check every movement path for orthogonal steps, water/bridge exclusion and every resulting state for overlap. |
| 2 | **PASS** | Tests 2–3: deterministic legal commands, frozen inputs and deep-equal rejected state; bounds, water, broken bridge, occupied target, excess steps, repeat move, wrong actor and stale turn rejected. Single `blockAlliedPassage` flag defaults true. |
| 3 | **PASS** | Test 4: `resolve(state, expectedTurn)` returns synchronously, no React/animation/timers; stale turn rejected. Sealed resolution explicitly rejects as map-only. |
| 4 | **PASS** | Tests 5–6: phase-start adjacent enemies increase progress, arrival does not immediately increase it, blocked enemies return a bounded wait intent; holding changes approach paths and progress. Idle loses, hold wins with blocking ON. |
| 5 | **PASS** | Tests 6–8 and three committed `.jsonl` traces: success, failure, retry/change strategy; independent reruns deep-equal and fixture bytes match. |
| 6 | **PASS** | Baseline/merge/implementation SHAs and measured time above, real commands/exit codes, filled resource checklist below; handoff committed separately. Push failure explicitly preserved. |

## 3. Not done / known limits

- **P1–P6 not started.** No UI, new art, story edits, Attack/Support, damage,
  reinforcements, boat simulation or full sealed-route escort logic. Both route
  modes deliberately share one fixed five-unit PoC deployment; they are not
  claimed as the final distinct encounter rosters.
- The reviewed spec's full five-knight encounter is not implemented. P0 uses
  only its two initial knights with blocking interference, as allowed by the
  task's minimal-enemy scope. No assertions of full-spec battle balance.
- QR-11 (open gate's dominant choice) remains known. Rewards, plot and K1
  costs were not changed. G005/SRD adaptation is not implemented.
- Browser resolution/keyboard checks and a 3–5 minute uncoached human battle
  remain unverified and out of this explicitly headless P0.
- Implementation and handoff are local because the normal network push failed.
- The existing hook emitted advisory `missing_canonical_memory` with
  `completion_claim_allowed=True`; commit succeeded. Task DONE is not SessionEnd;
  no canonical daily closeout was manufactured.

## 4. Risks

- Blocking without attacks proves a solvable occupancy mechanic, not tactical
  depth or the full spec's difficulty. A later authorized implementation must
  revalidate its actual roster, reinforcements and combat rules.
- The default passage choice is provisional; tests prove solvability for both
  flag values without deciding the final rule. AI path ties are fixed N/W/E/S.
- `docs/design/RULE-ADAPTATION-CONTRACT.md` referenced by the resource checklist
  is absent on this branch and the read-only review branch (checked via
  `git show`, exit **128**). No SRD or official-rule changes were attempted.

## 5. Open questions

- For Claude/GPT review: check that this deliberately reduced fixed-deployment
  hold proof meets P0, especially the phase-start progress timing and the
  distinction between sealed map reachability and unimplemented escort victory.
- For Gavin: P1 remains unauthorized; no decision is presumed. Failed delivery
  is local-only until a separately available normal push succeeds.

## 6. Not claimed

Owner acceptance, human playtest, fun/production keep, commercial art approval,
native hook callback, full SRD/G005 rules, complete playable encounter, full
sealed-route win, remote publication, main merge, PR and session end are not
proved by this handoff. Engineering keep means only retain this isolated P0
module for review; it does not authorize more work.

---

## Review

Claude writes findings in `docs/review/codex-playable-l03-research.md` on its
review branch. Codex stops after this P0 handoff.

## Resource self-check

Checklist source: `docs/review/RESOURCE-CHECKLIST.md` from merged `origin/main`.
Each N/A below is an explicit P0 boundary, not a claim of future completion.

### A. Skills (read only relevant SKILL.md; do not install)

Re-read all three relevant cached original SKILL.md files from
`gamedev-skills/awesome-gamedev-agent-skills` fixed commit
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`; SHA256 matched the existing
`ui-prototype/docs/playable-l03-research/source-manifest.json`:
prototype-fast `02491395c621833d2252f7a33a96aa11f26eb48523fea167c68272fb3c785ba1`,
level-design `f1656cb00b9af8dc625a9655448b410b37ce6f1e523048a5abf09fda25cbfd32`,
game-ai `ef23a6440743b3583d1072c92f6b0b45f3d11df33b3b77db53bce8b82c2f8940`.

- **PASS — prototype-fast (P0):** simplest isolated occupancy loop; question,
  retention choice and keep/stop conditions stated in README before tests/code
  completion. 60-minute cap, actual time above. Human fun signal remains N/A.
- **PASS for P0 / N/A full branch wins — level-design (P0):** Test 1 verifies
  terrain, placements, winch and sealed critical path; tests 6–8 prove an open
  win. A sealed win is explicitly outside P0, not silently treated as passed.
- **PASS — game-ai (P0):** shortest reachable winch-adjacent target reacts to
  occupied player tiles; stable ties, reason events and blocked fallback;
  tests 5–6 and success/failure traces expose the decisions.
- **N/A — game-ui-ux (P1):** no UI in P0; move/threat/intent visibility is not implemented.
- **N/A — game-feel (P1):** no animation, hit reaction or pacing in P0.

### B. Reference repos (architecture only; never copy unlicensed code or art)

- **PASS — franciscobom/Grid-Tactics (no license; read-only):** pure resolver
  returns state/events with no rendering or async execution; rule source and
  test 4. Prior architectural reading pinned at
  `8d1952b46c771318b6f798b44038bac4490afe64` in source-manifest; no external
  source or assets copied, no new execution of that repo.
- **N/A reuse / PASS separation — HopeMetal/2DTacticalRPGDemo (MIT):** no code
  or assets borrowed. Prior source-manifest pins
  `c58849b67a89897ecdb6b3dbb7f25183d3be96ac`: code MIT and images separately
  CC-BY-SA 3.0; no root-MIT assumption for images. Original implementation only.
- **PASS — no new engine or dependency:** package/lockfiles unchanged, only
  existing Node type stripping, TypeScript/Vite and pinned Python used.

### C. Playable acceptance bar

- **N/A — full 3–5 minute solo battle:** P0 headless mechanism only; not claimed.
- **PASS — understandable enemy actions:** reason events, phase-start progress,
  predictable shortest approach; tests 5–6 and both outcome traces.
- **PASS — player can win or lose:** fixed hold succeeds and idle loses; test 6.
- **PASS — tactical choices give different outcomes:** reposition versus idle
  changes enemy paths and progress, using identical deployment/config; test 6.
- **PASS — restart/change strategy:** failure→retry→hold success; test 7/retry trace.
- **PASS for P0 / N/A animations — no duplicate resolution, stuck turns or
  invalid moves:** stale turn guard, bounded BFS, blocked fallback, frozen input
  and rejection checks; tests 2–5. No animation system exists in this module.
- **N/A — 1280×720 / 1920×1080 and keyboard:** no UI in authorized P0.
- **PASS — automated/human evidence separate:** eight Node tests and build/scope
  are machine checks; no human playtest or model approval substituted.

### D. Project rules

- **N/A SRD adaptation / PASS no WotC content:** all occupancy/hold values are
  original provisional PoC rules. No SRD text, WotC IP, commercial art or new
  third-party code included. Missing rule-contract path is recorded above;
  no formal adaptation or attribution claim is made.
- **PASS — authorized scope:** task P0 only, own branch/worktree, requested
  merge of origin/main into this branch, no merge into main, no story/setting
  changes, no P1, no stash, no PR/deploy/Actions. Scope validator exit **0**.
