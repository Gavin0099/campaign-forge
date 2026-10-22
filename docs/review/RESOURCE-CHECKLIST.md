# Resource review checklist (every chunk)

Owner rule (2026-10-22): every finished chunk is reviewed against these resources before Gavin decides on it.
Codex self-checks in its handoff, then Claude and GPT each fill this in. Mark each line PASS / FAIL / N/A with evidence (file:line, command + exit code, or screenshot).

## A. Skills (read only the relevant SKILL.md; do not install)
Source: https://github.com/gamedev-skills/awesome-gamedev-agent-skills
- [ ] prototype-fast (P0): is this the simplest version that proves the mechanic? Were keep/discard conditions stated up front?
- [ ] level-design (P0): are terrain, routes, objectives and placements reachable and meaningful? Is there a verified win path for each branch?
- [ ] game-ai (P0): do enemies pick targets and act from understandable rules that react to the player's state?
- [ ] game-ui-ux (P1): are move range, threat, enemy intent, objective progress and input hints visible?
- [ ] game-feel (P1): are hit reaction and pacing readable without slowing turns down?

## B. Reference repos (architecture only; never copy unlicensed code or art)
- [ ] franciscobom/Grid-Tactics (no license; read-only): is game logic separate from the view? Do pure functions resolve state, with animation only playing events?
- [ ] HopeMetal/2DTacticalRPGDemo (MIT): any pattern borrowed is credited, and asset licenses were checked separately.
- [ ] No new engine or dependency (Phaser, Godot, easystarjs, @pixi/react) without an isolated PoC and Owner approval.

## C. Playable acceptance bar
- [ ] A player can play a full 3–5 minute battle alone.
- [ ] Enemies take understandable actions based on the player's state.
- [ ] The player can win or lose.
- [ ] Two tactical choices lead to different outcomes.
- [ ] The player can restart and change strategy.
- [ ] No duplicate resolution, stuck turns, invalid moves or interrupted animations.
- [ ] Works at 1280×720 and 1920×1080, plus basic keyboard play.
- [ ] Automated tests and human playtest feedback are recorded separately; model review is never human playtest.

## D. Project rules
- [ ] SRD 5.2.1 / CC-BY sources only, with attribution; no WotC IP. Rule changes follow docs/design/RULE-ADAPTATION-CONTRACT.md.
- [ ] Stayed inside the AGENTS.md authorization; no merge to main; no new plot or setting without Owner approval.
