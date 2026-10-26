extends RefCounted
## Reproducible test policies, not enemy rules or human strategy claims.
const Rules = preload("res://scripts/rules/field_rules.gd")

static func start(policy: String) -> Dictionary:
	var s := Rules.initial()
	if policy=="bypass":
		var placements := {"thoma":Vector2i(17,9),"guard":Vector2i(17,10),"bow-1":Vector2i(16,9),"bow-2":Vector2i(16,10),"scout-1":Vector2i(18,8),"scout-2":Vector2i(18,10)}
		for id in placements: Rules.unit(s,id).cell=placements[id]
		s.turn=4
		s.warned=true
		s=Rules.next_turn(s).state
	return s

static func target(s: Dictionary, id: String) -> String:
	var candidates := Rules.targets(s,id)
	candidates.sort_custom(func(a,b):
		if a=="leader" or b=="leader": return a=="leader"
		var aa := Rules.unit(s,a)
		var bb := Rules.unit(s,b)
		return aa.hp<bb.hp if aa.hp!=bb.hp else a<b)
	return candidates[0] if not candidates.is_empty() else ""

static func command(s: Dictionary, id: String, policy: String) -> Dictionary:
	var u := Rules.unit(s,id)
	if not Rules.allowed(s,u): return {}
	if policy=="scout-retreat" and u.kind=="mobile" and u.hp<=4 and not u.moved:
		var safest: Vector2i = u.cell
		var best := -INF
		for p in Rules.reach(s,id).costs:
			var nearest := 999
			for foe in s.units:
				if foe.hp>0 and foe.side=="enemy": nearest=mini(nearest,Rules.distance(p,foe.cell))
			var value := nearest-.1*Rules.distance(p,Rules.unit(s,"thoma").cell)
			if value>best:
				best=value
				safest=p
		if safest!=u.cell: return {"type":"move","unit":id,"to":safest}
	var victim := target(s,id)
	if victim!="": return {"type":"attack","unit":id,"target":victim}
	if not u.moved:
		var waypoint := Vector2i(-1,-1)
		if policy in ["flank","scout-retreat"] and u.kind=="mobile" and u.cell.x<17:
			waypoint=Vector2i(16,5) if u.cell.y<=6 or u.cell.x<12 else Vector2i(14,5)
		if policy=="turtle" and s.turn<=3:
			waypoint=Vector2i(10,9 if u.id in ["thoma","bow-1","scout-1"] else 10)
		var cache := {}
		var to := Rules.best_move(s,id,cache,waypoint)
		# Turtle: after establishing a firing line, ranged pursue; melee only advance
		# when a legal move could attack, instead of indefinite zero-contact camping.
		if policy=="turtle" and s.turn>3 and u.kind!="ranged":
			var fake := s.duplicate(true)
			Rules.unit(fake,id).cell=to
			if Rules.targets(fake,id).is_empty(): to=u.cell
		if to!=u.cell: return {"type":"move","unit":id,"to":to}
	return {"type":"wait","unit":id}

static func resolve(s: Dictionary, command_value: Dictionary) -> Dictionary:
	match command_value.type:
		"move": return Rules.move(s,command_value.unit,command_value.to)
		"attack": return Rules.attack(s,command_value.unit,command_value.target)
		_: return Rules.wait(s,command_value.unit)

static func order(s: Dictionary) -> Array:
	# Durable melee first; bows protect them; scouts exploit the remaining slots.
	var ids: Array = []
	for kind in ["melee","ranged","mobile"]:
		for u in s.units:
			if u.side=="ally" and u.hp>0 and u.kind==kind: ids.append(u.id)
	return ids
