extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/levels/Field24x18.tscn")
var battle
var cam

func before_each() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	battle=add_child_autofree(Scene.instantiate())
	cam=battle.camera
	await get_tree().process_frame

func after_each() -> void:
	get_tree().paused=false
	await get_tree().process_frame

func assert_clamped() -> void:
	assert_almost_eq(cam.position+cam.offset,cam.clamp_at(cam.position+cam.offset),Vector2(.001,.001))

func test_clamps_all_four_corners_each_zoom_and_shake() -> void:
	for step in cam.STEPS:
		cam.base_zoom=step
		for p in [Vector2(-99999,-99999),Vector2(99999,-99999),Vector2(-99999,99999),Vector2(99999,99999)]:
			cam.pan_to(p)
			assert_clamped()
			var half: Vector2 = cam.VIEW/step/2
			var bounds: Rect2 = battle.world_bounds()
			assert_between(cam.base_position.x,bounds.position.x+half.x-.001,bounds.end.x-half.x+.001)
			assert_between(cam.base_position.y,bounds.position.y+half.y-.001,bounds.end.y-half.y+.001)
			for direction in [Vector2.LEFT,Vector2.UP,Vector2.RIGHT,Vector2.DOWN]:
				cam.kick(direction,battle.impact.profile,true)
				assert_clamped()

func test_parsed_wasd_arrows_pan_expected_zoom_scaled_distance() -> void:
	cam.set_process(false)
	cam.pan_to(battle.world_bounds().get_center())
	for step in cam.STEPS:
		cam.base_zoom=step
		for code in [KEY_D,KEY_RIGHT,KEY_A,KEY_LEFT,KEY_W,KEY_UP,KEY_S,KEY_DOWN]:
			var before: Vector2 = cam.base_position
			var key := InputEventKey.new()
			key.keycode=code
			key.pressed=true
			Input.parse_input_event(key)
			await get_tree().process_frame
			cam._process(.1)
			key.pressed=false
			Input.parse_input_event(key)
			await get_tree().process_frame
			var direction: Vector2 = Vector2.RIGHT if code in [KEY_D,KEY_RIGHT] else (Vector2.LEFT if code in [KEY_A,KEY_LEFT] else (Vector2.UP if code in [KEY_W,KEY_UP] else Vector2.DOWN))
			assert_almost_eq(cam.base_position,before+direction*cam.pan_speed*.1/step,Vector2(.001,.001))

func test_middle_drag_and_wheel_cursor_anchor() -> void:
	cam.pan_to(battle.world_bounds().get_center())
	var before: Vector2 = cam.base_position
	var down := InputEventMouseButton.new()
	down.button_index=MOUSE_BUTTON_MIDDLE
	down.pressed=true
	cam._input(down)
	var motion := InputEventMouseMotion.new()
	motion.relative=Vector2(110,40)
	cam._input(motion)
	down.pressed=false
	cam._input(down)
	assert_almost_eq(cam.base_position,before-Vector2(110,40),Vector2(.001,.001))
	var cursor := Vector2(820,310)
	var world: Vector2 = cam.screen_to_world(cursor)
	cam.wheel(1,cursor)
	assert_almost_eq(cam.zoom.x,1.2,.00001)
	assert_almost_eq(cam.screen_to_world(cursor),world,Vector2(.001,.001))

func test_o_overview_fits_and_restores_exact_previous_position_and_zoom() -> void:
	cam.base_zoom=.8
	cam.pan_to(battle.center(Vector2i(12,9)))
	var saved: Vector2 = cam.base_position
	var key := InputEventKey.new()
	key.keycode=KEY_O
	key.pressed=true
	Input.parse_input_event(key)
	await get_tree().process_frame
	assert_true(cam.overview)
	var bounds: Rect2 = battle.world_bounds()
	assert_lte(bounds.size.x*cam.zoom.x,1180.001)
	assert_lte(bounds.size.y*cam.zoom.x,430.001)
	Input.parse_input_event(key)
	await get_tree().process_frame
	assert_false(cam.overview)
	assert_eq(cam.base_position,saved)
	assert_eq(cam.base_zoom,.8)

func test_attack_returns_to_pre_attack_scroll_position() -> void:
	cam.pan_to(battle.center(Vector2i(11,9)))
	var saved: Vector2 = cam.base_position
	cam.begin_attack(battle.center(Vector2i(14,9)),battle.impact.profile)
	await get_tree().create_timer(.26).timeout
	assert_ne(cam.position,saved)
	cam.kick(Vector2.RIGHT,battle.impact.profile,false)
	assert_clamped()
	cam.end_attack()
	await get_tree().create_timer(.22).timeout
	assert_eq(cam.base_position,saved)
	assert_eq(cam.position,saved)
	assert_eq(cam.offset,Vector2.ZERO)
	assert_eq(cam.zoom,Vector2.ONE)

func test_reduced_motion_snaps_follow_and_suppresses_shake_zoom() -> void:
	battle.reduced_motion=true
	cam.follow(battle.center(Vector2i(16,9)))
	assert_eq(cam.position,cam.clamp_at(battle.center(Vector2i(16,9))))
	var before: Vector2 = cam.position
	cam.begin_attack(battle.center(Vector2i(18,9)),battle.impact.profile)
	cam.kick(Vector2.RIGHT,battle.impact.profile,true)
	assert_eq(cam.position,before)
	assert_eq(cam.zoom,Vector2.ONE)
	assert_eq(cam.offset,Vector2.ZERO)
	cam.end_attack()
	assert_eq(cam.position,before)
	assert_false(cam.edge_scroll,"optional edge scroll defaults OFF")
