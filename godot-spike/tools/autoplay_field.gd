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
	var index_name := "index.json"
	var resume := false
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): out=arg.trim_prefix("--output=")
		if arg.begins_with("--seeds="): seeds=Harness.seeds_from(arg.trim_prefix("--seeds="))
		if arg.begins_with("--policies="): policies=Array(arg.trim_prefix("--policies=").split(","))
		if arg.begins_with("--variant="): variant=arg.trim_prefix("--variant=")
		if arg.begins_with("--enemy-mean="): enemy_mean=arg.trim_prefix("--enemy-mean=").to_float()
		if arg.begins_with("--index-name="): index_name=arg.trim_prefix("--index-name=")
		if arg=="--resume": resume=true
	if variant not in ["default","spike05","spike06"] or seeds.is_empty():
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
			var path := "runs/%s-%d.json" % [name,seed_value]
			var report: Dictionary
			if resume and FileAccess.file_exists(out+path):
				var parser := JSON.new()
				if parser.parse(FileAccess.get_file_as_string(out+path))==OK and parser.data is Dictionary:
					report=parser.data
					assert(report.policy==name and int(report.seed)==seed_value and report.variant==variant)
				else:
					print("RESUME recompute interrupted incomplete file: "+path)
					report=Harness.run(name,seed_value,variant,enemy_mean)
			else: report=Harness.run(name,seed_value,variant,enemy_mean)
			var file := FileAccess.open(out+path,FileAccess.WRITE)
			file.store_string(JSON.stringify(report,"\t"))
			index.runs.append(path)
			print("AUTOPLAY %s seed=%d %s T%d" % [name,seed_value,report.status,report.turns_to_result])
			failed=failed or report.status=="playing" or not report.illegal_commands.is_empty()
	FileAccess.open(out+index_name,FileAccess.WRITE).store_string(JSON.stringify(index,"\t"))
	quit(1 if failed else 0)
