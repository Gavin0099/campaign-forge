extends SceneTree
const OUT = "res://../docs/proposals/big-map/"
var scene
var shots: Array = []
var failed := false
var checks: Dictionary = {}

func _initialize() -> void:
	call_deferred("run")

func key(code: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func vec(value: Vector2) -> Array:
	return [value.x,value.y]

func shot(name: String, description: String) -> void:
	scene.caption.text = description+"  /  MOCKUP"
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	failed = image.get_size()!=Vector2i(1280,720) or image.save_png(OUT+name)!=OK or failed
	shots.append({"file":name,"caption":description,"native_resolution":[image.get_width(),image.get_height()],
		"tile_width":scene.tile_width,"tile_height":scene.half_tile().y*2,"unit_reference_height":scene.tile_width*0.6,
		"camera_position":vec(scene.camera.position),"zoom":scene.camera.zoom.x,"world_bounds":vec(scene.world_bounds().size),
		"clamped":scene.camera.position==scene.clamp_position(scene.camera.position)})

func run() -> void:
	if DisplayServer.get_name()=="headless":
		quit(2)
		return
	var directory_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	if directory_error!=OK:
		push_error("Cannot create mockup output: %s" % directory_error)
		quit(2)
		return
	scene = load("res://scenes/mockups/BigMapMockup.tscn").instantiate()
	root.add_child(scene)
	scene.edge_scroll = false
	await process_frame
	# Exercise actual parsed keyboard/mouse events before staged screenshots.
	var before: Vector2 = scene.camera.position
	key(KEY_D,true)
	for i in range(10): await process_frame
	key(KEY_D,false)
	await process_frame
	checks.keyboard_pan = scene.camera.position.x>before.x
	before = scene.camera.position
	var down := InputEventMouseButton.new()
	down.button_index = MOUSE_BUTTON_MIDDLE
	down.pressed = true
	Input.parse_input_event(down)
	await process_frame
	var motion := InputEventMouseMotion.new()
	motion.relative = Vector2(120,50)
	Input.parse_input_event(motion)
	await process_frame
	down.pressed = false
	Input.parse_input_event(down)
	await process_frame
	checks.drag_pan = scene.camera.position.distance_to(before)>0
	var wheel := InputEventMouseButton.new()
	wheel.button_index = MOUSE_BUTTON_WHEEL_UP
	wheel.pressed = true
	Input.parse_input_event(wheel)
	await process_frame
	checks.wheel_zoom = is_equal_approx(scene.camera.zoom.x,1.2)
	wheel.button_index = MOUSE_BUTTON_WHEEL_DOWN
	Input.parse_input_event(wheel)
	await process_frame
	# Own-window edge pan, then restore the pointer; disable edge motion for shots.
	var pointer := root.get_mouse_position()
	DisplayServer.window_move_to_foreground()
	root.warp_mouse(Vector2(1275,360))
	scene.edge_scroll = true
	before = scene.camera.position
	for i in range(10): await process_frame
	checks.edge_pan = scene.camera.position.x>before.x
	checks.edge_window_focused = DisplayServer.window_is_focused()
	root.warp_mouse(pointer)
	scene.edge_scroll = false
	key(KEY_O,true)
	key(KEY_O,false)
	await process_frame
	checks.overview_key = scene.overview
	key(KEY_F,true)
	key(KEY_F,false)
	await process_frame
	checks.centre_key = scene.camera.position==scene.clamp_position(scene.cell_center(scene.UNIT_CELLS[0])) and not scene.overview
	scene.interactive_camera = false
	for value in checks.values(): failed = failed or not value
	scene.set_overview(true)
	await shot("overview.png","全圖總覽：32×24，並非主要操作尺度")
	scene.set_overview(false)
	scene.pan_to(scene.cell_center(Vector2i(8,10)))
	await shot("scroll-west.png","西側部署：160×94.5 px 格，人物參考高 96 px")
	scene.pan_to(scene.cell_center(Vector2i(16,10)))
	await shot("scroll-crossing.png","中段捲動畫面：道路、河流與橋皆為裝飾示意")
	scene.pan_to(scene.cell_center(Vector2i(23,14)))
	await shot("scroll-east.png","東側捲動畫面：同一張地圖的另一片視野")
	for width in [128.0,160.0,192.0]:
		scene.set_tile_width(width)
		await shot("tile-%d.png" % int(width),"格寬 %d px／人物參考高 %.1f px；同一部署格" % [int(width),width*0.6])
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"pass":not failed,"checks":checks,"screenshots":shots,
		"engine":Engine.get_version_info().string,"renderer":RenderingServer.get_video_adapter_name(),
		"scope":"Throwaway decorative camera mockup; no rules, no level, no gameplay integration."},"\t"))
	print("CAPTURE_COMPLETE bigmap shots=%d checks=%s pass=%s" % [shots.size(),checks,not failed])
	quit(1 if failed else 0)
