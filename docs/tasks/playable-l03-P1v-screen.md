# Task P1v — first playable L03 battle screen (segment 1 of P1, 90 min timebox)

Authorized by Gavin 2026-10-22 17:13 Asia/Taipei: "兩個並行：Codex 做 P1 畫面，P0d 之後再補".
This authorizes ONLY this segment. P0d (`docs/tasks/playable-l03-P0d-pressure.md`) is written but deferred. Do not run it now. P2–P6 each still need separate authorization.

## Why
Gavin wants to play the battle with his own hands: see the map, the characters, the UI and the movement animation, instead of judging it only from headless searches. The rules question is not settled. P0c rated variant A THIN, so treat this screen as a test bed for the rules, not the final design.

## Goal
Add a browser-playable L03 hold battle driven entirely by the existing pure rules in `ui-prototype/src/playable-l03/rules.ts`, with the **A variant enabled for this screen only**: survive 6 turns, A's config flag on. The rules default and every P0/P0b/P0c test and output stay unchanged.

## Do
1. Add a new, separate entry point, for example a "Playable L03 (P1v)" button in `main.tsx` next to the existing L03 preview, and a new component under `ui-prototype/src/playable-l03/`. Do NOT rewrite `L03Preview.tsx`, `ArtGate.tsx` or `Battlefield.tsx`. Reuse their terrain, sprites, `AnimatedActor`, landmarks and CSS where possible.
2. Render the following from rules state:
   - the 11×9 map and the winch (2,1)
   - the 5 units: allies and the two knights, using the existing character art
   - a turn counter (x/6), winch progress (x/3), and the victory and defeat conditions in one short line
3. Player controls:
   - click a unit to select it and show its legal moves (highlighted, max 3 orthogonal steps)
   - click a highlighted tile to move there
   - Wait
   - End Turn
   - keyboard: Esc cancels a selection, Enter ends the turn
   - illegal clicks are rejected with a short message
4. Enemy phase:
   - before End Turn, show each knight's intent: its planned path or target tile, plus a one-line reason
   - after End Turn, animate the moves step by step from the rules `events`, using the existing walk animation
   - then update progress
   - the result must be identical whether or not the animation is played; add a "skip animation" toggle
5. Victory and defeat screens with Retry, which resets to the initial state.
6. Copy only: short Traditional Chinese UI labels. No story text, no new characters, no new art, no new dependencies.

## Acceptance
- `npm run build` exits 0. All P0, P0b and P0c tests still pass unchanged.
- Add a Playwright test, `tests/playable-l03-p1v-browser.mjs`. It loads the screen, replays the original P0 success trace under A, and reaches victory. It replays the P0 failure trace and reaches defeat. It checks that Retry clears all state.
- Add screenshots at 1280×720 and 1920×1080 to `ui-prototype/docs/playable-l03-p1v/`: the start of the battle, the knights' intent shown, mid-animation, victory, and defeat.
- Add a handoff section "P1v playable screen" to `docs/handoff/codex-playable-l03-research.md`. It covers how to run it (`npm run dev` plus where to click), what works, known gaps, and the resource self-check: game-ui-ux and game-feel now apply, and the 8-item playable bar becomes PASS/FAIL where testable. Mark human playtesting as HUMAN_PENDING.

## Stop
Commit, then try `git push`. If the push fails, leave the commits local and say so. Don't start P0d or P2, touch main, open a PR or use git stash. Stop at the timebox. If you aren't finished, commit what works and list what's left.
