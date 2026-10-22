# Task P1v4: hand-painted battlefield and character scale (art pass, 120 min timebox)

Authorized by Gavin on 2026-10-22 at 20:33 (Asia/Taipei): 「做 P1v4，可以用生圖補美術」 ("Do P1v4; you can use image generation to fill in the art"). This follows the P1v3 GPT review (`docs/review/gpt-playable-l03-p1v3.md` on `review/gpt-playable-l03-research`), whose verdict was needs Owner. P1v3's UI frame passed. The battlefield and the characters did not.

Presentation and art only. Do not change `rules.ts`, do not change the P2 worktree, and do not add new npm dependencies.

## Fix these P1 findings
1. **Battlefield.** Replace the 99 repeated diamond textures with ONE hand-painted isometric ferry battlefield image.
   - Generate it with built-in image_gen, matching `ui-prototype/docs/ART-DIRECTION.md`: dark fantasy, hand-painted, light from the upper left, earthy and low-saturation greens and blues.
   - Match the L03 layout: near bank, river with the broken bridge, far bank, and the winch on the near bank.
   - Align the interactive iso grid on top of it as a subtle overlay. Tiles show only on hover, in the move range, or on intent. The grid must still match the rules map exactly, so adjust the overlay transform rather than the rules.
   - Keep `ferry-scene-v2.png` as the backdrop only if it still helps.
2. **Props.** Replace the SVG geometry for the winch, broken bridge and wagon with hand-painted props on transparent backgrounds, either generated or cropped from the new battlefield.
3. **Portraits.** Give the two knights distinct portraits (generate one variant or crop differently). Every unit needs a unique portrait.
4. **Character scale.** Make units about 1.3 tiles tall (the brief range is 1.2–1.5).
   - Keep the depth sort and tile-only hit areas.
   - The P1v2 overlap and click tests must pass. If they genuinely conflict with the scale, choose the largest scale that passes and document why.
5. **Optional, only if time remains.** A 2–3 frame idle or attack pose for one character. Skip it rather than ship inconsistent frames.

## Art rules
- Record every generated image's prompt, date and hash in `ui-prototype/docs/art-prompts.json` / `art-manifest.json`, the same way the earlier art was recorded.
- No commercial game imagery, no imitation of existing IP, no WotC IP.
- Keep one consistent style with the existing party and enemy art. Reject and regenerate any outputs that don't match, and note the rejected attempts in the handoff.
- Save originals under `ui-prototype/public/art/l03-p1v4/`.

## Acceptance
- Build exits 0. The P0, P0b and P0c tests and the P1v, P1v2 and P1v3 browser tests pass. Update selectors only if the markup changed, and keep every behavioural assertion.
- Save after-screenshots at 1280×720 and 1920×1080 to `ui-prototype/docs/playable-l03-p1v4/` covering: start, a selected unit with path preview, enemy intent, the turn banner, victory and defeat.
- Measure and record the unit height to tile height ratio.
- Update `STYLE.md` from P1v3 with the battlefield and prop rules.
- Handoff section "P1v4 art pass": assets generated or used, scale, known gaps, and a resource self-check (game-ui-ux and game-feel PASS or FAIL with evidence; human playtest stays HUMAN_PENDING).

## Stop
Commit, then try `git push`. If the push fails, leave the commits local. Don't touch main, open a PR or use git stash.
