extends Control
var battle
const SAFE = Rect2(42,156,1196,386)
var items: Array = []

func indicator(world: Vector2) -> Dictionary:
	var cam = battle.camera
	var screen: Vector2 = (world-cam.position-cam.offset)*cam.zoom+cam.VIEW/2
	if SAFE.has_point(screen): return {}
	var middle := SAFE.get_center()
	var delta := screen-middle
	var half := SAFE.size/2-Vector2(18,18)
	var ratio := minf(half.x/maxf(absf(delta.x),.001),half.y/maxf(absf(delta.y),.001))
	var point := middle+delta*ratio
	var rect := Rect2((point-Vector2(62,18)).clamp(SAFE.position,SAFE.end-Vector2(124,36)),Vector2(124,36))
	return {"point":point,"direction":delta.normalized(),"rect":rect,"world":world}

func targets() -> Array:
	var found: Array = []
	var leader: Dictionary = battle.Rules.unit(battle.state,"leader")
	if leader.hp>0: found.append({"world":battle.center(leader.cell),"label":"領袖 ◆","id":"leader"})
	# One labelled representative per threatening group prevents edge-label piles.
	var groups := {}
	for u in battle.state.units:
		if u.side!="enemy" or u.hp<=0 or u.kind=="leader": continue
		var nearest := 999
		for ally in battle.state.units:
			if ally.side=="ally" and ally.hp>0: nearest=mini(nearest,battle.Rules.distance(u.cell,ally.cell))
		if nearest>8: continue
		if not groups.has(u.group): groups[u.group]={"world":battle.center(u.cell),"label":"敵群 "+u.group,"id":u.id,"distance":nearest}
		elif nearest<groups[u.group].distance:
			groups[u.group].world=battle.center(u.cell)
			groups[u.group].distance=nearest
	for group in groups.values(): found.append(group)
	var entries: Array = battle.hud.warning_entries()
	if not entries.is_empty(): found.append({"world":battle.center(entries[0]),"label":"增援 東北 ×3","id":"entry"})
	return found

func refresh_items() -> void:
	items.clear()
	for target in targets():
		var item := indicator(target.world)
		if item.is_empty(): continue
		item.label=target.label
		item.id=target.id
		# Try finite slots until ALL previous rectangles are clear, not just last.
		var placed := false
		for y in range(236,500,40):
			var candidate := Rect2(Vector2(item.rect.position.x,y),item.rect.size)
			if items.any(func(previous):return candidate.grow(3).intersects(previous.rect)): continue
			item.rect=candidate
			item.point=candidate.get_center()
			placed=true
			break
		if placed: items.append(item)

func centre_item(item: Dictionary) -> void:
	if battle.camera.overview: battle.camera.toggle_overview()
	battle.camera.follow(item.world)

func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index==MOUSE_BUTTON_LEFT:
		for item in items:
			if item.rect.has_point(event.position):
				centre_item(item)
				get_viewport().set_input_as_handled()
				return

func _draw() -> void:
	for item in items:
		draw_style_box(get_theme_stylebox("panel","Panel"),item.rect)
		var p: Vector2 = item.point
		var d: Vector2 = item.direction
		draw_colored_polygon(PackedVector2Array([p+d*10,p-d*6+d.orthogonal()*5,p-d*6-d.orthogonal()*5]),battle.BRASS)
		draw_string(get_theme_default_font(),item.rect.position+Vector2(8,24),item.label,HORIZONTAL_ALIGNMENT_LEFT,110,14,battle.BONE)

func _process(_delta: float) -> void:
	refresh_items()
	queue_redraw()
