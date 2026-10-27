extends SceneTree
const R = preload("res://scripts/rules/field_rules.gd")
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var rows: Array = []
	var failed := false
	for mode in ["normal","crit","reduced"]:
		var scene=load("res://scenes/levels/Field24x18.tscn").instantiate()
		root.add_child(scene)
		await process_frame
		var s := R.initial()
		s.units=[R.make_unit("thoma","ally","melee",Vector2i(3,9),"party",s.level),R.make_unit("foe","enemy","knight",Vector2i(4,9),"front",s.level),R.make_unit("leader","enemy","leader",Vector2i(22,9),"leader",s.level)]
		scene.state=s
		scene.build_units()
		scene.reduced_motion=mode=="reduced"
		scene.next_crit=mode=="crit"
		scene.refresh()
		await create_timer(.3).timeout
		await scene.accept(R.attack(scene.state,"thoma","foe"))
		var row: Dictionary = scene.attack_timings[-1].duplicate(true)
		row.mode=mode
		rows.append(row)
		print("FIELD07_TIMING ",row)
		failed=failed or row.wall_seconds>1.7 or scene.busy
		scene.queue_free()
		await process_frame
		await process_frame
	failed=failed or rows[2].wall_seconds>rows[0].wall_seconds
	FileAccess.open("res://docs/evidence/spike07/field-timing.json",FileAccess.WRITE).store_string(JSON.stringify({"pass":not failed,"readbacks":0,"runs":rows},"\t"))
	quit(1 if failed else 0)
