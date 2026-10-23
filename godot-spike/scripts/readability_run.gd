extends RefCounted
var scene
var shots: Array = []
var pending := 0
var failed := false
var prefix := "res://docs/evidence/spike02/"

func shot(name: String) -> void:
	pending += 1
	await scene.get_tree().process_frame
	RenderingServer.force_draw()
	var image: Image = scene.get_viewport().get_texture().get_image()
	var bodies: Array = []
	for id in scene.actors:
		var body: Sprite2D = scene.actors[id].get_node("Body")
		bodies.append({"id":id, "texture":body.texture.resource_path, "origin":[body.global_position.x,body.global_position.y], "scale":[body.global_scale.x,body.global_scale.y], "frame":scene.players[id].frame_index})
	shots.append({"file":name,"image":image,"bodies":bodies,"option":scene.readability_option,"setup":scene.setup_index,"phase":scene.phase,"zoom":scene.camera.zoom.x})
	pending -= 1

func on_phase(phase: String) -> void:
	if phase == "contact": shot("readability-%s-setup%d-contact.png" % [scene.readability_option,scene.setup_index+1])

func run(root) -> void:
	scene = root
	if DisplayServer.get_name() == "headless":
		scene.get_tree().quit(2)
		return
	DirAccess.make_dir_recursive_absolute(prefix)
	scene.get_window().always_on_top = true
	scene.phase_changed.connect(on_phase)
	await scene.get_tree().create_timer(0.4).timeout
	for option in ["a","b"]:
		scene.readability_option = option
		for index in range(3):
			scene.select_setup(index)
			await shot("readability-%s-setup%d-rest.png" % [option,index+1])
			await scene.play_attack()
			await scene.get_tree().create_timer(0.05).timeout
	while pending > 0: await scene.get_tree().process_frame
	for item in shots:
		var image: Image = item.image
		var error := image.save_png(prefix+item.file)
		failed = failed or error != OK or image.get_size() != Vector2i(1280,720)
		item.erase("image")
	var report := FileAccess.open(prefix+"readability.json",FileAccess.WRITE)
	report.store_string(JSON.stringify(shots,"\t"))
	report.close()
	failed = failed or shots.size()!=12
	print("CAPTURE_COMPLETE readability shots=%d pass=%s" % [shots.size(),not failed])
	scene.get_tree().quit(1 if failed else 0)
