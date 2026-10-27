extends Control
## Deterministic screen-space declutter. One compact HP/class plate per visible
## unit; overview uses constant-pixel shapes/pips and one label per group.
var battle
var items: Array = []
var obstacles: Array = []
var markers: Array = []
var suppressed: Array = []
const AREA = Rect2(54,232,1172,304)
const MARKER_RADIUS = 7.0

func screen(world: Vector2) -> Vector2:
	return (world-battle.camera.position-battle.camera.offset)*battle.camera.zoom+battle.camera.VIEW/2

func vacant(rect: Rect2) -> bool:
	if not AREA.encloses(rect): return false
	for obstacle in obstacles:
		if rect.grow(3).intersects(obstacle): return false
	for item in items:
		if rect.grow(3).intersects(item.rect): return false
	return true

func place(id: String, text: String, anchor: Vector2, color: Color, width: float = 100) -> void:
	var desired := Rect2(anchor-Vector2(width/2,28),Vector2(width,22))
	var candidates: Array[Rect2] = []
	for dy in [0,-26,26,-52,52,-78,78]:
		for dx in [0,106,-106,212,-212]: candidates.append(Rect2(desired.position+Vector2(dx,dy),desired.size))
	# Finite fallback slots, top-to-bottom then left-to-right, same each frame.
	for y in range(236,510,28):
		for x in range(60,1120,108): candidates.append(Rect2(Vector2(x,y),desired.size))
	for rect in candidates:
		if vacant(rect):
			items.append({"id":id,"text":text,"rect":rect,"anchor":anchor,"color":color})
			return
	suppressed.append(id) # Lower-priority labels may disappear; never intersect.

func refresh_layout() -> void:
	items.clear()
	obstacles.clear()
	markers.clear()
	suppressed.clear()
	if not is_instance_valid(battle.hud): return
	# Terminal modal owns the centre; world plates must not cover its result text.
	if battle.state.status!="playing": return
	for indicator in battle.hud.indicators.items: obstacles.append(indicator.rect)
	var zoom_value: float = battle.camera.zoom.x
	var overview: bool = battle.camera.overview
	var alive: Array = battle.state.units.filter(func(u):return u.hp>0)
	alive.sort_custom(func(a,b):
		if a.id==battle.selected_id or b.id==battle.selected_id: return a.id==battle.selected_id
		if a.kind=="leader" or b.kind=="leader": return a.kind=="leader"
		return a.id<b.id)
	for u in alive:
		if not battle.actors.has(u.id): continue
		var p := screen(battle.actors[u.id].position)
		if overview:
			var at := p
			for dy in [0,-24,24,-48,48,-72,72]:
				var placed := false
				for dx in [0,24,-24,48,-48]:
					var candidate := Rect2(p+Vector2(dx,dy)-Vector2(10,10),Vector2(20,27))
					if not AREA.encloses(candidate) or obstacles.any(func(o):return candidate.intersects(o)): continue
					at=p+Vector2(dx,dy)
					placed=true
					break
				if placed: break
			markers.append({"id":u.id,"at":at,"anchor":p,"side":u.side,"kind":u.kind,"hp":u.hp,"max_hp":u.max_hp,"radius":MARKER_RADIUS})
			obstacles.append(Rect2(at-Vector2(10,10),Vector2(20,27)))
		else:
			obstacles.append(Rect2(p-Vector2(34,98)*zoom_value,Vector2(68,108)*zoom_value))
	if not overview:
		# Proxy bounds of important authored props; don't print over trees/banner.
		for prop in battle.props:
			var p := screen(prop.position)
			obstacles.append(Rect2(p-Vector2(42,155)*zoom_value,Vector2(84,165)*zoom_value))
		for u in alive:
			if not battle.actors.has(u.id): continue
			var p := screen(battle.actors[u.id].position)
			if not Rect2(0,220,1280,320).has_point(p-Vector2(0,48)*zoom_value): continue
			var kind: String = {"melee":"M","ranged":"BOW","mobile":"BOOT","knight":"×","leader":"◆"}[u.kind]
			var hp_text: String = battle.actors[u.id].get_node("HP").text
			place(u.id,"%s %s" % [kind,hp_text],p-Vector2(0,98)*zoom_value,battle.TEAL if u.side=="ally" else battle.CLAY,84)
	else:
		var groups := {}
		for u in alive:
			if not groups.has(u.group): groups[u.group]={"sum":Vector2.ZERO,"count":0,"ally":u.side=="ally"}
			groups[u.group].sum+=screen(battle.center(u.cell))
			groups[u.group].count+=1
		for group in groups:
			var g: Dictionary = groups[group]
			place(group,"%s ×%d" % [group,g.count],g.sum/g.count,battle.TEAL if g.ally else battle.CLAY,144)
	var entries: Array = battle.hud.warning_entries()
	if not entries.is_empty(): place("wave","T%d 增援 ×3" % battle.state.level.reinforcement_turn,screen(battle.center(entries[1])),Color(battle.BRASS,.8),112)

func _process(_delta: float) -> void:
	refresh_layout()
	queue_redraw()

func _draw() -> void:
	for marker in markers:
		var p: Vector2 = marker.at
		var r: float = marker.radius
		var color: Color = battle.TEAL if marker.side=="ally" else battle.CLAY
		if marker.at!=marker.anchor: draw_line(marker.anchor,marker.at,Color(color,.45),1,true)
		if marker.kind=="leader": draw_colored_polygon(PackedVector2Array([p+Vector2(0,-r-2),p+Vector2(r+2,0),p+Vector2(0,r+2),p-Vector2(r+2,0)]),battle.BRASS)
		elif marker.side=="ally": draw_rect(Rect2(p-Vector2(r,r),Vector2.ONE*r*2),color)
		else: draw_colored_polygon(PackedVector2Array([p+Vector2(0,-r),p+Vector2(r,r),p+Vector2(-r,r)]),color)
		for i in range(4): draw_rect(Rect2(p+Vector2(-8+i*4,11),Vector2(3,3)),color if float(marker.hp)/marker.max_hp>i/4.0 else Color("343e39"))
	for item in items:
		draw_line(item.anchor,item.rect.get_center(),Color(item.color,.4),1,true)
		draw_rect(item.rect,Color("14201f"))
		draw_rect(item.rect,item.color*.7,false,1)
		draw_string(battle.hud.root.theme.default_font,item.rect.position+Vector2(5,16),item.text,HORIZONTAL_ALIGNMENT_LEFT,item.rect.size.x-10,15 if battle.camera.overview else 13,item.color)
