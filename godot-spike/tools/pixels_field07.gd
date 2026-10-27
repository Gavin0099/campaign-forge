extends SceneTree
## Actual runtime stills of frozen-idle deployment/V/O; not mockups.
var scene
var prefix := "res://docs/evidence/spike07/pixels-after-"
func _initialize() -> void: call_deferred("run")
func shot(label: String) -> void:
	scene.labels.refresh_layout()
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(prefix+label+".png")==OK)
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--prefix="): prefix=arg.trim_prefix("--prefix=")
	scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	await process_frame
	scene.camera.pan_to(scene.center(Vector2i(3,9)))
	for player in scene.players.values(): player.show_idle(); player.set_process(false)
	await shot("deployment")
	scene.select_unit("scout-1")
	scene.threat_visible=true
	scene.refresh()
	await shot("V")
	scene.threat_visible=false
	scene.refresh()
	scene.camera.toggle_overview()
	await shot("O")
	scene.queue_free()
	await process_frame
	quit(0)
