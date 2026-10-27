extends SceneTree
const H = preload("res://tools/field_harness.gd")
const D = preload("res://data/levels/field_24x18_spike06.gd")
const P = preload("res://tools/field_policy.gd")
const R = preload("res://scripts/rules/field_rules.gd")

func trial(policy: String, seed_value: int, overrides: Dictionary) -> Dictionary:
	# Ablation only: identical rules/operator without costly idle/LOS telemetry.
	var s := P.start(policy,seed_value,"spike06",overrides)
	var deaths: Array = []
	var trace: Array = []
	var wave := false
	while s.status=="playing":
		for id in P.order(s):
			for i in range(3):
				if s.status!="playing": break
				var cmd := P.command(s,id,policy)
				if cmd.is_empty(): break
				var resolved := P.resolve(s,cmd)
				assert(resolved.ok)
				wave=observe(s,resolved.events,deaths,trace) or wave
				s=resolved.state
		if s.status!="playing": break
		var resolved := R.enemy_phase(s)
		wave=observe(s,resolved.events,deaths,trace) or wave
		s=resolved.state
	return {"policy":policy,"seed":seed_value,"status":s.status,"turns_to_result":s.turn,"bypass_win":s.status=="win" and not wave,"ally_deaths":deaths,"trace_hash":JSON.stringify(trace).sha256_text()}

func observe(s: Dictionary, events: Array, deaths: Array, trace: Array) -> bool:
	var wave := false
	for e in events:
		trace.append({"turn":s.turn,"event":e})
		if e.type=="attack" and (e.unit.begins_with("reinforcement") or e.target.begins_with("reinforcement")): wave=true
		if e.type=="damage" and e.hp_after==0:
			var u := R.unit(s,e.unit)
			if u.side=="ally": deaths.append({"id":u.id,"kind":u.kind,"turn":s.turn})
	return wave
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var label := "leader-post"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--case="): label=arg.trim_prefix("--case=")
	var overrides := {}
	match label:
		"leader-post", "post-wave-t4", "post-one", "post-one-wave-t4", "post-wave-t3", "post-one-wave-t3":
			var deployment: Array = D.DEPLOYMENT.duplicate(true)
			var post := Vector2i(21,9) if label.begins_with("post-one") else Vector2i(22,9)
			deployment[-1][3]=post
			overrides={"deployment":deployment,"hold_point":post}
			if label.ends_with("wave-t4"): overrides.reinforcement_turn=4
			if label.ends_with("wave-t3"): overrides.reinforcement_turn=3
		"fallback": overrides={"leader_wave_fallback":true}
		"wave-t4": overrides={"reinforcement_turn":4}
		"wave-t3": overrides={"reinforcement_turn":3}
		"wave-entry": overrides={"entries":[Vector2i(21,8),Vector2i(21,9),Vector2i(21,10)]}
		"fallback-wave-t4": overrides={"leader_wave_fallback":true,"reinforcement_turn":4}
		_: quit(2); return
	var out := "res://docs/evidence/spike07/ablation/"+label+"/"
	DirAccess.make_dir_recursive_absolute(out)
	var rows: Array = []
	if FileAccess.file_exists(out+"runs.json"): rows=JSON.parse_string(FileAccess.get_file_as_string(out+"runs.json"))
	for policy in H.POLICIES:
		for seed_value in H.SEEDS:
			if rows.any(func(r):return r.policy==policy and int(r.seed)==seed_value): continue
			var r := trial(policy,seed_value,overrides)
			r.erase("trace")
			r.erase("commands")
			r.erase("unit_turns")
			r.erase("deliberate_holds")
			r.erase("ranged_shots")
			rows.append(r)
			print("ABLATION %s %s %d %s T%d bypass%s deaths%d" % [label,policy,seed_value,r.status,r.turns_to_result,r.bypass_win,r.ally_deaths.size()])
		FileAccess.open(out+"runs.json",FileAccess.WRITE).store_string(JSON.stringify(rows,"\t"))
	FileAccess.open(out+"config.json",FileAccess.WRITE).store_string(JSON.stringify(overrides,"\t"))
	quit(0)
