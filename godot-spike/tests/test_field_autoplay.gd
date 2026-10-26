extends "res://addons/gut/test.gd"
const Rules = preload("res://scripts/rules/field_rules.gd")
const Policy = preload("res://tools/field_policy.gd")
const Telemetry = preload("res://scripts/levels/field_telemetry.gd")

func run_policy(name: String) -> Dictionary:
	# Historical spike05 policy/result pins retain exact old deployment and operator.
	var s := Policy.start(name,24018,"spike05")
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
	assert_between(int(report.turns_to_result),2,15)
	assert_between(int(report.first_contact_turn),2,3)
	assert_gt(int(report.archetypes.melee.attacks),0)
	assert_gt(int(report.archetypes.ranged.attacks),0)
	assert_gt(int(report.archetypes.mobile.attacks),0)
	assert_eq(int(report.archetypes.leader.damage_taken),10)
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

func test_terminal_before_later_enemy_does_not_inflate_true_idle() -> void:
	var s := Rules.initial()
	s.units=[Rules.make_unit("thoma","ally","melee",Vector2i(3,9),"party",s.level),Rules.make_unit("knight","enemy","knight",Vector2i(4,9),"front",s.level),Rules.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	s.units[0].hp=2
	var metrics := Telemetry.new()
	metrics.register(s,"ally")
	var resolved := Rules.enemy_phase(s)
	metrics.record(s,resolved.events,resolved.state)
	var report := metrics.summary()
	assert_eq(report.status,"lose")
	assert_eq(report.enemy_idle_by_group.leader,0)
	assert_eq(report.ally_deaths,[{"id":"thoma","kind":"melee","turn":1}])
	var leader_rows: Array = report.unit_turns.filter(func(row):return row.id=="leader")
	assert_false(leader_rows[0].observed)

func test_after_traces_have_no_silent_active_idle_and_wave_bypass_is_contested() -> void:
	for name in ["road","flank","turtle","bypass","scout-retreat"]:
		var report: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://docs/evidence/spike05/autoplay/"+name+".json"))
		for row in report.unit_turns:
			if row.side!="enemy" or not row.eligible or not row.observed or row.move_steps>0 or row.attacks>0 or row.role_reason!="": continue
			var intents: Array = report.trace.filter(func(r):return r.turn==row.turn and r.event.type=="intent" and r.event.unit==row.id)
			assert_true(intents.all(func(r):return r.event.state=="guard"),"only inactive guards may silently wait")
		if name=="bypass": assert_between(int(report.reinforcement_first_engage_turn),6,8)
