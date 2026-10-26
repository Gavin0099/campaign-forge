# spike-06 work record (SPIKE TEST VALUES, not canon)

Owner authorization: 2026-10-26 19:17 Asia/Taipei; brief HEAD
8010bde2047bc9a5b268bedf03de64a2c1ef5873. Worktree starts
clean on codex/godot-spike. Scope is godot-spike/ only. No push/PR/merge/stash.
The Owner explicitly assigned this worktree; process listing found desktop and
CLI processes but does not prove their CWD. No additional agent is launched;
no concurrent file modifications observed. No claim of inspecting other worktrees.

## Fixed acceptance thresholds (set before W2 tuning)

- At least one intended policy >=60% wins on the committed 20 seeds; aim >=70%.
- A naive policy still loses >50%; wins must not all finish before T8,
  desired decisive turns 9–14. Winning policy true idle <=35%.
- Wave attacks or is attacked in >=70% of intended-policy winning seeds.
- Scouts outlive spike05 T4–5, lead/co-lead finishing kills/intercepts and do
  not lead damage. No HP padding, base damage/move/LOS/objective/limit changes.
- Enemy-phase estimate 15–25 minutes is reported honestly, never manufactured.
- Every new rule stays pure and has tests; all historical tests retained.

Keep/rework criterion: preserve the prototype if evidence shows an accessible
winning route with meaningful reinforcement/scout decisions. Rework if this
requires hidden forced engagement or arbitrary HP inflation. Human enjoyment,
blind plays and art approval are separate HUMAN_PENDING gates. The Owner's
W1–W8 scope supersedes the generic prototype-fast timebox; no art investment.

## W1

Preserved byte-for-byte field data as field_24x18_spike05.gd. Harness seeds:
24018,1001..1019. Seed24018 retains historical policy ordering; others hash
seed+turn+unit ID only among equal-class action choices and equal-HP targets.
AI retains its existing tiny coordinate tie-break. No RNG, deployment jitter,
damage variance or hidden game-rule adjustment. Trace distinctness excludes
report metadata. Bypass remains a labelled scripted mid-battle probe.

External executables: Owner-specified full Godot/Python paths fail resolution
inside sandbox; identical paths succeed with escalation (4.7.2/Python3.12.10).
Existing Git login/remote only, fetch succeeded. This is local offline tool use,
not complete trust-root hardening: inherited environment/DLL/Git resolution
are not adversarially verified. Evidence tools add no subprocess/network.
Shared PLAN/memory are outside this segment's writable scope; milestones are
recorded here and in the final project handoff. Task DONE is not SessionEnd.
