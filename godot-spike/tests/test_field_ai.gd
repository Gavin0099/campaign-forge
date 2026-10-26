extends "res://addons/gut/test.gd"
const R = preload("res://scripts/rules/field_rules.gd")

func board() -> Dictionary:
	# Preserve T4 timer and historical AI fixtures; tuned data tested separately.
	var s := R.initial(preload("res://data/levels/field_24x18_spike05.gd").build())
	for y in range(18): s.level.rows[y]=".".repeat(24)
	s.units=[R.make_unit("thoma","ally","melee",Vector2i(2,9),"party",s.level),
		R.make_unit("a","enemy","knight",Vector2i(12,9),"front",s.level),
		R.make_unit("b","enemy","knight",Vector2i(13,10),"rear",s.level),
		R.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	return s

func test_sight_timer_attacked_neighbour_and_latched_activation() -> void:
	var s := board()
	assert_eq(R.activation(s,s.units[1]),"")
	s.units[0].cell=Vector2i(6,9)
	assert_true(R.activation(s,s.units[1]).contains("sight"))
	s.units[0].cell=Vector2i(2,9)
	s.turn=4
	assert_true(R.activation(s,s.units[1]).contains("timer"))
	s.turn=1
	s.units[0].cell=Vector2i(11,9)
	var hit := R.attack(s,"thoma","a")
	assert_eq(hit.state.groups.front,"alert")
	assert_eq(hit.state.groups.rear,"alert")
	s=hit.state
	s.units[0].cell=Vector2i(0,0)
	assert_true(R.activation(s,s.units[1]).contains("latched"))

func test_active_advances_with_cohesion_and_never_mutates_input() -> void:
	var s := board()
	s.groups.front="alert"
	s.groups.rear="alert"
	var before := s.duplicate(true)
	var a := R.enemy_phase(s)
	assert_eq(a,R.enemy_phase(s))
	assert_eq(s,before)
	assert_lt(R.distance(R.unit(a.state,"a").cell,s.units[0].cell),10)
	assert_lte(R.distance(R.unit(a.state,"a").cell,R.unit(a.state,"b").cell),4)
	for id in ["a","b"]: assert_true(a.events.any(func(e):return e.type=="move" and e.unit==id))

func test_outnumbered_regroups_once_then_advances() -> void:
	var s := board()
	s.phase="enemy"
	s.units[0].cell=Vector2i(10,9)
	s.units[2].cell=Vector2i(18,9)
	s.units.append(R.make_unit("bow","ally","ranged",Vector2i(12,7),"party",s.level))
	var plan := R.ai_plan(s,"a",{})
	assert_eq(plan.state,"regroup")
	assert_gt(plan.to.x,12)
	s.units[1].regrouped=true
	assert_ne(R.ai_plan(s,"a",{}).state,"regroup")

func test_focus_priority_and_exposed_tie_break() -> void:
	var s := board()
	s.units.append(R.make_unit("bow","ally","ranged",Vector2i(10,9),"party",s.level))
	s.units[0].cell=Vector2i(12,11)
	s.units[0].hp=6
	assert_eq(R.focus_targets(s,"a",["thoma","bow"])[0],"bow")
	s.units[0].hp=2
	assert_eq(R.focus_targets(s,"a",["thoma","bow"])[0],"thoma")
	s.units[0].hp=6
	s.units[0].cell=Vector2i(19,9)
	s.units[1].cell=Vector2i(15,9)
	assert_eq(R.focus_targets(s,"a",["bow","thoma"])[0],"thoma")

func test_bodyguard_stays_near_leader_and_intercepts() -> void:
	var s := board()
	s.units[1].group="reserve"
	s.units[1].cell=Vector2i(19,8)
	assert_true(R.ai_plan(s,"a",{}).role_hold)
	s.units[0].cell=Vector2i(17,9)
	var plan := R.ai_plan(s,"a",{})
	assert_eq(plan.state,"bodyguard-intercept")
	assert_lte(R.distance(plan.to,s.units[3].cell),3)
	assert_lt(R.distance(plan.to,s.units[0].cell),3)

func test_leader_counters_or_steps_one_cell_back_when_surrounded_low() -> void:
	var s := board()
	s.units[0].cell=Vector2i(19,9)
	assert_eq(R.ai_plan(s,"leader",{}).state,"counter")
	s.units[3].hp=4
	s.units.append(R.make_unit("bow","ally","ranged",Vector2i(20,7),"party",s.level))
	var plan := R.ai_plan(s,"leader",{})
	assert_eq(plan.state,"step-back")
	assert_eq(R.distance(plan.to,s.units[3].cell),1)
	assert_lte(R.distance(plan.to,s.level.hold_point),2)

func test_reinforcement_bypass_intercept_engages_within_two_eligible_turns() -> void:
	var s := board()
	s.units=[s.units[0],s.units[3]]
	s.units[0].cell=Vector2i(18,9)
	s.turn=4
	s.warned=true
	s=R.next_turn(s).state
	var rest := R.enemy_phase(s)
	assert_false(rest.events.any(func(e):return e.type=="attack" and e.unit.begins_with("reinforcement")))
	s=rest.state
	var engaged := false
	for i in range(2):
		if s.status!="playing": break
		var resolved := R.enemy_phase(s)
		engaged=engaged or resolved.events.any(func(e):return e.type=="attack" and e.unit.begins_with("reinforcement"))
		s=resolved.state
	assert_true(engaged)
