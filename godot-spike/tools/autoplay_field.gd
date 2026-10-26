extends SceneTree
const Harness = preload("res://tools/field_harness.gd")
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var out := "res://docs/evidence/spike06/after/"
	var policies: Array = Harness.POLICIES.duplicate()
	var seeds: Array = [24018]
	var variant := "default"
	var enemy_mean := 3.456164
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): out=arg.trim_prefix("--output=")
		if arg.begins_with("--seeds="): seeds=Harness.seeds_from(arg.trim_prefix("--seeds="))
		if arg.begins_with("--policies="): policies=Array(arg.trim_prefix("--policies=").split(","))
		if arg.begins_with("--variant="): variant=arg.trim_prefix("--variant=")
		if arg.begins_with("--enemy-mean="): enemy_mean=arg.trim_prefix("--enemy-mean=").to_float()
	if variant not in ["default","spike05"] or seeds.is_empty():
		push_error("Unknown variant or empty seeds")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out+"runs/"))
	var failed := false
	var index := {"seeds":seeds,"policies":policies,"variant":variant,"runs":[],"variation":"AI coordinate tie-break + same-class policy action/target tie ordering; seed24018 retains historical ordering. Fixed damage; no jitter."}
	for name in policies:
		if name not in Harness.POLICIES:
			failed=true
			continue
		for seed_value in seeds:
			var report := Harness.run(name,seed_value,variant,enemy_mean)
			var path := "runs/%s-%d.json" % [name,seed_value]
			var file := FileAccess.open(out+path,FileAccess.WRITE)
			file.store_string(JSON.stringify(report,"\t"))
			index.runs.append(path)
			print("AUTOPLAY %s seed=%d %s T%d" % [name,seed_value,report.status,report.turns_to_result])
			failed=failed or report.status=="playing" or not report.illegal_commands.is_empty()
	FileAccess.open(out+"index.json",FileAccess.WRITE).store_string(JSON.stringify(index,"\t"))
	quit(1 if failed else 0)
