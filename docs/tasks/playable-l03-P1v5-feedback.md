# Task P1v5: battlefield interaction feedback (60 min timebox)

Authorized by Gavin on 2026-10-23 at 00:56 (Asia/Taipei): 「做 P1v5：戰場互動回饋，絞盤轉動拉索等」 ("Do P1v5: battlefield interaction feedback, such as the winch turning and pulling its rope"). This follows the P1v4 GPT review (`docs/review/gpt-playable-l03-p1v4.md`, verdict needs Owner), which recommended interaction feedback next. Gavin accepts the 1.0-tile unit scale for now.

Presentation only. Do not change `rules.ts`, do not touch the scratch worktrees, and do not add npm dependencies. CSS, SVG and canvas-free React animation are fine. Small new image_gen art (for example winch or rope frames) is allowed; record the prompt and hash as in P1v4.

## Do
Work in priority order. Commit after each step so that partial progress survives a quota cutoff.

1. **Winch interference feedback.** When an enemy interferes with the winch:
   - the winch visibly turns or jerks,
   - the rope pulls taut and shakes,
   - the winch gauge pip fills with a flash and a short number pop ("絞盤干擾 1/3").
   At 2/3, add a stronger warning state (red tint or pulse). At 3/3, transition into the defeat banner.
2. **Hit and shove feedback.** When a unit is shoved or blocked: a short knockback slide, a dust puff, a screen shake of 2–4 px max, and a damage or status pop. When an ally body-blocks an enemy, show a brief "阻擋" clash spark.
3. **Enemy intent telegraph on the board.** Pulse the target tile and animate the arrow so the threat reads before End Turn.
4. **Hover and confirm feedback.** A tile hover glow, a confirm pulse on move commit, and a subtle footstep dust on arrival.

## Rules
- Every effect respects the Reduced Motion setting and the existing 「跳過動畫」 ("skip animation") toggle.
- Effects must never block input longer than the existing animation lock.
- No change to rule outcomes.

## Acceptance
- Build exits 0. All P0, P0b and P0c tests and the P1v through P1v4 browser tests pass. Keep every behavioural assertion.
- Add a browser test asserting that the winch feedback appears when interference increments and is absent when reduced motion or skip animation is on.
- Save screenshots or short frame sequences at 1280×720 to `ui-prototype/docs/playable-l03-p1v5/` showing: winch interference, the 2/3 warning, a shove or block, and an intent pulse.
- Handoff section "P1v5 feedback" in the same handoff file: what is done, what is skipped, and a resource self-check (game-feel and game-ui-ux PASS or FAIL with evidence; human playtest stays HUMAN_PENDING).

## Stop
Commit, then try `git push`. If the push fails, leave the commits local. Don't touch main, open a PR or use git stash.
