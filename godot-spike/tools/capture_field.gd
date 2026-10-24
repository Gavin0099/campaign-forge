extends SceneTree
const Rules = preload("res://scripts/rules/field_rules.gd")
const Policy = preload("res://tools/field_policy.gd")
const OUT = "res://docs/evidence/spike04/"
var scene
var mode := "stills"
var failed := false
var shots: Array = []
var checks := {}
var contacts := {}
var frame_samples: Array = []
var measuring := false
var measure_kind := "scroll"
var last_stamp := 0
var camera_samples: Array = []

func _initialize() -> void:
	call_deferred("run")

func _process(_delta: float) -> bool:
	if measuring:
		var now := Time.get_ticks_usec()
		if last_stamp>0: frame_samples.append({"phase":measure_kind,"ms":(now-last_stamp)/1000.0})
		last_stamp=now
	return false

func json(path: String, data: Variant) -> void:
	var file := FileAccess.open(OUT+path,FileAccess.WRITE)
	if file==null:
		failed=true
		return
	file.store_string(JSON.stringify(data,"\t"))

func key(code: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode=code
	event.pressed=pressed
	Input.parse_input_event(event)

func tap(code: Key) -> void:
	key(code,true)
	key(code,false)
	await process_frame

func click_cell(cell: Vector2i) -> void:
	var point: Vector2 = scene.world.get_global_transform_with_canvas()*scene.center(cell)
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.button_index=MOUSE_BUTTON_LEFT
		event.position=point
		event.pressed=pressed
		Input.parse_input_event(event)
	await process_frame

func shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var im: Image = root.get_texture().get_image()
	failed=im.save_png(OUT+name+".png")!=OK or failed
	shots.append({"file":name+".png","resolution":[im.get_width(),im.get_height()],"turn":scene.state.turn,"phase":scene.state.phase,"camera":scene.camera.position,"zoom":scene.camera.zoom,"mode":mode})

func on_contact() -> void:
	var event: Dictionary = scene.impact.current_event
	if mode=="perf": return
	if not contacts.has("first-contact"):
		contacts["first-contact"]=true
		await shot("first-contact")
	if event.kind=="ranged" and not contacts.has("ranged-attack"):
		contacts["ranged-attack"]=true
		await shot("ranged-attack")
	elif event.kind=="melee" and not contacts.has("melee-hit"):
		contacts["melee-hit"]=true
		await shot("melee-hit")

func snapshot_before_attack() -> Dictionary:
	var s := Rules.initial()
	while s.status=="playing" and s.turn<=4:
		for id in Policy.order(s):
			for i in range(2):
				var command := Policy.command(s,id,"road")
				if command.is_empty(): break
				if command.type=="attack": return {"state":s,"command":command}
				s=Policy.resolve(s,command).state
		s=Rules.enemy_phase(s).state
	return {}

func snapshot_before_enemy() -> Dictionary:
	var s := Rules.initial()
	while s.turn<=2:
		for id in Policy.order(s):
			for i in range(2):
				var command := Policy.command(s,id,"road")
				if command.is_empty(): break
				s=Policy.resolve(s,command).state
		if s.turn==2: return s
		s=Rules.enemy_phase(s).state
	return {}

func install(s: Dictionary) -> void:
	scene.state=s.duplicate(true)
	scene.telemetry=preload("res://scripts/levels/field_telemetry.gd").new()
	scene.telemetry.register(scene.state,"ally")
	scene.build_units()
	scene.refresh()

func play_command(command: Dictionary) -> void:
	scene.select_unit(command.unit)
	if command.type=="wait":
		await scene.wait_selected()
	else:
		scene.choose(command.to if command.type=="move" else Rules.unit(scene.state,command.target).cell)
		if scene.pending.is_empty():
			failed=true
			push_error("UI did not arm valid policy command: %s" % command)
			return
		await scene.confirm()
	failed=failed or scene.busy

func sequence() -> void:
	await shot("deployment")
	var before: Vector2 = scene.camera.base_position
	key(KEY_D,true)
	for i in range(20): await process_frame
	key(KEY_D,false)
	checks.parsed_keyboard_pan=scene.camera.base_position.x>before.x
	before=scene.camera.base_position
	# Both position and relative are supplied; no inconsistent default (0,0) event.
	Input.use_accumulated_input=false
	var down := InputEventMouseButton.new()
	down.position=Vector2(640,340)
	down.button_index=MOUSE_BUTTON_MIDDLE
	down.pressed=true
	Input.parse_input_event(down)
	await process_frame
	var motion := InputEventMouseMotion.new()
	motion.position=Vector2(720,370)
	motion.relative=Vector2(80,30)
	Input.parse_input_event(motion)
	await process_frame
	down.pressed=false
	down.position=motion.position
	Input.parse_input_event(down)
	await process_frame
	checks.parsed_middle_drag=scene.camera.base_position.distance_to(before)>10
	await shot("scroll")
	await tap(KEY_O)
	checks.parsed_o_overview=scene.camera.overview
	await shot("overview")
	await tap(KEY_O)
	await tap(KEY_F)
	for i in range(16): await process_frame
	await click_cell(Vector2i(3,9))
	checks.parsed_select=scene.selected_id=="thoma"
	await click_cell(Vector2i(4,9))
	checks.parsed_move_preview=scene.pending.get("type")=="move"
	await click_cell(Vector2i(4,9))
	while scene.busy: await process_frame
	checks.parsed_move_confirm=Rules.unit(scene.state,"thoma").cell==Vector2i(4,9)
	await shot("move-confirmed")
	var setup := snapshot_before_attack()
	install(setup.state)
	scene.selected_id=setup.command.unit
	scene.camera.pan_to(scene.center(Rules.unit(scene.state,setup.command.unit).cell))
	await shot("camera-before")
	var saved: Vector2 = scene.camera.base_position
	var recorder := func():
		camera_samples.append({"frame":Engine.get_process_frames(),"base":scene.camera.base_position,"position":scene.camera.position,"offset":scene.camera.offset,"zoom":scene.camera.zoom})
	process_frame.connect(recorder)
	await click_cell(Rules.unit(scene.state,setup.command.unit).cell)
	await click_cell(Rules.unit(scene.state,setup.command.target).cell)
	checks.parsed_attack_preview=scene.pending.get("type")=="attack"
	await click_cell(Rules.unit(scene.state,setup.command.target).cell)
	while scene.busy: await process_frame
	checks.parsed_attack_confirm=Rules.unit(scene.state,setup.command.target).hp==4
	process_frame.disconnect(recorder)
	checks.attack_returns_to_saved_base=scene.camera.base_position.is_equal_approx(saved)
	checks.attack_budget_simulation=not scene.attack_timings.is_empty() and scene.attack_timings.back().process_seconds<=1.7
	await shot("camera-return")
	checks.profile_toned=is_equal_approx(scene.impact.profile.flash_mix,.8)
	for value in checks.values(): failed=failed or not value
	json("camera-sequence.json",{"checks":checks,"samples":camera_samples,"attack_timings":scene.attack_timings,"note":"Actual runtime sequence. Combat resumes the first-attack state of the deterministic road trace; not a continuous battle recording. AVI encoding/PNG readback wall time is not input latency; perf run separately measures wall time without recording."})

func full_battle() -> void:
	await shot("deployment")
	while scene.state.status=="playing" and scene.state.turn<=15:
		for id in Policy.order(scene.state):
			for i in range(2):
				if scene.state.status!="playing": break
				var command := Policy.command(scene.state,id,"road")
				if command.is_empty(): break
				await play_command(command)
		if scene.state.status!="playing": break
		if scene.state.turn==2:
			scene.end_turn()
			await process_frame
			await shot("enemy-phase")
			while scene.busy: await process_frame
		else: await scene.end_turn()
		if scene.state.turn==4:
			await create_timer(.28,true,false,true).timeout
			await shot("reinforcement-warning")
			checks.warning_one_full_turn_ahead=scene.state.warned and not scene.state.spawned and scene.state.level.reinforcement_turn-scene.state.turn>=1
		if scene.state.turn==5: await shot("reinforcement-arrival")
		if scene.state.turn==6:
			await tap(KEY_O)
			await shot("mid-battle-overview")
			await tap(KEY_O)
	await shot("win" if scene.state.status=="win" else "lose")
	checks.continuous_battle_win=scene.state.status=="win"
	checks.continuous_turn12=scene.state.turn==12
	for value in checks.values(): failed=failed or not value
	scene.telemetry.write(OUT+"runtime-battle.json")
	json("runtime-attack-timings.json",scene.attack_timings)

func performance() -> void:
	# No fixed FPS, AVI encoder or texture readbacks during this measurement.
	scene.camera.pan_to(scene.world_bounds().get_center())
	measuring=true
	last_stamp=0
	key(KEY_D,true)
	await create_timer(1.0,true,false,true).timeout
	key(KEY_D,false)
	key(KEY_A,true)
	await create_timer(1.0,true,false,true).timeout
	key(KEY_A,false)
	measuring=false
	for fast in [false,true]:
		install(snapshot_before_enemy())
		scene.fast_forward=fast
		scene.camera.pan_to(scene.center(Vector2i(12,9)))
		measure_kind="enemy-fast" if fast else "enemy-normal"
		last_stamp=0
		measuring=true
		await scene.end_turn()
		measuring=false
	json("performance.json",{"renderer":RenderingServer.get_video_adapter_name(),"method":"GL Compatibility, native720p, no fixed FPS/movie/readbacks; inter-process-frame wall times incl UI/rules, excludes startup; capped60FPS pacing is included.","samples":frame_samples,"enemy_phases":scene.enemy_times,"attacks":scene.attack_timings})

func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--mode="): mode=arg.trim_prefix("--mode=")
	if DisplayServer.get_name()=="headless":
		quit(2)
		return
	create_timer(240,true,false,true).timeout.connect(func():quit(3))
	if mode=="1080":
		root.min_size=Vector2i(1920,1080)
		root.size=Vector2i(1920,1080)
	scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	scene.impact.contact_started.connect(on_contact)
	await process_frame
	await process_frame
	match mode:
		"sequence": await sequence()
		"enemy":
			install(snapshot_before_enemy())
			scene.camera.pan_to(scene.center(Vector2i(12,9)))
			await scene.end_turn()
			json("enemy-movie.json",{"context":"Road policy immediately before turn2 enemy phase, no rule changes","duration":scene.enemy_times,"timings":scene.attack_timings})
		"perf": await performance()
		"1080": await shot("deployment-1080")
		"debug":
			await tap(KEY_F1)
			checks.parsed_debug=scene.debug_visible
			await shot("debug-overlay")
		_: await full_battle()
	for value in checks.values(): failed=failed or not value
	json("capture-"+mode+".json",{"pass":not failed,"checks":checks,"shots":shots,"engine":Engine.get_version_info().string,"renderer":RenderingServer.get_video_adapter_name(),"human":"HUMAN_PENDING","mode":mode})
	print("FIELD_CAPTURE mode=%s shots=%d checks=%s pass=%s" % [mode,shots.size(),checks,not failed])
	# Let the last placeholder thud finish before shutting down the Dummy mixer.
	await create_timer(.35,true,false,true).timeout
	scene.queue_free()
	await process_frame
	await process_frame
	quit(1 if failed else 0)
