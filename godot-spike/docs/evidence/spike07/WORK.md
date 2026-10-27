# spike-07 work ledger

Owner authority: 2026-10-27 09:54 Asia/Taipei; brief fc85094 on top of
1cff2db, clean codex/godot-spike worktree. Only godot-spike/ writes, local
W1–W8 commits, no push/merge/PR/stash. No new agent, art, story or shared-file edit.
All combat values remain spike test values, not canon.

## W1 — freeze and baseline

Keep criterion: original 100 runs reproduce, >=40 fixed seeds and full-route
leader-dash reveal bypasses without changing the seeded variation definition.
Snapshot spike06 data and operator; spike05 retained. Only telemetry gains
phase-start potential threat counts, attacker/source/death cells and spent/left
retreat budgets. Potential exposure is a legal reach/attack upper bound, not a
prediction that every enemy will select that scout. Existing register's boolean
could_attack loop now short-circuits on true; no state/event changes.

40 seeds = original 24018,1001–1019 plus 1020–1039. No deployment jitter or random
damage. Same AI coordinate ties and within-class policy ordering. Leader-dash
starts at real deployment and prioritizes leader attack slots while penalizing
wave threat; bypass remains explicitly SCRIPTED T5 partial start.

Original 100 trace hashes, commands, outcomes, archetypes, unit-turns and wave
engagement reproduce exactly (original20-reproduction.json). Flank14/20,
road10/20; 1014/1015/1017 retain T6 zero-death wave-free scripted wins.
New40: road50%, flank62.5%, turtle12.5%, retreat0%, leader-dash85% with33/40
wave-free wins. Flank also has1 full-route bypass win. See baseline/aggregate.json
for all policy×outcome strata, Wilson intervals, casualty/death spans and traces.
Distinct traces are not independent samples or a human difficulty estimate.

Commands: headless import exit0; test_spike07.gd3/3,8assertions exit0;
six-policy sweep partitioned into disjoint headless routes/naive/dash runs,
each exit0; summarize_spike07.py and check_spike07_baseline.py exit0.
Original unpartitioned sweep was interrupted to short-circuit telemetry and
split independent work. One half-written flank1015 JSON caused resume parse
failure; resume now validates/recomputes incomplete files. Failed/interrupted
logs retained under attempts; final240 outputs validated. No timings from
concurrent headless runs are treated as native performance evidence.

Historical seed assertion now pins SPIKE06_SEEDS; new test pins40 unique seeds
and first20 order, snapshot equality and deterministic real-deployment dash.
No earlier assertion removed or weakened.

Tool boundary: supplied absolute Godot/Python paths initially unavailable inside
sandbox; escalated commands succeeded (Godot4.7.2 ed1daf0bf, Python3.12.10).
Process listing showed only this CLI explicitly targeting this worktree and no
Godot before start; desktop app worktree association cannot be independently
proved from process command lines. No global trust/config changes. Existing
offline Python tools do not launch subprocess/network; ambient DLL/environment
trust is not fully audited and no comprehensive trust-root claim is made.
Resource methods read from fixed awesome-gamedev-agent-skills0a70cfc: prototype-fast,
level-design, game-ai, game-ui-ux, game-feel; no install/copy or new dependency.
