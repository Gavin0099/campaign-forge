extends SceneTree
const R = preload("res://scripts/rules/field_rules.gd")
const P = preload("res://tools/field_policy.gd")
const OUT = "res://docs/evidence/spike05/"
var scene
var mode := "qa"
var failed := false
var shots: Array = []

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
	scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	await process_frame
	await qa()
	json("capture-"+mode+".json",{"pass":not failed,"mode":mode,"shots":shots,"human":"HUMAN_PENDING","engine":Engine.get_version_info().string,"renderer":RenderingServer.get_video_adapter_name()})
	print("SPIKE05_FIELD mode=%s pass=%s" % [mode,not failed])
	scene.queue_free()
	await process_frame
	await process_frame
	quit(1 if failed else 0)
