extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/levels/Field24x18.tscn")
const Rules = preload("res://scripts/rules/field_rules.gd")
var battle

func before_each() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	battle=add_child_autofree(Scene.instantiate())
	await get_tree().process_frame
	# Keep original 18-actor scene/projection acceptance; default has tuned roster.
	battle.state=Rules.initial(preload("res://data/levels/field_24x18_spike05.gd").build())
	battle.build_units()
	battle.refresh()

func after_each() -> void:
	get_tree().paused=false
	await get_tree().process_frame # Let the emitting action unwind before autofree.

func contact_setup(kind: String = "melee") -> void:
	battle.state=Rules.initial()
	battle.state.units=[Rules.make_unit("thoma","ally",kind,Vector2i(12,9),"party",battle.state.level),
		Rules.make_unit("knight-1","enemy","knight",Vector2i(13 if kind!="ranged" else 14,9),"front",battle.state.level),
		Rules.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",battle.state.level)]
	battle.build_units()
	battle.refresh()

func test_separate_scene_projection_figures_and_main_scene_unchanged() -> void:
	assert_eq(battle.state.level.size,Vector2i(24,18))
	assert_eq(battle.HALF,Vector2(80,47.25))
	assert_almost_eq(battle.players.thoma.pixels_per_frame_pixel*360,96.0,.001)
	for y in range(18):
		for x in range(24): assert_eq(battle.world_cell(battle.center(Vector2i(x,y))),Vector2i(x,y))
	assert_eq(battle.actors.size(),18)
	assert_eq(battle.props.size(),7)
	assert_eq(ProjectSettings.get_setting("application/run/main_scene"),"res://scenes/Skirmish.tscn")

func test_preview_cancel_move_and_single_attack_resolution() -> void:
	contact_setup()
	var original: Dictionary = battle.state.duplicate(true)
	battle.choose(Vector2i(12,8))
	assert_eq(battle.pending.type,"move")
	assert_eq(battle.state,original)
	battle.cancel()
	assert_true(battle.pending.is_empty())
	battle.choose(Vector2i(13,9))
	assert_eq(battle.pending.type,"attack")
	var expected := Rules.attack(battle.state,"thoma","knight-1")
	battle.confirm()
	assert_true(battle.busy)
	battle.confirm()
	battle.restart()
	await battle.action_finished
	assert_eq(battle.state,expected.state)
	assert_false(battle.busy)
	assert_lte(battle.impact.last_seconds,1.7)
	assert_eq(battle.actors["knight-1"].position,battle.center(Vector2i(14,9)))

func test_field_melee_ranged_crit_reduced_budget_and_rest() -> void:
	var normal := 0.0
	for mode in ["normal","crit","reduced","ranged"]:
		contact_setup("ranged" if mode=="ranged" else "melee")
		battle.reduced_motion=mode=="reduced"
		battle.next_crit=mode=="crit"
		battle.choose(Rules.unit(battle.state,"knight-1").cell)
		await battle.confirm()
		assert_false(battle.busy)
		assert_eq(Rules.unit(battle.state,"knight-1").hp,4)
		assert_eq(battle.players.thoma.visual_offset,Vector2.ZERO)
		assert_eq(battle.camera.offset,Vector2.ZERO)
		assert_lte(battle.impact.last_seconds,1.7)
		if mode=="normal": normal=battle.impact.last_seconds
		if mode=="reduced": assert_lte(battle.impact.last_seconds,normal)

func test_parsed_keyboard_select_cursor_wait_end_turn_and_restart() -> void:
	for code in [KEY_TAB,KEY_I]:
		for pressed in [true,false]:
			var key := InputEventKey.new()
			key.keycode=code
			key.pressed=pressed
			Input.parse_input_event(key)
		await get_tree().process_frame
	assert_eq(battle.selected_id,"guard")
	assert_eq(battle.cursor_cell,Vector2i(3,9))
	await battle.wait_selected()
	assert_true(Rules.unit(battle.state,"guard").acted)
	await battle.end_turn()
	assert_eq(battle.state.turn,2)
	battle.restart()
	assert_eq(battle.state.turn,1)
	assert_false(Rules.unit(battle.state,"guard").acted)

func test_mouse_handler_uses_event_position_for_preview_and_confirm() -> void:
	# A button event need not first warp the OS mouse. Its viewport position is
	# authoritative, including when the camera has scrolled.
	battle.camera.pan_to(battle.center(Vector2i(3,9)))
	for i in range(2):
		var click := InputEventMouseButton.new()
		click.position=battle.world.get_global_transform_with_canvas()*battle.center(Vector2i(4,9))
		click.button_index=MOUSE_BUTTON_LEFT
		click.pressed=true
		# GUT's own GUI intercepts viewport clicks in headless runs. Exercise the
		# scene handler here; capture_field's rendered sequence parses real events.
		battle._unhandled_input(click)
		await get_tree().process_frame
		if i==0:
			assert_eq(battle.pending.get("type"),"move")
			assert_eq(Rules.unit(battle.state,"thoma").cell,Vector2i(3,9))
	while battle.busy: await get_tree().process_frame
	assert_eq(Rules.unit(battle.state,"thoma").cell,Vector2i(4,9))
