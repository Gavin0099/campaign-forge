extends SceneTree
const Rules = preload("res://scripts/rules/field_rules.gd")
const Policy = preload("res://tools/field_policy.gd")
const Telemetry = preload("res://scripts/levels/field_telemetry.gd")
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var out := "res://docs/evidence/spike04/autoplay/"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): out=arg.trim_prefix("--output=")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out))
	var failed := false
	for name in ["road","flank","turtle"]:
		var s := Rules.initial()
		var telemetry := Telemetry.new()
		telemetry.register(s,"ally")
		var commands: Array = []
		var started := Time.get_ticks_usec()
		while s.status=="playing" and s.turn<=s.level.turn_limit:
			for id in Policy.order(s):
				for action_index in range(2):
					if s.status!="playing": break
					var command: Dictionary = Policy.command(s,id,name)
					if command.is_empty(): break
					var resolved := Policy.resolve(s,command)
					if not resolved.ok:
						failed=true
						push_error("Policy produced illegal command: %s" % command)
						break
					commands.append({"turn":s.turn,"command":command.duplicate(true)})
					telemetry.record(s,resolved.events,resolved.state)
					s=resolved.state
			if s.status!="playing": break
			var resolved := Rules.enemy_phase(s)
			telemetry.record(s,resolved.events,resolved.state)
			s=resolved.state
		var report := telemetry.summary()
		report.policy=name
		report.commands=commands
		report.seed=s.level.seed
		report.final_units=s.units
		report.headless_compute_seconds=(Time.get_ticks_usec()-started)/1000000.0
		report.player_think_seconds_per_unit=[15,25]
		report.note="Deterministic automated policy, not human playtest. Compute time is NOT enemy presentation duration."
		var file := FileAccess.open(out+name+".json",FileAccess.WRITE)
		file.store_string(JSON.stringify(report,"\t"))
		print("AUTOPLAY %s status=%s result_turn=%d contact=%d metrics=%s" % [name,s.status,s.turn,telemetry.first_contact_turn,report.archetypes])
		failed=failed or s.status=="playing"
	quit(1 if failed else 0)
