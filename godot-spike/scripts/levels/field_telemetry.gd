extends RefCounted
## Measurement only. Events supply actions/damage; never changes rules.
const Rules = preload("res://scripts/rules/field_rules.gd")
const Sight = preload("res://scripts/rules/field_sight.gd")
var deaths: Array = []
var ranged_shots: Array = []
var reinforcement_first_engage := -1
var reinforcement_first_attack := -1
var reinforcement_first_attacked := -1
var los_opportunities := 0
var finishing_kills := {"melee":0,"ranged":0,"mobile":0}
var intercepts := {"melee":0,"ranged":0,"mobile":0}
var disengages := 0
var estimate_enemy_mean := 1.999
var estimate_source := "spike04 measured normal presentation"
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
		if u.kind=="ranged":
			for target in s.units:
				if Rules.in_range(s.level,u,target) and not Rules.attack_info(s,u,target).legal: los_opportunities+=1
		var reachable := Rules.reach(s,u.id)
		var could_attack := false
		for p in reachable.costs:
			var hypothetical: Dictionary = u.duplicate(true)
			hypothetical.cell=p
			for target in s.units:
				if Rules.attack_info(s,hypothetical,target).legal: could_attack=true
		unit_turns[key]={"turn":s.turn,"id":u.id,"side":u.side,"kind":u.kind,"group":u.group,"eligible":u.born_turn<s.turn,"observed":false,"move_steps":0,"move_cost":0,"attacks":0,"role_reason":"","could_reach_target":could_attack}
		ensure(u.kind,u.side)
		totals[u.kind].unit_turns+=1
		if not could_attack: totals[u.kind].idle_turns+=1

func record(before: Dictionary, events: Array, after: Dictionary) -> void:
	var turn: int = before.turn
	var spatial := before.duplicate(true)
	var roster := {}
	for u in before.units+after.units:
		roster[u.id]=u
		ensure(u.kind,u.side)
	for e in events:
		if e.type=="intercept": intercepts[roster[e.source].kind]+=1
		if e.type=="disengage": disengages+=1
		if e.type in ["intent","move","attack","wait"]:
			var key := "%d:%s" % [turn,e.unit]
			if unit_turns.has(key): unit_turns[key].observed=true
		if e.type=="phase":
			turn=int(e.turn)
			register(before if e.phase=="enemy" else after,"enemy" if e.phase=="enemy" else "ally")
		if e.type=="move":
			Rules.unit(spatial,e.unit).cell=e.path.back()
			var kind: String = roster[e.unit].kind
			var key := "%d:%s" % [turn,e.unit]
			if unit_turns.has(key):
				unit_turns[key].move_steps+=e.path.size()-1
				unit_turns[key].move_cost+=e.cost
			totals[kind].move_steps+=e.path.size()-1
			totals[kind].moves+=1
		if e.type=="attack":
			var key := "%d:%s" % [turn,e.unit]
			if unit_turns.has(key): unit_turns[key].attacks+=1
			if roster[e.unit].group=="reinforcements" or roster[e.target].group=="reinforcements":
				if reinforcement_first_engage<0: reinforcement_first_engage=turn
			if roster[e.unit].group=="reinforcements" and reinforcement_first_attack<0: reinforcement_first_attack=turn
			if roster[e.target].group=="reinforcements" and reinforcement_first_attacked<0: reinforcement_first_attacked=turn
			if roster[e.unit].kind=="ranged":
				var sight := Sight.check(spatial,Rules.unit(spatial,e.unit),Rules.unit(spatial,e.target))
				ranged_shots.append({"turn":turn,"source":e.unit,"target":e.target,"would_block":not sight.clear,"cover":sight.cover,"reason":sight.reason})
			if first_contact_turn<0:
				first_contact_turn=turn
				first_contact_side=roster[e.unit].side
			totals[roster[e.unit].kind].attacks+=1
		if e.type=="damage":
			if e.hp_after==0 and roster[e.source].side=="ally" and Rules.unit(spatial,e.unit).hp<Rules.unit(spatial,e.unit).max_hp: finishing_kills[roster[e.source].kind]+=1
			Rules.unit(spatial,e.unit).hp=e.hp_after
			totals[roster[e.source].kind].damage_dealt+=e.amount
			totals[roster[e.unit].kind].damage_taken+=e.amount
			if e.hp_after==0: totals[roster[e.source].kind].kills+=1
			if e.hp_after==0 and roster[e.unit].side=="ally": deaths.append({"id":e.unit,"kind":roster[e.unit].kind,"turn":turn})
		if e.type=="knockback": Rules.unit(spatial,e.unit).cell=e.to
		if e.type=="intent" and e.get("role_hold",false):
			var key := "%d:%s" % [turn,e.unit]
			if unit_turns.has(key): unit_turns[key].role_reason=e.reason
		trace.append({"turn":turn,"event":e.duplicate(true)})
	final_status=after.status
	final_turn=after.turn

func summary() -> Dictionary:
	var archetypes := totals.duplicate(true)
	var idle := {"front":0,"flank":0,"south":0,"reserve":0,"rear":0,"leader":0,"reinforcements":0}
	var deliberate: Array = []
	for row in unit_turns.values():
		if row.side!="enemy" or not row.eligible or not row.observed: continue
		if not row.role_reason.is_empty(): deliberate.append(row)
		elif not row.could_reach_target and row.move_steps==0 and row.attacks==0: idle[row.group]=idle.get(row.group,0)+1
	var ally_damage := 0.0
	var ally_kills := 0.0
	var living_turns := 0
	for kind in ["melee","ranged","mobile"]:
		if totals.has(kind):
			ally_damage+=totals[kind].damage_dealt
			ally_kills+=totals[kind].kills
			living_turns+=totals[kind].unit_turns
	for kind in archetypes:
		archetypes[kind].average_move_per_unit_turn=float(archetypes[kind].move_steps)/maxi(1,archetypes[kind].unit_turns)
		if archetypes[kind].side=="ally":
			archetypes[kind].damage_share=archetypes[kind].damage_dealt/maxf(1,ally_damage)
			archetypes[kind].kill_share=archetypes[kind].kills/maxf(1,ally_kills)
	return {"first_contact_turn":first_contact_turn,"first_contact_side":first_contact_side,
		"finishing_kills":finishing_kills,"intercepts":intercepts,"disengages":disengages,
		"reinforcement_first_attack_turn":reinforcement_first_attack,"reinforcement_first_attacked_turn":reinforcement_first_attacked,"los_blocked_opportunities":los_opportunities,
		"enemy_idle_by_group":idle,"deliberate_holds":deliberate,"reinforcement_first_engage_turn":reinforcement_first_engage,
		"ally_deaths":deaths,"ranged_shots":ranged_shots,"los_blocked_shots":ranged_shots.filter(func(r):return r.would_block).size(),
		"living_ally_unit_turns":living_turns,
		"battle_length_estimate_minutes":[(final_turn*estimate_enemy_mean+living_turns*15)/60.0,(final_turn*estimate_enemy_mean+living_turns*25)/60.0],
		"estimate_enemy_mean_seconds":estimate_enemy_mean,"estimate_enemy_mean_source":estimate_source,
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
