# Native runtime AVI + PNG strips

ffmpeg is not installed. Godot --write-movie records native1280×720 MJPEG AVI at60 simulation FPS.
Pillow verifies AVI headers/every frame dimension and extracts native frames/PNG strips; no generated screenshot.

- [Enemy phase AVI](enemy-phase-60fps.avi) / [strip](enemy-phase-60fps-strip.png): real road-turn2 state, advancing front, normal speed.
- [Select→move→ranged attack AVI](select-move-ranged-60fps.avi) / [strip](select-move-ranged-60fps-strip.png): explicitly staged four-unit original-field fixture. Real parsed mouse select, move preview, Esc, move confirm, attack preview, Enter, return. Not a continuous battle.
- [Hitfeel](hitfeel/impact-strip-spike04-vs-spike05.png): normal/crit04 vs05, contact±8; four native AVI/contact sets.
- Continuous road scene is separately automated through actual scene actions to lose8; runtime-battle.json is not human play.
- reinforcement-interception.png isolates thoma+leader+wave on original map/stats; first attempted full-probe capture failed to produce an enemy wave strike and is preserved in attempts/.
- win-staged-terminal.png is a staged lethal rules/result fixture. lose.png is continuous road defeat.

AVI encoding/readbacks stretch wall time; fixed movie clock is not measured runtime FPS. PERFORMANCE.md uses a separate unrecorded run.
Dummy audio triggers were recorded, not auditioned. Human feel/art/pacing remain HUMAN_PENDING.

