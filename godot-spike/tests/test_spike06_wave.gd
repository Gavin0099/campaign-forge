extends "res://addons/gut/test.gd"
const R = preload("res://scripts/rules/field_rules.gd")
const H = preload("res://tools/field_harness.gd")
func test_warning_visible_a_full_turn_before_legal_rested_arrival() -> void:
	var field = add_child_autofree(preload("res://scenes/levels/Field24x18.tscn").instantiate())
	await get_tree().process_frame
	var s := R.initial(preload("res://data/levels/field_24x18_spike06.gd").build())
	s.turn=3
	var warning := R.next_turn(s)
	var event: Dictionary = warning.events.filter(func(e):return e.type=="reinforcement_warning")[0]
	assert_lt(int(event.announced_on),int(event.turn))
	field.state=warning.state
	field.hud.on_event(event)
	field.refresh()
	assert_true(field.hud.notice.visible)
	assert_true(field.hud.notice.text.contains("第 5 回合"))
	assert_true(field.hud.notice.text.contains("東側渡口"))
	assert_eq(field.hud.warning_entries(),s.level.entries)
	var arrived := R.next_turn(warning.state)
	assert_eq(arrived,R.next_turn(warning.state))
	for u in arrived.state.units:
		if u.group!="reinforcements": continue
		assert_gt(R.cost(s.level,u.cell,u.kind),0)
		assert_eq(u.born_turn,arrived.state.turn)
		assert_false(R.allowed(arrived.state,u))
func test_actual_continuous_route_wave_attacks_and_is_attacked() -> void:
	var report := H.run("road",24018,"spike06")
	assert_eq(report.status,"win")
	assert_gte(report.reinforcement_first_engage_turn,6)
	assert_gte(report.reinforcement_first_attack_turn,6)
	assert_gte(report.reinforcement_first_attacked_turn,5)
	assert_eq(report.illegal_commands,[])
