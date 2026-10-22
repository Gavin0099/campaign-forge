# Task P1v2: battle-screen readability fix (P1 segment 2, 60 min timebox)

Authorized by Gavin on 2026-10-22: chain P1→P6 before the Codex reset, and review each segment. The source is the GPT P1v review (`docs/review/gpt-playable-l03-p1v.md` on `origin/review/gpt-playable-l03-research`), P1 finding 1 and decision 2.

## Goal
Players must be able to reliably tell units apart, read their labels, and click them, even when units stand on adjacent tiles. Fix only that. Keep the rules unchanged and keep variant A on this screen only.

## Do
1. Depth-sort the units by isometric row/column, so units in front draw over units behind them.
2. Scale and anchor the sprites so a unit's feet sit on its own tile and it doesn't cover the neighboring tile's unit or label.
3. Move the name labels so they don't collide. For example, put them on a small nameplate under the unit's base, or show only the selected/hovered unit's full name.
4. Make each unit's click/hit area its own tile, not the sprite bounds.
5. Mark ally and enemy clearly, using tile base color or rings.
6. Don't add new art, skeletal animation, new rules, P2 enemy behaviour or new dependencies. Don't edit `L03Preview.tsx` or `ArtGate.tsx` beyond what is needed.

## Acceptance
- The build exits 0, and the P0/P0b/P0c and P1v tests still pass.
- Add Playwright cases for overlap situations: the cluster next to the winch from the P0 success trace, and two units in a column. Each case clicks every unit by its tile and asserts that the right one is selected and that its label is visible and not covered (use bounding-box checks).
- Add before and after screenshots at 1280×720 and 1920×1080 to `ui-prototype/docs/playable-l03-p1v2/`.
- Append a "P1v2 readability" section to `docs/handoff/codex-playable-l03-research.md`, including the resource self-check. Human playtesting stays HUMAN_PENDING.

## Stop
Commit, then try `git push`. If the push fails, leave the commits local. Don't start P2, touch main, open a PR, or use git stash.
