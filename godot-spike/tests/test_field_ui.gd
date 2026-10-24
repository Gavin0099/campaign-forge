extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/levels/Field24x18.tscn")
const Rules = preload("res://scripts/rules/field_rules.gd")
var battle
func before_each() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	battle=add_child_autofree(Scene.instantiate())
	await get_tree().process_frame
func after_each() -> void:
	get_tree().paused=false
	await get_tree().process_frame

func test_minimap_round_trip_and_click_camera() -> void:
	var map = battle.hud.minimap
	for p in [Vector2.ZERO,battle.world_bounds().get_center(),battle.center(Vector2i(23,17))]:
		assert_almost_eq(map.map_to_world(map.world_to_map(p)),p,Vector2(.001,.001))
	var target: Vector2 = battle.center(Vector2i(14,9))
	var click := InputEventMouseButton.new()
	click.button_index=MOUSE_BUTTON_LEFT
	click.pressed=true
	click.position=map.world_to_map(target)
	map._gui_input(click)
	assert_almost_eq(battle.camera.base_position,battle.camera.clamp_at(target),Vector2(.001,.001))
	battle.hud.toggle_minimap()
	assert_false(map.visible)
	battle.hud.toggle_minimap()
	assert_true(map.visible)

func test_minimap_viewport_rect_matches_zoom_camera_and_offset() -> void:
	for zoom in [.8,1.0,1.2]:
		battle.camera.base_zoom=zoom
		battle.pan_to(battle.world_bounds().get_center())
		var rect: Rect2 = battle.hud.minimap.viewport_rect()
		var map = battle.hud.minimap
		assert_almost_eq(map.map_to_world(rect.position),battle.camera.position-battle.camera.VIEW/zoom/2,Vector2(.001,.001))
		assert_almost_eq(rect.size,battle.camera.VIEW/zoom*map.factor(),Vector2(.001,.001))

func test_indicators_only_outside_tactical_view_right_direction_and_safe() -> void:
	var indicators = battle.hud.indicators
	var camera = battle.camera
	assert_eq(indicators.indicator(camera.position),{})
	for direction in [Vector2.RIGHT,Vector2.LEFT,Vector2.UP,Vector2.DOWN,Vector2(1,1).normalized()]:
		var item: Dictionary = indicators.indicator(camera.position+direction*5000)
		assert_false(item.is_empty())
		assert_gt(item.direction.dot(direction),.99)
		assert_true(indicators.SAFE.has_point(item.point))
		assert_true(indicators.SAFE.encloses(item.rect))
	battle.reduced_motion=true
	var world: Vector2 = battle.center(Vector2i(17,9))
	indicators.centre_item(indicators.indicator(world))
	assert_eq(camera.base_position,camera.clamp_at(world))

func test_objective_panel_turn_limit_and_hover_show_real_values() -> void:
	battle.hud.update_state()
	assert_true(battle.hud.objective.text.contains("擊敗領袖"))
	assert_true(battle.hud.objective.text.contains("托瑪倒下"))
	assert_true(battle.hud.objective.text.contains(str(battle.state.level.turn_limit)))
	battle.state.turn=7
	battle.hud.update_state()
	assert_true(battle.hud.title.text.contains("7 / 15"))
	battle.hud.hover(Rules.unit(battle.state,"bow-1").cell)
	assert_true(battle.hud.inspect.text.contains("2–3"))

func test_warning_marker_precedes_arrival_and_tracks_announced_entries() -> void:
	var s: Dictionary = battle.state.duplicate(true)
	s.turn=3
	var warning := Rules.enemy_phase(s)
	var event: Dictionary = warning.events.filter(func(e):return e.type=="reinforcement_warning")[0]
	battle.state=warning.state
	battle.hud.on_event(event)
	battle.hud.update_state()
	assert_eq(battle.hud.warning_entries(),event.entries)
	assert_gte(event.turn-battle.state.turn,1)
	assert_true(battle.hud.notice.text.contains("第 5 回合"))
	assert_true(battle.hud.notice.text.contains("東北"))
	battle.hud.indicators.refresh_items()
	assert_true(battle.hud.indicators.targets().any(func(t):return t.id=="entry" and t.world==battle.center(event.entries[0])))
	battle.state=Rules.enemy_phase(warning.state).state
	assert_true(battle.hud.warning_entries().is_empty())

func test_win_lose_result_screens_come_from_rules_and_restart() -> void:
	for status in ["win","lose"]:
		var s: Dictionary = battle.state.duplicate(true)
		Rules.unit(s,"leader" if status=="win" else "thoma").hp=0
		var events: Array = []
		Rules.terminal(s,events)
		battle.state=s
		battle.hud.update_state()
		assert_true(battle.hud.result_panel.visible)
		assert_eq(events.back().status,status)
		assert_true(battle.hud.result_label.text.contains("勝利" if status=="win" else "敗北"))
		battle.restart()
		assert_false(battle.hud.result_panel.visible)
		assert_eq(battle.state.status,"playing")
