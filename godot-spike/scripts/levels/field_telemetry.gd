extends RefCounted
## Measurement only. Events supply actions/damage; never changes rules.
const Rules = preload("res://scripts/rules/field_rules.gd")
var first_contact_turn := -1
var first_contact_side := ""
var unit_turns := {}
var totals := {}
var enemy_phases: Array = []
var trace: Array = []
var final_status := "playing"
var final_turn := 1

func ensure(kind: String, side: String) -> void:
	if not totals.has(kind): totals[kind]={"side":side,"unit_turns":0,"move_steps":0,"moves":0,"attacks":0,"damage_dealt":0,"damage_taken":0,"kills":0,"idle_turns":0}

func register(s: Dictionary, side: String) -> void:
	for u in s.units:
		if u.hp<=0 or u.side!=side: continue
		var key := "%d:%s" % [s.turn,u.id]
		if unit_turns.has(key): continue
		var reachable := Rules.reach(s,u.id)
		var could_attack := false
		for p in reachable.costs:
			var hypothetical: Dictionary = u.duplicate(true)
			hypothetical.cell=p
			for target in s.units:
				if Rules.in_range(s.level,hypothetical,target): could_attack=true
		unit_turns[key]={"turn":s.turn,"id":u.id,"side":u.side,"kind":u.kind,"move_steps":0,"move_cost":0,"could_reach_target":could_attack}
		ensure(u.kind,u.side)
		totals[u.kind].unit_turns+=1
		if not could_attack: totals[u.kind].idle_turns+=1

func record(before: Dictionary, events: Array, after: Dictionary) -> void:
	var turn: int = before.turn
	var roster := {}
	for u in before.units+after.units:
		roster[u.id]=u
		ensure(u.kind,u.side)
	for e in events:
		if e.type=="phase":
			turn=int(e.turn)
			register(before if e.phase=="enemy" else after,"enemy" if e.phase=="enemy" else "ally")
		if e.type=="move":
			var kind: String = roster[e.unit].kind
			var key := "%d:%s" % [turn,e.unit]
			if unit_turns.has(key):
				unit_turns[key].move_steps+=e.path.size()-1
				unit_turns[key].move_cost+=e.cost
			totals[kind].move_steps+=e.path.size()-1
			totals[kind].moves+=1
		if e.type=="attack":
			if first_contact_turn<0:
				first_contact_turn=turn
				first_contact_side=roster[e.unit].side
			totals[roster[e.unit].kind].attacks+=1
		if e.type=="damage":
			totals[roster[e.source].kind].damage_dealt+=e.amount
			totals[roster[e.unit].kind].damage_taken+=e.amount
			if e.hp_after==0: totals[roster[e.source].kind].kills+=1
		trace.append({"turn":turn,"event":e.duplicate(true)})
	final_status=after.status
	final_turn=after.turn

func summary() -> Dictionary:
	var archetypes := totals.duplicate(true)
	for kind in archetypes:
		archetypes[kind].average_move_per_unit_turn=float(archetypes[kind].move_steps)/maxi(1,archetypes[kind].unit_turns)
	return {"first_contact_turn":first_contact_turn,"first_contact_side":first_contact_side,
		"unit_turns":unit_turns.values(),"archetypes":archetypes,"enemy_phase_seconds":enemy_phases.duplicate(true),
		"turns_to_result":final_turn,"status":final_status,"trace":trace.duplicate(true),
		"definitions":{"idle_turns":"No enemy in attack range from any cost-legal destination at phase start; may still move toward contact.",
		"average_move":"Actual traversed cells / living unit phases, including zero-move turns; weighted costs recorded separately."}}

func write(path: String) -> Error:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path.get_base_dir()))
	var file := FileAccess.open(path,FileAccess.WRITE)
	if file==null: return FileAccess.get_open_error()
	file.store_string(JSON.stringify(summary(),"\t"))
	return OK
