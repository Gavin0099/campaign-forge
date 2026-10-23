extends Node
## Evidence observer. Captures real rendered pixels; no pause extension, retime,
## scene reconstruction or screenshot compositing. PNG encode happens afterward.
var scene
var shots: Array = []
var runs: Array = []
var capture_runs: Array = []
var phases: Array = []
var pending := 0
var complete := false
var failed := false
var sequence_start := 0
var start_frame := 0
var game_world_seconds := 0.0
var process_seconds := 0.0
var prefix := "res://docs/evidence/spike02/"
var capture_enabled := true
var movie_mode := false
var movie_destination := ""

func _process(delta: float) -> void:
	if is_instance_valid(scene) and scene.busy and Engine.get_process_frames() > start_frame:
		process_seconds += delta
		if not scene.hold_active: game_world_seconds += delta

func key(code: Key) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = true
	Input.parse_input_event(event)
	var release := InputEventKey.new()
	release.keycode = code
	release.pressed = false
	Input.parse_input_event(release)

func shot(name: String, expected_phase: String = "", grayscale: bool = false) -> void:
	pending += 1
	await get_tree().process_frame
	RenderingServer.force_draw()
	var image: Image = scene.get_viewport().get_texture().get_image()
	var record := {"file":name,"image":image,"phase":scene.phase,"hold_active":scene.hold_active,
		"attacker_frame":scene.players.thoma.frame_index,"target_frame":scene.players["knight-1"].frame_index,
		"process_frame":Engine.get_process_frames(),"width":image.get_width(),"height":image.get_height(),
		"wall_ms":(Time.get_ticks_usec()-sequence_start)/1000.0,"grayscale_runtime_shader":grayscale}
	failed = failed or image.get_size()!=Vector2i(1280,720)
	if not expected_phase.is_empty(): failed = failed or scene.phase!=expected_phase
	if expected_phase=="contact": failed = failed or not scene.hold_active or scene.players.thoma.frame_index!=3
	shots.append(record)
	print("CAPTURE %s phase=%s hold=%s frame=%d %dx%d" % [name,scene.phase,scene.hold_active,scene.players.thoma.frame_index,image.get_width(),image.get_height()])
	pending -= 1

func recoil_shot() -> void:
	await get_tree().create_timer(0.09,false).timeout
	await shot("recoil.png")

func stagger_shot() -> void:
	while scene.players["knight-1"].frame_index<1:
		await scene.players["knight-1"].frame_entered
	await shot("blocked-unit-stagger.png" if scene.setup_index==1 else "blocked-terrain-stagger.png")

func on_phase(value: String) -> void:
	phases.append({"phase":value,"process_frame":Engine.get_process_frames(),"wall_ms":(Time.get_ticks_usec()-sequence_start)/1000.0})
	if not capture_enabled or movie_mode: return
	if scene.reduced_motion:
		if scene.setup_index==0 and value=="contact": shot("reduced-motion-contact.png","contact")
	elif scene.setup_index==0:
		match value:
			"windup": shot("anticipation.png","windup")
			"contact": shot("contact.png","contact")
			"knockback": recoil_shot()
	elif value=="blocked_recoil":
		stagger_shot()

func begin_measurement() -> void:
	sequence_start=Time.get_ticks_usec()
	start_frame=Engine.get_process_frames()
	game_world_seconds=0
	process_seconds=0
	phases=[]

func record_run(with_readback: bool = false) -> void:
	var triggers: Array = scene.contact_triggers.duplicate(true)
	var sync := triggers.size()==3
	for trigger in triggers:
		sync = sync and trigger.frame==triggers[0].frame
	var game_time: float = game_world_seconds + scene.manifest.impact.hitstop_ms / 1000.0
	var record := {"setup":scene.setup_index+1,"reduced_motion":scene.reduced_motion,
		"wall_seconds":scene.last_elapsed,"world_process_seconds_excluding_hold":game_world_seconds,
		"game_seconds_including_nominal_hitstop":game_time,"all_process_seconds":process_seconds,
		"hitstop_requested_ms":scene.manifest.impact.hitstop_ms,"hitstop_observed_wall_ms":scene.last_hold_ms,
		"hitstop_observed_process_ms":scene.hold_process_ms,
		"contact_triggers":triggers,"same_frame_contact":sync,"phases":phases.duplicate(true)}
	if with_readback:
		capture_runs.append(record)
	else:
		runs.append(record)
	failed = failed or not sync or (not movie_mode and scene.last_elapsed>1.7) or game_time>1.7 or scene.last_hold_ms<79.9 or scene.hold_process_ms<79.9
	# Real-time scheduler quantization is allowed up to one 60Hz frame + 10ms.
	if not movie_mode and not with_readback: failed = failed or scene.last_hold_ms>107

func run(root, movie: bool = false) -> void:
	scene=root
	movie_mode=movie
	if movie_mode:
		movie_destination=Engine.get_write_movie_path()
	process_mode=Node.PROCESS_MODE_ALWAYS
	if DisplayServer.get_name()=="headless":
		push_error("Spike02 screenshots require rendered mode")
		get_tree().quit(2)
		return
	DirAccess.make_dir_recursive_absolute(prefix)
	scene.get_window().always_on_top=true
	get_tree().create_timer(55,true,false,true).timeout.connect(func():
		if not complete:
			push_error("Spike02 capture watchdog: incomplete")
			get_tree().quit(3))
	scene.phase_changed.connect(on_phase)
	# Let startup/import resources settle before measuring any attack.
	if movie_mode and movie_destination.ends_with(".avi"):
		# Omit the PNG inspection pre-roll from the small, shareable AVI.
		await get_tree().process_frame
		await get_tree().process_frame
	else:
		await get_tree().create_timer(0.25).timeout
	if movie_mode:
		begin_measurement()
		key(KEY_SPACE)
		await scene.attack_finished
		record_run()
		await get_tree().process_frame
		await finish("movie-avi-timing.json" if movie_destination.ends_with(".avi") else "movie-timing.json")
		return
	# GPU readback blocks the render thread and perturbs the hold wall clock.
	# Measure ordinary playback separately, then record screenshot-run timings too.
	capture_enabled=false
	for reduced in [false,true]:
		if scene.reduced_motion!=reduced:
			key(KEY_M)
			await get_tree().process_frame
		for index in range(3):
			key(KEY_1+index)
			await get_tree().process_frame
			begin_measurement()
			key(KEY_R)
			await get_tree().process_frame
			failed = failed or not scene.busy or scene.setup_index!=index or scene.reduced_motion!=reduced
			await scene.attack_finished
			record_run()
			await get_tree().create_timer(0.12).timeout
	capture_enabled=true
	for reduced in [false,true]:
		if scene.reduced_motion!=reduced:
			key(KEY_M)
			await get_tree().process_frame
		for index in range(1 if reduced else 3):
			key(KEY_1+index)
			await get_tree().process_frame
			begin_measurement()
			key(KEY_R)
			await scene.attack_finished
			record_run(true)
			await get_tree().create_timer(0.12).timeout
	capture_enabled=false
	key(KEY_M)
	key(KEY_2)
	await get_tree().process_frame
	await shot("hud-minimal.png")
	key(KEY_F1)
	key(KEY_G)
	await get_tree().process_frame
	failed = failed or not scene.debug_visible or not scene.diagnostic
	await shot("hud-debug.png")
	key(KEY_F1)
	await get_tree().process_frame
	# Grayscale is rendered in-engine, with HUD hidden and no unit labels.
	scene.hud.hide()
	var layer := CanvasLayer.new()
	layer.layer=50
	scene.add_child(layer)
	var rect := ColorRect.new()
	layer.add_child(rect)
	rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter=Control.MOUSE_FILTER_IGNORE
	var material := ShaderMaterial.new()
	var shader := Shader.new()
	shader.code="shader_type canvas_item; uniform sampler2D screen_tex : hint_screen_texture, filter_nearest; void fragment(){ vec3 c=texture(screen_tex,SCREEN_UV).rgb; float y=dot(c,vec3(0.2126,0.7152,0.0722)); COLOR=vec4(vec3(y),1.0); }"
	material.shader=shader
	rect.material=material
	await shot("knights-grayscale.png","",true)
	layer.queue_free()
	scene.hud.show()
	await get_tree().process_frame
	# Final HUD version of both comparison contact shots; full A5 matrices remain.
	for option in ["a","b"]:
		scene.readability_option=option
		scene.select_setup(1)
		scene.play_attack()
		await scene.hitstop_started
		await shot("readability-option-%s.png" % option,"contact")
		await scene.attack_finished
		await get_tree().process_frame
	await finish("timing.json")

func finish(file_name: String) -> void:
	while pending>0: await get_tree().process_frame
	for item in shots:
		var image: Image=item.image
		var error:=image.save_png(prefix+item.file)
		failed=failed or error!=OK
		item.erase("image")
	var expected_shots:=0 if movie_mode else 11
	failed=failed or shots.size()!=expected_shots or runs.size()!=(1 if movie_mode else 6)
	var movie_frames_written := 0
	if movie_mode:
		if movie_destination.ends_with(".avi"):
			failed=failed or not FileAccess.file_exists(movie_destination)
		else:
			for name in DirAccess.get_files_at(movie_destination.get_base_dir()):
				if name.ends_with(".png"): movie_frames_written+=1
			failed=failed or movie_frames_written<40 or not FileAccess.file_exists(movie_destination.get_basename()+".wav")
	var report:={"complete":not failed,"engine":Engine.get_version_info().string,
		"renderer":RenderingServer.get_video_adapter_name(),"fixed_fps":60 if movie_mode else 0,
		"timing_definition":"runs measure rendered playback without synchronous GPU image readback; screenshot_runs retain the readback-perturbed timings separately. World process delta excludes paused frames; game total adds nominal 80ms hold. PNG encoding happens after playback. Movie wall clock is capture throughput, not playback duration.",
		"runs":runs,"screenshot_runs":capture_runs,"screenshots":shots,"movie_frames_written_before_final_frame":movie_frames_written,"movie_destination":movie_destination}
	var file:=FileAccess.open(prefix+file_name,FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	file.close()
	complete=true
	print("CAPTURE_COMPLETE spike02 movie=%s runs=%d screenshots=%d pass=%s" % [movie_mode,runs.size(),shots.size(),not failed])
	scene.phase_changed.disconnect(on_phase)
	if failed:
		get_tree().quit(1)
	else:
		print("KEYBOARD_EXIT_REQUESTED key=Escape")
		key(KEY_ESCAPE)
