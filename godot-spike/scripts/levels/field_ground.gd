extends Node2D
## Batched static diamond ground; navigation is read from rules, never pixels.
var battle
var textures := {}
const NAMES = {".":"plain","=":"road","f":"forest","w":"ford","~":"water","^":"cliff","d":"defense"}

func _ready() -> void:
	for tile in NAMES: textures[tile]=load("res://art/bigmap/"+NAMES[tile]+".png")

func _draw() -> void:
	if battle==null: return
	var level: Dictionary = battle.state.level
	for y in range(level.size.y):
		for x in range(level.size.x):
			var cell := Vector2i(x,y)
			var at: Vector2 = battle.center(cell)
			var points: PackedVector2Array = battle.diamond(cell)
			draw_texture_rect(textures[battle.Rules.terrain(level,cell)],Rect2(at-Vector2(80,47.25),Vector2(160,94.5)),false)
			if battle.grid_visible:
				var closed := points.duplicate()
				closed.append(points[0])
				draw_polyline(closed,Color(0.75,0.73,0.58,0.18),1,true)
	for cell in battle.move_cells:
		draw_colored_polygon(battle.diamond(cell),Color(0.45,0.69,0.63,0.28))
	for cell in battle.threat_cells:
		draw_colored_polygon(battle.diamond(cell),Color(0.74,0.34,0.26,0.18))
	for id in battle.attack_targets:
		var target: Dictionary = battle.Rules.unit(battle.state,id)
		draw_colored_polygon(battle.diamond(target.cell),Color(0.85,0.44,0.27,0.38))
	if not battle.preview_path.is_empty():
		var path := PackedVector2Array()
		for cell in battle.preview_path: path.append(battle.center(cell))
		draw_polyline(path,Color("e0c487"),3,true)
	var cursor: PackedVector2Array = battle.diamond(battle.cursor_cell)
	cursor.append(cursor[0])
	draw_polyline(cursor,Color("e9d9b1"),2,true)
