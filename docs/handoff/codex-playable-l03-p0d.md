# Handoff: codex/playable-l03-p0d

## P0d

**Recommendation: retain A+D as an opt-in candidate for Owner review.** It
removes every tested T1-deploy-then-wait win while preserving multiple winning
lane/reposition groups. A also meets this round's bounded OK criteria once its
missing three-command search is completed; D alone remains CHEESE. None becomes
the default. P0d ends here; no P1/P2, main merge or PR is authorized by this result.

The new finding is modest but concrete: the cheapest A and A+D wins need a
second-turn reposition, rather than only first-turn deployment. They still
wait on turns 3–6, exploit deterministic enemy routing, and do not trigger D's
breakout. Thus **OK means the stated P0d search gates pass, not that sustained
tactical depth, fun, or a production combat design has been proved**. D removes
static alternatives; it did not create the new cheapest dynamic strategy.

| Field | Value |
| --- | --- |
| Branch / own worktree | `codex/playable-l03-p0d` / `D:\campaign-forge\scratch\p0d` |
| Owner-named base | `13a6e17496dca1eaa8d3a98fe459dc819b37e8a4`; clean at start |
| Implementation commit | `cafe688143ad53dbc16d9a256592f8ddc683d060`, normal commit **0**, pushed **yes** |
| Handoff head / delivery | Implementation `git push -u origin codex/playable-l03-p0d` returned **0** and created only the authorized branch. This file follows in a separate documentation commit on that branch; final handoff SHA and remote-head confirmation are reported in the final response rather than a self-referential SHA. |
| Owner instruction | Only `docs/tasks/playable-l03-P0d-pressure.md`, 60-minute timebox; separate worktree, read-only junction, dedicated handoff; normal commit then try `git push -u origin codex/playable-l03-p0d`; on failure leave commits local; no P1/P2/main/PR/stash |
| Parallel coordination | Owner identifies the other Codex session in the main checkout on `codex/playable-l03-research`; this session uses only the newly assigned P0d worktree. No additional model agents started. |
| Time window (Asia/Taipei) | Start approximately **2026-10-22 17:28:09**; first recorded clock 17:28:13 after initial 3.6-second read/status batch. Both accepted searches complete by 17:56:47; implementation pushed before 17:58:50; handoff prepared at 18:00 (about **32 minutes**). Final commit/push overhead and elapsed time are in the final response; maximum 60 minutes. |

### Comparison

W/L counts named search spaces, not player win rates. Cost display is
**voluntarily moved allies / commands / path tiles**; ranking prioritizes
commands, then allies, then tiles. All three allies remain present in the
full-party searches, including unmoved blockers. Their absence is tested
separately. Overlapping spaces are not summed.

| Variant | Turn-1-then-wait W/L | Max-one-move W/L | Min-cost win (units/moves/tiles) | Original P0 success trace still wins? | Lace (0,3) cheese still wins? | Solo wins? | Duo wins? | Distinct winning strategy families | All best wins are T1-then-wait? | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A (6 turns) | 5/6791 | 0/217 | **2/3/5** | Yes, progress 2 | No | None found; no cap hit | None found; wider probe capped | **15** | **No** | **OK (bounded)** |
| D (5 turns) | 434/6362 | 6/211 | **1/1/1** | Yes, progress 2 | Yes, progress 2 | 3/3 lineups | 3/3 lineups | **131** | **No** | **CHEESE** |
| A+D (6 turns) | 0/6796 | 0/217 | **2/3/5** | No, legal loss at T6, progress 4 | No | None found; no cap hit | None found; wider probe capped | **8** | **No** | **OK (bounded)** |

Family totals are the union of the four full-party spaces, grouped by **which
living ally finishes in which lane and whether any voluntary move is after
T1**. Lanes: y>3 rear; otherwise y=0 north, x<=1 west, x=2 south, x>=3 east.
Within-lane tile and timing differences are merged; forced swaps alone do not
count as player repositioning. These coarse spatial groups can overstate
meaningful tactical diversity. Both A and A+D have six tied cheapest sequences,
all after T1 and all in the **same rear-delay family**; they do not have six
distinct best tactics. Other winning groups cost more.

| Variant | <=2 moves TOTAL, <=2/turn W/L | <=3 moves TOTAL, <=2/turn W/L | Families within <=3-total space | Cheapest tested T1-only win |
| --- | --- | --- | --- | --- |
| A | **0/24922** | **223/1855320** | 11 | 3/3/8 |
| D | **942/23726** | **80897/1727080** | 98 | 1/1/3 |
| A+D | **0/24922** | **109/1853529** | 8 | None |

Both multi-move searches are exhaustive within their stated bounds: no beam,
state cap or transition cap. The optional extension to three total moves was
feasible and completed for all three variants and every reduced lineup. T1
space separately includes three commands on T1; the multi space allows only
two per turn. This is not enumeration of every 10/12-command battle.

### Why these verdicts

- **A — OK within the declared gates.** The missing two-command search finds
  no win; three-command search finds 223 wins out of 1,855,543 sequences.
  Every cheapest sequence needs a later command. Five static wins remain, but
  their cheapest costs 3 allies/3 commands/8 tiles, meeting the declared
  costly-T1 threshold. There are at least two spatial/reposition groups, and
  the original P0 trace still succeeds. This supersedes P0c's incomplete
  3/3/8 minimum, not Owner's decision to keep A merely a candidate.
- **D — CHEESE.** Lace T2 (1,3)→(0,3), just one tile, still wins. A later
  action and many spatial families do not make this low-cost wait exploit
  a meaningful combat challenge. The 434 static wins also fail the costly-T1
  gate. The exact two-turn pressure rule is documented below.
- **A+D — OK within the declared gates.** No static or <=2-command win;
  109/1,853,638 three-command sequences win, distributed across eight groups.
  Every cheapest sequence needs a later move. The original trace's loss has
  a direct cause: knight-2 waits blocked on T3, swaps Thoma from (2,2) to
  (2,3) on T4, then both knights contribute on T5 and T6. Progress is
  **0,0,0,0,2,4**; loss takes precedence at the six-turn deadline. In D's
  five-turn version, the same trace ends before the second contribution and
  still wins with progress 2.

The OK gates were declared in the search code before running it: no T1 win or
minimum T1 cost >=3 commands/3 allies/8 tiles; >=2 groups; wins <50% in each
exact space with wins; some cheapest win after T1; original trace legal with
explained outcome. No human fun rating is inferred from these thresholds.

### Cheapest wins and distinct examples

**A and A+D, 2 allies / 3 commands / 5 tiles:** T1 Karen (2,5)→(1,5),
Lace (1,3)→(3,4); T2 Karen (1,5)→(2,5); wait T3–6. Thoma stays at (1,4).
Karen's return makes knight-1 backtrack to the west approach. Knight-2 is
blocked only once and subsequently routes around, so D never fires. Both end
with progress 2. This is timing/route manipulation, not continuous defense.

Two other A+D winning groups, each **2 allies / 3 commands / 8 tiles**:

| Lane roles at end | Commands | Cost/tradeoff |
| --- | --- | --- |
| Karen east, Lace west, Thoma south | T1 Thoma→(3,3); T3 Thoma→(2,2), then Karen→(3,3) | Three more path tiles than the cheapest rear-delay family; exchange east/south coverage on T3 |
| Karen south, Lace west, Thoma east | T1 Karen→(3,3); T3 Karen→(2,2), then Thoma→(3,3) | Same cost with different lane owners; Lace remains an unmoved west blocker |

Both witnesses and their visible enemy/progress consequences are replayed in
`ui-prototype/docs/playable-l03-p0d/witnesses.jsonl`. They demonstrate different
assignments with explicit cost; they do not prove an uncoached player would
recognize or enjoy them. D's cheapest full-party win is the one-tile Lace
retreat already listed.

### Solo/duo completion and limits

All absent allies are removed rather than left as invisible blockers. Each
lineup receives T1, <=1 total, exact <=2 total and exact <=3 total searches.
The additional wider search allows **<=2 commands per turn**, no total cap,
up to **10,000 retained states and 250,000 examined transitions per turn**.
It includes counter history and the previously moved-unit set in deduplication.

All solo searches complete without truncation. All duo wider searches hit the
**transition** cap from T3 onward; none hits the retained-state cap. Therefore
no-win duo results do not exclude four-or-more-command wins. Every existence
claim below has an independently replayed legal witness.

| Variant / lineup | Exact <=3-total W/L | Cheapest win found (units/moves/tiles) | Wider search truncated? |
| --- | --- | --- | --- |
| A / Karen | 0/42127 | None | No |
| A / Lace | 0/38625 | None | No |
| A / Thoma | 0/41058 | None | No |
| A / Karen+Lace | 0/618624 | None | Yes |
| A / Karen+Thoma | 0/624573 | None | Yes |
| A / Lace+Thoma | 0/520406 | None | Yes |
| D / Karen | 0/42127 | **1/4/9** (wider search) | No |
| D / Lace | 4/38621 | **1/3/6** | No |
| D / Thoma | 4/41054 | **1/3/7** | No |
| D / Karen+Lace | 3897/613387 | **1/2/5** | Yes |
| D / Karen+Thoma | 3744/619515 | **1/2/4** | Yes |
| D / Lace+Thoma | 6608/511464 | **1/2/4** | Yes |
| A+D / Karen | 0/42127 | None | No |
| A+D / Lace | 0/38625 | None | No |
| A+D / Thoma | 0/41058 | None | No |
| A+D / Karen+Lace | 0/618624 | None | Yes |
| A+D / Karen+Thoma | 0/624573 | None | Yes |
| A+D / Lace+Thoma | 0/520406 | None | Yes |

D's cheapest solo is Lace, 1/3/6: T1→(1,2), T3→(3,1), T4→(1,1).
Cheapest duo cost ties at 1/2/4: Karen+Thoma uses Thoma T2→(3,4),
T3→(1,4); Lace+Thoma uses Lace T1→(3,2), T3→(2,2). Full per-lineup T1,
one/two/three-command counts, layer widths, cap flags and commands are in JSON.

## 1. What changed

- `ui-prototype/src/playable-l03/rules.ts`: optional `p0d` pressure config,
  per-enemy consecutive blocked count and one deterministic breakout event.
  Default config and P0/P0b/P0c serialized behavior remain unchanged.
- `ui-prototype/tests/playable-l03-p0d-{support,search}.mjs`: exact searches,
  wider lineup probe, cost ties, spatial family classification and reports.
- `ui-prototype/tests/playable-l03-p0d.mjs`: nine tests, original-algorithm
  cross-check, replay/cost/bounds/occupancy assertions and byte comparison.
- `ui-prototype/docs/playable-l03-p0d/`: rule/method README, full JSON results,
  representative replay JSONL and execution evidence.
- This dedicated handoff is the task-local milestone record. **Shared files
  edited: NONE.** The research handoff, `ui-prototype/PLAN.md`, shared memory
  01/02, story and decisions remain untouched. Their prescribed lock path is
  outside this Owner-constrained worktree; no outside lock or shared edit was
  attempted. Coordinator reconciliation is an open question, not silently
  performed during the parallel task.

D's exact minimal rule: after N consecutive blocked enemy phases (N=2 here),
plan the shortest winch-neighbor route ignoring allies but still blocking on
other enemies. Take up to three steps; on the first ally encountered, swap it
into the preceding cell and stop. Reset the streak after normal movement,
contributing, or a performed breakout; if no breakout path exists, wait with
the streak saturated at N. N/W/E/S ties, phase-start progress and loss-first
terminal precedence remain unchanged. No HP, attack, new objective or UI.

## 2. How to verify

Run from the P0d root. Full commands, environment failures/recovery and hashes
are in `ui-prototype/docs/playable-l03-p0d/VERIFICATION.md`.

| Command | Expected | Actual exit |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0d-search.mjs` (twice, explicit native-exit capture) | Exact report bytes | **0 / 0**, matching SHA-256 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0d.mjs` | 9 PASS; exact witnesses | **0** |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | Original 8 PASS | **0** |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | Original 9 PASS | **0** |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | Original 9 PASS | **0** |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs` | Original JSON byte-identical | **0** |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c-search.mjs` | Original JSON byte-identical | **0** |
| `npm run build --prefix ui-prototype` | Build succeeds | **0** |
| Existing Python 3.12 executable + `scripts/validate_ui_scope.py` | Protected scope passes | **0** after pinned submodule checkout; earlier failures retained in verification log |
| `git diff --exit-code 13a6e17 --` original P0/P0b/P0c test/support/search/evidence paths | No changes | **0** |
| `git diff --check` | No whitespace errors | **0** |

Screenshots/recordings/720p/1080p/keyboard: N/A, expressly headless P0d.
The first generating search wrapper returned 1 and did not capture native exit;
it is not passed off as one of the two successful acceptance runs.

Delivery evidence: implementation `git add`, staged whitespace check and normal
commit all **0**. Required pre-push `git fetch origin` **0**; the P0d remote
branch did not previously exist, so no unknown remote commits were incorporated.
Normal push **0**, no force or hook bypass. The existing pre-commit advisory
reported `missing_canonical_memory`, `completion_claim_allowed=True`; task DONE
is not SessionEnd, so no daily closeout was manufactured. The existing shared
pre-push hook passed its JSON-object inventory and ran framework self-smoke /
advisory checks. Its output named `D:/campaign-forge/ai-governance-framework`
as framework/smoke root and this P0d worktree as target; this inherited hook
execution is distinct from this session's own source edits and is **not** a
claim of P0d-native callbacks or complete governance adoption. No hook, global
trust or main-checkout source was manually changed. A later sandbox
`git ls-remote` inspection failed to connect (1); it does not negate the
successful push, and final remote verification uses the approved Git access.

## 3. Not done / known limits

- No P1/P2, UI, art, animation, HP, attacks, story, engine, new package or
  formal rule adoption. The sealed-route escort remains outside this PoC.
- No unrestricted all-turn multi-move enumeration. Duo no-win results remain
  capped; no party-size balance or optional-companion robustness is claimed.
- The cheapest A/A+D win uses all three bodies, only two voluntarily moving.
  All six cheapest ties belong to one family, never trigger breakout and wait
  from T3 onward. This is a substantial limit on any claim of tactical depth.
- Family counts classify final lane ownership, not independent tactical value.
  Tests/build do not validate fun, human comprehension or commercial quality.
- No shared PLAN/memory edit; this branch-specific report carries the milestone
  pending coordinated reconciliation. Task DONE is not SessionEnd.

## 4. Risks

- D only reacts to **consecutive no-path/no-step** states. Long detours and
  alternating blocked/unblocked phases evade its threshold, as the cheapest
  witness demonstrates. Increasing difficulty is not itself better gameplay.
- The costly-T1 threshold is explicit but provisional. A's OK rating depends
  on that definition; A+D's zero static wins is the stronger observation.
- The new optional fields/events may require reconciliation if P1v independently
  edits `rules.ts`; no merge into that branch or worktree was attempted.

## 5. Open questions

- For Claude/GPT review when Owner requests it: audit the lane-family grouping,
  cost tie tracking, no-cap three-command enumeration, and the distinction
  between bounded OK and genuine sustained play. Review input is not approval.
- For Gavin: decide whether to retain A+D as an experimental candidate, given
  the cheapest route-delay exploit and unresolved reduced-party results. This
  recommendation grants no next-phase authority and changes no default.
- For the coordinator: reconcile this milestone into shared PLAN/memory using
  the normal single-writer lock after the parallel tasks, if desired.

## 6. Not claimed

Owner acceptance, adopted story/combat rules, human playtest, commercial art
approval, complete playable battle, complete solo/duo balance, native governance
callbacks, canonical session closeout, main merge, PR, deployment and Actions.
Remote delivery is claimed only if the actual push succeeds.

## Resource self-check

Source: `docs/review/RESOURCE-CHECKLIST.md`. P0d-only N/A boundaries are explicit.
The three relevant public SKILL.md files were fully reread at fixed commit
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`; downloaded bodies stay in ignored
`scratch/p0d/`. Hashes match the existing source manifest:

- prototype-fast: `02491395c621833d2252f7a33a96aa11f26eb48523fea167c68272fb3c785ba1`
- level-design: `f1656cb00b9af8dc625a9655448b410b37ce6f1e523048a5abf09fda25cbfd32`
- game-ai: `ef23a6440743b3583d1072c92f6b0b45f3d11df33b3b77db53bce8b82c2f8940`

### A. Skills

- **PASS — prototype-fast:** single question, declared keep/stop gates,
  60-minute cap, minimal original headless experiment; search header/README.
  Human fun/playtest part N/A under the narrower verification-only instruction.
- **PASS bounded verification / depth unproved — level-design:** unchanged
  map/placement reachability regressions pass; all reported winning witnesses
  replay; exact two/three-command and bounded reduced-party searches disclosed.
  Sealed-route win N/A; no claim that final lane groups prove tactical quality.
- **PASS program behavior — game-ai:** deterministic target/path/swap events,
  state-based consecutive pressure, bounded fallback, no early contribution;
  new tests 1–5 and original-P0 trace explanation. Human readability N/A.
- **N/A — game-ui-ux:** UI is prohibited in P0d.
- **N/A — game-feel:** no hit reaction, animation or pacing work authorized.

### B. Reference repos

- **PASS — Grid-Tactics separation:** existing pure state/events boundary
  retained, no view import or async resolver; original tests and build pass.
  Historical reference pin `8d1952b46c771318b6f798b44038bac4490afe64` remains
  read-only, license unconfirmed. No code or assets copied or executed.
- **N/A reuse / PASS license separation — HopeMetal/2DTacticalRPGDemo:** no
  code/assets borrowed. Existing pin `c58849b67a89897ecdb6b3dbb7f25183d3be96ac`
  records MIT code separately from CC-BY-SA 3.0 images; not treated as all MIT.
- **PASS — no new engine/dependency:** package and lock unchanged, junction
  read-only; existing pinned governance submodule checked out only to run the
  repo-required validator, not updated or newly added as a dependency.

### C. Playable acceptance bar

- **N/A — full 3–5 minute uncoached battle:** expressly verification only.
- **PASS program layer — understandable enemy actions:** deterministic intent,
  breakout event with displaced cell, and per-turn progress; tests 2–5. Human
  readability remains unverified.
- **PASS — win/lose outcomes:** all three variants have replayed wins and losses;
  counts and original trace rows above.
- **PASS bounded differing choices / sustained depth unproved:** alternate lane
  roles and second/third-turn movement change outcomes; six cheapest A/A+D
  sequences still share one route-delay family. This qualification is not
  omitted or equated with human tactical enjoyment.
- **PASS — restart/change strategy:** original P0 regression plus new test 5
  verifies D config retained and pressure reset on retry.
- **PASS tested rules / N/A animation — no duplicate resolution, stuck turns,
  invalid moves:** original guards plus frozen-input and deterministic swap,
  per-witness collision/terrain/cost/bounds checks; finite fallback.
- **N/A — 720p/1080p/keyboard:** no UI change, per P0d scope.
- **PASS — automated/human evidence separate:** real machine exits and byte
  comparisons recorded; no human playtest or model approval substituted.

### D. Project rules

- **N/A formal SRD adaptation / PASS no copied IP:** original provisional
  occupancy experiment only. No WotC text, art or third-party code added.
  The checklist's rule-adaptation contract is not introduced or altered.
- **PASS — authorized scope:** dedicated Owner-named worktree/branch/handoff,
  no other worktree edits, no shared-file lock outside it, no package install,
  P1/P2/story/main/PR/stash/deploy/Actions/force/hook bypass. Scope validator 0.

## Review

Claude/GPT review, when requested by Owner, belongs on the separate review
branch. Neither this self-check nor a later model review is Owner approval.
