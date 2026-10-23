extends RefCounted
## Real viewport evidence. Does not pause, retime, alter rules, or fake rendered pixels.

var scene
var records: Array = []
var phases: Array = []
var shots: Array = []
var images_to_save: Array = []
var sequence_start := 0
var capture_error := false
var pending := 0
var prefix := "res://docs/evidence/"
var complete := false

func key(code: Key) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = true
	Input.parse_input_event(event)
	event = InputEventKey.new()
	event.keycode = code
	event.pressed = false
	Input.parse_input_event(event)

func screenshot(file: String) -> void:
	pending += 1
	await scene.get_tree().process_frame
	# An occluded desktop window may skip frame_post_draw. Force a real GPU
	# redraw instead of hanging or accepting stale evidence on --quit-after.
	RenderingServer.force_draw()
	var image: Image = scene.get_viewport().get_texture().get_image()
	images_to_save.append({"file": file, "image": image, "phase": scene.phase, "wall_ms": (Time.get_ticks_usec() - sequence_start) / 1000.0})
	print("CAPTURE %s %dx%d buffered" % [file, image.get_width(), image.get_height()])
	pending -= 1

func on_phase(phase: String) -> void:
	phases.append({"phase": phase, "wall_ms": (Time.get_ticks_usec() - sequence_start) / 1000.0,
		"target_position": [scene.actors["knight-1"].position.x, scene.actors["knight-1"].position.y]})
	if scene.reduced_motion:
		if phase == "settled":
			screenshot("reduced-motion.png")
	elif scene.setup_index == 0:
		match phase:
			"lunge": screenshot("sequence-anticipation.png")
			"contact": capture_contact()
			"settled": screenshot("knockback-end.png")
			"ready": screenshot("sequence-recovered.png")
	elif scene.setup_index == 1 and phase == "blocked_recoil":
		screenshot("knockback-blocked-unit.png")
	elif scene.setup_index == 2 and phase == "blocked_recoil":
		screenshot("knockback-blocked.png")

func capture_contact() -> void:
	# Let the first particles appear while both actors remain in the 80ms hold.
	await scene.get_tree().create_timer(0.025, true, false, true).timeout
	await screenshot("hit-frame.png")

func run(root) -> void:
	scene = root
	if DisplayServer.get_name() == "headless":
		push_error("Capture requires a rendered run, not --headless")
		scene.get_tree().quit(2)
		return
	DirAccess.make_dir_recursive_absolute(prefix)
	scene.get_window().always_on_top = true
	scene.get_tree().create_timer(12.0, true, false, true).timeout.connect(func():
		if not complete:
			push_error("Capture watchdog: incomplete evidence")
			scene.get_tree().quit(3))
	scene.phase_changed.connect(on_phase)
	await scene.get_tree().create_timer(0.35).timeout
	# Test routes go through engine input dispatch, not direct setup mutation.
	for index in range(3):
		key(KEY_1 + index)
		await scene.get_tree().process_frame
		phases = []
		sequence_start = Time.get_ticks_usec()
		key(KEY_R)
		await scene.get_tree().process_frame
		if not scene.busy or scene.setup_index != index:
			capture_error = true
			push_error("Rendered keyboard dispatch failed")
			break
		await scene.attack_finished
		records.append({"setup": index+1, "reduced": false, "elapsed_wall_s": scene.last_elapsed, "phases": phases.duplicate(true)})
		await scene.get_tree().create_timer(0.18).timeout
	# Exercise actual CheckButton state, then the same replay input path.
	key(KEY_1)
	key(KEY_M)
	await scene.get_tree().process_frame
	phases = []
	sequence_start = Time.get_ticks_usec()
	key(KEY_SPACE)
	await scene.attack_finished
	records.append({"setup": 1, "reduced": scene.reduced_motion, "elapsed_wall_s": scene.last_elapsed, "phases": phases.duplicate(true)})
	key(KEY_G)
	await scene.get_tree().process_frame
	await screenshot("grid-diagnostic.png")
	while pending > 0:
		await scene.get_tree().process_frame
	for shot in images_to_save:
		var image: Image = shot.image
		var error: Error = image.save_png(prefix + shot.file)
		shots.append({"file": shot.file, "width": image.get_width(), "height": image.get_height(), "error": error, "phase": shot.phase, "wall_ms": shot.wall_ms})
		capture_error = capture_error or error != OK
	for record in records:
		capture_error = capture_error or record.elapsed_wall_s > 1.7
	capture_error = capture_error or records.size() != 4 or shots.size() != 8 or not scene.reduced_motion or not scene.diagnostic
	var report := {"complete": not capture_error, "captured_at": Time.get_datetime_string_from_system(true), "engine": Engine.get_version_info().string, "renderer": RenderingServer.get_video_adapter_name(), "capture": "rendered viewport PNG, forced GPU redraw, no postprocessing", "timing": "wall clock includes local hitstop and GPU image readback; PNG encoding occurs after playback", "runs": records, "screenshots": shots, "reduced_toggle": scene.reduced_motion, "grid_toggle": scene.diagnostic}
	var file := FileAccess.open(prefix + "capture-report.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t"))
	file.close()
	complete = true
	print("CAPTURE_COMPLETE runs=%d screenshots=%d pass=%s" % [records.size(), shots.size(), not capture_error])
	scene.phase_changed.disconnect(on_phase)
	scene.get_tree().quit(1 if capture_error else 0)
