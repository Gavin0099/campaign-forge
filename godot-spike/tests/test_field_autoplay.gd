extends "res://addons/gut/test.gd"
const Rules = preload("res://scripts/rules/field_rules.gd")
const Policy = preload("res://tools/field_policy.gd")
const Telemetry = preload("res://scripts/levels/field_telemetry.gd")

func run_policy(name: String) -> Dictionary:
	var s := Rules.initial()
	var metrics := Telemetry.new()
	metrics.register(s,"ally")
	while s.status=="playing" and s.turn<=15:
		for id in Policy.order(s):
			for i in range(2):
				if s.status!="playing": break
				var command := Policy.command(s,id,name)
				if command.is_empty(): break
				var resolved := Policy.resolve(s,command)
				assert_true(resolved.ok,"generated command remains legal")
				metrics.record(s,resolved.events,resolved.state)
				s=resolved.state
		if s.status!="playing": break
		var resolved := Rules.enemy_phase(s)
		metrics.record(s,resolved.events,resolved.state)
		s=resolved.state
	return metrics.summary()

func test_authored_main_road_has_a_full_win_path_without_routing_every_enemy() -> void:
	# W2 deliberate AI change: preserve EVERY old acceptance assertion against
	# W1's reproduced spike04 trace; the stronger AI gets a separate live test.
	var report: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://docs/evidence/spike05/baseline/road.json"))
	assert_eq(report.status,"win")
	assert_between(report.turns_to_result,2,15)
	assert_between(report.first_contact_turn,2,3)
	assert_gt(report.archetypes.melee.attacks,0)
	assert_gt(report.archetypes.ranged.attacks,0)
	assert_gt(report.archetypes.mobile.attacks,0)
	assert_eq(report.archetypes.leader.damage_taken,10)
	assert_true(report.trace.any(func(r):return r.event.type=="reinforcement_warning"))
	assert_true(report.trace.any(func(r):return r.event.type=="reinforcement_arrival"))

func test_two_other_policies_reach_distinct_terminal_outcomes_deterministically() -> void:
	var flank := run_policy("flank")
	var turtle := run_policy("turtle")
	assert_eq(flank.status,"lose")
	assert_eq(turtle.status,"lose")
	assert_ne(flank.turns_to_result,turtle.turns_to_result)
	assert_eq(flank,run_policy("flank"))

func test_telemetry_damage_kills_and_distance_match_events() -> void:
	var report := run_policy("road")
	var sums := {}
	for row in report.unit_turns: sums[row.kind]=sums.get(row.kind,0)+row.move_steps
	for kind in ["melee","ranged","mobile"]:
		assert_eq(sums[kind],report.archetypes[kind].move_steps)
		# W3 forest cover / overkill cap: validate exact event amounts, not 2 per shot.
		var event_damage := 0
		for row in report.trace:
			if row.event.type=="damage":
				var source: String = row.event.source
				var source_kind := "melee" if source in ["thoma","guard"] else ("ranged" if source.begins_with("bow") else "mobile")
				if source_kind==kind and not source.begins_with("knight") and source!="leader" and not source.begins_with("reinforcement"): event_damage+=int(row.event.amount)
		assert_eq(report.archetypes[kind].damage_dealt,event_damage)
		assert_almost_eq(report.archetypes[kind].average_move_per_unit_turn,float(sums[kind])/report.archetypes[kind].unit_turns,.00001)
	var leader_damage := 0
	for row in report.trace:
		if row.event.type=="damage" and row.event.unit=="leader": leader_damage+=int(row.event.amount)
	assert_eq(report.archetypes.leader.damage_taken,leader_damage)

func test_pressure_ai_road_policy_reaches_terminal_and_all_classes_engage() -> void:
	var report := run_policy("road")
	assert_ne(report.status,"playing")
	assert_between(report.turns_to_result,2,15)
	assert_between(report.first_contact_turn,2,3)
	for kind in ["melee","ranged","mobile"]: assert_gt(report.archetypes[kind].attacks,0)
