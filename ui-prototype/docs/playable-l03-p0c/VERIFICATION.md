# P0c verification record

Owner scope: `docs/tasks/playable-l03-P0c-variants.md` only, verification,
45-minute maximum. Baseline `d42024bf381f466c665fb661f493e291968aa2bb`.
First recorded clock: 2026-10-22 15:31:55 +08:00 (the initial read/status
batch took 6.1 seconds immediately before it). Evidence freeze:
2026-10-22 15:43 +08:00. Commit/push/handoff overhead and final elapsed time
are in the handoff/final response. No P1, UI, art, attack, HP or story changes.

All commands run from `D:\campaign-forge`; existing Node tools only, no
new dependency. No `--write-traces` or `--write-results` on P0/P0b.

| Command | Real exit and evidence |
| --- | --- |
| `git status --short`; `git branch --show-current`; `git rev-parse HEAD` | 0; clean, required branch, baseline above |
| `git fetch origin` at task start | 0; updated review ref only; no pull per latest Owner instruction |
| `git show origin/review/gpt-playable-l03-research:docs/review/gpt-playable-l03-p0b.md` | 0; GPT review read, input not approval |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c-search.mjs --write-results` | 0; first full search, `scratch/p0c/search-1.txt` |
| Same search without `--write-results` | 0; second full search byte-checks committed report candidate, `scratch/p0c/search-2.txt` |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0c.mjs --write-traces` | 0; 9 PASS, new P0c witnesses only |
| Same P0c tests without `--write-traces`, twice | 0 / 0; 9 PASS each, byte-identical traces and stdout |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0.mjs` | 0; 8 PASS, original three fixtures exact |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b.mjs` | 0; 9 PASS, original fixtures exact |
| `node --experimental-strip-types ui-prototype/tests/playable-l03-p0b-search.mjs` | 0; original JSON exact, 493/6303 and 6/211 unchanged |
| `npm run build --prefix ui-prototype` | 0; TypeScript and Vite, 46 modules |
| `& 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe' scripts/validate_ui_scope.py` | 0 on approved existing-interpreter run; 13 planning files and original art protected |
| `git diff --exit-code d42024b --` original P0/P0b tests/support/search and both evidence directories | 0; original source tests and outputs unchanged |
| `git diff --check` | 0 |
| Shared-edit fetch and ancestor check | 0 / 0; no unknown remote commits, no pull |

PowerShell stdout capture SHA256 (ignored scratch, not UTF-8 JSON hashes):

| Output | SHA256 |
| --- | --- |
| Both P0c searches | `de4ea34aacd662ea514444d1f2c53365dd921a8784f81575b55b7bfac627da8e` |
| Both P0c tests | `d0a638e28ae85c6d9876f6553265b1c37b99a0999bb9cbb243958bce94a218c4` |
| P0 test | `f3b91ced586bd46a83e873c5b07750b72a08d4831a895e08a3b73e25465dcc15` |
| P0b test | `0ee81138822e187cff8a8c97d6696eaa2f69796e877a0429e5afacfd48c904c3` (same as P0b handoff) |
| P0b search | `14d2beed456c76e53119b159c998e6b56b776f9c4fde1a7bf37cc834d0dcc6cb` (same as P0b handoff) |

UTF-8 evidence SHA256:

- `search-results.json`: `4b45dc9bbf8c60a1b9ea786ecd3abed8270c2ca313abaab994633efb0029a88f`
- `multi-move-witnesses.jsonl`: `2598bb48e41e413380e19d0897834e05b7ff55c8933650a53acb90834fdf224b`

Setup/inspection failures are not omitted: `rg` unavailable (PowerShell
command failure 1, used local PowerShell reads); one summary-table pipeline
had a PowerShell parse error (1, corrected); the sandbox could not launch
the existing Python interpreter (command failure 1, no Python process/exit
code), approved retry passed above. A sandbox shared-edit fetch reported
`.git/FETCH_HEAD` permission denied; the approved retry returned 0. Its
combined shell's final 0 was from the later ancestor command, and is not
claimed as a successful fetch. No credentials, trust or hooks changed.

Results use default passage blocking ON, both original enemies and living
allies only. Absent solo/duo allies are removed. T1 is deduplicated by labeled
endpoint placement, not command order; <=1 move counts command/turn plus
idle once. Solo/duo witness search uses the same <=1 command/turn and 10,000
state cap as P0b, now including hold history in its key. B/B+ Karen+Lace
hits the cap but still supplies a legal win: existence only, never a count
or optimum. A's six reduced lineups find no win without hitting the cap,
but this still covers only <=1 move/turn, not all legal battle strategies.

Multi-move search is exact within **<=2 commands total AND <=2 per turn**,
for both 5 and 6 turns, all actors/destinations/orders, no cap. At five turns
B, B+2 and B+3 have 229, 208 and 172 wins out of 24,668 command sequences.
At six turns all three have 0/24,922 within this two-command bound:
**UNSOLVABLE within these bounds**, not a fix or a global impossibility claim.
No full six-turn variant verdict is inferred from this negative result.

The comparison, recommendation, resource self-check and delivery state live
in `docs/handoff/codex-playable-l03-research.md`, section
"P0c variant comparison". Browser/human playtest N/A; no session end claimed.
