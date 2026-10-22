# P2 verification

Owner-named base: `ce45ad2b29ddbfd9e975e4f894b4001faa63d378`.
Worktree: `D:\campaign-forge\scratch\p2`; branch `codex/playable-l03-p2`.
Started 2026-10-22 approximately 18:15:14 Asia/Taipei (first recorded clock
18:15:17 after initial read/status batch). Timebox: 90 minutes.

## Actual results

| Command | Native exit | Evidence |
| --- | ---: | --- |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p2-search.mjs` final run 1 | 0 | Complete bounded search plus separate directed witness probe |
| Same command, final run 2 | 0 | Both JSON/JSONL outputs byte-identical |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p2.mjs` | 0 | 11 tests; `p2-tests.log` |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0 | 8 unchanged tests; original byte fixtures |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0 | 9 unchanged tests |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs` | 0 | 9 unchanged tests |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs` | 0 | Original output unchanged |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c-search.mjs` | 0 | Original output unchanged |
| `npm run build --prefix ui-prototype` | 0 | TypeScript + Vite; `build.log` |
| Installed Python 3.12 + `scripts/validate_ui_scope.py` | 0 | 13 protected planning files; `scope.log` |
| `P1V_URL=http://127.0.0.1:5184/ node --experimental-strip-types ui-prototype/tests/playable-l03-p1v-browser.mjs` | 0 | 26 unchanged browser checks; `p1v-regression/browser-results.json` |
| Node byte/hash assertion batch | 0 | `command-results.json` repeat/source hashes; original P1v evidence restored exactly |
| `git diff --exit-code ce45ad2 --` old P0/P0b/P0c/P1v tests/evidence, P1v TSX/CSS and package/lock | 0 | No changes, including regenerated legacy search output |
| `git diff --check` | 0 | No whitespace errors |

The raw native-exit captures are recorded in `command-results.json`. A successful
later command is not used to infer a prior test exit: final test/build/scope
and legacy-search batches captured `$LASTEXITCODE` after each process.

The final repeated report hashes are:

- `search-results.json`: `c51d862a9c1e3060643773ce4bac655db9bdccea30c2e8f0bd996ffc70b92d86`
- `witnesses.jsonl`: `81f5ff28141dd74707f7d4f4014a84c87535081b89b674230fa027e3aab42c79`

Two earlier complete runs also matched before the directed probe was added.
They are exploratory evidence in ignored scratch, not substituted for the two
final runs. Rules were not retuned after observing the cheap wins. The later
probe adds evidence only; its six-command witness is outside the <=3 table.

## Browser evidence

Used the already installed Chrome at
`C:\Program Files\Google\Chrome\Application\chrome.exe`, with a worktree-local
ignored `.codex/visual-browser-binding.json`. The existing unchanged harness
checks canonical path, length and SHA-256 before importing the driver or
launching Chrome, uses an allowlisted child environment and a private local
profile, and blocks non-local requests. No global trust or hook settings changed.

Built preview: `node ui-prototype/node_modules/vite/bin/vite.js preview
ui-prototype --host 127.0.0.1 --port 5184 --strictPort`. It served this worktree's
`dist`; no Vite development dependency cache or `npm install` was used. The
`node_modules` junction was treated as read-only.

The original P1v harness writes into its original evidence directory. That
directory was snapshotted first, this run's captures/report copied into
`p1v-regression/`, and original files restored byte-for-byte from that snapshot.
The raw report retains original capture paths; resolve them by basename in
`p1v-regression/` for this run. Every relocated capture hash and every source
hash in that report were verified. Old copied command/verification metadata
was removed from the new evidence folder to avoid mixing runs.

The 26 checks cover both resolutions, legal/illegal clicks, animated vs skipped
states, victory/defeat/retry, keyboard and repeat input, cancellation and exit,
reduced motion, 200% text, mobile fallback, old L03 preview, and both original
story routes including absent allies. This is **P1v regression with P2 disabled**,
not visible P2 intent or human-playtest evidence.

## Environment failures and recovery

- Initial sandbox `git fetch origin`: exit 1, unable to write this worktree's
  `FETCH_HEAD` in shared Git metadata. Approved fetch from the same P2 cwd: 0.
- `rg` is unavailable; used Git file listings and PowerShell reads instead.
- `python`/`python3` were not on this shell's PATH. Used existing
  `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`.
- First scope validator: exit 1, `ModuleNotFoundError: governance_tools` because
  this new worktree's pinned submodule was empty. `git submodule update --init --
  ai-governance-framework`: 0, checked out the existing unchanged
  `e8e67796894cd562ef0bce217bfad0fac211a44d` pin inside this worktree. Validator
  rerun: 0. No package install, dependency addition or pin update.
- Sandbox process setup later returned `setup refresh had errors`; those
  failures started no process and have no native exit code. Approved commands
  ran in the same P2 cwd outside that failing sandbox. No approval was rejected.
- One exploratory inline Node trace command had PowerShell quotation loss and
  exited 1 before loading rules; the corrected stdin script exited 0. It was
  not counted as an acceptance run.

The external-executable-trust-audit skill was read for the browser launch.
Chrome's existing binding was checked; ordinary shell/Node/npm/Git execution
still has ambient executable/toolchain roots. This is not a full trust audit,
native hook callback verification, or complete governance adoption claim.

## Boundaries

Only rules, P2 tests/evidence and the dedicated handoff are edited. Original
P1v source, fixtures, packages, story, shared PLAN/memory and decisions remain
unchanged. No other worktree source was manually read or edited; P0d reference
files were read through `git show`, and its harness was copied rather than merged.
The existing shared pre-push hook invoked its own framework self-smoke rooted
at `D:/campaign-forge/ai-governance-framework`, naming this worktree as its target.
It passed and the implementation push returned 0; this inherited hook invocation
is not a claim of workspace-native lifecycle callbacks. See handoff for details.

The handoff is the task-local milestone record. Shared PLAN/memory reconciliation
is left to the coordinator because this task expressly restricts writes to P2
and their prescribed shared lock lives outside this worktree. No lock outside
the worktree or canonical daily memory was written. Task DONE is not SessionEnd.

See the handoff for actual commit/push results. No main push, PR, deployment,
Actions, force, stash, hook bypass, formal story/rule adoption or UI integration.
