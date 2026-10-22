# P1v playable screen

Only `docs/tasks/playable-l03-P1v-screen.md` is implemented. Baseline:
`13a6e17496dca1eaa8d3a98fe459dc819b37e8a4`, clean
`codex/playable-l03-research`; Owner confirmed exclusive use of this worktree.
No pull. P0d is deferred; P2 is not started.

## Run and play

From `D:\campaign-forge`:

```powershell
npm run dev --prefix ui-prototype -- --port 5183 --strictPort
```

Open `http://127.0.0.1:5183/`, click **Playable L03 (P1v)** beside the existing
L03 preview. Direct entry: `http://127.0.0.1:5183/?scene=playable-l03`.
Port 5173 was already occupied; its process was left alone.

- Click an ally or its base/list button; highlighted **＋** tiles are legal
  destinations, at most three orthogonal steps. Click one to move.
- While a unit is selected, figures let destination clicks pass through;
  use another unit's base or roster button to switch units.
- **等待** forgoes that ally's movement for this player phase. This is a local
  UI choice: no new rules command or modification to `State.moved`.
- **結束回合** plays the knights' movement, then adopts the rules result and
  updates interference. Dashed arrows and sidebar reasons preview both knights.
- Space selects a focused cell; arrows move focus. Esc cancels selection;
  Enter on the map ends the turn. Native buttons retain their Enter behavior.
- **跳過動畫** also works during playback. Reduced-motion preference skips
  playback automatically. **重試** resets the state and UI after either result.

## Boundary and mechanism

Only this new screen passes
`{ ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 } }` to `initialState("open", …)`.
The rules default, pure rules, prior tests/searches/fixtures, package/lockfiles,
original art, `L03Preview.tsx`, `ArtGate.tsx`, and `Battlefield.tsx` are unchanged.

The view asks `command` for legal destinations and `resolve` for intent. An
accepted command produces one pending `Result`; the renderer plays each move
event's orthogonal path at 230 ms per step. Only completion/skip adopts that
same result, including progress and terminal status. A synchronous busy guard,
pending-result consumption, RAF cleanup and Enter-repeat/double-click guards
prevent duplicate resolution. Motion never determines an enemy action.

Existing L03 party/knight atlases, terrain texture, projection and wagon
geometry are reused. `AnimatedActor` accepts optional painted children to
apply its walk clock/bob; its existing articulated callers retain their path.
These single-frame L03 cutouts do **not** gain articulated limbs.

## Executed checks

| Command (repo root) | Observed result | Exit |
| --- | --- | --- |
| `npm run build --prefix ui-prototype` | TypeScript + Vite build | 0 |
| `node ui-prototype/tests/playable-l03-p0.mjs` | 8 tests; original traces byte-identical | 0 |
| `node ui-prototype/tests/playable-l03-p0b.mjs` | 9 tests; original stance/witness outputs unchanged | 0 |
| `node ui-prototype/tests/playable-l03-p0c.mjs` | 9 tests; defaults/variants and original witnesses unchanged | 0 |
| `node ui-prototype/tests/playable-l03-p1v-browser.mjs` | 26 checks, both sizes, original success/failure replay under A | 0 |
| `python scripts/validate_ui_scope.py` | 13 protected planning files, no Actions/root LICENSE, original assets present | 0 |
| `python scripts/record_governance_checks.py` | Fresh lifecycle replay, scope, typecheck and Vite receipts | 0 |
| `git diff --check` | No whitespace errors | 0 |
| `git diff --exit-code 13a6e17 -- <rules, all P0/P0b/P0c tests and outputs, three original views, art, package and lockfile>` | Empty diff for the enumerated protected paths | 0 |

On this machine Python is invoked through the existing binding
`C:/Users/daish/AppData/Local/Programs/Python/Python312/python.exe -I -B`.
The sandbox could not access that interpreter; the approved execution succeeded.
The recorder's durable receipt is `artifacts/governance-native-acceptance.json`;
it is isolated replay/build evidence, **not** platform-native lifecycle proof.

`browser-results.json` records actual check results, input/art SHA-256,
screenshot hashes, state and in-flight frame snapshots. Its final check
rejects source changes during the run. The browser uses the existing bound
Chrome after verifying exact path/length/hash, repo-local profile/temp and
loopback-only requests; no dependency or browser installation was added.

The P0 success trace is read from the existing JSONL without edits, followed
by A's sixth resolve: **success, turn 6, interference 2**. Original idle
failure: **failure, turn 5, interference 4**. `4 / 3` is the actual atomic
rules result when both knights contribute; the UI does not clamp it to 3.
Every committed command is compared with an independent pure-rules result.
Normal and skipped playbacks match exactly for both outcomes at both sizes.

Browser coverage also includes illegal water/enemy clicks, exact legal range,
unit-body selection, destination clicks behind a figure, Wait, Space/arrows,
Esc, Enter, duplicate/held input, mid-play skip, dynamic reduced motion,
exit/unmount/reopen, result focus/inert background, Retry, 200% actual body
text, 390px stacked fallback, direct entry, existing preview, dialogue log,
both original story branches, missing companions, move/skill preview/cancel,
confirmation and result-to-campaign. No page errors or failed HTTP responses.

## Runtime screenshots

All PNGs are actual Playwright viewport captures, with SVG artwork decoded
before capture. No generated mock screenshots or overwritten historical evidence.

| State | 1280×720 | 1920×1080 |
| --- | --- | --- |
| Start | [start](1280x720-start.png) | [start](1920x1080-start.png) |
| Knights' intent | [intent](1280x720-intent.png) | [intent](1920x1080-intent.png) |
| Mid-animation | [mid-animation](1280x720-mid-animation.png) | [mid-animation](1920x1080-mid-animation.png) |
| Victory | [victory](1280x720-victory.png) | [victory](1920x1080-victory.png) |
| Defeat | [defeat](1280x720-defeat.png) | [defeat](1920x1080-defeat.png) |
| Legal moves (extra) | [move range](1280x720-move-range.png) | [move range](1920x1080-move-range.png) |

Additional [200% text capture](1280x720-text-200.png) shows reachable controls
after scrolling. Zoomed and narrow layouts use vertical scrolling.

## Known limits and human status

- **HUMAN_PENDING:** no human playtest, 3–5 minute duration measurement,
  enjoyment decision, commercial art approval, or final rule selection.
  A remains the P0c **THIN** experiment, including known first-turn-then-wait wins.
- Only the open/hold encounter is playable here. No P0d pressure changes,
  sealed escort, damage/attacks, HP, new story, new art, engine, account or save.
- Existing tall single-frame cutouts overlap at adjacent diagonal positions;
  bases, labels and roster buttons remain available. Walking is eased tile
  travel with restrained bob, not new frame-by-frame character animation.
- Browser automation covers basic keyboard/reduced-motion/text behavior, not
  a screen-reader/gamepad audit, full WCAG certification or a performance study.
- Main, PRs, deployment, Actions and formal story/rule adoption remain outside
  this segment. Delivery status and SHAs are in the P1v handoff.
