extends Node
## Real rendered A2 evidence. Readbacks are separate from ordinary timing runs.
const PREFIX = "res://docs/evidence/spike02-a2/"
var scene
var movie := false
var shots: Array = []
var runs: Array = []
var readback_runs: Array = []
var phases: Array = []
var started_frame := 0
var started_usec := 0
var capturing := false
var pending := 0
var failed := false
var complete := false

func key(code: Key) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = true
	Input.parse_input_event(event)
	var release := InputEventKey.new()
	release.keycode = code
	release.pressed = false
	Input.parse_input_event(release)

func shot(name: String, expected: String = "") -> void:
	pending += 1
	await get_tree().process_frame
	RenderingServer.force_draw()
	var image: Image = scene.get_viewport().get_texture().get_image()
	var record := {"file":name,"image":image,"phase":scene.phase,"hold":scene.hold_active,
		"attacker_frame":scene.players.thoma.frame_index,"target_frame":scene.players["knight-1"].frame_index,
		"width":image.get_width(),"height":image.get_height(),"process_frame":Engine.get_process_frames(),
		"debug_visible":scene.debug_visible,"help_visible":scene.hud.help_panel.visible,"forecast_visible":scene.hud.forecast_panel.visible}
	failed = failed or image.get_size()!=Vector2i(1280,720)
	if not expected.is_empty(): failed = failed or scene.phase!=expected
	if expected=="contact": failed = failed or not scene.hold_active or scene.players.thoma.frame_index!=3
	if name=="blocked-stagger.png": failed = failed or scene.players["knight-1"].frame_index!=1
	shots.append(record)
	pending -= 1
	print("CAPTURE_A2 %s phase=%s hold=%s frame=%d" % [name,scene.phase,scene.hold_active,scene.players.thoma.frame_index])

func stagger_shot() -> void:
	while scene.players["knight-1"].frame_index<1: await scene.players["knight-1"].frame_entered
	await shot("blocked-stagger.png")

func on_phase(value: String) -> void:
	phases.append({"phase":value,"frame":Engine.get_process_frames(),"wall_ms":(Time.get_ticks_usec()-started_usec)/1000.0})
	if not capturing or movie: return
	if scene.setup_index==0 and value=="contact": shot("contact.png","contact")
	if scene.setup_index==1 and value=="blocked_recoil": stagger_shot()

func begin_run() -> void:
	phases.clear()
	started_frame = Engine.get_process_frames()
	started_usec = Time.get_ticks_usec()

func record_run(readback: bool = false) -> void:
	var sync: bool = scene.contact_triggers.size()==3
	for trigger in scene.contact_triggers: sync = sync and trigger.frame==scene.contact_triggers[0].frame
	var begin: int = phases[0].frame
	var end: int = phases[-1].frame
	var record := {"setup":scene.setup_index+1,"reduced_motion":scene.reduced_motion,"wall_seconds":scene.last_elapsed,
		"strike_frame":begin,"ready_frame":end,"fixed_fps_seconds":(end-begin)/60.0 if movie else null,
		"hitstop_wall_ms":scene.last_hold_ms,"hitstop_process_ms":scene.hold_process_ms,
		"same_frame_contact":sync,"phases":phases.duplicate(true),"triggers":scene.contact_triggers.duplicate(true)}
	if readback: readback_runs.append(record)
	else: runs.append(record)
	failed = failed or not sync or scene.last_hold_ms<80 or scene.hold_process_ms<80
	failed = failed or ((end-begin)/60.0>1.7 if movie else scene.last_elapsed>1.7)

func run(root, is_movie: bool) -> void:
	scene = root
	movie = is_movie
	process_mode = Node.PROCESS_MODE_ALWAYS
	if DisplayServer.get_name()=="headless":
		push_error("Rendered A2 evidence requires a non-headless run")
		get_tree().quit(2)
		return
	if "--overview-a2" in OS.get_cmdline_user_args():
		scene.get_window().min_size = Vector2i(1920,1080)
		scene.get_window().size = Vector2i(1920,1080)
		await get_tree().create_timer(1.2).timeout
		scene.hud.arm_attack()
		await get_tree().process_frame
		await get_tree().process_frame
		await RenderingServer.frame_post_draw
		var overview: Image = scene.get_viewport().get_texture().get_image()
		var ok := overview.get_size()==Vector2i(1920,1080) and overview.save_png(PREFIX+"overview-1080.png")==OK
		print("CAPTURE_COMPLETE A2 overview=1920x1080 pass=%s" % ok)
		get_tree().quit(0 if ok else 1)
		return
	get_tree().create_timer(55,true,false,true).timeout.connect(func():
		if not complete:
			push_error("A2 capture watchdog")
			get_tree().quit(3))
	scene.phase_changed.connect(on_phase)
	if movie:
		# Record the normal post-banner state, without >1s of irrelevant pre-roll.
		scene.hud.banner_tween.kill()
		scene.hud.banner.hide()
		await get_tree().process_frame
		await get_tree().process_frame
		begin_run()
		key(KEY_R)
		await scene.attack_finished
		record_run()
		await get_tree().process_frame
		await finish()
		return
	await get_tree().create_timer(1.2).timeout
	# Measure six ordinary attacks first; there is no synchronous GPU readback here.
	for reduced in [false,true]:
		if scene.reduced_motion!=reduced:
			key(KEY_M)
			await get_tree().process_frame
		for index in range(3):
			key(KEY_1+index)
			await get_tree().process_frame
			begin_run()
			key(KEY_R)
			await scene.attack_finished
			record_run()
			await get_tree().process_frame
	key(KEY_M)
	key(KEY_1)
	await get_tree().process_frame
	failed = failed or scene.debug_visible or scene.hud.help_panel.visible or scene.hud.forecast_panel.visible
	await shot("default-view.png")
	await shot("selected-unit.png")
	# Space passes through the focused real Button, exercising arm/confirm.
	key(KEY_SPACE)
	await get_tree().process_frame
	failed = failed or not scene.hud.armed or scene.busy
	await shot("attack-forecast.png")
	capturing = true
	begin_run()
	key(KEY_SPACE)
	await scene.attack_finished
	record_run(true)
	capturing = false
	key(KEY_2)
	await get_tree().process_frame
	key(KEY_SPACE)
	await get_tree().process_frame
	await shot("forecast-blocked-unit.png")
	capturing = true
	begin_run()
	key(KEY_SPACE)
	await scene.attack_finished
	record_run(true)
	capturing = false
	key(KEY_3)
	await get_tree().process_frame
	key(KEY_SPACE)
	await get_tree().process_frame
	await shot("forecast-blocked-terrain.png")
	key(KEY_ESCAPE)
	await get_tree().process_frame
	key(KEY_H)
	await get_tree().process_frame
	failed = failed or not scene.hud.help_panel.visible
	await shot("help-overlay.png")
	key(KEY_ESCAPE)
	await get_tree().process_frame
	key(KEY_F1)
	await get_tree().process_frame
	failed = failed or not scene.debug_visible
	await shot("debug-f1.png")
	key(KEY_F1)
	await get_tree().process_frame
	await finish()

func finish() -> void:
	while pending>0: await get_tree().process_frame
	for record in shots:
		var image: Image = record.image
		failed = image.save_png(PREFIX+record.file)!=OK or failed
		record.erase("image")
	failed = failed or shots.size()!=(0 if movie else 9) or runs.size()!=(1 if movie else 6)
	var movie_path := Engine.get_write_movie_path() if movie else ""
	var output := "movie-avi-timing.json" if movie_path.ends_with(".avi") else ("movie-png-timing.json" if movie else "timing.json")
	var report := {"complete":not failed,"engine":Engine.get_version_info().string,"renderer":RenderingServer.get_video_adapter_name(),
		"timing_definition":"ordinary runs exclude GPU readback; screenshot_runs preserve perturbed wall times; movie duration uses process-frame differences at fixed 60 fps, never encoding wall time",
		"runs":runs,"screenshot_runs":readback_runs,"screenshots":shots,"movie_path":movie_path,"fixed_fps":60 if movie else 0}
	var file := FileAccess.open(PREFIX+output,FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	file.close()
	complete = true
	print("CAPTURE_COMPLETE A2 movie=%s runs=%d shots=%d pass=%s" % [movie,runs.size(),shots.size(),not failed])
	if failed: get_tree().quit(1)
	else:
		key(KEY_ESCAPE)
		print("A2_EXIT Escape dispatched")
