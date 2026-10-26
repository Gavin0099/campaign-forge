extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/levels/Field24x18.tscn")
var field

func before_each() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	field=add_child_autofree(Scene.instantiate())
	await get_tree().process_frame

func after_each() -> void:
	get_tree().paused=false
	await get_tree().process_frame

func test_full_actor_inside_hud_safe_rect_at_all_edges_zoom_steps_and_focus() -> void:
	var cam = field.camera
	for z in cam.STEPS:
		for cell in [Vector2i(0,0),Vector2i(23,0),Vector2i(0,17),Vector2i(23,17)]:
			cam.base_zoom=z
			field.actors.thoma.position=field.center(cell)
			field.actors["knight-1"].position=field.center(cell+Vector2i(-1 if cell.x>0 else 1,0))
			cam.follow(field.actors.thoma.position)
			cam.protect(["thoma"])
			await get_tree().create_timer(.25).timeout
			assert_true(cam.SAFE.encloses(cam.screen_actor(field.actors.thoma.position,cam.position+cam.offset,cam.zoom.x)),"follow edge %s zoom%s" % [cell,z])
			cam.protect(["thoma","knight-1"])
			cam.begin_attack((field.actors.thoma.position+field.actors["knight-1"].position)/2,field.impact.profile)
			for i in range(18):
				cam.kick(Vector2.RIGHT,field.impact.profile,true)
				cam.sync()
				for id in ["thoma","knight-1"]:
					assert_true(cam.SAFE.encloses(cam.screen_actor(field.actors[id].position,cam.position+cam.offset,cam.zoom.x)),"focus edge %s zoom%s" % [cell,z])
				assert_eq(cam.position+cam.offset,cam.clamp_at(cam.position+cam.offset))
				await get_tree().process_frame
			cam.end_attack()
			await get_tree().create_timer(.22).timeout
			cam.finish_return()

func test_distant_ranged_pair_fits_without_clipping_even_during_focus_transition() -> void:
	var cam = field.camera
	cam.base_zoom=1.2
	field.actors.thoma.position=field.center(Vector2i(20,17))
	field.actors["knight-1"].position=field.center(Vector2i(23,17))
	cam.protect(["thoma","knight-1"])
	cam.begin_attack((field.actors.thoma.position+field.actors["knight-1"].position)/2,field.impact.profile)
	for i in range(20):
		cam.sync()
		for id in ["thoma","knight-1"]: assert_true(cam.SAFE.encloses(cam.screen_actor(field.actors[id].position,cam.position+cam.offset,cam.zoom.x)))
		await get_tree().process_frame
	cam.finish_return()

func test_overview_markers_are_constant_pixel_shapes_with_hp_and_group_labels() -> void:
	field.camera.toggle_overview()
	field.labels.refresh_layout()
	assert_eq(field.labels.markers.size(),18)
	for marker in field.labels.markers: assert_gte(marker.radius*2,14.0)
	assert_true(field.labels.items.any(func(i):return i.id=="party"))
	assert_true(field.labels.items.any(func(i):return i.id=="leader"))
	assert_no_overlap()

func assert_no_overlap() -> void:
	var labels = field.labels
	for i in range(labels.items.size()):
		var a: Dictionary = labels.items[i]
		assert_true(labels.AREA.encloses(a.rect))
		for obstacle in labels.obstacles: assert_false(a.rect.intersects(obstacle),"label avoids figures/props/indicators")
		for j in range(i): assert_false(a.rect.intersects(labels.items[j].rect),"plates disjoint")

func test_dense_labels_and_reinforcement_marker_declutter() -> void:
	field.camera.pan_to(field.center(Vector2i(19,9)))
	field.state.warned=true
	field.hud.indicators.refresh_items()
	field.labels.refresh_layout()
	assert_no_overlap()
	var marker: Dictionary = field.hud.warning_marker()
	assert_eq(marker.count,3)
	assert_eq(marker.cell,field.state.level.entries[1])
	assert_lt(marker.radius,22.0)
	assert_lt(marker.alpha,.7)
	var entries: Array = field.hud.indicators.items
	for i in range(entries.size()):
		for j in range(i): assert_false(entries[i].rect.intersects(entries[j].rect))
