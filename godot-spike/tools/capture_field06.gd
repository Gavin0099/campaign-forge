extends SceneTree
## Automated operator of the real scene. Snapshot movies explicitly labelled.
const R = preload("res://scripts/rules/field_rules.gd")
const P = preload("res://tools/field_policy.gd")
const OUT = "res://docs/evidence/spike06/"
var scene
var mode := "qa"
var failed := false
var shots: Array = []
var checks := {}
var samples: Array = []
var measuring := false
var sample_phase := "scroll"
var last_usec := 0

func _initialize() -> void: call_deferred("run")
func _process(_delta: float) -> bool:
	if measuring:
		var now := Time.get_ticks_usec()
		if last_usec>0: samples.append({"phase":sample_phase,"ms":(now-last_usec)/1000.0})
		last_usec=now
	return false
func json(name: String, value: Variant) -> void:
	FileAccess.open(OUT+name,FileAccess.WRITE).store_string(JSON.stringify(value,"\t"))
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
func shot(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	scene.labels.refresh_layout()
	var overlaps := 0
	for i in range(scene.labels.items.size()):
		for j in range(i):
			if scene.labels.items[i].rect.intersects(scene.labels.items[j].rect): overlaps+=1
	var im := root.get_texture().get_image()
	failed=im.save_png(OUT+name+".png")!=OK or overlaps>0 or failed
	shots.append({"name":name,"resolution":[im.get_width(),im.get_height()],"turn":scene.state.turn,"overlaps":overlaps,"labels":scene.labels.items.duplicate(true),"suppressed":scene.labels.suppressed.duplicate()})
func install(s: Dictionary) -> void:
	scene.state=s.duplicate(true)
	scene.pending.clear()
	scene.selected_id="thoma"
	scene.hud.warning.clear()
	scene.telemetry=preload("res://scripts/levels/field_telemetry.gd").new()
	scene.telemetry.register(scene.state,"ally")
	scene.build_units()
	scene.refresh()
func contact() -> void:
	var e: Dictionary = scene.impact.current_event
	if mode in ["runtime","enemy"] and e.unit.begins_with("reinforcement") and not checks.get("wave_hit",false):
		checks.wave_hit=true
		await shot("reinforcement-engaging" if mode=="runtime" else "enemy-wave-contact")
	if mode in ["runtime","scout"] and e.kind=="mobile" and e.get("finisher",false) and not checks.get("scout_hit",false):
		checks.scout_hit=true
		await shot("scout-finisher-hit" if mode=="scout" else "route-scout-finisher")

func snapshot(kind: String) -> Dictionary:
	var s := P.start("flank")
	while s.status=="playing":
		for id in P.order(s):
			var before_unit: Dictionary = s.duplicate(true)
			var commands: Array = []
			for i in range(3):
				if s.status!="playing": break
				var command := P.command(s,id,"flank")
				if command.is_empty(): break
				commands.append(command)
				if kind=="scout" and command.type=="attack" and R.unit(s,id).kind=="mobile" and commands[0].type=="move":
					var info := R.attack_info(s,R.unit(s,id),R.unit(s,command.target))
					var hit := P.resolve(s,command)
					if info.finisher and R.unit(hit.state,command.target).hp==0 and R.can_escape(hit.state,R.unit(hit.state,id)):
						commands.append(P.command(hit.state,id,"flank"))
						return {"state":before_unit,"commands":commands,"unit":id,"context":"Reachable continuous flank seed24018 snapshot, before scout flank move; not a continuous movie"}
				s=P.resolve(s,command).state
		if s.status!="playing": break
		var enemy := R.enemy_phase(s)
		if kind=="enemy" and enemy.events.any(func(e):return e.type=="attack" and e.unit.begins_with("reinforcement")):
			return {"state":s,"context":"Reachable continuous flank seed24018 snapshot before wave enemy phase; not a continuous movie"}
		s=enemy.state
	return {}

func runtime() -> void:
	var policy := "road" if mode=="lose" else "flank"
	install(P.start(policy,1001 if mode=="lose" else 24018))
	if mode!="measure": await shot("lose-deployment" if mode=="lose" else "deployment")
	while scene.state.status=="playing":
		for id in P.order(scene.state):
			for i in range(3):
				if scene.state.status!="playing": break
				var command := P.command(scene.state,id,policy)
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
		if mode=="runtime" and scene.state.turn in [4,5,7]: await shot({4:"warning",5:"arrival",7:"route-midbattle"}[scene.state.turn])
	checks.terminal=scene.state.status==("lose" if mode=="lose" else "win")
	if mode!="measure": await shot("lose" if mode=="lose" else "win-continuous")
	scene.telemetry.write(OUT+"runtime-"+mode+".json")
	json("attacks-"+mode+".json",scene.attack_timings)

func scout() -> void:
	var snap := snapshot("scout")
	if snap.is_empty():
		failed=true
		return
	install(snap.state)
	json("snapshot-scout.json",snap)
	scene.select_unit(snap.unit)
	await create_timer(.25).timeout
	await click(R.unit(scene.state,snap.unit).cell)
	await tap(KEY_V)
	var commands: Array = snap.commands
	await click(commands[0].to)
	checks.move_preview=scene.pending.get("type")=="move"
	await shot("scout-flank-preview")
	await tap(KEY_ESCAPE)
	checks.cancel=scene.pending.is_empty()
	await click(commands[0].to)
	await tap(KEY_ENTER)
	while scene.busy: await process_frame
	checks.flank=R.unit(scene.state,snap.unit).cell==commands[0].to
	await shot("scout-zoc-preview")
	await click(R.unit(scene.state,commands[1].target).cell)
	checks.finisher_preview=scene.hud.notice.text.contains("收割")
	await tap(KEY_ENTER)
	while scene.busy: await process_frame
	checks.finished=R.unit(scene.state,commands[1].target).hp==0
	checks.escape_available=not scene.move_cells.is_empty()
	await shot("scout-retreat-preview")
	var escape := P.command(scene.state,snap.unit,"flank")
	checks.escape_move=escape.get("type")=="move"
	if escape.type=="move":
		await click(escape.to)
		await tap(KEY_ENTER)
		while scene.busy: await process_frame
	checks.budget=R.unit(scene.state,snap.unit).get("move_spent",0)<=6 and not R.can_move(scene.state,R.unit(scene.state,snap.unit))
	await shot("scout-retreated")
	json("scout-sequence.json",{"checks":checks,"timings":scene.attack_timings,"context":snap.context})

func performance() -> void:
	scene.camera.pan_to(scene.world_bounds().get_center())
	measuring=true
	last_usec=0
	scene.camera.keys[KEY_D]=true
	await create_timer(2).timeout
	scene.camera.keys.clear()
	measuring=false
	var snap := snapshot("enemy")
	for fast in [false,true]:
		install(snap.state)
		scene.fast_forward=fast
		scene.camera.pan_to(scene.center(Vector2i(17,9)))
		sample_phase="enemy-fast" if fast else "enemy-normal"
		last_usec=0
		measuring=true
		await scene.end_turn()
		measuring=false
	json("performance.json",{"renderer":RenderingServer.get_video_adapter_name(),"samples":samples,"phases":scene.enemy_times,"method":"Native720p GL Compatibility max60FPS, no fixed clock/movie/readbacks or concurrent Godot. Wall frame intervals incl UI/rules/pacing. Wave-engaging reached phase; spike05 sampled T2 so workloads differ."})

func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--mode="): mode=arg.trim_prefix("--mode=")
	if DisplayServer.get_name()=="headless":
		quit(2)
		return
	if mode=="1080":
		root.min_size=Vector2i(1920,1080)
		root.size=Vector2i(1920,1080)
	scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	scene.impact.contact_started.connect(contact)
	await process_frame
	await process_frame
	match mode:
		"runtime","measure","lose": await runtime()
		"scout": await scout()
		"perf": await performance()
		"enemy":
			var snap := snapshot("enemy")
			if snap.is_empty(): failed=true
			else:
				install(snap.state)
				json("snapshot-enemy.json",snap)
				scene.camera.pan_to(scene.center(Vector2i(17,9)))
				await scene.end_turn()
				checks.wave_hit=checks.get("wave_hit",false)
		"1080": await shot("deployment-1080")
		_:
			await shot("deployment")
			scene.camera.toggle_overview()
			await shot("overview")
			scene.camera.toggle_overview()
			scene.select_unit("scout-1")
			await tap(KEY_V)
			checks.legend=scene.hud.threat_legend.visible
			await shot("threat-legend")
	for value in checks.values(): failed=failed or not value
	json("capture-"+mode+".json",{"pass":not failed,"mode":mode,"checks":checks,"shots":shots,"engine":Engine.get_version_info().string,"human":"HUMAN_PENDING"})
	print("SPIKE06_FIELD mode=%s pass=%s" % [mode,not failed])
	await create_timer(.4,true,false,true).timeout
	scene.queue_free()
	await process_frame
	await process_frame
	quit(1 if failed else 0)
