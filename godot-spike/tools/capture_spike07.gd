extends SceneTree
## Every post-draw frame is sampled in memory; PNG encoding happens after ready.
## Fixed-FPS times describe simulation, wall times include capture/encoding cost.
var scene
var rows: Array = []
var images: Array[Image] = []
var phases: Array = []
var recording := false
var start_frame := 0
var start_usec := 0
var origin := Vector2.ZERO
var output := "before"
var failed := false
var complete := false
var timing_only := false
var runtime_timing := false
var runs: Array = []
const PREFIX = "res://docs/evidence/spike07/hitfeel/"

func _initialize() -> void:
	call_deferred("run")

func has_property(object: Object, key: String) -> bool:
	return key in object

func vec(value: Vector2) -> Array:
	return [value.x, value.y]

func sample() -> void:
	if not recording: return
	var numbers: Array = []
	var emitters := 0
	var particle_capacity := 0
	var bursts := 0
	for node in scene.world.get_children():
		if node is Label:
			numbers.append({"scale":vec(node.scale),"position":vec(node.position),"alpha":node.modulate.a})
		if node is CPUParticles2D:
			emitters += 1
			particle_capacity += node.amount
		if node.has_meta("impact_burst"): bursts += 1
	var sfx: Array = []
	if has_property(scene,"sfx_trace"):
		for event in scene.sfx_trace:
			if event.frame == Engine.get_process_frames(): sfx.append(event)
	else:
		for event in scene.contact_triggers:
			if event.type == "sfx" and event.frame == Engine.get_process_frames(): sfx.append(event)
	rows.append({"process_frame":Engine.get_process_frames(),"strike_frame":Engine.get_process_frames()-start_frame,
		"ms_from_strike":(Engine.get_process_frames()-start_frame)*1000.0/60.0,
		"wall_ms_from_strike":(Time.get_ticks_usec()-start_usec)/1000.0,
		"phase":scene.phase,"swing_frame_index":scene.players.thoma.frame_index,
		"paused":paused,"hitstop":scene.hold_active,"camera_offset":vec(scene.camera.offset),
		"camera_zoom":vec(scene.camera.zoom),"target_flash":scene.actors["knight-1"].get_node("Body").material.get_shader_parameter("flash"),
		"target_delta":vec(scene.actors["knight-1"].position-origin),
		"recoil_delta":vec(scene.actors["knight-1"].get_meta("recoil_delta",Vector2.ZERO)),
		"damage_numbers":numbers,"live_particle_emitters":emitters,"live_particle_count_upper_bound":particle_capacity,
		"live_bursts":bursts,"sfx_triggers":sfx})
	images.append(root.get_texture().get_image())

func begin() -> void:
	phases.clear()
	start_frame = Engine.get_process_frames()
	start_usec = Time.get_ticks_usec()
	origin = scene.actors["knight-1"].position

func record_run(mode: String, setup: int) -> void:
	var sync := true
	for trigger in scene.contact_triggers: sync = sync and trigger.frame == scene.contact_triggers[0].frame
	var seconds := (Engine.get_process_frames()-start_frame)/60.0
	if runtime_timing: seconds=scene.last_elapsed
	failed = failed or seconds > 1.7 or not sync or scene.busy or scene.action_button.disabled
	runs.append({"mode":mode,"setup":setup+1,"fixed_fps_seconds":null if runtime_timing else seconds,"wall_seconds":scene.last_elapsed,
		"hitstop_wall_ms":scene.last_hold_ms,"hitstop_process_ms":scene.hold_process_ms,
		"same_frame_contact":sync,"input_ready":not scene.busy and not scene.action_button.disabled,
		"hp":scene.units[1].hp,"cell":vec(Vector2(scene.units[1].cell)),"phases":phases.duplicate(true),
		"triggers":scene.contact_triggers.duplicate(true)})

func write_json(path: String, data: Variant) -> void:
	var file := FileAccess.open(path,FileAccess.WRITE)
	if file == null:
		failed = true
		return
	file.store_string(JSON.stringify(data,"\t"))

func run() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output = arg.trim_prefix("--output=")
	runtime_timing = "--wall-timing" in OS.get_cmdline_user_args()
	timing_only = "--timing" in OS.get_cmdline_user_args() or runtime_timing
	if "--still1080" in OS.get_cmdline_user_args():
		root.min_size = Vector2i(1920,1080)
		root.size = Vector2i(1920,1080)
	create_timer(60,true,false,true).timeout.connect(func():
		if not complete: quit(3))
	scene = load("res://scenes/Skirmish.tscn").instantiate()
	root.add_child(scene)
	scene.hud.banner_tween.kill()
	scene.hud.banner.hide()
	scene.phase_changed.connect(func(value): phases.append({"phase":value,"frame":Engine.get_process_frames()}))
	await process_frame
	await process_frame
	if "--still1080" in OS.get_cmdline_user_args():
		for pressed in [true,false]:
			var key := InputEventKey.new()
			key.keycode = KEY_R
			key.pressed = pressed
			Input.parse_input_event(key)
		await scene.hitstop_started
		await RenderingServer.frame_post_draw
		var still: Image = root.get_texture().get_image()
		failed = still.get_size()!=Vector2i(1920,1080)
		await scene.attack_finished
		failed = still.save_png(PREFIX+"contact-1080.png")!=OK or failed
	elif timing_only:
		for mode in ["normal","crit","reduced"]:
			for setup in range(3):
				scene.select_setup(setup)
				scene.motion_button.button_pressed = mode == "reduced"
				if has_property(scene,"next_hit_crit"): scene.next_hit_crit = mode == "crit"
				begin()
				scene.play_attack()
				await scene.attack_finished
				record_run(mode,setup)
				await process_frame
		write_json(PREFIX+("timing-runtime.json" if runtime_timing else "timing.json"),{"runs":runs,"pass":not failed,"fixed_fps":null if runtime_timing else 60,"readbacks":0})
	else:
		DirAccess.make_dir_recursive_absolute(PREFIX+output+"/frames")
		if has_property(scene,"next_hit_crit"): scene.next_hit_crit = "--crit" in OS.get_cmdline_user_args()
		RenderingServer.frame_post_draw.connect(sample)
		begin()
		recording = true
		scene.play_attack()
		await scene.attack_finished
		record_run("crit" if "--crit" in OS.get_cmdline_user_args() else "normal",0)
		await RenderingServer.frame_post_draw
		recording = false
		var contact := -1
		for i in range(rows.size()):
			if rows[i].hitstop:
				contact = i
				break
		failed = failed or contact < 8 or images.is_empty() or images[0].get_size() != Vector2i(1280,720)
		for i in range(maxi(0,contact-8),rows.size()):
			var name := "frames/%04d.png" % rows[i].strike_frame
			failed = images[i].save_png(PREFIX+output+"/"+name) != OK or failed
			rows[i]["png"] = name
		write_json(PREFIX+output+"/timeline.json",{"frames":rows,"runs":runs,"contact_row":contact,
			"impact_profile":scene.impact_profile.resource_path if has_property(scene,"impact_profile") else "A9 pre-W2 code",
			"impact_layers":scene.impact_layers if has_property(scene,"impact_layers") else [],
			"sfx_trace":scene.sfx_trace if has_property(scene,"sfx_trace") else [],
			"contact_process_frame":rows[contact].process_frame if contact>=0 else -1,
			"fixed_fps":60,"resolution":[1280,720],"movie_path":Engine.get_write_movie_path(),
			"particle_note":"Godot CPU particles expose emitter capacity, not live particle count; upper bound is capacity of live emitters.",
			"pass":not failed})
	complete = true
	print("CAPTURE_COMPLETE spike06 output=%s runs=%d frames=%d pass=%s" % [output,runs.size(),rows.size(),not failed])
	quit(1 if failed else 0)
