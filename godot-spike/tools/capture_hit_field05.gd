extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var scene = load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.state.units=[scene.Rules.make_unit("thoma","ally","melee",Vector2i(12,9),"party",scene.state.level),scene.Rules.make_unit("target","enemy","knight",Vector2i(13,9),"front",scene.state.level),scene.Rules.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",scene.state.level)]
	scene.build_units()
	scene.refresh()
	scene.camera.pan_to(scene.center(Vector2i(12,9)))
	scene.choose(Vector2i(13,9))
	scene.confirm()
	await scene.impact.contact_started
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png("res://docs/evidence/spike05/hitfeel/field-melee-hit.png")
	await scene.action_finished
	await create_timer(.4,true,false,true).timeout
	scene.queue_free()
	await process_frame
	quit(0 if error==OK else 1)
