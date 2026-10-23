# Task P1v7: zero-step turn feedback and a playback-synced blocked marker (60 min timebox)

Authorized by Gavin on 2026-10-23 (Asia/Taipei): 「開 P1v7：修無移動回合的回饋和播放同步的受阻標記」 ("Start P1v7: fix feedback on turns with no movement and sync the blocked marker with playback"). This follows the P1v6 GPT review (`docs/review/gpt-playable-l03-p1v6.md` on `review/gpt-playable-l03-research`, verdict needs Owner, no P0). That review found two P1 problems and one P2 problem. The Owner accepted one P1 as is (see step 3), and this segment fixes the other two.

This is a small, presentation-only segment. Do not change `rules.ts` or any rule outcome, do not change event order, do not touch the P2 worktree or other scratch worktrees, do not add npm dependencies, and do not generate new art.

## Do
Work in priority order. Commit after each step so that partial progress survives a quota cutoff.

1. **Visible feedback on zero-step turns** (review P1, `PlayableL03.tsx` ~166–168).
   - Today a turn whose events contain no `move` path steps runs `playThrough(0)` and then calls `finish()` synchronously. Block, 「通道受阻」 and winch-progress cues for that turn may land in the same React batch as the state commit, so the player may never see them.
   - Give zero-step turns a separate presentation path: a short cue (roughly 600–900 ms is a reasonable target) that stays visible after `finish()` commits the state.
   - The cue must be **non-blocking**. It must not extend `busy`, the animation lock or the input wait for any turn, whether it has moves or not. Input stays available as soon as `finish()` runs, as it does today. Starting a new action, or Retry, clears or replaces the cue cleanly, with no stale effects and no double commit.
   - For example, keep cue state independent of `pending`/`busy`, with its own serial and expiry, the same way landing dust uses `expiresAt`. Reuse the existing painted block, 「通道受阻」 and winch visuals and keep the dark-fantasy style. Do not add a modal or toast that covers the board.
   - Normal turns with moves keep their current timing exactly. Do not add a pause before or after `finish()`.
2. **Blocked marker synced to playback** (review P2, ~325–326).
   - Today, during playback, the marker list comes from `intents`, the final prediction for the whole turn based on the committed state, but its position comes from `visualUnits`. That mixes the end-of-turn result with the moment being played, and it can reveal a block before it happens.
   - Keep the preview phase as it is.
   - During resolution, derive the shown blocked set from the events played so far: an enemy's marker appears when its `blocked` intent event (its `block` cue) has been reached, and is placed at that enemy's current visual cell. Prefer a pure helper, for example `blockedAtEventIndex(events, playedIndex)` in `feedback.ts`, plus a played-event index tracked alongside `nextCue`.
   - After `finish()`, the marker returns to the normal prediction for the new state.
   - Skip and Reduced Motion jump straight to the committed state, so they show the final static marker and nothing transient.
3. **Last landing shares the `finish()` boundary: accepted, document only** (review P1, ~168–183).
   - The Owner accepted the reviewer's recommendation: don't lengthen every turn for 180 ms of dust. Make no timing change for this.
   - Make sure the handoff and `VERIFICATION.md` state this as an accepted known limit, and add a short code comment at the boundary. If step 1's cue mechanism naturally lets the final dust outlive `finish()` without adding any wait, that is fine, but it is not required.

## Rules
- Every transient cue respects Reduced Motion and the 「跳過動畫」 ("skip animation") toggle. With either on, show no transient effects. The blocked marker is static state, so it stays visible.
- No change to rule outcomes, event order or the behavioural assertions in existing tests.

## Acceptance
- Build exits 0. All 107 existing game checks pass: the P0, P0b and P0c pure suites, the P1v6 pure feedback tests, and the P1v through P1v6 browser suites. Update selectors only if the markup changed, and keep every behavioural assertion.
- New tests:
  - **Pure tests** for the playback-synced blocked helper: no marker before the enemy's `blocked` intent event, a marker from that event on, and a correct set when several enemies are involved.
  - **Browser test, zero-step turn.** Set up a turn that resolves with no move steps but with a blocked and/or winch-progress event. Assert:
    - the cue becomes visible and stays visible for at least ~300 ms after the state commit;
    - input is accepted immediately after the commit, with no added lock (measure it);
    - a normal turn with moves keeps the same lock duration as P1v6;
    - the cue is absent with Reduced Motion or skip on;
    - Retry or a new action clears the cue.
  - **Browser test, synced marker.** During an enemy phase where a blocked enemy's intent comes after another enemy's move, the marker is absent while the earlier move plays and present once the block is reached.
- Save screenshots at 1280×720 to `ui-prototype/docs/playable-l03-p1v7/`, showing:
  - the zero-step cue (block and/or winch progress) visible after the commit;
  - the synced blocked marker before and after its event during playback.
  Write `VERIFICATION.md` there with commands, real exit codes and results, including the accepted last-landing boundary.
- Final verification commit: tests and build results plus the screenshots.
- Then a handoff section "P1v7" in `docs/handoff/codex-playable-l03-research.md`: what is done, what is skipped, the accepted limit, and a resource self-check (game-feel and game-ui-ux PASS or FAIL with evidence; human playtest stays HUMAN_PENDING).

## Stop
Commit only. Don't push, because the Owner's agent pushes afterwards. Don't touch main, open a PR or use git stash. Stop after the handoff commit and wait for review.
