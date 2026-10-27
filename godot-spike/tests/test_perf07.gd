extends "res://addons/gut/test.gd"
const R = preload("res://scripts/rules/field_rules.gd")
const Old = preload("res://tests/fixtures/field_rules_preperf07.gd")
const P = preload("res://tools/field_policy.gd")
func test_call_local_indexes_equal_original_after_move_attack_and_turn() -> void:
	var states: Dictionary = bytes_to_var(FileAccess.get_file_as_bytes("res://tools/perf_states07.bin"))
	var s := P.start("road",1014)
	var samples: Array = [s,states.t2,states.wave]
	var contact := R.initial()
	contact.units=[R.make_unit("thoma","ally","melee",Vector2i(3,9),"party",contact.level),R.make_unit("foe","enemy","knight",Vector2i(4,9),"front",contact.level),R.make_unit("leader","enemy","leader",Vector2i(22,9),"leader",contact.level)]
	var attacked := R.attack(contact,"thoma","foe")
	assert_true(attacked.ok)
	assert_eq(attacked,Old.attack(contact,"thoma","foe"))
	samples.append(attacked.state)
	for id in P.order(s):
		for i in range(3):
			var command := P.command(s,id,"road")
			if command.is_empty(): break
			s=P.resolve(s,command).state
			samples.append(s)
	samples.append(R.enemy_phase(s).state)
	for state in samples:
		var before: Dictionary = state.duplicate(true)
		for u in state.units:
			if u.hp<=0: continue
			assert_eq(R.reach(state,u.id),Old.reach(state,u.id),"reach costs AND parents")
			assert_eq(R.threat(state,u.id),Old.threat(state,u.id),"fresh threat/LOS after state change")
		for kind in ["knight","ranged","mobile"]:
			assert_eq(R.distance_map(state,kind,"enemy"),Old.distance_map(state,kind,"enemy"))
		assert_eq(R.enemy_phase(state),Old.enemy_phase(state),"identical events and next state")
		assert_eq(state,before)
func test_retained_minimap_invalidates_geometry_only_and_matches_fresh() -> void:
	var scene=add_child_autofree(preload("res://scenes/levels/Field24x18.tscn").instantiate())
	await get_tree().process_frame
	var map=scene.hud.minimap
	map.ensure_geometry()
	var revision: int = map.static_revision
	var polygons: Array = map.static_layer.polygons.duplicate(true)
	for state in [R.move(scene.state,"thoma",Vector2i(4,9)).state,R.next_turn(scene.state).state]:
		scene.state=state
		scene.refresh()
		map.ensure_geometry()
		assert_eq(map.static_revision,revision,"units/turn don't invalidate terrain")
		assert_eq(map.static_layer.polygons,polygons)
	scene.state.level.rows[0]="="+scene.state.level.rows[0].substr(1)
	map.ensure_geometry()
	assert_eq(map.static_revision,revision+1)
	assert_ne(map.static_layer.polygons,polygons)
	map.size+=Vector2(20,10)
	scene.state.level.hold_point+=Vector2i.RIGHT
	map.ensure_geometry()
	assert_eq(map.static_revision,revision+2)
	var cached: Array = map.static_layer.polygons.duplicate(true)
	var goal: Vector2 = map.static_layer.goal
	map.static_key={}
	map.ensure_geometry()
	assert_eq(map.static_layer.polygons,cached,"cached equals forced fresh geometry")
	assert_eq(map.static_layer.goal,goal)
	var p: Vector2 = scene.center(Vector2i(23,17))
	assert_almost_eq(map.map_to_world(map.world_to_map(p)),p,Vector2(.001,.001))
