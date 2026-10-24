extends "res://addons/gut/test.gd"
## The brief permits one isolated smoke test; no real level/rules touched.
func test_mockup_loads_and_clamps_at_all_sizes_and_zooms() -> void:
	var scene = add_child_autofree(load("res://scenes/mockups/BigMapMockup.tscn").instantiate())
	scene.interactive_camera = false
	await get_tree().process_frame
	assert_eq(scene.COLS,32)
	assert_eq(scene.ROWS,24)
	assert_eq(scene.unit_root.get_child_count(),12)
	for width in [128.0,160.0,192.0]:
		scene.set_tile_width(width)
		for zoom in [0.8,1.0,1.5]:
			scene.camera.zoom = Vector2.ONE*zoom
			var bounds: Rect2 = scene.world_bounds()
			var half: Vector2 = scene.get_viewport_rect().size/scene.camera.zoom/2
			scene.pan_to(Vector2(-99999,-99999))
			assert_eq(scene.camera.position,bounds.position+half)
			scene.pan_to(Vector2(99999,99999))
			assert_eq(scene.camera.position,bounds.end-half)
			scene.pan_to(bounds.get_center())
			assert_eq(scene.camera.position,bounds.get_center())
		scene.set_overview(true)
		scene.pan_to(Vector2(-99999,99999))
		assert_eq(scene.camera.position,scene.world_bounds().get_center())
	assert_eq(ProjectSettings.get_setting("application/run/main_scene"),"res://scenes/Skirmish.tscn")
