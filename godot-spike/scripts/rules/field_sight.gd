extends RefCounted
## SPIKE TEST VALUES. Geometry first used counterfactually by W1 telemetry.
## Centre-to-centre supercover; exact corners visit BOTH side cells, x then y.
static func cells(a: Vector2i, b: Vector2i) -> Array[Vector2i]:
	var found: Array[Vector2i] = []
	var p := a
	var delta := b-a
	var nx := absi(delta.x)
	var ny := absi(delta.y)
	var step := Vector2i(signi(delta.x),signi(delta.y))
	var ix := 0
	var iy := 0
	while ix<nx or iy<ny:
		var decision := (1+2*ix)*ny-(1+2*iy)*nx
		if decision==0:
			found.append(p+Vector2i(step.x,0))
			found.append(p+Vector2i(0,step.y))
			p+=step
			ix+=1
			iy+=1
		elif decision<0:
			p.x+=step.x
			ix+=1
		else:
			p.y+=step.y
			iy+=1
		found.append(p)
	return found.filter(func(c): return c!=a and c!=b)

static func check(s: Dictionary, a: Dictionary, b: Dictionary) -> Dictionary:
	var cover := false
	var crossed := cells(a.cell,b.cell)
	for p in crossed:
		var tile: String = s.level.rows[p.y][p.x]
		if tile in ["^","~"]: return {"clear":false,"cover":false,"reason":"峭壁／深水岸阻擋","cell":p}
		for u in s.units:
			if u.hp>0 and u.id!=a.id and u.id!=b.id and u.cell==p:
				return {"clear":false,"cover":false,"reason":"中間單位阻擋","cell":p}
		if tile=="f": cover=true
	cover=cover or s.level.rows[b.cell.y][b.cell.x]=="f"
	return {"clear":true,"cover":cover,"reason":"森林掩護 −1（最低1）" if cover else "視線暢通"}
