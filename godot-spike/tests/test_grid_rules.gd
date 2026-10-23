extends "res://addons/gut/test.gd"

const Rules = preload("res://scripts/rules/grid_rules.gd")

func test_adjacent_attack_event_order_hp_and_immutability() -> void:
	var state := Rules.setup(0)
	var before := state.duplicate(true)
	var result := Rules.attack(state, "thoma", "knight-1")
	assert_true(result.ok)
	assert_eq(result.events.map(func(e): return e.type), ["attack", "damage", "knockback"])
	assert_eq(result.events[1], {"type": "damage", "unit": "knight-1", "amount": 2, "hp_after": 4})
	assert_eq(result.units[1].hp, state[1].hp - result.events[1].amount)
	assert_eq(result.units[1].cell, Vector2i(1, 6))
	assert_eq(state, before, "Pure resolution must not mutate input dictionaries")

func test_nonadjacent_and_diagonal_attacks_are_rejected() -> void:
	var state := Rules.setup(0)
	state[1].cell = Vector2i(1, 7)
	var result := Rules.attack(state, "thoma", "knight-1")
	assert_false(result.ok)
	assert_eq(result.events, [])
	assert_eq(result.units, state)
	state[1].cell = Vector2i(2, 5)
	assert_false(Rules.attack(state, "thoma", "knight-1").ok)

func test_destroyed_crossing_blocks_knockback() -> void:
	var state := Rules.setup(2)
	var result := Rules.attack(state, "thoma", "knight-1")
	assert_eq(result.events[2], {"type": "knockback_blocked", "unit": "knight-1", "from": Vector2i(3, 4), "into": Vector2i(4, 4), "blocker": "terrain"})
	assert_eq(result.units[1].cell, state[1].cell)
	assert_eq(result.units[1].hp, 4, "No optional impact bonus is used")

func test_water_blocks_knockback() -> void:
	var state := Rules.setup(0)
	state[0].cell = Vector2i(2, 3)
	state[1].cell = Vector2i(3, 3)
	var result := Rules.attack(state, "thoma", "knight-1")
	assert_eq(result.events[2].type, "knockback_blocked")
	assert_eq(result.events[2].blocker, "terrain")
	assert_eq(result.events[2].into, Vector2i(4, 3))
	assert_eq(result.units[1].cell, Vector2i(3, 3))

func test_unit_blocker_preserves_both_positions() -> void:
	var state := Rules.setup(1)
	var result := Rules.attack(state, "thoma", "knight-1")
	assert_eq(result.events.map(func(e): return e.type), ["attack", "damage", "knockback_blocked"])
	assert_eq(result.events[2].blocker, "unit")
	assert_eq(result.events[2].blocker_id, "knight-2")
	assert_eq(result.units[1].cell, state[1].cell)
	assert_eq(result.units[2], state[2])
	assert_ne(result.units[1].cell, result.units[2].cell)

func test_all_four_map_edges_block_knockback() -> void:
	for pair in [[Vector2i(1,1),Vector2i(0,1)], [Vector2i(9,1),Vector2i(10,1)], [Vector2i(2,1),Vector2i(2,0)], [Vector2i(2,7),Vector2i(2,8)]]:
		var state := Rules.setup(0)
		state[0].cell = pair[0]
		state[1].cell = pair[1]
		var result := Rules.attack(state, "thoma", "knight-1")
		assert_eq(result.events[2].type, "knockback_blocked")
		assert_eq(result.events[2].blocker, "terrain")
		assert_eq(result.units[1].cell, pair[1])

func test_open_route_terrain_matches_source_contract() -> void:
	assert_eq(Rules.ROWS.size(), 9)
	for y in range(9):
		assert_eq(Rules.ROWS[y].length(), 11)
		for x in range(11):
			assert_eq(Rules.walkable(Vector2i(x,y)), x not in [4,5], "Open route has two impassable river columns, including the broken crossing")
	assert_true(Rules.walkable(Vector2i(0,0)), "Source forest is passable; do not invent walls")
	for cell in [Vector2i(-1,0),Vector2i(0,-1),Vector2i(11,0),Vector2i(0,9)]:
		assert_false(Rules.walkable(cell))

func test_bfs_detours_without_passing_through_units() -> void:
	var state := Rules.setup(1)
	var result := Rules.move(state, "thoma", Vector2i(1, 7))
	assert_true(result.ok)
	var path: Array = result.events[0].path
	assert_eq(path.front(), Vector2i(1,4))
	assert_eq(path.back(), Vector2i(1,7))
	assert_eq(path.size(), 6, "Shortest detour is five steps")
	assert_eq(path[1], Vector2i(0,4), "Fixed UP LEFT RIGHT DOWN tie order")
	for i in range(1, path.size()):
		assert_true(Rules.walkable(path[i]))
		assert_true(Rules.occupant(state, path[i], "thoma").is_empty())
		var step: Vector2i = path[i] - path[i-1]
		assert_eq(absi(step.x)+absi(step.y), 1)
	assert_eq(state[0].cell, Vector2i(1,4))
	assert_eq(result.units[0].cell, Vector2i(1,7))

func test_invalid_moves_and_disconnected_bank_rejected() -> void:
	var state := Rules.setup(1)
	for cell in [Vector2i(1,5), Vector2i(1,6), Vector2i(4,4), Vector2i(6,4), Vector2i(-1,4), Vector2i(1,4)]:
		var result := Rules.move(state, "thoma", cell)
		assert_false(result.ok)
		assert_eq(result.events, [])
		assert_eq(result.units, state)

func test_invalid_combatants_and_lethal_damage_are_bounded() -> void:
	var state := Rules.setup(0)
	assert_false(Rules.attack(state, "missing", "knight-1").ok)
	assert_false(Rules.attack(state, "thoma", "thoma").ok)
	state[1].hp = 1
	var result := Rules.attack(state, "thoma", "knight-1")
	assert_eq(result.units[1].hp, 0)
	assert_eq(result.events[1].amount, 1)
	assert_false(Rules.attack(result.units, "thoma", "knight-1").ok)
