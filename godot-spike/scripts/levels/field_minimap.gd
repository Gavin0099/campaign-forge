extends Control
var battle
var static_layer
var static_key := {}
var static_revision := 0
var cached_bounds := Rect2()
var cached_factor := 1.0
var cached_origin := Vector2.ZERO
func _ready() -> void:
	ensure_geometry()

func ensure_geometry() -> void:
	if battle==null: return
	var bounds: Rect2 = battle.world_bounds()
	var key := {"bounds":bounds,"size":size,"rows":battle.state.level.rows,"goal":battle.state.level.hold_point}
	if static_key==key: return
	static_key=key.duplicate(true)
	cached_bounds=bounds
	cached_factor=minf(size.x/bounds.size.x,size.y/bounds.size.y)
	cached_origin=(size-bounds.size*cached_factor)/2
	if static_layer==null:
		static_layer=preload("res://scripts/levels/field_minimap_terrain.gd").new()
		static_layer.show_behind_parent=true
		add_child(static_layer)
	static_layer.dimensions=size
	static_layer.polygons.clear()
	var colors := {".":Color("62634e"),"=":Color("b49a68"),"f":Color("48583c"),"w":Color("81a59a"),"~":Color("334e57"),"^":Color("363b39"),"d":Color("c2ad7c")}
	for y in range(battle.state.level.size.y):
		for x in range(battle.state.level.size.x):
			var cell := Vector2i(x,y)
			var points := PackedVector2Array()
			for p in battle.diamond(cell): points.append(world_to_map(p))
			static_layer.polygons.append({"points":points,"color":colors[battle.Rules.terrain(battle.state.level,cell)]})
	static_layer.goal=world_to_map(battle.center(battle.state.level.hold_point))
	static_layer.queue_redraw()
	static_revision+=1

func factor() -> float:
	ensure_geometry()
	return cached_factor

func origin() -> Vector2:
	ensure_geometry()
	return cached_origin

func world_to_map(world: Vector2) -> Vector2:
	return cached_origin+(world-cached_bounds.position)*cached_factor

func map_to_world(point: Vector2) -> Vector2:
	ensure_geometry()
	return (point-cached_origin)/cached_factor+cached_bounds.position

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
	ensure_geometry()
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
	ensure_geometry()
	queue_redraw() # Camera viewport and actor dots are live presentation.
