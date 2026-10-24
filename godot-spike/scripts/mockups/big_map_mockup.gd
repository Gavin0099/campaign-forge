extends Node2D
## THROWAWAY scale/camera study. No rules, real level, battle HUD or game reference.
## Terrain and placements are decorative MOCKUP data, never walkability/objectives.
const COLS = 32
const ROWS = 24
const BONE = Color("eee7d6")
const BRASS = Color("d2b777")
const TEAL = Color("98c9be")
const CLAY = Color("dd9c7e")
const ZOOM_STEPS = [0.8,1.0,1.2,1.5]
const UNIT_CELLS = [Vector2i(8,10),Vector2i(9,10),Vector2i(8,11),Vector2i(10,10),
	Vector2i(14,10),Vector2i(15,10),Vector2i(21,13),Vector2i(22,13),Vector2i(22,14),
	Vector2i(25,6),Vector2i(7,19),Vector2i(27,19)]
var tile_width := 160.0
var camera: Camera2D
var unit_root: Node2D
var overlay: Control
var metrics: Label
var caption: Label
var minimap: Control
var interactive_camera := true
var edge_scroll := true
var dragging := false
var overview := false
var zoom_index := 1
var pan_speed := 620.0
var edge_margin := 16.0
var terrain_texture: Texture2D = preload("res://art/battlefield.png")

func half_tile() -> Vector2:
	return Vector2(tile_width/2,tile_width*26.0/44.0/2)

func corner(x: float, y: float) -> Vector2:
	var half := half_tile()
	return Vector2(ROWS*half.x+(x-y)*half.x,(x+y)*half.y)

func cell_center(cell: Vector2i) -> Vector2:
	return corner(cell.x,cell.y)+Vector2(0,half_tile().y)

func world_bounds() -> Rect2:
	return Rect2(Vector2.ZERO,half_tile()*(COLS+ROWS))

func clamp_position(at: Vector2) -> Vector2:
	var half_view := get_viewport_rect().size/camera.zoom/2
	var bounds := world_bounds()
	var result := at
	for axis in range(2):
		result[axis] = bounds.get_center()[axis] if half_view[axis]*2 >= bounds.size[axis] else clampf(at[axis],bounds.position[axis]+half_view[axis],bounds.end[axis]-half_view[axis])
	return result

func pan_to(at: Vector2) -> void:
	camera.position = clamp_position(at)
	camera.force_update_scroll()
	if is_instance_valid(minimap): minimap.queue_redraw()

func _ready() -> void:
	camera = Camera2D.new()
	add_child(camera)
	unit_root = Node2D.new()
	add_child(unit_root)
	build_units()
	build_overlay()
	pan_to(cell_center(UNIT_CELLS[0]))
	queue_redraw()

func build_units() -> void:
	for node in unit_root.get_children(): node.free()
	for i in range(UNIT_CELLS.size()):
		var actor := Node2D.new()
		actor.position = cell_center(UNIT_CELLS[i])
		actor.z_index = int(actor.position.y)
		unit_root.add_child(actor)
		var shadow := Polygon2D.new()
		var points := PackedVector2Array()
		for j in range(24): points.append(Vector2(cos(j*TAU/24)*tile_width*0.18,sin(j*TAU/24)*tile_width*0.06))
		shadow.polygon = points
		shadow.color = Color(Color("101a19"),0.65)
		actor.add_child(shadow)
		var body := Sprite2D.new()
		var character: String = "thoma" if i<4 else ("knight-a" if i%2==0 else "knight-b")
		body.texture = load("res://art/anim-shared/"+character+"/idle/"+("01.png" if character=="thoma" else "00.png"))
		body.centered = false
		body.scale = Vector2.ONE*(tile_width*0.6/360.0)
		body.position = -Vector2(256,464)*body.scale
		body.flip_h = i>=4
		actor.add_child(body)
		var badge := Line2D.new()
		badge.points = PackedVector2Array([Vector2(-tile_width*0.15,8),Vector2(tile_width*0.15,8)])
		badge.default_color = TEAL if i<4 else CLAY
		badge.width = 3
		actor.add_child(badge)

func set_tile_width(value: float) -> void:
	tile_width = value
	build_units()
	queue_redraw()
	set_overview(false)
	pan_to(cell_center(UNIT_CELLS[0]))

func set_overview(value: bool) -> void:
	overview = value
	if overview:
		var bounds := world_bounds()
		camera.zoom = Vector2.ONE*minf(1184/bounds.size.x,500/bounds.size.y)
		pan_to(bounds.get_center())
	else:
		camera.zoom = Vector2.ONE*ZOOM_STEPS[zoom_index]
		pan_to(camera.position)

func terrain(x: int, y: int) -> String:
	var river := 15+int(round(sin(y*0.35)*2))
	if absi(x-river)<=1:
		return "bridge" if y in [10,18] else "water"
	if y in [10,18] or x==8: return "road"
	if (x*7+y*3)%19<4: return "forest"
	return "ground"

func _draw() -> void:
	var half := half_tile()
	for y in range(ROWS):
		for x in range(COLS):
			var p := corner(x,y)
			var points := PackedVector2Array([p,p+half,p+Vector2(0,half.y*2),p+Vector2(-half.x,half.y)])
			var kind := terrain(x,y)
			var color := Color("9a9975")
			match kind:
				"water": color = Color("334d50")
				"bridge": color = Color("8d7953")
				"road": color = Color("c8b788")
				"forest": color = Color("66765a")
			color = color.lightened(float((x*13+y*7)%7)*0.012)
			if kind=="water":
				draw_colored_polygon(points,color)
				draw_line(p+Vector2(-half.x*0.3,half.y),p+Vector2(half.x*0.4,half.y),Color(Color("799c9c"),0.5),1)
			else:
				# Sample one small earth patch from our existing painting. UVs are
				# decorative texture only; no inferred terrain or copied new assets.
				var uv_rect := Rect2(Vector2(310,180)/terrain_texture.get_size(),Vector2(80,55)/terrain_texture.get_size())
				var uvs := PackedVector2Array([uv_rect.position+Vector2(uv_rect.size.x/2,0),uv_rect.position+Vector2(uv_rect.size.x,uv_rect.size.y/2),uv_rect.position+Vector2(uv_rect.size.x/2,uv_rect.size.y),uv_rect.position+Vector2(0,uv_rect.size.y/2)])
				draw_polygon(points,PackedColorArray([color]),uvs,terrain_texture)
			var closed := points.duplicate()
			closed.append(points[0])
			draw_polyline(closed,Color(Color("b5b195"),0.35),1,true)
			if kind=="bridge":
				for j in range(1,5):
					var at := p+Vector2(0,half.y*float(j)/3)
					draw_line(at+Vector2(-half.x*0.35,0),at+Vector2(half.x*0.35,0),Color(Color("e1c798"),0.55),2)
	# Coordinate axes are reference marks, not actionable tactical UI.
	for x in range(0,COLS,4):
		var at := cell_center(Vector2i(x,0))
		draw_circle(at,3,BRASS)

func make_label(parent: Node, text: String, at: Vector2, font_size: int, color: Color = BONE) -> Label:
	var label := Label.new()
	label.text = text
	label.position = at
	label.add_theme_font_size_override("font_size",font_size)
	label.add_theme_color_override("font_color",color)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(label)
	return label

func build_overlay() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)
	overlay = Control.new()
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var theme := Theme.new()
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei","Noto Sans TC","PingFang TC"])
	theme.default_font = font
	overlay.theme = theme
	canvas.add_child(overlay)
	for rect in [Rect2(0,0,1280,76),Rect2(0,608,1280,112)]:
		var panel := ColorRect.new()
		panel.color = Color(Color("101a19"),0.97)
		panel.position = rect.position
		panel.size = rect.size
		panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
		overlay.add_child(panel)
	make_label(overlay,"MOCKUP  /  戰場尺度研究",Vector2(28,12),26,BRASS)
	make_label(overlay,"32 × 24  ·  768 格  ·  裝飾地形／固定站位，沒有戰鬥規則",Vector2(30,48),14)
	metrics = make_label(overlay,"",Vector2(740,16),18,TEAL)
	caption = make_label(overlay,"部署近景 / 非正式關卡",Vector2(28,620),23,BRASS)
	make_label(overlay,"WASD／方向鍵　移鏡頭　·　中鍵拖曳　·　滾輪縮放　·　F／Home 回到單位",Vector2(28,657),16)
	make_label(overlay,"1／2／3　128／160／192 px　·　O 全圖　·　E 邊緣捲動　·　Esc 離開",Vector2(28,683),14)
	minimap = Control.new()
	minimap.position = Vector2(1056,616)
	minimap.size = Vector2(196,94)
	minimap.clip_contents = true
	minimap.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(minimap)
	minimap.draw.connect(draw_minimap)

func draw_minimap() -> void:
	var bounds := world_bounds()
	var factor: float = minf(minimap.size.x/bounds.size.x,minimap.size.y/bounds.size.y)
	var offset: Vector2 = (minimap.size-bounds.size*factor)/2
	minimap.draw_rect(Rect2(Vector2.ZERO,minimap.size),Color("1f2b28"))
	var outline := PackedVector2Array()
	for p in [corner(0,0),corner(COLS,0),corner(COLS,ROWS),corner(0,ROWS)]: outline.append(p*factor+offset)
	minimap.draw_colored_polygon(outline,Color("5a6552"))
	for i in range(UNIT_CELLS.size()):
		minimap.draw_circle(offset+cell_center(UNIT_CELLS[i])*factor,2,TEAL if i<4 else CLAY)
	var visible_size := get_viewport_rect().size/camera.zoom
	minimap.draw_rect(Rect2(offset+(camera.position-visible_size/2)*factor,visible_size*factor),BRASS,false,1)

func _process(delta: float) -> void:
	if interactive_camera and not dragging:
		var movement := Vector2(float(Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT))-float(Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT)),float(Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN))-float(Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP)))
		var pointer := get_viewport().get_mouse_position()
		var size := get_viewport_rect().size
		if edge_scroll and DisplayServer.window_is_focused() and Rect2(Vector2.ZERO,size).has_point(pointer):
			movement += Vector2(float(pointer.x>size.x-edge_margin)-float(pointer.x<edge_margin),float(pointer.y>size.y-edge_margin)-float(pointer.y<edge_margin))
		if movement.length()>0: pan_to(camera.position+movement.normalized()*pan_speed*delta/camera.zoom.x)
	metrics.text = "格寬 %.0f  /  人物 %.0f px  /  zoom %.2f\n%s  ·  edge %s" % [tile_width,tile_width*0.6,camera.zoom.x,"全圖閱讀" if overview else "局部戰術尺度","ON" if edge_scroll else "OFF"]

func _unhandled_input(event: InputEvent) -> void:
	if not interactive_camera: return
	if event is InputEventMouseButton:
		if event.button_index==MOUSE_BUTTON_MIDDLE: dragging = event.pressed
		if event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP,MOUSE_BUTTON_WHEEL_DOWN]:
			zoom_index = clampi(zoom_index+(1 if event.button_index==MOUSE_BUTTON_WHEEL_UP else -1),0,ZOOM_STEPS.size()-1)
			set_overview(false)
	if event is InputEventMouseMotion and dragging: pan_to(camera.position-event.relative/camera.zoom)

func _unhandled_key_input(event: InputEvent) -> void:
	if not interactive_camera or not event is InputEventKey or not event.pressed or event.echo: return
	match event.keycode:
		KEY_1,KEY_2,KEY_3: set_tile_width([128.0,160.0,192.0][event.keycode-KEY_1])
		KEY_O: set_overview(not overview)
		KEY_F,KEY_HOME:
			set_overview(false)
			pan_to(cell_center(UNIT_CELLS[0]))
		KEY_E: edge_scroll = not edge_scroll
		KEY_ESCAPE: get_tree().quit()
