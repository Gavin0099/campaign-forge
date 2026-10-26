extends RefCounted
## Offline deterministic operator; no RNG state and no game-rule mutations.
const Rules = preload("res://scripts/rules/field_rules.gd")
const Policy = preload("res://tools/field_policy.gd")
const Telemetry = preload("res://scripts/levels/field_telemetry.gd")
const SEEDS = [24018,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]
const POLICIES = ["road","flank","turtle","scout-retreat","bypass"]

static func seeds_from(value: String) -> Array:
	if value=="fixed": return SEEDS.duplicate()
	var seeds: Array = []
	if value.contains(":"):
		var ends := value.split(":")
		for n in range(int(ends[0]),int(ends[1])+1): seeds.append(n)
	else:
		for n in value.split(","): seeds.append(int(n))
	return seeds

static func run(name: String, seed_value: int, variant: String, enemy_mean: float = 3.456164) -> Dictionary:
	var s := Policy.start(name,seed_value,variant)
	var telemetry := Telemetry.new()
	telemetry.estimate_enemy_mean=enemy_mean
	telemetry.estimate_source="spike05 measured normal phase mean" if is_equal_approx(enemy_mean,3.456164) else "spike06 measured normal phase mean"
	telemetry.register(s,"ally")
	var commands: Array = []
	var illegal: Array = []
	while s.status=="playing" and s.turn<=s.level.turn_limit:
		for id in Policy.order(s):
			for action_index in range(3):
				if s.status!="playing": break
				var command: Dictionary = Policy.command(s,id,name)
				if command.is_empty(): break
				var resolved := Policy.resolve(s,command)
				if not resolved.ok:
					illegal.append(command)
					break
				commands.append({"turn":s.turn,"command":command.duplicate(true)})
				telemetry.record(s,resolved.events,resolved.state)
				s=resolved.state
		if s.status!="playing": break
		var resolved := Rules.enemy_phase(s)
		telemetry.record(s,resolved.events,resolved.state)
		s=resolved.state
	var report := telemetry.summary()
	report.merge({"policy":name,"seed":seed_value,"variant":variant,"commands":commands,"illegal_commands":illegal,
		"context":"SCRIPTED mid-battle probe at turn5, not deployment-to-result" if name=="bypass" else "Continuous deployment-to-result automated operator, not human playtest",
		"final_units":s.units,"trace_hash":JSON.stringify(report.trace).sha256_text()})
	return report
