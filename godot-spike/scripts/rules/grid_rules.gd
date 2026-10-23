extends RefCounted
## Independent spike model. Inputs are never mutated; playback only consumes events.
## Forest (F) is walkable in the source. There is no wall tile in this map.

const ROWS = [
	"FFF.~~.....", "FF..~~.....", "F...~~..F..", "....~~.....",
	"...RRRRRR..", "....~~.....", "....~~...FF", "....~~..FFF", "....~~.FFFF",
]
const SPIKE = {"thoma_hp": 8, "knight_hp": 6, "damage": 2, "impact_bonus": 0}
const DIRECTIONS = [Vector2i.UP, Vector2i.LEFT, Vector2i.RIGHT, Vector2i.DOWN]

static func walkable(cell: Vector2i) -> bool:
	return cell.x >= 0 and cell.x < 11 and cell.y >= 0 and cell.y < 9 \
		and ROWS[cell.y][cell.x] != "~" \
		and not (cell.y == 4 and cell.x in [4, 5])

static func unit(id: String, side: String, cell: Vector2i, hp: int) -> Dictionary:
	return {"id": id, "side": side, "cell": cell, "hp": hp, "max_hp": hp}

static func setup(index: int) -> Array:
	var a := Vector2i(1, 4) if index != 2 else Vector2i(2, 4)
	var b := Vector2i(1, 5) if index != 2 else Vector2i(3, 4)
	return [unit("thoma", "ally", a, SPIKE.thoma_hp),
		unit("knight-1", "enemy", b, SPIKE.knight_hp),
		unit("knight-2", "enemy", Vector2i(1, 6) if index == 1 else Vector2i(3, 8), SPIKE.knight_hp)]

static func find_unit(units: Array, id: String) -> Dictionary:
	for actor in units:
		if actor.id == id:
			return actor
	return {}

static func occupant(units: Array, cell: Vector2i, except_id: String = "") -> Dictionary:
	for actor in units:
		if actor.id != except_id and actor.hp > 0 and actor.cell == cell:
			return actor
	return {}

static func reject(units: Array, reason: String) -> Dictionary:
	return {"ok": false, "units": units.duplicate(true), "events": [], "reason": reason}

static func move(units: Array, id: String, to: Vector2i) -> Dictionary:
	var actor := find_unit(units, id)
	if actor.is_empty() or actor.hp <= 0 or not walkable(to) or not occupant(units, to, id).is_empty():
		return reject(units, "illegal-move")
	if actor.cell == to:
		return reject(units, "already-there")
	var queue: Array = [[actor.cell]]
	var seen: Dictionary = {actor.cell: true}
	var cursor := 0
	while cursor < queue.size():
		var path: Array = queue[cursor]
		cursor += 1
		var here: Vector2i = path.back()
		if here == to:
			var next := units.duplicate(true)
			find_unit(next, id).cell = to
			return {"ok": true, "units": next, "events": [{"type": "move", "unit": id, "path": path}]}
		for direction in DIRECTIONS:
			var cell: Vector2i = here + direction
			if seen.has(cell) or not walkable(cell) or not occupant(units, cell, id).is_empty():
				continue
			seen[cell] = true
			queue.append(path + [cell])
	return reject(units, "unreachable")

static func attack(units: Array, attacker_id: String, target_id: String) -> Dictionary:
	var attacker := find_unit(units, attacker_id)
	var target := find_unit(units, target_id)
	if attacker.is_empty() or target.is_empty():
		return reject(units, "missing-unit")
	if attacker.hp <= 0 or target.hp <= 0 or attacker.side == target.side:
		return reject(units, "invalid-combatants")
	var direction: Vector2i = target.cell - attacker.cell
	if absi(direction.x) + absi(direction.y) != 1:
		return reject(units, "not-adjacent")
	var next := units.duplicate(true)
	var victim := find_unit(next, target_id)
	var amount: int = mini(SPIKE.damage, victim.hp)
	victim.hp -= amount
	var into: Vector2i = target.cell + direction
	var events: Array = [
		{"type": "attack", "unit": attacker_id, "target": target_id},
		{"type": "damage", "unit": target_id, "amount": amount, "hp_after": victim.hp},
	]
	var blocker := occupant(units, into, target_id)
	if not walkable(into):
		events.append({"type": "knockback_blocked", "unit": target_id, "from": target.cell, "into": into, "blocker": "terrain"})
	elif not blocker.is_empty():
		events.append({"type": "knockback_blocked", "unit": target_id, "from": target.cell, "into": into, "blocker": "unit", "blocker_id": blocker.id})
	else:
		victim.cell = into
		events.append({"type": "knockback", "unit": target_id, "from": target.cell, "to": into})
	return {"ok": true, "units": next, "events": events}
