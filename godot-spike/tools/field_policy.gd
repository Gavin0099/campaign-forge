extends RefCounted
## Reproducible test policies, not enemy rules or human strategy claims.
const Rules = preload("res://scripts/rules/field_rules.gd")
const Data = preload("res://data/levels/field_24x18.gd")
const OldData = preload("res://data/levels/field_24x18_spike05.gd")
const Legacy = preload("res://tools/field_policy_spike05.gd")

static func start(policy: String, seed_value: int = 24018, variant: String = "default") -> Dictionary:
	var level := OldData.build() if variant=="spike05" else Data.build()
	level.seed=seed_value
	level.variant=variant
	var s := Rules.initial(level)
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
		var aa := Rules.unit(s,a)
		var bb := Rules.unit(s,b)
		var ak: bool = aa.hp<=Rules.attack_info(s,Rules.unit(s,id),aa).damage
		var bk: bool = bb.hp<=Rules.attack_info(s,Rules.unit(s,id),bb).damage
		if ak!=bk: return ak
		if a=="leader" or b=="leader": return a=="leader"
		if aa.hp!=bb.hp: return aa.hp<bb.hp
		return a<b if s.level.seed==24018 else tie(s,a)<tie(s,b))
	return candidates[0] if not candidates.is_empty() else ""

static func command(s: Dictionary, id: String, policy: String) -> Dictionary:
	if s.level.get("variant","")=="spike05" or policy in ["turtle","scout-retreat","bypass"]: return Legacy.command(s,id,policy)
	return supported_command(s,id,policy)

static func resolve(s: Dictionary, command_value: Dictionary) -> Dictionary:
	match command_value.type:
		"move": return Rules.move(s,command_value.unit,command_value.to)
		"attack": return Rules.attack(s,command_value.unit,command_value.target)
		_: return Rules.wait(s,command_value.unit)

static func order(s: Dictionary) -> Array:
	if s.level.get("variant","")=="spike05": return Legacy.order(s)
	# Durable melee first; bows protect them; scouts exploit the remaining slots.
	var ids: Array = []
	for kind in ["melee","ranged","mobile"]:
		for u in s.units:
			if u.side=="ally" and u.hp>0 and u.kind==kind: ids.append(u.id)
	if s.level.seed!=24018:
		# Same class priority; seeded ordering only among equally ranked allies.
		ids.sort_custom(func(a,b):
			var ranks := {"melee":0,"ranged":1,"mobile":2}
			var aa: int = ranks[Rules.unit(s,a).kind]
			var bb: int = ranks[Rules.unit(s,b).kind]
			return aa<bb if aa!=bb else tie(s,a)<tie(s,b))
	return ids

static func exposure(s: Dictionary, cell: Vector2i, id: String) -> float:
	# Conservative local threat estimate, not hidden enemy future-state access.
	var risk := 0.0
	for foe in s.units:
		if foe.side!="enemy" or foe.hp<=0 or foe.born_turn>=s.turn: continue
		if foe.kind=="leader" or foe.group=="reserve":
			if Rules.distance(cell,foe.cell)<=2: risk+=1.0
		else:
			var d := Rules.distance(cell,foe.cell)
			if d<=2: risk+=1.0
			elif d<=5: risk+=.5
	# A close durable screen reduces but never erases threat.
	for ally in s.units:
		if ally.id!=id and ally.side=="ally" and ally.hp>=4 and ally.kind=="melee" and Rules.distance(cell,ally.cell)<=2: risk-=.4
	return maxf(0,risk)

static func supported_command(s: Dictionary, id: String, policy: String) -> Dictionary:
	var u := Rules.unit(s,id)
	if not Rules.allowed(s,u): return {}
	var victim := target(s,id)
	var retreat: bool = not u.moved and u.hp<=4 and exposure(s,u.cell,id)>=1.0
	if victim!="" and not retreat: return {"type":"attack","unit":id,"target":victim}
	if u.moved: return {"type":"wait","unit":id}
	var reachable := Rules.reach(s,id)
	var distances := Rules.distance_map(s,u.kind,u.side)
	var best: Vector2i = u.cell
	var best_score := -INF
	for p in reachable.costs:
		var hypothetical := u.duplicate(true)
		hypothetical.cell=p
		var attack_value := 0.0
		for foe in s.units:
			var info := Rules.attack_info(s,hypothetical,foe)
			if info.legal:
				var value := float(mini(info.damage,foe.hp))*2.0
				if foe.hp<=info.damage: value+=9.0
				if foe.id=="leader": value+=3.0
				attack_value=maxf(attack_value,value)
		var danger := exposure(s,p,id)
		var danger_weight := 1.3 if u.kind=="melee" else 2.0
		if u.hp<=4: danger_weight*=2.0
		if id=="thoma" and u.hp<=4: danger_weight*=4.0
		var progress: float = distances.get(p,100)
		var score := attack_value-progress*.65-danger*danger_weight
		if u.kind=="mobile":
			var guard := Rules.unit(s,"guard")
			var anchor: Vector2i = guard.cell if not guard.is_empty() and guard.hp>0 else Rules.unit(s,"thoma").cell
			score-=maxi(0,Rules.distance(p,anchor)-3)*1.2
			if policy=="flank": score-=absf(p.y-7)*.12
		score+=float(tie(s,str(p))%1000)*.00001
		if score>best_score:
			best_score=score
			best=p
	if best!=u.cell: return {"type":"move","unit":id,"to":best}
	if victim!="": return {"type":"attack","unit":id,"target":victim}
	return {"type":"wait","unit":id}

static func tie(s: Dictionary, key: String) -> int:
	return ("%d:%d:%s" % [s.level.seed,s.turn,key]).hash()
