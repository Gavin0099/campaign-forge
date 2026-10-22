# P0d execution evidence

Base: `13a6e17496dca1eaa8d3a98fe459dc819b37e8a4`.
Worktree: `D:\campaign-forge\scratch\p0d`, branch `codex/playable-l03-p0d`.
First tool batch started about **2026-10-22 17:28:09 +08:00**; first recorded
UTC clock was `09:28:13`, after that 3.6-second batch. Hard limit: 60 minutes.
Final commit/push SHAs and elapsed wall time are in the handoff/final response.

## Actual commands and exits

Commands run from this worktree root. No installation or writes through the
read-only `ui-prototype/node_modules` junction. No P1/P2, UI or browser run.

| Command | Observed result |
| --- | --- |
| `git status --short --branch`; `git rev-parse HEAD` | 0; clean authorized branch and exact base |
| `git fetch origin` | Initial sandbox attempt 1 (shared `.git/worktrees/p0d/FETCH_HEAD` access); approved retry 0 |
| `git show origin/review/gpt-playable-l03-research:docs/review/gpt-playable-l03-p0c.md` | 0; read the task's review input, not an approval |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0d-search.mjs --write-results > scratch/p0d/search-1.txt 2> scratch/p0d/search-1-progress.txt` | Wrapper **1**, despite complete JSON generation; Node exit was not separately captured. Stderr progress became PowerShell NativeCommandError records. This run is **not counted as a successful acceptance run**. |
| Same P0d search without write flag, with explicit `$LASTEXITCODE` capture and `exit` | Two fresh acceptance runs: **0 / 0**, complete JSON byte-identical; logs `scratch/p0d/search-2.txt` and `search-3.txt` |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0d.mjs --unit-only` | 0; six unit/algorithm-cross-check tests |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0d.mjs --write-traces` | 0; nine tests, writes only new P0d evidence |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0d.mjs` | 0; nine tests, exact trace bytes checked |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0; eight tests, original trace fixtures unchanged |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0; nine tests, original trace fixtures unchanged |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0; nine tests, original trace fixtures unchanged |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs` | 0; complete original JSON compared byte for byte |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c-search.mjs` | 0; complete original JSON compared byte for byte |
| `npm run build --prefix ui-prototype` | 0; TypeScript/Vite, 46 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | Initial sandbox launch failed (wrapper 1, no Python process); approved interpreter run 1 because this new worktree lacked the pinned governance submodule; after checkout, **0**, 13 protected planning files checked |
| `git submodule update --init -- ai-governance-framework` | 0; initialized existing pin `e8e67796894cd562ef0bce217bfad0fac211a44d` inside P0d only; no version update or governance source change |
| `git diff --exit-code 13a6e17 --` original P0/P0b/P0c test, support, search and evidence paths | 0; old tests/support/search/output files unchanged |
| `git diff --check` | 0 |

The two accepted search wrappers explicitly preserve the native exit code:

```powershell
node --experimental-strip-types ui-prototype/tests/playable-l03-p0d-search.mjs > scratch/p0d/search-2.txt 2> scratch/p0d/search-2-progress.txt
$p0dRepeatExit = $LASTEXITCODE
$p0dRepeatExit | Set-Content scratch/p0d/search-2-exit.txt
exit $p0dRepeatExit
```

Run 3 uses the same command with filenames ending `3`. The two runs are
independent read-only processes, not model agents. Both recompute every search
and compare the complete UTF-8 report, including all counts, caps and witnesses.

## Hashes

| File / output | SHA-256 |
| --- | --- |
| `search-results.json` (UTF-8) | `055ad2cfc0645beb57ed21dc339abd5f97889f43b189aa910d60b9f9ac7bb468` |
| `witnesses.jsonl` (UTF-8) | `3b28d8f0afa7e542064254435e0ae7b1424a51cb9e8028ca57b83231b795ce60` |
| All three P0d search stdout captures (PowerShell encoding) | `8fedb24851d584cd658819277a2410e37531bcbc1597cabb1ad5fb199787be79` |
| Both P0d test stdout captures (PowerShell encoding) | `e77dee045313b94e4aee00e9490a170f3c47b87a7561895af821efc7a3979bc6` |
| P0 stdout | `f3b91ced586bd46a83e873c5b07750b72a08d4831a895e08a3b73e25465dcc15` |
| P0b stdout | `0ee81138822e187cff8a8c97d6696eaa2f69796e877a0429e5afacfd48c904c3` |
| P0b search stdout | `14d2beed456c76e53119b159c998e6b56b776f9c4fde1a7bf37cc834d0dcc6cb` |
| P0c search stdout | `de4ea34aacd662ea514444d1f2c53365dd921a8784f81575b55b7bfac627da8e` |

The four original stdout hashes match the previous P0c verification record.
PowerShell stdout hashes are not UTF-8 fixture hashes; they are kept distinct.
The two accepted full searches completed by **17:56:47 +08:00** (about 29
minutes into the task); the initial generation has the same stdout hash but
its wrapper exit remains recorded as 1. A hash equality assertion and explicit
check of both recorded native exit codes returned **0**.

## Other inspection/setup failures

- `rg` was unavailable; used PowerShell file reads. No tool installed.
- Initial public skill downloads failed in the sandbox. Approved read-only
  retrieval succeeded; all three pinned SHA-256 values matched the existing
  source manifest. Bodies remain ignored under this worktree's scratch.
- `ui-prototype/vite.config.ts` and
  `governance/RESPONSE_ENVELOPE_CONTRACT.md` do not exist. The package scripts,
  tsconfig and `AGENTS.base.md` fallback were used, respectively.
- One PowerShell summary-only `foreach` pipeline failed to parse (1); corrected
  by storing the rows before piping (0). No evidence or rules changed.
- Sandbox Git inspection emitted an inaccessible user-global ignore warning;
  no global configuration, trust, credentials or hooks were changed.

## Evidence boundary

The new tests cover opt-in defaults, threshold validation/reset, deterministic
swap path and stopping, collision/terrain invariants, no early progress,
multiple-enemy sequencing, retry and stale-turn guards. A's two-command search
is independently cross-checked against the **unchanged P0c algorithm**: exactly
0 wins / 24,922 sequences. Every reported minimum and family representative is
legally replayed, with actual costs checked; original success/retreat traces
are also retained. Test generation followed by a normal read-only test run
compares the entire new JSONL byte for byte.

No complete unrestricted multi-turn search, human playtest, gameplay approval,
native governance callback, automatic session closeout, or Owner rule adoption
is claimed. This task does not change governance code, so it does not generate
a new governance-code acceptance receipt. The pinned submodule checkout only
restores the existing validator dependency in this separate worktree.
