extends "res://addons/gut/test.gd"
const Rules = preload("res://scripts/rules/field_rules.gd")

func fixture(kind: String = "melee") -> Dictionary:
	var s := Rules.initial()
	for y in range(18): s.level.rows[y]=".".repeat(24)
	s.units=[Rules.make_unit("thoma","ally",kind,Vector2i(3,9),"party",s.level),
		Rules.make_unit("knight","enemy","knight",Vector2i(4,9),"front",s.level),
		Rules.make_unit("leader","enemy","leader",Vector2i(20,9),"leader",s.level)]
	return s

func test_map_dimensions_costs_paths_and_party() -> void:
	var s := Rules.initial()
	assert_eq(s.level.size,Vector2i(24,18))
	assert_eq(s.level.rows.size(),18)
	for row in s.level.rows: assert_eq(row.length(),24)
	assert_eq(s.units.filter(func(u): return u.side=="ally").size(),6)
	assert_eq(s.units.filter(func(u): return u.side=="enemy").size(),12)
	assert_eq(Rules.cost(s.level,Vector2i(15,5),"melee"),2)
	assert_eq(Rules.cost(s.level,Vector2i(15,8),"melee"),0)
	assert_eq(Rules.cost(s.level,Vector2i(15,9),"melee"),1)
	for u in s.units: assert_gt(Rules.cost(s.level,u.cell,u.kind),0,u.id)
	# Empty-board route to the leader and the northern flank are both reachable.
	s.units=[s.units[0],s.units.back()]
	var nav := Rules.reach(s,"thoma",100)
	assert_has(nav.costs,Vector2i(19,9))
	assert_has(nav.costs,Vector2i(16,5))
	assert_between(Rules.distance(Vector2i(3,9),Vector2i(14,9)),8,15)

func test_archetype_ranges_and_terrain_costs() -> void:
	for kind in ["melee","ranged","mobile"]:
		var s := fixture(kind)
		s.units[1].cell=Vector2i(22,15)
		var budget: int = s.level.stats[kind].move
		assert_true(Rules.move(s,"thoma",Vector2i(3+budget,9)).ok)
		assert_false(Rules.move(s,"thoma",Vector2i(4+budget,9)).ok)
		s.level.rows[9]="...f"+".".repeat(20)
		assert_eq(Rules.cost(s.level,Vector2i(3,9),kind),3 if kind=="mobile" else 2)
		var nav := Rules.reach(s,"thoma")
		for p in nav.costs: assert_lte(int(nav.costs[p]),budget)

func test_ranged_min_max_no_adjacent_no_knockback() -> void:
	var s := fixture("ranged")
	for d in range(1,5):
		s.units[1].cell=Vector2i(3+d,9)
		var hit := Rules.attack(s,"thoma","knight")
		assert_eq(hit.ok,d in [2,3])
		if hit.ok:
			assert_eq(hit.events.size(),2)
			assert_eq(Rules.unit(hit.state,"knight").cell,s.units[1].cell)
			assert_eq(Rules.unit(hit.state,"knight").hp,4)

func test_melee_knockback_and_both_blockers_match_small_semantics() -> void:
	var s := fixture()
	var hit := Rules.attack(s,"thoma","knight")
	assert_eq(hit.events.map(func(e): return e.type),["attack","damage","knockback"])
	assert_eq(Rules.unit(hit.state,"knight").cell,Vector2i(5,9))
	assert_eq(Rules.unit(hit.state,"knight").hp,4)
	s.units.append(Rules.make_unit("blocker","enemy","knight",Vector2i(5,9),"front",s.level))
	hit=Rules.attack(s,"thoma","knight")
	assert_eq(hit.events[2].blocker,"unit")
	assert_eq(hit.events[2].blocker_id,"blocker")
	assert_eq(Rules.unit(hit.state,"knight").cell,Vector2i(4,9))
	s.units.pop_back()
	s.level.rows[9]=".....~"+".".repeat(18)
	hit=Rules.attack(s,"thoma","knight")
	assert_eq(hit.events[2].blocker,"terrain")

func test_move_then_act_once_no_move_after_wait_or_attack() -> void:
	var s := fixture()
	var moved := Rules.move(s,"thoma",Vector2i(3,8))
	assert_true(moved.ok)
	assert_false(Rules.move(moved.state,"thoma",Vector2i(3,7)).ok)
	assert_true(Rules.wait(moved.state,"thoma").ok)
	var waited := Rules.wait(s,"thoma")
	assert_false(Rules.move(waited.state,"thoma",Vector2i(3,8)).ok)
	assert_false(Rules.attack(waited.state,"thoma","knight").ok)
	var hit := Rules.attack(s,"thoma","knight")
	assert_false(Rules.attack(hit.state,"thoma","knight").ok)
	assert_false(Rules.move(hit.state,"thoma",Vector2i(3,8)).ok)

func test_enemy_phase_order_and_next_turn_resets_actions() -> void:
	var s := fixture()
	var resolved := Rules.enemy_phase(s)
	assert_eq(resolved.events[0].type,"phase")
	assert_eq(resolved.events[0].phase,"enemy")
	assert_eq(resolved.events.back().phase,"player")
	assert_eq(resolved.state.turn,2)
	assert_eq(resolved.state.phase,"player")
	assert_false(Rules.unit(resolved.state,"thoma").acted)
	assert_true(resolved.events.any(func(e):return e.type=="attack"))

func test_non_rout_objective_win_and_loss_precedence() -> void:
	var s := fixture()
	s.units[2].cell=Vector2i(3,10)
	s.units[2].hp=2
	var won := Rules.attack(s,"thoma","leader")
	assert_eq(won.state.status,"win")
	assert_gt(Rules.unit(won.state,"knight").hp,0,"surviving opposition does not block win")
	assert_eq(won.events.back().reason,"leader_defeated")
	s=fixture()
	s.units[0].hp=2
	s.phase="enemy"
	var lost := Rules.attack(s,"knight","thoma")
	assert_eq(lost.state.status,"lose")
	assert_eq(lost.events.back().reason,"thoma_falls")
	s=fixture()
	s.turn=s.level.turn_limit
	s.units[1].cell=Vector2i(22,15)
	lost=Rules.enemy_phase(s)
	assert_eq(lost.state.status,"lose")
	assert_eq(lost.events.back().reason,"turn_limit")

func test_reinforcements_warn_one_full_turn_then_arrive_and_rest() -> void:
	var s := fixture()
	s.units[1].cell=Vector2i(22,15)
	s.turn=3
	var warned := Rules.enemy_phase(s)
	var warning: Dictionary = warned.events.filter(func(e):return e.type=="reinforcement_warning")[0]
	assert_eq(warned.state.turn,4)
	assert_gte(int(warning.turn)-int(warning.announced_on),1)
	assert_eq(warning.entries,s.level.entries)
	var arrived := Rules.enemy_phase(warned.state)
	var arrivals: Array = arrived.events.filter(func(e):return e.type=="reinforcement_arrival")
	assert_eq(arrivals.size(),3)
	for i in range(3):
		assert_eq(arrivals[i].turn,warning.turn)
		assert_eq(arrivals[i].cell,warning.entries[i])
		assert_false(arrivals[i].can_act)
	var rest := Rules.enemy_phase(arrived.state)
	for event in rest.events:
		if event.type in ["attack","move","intent"]: assert_false(event.unit.begins_with("reinforcement-"))
	assert_eq(rest.state.turn,6)

func test_occupied_entry_fallback_is_nearest_legal_cell() -> void:
	var s := fixture()
	s.units[1].cell=s.level.entries[0]
	assert_eq(Rules.entry_fallback(s,s.level.entries[0]),Vector2i(23,3))
	assert_eq(Rules.occupant(s,Rules.entry_fallback(s,s.level.entries[0])),{})

func test_ai_guard_group_alert_leader_hold_and_determinism() -> void:
	var s := Rules.initial()
	var before := s.duplicate(true)
	var a := Rules.enemy_phase(s)
	assert_eq(a,Rules.enemy_phase(s))
	assert_eq(s,before)
	assert_false(a.events.any(func(e):return e.type=="move"),"initial distant guards do not chase")
	s.groups.front="alert"
	a=Rules.enemy_phase(s)
	assert_true(a.events.any(func(e):return e.type=="move" and e.unit.begins_with("knight-")))
	assert_eq(Rules.unit(a.state,"leader").cell,Vector2i(20,9))
	s.units[0].cell=Vector2i(18,9)
	a=Rules.enemy_phase(s)
	# W2: explicit leader step-back/counter states replace generic alert.
	assert_true(a.events.any(func(e):return e.type=="intent" and e.unit=="leader" and e.state in ["step-back","counter","leader-hold"]))

func test_distance_map_invalidated_on_occupancy_revision() -> void:
	var s := fixture()
	s.units[1].cell=Vector2i(14,9)
	var cache := {}
	Rules.best_move(s,"thoma",cache)
	var moved := Rules.move(s,"thoma",Vector2i(7,9))
	assert_true(moved.ok)
	Rules.best_move(moved.state,"knight",cache)
	assert_eq(cache.size(),2)
	assert_ne(s.occupancy_revision,moved.state.occupancy_revision)

func test_every_public_command_preserves_inputs_and_rejects_wrong_side() -> void:
	var s := fixture()
	var original := s.duplicate(true)
	Rules.reach(s,"thoma")
	Rules.move(s,"thoma",Vector2i(3,8))
	Rules.attack(s,"thoma","knight")
	Rules.wait(s,"thoma")
	Rules.enemy_phase(s)
	assert_false(Rules.move(s,"knight",Vector2i(4,8)).ok)
	assert_false(Rules.attack(s,"knight","thoma").ok)
	assert_eq(s,original)
