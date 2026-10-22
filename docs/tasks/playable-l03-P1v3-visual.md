# Task P1v3: make the battle screen look like a game (visual pass, 90 min timebox)

Authorized by Gavin on 2026-10-22 at 19:04 (Asia/Taipei). He said: 「畫面還是很弱、看起來不像遊戲、風格也不統一，先優化這邊」 ("The screen still looks weak, doesn't look like a game, and the style isn't consistent. Optimize this first.")

P2 (enemy rules) is running in parallel in `D:\campaign-forge\scratch\p2`. Do not touch `rules.ts` or that worktree. This segment is presentation only.

## Problem (from P1v2 screenshots)
- The tiles are flat and colored like a spreadsheet grid. The units are tiny (about 1/4 tile tall) and unreadable at 720p.
- The UI panels look like an admin dashboard: plain boxes, lots of developer text such as coordinates and "已移動".
- Styles are mixed. The project has painterly, dark-fantasy art in `ui-prototype/public/art/`, but the screen barely uses it.

## Target look
Read `ui-prototype/docs/ART-DIRECTION.md` first and follow it. Where it conflicts with this brief, ART-DIRECTION wins; note any conflict in the handoff.

Use a classic isometric SRPG as the reference (Tactics Ogre / Triangle Strategy feel): a readable board that feels painted, characters as the visual focus, and framed UI that fits the art. Keep one consistent dark-fantasy palette taken from the existing art.

## Do (existing assets only, no new dependencies)
1. **Board**
   - Texture the tiles with `terrain-v2.png` (grass, stone, water and forest quadrants), cropped and clipped to the iso diamonds.
   - Give each tile visible side faces or edges for depth.
   - Animate the water subtly (CSS only, and respect Reduced Motion).
   - Draw the landmarks (winch, broken bridge, wagon) from `landmarks-v3.png` / `props-v2.png` where they fit.
   - Optional: use `ferry-scene-v2.png`, darkened and blurred, as the backdrop behind the board.
2. **Characters**
   - Make units about 1.2–1.5 tiles tall using the `l03-party-v1.png` / `l03-enemies-v1.png` crops.
   - Add soft shadows. Show ally and enemy with a subtle colored ring at the feet, not big debug shapes.
   - Keep P1v2's depth sort and tile-only hit areas. Readability must not regress: rerun the P1v2 overlap tests.
3. **UI frame**
   - Restyle the top bar, side panel and action bar as framed fantasy panels: dark parchment or metal, a serif heading font already available, and gold accents.
   - Turn the unit list into small portrait cards, cropped from the party art, that show acted/ready state with an icon instead of text.
   - Show enemy intent as a card with the knight's portrait plus arrows on the board.
   - Turn the turn and winch counters into icon gauges.
   - Hide coordinates and debug text unless a dev toggle is on.
4. **Feel**
   - Selection pulse and hover highlight on tiles.
   - A move path preview.
   - A small arrival bounce.
   - A banner for turn transitions ("敵方回合" / "我方回合").
   - Victory and defeat screens styled as a framed banner over a dimmed board.
5. **Consistency.** Write a short style guide at `ui-prototype/docs/playable-l03-p1v3/STYLE.md` covering the palette, fonts, panel style and unit scale, so later screens match.

## Constraints
- No rules changes. Variant A stays scoped to this screen.
- No new generated art and no new npm dependencies.
- Use the existing licensed assets only, and record which ones you used.
- No story text changes.
- Don't edit `L03Preview.tsx` or `ArtGate.tsx` except to share CSS tokens.

## Acceptance
- Build exits 0. The P0, P0b and P0c tests, plus the P1v and P1v2 browser tests, still pass. Update selectors if the markup changed, but keep every behavioural assertion.
- Save before/after screenshots at 1280×720 and 1920×1080 to `ui-prototype/docs/playable-l03-p1v3/` covering: start, selected unit with move range, enemy intent, mid-animation, turn banner, victory and defeat.
- In the handoff section "P1v3 visual pass", list the assets used, the style guide, known gaps, and a resource self-check. For game-ui-ux and game-feel, mark each item PASS or FAIL with evidence. Human playtest stays HUMAN_PENDING.

## Stop
Commit, then try `git push`. If the push fails, leave the commits local. Don't touch main, open a PR or use git stash.
