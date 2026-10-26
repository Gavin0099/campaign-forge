extends "res://addons/gut/test.gd"
const R = preload("res://scripts/rules/field_rules.gd")
const D = preload("res://data/levels/field_24x18.gd")
const Old = preload("res://data/levels/field_24x18_spike05.gd")
func test_data_frozen_stats_objective_and_every_spawn_legal() -> void:
	var s := R.initial()
	assert_eq(s.level.size,Vector2i(24,18))
	assert_eq(s.level.stats,Old.STATS)
	assert_eq(s.level.rows,Old.build().rows)
	assert_eq(s.level.turn_limit,15)
	assert_eq(s.level.objective,"defeat_leader")
	var seen := {}
	for u in s.units:
		assert_gt(R.cost(s.level,u.cell,u.kind),0)
		assert_false(seen.has(u.cell))
		seen[u.cell]=true
	for cell in s.level.entries: assert_gt(R.cost(s.level,cell,"knight"),0)
func test_leader_and_entries_reachable_on_empty_board() -> void:
	var s := R.initial()
	s.units=[s.units[0]]
	var nav := R.reach(s,"thoma",200)
	assert_has(nav.costs,Vector2i(19,9))
	for p in s.level.entries: assert_has(nav.costs,p)
func test_tuned_ai_deterministic_and_commands_preserve_input() -> void:
	var s := R.initial()
	s.turn=6
	var before := s.duplicate(true)
	assert_eq(R.enemy_phase(s),R.enemy_phase(s))
	assert_eq(s,before)
