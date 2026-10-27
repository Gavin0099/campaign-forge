extends SceneTree
const Meter = preload("res://tools/perf_meter07.gd")
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	var states: Dictionary = bytes_to_var(FileAccess.get_file_as_bytes("res://tools/perf_states07.bin"))
	var results: Array = []
	for s in [states.t2,states.wave]:
		for repeat in range(3):
			scene.state=s.duplicate(true)
			scene.build_units()
			scene.selected_id="scout-1"
			for threat in [false,true]:
				Meter.scopes={}
				Meter.enabled=true
				scene.threat_visible=threat
				var started := Time.get_ticks_usec()
				scene.refresh()
				var cpu := Time.get_ticks_usec()-started
				await process_frame
				await process_frame
				Meter.enabled=false
				results.append({"turn":s.turn,"repeat":repeat,"V":threat,"refresh_ms":cpu/1000.0,"scopes":Meter.scopes.duplicate(true)})
	# Synthetic legal-budget preview, explicitly not a reached route.
	var scout: Dictionary = scene.Rules.unit(scene.state,"scout-1")
	scout.hp=maxi(1,scout.hp)
	scout.acted=true
	scout.moved=true
	scout.move_spent=4
	scout.retreat_left=2
	scene.threat_visible=false
	var started := Time.get_ticks_usec()
	scene.refresh()
	var retreat_ms := (Time.get_ticks_usec()-started)/1000.0
	FileAccess.open(OS.get_cmdline_user_args()[0],FileAccess.WRITE).store_string(JSON.stringify({"previews":results,"retreat_preview_ms":retreat_ms,"retreat_context":"synthetic <=2cost legal-budget preview","note":"All expensive reach/threat scopes occur on refresh/action, not per scroll frame; no per-frame AI. LOS inside ranged threat/attack_info; legend in HUD.update_state; ZoC inside ground V draw."},"\t"))
	scene.queue_free()
	await process_frame
	await process_frame
	quit(0)
