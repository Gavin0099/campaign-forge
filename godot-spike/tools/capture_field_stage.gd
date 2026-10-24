extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var scene = load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png("res://docs/evidence/spike04/w3-deployment.png")
	print("FIELD_STAGE exit=%d" % error)
	quit(0 if error==OK else 1)
