extends RefCounted
var scene
var shots: Array = []
var pending := 0
var failed := false
const PREFIX = "res://docs/evidence/spike02-a2/"

func shot(name: String) -> void:
	pending += 1
	await scene.get_tree().process_frame
	RenderingServer.force_draw()
	var image: Image = scene.get_viewport().get_texture().get_image()
	var bodies: Array = []
	for id in scene.actors:
		var body: Sprite2D = scene.actors[id].get_node("Body")
		var t := body.get_global_transform_with_canvas()
		bodies.append({"id":id,"texture":body.texture.resource_path,"screen_transform":[t.x.x,t.x.y,t.y.x,t.y.y,t.origin.x,t.origin.y],"frame":scene.players[id].frame_index})
	shots.append({"file":name,"image":image,"bodies":bodies,"option":"a2","setup":scene.setup_index,"phase":scene.phase,"zoom":scene.camera.zoom.x})
	pending -= 1

func on_phase(phase: String) -> void:
	if phase=="contact": shot("overlap-setup%d-contact.png" % (scene.setup_index+1))

func run(root) -> void:
	scene = root
	if DisplayServer.get_name()=="headless":
		scene.get_tree().quit(2)
		return
	DirAccess.make_dir_recursive_absolute(PREFIX)
	scene.phase_changed.connect(on_phase)
	await scene.get_tree().create_timer(1.2).timeout
	for index in range(3):
		scene.select_setup(index)
		scene.phase = "ready"
		await shot("overlap-setup%d-rest.png" % (index+1))
		await scene.play_attack()
		await scene.get_tree().process_frame
	while pending>0: await scene.get_tree().process_frame
	scene.select_setup(1)
	scene.hud.hide()
	await shot("knights-default-view.png")
	# Render grayscale in-engine. This is not a postprocessed screenshot.
	var layer := CanvasLayer.new()
	layer.layer = 50
	scene.add_child(layer)
	var rect := ColorRect.new()
	layer.add_child(rect)
	rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var material := ShaderMaterial.new()
	var shader := Shader.new()
	shader.code = "shader_type canvas_item; uniform sampler2D screen_tex : hint_screen_texture, filter_nearest; void fragment(){ vec3 c=texture(screen_tex,SCREEN_UV).rgb; float y=dot(c,vec3(0.2126,0.7152,0.0722)); COLOR=vec4(vec3(y),1.0); }"
	material.shader = shader
	rect.material = material
	await shot("knights-grayscale.png")
	layer.queue_free()
	await scene.get_tree().process_frame
	# Diagnostic close framing without playing a hit: identity is not hidden by flash.
	scene.camera.zoom = Vector2.ONE*scene.manifest.camera.zoom
	scene.camera.position = scene.camera_home.lerp((scene.actors.thoma.position+scene.actors["knight-1"].position)/2.0,scene.manifest.camera.focus_weight)
	await shot("knights-zoomed.png")
	for item in shots:
		var image: Image = item.image
		failed = image.save_png(PREFIX+item.file)!=OK or image.get_size()!=Vector2i(1280,720) or failed
		item.erase("image")
	var file := FileAccess.open(PREFIX+"readability.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(shots,"\t"))
	file.close()
	failed = failed or shots.size()!=9
	print("CAPTURE_COMPLETE A2 readability shots=%d pass=%s" % [shots.size(),not failed])
	scene.get_tree().quit(1 if failed else 0)
