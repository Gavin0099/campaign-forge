extends SceneTree
const R = preload("res://scripts/rules/field_rules.gd")
const P = preload("res://tools/field_policy.gd")
const OUT = "res://docs/evidence/spike05/"
var scene
var mode := "qa"
var failed := false
var shots: Array = []
var frame_samples: Array = []
var measuring := false
var measure_kind := "scroll"
var last_stamp := 0
var checks := {}

func _process(_delta: float) -> bool:
	if measuring:
		var now := Time.get_ticks_usec()
		if last_stamp>0: frame_samples.append({"phase":measure_kind,"ms":(now-last_stamp)/1000.0})
		last_stamp=now
	return false

func tap(code: Key) -> void:
	for pressed in [true,false]:
		var event := InputEventKey.new()
		event.keycode=code
		event.pressed=pressed
		Input.parse_input_event(event)
	await process_frame

func click(cell: Vector2i) -> void:
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.position=scene.world.get_global_transform_with_canvas()*scene.center(cell)
		event.button_index=MOUSE_BUTTON_LEFT
		event.pressed=pressed
		Input.parse_input_event(event)
	await process_frame

func snapshot_enemy() -> Dictionary:
	var s := R.initial()
	while s.turn<=2:
		for id in P.order(s):
			for i in range(2):
				var command := P.command(s,id,"road")
				if command.is_empty(): break
				s=P.resolve(s,command).state
		if s.turn==2: return s
		s=R.enemy_phase(s).state
	return {}

func performance() -> void:
	scene.camera.pan_to(scene.world_bounds().get_center())
	measuring=true
	last_stamp=0
	scene.camera.keys[KEY_D]=true
	await create_timer(1).timeout
	scene.camera.keys.clear()
	scene.camera.keys[KEY_A]=true
	await create_timer(1).timeout
	scene.camera.keys.clear()
	measuring=false
	for fast in [false,true]:
		install(snapshot_enemy())
		scene.fast_forward=fast
		scene.camera.pan_to(scene.center(Vector2i(12,9)))
		measure_kind="enemy-fast" if fast else "enemy-normal"
		last_stamp=0
		measuring=true
		await scene.end_turn()
		measuring=false
	json("performance.json",{"renderer":RenderingServer.get_video_adapter_name(),"method":"Native720p, GL Compatibility, capped60FPS; inter-process wall time incl pacing/UI/rules. No fixed FPS, movie or readbacks during samples; startup excluded.","samples":frame_samples,"enemy_phases":scene.enemy_times,"attacks":scene.attack_timings})

func contact() -> void:
	if mode=="runtime":
		if scene.impact.current_event.kind=="melee" and not checks.has("melee"):
			checks.melee=true
			await shot("field-melee-hit")
	elif mode=="intercept" and scene.impact.current_event.unit.begins_with("reinforcement"):
		checks.reinforcement_attack=true
		await shot("reinforcement-interception")
	elif mode=="sequence": await shot("ranged-contact")

func runtime() -> void:
	while scene.state.status=="playing" and scene.state.turn<=15:
		for id in P.order(scene.state):
			for i in range(2):
				if scene.state.status!="playing": break
				var command := P.command(scene.state,id,"road")
				if command.is_empty(): break
				scene.select_unit(id)
				if command.type=="wait": await scene.wait_selected()
				else:
					scene.choose(command.to if command.type=="move" else R.unit(scene.state,command.target).cell)
					if scene.pending.is_empty():
						failed=true
						return
					await scene.confirm()
		if scene.state.status!="playing": break
		await scene.end_turn()
		if scene.state.turn in [4,5]: await shot("warning" if scene.state.turn==4 else "arrival")
	await shot("lose" if scene.state.status=="lose" else "win")
	scene.telemetry.write(OUT+"runtime-battle.json")
	json("runtime-attack-timings.json",scene.attack_timings)
	checks.terminal=scene.state.status!="playing"

func sequence() -> void:
	var s := R.initial()
	s.units=[R.make_unit("thoma","ally","melee",Vector2i(10,10),"party",s.level),R.make_unit("bow-1","ally","ranged",Vector2i(10,9),"party",s.level),R.make_unit("target","enemy","knight",Vector2i(14,9),"front",s.level),R.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	install(s)
	scene.camera.pan_to(scene.center(Vector2i(10,9)))
	await click(Vector2i(10,9))
	checks.parsed_select=scene.selected_id=="bow-1"
	await create_timer(.25).timeout
	await click(Vector2i(11,9))
	checks.parsed_move_preview=scene.pending.get("type")=="move"
	await tap(KEY_ESCAPE)
	checks.parsed_cancel=scene.pending.is_empty()
	await click(Vector2i(11,9))
	await tap(KEY_ENTER)
	while scene.busy: await process_frame
	checks.parsed_move_confirm=R.unit(scene.state,"bow-1").cell==Vector2i(11,9)
	await shot("ranged-move-confirmed")
	await click(Vector2i(14,9))
	checks.parsed_attack_preview=scene.pending.get("target")=="target"
	await shot("ranged-preview")
	await tap(KEY_ENTER)
	while scene.busy: await process_frame
	checks.parsed_attack_confirm=R.unit(scene.state,"target").hp==4
	checks.timing=not scene.attack_timings.is_empty() and scene.attack_timings.back().process_seconds<=1.7
	await shot("ranged-return")
	json("sequence.json",{"checks":checks,"timings":scene.attack_timings,"context":"Scripted four-unit actual field fixture, original stats/terrain. Parsed select→move preview→Esc→move confirm→ranged attack; not a full battle."})

func sight() -> void:
	var s := R.initial()
	s.units=[R.make_unit("thoma","ally","melee",Vector2i(3,9),"party",s.level),R.make_unit("bow-1","ally","ranged",Vector2i(14,8),"party",s.level),R.make_unit("target","enemy","knight",Vector2i(16,8),"front",s.level),R.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	install(s)
	scene.select_unit("bow-1")
	await create_timer(.3).timeout
	scene.hud.hover(Vector2i(16,8))
	checks.blocked=not scene.attack_targets.has("target") and scene.hud.inspect.text.contains("阻擋")
	await shot("los-blocked")
	await tap(KEY_V)
	await shot("threat-los")
	checks.threat=scene.threat_visible and scene.threat_cells==R.threat(scene.state,"target").merged(R.threat(scene.state,"leader"))
	scene.threat_visible=false
	R.unit(s,"bow-1").cell=Vector2i(11,6)
	R.unit(s,"target").cell=Vector2i(14,6)
	install(s)
	scene.select_unit("bow-1")
	await create_timer(.3).timeout
	scene.choose(Vector2i(14,6))
	checks.cover=scene.pending.get("target")=="target" and scene.hud.notice.text.contains("傷害 1")
	await shot("cover-preview")

func interception() -> void:
	# Isolated unit-test scenario, not a full deployment trace: thoma, leader,
	# original three entry cells/kinds/warning/arrival/rest, original map/stats.
	var s := R.initial()
	s.units=[s.units[0],R.unit(s,"leader")]
	s.units[0].cell=Vector2i(18,9)
	s.turn=4
	s.warned=true
	s=R.next_turn(s).state
	s=R.enemy_phase(s).state
	install(s)
	scene.camera.pan_to(scene.center(Vector2i(20,7)))
	await scene.end_turn()
	if not checks.get("reinforcement_attack",false) and scene.state.status=="playing": await scene.end_turn()
	checks.reinforcement_attack=checks.get("reinforcement_attack",false)

func result_fixture() -> void:
	var s := R.initial()
	s.units=[R.make_unit("thoma","ally","melee",Vector2i(19,9),"party",s.level),R.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	s.units[1].hp=2
	install(s)
	scene.select_unit("thoma")
	scene.choose(Vector2i(20,9))
	await scene.confirm()
	checks.staged_win=scene.state.status=="win"
	await shot("win-staged-terminal")

func _initialize() -> void:
	call_deferred("run")

func json(name: String, value: Variant) -> void:
	var file := FileAccess.open(OUT+name,FileAccess.WRITE)
	file.store_string(JSON.stringify(value,"\t"))

func shot(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	scene.labels.refresh_layout()
	var overlaps := 0
	var labels: Array = scene.labels.items
	for i in range(labels.size()):
		for j in range(i):
			if labels[i].rect.intersects(labels[j].rect): overlaps+=1
	var image := root.get_texture().get_image()
	failed=image.save_png(OUT+name+".png")!=OK or overlaps>0 or failed
	shots.append({"name":name,"resolution":[image.get_width(),image.get_height()],"label_overlaps":overlaps,"labels":labels.duplicate(true),"suppressed":scene.labels.suppressed.duplicate(),"markers":scene.labels.markers.duplicate(true),"zoom":scene.camera.zoom.x,"turn":scene.state.turn})

func install(s: Dictionary) -> void:
	scene.state=s.duplicate(true)
	scene.selected_id="thoma"
	scene.hud.warning.clear()
	scene.hud.notice.text=""
	scene.telemetry=preload("res://scripts/levels/field_telemetry.gd").new()
	scene.telemetry.register(scene.state,"ally")
	scene.build_units()
	scene.refresh()

func qa() -> void:
	await shot("deployment")
	scene.camera.toggle_overview()
	await shot("overview")
	scene.camera.toggle_overview()
	scene.camera.pan_to(scene.center(Vector2i(19,9)))
	scene.state.warned=true
	scene.state.turn=4
	scene.refresh()
	await shot("dense-labels")
	var s := R.initial()
	R.unit(s,"thoma").cell=Vector2i(0,0)
	R.unit(s,"knight-1").cell=Vector2i(1,0)
	install(s)
	scene.select_unit("thoma")
	await create_timer(.3).timeout
	await shot("edge-safe")
	var rect: Rect2 = scene.camera.screen_actor(scene.actors.thoma.position,scene.camera.position,scene.camera.zoom.x)
	failed=failed or not scene.camera.SAFE.encloses(rect)

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
	scene.impact.contact_started.connect(contact)
	await process_frame
	await process_frame
	match mode:
		"perf": await performance()
		"runtime": await runtime()
		"sequence": await sequence()
		"sight": await sight()
		"intercept": await interception()
		"result": await result_fixture()
		"1080": await shot("deployment-1080")
		"enemy":
			install(snapshot_enemy())
			scene.camera.pan_to(scene.center(Vector2i(12,9)))
			scene.end_turn()
			await process_frame
			await shot("enemy-advancing-front")
			while scene.busy: await process_frame
		_: await qa()
	for value in checks.values(): failed=failed or not value
	json("capture-"+mode+".json",{"pass":not failed,"mode":mode,"checks":checks,"shots":shots,"human":"HUMAN_PENDING","engine":Engine.get_version_info().string,"renderer":RenderingServer.get_video_adapter_name()})
	print("SPIKE05_FIELD mode=%s pass=%s" % [mode,not failed])
	await create_timer(.4,true,false,true).timeout
	scene.queue_free()
	await process_frame
	await process_frame
	quit(1 if failed else 0)
