extends "res://addons/gut/test.gd"
const R = preload("res://scripts/rules/field_rules.gd")
const P = preload("res://tools/field_policy.gd")
func fixture() -> Dictionary:
	var s := R.initial()
	for y in range(18): s.level.rows[y]=".".repeat(24)
	s.units=[R.make_unit("thoma","ally","melee",Vector2i(7,9),"party",s.level),R.make_unit("scout","ally","mobile",Vector2i(3,9),"party",s.level),R.make_unit("target","enemy","knight",Vector2i(8,9),"front",s.level),R.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	return s
func test_finisher_threshold_and_class_and_variant_boundaries() -> void:
	var s := fixture()
	s.units[1].cell=Vector2i(7,10)
	s.units[2].cell=Vector2i(8,10)
	for hp in [6,4,3,2,1]:
		s.units[2].hp=hp
		var info := R.attack_info(s,s.units[1],s.units[2])
		assert_eq(info.damage,3 if hp<=3 else 2)
		assert_eq(info.finisher,hp<=3)
	s.level.scout_kit=false
	assert_eq(R.attack_info(s,s.units[1],s.units[2]).damage,2)
	s.level.scout_kit=true
	s.units[1].kind="melee"
	assert_eq(R.attack_info(s,s.units[1],s.units[2]).damage,2)
func test_attack_then_escape_total_budget_and_no_second_attack() -> void:
	var s := fixture()
	var before := s.duplicate(true)
	var moved := R.move(s,"scout",Vector2i(7,10))
	assert_true(moved.ok) # cost5 leaves only1, not free extra2
	var contact := R.unit(moved.state,"target")
	contact.cell=Vector2i(8,10)
	contact.hp=3
	var hit := R.attack(moved.state,"scout","target")
	assert_true(hit.ok)
	assert_eq(R.unit(hit.state,"target").hp,0)
	assert_eq(R.unit(hit.state,"scout").retreat_left,1)
	assert_false(R.attack(hit.state,"scout","leader").ok)
	assert_false(R.move(hit.state,"scout",Vector2i(5,10)).ok)
	var escaped := R.move(hit.state,"scout",Vector2i(6,10))
	assert_true(escaped.ok)
	assert_eq(R.unit(escaped.state,"scout").move_spent,6)
	assert_false(R.move(escaped.state,"scout",Vector2i(5,10)).ok)
	assert_eq(s,before)
func test_full_move_has_no_escape_and_wait_consumes_escape() -> void:
	var s := fixture()
	s.units[0].cell=Vector2i(0,0)
	s.units[2].cell=Vector2i(10,9)
	var moved := R.move(s,"scout",Vector2i(9,9))
	var hit := R.attack(moved.state,"scout","target")
	assert_true(hit.ok)
	assert_false(R.can_escape(hit.state,R.unit(hit.state,"scout")))
	s.units[1].cell=Vector2i(9,9)
	hit=R.attack(s,"scout","target")
	assert_eq(R.unit(hit.state,"scout").retreat_left,2)
	var waited := R.wait(hit.state,"scout")
	assert_true(waited.ok)
	assert_false(R.can_move(waited.state,R.unit(waited.state,"scout")))
func test_zoc_stops_entry_but_can_leave_starting_control() -> void:
	var s := fixture()
	s.units[0].cell=Vector2i(0,0)
	s.units[1].cell=Vector2i(6,8)
	s.units[2].cell=Vector2i(3,9)
	s.phase="enemy"
	var before := s.duplicate(true)
	var nav := R.reach(s,"target")
	assert_has(nav.costs,Vector2i(6,9))
	assert_false(nav.costs.has(Vector2i(7,9)),"cannot pass through controlled cell")
	var stopped := R.move(s,"target",Vector2i(6,9))
	assert_true(stopped.ok)
	assert_true(stopped.events.any(func(e):return e.type=="intercept" and e.source=="scout"))
	s.units[2].cell=Vector2i(6,9)
	assert_has(R.reach(s,"target").costs,Vector2i(3,9))
	assert_eq(before.units[1],s.units[1])
func test_ai_uses_controlled_reach_and_is_immutable() -> void:
	var s := fixture()
	s.units[1].cell=Vector2i(6,9)
	s.units[2].cell=Vector2i(3,9)
	s.units[0].cell=Vector2i(9,9)
	var before := s.duplicate(true)
	var plan := R.ai_plan(s,"target",{})
	assert_has(R.reach(s,"target").costs,plan.to)
	assert_eq(plan,R.ai_plan(s,"target",{}))
	assert_eq(s,before)
func test_preview_hover_escape_and_overlay_use_same_rules() -> void:
	var field = add_child_autofree(preload("res://scenes/levels/Field24x18.tscn").instantiate())
	await get_tree().process_frame
	var s := fixture()
	s.units[1].cell=Vector2i(7,10)
	s.units[2].cell=Vector2i(8,10)
	s.units[2].hp=3
	field.state=s
	field.build_units()
	field.select_unit("scout")
	field.choose(Vector2i(8,10))
	assert_true(field.hud.notice.text.contains("傷害 3"))
	assert_true(field.hud.inspect.text.contains("收割"))
	field.confirm()
	await field.action_finished
	assert_false(field.move_cells.is_empty())
	assert_true(field.attack_targets.is_empty())
	assert_true(field.hud.selected.text.contains("可撤離"))
	assert_has(R.zoc_cells(field.state),Vector2i(7,9))
	field.choose(Vector2i(6,10))
	assert_eq(field.pending.type,"move")
	field.cancel()
	assert_eq(R.unit(field.state,"scout").cell,Vector2i(7,10))
	await get_tree().process_frame # action_finished emitter must unwind before autofree
