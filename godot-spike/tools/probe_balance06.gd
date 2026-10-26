extends SceneTree
const H = preload("res://tools/field_harness.gd")
const D = preload("res://data/levels/field_24x18_spike05.gd")
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var out := "res://docs/evidence/spike06/w2-second/"
	DirAccess.make_dir_recursive_absolute(out)
	var original := D.build()
	var cases := {"policy-only":{},"deployment":{},"stagger":{},"eight-knights":{},"six-knights":{}}
	var deployment: Array = original.deployment.duplicate(true)
	var positions := {"thoma":Vector2i(3,10),"guard":Vector2i(4,9),"bow-1":Vector2i(3,8),"bow-2":Vector2i(3,11),"scout-1":Vector2i(2,8),"scout-2":Vector2i(2,11)}
	for row in deployment:
		if positions.has(row[0]): row[3]=positions[row[0]]
	cases.deployment={"deployment":deployment}
	var ai: Dictionary = original.ai.duplicate(true)
	ai.march_turn=6
	cases.stagger={"deployment":deployment,"ai":ai}
	var smaller := deployment.filter(func(row):return row[0] not in ["knight-4","knight-7","knight-11"])
	cases["eight-knights"]={"deployment":smaller,"ai":ai}
	var smallest := smaller.filter(func(row):return row[0] not in ["knight-6","knight-10"])
	cases["six-knights"]={"deployment":smallest,"ai":ai}
	for label in cases:
		for seed_value in [24018,1001,1007]:
			var overrides: Dictionary = cases[label].duplicate(true)
			overrides.variant="default"
			var report := H.run("road",seed_value,"spike05",3.456164,overrides)
			FileAccess.open(out+"%s-%d.json" % [label,seed_value],FileAccess.WRITE).store_string(JSON.stringify(report,"\t"))
			print("ABLATION %s seed%d %s T%d casualties%d idle%s" % [label,seed_value,report.status,report.turns_to_result,report.ally_deaths.size(),report.enemy_idle_by_group])
	quit(0)
