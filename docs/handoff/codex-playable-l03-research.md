# Handoff: codex/playable-l03-research

P0 proves that repositioning can protect the relocated west-bank winch: the
fixed hold trace survives five turns with progress 1, while doing nothing
loses on turn five with progress 4. Retrying the loss and changing strategy
reproduces the success. This is a headless rules proof, not a playable UI or
the full reviewed encounter. The normal push failed; commits remain local.

| Field | Value |
| --- | --- |
| Branch | `codex/playable-l03-research` |
| Base | Task baseline `d0f400500d60d013d7d95c2bc97c12387d22baaf` after requested fast-forward pull |
| Merged origin/main | `aea2af7e400b446ea84a610fac75edd9664218f9`; merge `f80677d21c2f928d7add7fda81482ad6e1e97cf6` |
| Implementation SHA | `4e6d0d8a27c02ec04d8e1178310ce472fc0e6ef1` (pushed: no) |
| Head | This handoff is a separate local documentation commit after the implementation SHA; obtain its exact SHA with `git rev-parse HEAD`. No self-referential SHA is asserted. |
| Owner instruction | Only `docs/tasks/playable-l03-P0.md`, 60 minutes maximum, pure TypeScript, acceptance 1–6, resource self-check, commit and attempt normal branch push. No P1, main changes, PR or stash. |
| Time window (Asia/Taipei) | Start `2026-10-22T10:48:56+08:00`; implementation commit `2026-10-22T10:54:38+08:00` (5m42s). Handoff evidence freeze `2026-10-22T10:56:18+08:00`; elapsed `7m22s`, including setup, tests and failed push. Final commit overhead follows this freeze and is reported in the final response. |
| Review input | Read-only `origin/review/quality-gameplay-audit` @ `211594279fb48add8fd7cb524122b6e536398812`, `ui-prototype/docs/quality-review/L03-PLAYABLE-SPEC.md` via `git show` |

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
