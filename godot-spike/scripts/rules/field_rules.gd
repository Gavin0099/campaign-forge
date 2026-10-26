extends RefCounted
## Pure, deterministic field rules. No nodes, animation, I/O or shared mutable cache.
const Data = preload("res://data/levels/field_24x18.gd")
const Sight = preload("res://scripts/rules/field_sight.gd")
const DIRS = [Vector2i.UP,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.DOWN]

static func make_unit(id: String, side: String, kind: String, cell: Vector2i, group: String, level: Dictionary, born: int = 0) -> Dictionary:
	var stats: Dictionary = level.stats[kind]
	return {"id":id,"side":side,"kind":kind,"cell":cell,"group":group,"hp":stats.hp,"max_hp":stats.hp,
		"moved":false,"acted":false,"born_turn":born,"threatened":false,"ai":"guard"}

static func initial(level: Dictionary = Data.build()) -> Dictionary:
	var units: Array = []
	for row in level.deployment: units.append(make_unit(row[0],row[1],row[2],row[3],row[4],level))
	return {"level":level.duplicate(true),"units":units,"turn":1,"phase":"player","status":"playing",
		"groups":{},"warned":false,"spawned":false,"occupancy_revision":0}

static func unit(s: Dictionary, id: String) -> Dictionary:
	for u in s.units:
		if u.id==id: return u
	return {}

static func occupant(s: Dictionary, cell: Vector2i, except_id: String = "") -> Dictionary:
	for u in s.units:
		if u.id!=except_id and u.hp>0 and u.cell==cell: return u
	return {}

static func inside(level: Dictionary, cell: Vector2i) -> bool:
	return cell.x>=0 and cell.y>=0 and cell.x<level.size.x and cell.y<level.size.y

static func terrain(level: Dictionary, cell: Vector2i) -> String:
	return level.rows[cell.y][cell.x] if inside(level,cell) else "^"

static func cost(level: Dictionary, cell: Vector2i, kind: String) -> int:
	var tile := terrain(level,cell)
	var value: int = level.terrain[tile].cost
	return value + (int(level.stats[kind].forest_extra) if tile=="f" else 0) if value>0 else 0

static func distance(a: Vector2i, b: Vector2i) -> int:
	return absi(a.x-b.x)+absi(a.y-b.y)

static func allowed(s: Dictionary, u: Dictionary) -> bool:
	return not u.is_empty() and u.hp>0 and s.status=="playing" and not u.acted \
		and u.side==("ally" if s.phase=="player" else "enemy") and u.born_turn<s.turn

static func reject(s: Dictionary, reason: String) -> Dictionary:
	return {"ok":false,"state":s.duplicate(true),"events":[],"reason":reason}

static func result(s: Dictionary, events: Array) -> Dictionary:
	return {"ok":true,"state":s,"events":events}

static func reach(s: Dictionary, id: String, budget: int = -1) -> Dictionary:
	var u := unit(s,id)
	if u.is_empty() or u.hp<=0: return {"costs":{},"parents":{}}
	if budget<0: budget = s.level.stats[u.kind].move
	var costs := {u.cell:0}
	var parents := {}
	var open: Array = [u.cell]
	while not open.is_empty():
		open.sort_custom(func(a,b): return costs[a]<costs[b])
		var here: Vector2i = open.pop_front()
		for direction in DIRS:
			var next: Vector2i = here+direction
			var step := cost(s.level,next,u.kind)
			var total: int = costs[here]+step
			if step==0 or total>budget or not occupant(s,next,id).is_empty(): continue
			if costs.has(next) and costs[next]<=total: continue
			costs[next]=total
			parents[next]=here
			if next not in open: open.append(next)
	return {"costs":costs,"parents":parents}

static func path_to(reachable: Dictionary, start: Vector2i, to: Vector2i) -> Array:
	if not reachable.costs.has(to): return []
	var path: Array = [to]
	while path.front()!=start: path.push_front(reachable.parents[path.front()])
	return path

static func move(s: Dictionary, id: String, to: Vector2i) -> Dictionary:
	var u := unit(s,id)
	if not allowed(s,u) or u.moved: return reject(s,"cannot-move")
	var reachable := reach(s,id)
	var path := path_to(reachable,u.cell,to)
	if path.size()<2: return reject(s,"illegal-move")
	var next := s.duplicate(true)
	unit(next,id).cell=to
	unit(next,id).moved=true
	next.occupancy_revision+=1
	return result(next,[{"type":"move","unit":id,"path":path,"cost":reachable.costs[to]}])

static func in_range(level: Dictionary, attacker: Dictionary, target: Dictionary) -> bool:
	if attacker.is_empty() or target.is_empty() or attacker.hp<=0 or target.hp<=0 or attacker.side==target.side: return false
	var stats: Dictionary = level.stats[attacker.kind]
	var d := distance(attacker.cell,target.cell)
	return d>=stats.min_range and d<=stats.max_range

static func targets(s: Dictionary, id: String) -> Array:
	var found: Array = []
	var u := unit(s,id)
	for other in s.units:
		if attack_info(s,u,other).legal: found.append(other.id)
	return found

static func attack_info(s: Dictionary, a: Dictionary, b: Dictionary) -> Dictionary:
	if not in_range(s.level,a,b): return {"legal":false,"damage":0,"cover":false,"reason":"不在射程／同陣營"}
	var sight := {"clear":true,"cover":false,"reason":"近戰接觸"}
	if a.kind=="ranged": sight=Sight.check(s,a,b)
	return {"legal":sight.clear,"damage":maxi(1,int(s.level.stats[a.kind].damage)-(1 if sight.cover else 0)) if sight.clear else 0,"cover":sight.cover,"reason":sight.reason}

static func threat(s: Dictionary, id: String) -> Dictionary:
	var found := {}
	var u := unit(s,id)
	if u.is_empty() or u.hp<=0 or u.born_turn>=s.turn: return found
	var stats: Dictionary = s.level.stats[u.kind]
	for p in reach(s,id).costs:
		var hypothetical := u.duplicate(true)
		hypothetical.cell=p
		for y in range(-int(stats.max_range),int(stats.max_range)+1):
			for x in range(-int(stats.max_range),int(stats.max_range)+1):
				var at: Vector2i = p+Vector2i(x,y)
				if not inside(s.level,at) or cost(s.level,at,"melee")==0: continue
				var target := {"id":"threat-probe","side":"ally" if u.side=="enemy" else "enemy","hp":1,"cell":at}
				if attack_info(s,hypothetical,target).legal: found[at]=true
	return found

static func terminal(s: Dictionary, events: Array) -> void:
	if unit(s,"thoma").hp<=0: s.status="lose"
	elif unit(s,"leader").hp<=0: s.status="win"
	elif s.turn>s.level.turn_limit: s.status="lose"
	if s.status!="playing":
		s.phase="finished"
		events.append({"type":"result","status":s.status,"reason":"thoma_falls" if unit(s,"thoma").hp<=0 else ("leader_defeated" if s.status=="win" else "turn_limit")})

static func attack(s: Dictionary, id: String, target_id: String) -> Dictionary:
	var u := unit(s,id)
	var victim := unit(s,target_id)
	if not allowed(s,u): return reject(s,"illegal-attack")
	var info := attack_info(s,u,victim)
	if not info.legal: return reject(s,info.reason)
	var next := s.duplicate(true)
	var target := unit(next,target_id)
	var amount := mini(int(info.damage),int(target.hp))
	target.hp-=amount
	target.threatened=true
	unit(next,id).moved=true
	unit(next,id).acted=true
	next.groups[victim.group]="alert"
	# Alert neighbours of the attacked group, measured before knockback/death.
	for member in s.units:
		if member.group!=victim.group: continue
		for neighbour in s.units:
			if neighbour.side==victim.side and neighbour.hp>0 and distance(member.cell,neighbour.cell)<=s.level.ai.neighbour_radius:
				next.groups[neighbour.group]="alert"
	var events: Array = [{"type":"attack","unit":id,"target":target_id,"kind":u.kind,"cover":info.cover,"sight_reason":info.reason},
		{"type":"damage","unit":target_id,"source":id,"amount":amount,"hp_after":target.hp}]
	if s.level.stats[u.kind].knockback:
		var into: Vector2i = victim.cell+(victim.cell-u.cell)
		var blocker := occupant(s,into,target_id)
		if cost(s.level,into,victim.kind)==0 or not blocker.is_empty():
			var blocked := {"type":"knockback_blocked","unit":target_id,"from":victim.cell,"into":into,"blocker":"terrain" if blocker.is_empty() else "unit"}
			if not blocker.is_empty(): blocked.blocker_id=blocker.id
			events.append(blocked)
		else:
			target.cell=into
			events.append({"type":"knockback","unit":target_id,"from":victim.cell,"to":into})
	next.occupancy_revision+=1
	terminal(next,events)
	return result(next,events)

static func wait(s: Dictionary, id: String) -> Dictionary:
	if not allowed(s,unit(s,id)): return reject(s,"cannot-wait")
	var next := s.duplicate(true)
	unit(next,id).acted=true
	unit(next,id).moved=true
	return result(next,[{"type":"wait","unit":id}])

static func entry_fallback(s: Dictionary, requested: Vector2i) -> Vector2i:
	# Nearest empty passable cell, BFS UP/LEFT/RIGHT/DOWN. Deferred if no space.
	var open: Array = [requested]
	var seen := {requested:true}
	for unused in range(s.level.size.x*s.level.size.y):
		if open.is_empty(): break
		var here: Vector2i = open.pop_front()
		if cost(s.level,here,"knight")>0 and occupant(s,here).is_empty(): return here
		for dir in DIRS:
			var p: Vector2i = here+dir
			if inside(s.level,p) and not seen.has(p):
				seen[p]=true
				open.append(p)
	return Vector2i(-1,-1)

static func next_turn(s: Dictionary) -> Dictionary:
	var next := s.duplicate(true)
	var events: Array = []
	next.turn+=1
	terminal(next,events)
	if next.status!="playing": return result(next,events)
	next.phase="player"
	for u in next.units:
		u.moved=false
		u.acted=false
	if not next.warned and next.turn>=next.level.reinforcement_turn-1:
		next.warned=true
		events.append({"type":"reinforcement_warning","turn":next.level.reinforcement_turn,"entries":next.level.entries.duplicate(),"kinds":next.level.reinforcement_kinds.duplicate(),"announced_on":next.turn})
	if not next.spawned and next.turn>=next.level.reinforcement_turn:
		var spawned := 0
		for i in range(next.level.entries.size()):
			var id := "reinforcement-%d" % i
			if not unit(next,id).is_empty():
				spawned+=1
				continue
			var entry: Vector2i = next.level.entries[i]
			var at := entry_fallback(next,entry)
			if at.x<0:
				events.append({"type":"reinforcement_deferred","entry":entry})
				continue
			next.units.append(make_unit(id,"enemy",next.level.reinforcement_kinds[i],at,"reinforcements",next.level,next.turn))
			next.occupancy_revision+=1
			spawned+=1
			events.append({"type":"reinforcement_arrival","unit":id,"turn":next.turn,"entry":entry,"cell":at,"kind":next.level.reinforcement_kinds[i],"can_act":false})
		next.spawned=spawned==next.level.entries.size()
	events.append({"type":"phase","phase":"player","turn":next.turn})
	return result(next,events)

static func distance_map(s: Dictionary, kind: String, side: String, target_id: String = "") -> Dictionary:
	# Shared reverse Dijkstra to all legal attack slots, not per destination/target.
	# A phase-local cache keys kind+occupancy_revision and is invalidated on moves/death.
	var costs := {}
	var open: Array = []
	var stats: Dictionary = s.level.stats[kind]
	for target in s.units:
		if target.hp<=0 or target.side==side: continue
		if not target_id.is_empty() and target.id!=target_id: continue
		for dy in range(-int(stats.max_range),int(stats.max_range)+1):
			for dx in range(-int(stats.max_range),int(stats.max_range)+1):
				var p: Vector2i = target.cell+Vector2i(dx,dy)
				var d := distance(p,target.cell)
				if d<stats.min_range or d>stats.max_range or cost(s.level,p,kind)==0 or not occupant(s,p).is_empty(): continue
				if kind=="ranged" and not Sight.check(s,{"id":"path-probe","cell":p},target).clear: continue
				if not costs.has(p):
					costs[p]=0
					open.append(p)
	while not open.is_empty():
		open.sort_custom(func(a,b): return costs[a]<costs[b])
		var here: Vector2i = open.pop_front()
		for dir in DIRS:
			var p: Vector2i = here+dir
			if cost(s.level,p,kind)==0: continue
			var occupied := occupant(s,p)
			if not occupied.is_empty() and occupied.side!=side: continue
			var total: int = costs[here]+cost(s.level,here,kind)
			if costs.has(p) and costs[p]<=total: continue
			costs[p]=total
			# Friendly occupied cells may read a distance, but cannot be transit.
			if occupied.is_empty() and p not in open: open.append(p)
	return costs

static func best_move(s: Dictionary, id: String, cache: Dictionary, waypoint: Vector2i = Vector2i(-1,-1)) -> Vector2i:
	var u := unit(s,id)
	var key := "%s:%s:%d" % [u.kind,u.side,s.occupancy_revision]
	if not cache.has(key): cache[key]=distance_map(s,u.kind,u.side)
	var distances: Dictionary = cache[key]
	var reachable := reach(s,id)
	var best: Vector2i = u.cell
	var score := INF
	for p in reachable.costs:
		var value: float = distances.get(p,10000)
		if waypoint.x>=0: value=distance(p,waypoint)
		# Seeded deterministic coordinate tie break. Never use process-global RNG.
		value += float((p.x*31+p.y*17+int(s.level.seed))%101)*0.0001
		if value<score:
			score=value
			best=p
	return best

static func focus_targets(s: Dictionary, id: String, candidates: Array) -> Array:
	var u := unit(s,id)
	var ordered := candidates.duplicate()
	ordered.sort_custom(func(a,b):
		var aa := unit(s,a)
		var bb := unit(s,b)
		if aa.hp!=bb.hp: return aa.hp<bb.hp
		var ta := distance(aa.cell,unit(s,"leader").cell)<=4
		var tb := distance(bb.cell,unit(s,"leader").cell)<=4
		if ta!=tb: return ta
		var da := distance(u.cell,aa.cell)
		var db := distance(u.cell,bb.cell)
		if da!=db: return da<db
		var ea: bool = aa.kind in ["ranged","mobile"]
		var eb: bool = bb.kind in ["ranged","mobile"]
		if ea!=eb: return ea
		return a<b)
	return ordered

static func activation(s: Dictionary, u: Dictionary) -> String:
	if s.groups.get(u.group,"")=="alert": return "latched / attacked group or neighbour"
	if u.group=="reinforcements": return "arrival rested; intercept leader approach"
	if s.turn>=s.level.ai.march_turn: return "turn 4 march timer"
	for ally in s.units:
		if ally.side=="ally" and ally.hp>0 and distance(u.cell,ally.cell)<=s.level.alert_radius: return "Manhattan sight 6"
	return ""

static func ai_plan(s: Dictionary, id: String, cache: Dictionary) -> Dictionary:
	var u := unit(s,id)
	var leader := unit(s,"leader")
	var available := targets(s,id)
	var nearby_allies: Array = s.units.filter(func(v):return v.hp>0 and v.side=="ally" and distance(v.cell,u.cell)<=3)
	var friends: Array = s.units.filter(func(v):return v.hp>0 and v.side=="enemy" and v.id!=id and v.kind!="leader")
	var state_name := "advance"
	var role_reason := ""
	var waypoint := Vector2i(-1,-1)
	if u.kind=="leader":
		# Counter unless low HP and surrounded. Retreat exactly one adjacent cell,
		# stay within 2 of the authored point, improve nearest opponent distance.
		if not available.is_empty() and not (u.hp<=4 and nearby_allies.size()>=2):
			return {"state":"counter","to":u.cell,"reason":"adjacent counter","role_hold":false}
		var best: Vector2i = u.cell
		var safety := 999
		for ally in s.units:
			if ally.side=="ally" and ally.hp>0: safety=mini(safety,distance(u.cell,ally.cell))
		for dir in DIRS:
			var p: Vector2i = u.cell+dir
			if cost(s.level,p,u.kind)==0 or not occupant(s,p).is_empty() or distance(p,s.level.hold_point)>2: continue
			var value := 999
			for ally in s.units:
				if ally.side=="ally" and ally.hp>0: value=mini(value,distance(p,ally.cell))
			if safety<=2 and value>safety:
				best=p
				safety=value
		return {"state":"step-back" if best!=u.cell else "leader-hold","to":best,"reason":"safer adjacent within hold radius 2" if best!=u.cell else "leader holds command point","role_hold":best==u.cell}
	if not available.is_empty(): return {"state":"attack","to":u.cell,"reason":"legal target before movement","role_hold":false}
	var interceptors: Array = s.units.filter(func(v):return v.hp>0 and v.side=="ally" and distance(v.cell,leader.cell)<=s.level.ai.intercept_radius)
	if u.group=="reserve":
		state_name="bodyguard-intercept"
		if interceptors.is_empty():
			if distance(u.cell,leader.cell)<=s.level.ai.bodyguard_radius:
				return {"state":"bodyguard-hold","to":u.cell,"reason":"bodyguard within leader radius 3","role_hold":true}
			waypoint=leader.cell
	elif u.group=="reinforcements": state_name="intercept"
	# One regroup movement per activation; then resume advance. No oscillating
	# infinite regroup loop. Immediate reachable attacks always take precedence.
	var support: Array = friends.filter(func(v):return distance(v.cell,u.cell)<=s.level.ai.support_radius)
	if nearby_allies.size()>support.size()+1 and support.is_empty() and not friends.is_empty() and not u.get("regrouped",false):
		friends.sort_custom(func(a,b):return distance(a.cell,u.cell)<distance(b.cell,u.cell) if distance(a.cell,u.cell)!=distance(b.cell,u.cell) else a.id<b.id)
		waypoint=friends[0].cell
		state_name="regroup"
		role_reason="outnumbered locally; one regroup toward nearest supporting knight"
	var target_id := ""
	if state_name in ["intercept","bodyguard-intercept"] and not interceptors.is_empty():
		interceptors.sort_custom(func(a,b):return distance(a.cell,leader.cell)<distance(b.cell,leader.cell) if distance(a.cell,leader.cell)!=distance(b.cell,leader.cell) else a.id<b.id)
		target_id=interceptors[0].id
	var key := "%s:%s:%d:%s" % [u.kind,u.side,s.occupancy_revision,target_id]
	if not cache.has(key): cache[key]=distance_map(s,u.kind,u.side,target_id)
	var distances: Dictionary = cache[key]
	var reachable := reach(s,id)
	var best: Vector2i = u.cell
	var score := INF
	for p in reachable.costs:
		if u.group=="reserve" and state_name!="regroup" and distance(p,leader.cell)>s.level.ai.bodyguard_radius: continue
		var progress: float = distances.get(p,10000)
		if waypoint.x>=0: progress=distance(p,waypoint)
		var cohesion := 0.0
		if not friends.is_empty():
			var nearest := 999
			for mate in friends: nearest=mini(nearest,distance(p,mate.cell))
			cohesion=minf(6,nearest)*.12 # less than one path-cost step: loose front
		var value: float = progress+cohesion+float((p.x*31+p.y*17+int(s.level.seed))%101)*.0001
		if value<score:
			score=value
			best=p
	# If a lane is blocked, try a legal lateral regroup step instead of silent idle.
	if best==u.cell and waypoint.x<0 and reachable.costs.size()>1 and not distances.has(u.cell):
		for p in reachable.costs:
			if p!=u.cell and distance(p,leader.cell)<=distance(u.cell,leader.cell):
				best=p
				state_name="regroup"
				break
	return {"state":state_name,"to":best,"reason":role_reason if not role_reason.is_empty() else ("leader approach interception" if target_id!="" else "shared distance map; loose-front cohesion"),"role_hold":false}

static func enemy_phase(s: Dictionary) -> Dictionary:
	if s.phase!="player" or s.status!="playing": return reject(s,"cannot-end-turn")
	var next := s.duplicate(true)
	var events: Array = [{"type":"phase","phase":"enemy","turn":s.turn}]
	next.phase="enemy"
	for u in next.units:
		if u.side=="ally":
			u.moved=true
			u.acted=true
	# Activation snapshots before movement; groups latch and never deactivate.
	var reasons := {}
	for u in next.units:
		if u.side!="enemy" or u.hp<=0: continue
		var reason := activation(s,u)
		if not reason.is_empty():
			next.groups[u.group]="alert"
			reasons[u.group]=reason
	var cache := {}
	for original in s.units:
		var u := unit(next,original.id)
		if u.side!="enemy" or not allowed(next,u): continue
		var active: bool = next.groups.get(u.group,"guard")=="alert"
		if not active:
			u.ai="guard"
			events.append({"type":"intent","unit":u.id,"state":"guard","reason":"hold until radius %d / group attacked" % next.level.alert_radius})
			continue
		var plan := ai_plan(next,u.id,cache)
		u.ai=plan.state
		if plan.state=="regroup": u.regrouped=true
		events.append({"type":"intent","unit":u.id,"state":plan.state,"reason":plan.reason,"activation":reasons.get(u.group,"group latched"),"role_hold":plan.role_hold})
		if plan.to!=u.cell:
			var moved := move(next,u.id,plan.to)
			if moved.ok:
				next=moved.state
				events.append_array(moved.events)
		var available := targets(next,u.id)
		if not available.is_empty():
			available=focus_targets(next,u.id,available)
			events.append({"type":"intent","unit":u.id,"state":"attack","target":available[0],"reason":"low HP > leader threat > closest > exposed class > id"})
			var hit := attack(next,u.id,available[0])
			next=hit.state
			events.append_array(hit.events)
		else:
			var waited := wait(next,u.id)
			next=waited.state
			events.append_array(waited.events)
		if next.status!="playing": return result(next,events)
	var advanced := next_turn(next)
	events.append_array(advanced.events)
	return result(advanced.state,events)
