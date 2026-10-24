extends SceneTree
## Rendered A6 capture. Timing-only runs are isolated from synchronous readbacks.
const PREFIX = "res://docs/evidence/spike02-a6/"
var scene
var render_trace: Array = []
var movie := false
var runs: Array = []
var shots: Array = []
var phases: Array = []
var failed := false
var complete := false
var desired := -1
var pending := 0
var phase_start := 0
var baseline_mode := false
var capture_size := Vector2i(1280,720)
var suffix := ""

func _initialize() -> void:
	call_deferred("run")

func key(code: Key) -> void:
	for pressed in [true,false]:
		var event := InputEventKey.new()
		event.keycode = code
		event.pressed = pressed
		Input.parse_input_event(event)

func phase_changed(value: String) -> void:
	phases.append({"phase":value,"frame":Engine.get_process_frames(),"wall_ms":(Time.get_ticks_usec()-phase_start)/1000.0})

func record_run() -> void:
	var sync: bool = scene.contact_triggers.size()==3
	for trigger in scene.contact_triggers: sync = sync and trigger.frame==scene.contact_triggers[0].frame
	var frames: int = phases[-1].frame-phases[0].frame
	var measured: float = frames/60.0 if movie else scene.last_elapsed
	failed = measured>1.7 or measured<=0 or not sync or scene.last_hold_ms<80 or scene.hold_process_ms<80 or failed
	runs.append({"setup":scene.setup_index+1,"reduced_motion":scene.reduced_motion,
		"wall_seconds":scene.last_elapsed,"fixed_fps_seconds":frames/60.0 if movie else null,
		"hitstop_wall_ms":scene.last_hold_ms,"hitstop_process_ms":scene.hold_process_ms,
		"same_frame_contact":sync,"phases":phases.duplicate(true),"triggers":scene.contact_triggers.duplicate(true),
		"input_ready":not scene.busy and not scene.action_button.disabled})

func shot(name: String, expected: int = -1) -> void:
	pending += 1
	# Read only after the entered texture/transform has reached the rendered frame.
	# force_draw inside frame_entered can still expose the previous canvas state.
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var named := name.replace(".png",suffix+".png")
	var filename := "rendered-baseline-a5/"+named if baseline_mode else named
	var row := {"file":filename,"image":image,"phase":scene.phase,"frame":scene.players.thoma.frame_index,
		"hold":scene.hold_active,"width":image.get_width(),"height":image.get_height(),"process_frame":Engine.get_process_frames()}
	failed = image.get_size()!=capture_size or failed
	if expected>=0: failed = row.frame!=expected or failed
	if name=="contact.png": failed = not scene.hold_active or scene.phase!="contact" or failed
	shots.append(row)
	pending -= 1
	print("CAPTURE_A6 %s frame=%d phase=%s hold=%s" % [name,row.frame,row.phase,row.hold])

func on_frame(index: int) -> void:
	if index!=desired: return
	var name: String = {1:"swing-raised.png",2:"swing-smear.png",4:"follow-through.png",5:"recover.png"}.get(index,"")
	if not name.is_empty(): shot(name,index)

func on_hold() -> void:
	if desired==3: shot("contact.png",3)

func begin_run() -> void:
	phases.clear()
	phase_start = Time.get_ticks_usec()

func run() -> void:
	if DisplayServer.get_name()=="headless":
		push_error("A6 capture requires a rendered 1280x720 run")
		quit(2)
		return
	movie = "--movie-a6" in OS.get_cmdline_user_args()
	if "--1080p" in OS.get_cmdline_user_args():
		capture_size = Vector2i(1920,1080)
		suffix = "-1080p"
		# Windows may clamp the startup request to the available work area.
		# Capture the actual requested viewport, never upscale a smaller readback.
		root.min_size = capture_size
		root.size = capture_size
	create_timer(55,true,false,true).timeout.connect(func():
		if not complete:
			push_error("A6 capture watchdog")
			quit(3))
	scene = load("res://scenes/Skirmish.tscn").instantiate()
	root.add_child(scene)
	scene.phase_changed.connect(phase_changed)
	scene.hitstop_started.connect(on_hold)
	RenderingServer.frame_post_draw.connect(record_render_frame)
	if movie:
		scene.hud.banner_tween.kill()
		scene.hud.banner.hide()
		await process_frame
		await process_frame
		begin_run()
		key(KEY_R)
		await scene.attack_finished
		record_run()
		await process_frame
		finish()
		return
	await create_timer(1.2).timeout
	for reduced in [false,true]:
		if scene.reduced_motion!=reduced:
			key(KEY_M)
			await process_frame
		for index in range(3):
			key(KEY_1+index)
			await process_frame
			begin_run()
			key(KEY_R)
			await scene.attack_finished
			record_run()
			await process_frame
	key(KEY_M)
	key(KEY_1)
	await process_frame
	await process_frame
	shot("idle.png",0)
	# One readback per replay avoids a readback stalling/skipping the next key pose.
	DirAccess.make_dir_recursive_absolute(PREFIX+"rendered-baseline-a5")
	for old in [false,true]:
		baseline_mode = old
		for frame in [0,1,2,3,4,5]:
			desired = frame
			key(KEY_R)
			# Parsed physical input dispatches on the next frame and rebuilds players.
			await process_frame
			if baseline_mode:
				# Capture-only texture override. Never write to live assets/manifest.
				for i in range(6):
					var im := Image.new()
					var error := im.load_png_from_buffer(FileAccess.get_file_as_bytes(PREFIX+"baseline-a5/%02d.png" % i))
					failed = error!=OK or failed
					scene.players.thoma.textures["thoma/swing/%02d.png" % i] = ImageTexture.create_from_image(im)
				scene.players.thoma.apply_frame()
			scene.players.thoma.frame_entered.connect(on_frame)
			if frame==0:
				await process_frame
				shot("swing-anticipation.png",0)
			await scene.attack_finished
			await process_frame
	desired = -1
	while pending>0: await process_frame
	finish()

func record_render_frame() -> void:
	if not movie or complete or not is_instance_valid(scene): return
	var player = scene.players.thoma
	render_trace.append({"process_frame":Engine.get_process_frames(),"phase":scene.phase,
		"index":player.frame_index,"path":player.sequence.frames[player.frame_index].path,
		"hold":scene.hold_active,"body_transform":[player.body.get_global_transform_with_canvas().x.x,
		player.body.get_global_transform_with_canvas().y.y,player.body.get_global_transform_with_canvas().origin.x,
		player.body.get_global_transform_with_canvas().origin.y]})

func finish() -> void:
	for row in shots:
		failed = row.image.save_png(PREFIX+row.file)!=OK or failed
		row.erase("image")
	failed = shots.size()!=(0 if movie else 13) or runs.size()!=(1 if movie else 6) or failed
	var output := "movie-timing.json" if movie else "timing"+suffix+".json"
	var file := FileAccess.open(PREFIX+output,FileAccess.WRITE)
	file.store_string(JSON.stringify({"complete":not failed,"engine":Engine.get_version_info().string,
		"renderer":RenderingServer.get_video_adapter_name(),"resolution":[capture_size.x,capture_size.y],"runs":runs,"screenshots":shots,
		"timing_definition":"Normal/reduced wall-time runs have no readback; screenshot replays are excluded. Movie uses process frames /60, never encoding wall time.",
		"fixed_fps":60 if movie else 0,"movie_path":Engine.get_write_movie_path() if movie else ""},"\t"))
	file.close()
	if movie:
		var trace_file := FileAccess.open(PREFIX+"render-trace.json",FileAccess.WRITE)
		trace_file.store_string(JSON.stringify(render_trace,"\t"))
		trace_file.close()
	complete = true
	print("CAPTURE_COMPLETE A6 movie=%s runs=%d shots=%d pass=%s" % [movie,runs.size(),shots.size(),not failed])
	quit(1 if failed else 0)
