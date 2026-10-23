extends SceneTree
## Capture-only observer; no gameplay/art/placement/camera parameter changes.
const PREFIX = "res://docs/evidence/spike02-a3/"
var scene
var grayscale: CanvasLayer
var shots: Array = []
var failed := false
var pending := 0
var complete := false
var gray_mode := false

func _initialize() -> void:
	call_deferred("run")

func hide_labels(node: Node) -> void:
	if node is Label: node.hide()
	for child in node.get_children(): hide_labels(child)

func shot(view: String) -> void:
	pending += 1
	hide_labels(scene.world)
	await process_frame
	hide_labels(scene.world)
	RenderingServer.force_draw()
	var image: Image = root.get_texture().get_image()
	var name := "knights-720p-setup%d-%s-%s.png" % [scene.setup_index+1,view,"gray" if gray_mode else "color"]
	var bodies: Array = []
	for id in ["knight-1","knight-2"]:
		var body: Sprite2D = scene.actors[id].get_node("Body")
		var t := body.get_global_transform_with_canvas()
		bodies.append({"id":id,"texture":body.texture.resource_path,"screen_transform":[t.x.x,t.x.y,t.y.x,t.y.y,t.origin.x,t.origin.y],"frame":scene.players[id].frame_index})
	failed = image.get_size()!=Vector2i(1280,720) or failed
	if view=="zoom": failed = not scene.busy or scene.camera.zoom.x<1.39 or failed
	shots.append({"file":name,"image":image,"setup":scene.setup_index+1,"view":view,"grayscale":gray_mode,"bodies":bodies,
		"phase":scene.phase,"thoma_frame":scene.players.thoma.frame_index,"camera_zoom":scene.camera.zoom.x,
		"hud_hidden":not scene.hud.visible,"name_role_labels_hidden":true,"capture":"rendered viewport; grayscale via screen shader"})
	pending -= 1

func on_frame(index: int) -> void:
	if index==4: shot("zoom")

func run() -> void:
	if DisplayServer.get_name()=="headless":
		push_error("A3 readability requires rendered 1280x720")
		quit(2)
		return
	create_timer(50,true,false,true).timeout.connect(func():
		if not complete:
			push_error("A3 readability watchdog")
			quit(3))
	scene = load("res://scenes/Skirmish.tscn").instantiate()
	root.add_child(scene)
	scene.hud.hide()
	grayscale = CanvasLayer.new()
	grayscale.layer = 50
	root.add_child(grayscale)
	var rect := ColorRect.new()
	grayscale.add_child(rect)
	rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var material := ShaderMaterial.new()
	var shader := Shader.new()
	shader.code = "shader_type canvas_item; uniform sampler2D screen_tex : hint_screen_texture, filter_nearest; void fragment(){ vec3 c=texture(screen_tex,SCREEN_UV).rgb; float y=dot(c,vec3(0.2126,0.7152,0.0722)); COLOR=vec4(vec3(y),1.0); }"
	material.shader = shader
	rect.material = material
	await create_timer(1.2).timeout
	for gray in [false,true]:
		gray_mode = gray
		grayscale.visible = gray
		for index in range(3):
			scene.select_setup(index)
			scene.hud.hide()
			await shot("rest")
			scene.play_attack()
			# play_attack rebuilds the fixture; subscribe to its new frame player.
			scene.players.thoma.frame_entered.connect(on_frame)
			await scene.attack_finished
			await process_frame
			while pending>0: await process_frame
	while pending>0: await process_frame
	for item in shots:
		failed = item.image.save_png(PREFIX+item.file)!=OK or failed
		item.erase("image")
	failed = shots.size()!=12 or failed
	var file := FileAccess.open(PREFIX+"readability-capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"complete":not failed,"shots":shots},"\t"))
	file.close()
	complete = true
	print("CAPTURE_COMPLETE A3 readability shots=%d pass=%s" % [shots.size(),not failed])
	quit(1 if failed else 0)
