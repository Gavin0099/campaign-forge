extends SceneTree
## Same harness is injected into exact historical exports. No movie/readbacks.
const Meter = preload("res://tools/perf_meter07.gd")
var scene
var measured := false
var last_usec := 0
var frames: Array = []
var reports: Array = []
var tag := "current"
var output := "res://docs/evidence/spike07/perf/current.json"
var mode := "all"
var render_timers := false
var include_ai := false
func _initialize() -> void: call_deferred("run")
func _process(_delta: float) -> bool:
	if measured:
		var now := Time.get_ticks_usec()
		if last_usec:
			frames.append({"ms":(now-last_usec)/1000.0,"process_ms":Performance.get_monitor(Performance.TIME_PROCESS)*1000,"physics_ms":Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)*1000,"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),"objects":Performance.get_monitor(Performance.RENDER_TOTAL_OBJECTS_IN_FRAME),"nodes":Performance.get_monitor(Performance.OBJECT_NODE_COUNT)})
			if render_timers:
				frames[-1].render_cpu_ms=RenderingServer.call("viewport_get_measured_render_time_cpu",root.get_viewport_rid())
				frames[-1].render_gpu_ms=RenderingServer.call("viewport_get_measured_render_time_gpu",root.get_viewport_rid())
		last_usec=now
	return false
func install(s: Dictionary) -> void:
	scene.state=s.duplicate(true)
	scene.pending.clear()
	scene.busy=false
	scene.selected_id="thoma"
	scene.build_units()
	scene.refresh()
func begin() -> void:
	frames=[]
	Meter.scopes={}
	Meter.enabled=true
	last_usec=Time.get_ticks_usec()
	measured=true
func finish(label: String, repeat: int) -> void:
	measured=false
	Meter.enabled=false
	reports.append({"workload":label,"repeat":repeat,"frames":frames.duplicate(true),"scopes":Meter.scopes.duplicate(true)})
	print("PERF07 %s %s repeat%d frames%d" % [tag,label,repeat,frames.size()])
func scroll(s: Dictionary, label: String, repeat: int, disable_map: bool = false) -> void:
	install(s)
	var minimap=scene.hud.minimap
	minimap.set_process(not disable_map)
	if disable_map: minimap.hide()
	else: minimap.show()
	scene.camera.protected_ids.clear()
	await create_timer(.35).timeout
	var points: Array = []
	for cell in [Vector2i(0,0),Vector2i(23,0),Vector2i(23,17),Vector2i(0,17),Vector2i(0,0)]: points.append(scene.center(cell))
	begin()
	for segment in range(4):
		for frame in range(45):
			scene.camera.pan_to(points[segment].lerp(points[segment+1],frame/44.0))
			await process_frame
	finish(label,repeat)
	minimap.set_process(true)
	minimap.show()
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--tag="): tag=arg.trim_prefix("--tag=")
		if arg.begins_with("--out="): output=arg.trim_prefix("--out=")
		if arg.begins_with("--mode="): mode=arg.trim_prefix("--mode=")
		if arg=="--render-timers": render_timers=RenderingServer.has_method("viewport_set_measure_render_time") and RenderingServer.has_method("viewport_get_measured_render_time_gpu")
		if arg=="--include-ai": include_ai=true
	if DisplayServer.get_name()=="headless": quit(2); return
	Engine.max_fps=60
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	if render_timers: RenderingServer.call("viewport_set_measure_render_time",root.get_viewport_rid(),true)
	scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	await process_frame
	var snapshots: Dictionary = bytes_to_var(FileAccess.get_file_as_bytes("res://tools/perf_states07.bin"))
	for repeat in range(1,4):
		if mode in ["all","scroll"]:
			await scroll(snapshots.t2,"scroll-T2",repeat)
			await scroll(snapshots.wave,"scroll-wave",repeat)
		if mode=="diagnostic": await scroll(snapshots.wave,"scroll-wave-no-minimap",repeat,true)
		if mode in ["all","enemy"]:
			for fast in [false,true]:
				install(snapshots.wave)
				scene.fast_forward=fast
				scene.camera.pan_to(scene.center(Vector2i(17,9)))
				await create_timer(.35).timeout
				# Precomputed common events ensure identical animation workload even
				# across pre-kit code. Separately time each build's own pure AI.
				if include_ai: begin()
				Meter.scopes={}
				Meter.enabled=true
				var started := Time.get_ticks_usec()
				var evaluated: Dictionary = scene.Rules.enemy_phase(scene.state)
				var ai_ms := (Time.get_ticks_usec()-started)/1000.0
				var ai_scopes := Meter.scopes.duplicate(true)
				Meter.enabled=false
				if not include_ai: begin()
				else: Meter.enabled=true
				await scene.accept(evaluated if include_ai else snapshots.enemy)
				finish("enemy-2x" if fast else "enemy-normal",repeat)
				reports[-1].ai_ms=ai_ms
				reports[-1].ai_scopes=ai_scopes
				reports[-1].own_result_sha256=var_to_bytes(evaluated).hex_encode().sha256_text()
	var report := {"tag":tag,"mode":mode,"engine":Engine.get_version_info().string,"adapter":RenderingServer.get_video_adapter_name(),"backend":RenderingServer.get_current_rendering_method(),"resolution":root.size,"vsync":"disabled; max_fps60","workload_sha256":FileAccess.get_sha256("res://tools/perf_states07.bin"),"method":"Native720p, no readbacks/movie/concurrent Godot. Inclusive CPU scopes overlap; frame wall minus process is NOT GPU time. Identical precomputed event replay, pure AI measured separately.","reports":reports}
	report.render_timers=render_timers
	report.include_ai=include_ai
	FileAccess.open(output,FileAccess.WRITE).store_string(JSON.stringify(report,"\t"))
	scene.queue_free()
	await process_frame
	quit(0)
