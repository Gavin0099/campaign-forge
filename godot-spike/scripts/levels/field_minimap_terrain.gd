extends Node2D
## Retained static canvas commands, behind the live markers. No texture baking.
var dimensions := Vector2.ZERO
var polygons: Array = []
var goal := Vector2.ZERO
func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO,dimensions),Color("151d1b"))
	for polygon in polygons: draw_colored_polygon(polygon.points,polygon.color)
	draw_arc(goal,5,0,TAU,16,Color("e7cb88"),1.5)
