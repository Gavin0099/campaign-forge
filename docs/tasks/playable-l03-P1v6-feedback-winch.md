# Task P1v6: per-event feedback and a hand-painted winch (90 min timebox)

Authorized by Gavin on 2026-10-23 (Asia/Taipei): 「開 P1v6：修正回饋，也重畫手繪絞盤」 ("Start P1v6: fix the feedback and redraw the winch by hand"). This follows the P1v5 GPT review (`docs/review/gpt-playable-l03-p1v5.md` on `review/gpt-playable-l03-research`, verdict needs Owner, no P0). That review found three P1 problems and two P2 problems; this segment fixes all five.

Presentation and art only. Do not change `rules.ts` or any rule outcome, do not touch the P2 worktree or other scratch worktrees, and do not add npm dependencies.

## Do
Work in priority order. Commit after each step so that partial progress survives a quota cutoff.

1. **Per-event feedback timeline** (P1, `PlayableL03.tsx` ~60–79 and ~158–174).
   - Today `finish()` fires the winch, block and arrival feedback all at once after the whole animation ends. Replace that with a small presentation timeline built from `result.events` in order.
   - Each feedback effect is scheduled at the visual moment of its own event. Landing dust fires when that unit's last path step lands. A block fires when that enemy's intent is played. Winch interference fires when the `progress` event is reached, after the moves that caused it.
   - Keep the timeline a pure, testable function, for example `buildFeedbackTimeline(events, stepMs)` in a new presentation module that returns `{ atMs, kind, unit, cell }[]`.
   - The rule state is still committed exactly once, in `finish()`. Feedback playback must not delay input beyond the existing animation lock.
2. **Spark only on real contact** (P1, ~64–75).
   - Don't pick an arbitrary adjacent ally. The `blocked` intent event has no blocker id, so derive the blocker in presentation code with a pure counterfactual query: for each living ally adjacent to the blocked enemy's route, run the existing pure `resolve`/`command` on a copy of the state with that ally removed. The ally is the blocker only if the enemy's path to the winch then opens.
   - Play the 「阻擋」 clash spark only between the enemy and a confirmed blocker.
   - If no single ally is confirmed, show no spark, only the blocked marker from step 4 plus a 「通道受阻」 label.
   - Don't edit `rules.ts` to add a blocker field.
3. **Landing dust for every mover** (P1, ~78–79). Emit one arrival or dust effect per `move` event, not only for the last one. This covers several enemies moving in the same enemy phase, and they may overlap in time.
4. **Blocked-enemy marker on the map** (P2, ~250–264). A blocked enemy has no predicted target today. Draw a clear marker at its feet in both the intent preview and during resolution, so the state reads from the board without the side panel. Use a painted-style broken-chain or barred sigil, not a plain red X. It must stay legible at 720p.
5. **Hand-painted winch and rope** (P2, `presentation.tsx` ~68–72).
   - Remove the geometric SVG wheel (the circle and cross lines) and the plain SVG rope path.
   - Replace them with hand-painted art, either:
     - 3–4 transparent winch frames (rest, turning ×2, jerk), or
     - one painted winch plus a separately painted drum or handle layer that rotates.
   - Add a painted rope strip or frames for the slack and taut states. A light shake transform on the painted rope is fine.
   - Generate the art with built-in image_gen to match `ui-prototype/docs/ART-DIRECTION.md` and `ui-prototype/docs/playable-l03-p1v3/STYLE.md`: dark fantasy, hand-painted, light from the upper left, earthy low-saturation palette, the same brushwork as `public/art/l03-p1v4/battlefield.png` and `props.png`. Crop or derive it from the existing winch prop if that matches better.
   - Keep the 2/3 warning state, but in the painted style, for example a red-ember glow on the painted drum rather than a flat ellipse stroke.

## Art rules
- Save originals under `ui-prototype/public/art/l03-p1v6/`.
- Record every generated image's prompt, date and hash in `ui-prototype/docs/art-prompts.json` / `art-manifest.json`, the same way as in P1v4.
- Keep one consistent style. Reject and regenerate any output that doesn't match, keep rejected attempts as `*-attempt-NN.png`, and list them in the handoff.
- No commercial game imagery, no imitation of existing IP, no WotC IP.

## Rules
- Every effect respects Reduced Motion and the 「跳過動畫」 ("skip animation") toggle. With either on, show no transient effects. The blocked marker is static state, so it stays visible.
- No change to rule outcomes, event order or tests' behavioural assertions.

## Acceptance
- Build exits 0. All P0, P0b and P0c tests and the P1v through P1v5 browser tests pass. Update selectors only if the markup changed, and keep every behavioural assertion.
- New tests:
  - **Unit tests for the timeline function.** Feedback times follow event order. Each `move` event gets its own landing. Winch feedback comes after the moves that caused it.
  - **Spark targeting.** A blocked enemy with a confirmed blocker gets a spark tied to that ally. A blocked enemy with only incidental adjacent allies (no counterfactual opening) gets no spark.
  - **Browser test.** During an enemy phase with two movers, a landing dust appears for each, at different times, before the turn finishes. The winch feedback uses the painted assets (no `.p1v-winch-wheel` circle). All effects are absent with Reduced Motion or skip on.
- Save screenshots at 1280×720 to `ui-prototype/docs/playable-l03-p1v6/`, plus a short frame sequence for the winch turn, showing:
  - the painted winch turning with the rope taut,
  - the 2/3 warning,
  - a block spark on a confirmed blocker,
  - landing dust on two movers,
  - the blocked-enemy marker.
  Write `VERIFICATION.md` there with commands and results.
- Final verification commit: tests and build results plus the screenshots.
- Then a handoff section "P1v6 feedback and winch" in `docs/handoff/codex-playable-l03-research.md`: what is done, what is skipped, assets and rejected attempts, and a resource self-check (game-feel and game-ui-ux PASS or FAIL with evidence; human playtest stays HUMAN_PENDING).

## Stop
Commit only. Don't push, because the sandbox cannot reach GitHub and the Owner's agent pushes afterwards. Don't touch main, open a PR or use git stash. Stop after the handoff commit and wait for review.
