extends Control
var battle

func factor() -> float:
	var bounds: Rect2 = battle.world_bounds()
	return minf(size.x/bounds.size.x,size.y/bounds.size.y)

func origin() -> Vector2:
	return (size-battle.world_bounds().size*factor())/2

func world_to_map(world: Vector2) -> Vector2:
	return origin()+(world-battle.world_bounds().position)*factor()

func map_to_world(point: Vector2) -> Vector2:
	return (point-origin())/factor()+battle.world_bounds().position

func viewport_rect() -> Rect2:
	var camera = battle.camera
	var visible_size: Vector2 = camera.VIEW/camera.zoom
	return Rect2(world_to_map(camera.position+camera.offset-visible_size/2),visible_size*factor())

func centre_from_map(point: Vector2) -> void:
	if battle.camera.overview: battle.camera.toggle_overview()
	battle.camera.pan_to(map_to_world(point))

func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index==MOUSE_BUTTON_LEFT:
		centre_from_map(event.position)
		accept_event()

func _draw() -> void:
	if battle==null: return
	draw_rect(Rect2(Vector2.ZERO,size),Color("151d1b"))
	var colors := {".":Color("62634e"),"=":Color("b49a68"),"f":Color("48583c"),"w":Color("81a59a"),"~":Color("334e57"),"^":Color("363b39"),"d":Color("c2ad7c")}
	for y in range(battle.state.level.size.y):
		for x in range(battle.state.level.size.x):
			var cell := Vector2i(x,y)
			var points := PackedVector2Array()
			for p in battle.diamond(cell): points.append(world_to_map(p))
			draw_colored_polygon(points,colors[battle.Rules.terrain(battle.state.level,cell)])
	var goal: Vector2 = world_to_map(battle.center(battle.state.level.hold_point))
	draw_arc(goal,5,0,TAU,16,Color("e7cb88"),1.5)
	for u in battle.state.units:
		if u.hp<=0: continue
		var at: Vector2 = world_to_map(battle.center(u.cell))
		if u.kind=="leader":
			draw_colored_polygon(PackedVector2Array([at+Vector2(0,-5),at+Vector2(5,0),at+Vector2(0,5),at-Vector2(5,0)]),battle.BRASS)
		elif u.side=="ally": draw_rect(Rect2(at-Vector2(2.5,2.5),Vector2(5,5)),battle.TEAL)
		else: draw_colored_polygon(PackedVector2Array([at+Vector2(0,-3),at+Vector2(3,3),at+Vector2(-3,3)]),battle.CLAY)
	var marker: Dictionary = battle.hud.warning_marker()
	if not marker.is_empty():
		var at: Vector2 = world_to_map(battle.center(marker.cell))
		draw_arc(at,3,0,TAU,12,Color(battle.BRASS,.6),1)
	draw_rect(viewport_rect(),battle.BONE,false,1.2)

func _process(_delta: float) -> void:
	queue_redraw() # Camera viewport and actor dots are live presentation.
