extends "res://addons/gut/test.gd"
const R = preload("res://scripts/rules/field_rules.gd")
const S = preload("res://scripts/rules/field_sight.gd")

func board() -> Dictionary:
	var s := R.initial()
	for y in range(18): s.level.rows[y]=".".repeat(24)
	s.units=[R.make_unit("thoma","ally","ranged",Vector2i(4,9),"party",s.level),
		R.make_unit("target","enemy","knight",Vector2i(7,9),"front",s.level),
		R.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	return s

func tile(s: Dictionary, p: Vector2i, value: String) -> void:
	s.level.rows[p.y]=s.level.rows[p.y].substr(0,p.x)+value+s.level.rows[p.y].substr(p.x+1)

func test_clear_range_limits_and_no_input_mutation() -> void:
	var s := board()
	var before := s.duplicate(true)
	assert_true(R.attack_info(s,s.units[0],s.units[1]).legal)
	assert_eq(R.attack(s,"thoma","target").events[1].amount,2)
	assert_eq(s,before)
	for d in [1,2,3,4]:
		s.units[1].cell=Vector2i(4+d,9)
		assert_eq(R.targets(s,"thoma").has("target"),d in [2,3])

func test_cliff_deep_water_and_unit_between_block_but_endpoint_is_not_blocker() -> void:
	var s := board()
	for terrain_type in ["^","~"]:
		tile(s,Vector2i(5,9),terrain_type)
		assert_false(R.attack(s,"thoma","target").ok)
		assert_false(R.targets(s,"thoma").has("target"))
	tile(s,Vector2i(5,9),".")
	s.units.append(R.make_unit("blocker","ally","melee",Vector2i(6,9),"party",s.level))
	assert_false(R.attack_info(s,s.units[0],s.units[1]).legal)
	s.units.back().hp=0
	assert_true(R.attack_info(s,s.units[0],s.units[1]).legal)
	tile(s,Vector2i(7,9),"^")
	assert_true(R.attack_info(s,s.units[0],s.units[1]).legal,"only intermediate hard terrain blocks")

func test_forest_line_or_target_cover_is_deterministic_one_damage_minimum() -> void:
	var s := board()
	for p in [Vector2i(5,9),Vector2i(7,9)]:
		tile(s,p,"f")
		var info := R.attack_info(s,s.units[0],s.units[1])
		assert_true(info.cover)
		assert_eq(info.damage,1)
		assert_eq(R.attack(s,"thoma","target").events[1].amount,1)
	s.level.stats.ranged.damage=1
	assert_eq(R.attack_info(s,s.units[0],s.units[1]).damage,1)

func test_exact_corner_checks_both_sides_symmetrically() -> void:
	var s := board()
	s.units[1].cell=Vector2i(5,10)
	assert_eq(S.cells(Vector2i(4,9),Vector2i(5,10)),[Vector2i(5,9),Vector2i(4,10)])
	for p in [Vector2i(5,9),Vector2i(4,10)]:
		tile(s,p,"^")
		assert_false(S.check(s,s.units[0],s.units[1]).clear)
		assert_false(S.check(s,s.units[1],s.units[0]).clear)
		tile(s,p,".")
	assert_true(R.attack_info(s,s.units[0],s.units[1]).legal)

func test_threat_and_preview_agree_on_stationary_ranged_blocked_and_cover() -> void:
	var s := board()
	s.level.stats.ranged.move=0
	assert_has(R.threat(s,"thoma"),Vector2i(7,9))
	tile(s,Vector2i(5,9),"^")
	assert_false(R.threat(s,"thoma").has(Vector2i(7,9)))
	assert_false(R.attack_info(s,s.units[0],s.units[1]).legal)
	tile(s,Vector2i(5,9),"f")
	assert_has(R.threat(s,"thoma"),Vector2i(7,9))
	assert_true(R.attack_info(s,s.units[0],s.units[1]).cover)

func test_enemy_ranged_and_policy_use_same_los() -> void:
	var s := board()
	s.units[1].kind="ranged"
	s.phase="enemy"
	tile(s,Vector2i(5,9),"^")
	assert_false(R.attack(s,"target","thoma").ok)
	assert_true(R.targets(s,"target").is_empty())
