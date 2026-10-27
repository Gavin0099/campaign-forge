extends SceneTree
const P = preload("res://tools/field_policy.gd")
const R = preload("res://scripts/rules/field_rules.gd")
func _initialize() -> void:
	var s := P.start("flank",24018,"spike06")
	var states := {}
	while s.status=="playing":
		if s.turn==2: states.t2=s.duplicate(true)
		for id in P.order(s):
			for i in range(3):
				if s.status!="playing": break
				var cmd := P.command(s,id,"flank")
				if cmd.is_empty(): break
				s=P.resolve(s,cmd).state
		var enemy := R.enemy_phase(s)
		if enemy.events.any(func(e):return e.type=="attack" and e.unit.begins_with("reinforcement")):
			states.wave=s.duplicate(true)
			states.enemy=enemy
			break
		s=enemy.state
	assert(states.has("t2") and states.has("wave"))
	FileAccess.open("res://tools/perf_states07.bin",FileAccess.WRITE).store_buffer(var_to_bytes(states))
	print("PERF_STATES07 T2 + reached waveT%d units%d events%d" % [states.wave.turn,states.wave.units.size(),states.enemy.events.size()])
	quit(0)
