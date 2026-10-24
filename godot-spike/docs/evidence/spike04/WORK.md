# spike-04 work ledger

Owner brief `cbf3608`, clean branch `codex/godot-spike`; task-specific worktree
authorization supersedes the older main-worktree role table. Commit only.
Sandbox fetch initially denied metadata access; scoped elevated fetch succeeded.
Process names can be inspected but do not establish which desktop worktree is
open. Proceeding under Owner's explicit autonomous worktree authorization.

Question: can a human navigate, find threats and finish a 24×18 tactics battle
with 160×94.5 diamonds and 96px stand-ins? Separate disposable spike, not canon.
Keep only after a full human battle confirms navigation/readability/pacing;
retune or discard if long walks or camera discomfort outweigh tactical choices.
W1–W8 is the binding scope; no arbitrary short skill timebox overrides it.

W1 choices: flash mix .8, hold/duration unchanged (16.67/80ms); crit changes
duration only, effective mix stays .8. Spark22/spoke7/crit1.3; directional streak22
unchanged; bias .8 narrows spray. Fonts24/30 are 14.29%/11.76% smaller.
Dust count and its normal parameters unchanged; crit count follows the required
lower shared particle multiplier. Hitstop/shake/recoil/zoom/SFX unchanged.
Historical spike03 tests explicitly select the exact preserved resource so their
assertions remain meaningful; separate tests enforce spike04 default values.
No PLAN/memory/shared-file edits: this brief restricts writes to godot-spike/.

W2: separate pure FieldRules + authored level data. Six allies / twelve initial enemies; defeat leader, Thoma loss or turn >15. Warning starts player turn4, arrival starts turn5, arrivals first eligible enemy turn6. Occupied entry uses nearest empty passable BFS; defer if full. Ranged has no LOS, Manhattan2-3. Mobile retains melee knockback semantics, forest costs3. AI guard radius4, group attack alerts, leader holds until attacked/point contested within2. Reverse Dijkstra maps are phase-local, keyed by archetype/side/occupancy_revision. GUT12/12,264 assertions, exit0; import0.

W3: independent Field24x18 scene, batched rule-driven ground, textured PLACEHOLDER tiles/chunks, y-sorted props with occlusion fade,96px reused frames and BOW/BOOT/leader badges. Preview then confirm move/attack, keyboard/hover/threat/end-turn/wait/restart, enemy2x and movement skip, Reduced Motion. Small impact adapter intentionally leaves Skirmish unchanged. Initial smoke exited0 despite parse error; rejected log retained. Initial GUT4/4 had locked-object teardown error; fixed by letting action signal unwind; final4/4,474 assertions clean exit0. First rendered tile noise was too coarse; softened with our original earth patch, no frame art touched. W4 camera layers pending at this step.

W4: independent camera base/focus/impact layers; pan620px/s scaled byzoom, WASD/arrows, middle drag, cursor-anchored .8/1/1.2, O preserves prior base/zoom, F/Home selected follow, E edgeOFF bydefault. Overview reading uses whole field; clicking returns and centres. Reduced Motion snaps with no shake/punch/focus animation. Bounds include authored empty120px horizontal/180px vertical HUD-safe perimeter. Shake clamps within these bounds. Attack restores saved base/zoom exactly; no drift without event/input. Initial camera test4/6 caught float32 tolerance and viewport-injected synthetic mouse delta; final6/6,129 assertions with .001 tolerance and direct InputEvent drag contract. Real parsed drag remains W6 runtime evidence. Field battle regressions4/4 exit0.
