# Handoff: codex/playable-l03-research

## P1v4 art pass

This is the latest chunk. All earlier P1v/P1v2/P1v3/P0 sections below describe
historical deliveries. The scope here is presentation only: replace the tiled
ground and geometric props, distinguish the knight portraits, and enlarge
figures without breaking the retained input/overlap contracts.

| Field | P1v4 |
| --- | --- |
| Branch / own worktree | `codex/playable-l03-research` / `D:\campaign-forge` |
| Owner-named baseline | `f1e0ab627e92e68c726c3cdef47c08735cd70831`; clean, exclusive worktree confirmed by Owner; no pull |
| Implementation | **`8bd06dbb870f406ff76ceffe531027cb44ec3187`**, normal commit exit 0, **pushed successfully** |
| Push | `git push origin codex/playable-l03-research` exit **0**, remote `f1e0ab6..8bd06db`; hooks enabled |
| Owner instruction | Only P1v4 art, 120-minute cap; built-in image_gen allowed; rules.ts/packages/P2/P0d untouched; commit and try push; no main/PR/stash |
| Time, Asia/Taipei | Start **2026-10-22 20:34:40**; implementation push confirmed **21:07:49** = **33m09s**. This handoff is a separate documentation commit. Its final SHA, push result and total elapsed are reported in the final response. |

### 1. What changed visually

- One continuous original painted ferry landscape replaces 99 repeated material
  diamonds. The exact original grid sits over it; idle lines are hidden, legal
  ranges/hover/focus/selection remain visible, and intent arrows are unchanged.
- Built-in generated alpha props replace the SVG winch, wooden bridge ends and
  wagon chassis. Original coordinates remain winch (2,1), wagon (8,4),
  surviving bridge ends (3,4)/(6,4). The river gap stays open and impassable.
- The second knight now has a distinct open-face kettle-helmet portrait;
  all five portrait signatures are unique. Battlefield knight bodies remain
  the existing closed-helmet figure, a known visual mismatch.
- Common figure viewport increased from 50 to 52 scene units. A tighter knight
  crop removes unused space/neighboring creature fringe, making the visible
  knight art about 24.7% taller; party art is 4% taller.
- **Shared-file: `ui-prototype/PLAN.md`** and
  **Shared-file: `memory/01_active_task.md`**. Both were edited under Codex-owned
  locks, with SHARED-EDIT output and matching commit trailers. Initial and
  pre-push fetches showed no unknown commits on this branch. Owner's no-pull
  instruction overrides the default shared-file pull step.
- No original PNG bytes, rules, story/Ink, dependencies, older UI logic,
  P0/P0b/P0c fixtures or other worktrees were changed.

### Assets generated / rejected

All originals: `ui-prototype/public/art/l03-p1v4/`. Built-in image_gen only.
Full prompts/date: [art-prompts.json](../../ui-prototype/docs/art-prompts.json).
Full hashes/dimensions: [art-manifest.json](../../ui-prototype/docs/art-manifest.json).

| Original | Use | SHA-256 |
| --- | --- | --- |
| `battlefield.png` | Used, guide-aligned single painting | `8c42a5e46952a85db4bce232ac8b3463090a1ddc0f3bf65b25bcea6031e713c5` |
| `props.png` | Used, winch / broken bridge / wagon transparent atlas | `8f9e678bd048cffe67c9d1f384b6cb0a3ae53cf4d306fa5262019787ac0d16cf` |
| `knight-2-portrait.png` | Used, distinct second knight portrait | `419984a8c18c6a25341857a61ca29e3cc15137c88a0eae2368bc7717dde58019` |
| `battlefield-attempt-01.png` | **REJECTED**, river too wide / bridge layout displaced; original retained | `dceaf33a86eda498f3a44c82be53bc5c1d1347c8a7e69bfcc3bd6bf792f4530b` |

The source-authored geometry guide is explicitly a diagram, not a game
screenshot. The accepted painting was regenerated from that guide, preserving
the original camera. Runtime crops/masks do not modify PNG bytes. Existing
party/enemy art is reused unchanged. No commercial/reference-game imagery.

### Scale exception, with actual failure evidence

1.3 full diamond heights = 67.6 units. Running the unweakened P1v2 browser
suite failed `figures overlap: lace/thoma`, exit **1**. The original report
and screenshot are in
[rejected-scale-1.3](../../ui-prototype/docs/playable-l03-p1v4/rejected-scale-1.3/after-results.json).
The winch cluster also has same-screen-X foot positions only 52 units apart.

Final common viewport: **52 / 52 = 1.00 tile**. This is the geometric
zero-overlap maximum, not an assertion that the 1.2–1.5 target was met.
Visible pixels measured with alpha ≥128: **0.95973–0.97890 tile**.
Viewport screen height is **39.31px at 720p / 66.98px at 1080p**.
Feet, depth sort and tile-only hit areas are unchanged; no tolerance/behavior
assertion was relaxed. See [STYLE](../../ui-prototype/docs/playable-l03-p1v4/STYLE.md).

### 2. Verification and screenshots

[Verification](../../ui-prototype/docs/playable-l03-p1v4/VERIFICATION.md),
[actual command ledger](../../ui-prototype/docs/playable-l03-p1v4/command-results.json),
[Before/After viewer](../../ui-prototype/docs/playable-l03-p1v4/comparison.html).

| Command from repo root | Exit / result |
| --- | --- |
| `node ui-prototype/tests/playable-l03-p0.mjs` | **0**, 8 checks, original traces byte-identical |
| `node ui-prototype/tests/playable-l03-p0b.mjs` | **0**, 9 checks |
| `node ui-prototype/tests/playable-l03-p0c.mjs` | **0**, 9 checks |
| `node ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v4` | **0**, 26 checks |
| `node ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v4` | **0**, 9 checks |
| `node ui-prototype/tests/playable-l03-p1v3-browser.mjs --p1v4` | **0**, 9 checks |
| `node ui-prototype/tests/playable-l03-p1v4-browser.mjs` | **0**, 9 checks |
| `npm run build --prefix ui-prototype` | **0**, TypeScript + Vite |
| Existing Python `scripts/validate_ui_scope.py` | **0**, 13 protected files; approved sandbox retry |
| `node ui-prototype/tests/verify-p1v4-evidence.mjs` | **0**, 53 browser checks / 33 capture hashes / 47 source bindings current |
| `git diff --check`, staged check, protected-path and original-art baseline checks | **0** |
| Normal implementation commit / pre-push fetch / normal push | **0 / 0 / 0** |

**79 final automated checks** (26 pure + 53 browser). Earlier browser
assertions/selectors are unchanged; only evidence destinations and source
hash inclusion were extended. The P1v regression includes both legacy story
choices, absence/solo deployment, dialogue log, move/skill preview, Esc,
confirmation and result-to-campaign, plus victory/defeat/retry, interrupted
animations, keyboard, 200% text and the 390px fallback. P1v2 keeps its 100
pointer hits and overlap/depth/anchor checks. New art checks cover all 99
cell-centre hits, 18 impassable river cells, true-alpha props, unique portraits,
one ground image, hidden idle grid and measured character size.

All captures are real browser output under
`ui-prototype/docs/playable-l03-p1v4/`. For each `SIZE` =
`1280x720` / `1920x1080`:

- `after-SIZE-start.png`
- `after-SIZE-selected-path-preview.png`
- `after-SIZE-enemy-intent.png`
- `p1v3-regression/after-SIZE-{enemy,ally}-turn-banner.png`
- `p1v-regression/SIZE-{victory,defeat}.png`
- `p1v2-regression/after-SIZE-{column,winch,text-200}.png`

The separate `DIAGNOSTIC-grid-alignment` captures deliberately reveal the
full grid through test-only CSS; they are not normal gameplay screenshots.
Prior P1v3 images in the comparison are archived Before evidence, not
freshly recaptured or regenerated. The model inspected both sizes, path,
cluster, phase, success/failure and alignment. This is not human testing.

### 3–6. Known gaps, risks, open questions and not claimed

- Requested 1.3-tile scale is not attained: explicit retained-test exception
  above. 720p face recognition and readability require human assessment.
- Both knight bodies still share their old sprite; second portrait/body
  helmet consistency remains unfinished.
- Painted shoreline/foliage edges are approximate decoration, not a navigation
  mesh. Rule polygons alone determine movement; the two-column gap is retained.
- Optional 2–3 frame animation was skipped; single-frame bob/slide remains.
  No attack/hit/audio/engine/rules work was added.
- A remains **THIN**; no claim of deeper tactics or improved 3–5 minute pacing.
- **HUMAN_PENDING**: human playtest and Owner art approval. No commercial
  quality acceptance, gamepad/screen-reader trial, GPU benchmark, full
  accessibility certification or native lifecycle completion is claimed.
- Normal pre-commit issued its existing advisory `missing_canonical_memory`
  with `completion_claim_allowed=True`; it did not fail. Pre-push inventory
  and framework self-smoke ran normally. Self-smoke is not a native callback,
  and its doc-only advisories do not authorize additional work.
- Sandbox initially blocked Python access and Git index writes; approved
  same-scope escalations ran the existing validator and normal Git operations.
  No credentials, global settings, hooks, governance code or trust were changed.
- For Claude/GPT when Owner requests review: assess the painting/grid alignment,
  material/portrait consistency and the explicit size compromise from captures.
- For Gavin: accept/reject the art and scale exception; model review is input
  only. No review, merge or future slice has been initiated.
- This handoff is task DONE, not SessionEnd; no daily memory was hand-edited.

### Resource self-check — RESOURCE-CHECKLIST A–D

Read the cached game-ui-ux / game-feel skills at
`gamedev-skills/awesome-gamedev-agent-skills@0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`
(SHA-256 `8a094c84a377503aa8f4c40df676d1c6b6fc07d36ff95554ce06467f1614397e` /
`68fc818ad939151be2db9e358e4295a71830c19d61f3aff849f1599307f39f9d`).
Also applied imagegen, frontend-design and the executable trust-audit skill
to the existing browser binding. No skill/dependency install or code borrowing.

| Checklist item | Result and evidence |
| --- | --- |
| A: prototype-fast | **N/A new mechanic / PASS scope** — art only; keep if continuous painting preserves existing input/overlap/trace contracts |
| A: level-design | **N/A map design / PASS regression** — unchanged rules/MAP; P0 reachability and win traces |
| A: game-ai | **N/A AI changes / PASS regression** — unchanged resolver, existing intent reasons and exact replay parity |
| A: game-ui-ux — range/threat/intent | **PASS scoped** — visible legal range, same-command preview and enemy arrows; no attack threat exists in this ruleset |
| A: game-ui-ux — objectives/input | **PASS** — existing counters, phase, key hints; P1v/P1v3 reports and both-size captures |
| A: game-ui-ux — focus/responsive | **PASS tested scope** — keyboard, Retry, Esc, 200%, 720p/1080p and 390px; no gamepad claim |
| A: game-feel — pacing/feedback | **PASS scoped** — existing short landing/phase feedback returns to rest, unchanged result before/after playback; P1v3 9 checks |
| A: game-feel — impact | **N/A** — no attack/hit event in scope; no fabricated damage feedback |
| A: game-feel — reduced motion | **PASS** — pulse/glints/landing/banner effects disabled with identical rule results |
| B: Grid-Tactics separation | **PASS** — pure rules unchanged, view reads events; architecture reference only, no copied unlicensed code |
| B: HopeMetal licenses | **N/A new borrowing / PASS boundary** — original generated/reused art only, no external code or art |
| B: engine/dependencies | **PASS** — package and lockfile unchanged |
| C: solo 3–5 minute battle | **FAIL / HUMAN_PENDING** — no uncoached human trial; automated replay is insufficient |
| C: understandable enemy actions | **PASS engineering / HUMAN_PENDING comprehension** — visible reasons/arrows, unchanged resolver parity |
| C: win or lose | **PASS** — animated/skipped victory and defeat at both sizes |
| C: tactical alternatives | **PASS minimum / THIN retained** — hold vs idle still produce different outcomes; no depth claim |
| C: restart/change strategy | **PASS** — Retry/reset/focus and pure-rule replay checks |
| C: duplicates/stuck/invalid/interrupted | **PASS tested scope** — all retained P1v guards/skip/unmount checks |
| C: resolutions/keyboard | **PASS automated** — 53 browser checks, actual images and all 99 grid-centre hit checks |
| C: automated vs human | **PASS** — HUMAN_PENDING is separate from machine results and model inspection |
| D: SRD/CC-BY/IP/contract | **N/A rule adaptation / PASS boundary** — no rules change, WotC IP, commercial imagery or external source imported |
| D: authorization | **PASS** — Owner branch/base, no pull/main/PR/stash/P2/P0d/story/dependencies; normal hooks and own-branch push |

The human-playtest FAIL is explained and remains open. No unexplained C/D
FAIL is being hidden as art approval. This self-check supports scoped delivery,
not full playable/commercial acceptance.

---

## P1v playable screen

This is the current chunk. Earlier P0/P0b/P0c delivery and scope statements
below are historical; only the P1v screen is added here. A remains **THIN**,
enabled only in this screen. Rules defaults and all P0/P0b/P0c outputs remain
unchanged. P0d is deferred; P2 is not started.

| Field | P1v current chunk |
| --- | --- |
| Branch / own worktree | `codex/playable-l03-research` / `D:\campaign-forge` |
| Owner-named baseline | `13a6e17496dca1eaa8d3a98fe459dc819b37e8a4`; clean status; Owner confirmed exclusive worktree use |
| Implementation | `ece8e50dae7fadcec66e8f46b0d4ce2230130db0`, normal commit with hooks, pushed successfully |
| Delivery | `git push origin codex/playable-l03-research` exit **0**, remote advanced `13a6e17..ece8e50`. This handoff is a separate documentation commit; its SHA and push result are reported in the final response. No PR/main/force/stash/hook bypass. |
| Owner instruction | Only `docs/tasks/playable-l03-P1v-screen.md`, 90-minute maximum, A for this screen only, reuse art/components, no dependencies, real Playwright/screenshots, commit then try push. Explicit **do not pull** supersedes the shared-edit pull default. |
| Time, Asia/Taipei | First clock `2026-10-22T17:15:29+08:00` immediately after initial reads; final browser run `17:38:49–17:39:44`; implementation pushed before `17:46`; handoff prepared `17:48`. Final elapsed including delivery is reported in the final response. |

### 1. What changed

- New **Playable L03 (P1v)** menu entry and optional direct URL; the old L03
  preview is retained. New screen/CSS live under `ui-prototype/src/playable-l03/`.
- Existing 11×9 terrain, winch, wagon geometry and five painted characters;
  six-turn counter, interference, concise objective, exact legal moves,
  selection, Wait, End Turn, illegal-input message and keyboard controls.
- Both knights' planned paths and reasons come from pure `resolve`. Each
  accepted result is computed once; RAF plays its move events one tile at a
  time, then adopts the same result. Busy/input guards prevent duplicate
  turns; skip/reduced-motion consume that same pending result.
- Existing `AnimatedActor` accepts optional painted children, retaining its
  default articulated rendering. L03 cutouts use eased travel and walk bob;
  this does not create articulated limbs or new frame animation.
- Victory/defeat dialog, focus confinement, inert background and Retry;
  exit/unmount cancels playback and reopening starts fresh.
- Browser test and 13 real runtime PNGs, plus source/art hashes and exact
  result/frame evidence under `ui-prototype/docs/playable-l03-p1v/`.

Shared files edited: `ui-prototype/PLAN.md`, `memory/01_active_task.md`.
Own locks acquired; fetch/remote ancestry checked, **no pull** per Owner;
`SHARED-EDIT` printed and `Shared-file` trailers included in implementation
commit. Release only these own locks after handoff delivery. No daily memory,
story, Ink, rules defaults, governance program, dependencies or original art
changed. Governance acceptance receipt was refreshed with the existing recorder.

### 2. How to run and verify

From the worktree root:

```powershell
npm run dev --prefix ui-prototype -- --port 5183 --strictPort
```

Open `http://127.0.0.1:5183/`, click **Playable L03 (P1v)** beside the existing
preview; or open `http://127.0.0.1:5183/?scene=playable-l03` directly. Port
5173 was occupied and was left alone. Click an ally, then a highlighted ＋
tile; **等待** forgoes that ally's move and **結束回合** resolves enemies.
Space selects a focused cell; arrows move focus, Esc cancels selection,
Enter on the map ends the turn. Buttons keep their native Enter behavior.
Use unit bases/roster to switch while selected; figures let legal destination
clicks pass through. **跳過動畫** can interrupt playback; **重試** clears all state.

| Command / check | Observed result | Exit |
| --- | --- | --- |
| `npm run build --prefix ui-prototype` | TypeScript + Vite, 49 modules | **0** |
| `node ui-prototype/tests/playable-l03-p0.mjs` | 8 PASS; original traces unchanged | **0** |
| `node ui-prototype/tests/playable-l03-p0b.mjs` | 9 PASS; original witnesses unchanged | **0** |
| `node ui-prototype/tests/playable-l03-p0c.mjs` | 9 PASS; defaults/variants and fixtures unchanged | **0** |
| `node ui-prototype/tests/playable-l03-p1v-browser.mjs` | 26 browser checks, both sizes; animated and skipped full win/loss | **0** |
| `python scripts/validate_ui_scope.py` | 13 protected planning files | **0** |
| `python scripts/record_governance_checks.py` | 13 isolated lifecycle tests, scope/typecheck/build receipts | **0** |
| `python -I -B ui-prototype/tests/verify-governance.py` | Current source matches acceptance receipt | **0** |
| `git diff --check` | No whitespace errors | **0** |
| Protected-path `git diff --exit-code 13a6e17 -- ...` | Rules, all prior P0/P0b/P0c tests/outputs, three original views, art and package/lock unchanged | **0** |
| Evidence hash/dimension readback | 15 inputs and 13 PNGs match; both captured knight frames actually in flight | **0** |
| Implementation commit; pre-push fetch and ancestry; normal push | Hooks exit 0; no unknown remote commits; branch pushed | **0** |

Python commands used the existing absolute Python 3.12 binding with approved
execution after sandbox access failed; the successful actual checks above
are retained. See [verification](../../ui-prototype/docs/playable-l03-p1v/VERIFICATION.md),
[browser results](../../ui-prototype/docs/playable-l03-p1v/browser-results.json)
and [command results](../../ui-prototype/docs/playable-l03-p1v/command-results.json).
No browser/dependency install, new credential or trust change.

Original success JSONL plus A's sixth resolve reaches **turn 6 / success /
progress 2**. Original idle failure reaches **turn 5 / failure / progress 4**;
4/3 is the actual atomic rules result, intentionally not clamped. Every
committed command is compared with an independent pure-rules result.
Retry, illegal moves, Wait, repeated/held input, mid-play skip, dynamic
reduced motion, exit/reopen, focus, 200% body text and a narrow fallback
are covered. Existing two story routes, absent companions, dialogue log,
move/skill preview/cancel/confirmation and results-to-campaign also pass.

Screenshots: `ui-prototype/docs/playable-l03-p1v/` has
`1280x720-{start,intent,mid-animation,victory,defeat,move-range}.png`,
`1920x1080-{start,intent,mid-animation,victory,defeat,move-range}.png`, and
`1280x720-text-200.png`. These are runtime viewport captures after artwork
decode, not generated mockups. Linked individually in the verification file.

### 3–6. Limits, risks, questions and not claimed

- **HUMAN_PENDING:** no human playtest or measured 3–5 minute solo battle,
  enjoyment decision, Owner acceptance or commercial art approval. A still
  has known first-turn-position-then-wait wins; this screen does not fix THIN.
- Only open/hold is playable. No sealed escort, pressure experiment, HP,
  attacks, new rule/story/art, P0d or P2. Formal rule selection remains open.
- Tall existing cutouts overlap in adjacent diagonal cells. Bases and roster
  remain usable; labels can be partly occluded. Walking is single-frame
  travel/bob. No screen-reader/gamepad audit or performance certification.
- For Claude, when Owner requests review: inspect pure-result consumption
  during skip/unmount, local Wait versus unchanged `State.moved`, and range,
  figure click-through and label visibility. No review agents were started.
- For Gavin: play both outcomes and judge whether A deserves pressure/depth
  work in a separately authorized chunk. No automatic continuation proposed.
- Passing hooks/isolated replay are not native platform callbacks. No native
  adoption, SessionEnd/canonical closeout, model approval or merge is claimed.
  Pre-commit advisory `missing_canonical_memory` did not fail the hook; this
  task handoff is not SessionEnd. Canonical memory was not fabricated.

### Resource self-check — P1v

Checklist: `docs/review/RESOURCE-CHECKLIST.md`. All five relevant cached
original gamedev skills read at pinned upstream
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`; no installation. Existing source
manifests retain provenance. Local frontend-design, ui-design, typography
and executable-trust guidance were applied to layout/input/browser binding.

| Section / item | Result and evidence |
| --- | --- |
| A: prototype-fast | **PASS** — one isolated screen and explicit 90-minute stop; playability verified while depth remains THIN, no default adoption |
| A: level-design | **PASS scoped reachability / N/A sealed** — unchanged map and pure legal paths, open success/failure replay; no new depth claim |
| A: game-ai | **PASS** — pure deterministic resolve supplies both intent and actual events; previews update with positioning |
| A: game-ui-ux | **PASS automated** — exact range, both enemy intents/reasons, progress/objective, input hints, invalid message, focus and keyboard; human comprehension pending |
| A: game-feel | **PASS scoped movement/skip** — real mid-animation captures, step timing, busy guard and equal skipped outcome; hit reaction N/A because no attacks, pacing enjoyment HUMAN_PENDING |
| B: Grid-Tactics | **PASS architecture / N/A reuse** — prior read-only reference pinned `8d1952b46c771318b6f798b44038bac4490afe64`; no license, no code/art copied; pure rules remain separate and animation plays events |
| B: HopeMetal | **PASS license separation / N/A reuse** — prior reference pinned `c58849b67a89897ecdb6b3dbb7f25183d3be96ac`, code MIT versus images CC-BY-SA 3.0; no source/art borrowed |
| B: engine/dependencies | **PASS** — no engine or dependency added; package and lockfile unchanged |
| C1: full 3–5 minute solo battle | **FAIL / HUMAN_PENDING** for the human-duration criterion: complete six-turn automated battle works, but no human timing/playtest occurred; explained acceptance gap, not ready for full playable-bar approval |
| C2: understandable responsive enemy actions | **PASS automated** — both paths and one-line reasons visible, resolve reflects player state; human comprehension pending |
| C3: win or lose | **PASS** — both full outcomes at both sizes, animation/skip equality |
| C4: two choices produce different outcomes | **PASS** — original repositioning trace wins, idle loses; tactical depth still THIN |
| C5: restart and change strategy | **PASS** — Retry clears pure state and all local UI, both strategies replayed |
| C6: no duplicate/stuck/invalid/interrupted state | **PASS tested paths** — repeated/held input, illegal moves, mid-skip, reduced motion and exit/unmount; deterministic result readback |
| C7: both resolutions/basic keyboard | **PASS** — 1280×720, 1920×1080, Space/arrows/Esc/Enter; extra 200% text and 390px fallback |
| C8: separate automated/human evidence | **PASS** — browser report separate; HUMAN_PENDING explicit, no model-as-human substitution |
| D: SRD/rule adaptation/no WotC IP | **PASS unchanged provenance / N/A new adaptation** — no external text, art or new rules; only pre-existing authorized A screen opt-in, default untouched |
| D: project authorization | **PASS** — only P1v, own worktree/branch, no main/PR/deploy/Actions/stash, no P0d/P2/story changes; current handoff is the stop point |

The explained C1 gap means this is a playable-screen delivery for Owner
testing, not a claim that the full playable acceptance bar has passed.

## P0c variant comparison

**Recommendation: A, THIN, as an experiment only.** Extending to six turns
removes the known one-command wins in the P0b spaces while preserving the
original P0 success. It still has five T1-then-wait wins, so this is a narrow
mechanical improvement, not evidence of an engaging battle. B and both B+
windows still permit one ally to move twice, four tiles total, and wait to
win. No variant is OK. No option was adopted as default; P1 is not started.

| Field | P0c current chunk |
| --- | --- |
| Branch / own worktree | `codex/playable-l03-research` / `D:\campaign-forge` |
| Baseline | `d42024bf381f466c665fb661f493e291968aa2bb`; clean status, Owner confirms no competing agent |
| Implementation | `ab749d6523e48a469456bc3a1047b5d69313b437` (**local**, normal commit succeeded with hooks) |
| Delivery | Normal `git push origin codex/playable-l03-research` exit **1**, github.com:443 connection failure. No retry, escalation of push, force, hook bypass or credential change. This handoff is a separate local documentation commit; its SHA is reported in the final response (`git rev-parse HEAD`). |
| Owner instruction | Only P0c, 45 minutes, opt-in variants, original P0/P0b byte-identical, commit then try push; leave local on failure. Latest direct instruction explicitly says **do not pull**, superseding the task's pull step and shared-edit pull default. No P1/main/PR/stash. |
| Review input | `origin/review/gpt-playable-l03-research` @ `336016e`, `docs/review/gpt-playable-l03-p0b.md`, read with `git show`, exit 0; model input, not approval |
| Time | First recorded clock `2026-10-22T15:31:55+08:00`, immediately after a 6.1-second initial status/read batch. Evidence freeze `15:43`; final handoff preparation `15:46` (about 14 minutes since first clock). Final commit/check overhead and precise elapsed time reported in final response; 45-minute maximum. |

### Results and verdicts

W/L are counts of strategies in the named search space, never human win
rates. T1 includes all legal 0–3-command orders and deduplicates by labeled
end placement, retaining the minimum-cost representative, then only waits.
Max-one-move includes all legal command/turn combinations along the idle
timeline plus idle once; commands after a terminal state are excluded.
Cost order is **commands, distinct moved allies, path tiles**, matching P0b;
the display below is **units/moves/tiles**. Full party remains present in
these two searches, so unmoved allies can still block enemies.

| Variant | Turn-1-then-wait W/L | Max-one-move W/L | Min-cost win (units/moves/tiles) | Original P0 success trace still wins? | Lace (0,3) cheese still wins? | Solo wins? | Duo wins? | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 493/6303 | 6/211 | 1/1/1 | Yes, progress 1 | Yes, progress 2 | 3/3 lineups | 3/3 lineups | **CHEESE** |
| A (6 turns) | 5/6791 | 0/217 | 3/3/8 | Yes, progress 2 | No | None found (bounded) | None found (bounded) | **THIN** |
| B | 330/6466 | 0/217 | 1/2/4 | Yes, progress 1 | No | 3/3 lineups | 3/3 lineups | **CHEESE** |
| C | 234/5435 | 6/213 | 1/1/1 | No: Thoma's T1 move becomes illegal | No | 3/3 lineups | 3/3 lineups | **CHEESE** |
| B+ N=2 | 330/6466 | 0/217 | 1/2/4 | Yes, progress 1 | No | 3/3 lineups | 3/3 lineups | **CHEESE** |
| B+ N=3 | 330/6466 | 0/217 | 1/2/4 | Yes, progress 1 | No | 3/3 lineups | 3/3 lineups | **CHEESE** |

Minima combine the P0b spaces with the additional five-turn B/B+ two-command
searches. A's 3/3/8 is the cheapest **found in its P0b spaces**, not a global
optimum across multi-turn play. A was not given the additional B/B+ search;
its THIN verdict is correspondingly limited. Solo/duo uses the same P0b
existence search: absent allies removed, both enemies retained, <=1 command
per turn, deduplicated by position/progress/**hold history**, deterministic
10,000-state cap, stops at first win. A had no truncation but only covers
that command-per-turn bound; it is not a global claim that reduced parties
cannot win. B and B+ Karen+Lace lineups hit the cap and still find legal
witnesses. No solo/duo optimum or full multi-turn W/L is asserted.
Per-lineup T1 and one-command counts, widths and cap flags are in JSON.

- **Baseline — CHEESE:** the original Lace T2 (1,3)→(0,3) one-tile retreat
  still wins; no actual protection of the winch is required.
- **A — THIN:** one-command wins disappear; its cheapest T1 solution moves
  Karen→(2,2), Lace→(1,1), Thoma→(3,3), eight path tiles, then waits through
  turn six, progress 2. This asks for coordinated initial positioning but
  still no later action. Reduced-party robustness is unproved. Recommend
  retaining A for Owner comparison because it is the only tested option
  without a demonstrated one/two-command cheap win at its selected horizon;
  this is not a rule adoption or authorization to continue.
- **B — CHEESE:** final adjacency eliminates the old remote retreat, but a
  two-command one-ally win remains, including last-turn arrival.
- **C — CHEESE:** changing Thoma to (0,4) eliminates the exact old retreat
  while creating Lace T2 (1,3)→(1,4), one tile, progress 2. The original P0
  Thoma command to (2,2) is now four steps and rejected; not a valid loss
  replay and not silently rerouted.
- **B+ N=2 — CHEESE:** excludes last-turn-only arrival but still permits two
  moves by one ally; the additional hold turn is largely waiting.
- **B+ N=3 — CHEESE:** same minimum and T1 winning placements as N=2;
  longer holding cuts some timed sequences but does not remove cheap wins.

THIN here means solvable and no cheap witness in the tested spaces, with
depth unproved. CHEESE means <=1 command or a <=2-command hold/rush witness
in the selected horizon. OK requires additional tactical evidence. No win
found means **UNSOLVABLE within the reported bounds**, never a successful
fix or a proof of global impossibility. No extra candidate rules proposed.

### Cheapest bounded multi-move wins for B and B+

Exact bounds: **at most 2 commands per turn AND 2 total**, all legal units,
destinations and command orders, at 5 and 6 turns, no beam or state cap.
These are deliberately cheap-strategy searches, not all strategies allowed
up to ten/twelve commands. Every winning witness below is independently
replayed through the real `command`/`resolve` API in the P0c tests and new
JSONL evidence. Cost is **1 ally / 2 commands / 4 path tiles** in every
five-turn row. Other two allies stay present as stationary blockers.

| Variant / horizon | W/L within bounds | Cheapest found | Cheapest arrival at the latest allowed time |
| --- | --- | --- | --- |
| B / 5 | 229/24439 | Lace T1→(0,3), T3→(2,2), then wait; progress 2 | Lace T2→(0,3), **T5→(1,1)**; holds only T5, progress 2 |
| B+ N=2 / 5 | 208/24460 | Same T1/T3 strategy; holds T3–5, progress 2 | Lace T1→(0,3), **T4→(2,2)**; holds T4–5, progress 2 |
| B+ N=3 / 5 | 172/24496 | Same T1/T3 strategy; holds T3–5, progress 2 | Same; arrival **T3**, progress 2 |
| B / 6 | 0/24922 | No win found: **UNSOLVABLE in these two-command bounds** | None found |
| B+ N=2 / 6 | 0/24922 | No win found: **UNSOLVABLE in these two-command bounds** | None found |
| B+ N=3 / 6 | 0/24922 | No win found: **UNSOLVABLE in these two-command bounds** | None found |

Six-turn rows are extra horizon probes, not adoption of A+B or a claim
those complete variants cannot win with more commands. Within five turns
the exhaustive zero/one-command search has no wins, and all two-command
sequences were checked, establishing the minimum displayed command count
and its minimum units/tiles under the existing P0b cost order.

### 1. What changed

`ui-prototype/src/playable-l03/rules.ts` gains optional `config.p0c` only:
survivalTurns 5/6, requiredHoldTurns N, Thoma west-start flag. No experiment
in DEFAULT_CONFIG. A hold requires a living ally orthogonally adjacent to
(2,1) after enemy resolution and progress <3; a gap resets history. Required
history is serialized only when enabled; threshold failure precedes success.
New tests/search/report/witnesses are isolated under `playable-l03-p0c`.
README documents the contract. No attack/HP/push gameplay/UI/art/story.

Shared files edited: `ui-prototype/PLAN.md`, `memory/01_active_task.md`.
Own locks acquired, fetch/ancestry checked, no pull per latest Owner
instruction, `SHARED-EDIT` printed and `Shared-file` commit trailers added.
Locks released only for this task's own files at local handoff after failed
push; no other agent's lock/worktree touched. No daily memory record edited.

### 2. Tests and delivery evidence

Detailed commands/hashes/setup failures are in
`ui-prototype/docs/playable-l03-p0c/VERIFICATION.md`. All from repo root:

| Command/check | Exit code / observed result |
| --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c-search.mjs --write-results`, then without write flag | **0 / 0**, full searches twice, identical report/stdout |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs --write-traces` | **0**, 9 PASS, new witnesses only |
| Same P0c tests without write flag, twice | **0 / 0**, 9 PASS each, identical stdout and JSONL |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | **0**, 8 PASS; original fixtures exact |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | **0**, 9 PASS; original fixtures exact; stdout hash equals prior P0b handoff |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs` | **0**, original report exact; stdout hash equals prior P0b handoff |
| `npm run build --prefix ui-prototype` | **0**, TypeScript + Vite, 46 modules |
| Existing absolute Python + `scripts/validate_ui_scope.py` | **0** on approved run; 13 planning files checked |
| `git diff --exit-code d42024b --` original P0/P0b test/support/search and evidence paths | **0**, unchanged |
| `git diff --check`; `git diff --cached --check` before implementation commit | **0 / 0** |
| `git add` exact implementation paths | **0** |
| `git commit --file scratch/p0c/implementation-message.txt` | Sandbox **1** (`index.lock` denied), approved same command **0**, `ab749d6`; normal hooks, no bypass |
| Pre-push `git fetch origin`; `git log --oneline HEAD..origin/codex/playable-l03-research`; ancestor check | **0 / 0 / 0**, no unknown commits |
| `git push origin codex/playable-l03-research` | **1**, could not connect github.com:443; no retry; local commits retained |
| Handoff staging/commit | Sandbox `git add` **128** (`index.lock` denied); following commit **1** because nothing was staged, not a hook rejection. Approved stage/check/commit retried with normal hooks; final result reported with final SHA. |

Both search captures SHA256:
`de4ea34aacd662ea514444d1f2c53365dd921a8784f81575b55b7bfac627da8e`.
Both test captures:
`d0a638e28ae85c6d9876f6553265b1c37b99a0999bb9cbb243958bce94a218c4`.
These are PowerShell stdout captures, distinct from UTF-8 report hashes.

The successful pre-commit hook advised `missing_canonical_memory` with
`completion_claim_allowed=True`. This milestone is not SessionEnd; no
canonical closeout was fabricated. The network failed before pre-push
verification could be observed: installed hooks are **not** evidence of a
successful pre-push hook run. No governance code changed; governance-code
regression suite is N/A. No native lifecycle callback claim.

### 3–6. Limits, risks, open questions, not claimed

P1–P6, formal rules/story, art, playable UI, keyboard/resolution acceptance,
complete sealed-route victory, human fun, Owner approval and merge into
main are not completed or claimed. Search caps and omitted strategies limit
negative conclusions, especially A's reduced parties. A's five static wins
may still feel trivial; THIN is a provisional model interpretation, not
human gameplay acceptance. Results do not address QR-11 rewards/costs.
Implementation and handoff remain local after the failed normal push.

For independent review: assess the THIN threshold, dedup/cost boundaries,
last-N-end interpretation and whether these two-command counterexamples
are sufficient to reject B/B+ as tactical fixes. For Gavin: A is the
recommended comparison candidate with these limits; no further work or
default selection is presumed. No reviewer agents were started.

### Resource self-check — P0c

Source: `docs/review/RESOURCE-CHECKLIST.md`. Cached original prototype-fast,
level-design and game-ai SKILL.md reread at pinned upstream
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`; same files recorded in the
existing source manifest. No skill installation, external code execution,
additional agents or borrowed source/art. Earlier manifests remain provenance,
not proof of a current human playtest.

| Section / item | Result and evidence |
| --- | --- |
| A: prototype-fast | **PASS verification** — one question, explicit keep/verdict/timebox before search, isolated options, results retained without promoting default; human fun **N/A** |
| A: level-design | **PASS open solvability / FAIL depth for B/C/B+** — table and witnesses expose cheap wins; A **THIN**, sealed victory **N/A** map-only boundary, no complete-branch claim |
| A: game-ai | **PASS determinism / FAIL tactical resistance** — same real API, two identical search outputs, unchanged P0b tie/order tests; cheap waiting remains for B/B+ |
| A: game-ui-ux | **N/A**, P1/UI excluded |
| A: game-feel | **N/A**, animation/feedback excluded |
| B: Grid-Tactics | **PASS architecture separation**, pure state/event API and no view dependency; prior pinned reference only, no new external implementation copied |
| B: HopeMetal | **N/A reuse / PASS license separation**, no code/assets borrowed; existing code-MIT versus image-CC-BY-SA distinction retained |
| B: new engine/dependency | **PASS**, package and lockfiles unchanged; existing Node/TypeScript/Vite/Python only |
| C: complete 3–5 minute solo battle | **N/A**, headless verification only; no human duration claim |
| C: understandable enemy actions | **PASS mechanics**, unchanged intent events/tie/order tests and legal witness replays; human readability **N/A** |
| C: can win/lose | **PASS**, counts, boundary tests and trace replays; reduced parties have explicit bounds |
| C: two tactical choices change outcome | **PASS outcome differences / FAIL depth for B/C/B+**, retreat versus waiting and hold deadline tested; explained measured defect, not an unexplained release gate. A remains THIN, no OK claim |
| C: retry/change strategy | **PASS regression**, unchanged P0 tests plus P0c retry resets history and keeps experiment |
| C: duplicate/stuck/invalid paths | **PASS tested rules / N/A animation**, unchanged P0/P0b guards plus new hold/threshold tests; finite search, real movement API |
| C: 720p/1080p/keyboard | **N/A**, no UI changes or complete playable claim |
| C: automated vs human feedback | **PASS**, all new evidence explicitly machine-only; GPT review is model input |
| D: SRD/CC-BY/rule contract | **N/A adaptation / PASS scope**, original provisional occupancy options explicitly authorized, no copied SRD/WotC content or third-party art. Missing formal rule contract remains a historical limitation, not treated as satisfied |
| D: AGENTS/Owner scope | **PASS**, only P0c, own branch/worktree, locked shared milestones, no default adoption, pull, main changes, story/Ink, P1, stash, PR, force, deployment, Actions, trust changes or paid tool |

## Historical P0b report

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

## P1v2 readability

This section is the current readability delivery; earlier P0/P1v delivery
statements above remain historical. Adjacent units previously obscured names
and intercepted clicks meant for other tiles. The new view uses tile-only
input, smaller foot-anchored silhouettes, deterministic depth order and a
separate name strip. Automated checks establish reliable tile targeting and
unobscured names in the requested clusters; they do not establish human
recognition, fun or commercial art quality.

| Field | Value |
| --- | --- |
| Branch / named base | `codex/playable-l03-research` / `63a1f112cc7a331aee20bf37e82b935e57cbd2e8` |
| Implementation | `d98a4725d98282c26592884866932ce2d96e9680` |
| Delivery | **LOCAL ONLY**: normal push exit **1**, GitHub port 443 connection failure; no retry or bypass |
| Owner instruction | Only `docs/tasks/playable-l03-P1v2-readability.md`, 60-minute cap, no pull, unchanged rules, A only on this screen; commit then try push, retain locally on failure |
| Measured work window | 2026-10-22 18:09:04–18:27:20 Asia/Taipei through implementation push and handoff preparation: **18m16s**; final response includes remaining handoff commit time |
| Human acceptance | **HUMAN_PENDING** |

### 1. What changed

- `ui-prototype/src/playable-l03/PlayableL03.tsx`: sort by actual animated
  projected foot Y, then X/id; use 26-unit-high existing silhouettes and crop
  transparent foot padding. Each tile owns the entire hit area; artwork and
  landmarks cannot intercept it. Ally circles and enemy diamonds differ in
  colour as well as shape. The name strip shows full name, side, coordinate
  and action status on hover, focus or click.
- Inspection is distinct from action selection: enemies and already-used
  allies can be inspected but cannot move or Wait. Esc clears inspection;
  Retry and commands clear transient name/selection state.
- `playable.css`: names use 1rem text outside the SVG. Reserved placeholder
  footprint prevents label wrapping from moving the tile under the pointer
  at 200% text. Board height leaves the 720p controls visible.
- Added `playable-l03-p1v2-browser.mjs`. Retained P1v assertions, updating four
  sprite-click selectors to their owning tile and isolating new regression
  output under `playable-l03-p1v2/p1v-regression/`.
- Shared-file: `ui-prototype/PLAN.md`; Shared-file: `memory/01_active_task.md`.
  Codex acquired its own locks, fetched and checked the branch, printed both
  SHARED-EDIT lines and used both commit trailers. Owner's explicit no-pull
  instruction superseded the default shared-file pull step. Own locks are
  released after the failed push/local handoff; no other lock is touched.
- `rules.ts`, source PNGs, `AnimatedActor.tsx`, `L03Preview.tsx`, `ArtGate.tsx`,
  dependency files, original P0/P0b/P0c evidence and story files are unchanged.

### 2. Verification and screenshot paths

Full actual output, hashes, exact capture states and failed-attempt details:
[verification](../../ui-prototype/docs/playable-l03-p1v2/VERIFICATION.md),
[command results](../../ui-prototype/docs/playable-l03-p1v2/command-results.json),
[readability report](../../ui-prototype/docs/playable-l03-p1v2/after-results.json),
[P1v regression](../../ui-prototype/docs/playable-l03-p1v2/p1v-regression/browser-results.json).

| Command from repo root | Exit | Result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | **0** | 8 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | **0** | 9 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | **0** | 9 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v2` | **0** | 26 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs` | **0** | 9 checks |
| `npm run build --prefix ui-prototype` | **0** | TypeScript/Vite, 49 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | **0** | 13 protected planning files |
| `git diff --check`, `git diff --cached --check` | **0**, **0** | Whitespace checks |
| Protected-scope `git diff --quiet 63a1f11 -- …` | **0** | Rules, original screens/assets/fixtures/dependencies/story unchanged |
| Implementation `git add`, `git commit` | **0**, **0** | Normal hooks; advisory `missing_canonical_memory`, `completion_claim_allowed=True` |
| Pre-push `git fetch origin`, unknown-commit check | **0**, **0** | No unknown remote commits on this branch |
| `git push origin codex/playable-l03-research` | **1** | Cannot connect to `github.com` port 443; commits retained locally |

The 9 new cases include four overlap scenarios (two sizes × two arrangements),
100 actual pointer checks (all five units × five tile points × four scenarios),
name visibility/topmost/bounding-box checks, silhouette separation, foot
anchors, draw order, keyboard/Esc, hover exit, 200% text stability and animated
sorting. The P0 winch cluster is replayed from its real success commands;
the column pair is the initial Lace (1,3)/Thoma (1,4) deployment. No injected
state or force-click is used. The 26 original browser cases include animated
and skipped wins/losses, Retry, input guards and both legacy story workflows.

All screenshots are under `ui-prototype/docs/playable-l03-p1v2/`:

| Scene | 1280×720 Before / After | 1920×1080 Before / After |
| --- | --- | --- |
| Winch cluster | `before-1280x720-winch.png` / `after-1280x720-winch.png` | `before-1920x1080-winch.png` / `after-1920x1080-winch.png` |
| Column | `before-1280x720-column.png` / `after-1280x720-column.png` | `before-1920x1080-column.png` / `after-1920x1080-column.png` |
| 200% name | `after-1280x720-text-200.png` | `after-1920x1080-text-200.png` |

Before capture command (`--before`) exited **0** on the unchanged baseline
source. Initial new-test exit **1** was an unclipped SVG atlas-bounds false
positive; viewport measurement fixed it. Expanded 200% test exit **1** exposed
a real name-wrap layout shift; the reserved footprint fixed it. Both failed
reports are retained locally in scratch and documented in verification.
Initial sandbox fetch and Python probe exited **1**; approved same-command
retries exited **0**. The actual push failure above was not retried.

### 3–6. Limits, risks, review questions and claims

- **HUMAN_PENDING**: no uncoached 3–5 minute trial, recognition study or Owner
  art approval. 26-unit figures preserve spacing but lose fine detail at
  720p; the single name strip requires pointing/focusing/clicking to identify
  a unit. Existing sprite-only stepping remains, with no skeletal animation.
- A remains **THIN**, enabled only on this screen; no P0d integration, P2 AI,
  new rules, new assets, engine, dependency, story, S4, main, PR, stash,
  deployment, Actions or additional agents. No gamepad/screen-reader claim.
- For Claude/GPT review when Owner requests: check tile hit ownership,
  inspection/action separation, alpha-foot anchors and 200% footprint, and
  judge whether the 720p figure size is an acceptable tradeoff.
- For Gavin: human recognition and playability remain pending. Model checks
  do not approve them. This handoff makes no new work request or authorization.
- No remote-publication claim: the implementation and this handoff stay local.
  Task DONE is not SessionEnd; no canonical daily record or native hook
  callback was manufactured. No governance code was changed.

### Resource self-check (RESOURCE-CHECKLIST A–D)

Relevant cached `game-ui-ux` and `game-feel` SKILL.md were read this turn from
the existing pinned `gamedev-skills/awesome-gamedev-agent-skills` snapshot
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`. SHA-256 respectively:
`8a094c84a377503aa8f4c40df676d1c6b6fc07d36ff95554ce06467f1614397e` and
`68fc818ad939151be2db9e358e4295a71830c19d61f3aff849f1599307f39f9d`.
Local ui-design, typography-audit and external-executable-trust-audit were
also read and applied; nothing installed or copied from reference projects.

| Checklist item | Self-check and evidence |
| --- | --- |
| A: prototype-fast | **N/A new mechanic** — narrow readability change; 60-minute cap, keep criterion is correct tile targeting and clear labels |
| A: level-design | **N/A new layout / PASS regression** — unchanged map/rules; P0 8 checks, original success trace replay; full sealed route remains outside this segment |
| A: game-ai | **N/A new AI / PASS regression** — unchanged resolver and intents; P0b/P0c and P1v replay pass |
| A: game-ui-ux | **PASS automated scoped fix** — full names scale, tile targeting, focus/Esc, both resolutions and 200%; human understanding pending |
| A: game-feel | **PASS existing movement regression / N/A new hit feedback** — animation order and same rule result verified; full animation quality remains unaccepted |
| B: Grid-Tactics separation | **PASS** — rendering/inspection only, pure rules unchanged; prior architectural reference retained, no unlicensed code copied |
| B: HopeMetal licenses | **N/A new borrowing / PASS scope** — no external code/art introduced; existing repo-original PNGs unchanged |
| B: no new engine/dependency | **PASS** — package/lockfiles unchanged |
| C: full 3–5 minute solo battle | **FAIL (HUMAN_PENDING)** — automated six-turn completion is not a human trial; explicit retained gap, not Owner acceptance |
| C: understandable enemy action | **PASS engineering / HUMAN_PENDING understanding** — existing intent/reason and paths remain, P1v full replay passes |
| C: win or lose | **PASS** — animated and skipped success/failure in both sizes, P1v tests 4–6 and 11–13 |
| C: tactical choices differ | **PASS minimum / THIN retained** — hold wins, idle loses; no claim of deeper tactical improvement |
| C: restart/change strategy | **PASS** — P0 retry and P1v Retry state checks |
| C: duplicate/stuck/invalid/interruption | **PASS tested scope** — P1v tests 15–18 plus original pure guards; no new simulation |
| C: 720p/1080p/keyboard | **PASS automated** — 9 new cases + 26 regressions; Space/arrows/Esc/Enter, real captures |
| C: automated vs human | **PASS** — HUMAN_PENDING throughout; no model review substituted for human playtest |
| D: SRD/CC-BY/WotC/contract | **N/A new adaptation / PASS no new IP** — rules and original assets unchanged, no imported SRD or commercial material |
| D: authorization | **PASS** — P1v2 only, own named branch/worktree, no pull, no main/PR/P2/story/stash/Actions/deploy, normal commit and failed push |

The explained human-playtest FAIL remains open and prevents claiming full
playable/Owner acceptance; the scoped readability engineering checks pass.

## P1v3 visual pass

The original screen's pale flat grid, tiny figures and text lists made it read
like a prototype dashboard. This pass uses the existing painted materials at
full strength, deeper terrain edges, larger figures, close portrait cards and
one moss/slate/brass frame. Movement and phase feedback remain presentation
of the existing pure command result. The result is visually more cohesive;
the tests establish correct interaction and state, not Owner art approval.

| Field | Value |
| --- | --- |
| Branch / Owner-named base | `codex/playable-l03-research` / `7319ef03923a6838375e95a6a16f1de4c42c9d11` |
| Implementation head | `5f7cc4102d92a10d63f574dfedfa790262d79383` |
| Implementation push | **YES**, normal `git push origin codex/playable-l03-research`, exit **0**; remote advanced `7319ef0..5f7cc41` |
| Owner instruction | ONLY P1v3 visual pass, 90-minute cap, no pull, rules unchanged, existing art only, no dependencies; P2 in scratch/p2 is off limits; commit then try push |
| Recorded window through implementation push | 2026-10-22 19:05:58–19:31:13 Asia/Taipei, **25m15s**; final reply includes handoff delivery time |
| Human acceptance | **HUMAN_PENDING** |

### 1. What changed

- `PlayableL03.tsx`, `presentation.tsx`, `playable.css`: painted grass/stone/
  water/forest, 18-unit bank faces, lower water surface, subtle CSS water
  glint, outer trees, wagon cargo, bridge remnants and a framed winch marker.
- This screen's projection changes to ±44/+26 per cell step; figures grow
  from 26 to 50 scene units. Original PNG crop/foot anchors and actual animated
  Y/X/id depth order remain. Ally rings/enemy diamonds are small, with soft
  shadows. Only the tiles receive pointer input.
- Dark metal/brass header, side panel, controls and result overlay; portraits
  for three allies/two knights, ready/used icons, turn/interference gauges,
  persistent phase, and opt-in development coordinates. Existing state labels
  remain available to assistive technology.
- Mouse/keyboard move-path preview reads the same pure command's returned
  path; 180ms arrival feedback, 900ms phase banners, selection pulse and hover.
  Reduced Motion disables these effects without changing the rule result.
- **Shared-file: `ui-prototype/PLAN.md`**;
  **Shared-file: `memory/01_active_task.md`**. Codex acquired both locks,
  fetched, checked for unknown remote branch commits, printed SHARED-EDIT
  lines and used both commit trailers. Owner's no-pull instruction took
  precedence. Only Codex's own locks are released after the successful push.
- `rules.ts`, original PNGs, `L03Preview.tsx`, `ArtGate.tsx`, `l03Scene.ts`,
  `AnimatedActor.tsx`, dependencies, original fixtures and story are unchanged.

### Assets and style guide

Five existing original assets, all unchanged: `terrain-v2.png` (four material
quadrants), `props-v2.png` (trees and cargo), `ferry-scene-v2.png` (dim blurred
backdrop), `l03-party-v1.png` (figures/portraits), `l03-enemies-v1.png` (knights).
No new image generation, copied commercial art or font download. Dimensions
and SHA-256 are in [asset manifest](../../ui-prototype/docs/playable-l03-p1v3/asset-manifest.json).
Sources remain the existing L03 art direction/prompts and visual-sprint
manifest. Inspected `landmarks-v3.png` but did not use its unrelated survey
stones/lantern/brazier as a fictitious winch. Winch, bridge remnants and wagon
chassis use original SVG geometry; these remain less painterly than the atlas.

[STYLE.md](../../ui-prototype/docs/playable-l03-p1v3/STYLE.md) records palette,
fonts, framing, scale, camera and motion. No conflict with the supplied root
ART-DIRECTION was found. There is a brief-internal tradeoff: literal 1.2–1.5
full diamond-height figures would violate P1v2's same-column zero-overlap
assertion. Kept the tests and a 50-unit figure / 52-unit foot separation;
**the literal requested height ratio is not achieved**. This is visible and
documented, not hidden by changing the assertion or relabelling the scale.

### 2. Verification

Full outputs, source/capture hashes and failed attempts:
[verification](../../ui-prototype/docs/playable-l03-p1v3/VERIFICATION.md),
[command results](../../ui-prototype/docs/playable-l03-p1v3/command-results.json).

| Command from root | Exit | Result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | **0** | 8 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | **0** | 9 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | **0** | 9 checks |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v3` | **0** | 26 checks, including both legacy story/absence flows |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v3` | **0** | 9 checks, all original overlap/click assertions retained |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v3-browser.mjs` | **0** | 9 new path/phase/arrival/gauge/dev/reduced-motion checks |
| `npm run build --prefix ui-prototype` | **0** | TypeScript + Vite, 50 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | **0** | 13 protected planning files |
| Source/capture digest and comparison-path audit | **0** | All final report hashes current; 28 comparison PNG paths present |
| `git diff --check`, `git diff --cached --check` | **0**, **0** | Clean |
| Protected-path `git diff --quiet 7319ef0 -- …` | **0** | Rules, assets, old screens, dependencies, traces and story unchanged |
| Normal implementation commit | **0** | Existing pre-commit advisory `missing_canonical_memory`, `completion_claim_allowed=True`; not bypassed |
| Pre-push fetch / unknown-commit check | **0** | No unknown commits on this remote branch |
| Normal implementation push | **0** | Existing inventory and governance hooks ran; no bypass; branch updated |

70 final checks = 26 pure + 44 browser. The baseline capture run also passed
26 checks before implementation. Original P1v behavior assertions remain;
only the winch text selector was adjusted for coordinates hidden by default.
P1v2 still tests 100 real pointer hits, all five units, initial column and
winch cluster, names/foot anchors/viewport separation, depth order, keyboard,
Esc, hover exit and 200% text.

Failed attempts are retained under `playable-l03-p1v3/attempts/`: 720p sidebar
overflow (exit 1), 1080p control overflow of 10px (exit 1), and a short arrival
effect missed by selector backoff polling (exit 1). Layout was fixed; the
effect test now starts RAF observation before input, without lengthening the
effect. Initial sandbox fetch/Python access failed; approved same-scope
invocations succeeded. Final checks above all passed. No code in the
governance framework was changed; its push smoke is not a native callback.

### Screenshots

All 42 real execution PNGs are under `ui-prototype/docs/playable-l03-p1v3/`.
Use [comparison.html](../../ui-prototype/docs/playable-l03-p1v3/comparison.html)
to switch resolution and state. For each size `1280x720` / `1920x1080`:

- `before/<size>-{start,move-range,intent,mid-animation,turn-banner,victory,defeat}.png`
- `p1v-regression/<size>-{start,move-range,intent,mid-animation,turn-banner,victory,defeat}.png`
- `after-<size>-{path-preview,enemy-turn-banner,ally-turn-banner}.png`
- `p1v2-regression/after-<size>-{column,winch,text-200}.png`

Before transition captures contain no banner because the old UI had none.
Dynamic captures are real samples at equivalent replay stages, not perfectly
identical animation frames. Both sizes were visually inspected by the model;
that is not human playtest or Owner art acceptance.

### 3–6. Limits, risks, open questions and not claimed

- Literal unit-height ratio remains below the brief as explained above;
  720p details and face recognition still need human review. The portraits
  carry finer facial detail than the battlefield figures.
- Single-frame sprite sliding/bobbing, repeated terrain and geometric machine/
  bridge parts remain visible. No true 3D, skeletal animation, attacks, sound,
  new hit feedback, camera zoom/pan or performance benchmark was introduced.
- A remains THIN; P2, new rules, story/Ink, S4, other worktrees, main, PR,
  deployment, Actions and dependencies are outside this pass. No agent was
  spawned. No `stash`, force push or `--no-verify` was used.
- For Claude/GPT when Owner requests review: judge consistency and 720p
  character readability from actual captures, and verify that the explicitly
  documented scale tradeoff is acceptable. Review remains input to Gavin.
- For Gavin: human playtest and art approval remain **HUMAN_PENDING**.
  This handoff does not authorize further work or claim commercial quality,
  full accessibility certification, gamepad/screen-reader testing, native
  lifecycle completion or session end. No daily memory was hand-edited.

### Resource self-check — RESOURCE-CHECKLIST A–D

Read the cached `game-ui-ux` and `game-feel` SKILL.md from pinned
`gamedev-skills/awesome-gamedev-agent-skills@0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`,
with the existing SHA-256 values `8a094c84a377503aa8f4c40df676d1c6b6fc07d36ff95554ce06467f1614397e`
and `68fc818ad939151be2db9e358e4295a71830c19d61f3aff849f1599307f39f9d`.
Also read/applied local frontend-design 2.0. No installation or code borrowing.

| Item | Result and evidence |
| --- | --- |
| A: prototype-fast | **N/A new mechanic / PASS scope** — presentation-only; keep criterion: cohesive painted screen with preserved original behavior/overlap checks |
| A: level-design | **N/A new map / PASS regression** — unchanged MAP/rules; P0 8 checks and original win trace replay |
| A: game-ai | **N/A new AI / PASS regression** — same resolver/intent; P0b/P0c/P1v pass |
| A: game-ui-ux — range/threat/intent | **PASS scoped** — visible move range, same-command path, knight portraits and real predicted arrows; no attack threat exists in this P1v ruleset |
| A: game-ui-ux — objectives/input | **PASS** — counters/gauges, persistent phase, key hints; final P1v/P1v3 reports and both-size screenshots |
| A: game-ui-ux — responsive/focus | **PASS tested scope** — 720p/1080p, 200%, 390px, Space/arrows/Esc/Enter/Retry; no gamepad claim |
| A: game-feel — pacing/feedback | **PASS scoped** — exact command result before/after animation, 180ms landing/900ms banners return to rest, selection/path feedback; P1v3 9 checks |
| A: game-feel — impact | **N/A** — no hit event or attack in unchanged rules; no fabricated damage or combat animation |
| A: game-feel — reduced motion | **PASS** — water/pulse/bounce/banner animation names become none; same final state, both sizes |
| B: Grid-Tactics separation | **PASS** — pure rules unchanged, presentation reads command events; architecture reference only, no copied code |
| B: HopeMetal licensing | **N/A new borrowing / PASS boundary** — no external code/art; five existing repo-original assets with provenance and hashes |
| B: engine/dependencies | **PASS** — package and lockfile unchanged; no engine or new dependency |
| C: solo 3–5 minute battle | **FAIL / HUMAN_PENDING** — no uncoached human trial; machine replay is not that evidence |
| C: understandable enemy actions | **PASS engineering / HUMAN_PENDING comprehension** — existing reason plus preview arrows/portrait cards; exact resolver parity |
| C: win or lose | **PASS** — actual animated/skipped success and failure, both sizes |
| C: tactical alternatives | **PASS minimum / THIN retained** — original hold vs idle outcomes; no claim of improved tactical depth |
| C: restart/change strategy | **PASS** — pure Retry and browser state/reset/focus checks |
| C: duplicate/stuck/invalid/interrupted | **PASS tested scope** — original input guards, skip, reduced-motion change and unmount assertions retained |
| C: sizes/keyboard | **PASS automated** — 44 final browser checks, actual screenshots, keyboard path preview and movement |
| C: automated vs human | **PASS** — HUMAN_PENDING consistently recorded; no model review substituted |
| D: SRD/CC-BY/IP/contract | **N/A rule adaptation / PASS boundary** — no rules change, WotC IP or new third-party source; original proposal assets reused |
| D: authorization | **PASS** — Owner-named branch/base, no pull/main/PR/stash/P2/story/Actions/deploy/new art/dependencies; normal hooks and own-branch push |

The human-playtest FAIL is explained and remains open. These results support
the scoped visual implementation, not full playable or commercial approval.

## P1v5 feedback

The battlefield previously showed counters and movement without explaining
interference or blocked movement at the point of action. This pass ties short
visual feedback to the existing progress and blocked-intent events, and shows
the current predicted destination before End Turn. Rules, logical positions
and the existing animation lock remain unchanged.

| Field | Value |
| --- | --- |
| Branch / Owner-named base | `codex/playable-l03-research` / `3c95f0e91b5c8ed5e1b65d48f92935da986bc62c` |
| Step 1 / 2 / 3 / 4 | `f3aba38` / `0483147` / `c3a65ea` / `435c886` |
| Verification milestone | `4825b7d` |
| Owner instruction | ONLY P1v5, 60-minute cap, commit after each numbered step, no pull, no rules.ts/dependency/scratch-worktree changes; normal task-branch push attempt |
| Started (Asia/Taipei) | 2026-10-23 00:57:41 |
| Human acceptance | **HUMAN_PENDING** |

### 1. Done and skipped

- **Step 1 done:** winch jerk and wheel turn, rope pulled taut with shake,
  newly filled gauge pips flash, short actual-value pop including `絞盤干擾 1/3`,
  stronger red 2/3 warning, and defeat fade. The existing threshold remains
  `>=3`; the idle trace can go 2→4, and the view does not rewrite it to 3.
- **Step 2 done for the available blocked event:** short enemy recoil,
  dust, visual-layer shake (3 scene px maximum), status pop and an adjacent
  ally's clash spark labelled 阻擋. Tile hit polygons do not shake.
- **Step 3 done:** animated intent arrows and pulsing exact predicted target
  tiles. Already-adjacent contributors point to the winch.
- **Step 4 done:** hover/focus glow, move-commit pulse and subtle arrival dust.
  During impact feedback the phase banner sits above the action.
- All transient feedback respects Reduced Motion and Skip Animation;
  toggling either mid-feedback clears it permanently. Static warnings and
  intent outlines remain. No effect extends busy or resolves a command.
- **Skipped / N/A:** physical shove, damage numbers and hit reaction to damage,
  because the unchanged rules contain no shove, HP or hit event. No fabricated
  damage or new mechanic. No priority was dropped for the timebox.
- No new art, dependencies or engine. Original bitmap files remain unchanged.
- Shared-file: `ui-prototype/PLAN.md`; Shared-file: `memory/01_active_task.md`.
  Both were edited under Codex-owned locks, after fetch and the no-unknown-
  commits check. Owner's no-pull instruction overrides the shared-file default.
  `memory/03_knowledge_base.md` records the observed duplicate-key cleanup bug.

### 2. Verification and screenshots

[Verification](../../ui-prototype/docs/playable-l03-p1v5/VERIFICATION.md),
[actual command results](../../ui-prototype/docs/playable-l03-p1v5/command-results.json),
[source/capture audit](../../ui-prototype/docs/playable-l03-p1v5/evidence-audit.json).

| Command from repo root | Exit | Result |
| --- | --- | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs --p1v4 --p1v5` | 0 | 26 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v2-browser.mjs --p1v4 --p1v5` | 0 | 9 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v3-browser.mjs --p1v5` | 0 | 9 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v4-browser.mjs --p1v5` | 0 | 9 |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p1v5-browser.mjs` | 0 | 14 |
| `npm run build --prefix ui-prototype` | 0 | TypeScript + Vite |
| `scripts/validate_ui_scope.py` via installed Python | 0 | 13 protected planning files |
| `node ui-prototype/tests/verify-p1v5-evidence.mjs` | 0 | 67 browser checks, 41 capture hashes, 52 source bindings |
| `scripts/record_governance_checks.py` via installed Python | 0 | 13 isolated lifecycle tests; scope, typecheck, Vite all 0 |
| Protected-path diff; whitespace / staged whitespace checks | 0 | Rules, original art, dependencies and story unchanged |

93 game checks = 26 pure + 53 existing browser + 14 feedback-specific browser.
The 13 governance replay tests are separate. Old browser harnesses only gain
a new evidence output destination; no behavioural assertion was removed.
Tests cover both resolutions, 200% text, narrow fallback, keyboard, Retry,
both legacy story/absence flows, invalid/duplicate input and animation exit.
The recorder refresh is local isolated replay, not a native platform callback.

Step 4 initially failed twice (exit 1): dust and the arrival wrapper shared
a sibling React key, leaving stale SVG after timeout. Unique keys fix it;
failed report and screenshots are retained under `attempts/`. Read-only
shell/Python probes and sandbox Git writes also initially failed; approved
same-scope invocations succeeded. These are recorded separately from passing
product checks.

Actual 1280×720 browser captures, all under
`ui-prototype/docs/playable-l03-p1v5/`:

- `1280x720-winch-interference.png`
- `1280x720-winch-1-of-3.png`
- `1280x720-warning-2-of-3.png`
- `1280x720-body-block.png`
- `1280x720-intent-pulse.png`
- `1280x720-hover-glow.png`
- `1280x720-move-confirm.png`
- `1280x720-defeat.png`

Both-resolution regressions are in `p1v-regression/`, `p1v2-regression/`,
`p1v3-regression/`, `p1v4-regression/`. They are actual execution screenshots,
not generated mockups. Production timers were not slowed to capture effects.

### 3–6. Limits, risks, open questions and not claimed

Effects are short CSS/SVG presentation over the existing single-frame
figures. The wheel and rope overlays remain geometric. This is not skeletal
animation or a new combat system. Exact impacts are keyed to blocked intent
at settlement; they do not invent attack turns.

For Owner-requested Claude/GPT review: inspect whether the 720p winch overlay,
clash spark and warning remain readable without hiding the painted scene,
and check event/state isolation and dynamic motion cancellation.
For Gavin: effect strength, comfort and readability await actual human play.
No uncoached 3–5 minute human trial, commercial art acceptance, full
accessibility/gamepad certification, story/S4 decision, main merge, PR,
deployment, Actions, or natural native lifecycle completion is claimed.
No agents were spawned; no other worktree was touched. Task DONE is not
SessionEnd; no daily canonical record was hand-written.

### Resource self-check — RESOURCE-CHECKLIST A–D

Read the cached **game-feel** and **game-ui-ux** skills from the existing pinned
`gamedev-skills/awesome-gamedev-agent-skills@0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`.
SHA-256: game-feel
`68fc818ad939151be2db9e358e4295a71830c19d61f3aff849f1599307f39f9d`;
game-ui-ux
`8a094c84a377503aa8f4c40df676d1c6b6fc07d36ff95554ce06467f1614397e`.
Applied discrete event hooks, transient layered feedback, unchanged simulation,
event-driven HUD and keyboard/focus preservation. No skill was installed.

| Item | Self-check and evidence |
| --- | --- |
| A: prototype-fast | N/A new mechanic; PASS narrow four-step presentation scope and checkpoint commits |
| A: level-design | N/A new map; PASS regression, P0 trace and map unchanged |
| A: game-ai | N/A new AI; PASS pure resolver and predicted-intent parity |
| A: game-ui-ux | **PASS scoped engineering** — legal ranges, exact intent targets, visible gauge/warning, keyboard/focus and both-size original browser assertions |
| A: game-feel | **PASS scoped engineering** — 14 feedback checks, real blocked/progress events, recoil/dust/spark, decay, no extra lock, reduced/skip and mid-effect cancellation; captures above |
| B: Grid-Tactics separation | PASS — pure rules unchanged; renderer consumes existing events; architecture reference only, no copied source |
| B: HopeMetal licenses | N/A new borrowing; no third-party code/art added |
| B: engine/dependencies | PASS — package and lockfile unchanged |
| C: solo 3–5 minute battle | **FAIL / HUMAN_PENDING** — no uncoached human trial; automated replay is not human evidence |
| C: understandable enemy action | PASS engineering / HUMAN_PENDING comprehension — exact targets, arrows, reasons and real event feedback |
| C: win or lose | PASS — animated and skipped victory/defeat, both sizes |
| C: tactical choices differ | PASS minimum / THIN retained — existing hold vs idle outcomes; no deeper tactical claim |
| C: restart/change strategy | PASS — original Retry and state/focus assertions |
| C: duplicates/stuck/invalid/interruption | PASS tested scope — unchanged original guards plus mid-feedback skip/reduce cancellation |
| C: 720p/1080p/keyboard | PASS automated — original size, click, overlap, 200% and keyboard assertions retained |
| C: automated vs human | PASS — human acceptance consistently HUMAN_PENDING |
| D: SRD/CC-BY/WotC/contract | N/A new rule adaptation; PASS original rules/art unchanged, no new third-party IP |
| D: authorization | PASS — own named branch/worktree, four presentation priorities only, no pull/rules/dependencies/main/PR/stash/S4/Actions/deploy |

The explained human-playtest FAIL remains open. These results support the
scoped feedback implementation, not full playable or art approval.


### Git delivery and time

The four numbered steps were committed immediately after their scoped checks.
Implementation/evidence push succeeded with exit **0**, advancing the existing
remote task branch from `3c95f0e` to `4825b7d`. Normal pre-commit/pre-push hooks
ran; no bypass. Shared-file locks are released only after that successful push.
The final handoff commit/push and exact total elapsed time are reported in the
final response; this handoff does not pretend to know its own future SHA.
Recorded implementation-delivery window: 2026-10-23 00:57:41–01:19:16
Asia/Taipei, **21m35s**. This is actual elapsed time, not the 60-minute budget.
