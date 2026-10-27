extends "res://addons/gut/test.gd"
const H = preload("res://tools/field_harness.gd")
const P = preload("res://tools/field_policy.gd")
const D06 = preload("res://data/levels/field_24x18_spike06.gd")
const D = preload("res://data/levels/field_24x18.gd")
const R = preload("res://scripts/rules/field_rules.gd")
func test_fixed_seed_extension_preserves_original_twenty() -> void:
	assert_gte(H.SEEDS.size(),40)
	assert_eq(H.SEEDS.slice(0,20),H.SPIKE06_SEEDS)
	var seen := {}
	for n in H.SEEDS: seen[n]=true
	assert_eq(seen.size(),H.SEEDS.size())
func test_spike06_preserves_baseline_data() -> void:
	# W2 changes default levers; pin the FULL historical data bytes instead.
	assert_eq(FileAccess.get_file_as_string("res://data/levels/field_24x18_spike06.gd").replace("\r\n","\n").sha256_text(),"b206af4e2ce5da16756f112aa30aac6bb55203e2437ccbf3a9ef7bcdb004d6d5")
	assert_eq(P.start("road",1014,"spike06").level.stats,D06.STATS)
func test_leader_dash_deterministic_from_real_deployment() -> void:
	var s := P.start("leader-dash",1014,"spike06")
	assert_eq(s.turn,1)
	assert_eq(s.units[0].cell,D06.DEPLOYMENT[0][3])
	assert_eq(P.command(s,"thoma","leader-dash"),P.command(s,"thoma","leader-dash"))

func test_minimal_data_levers_keep_all_fixed_contracts() -> void:
	var a := D06.build()
	var b := D.build()
	for key in ["stats","rows","terrain","size","scout_kit","ai","turn_limit","objective","entries","reinforcement_kinds","alert_radius","line_of_sight"]: assert_eq(a[key],b[key])
	for i in range(a.deployment.size()-1): assert_eq(a.deployment[i],b.deployment[i])
	assert_eq(b.hold_point,Vector2i(22,9))
	var s := R.initial(b)
	var before := s.duplicate(true)
	for u in s.units: assert_gt(R.cost(s.level,u.cell,u.kind),0)
	s.units=[s.units[0]]
	var paths := R.reach(s,"thoma",200)
	assert_has(paths.costs,Vector2i(21,9))
	for p in b.entries: assert_has(paths.costs,p)
	assert_eq(before,R.initial(b))

func test_warning_birth_rest_and_immutable_deterministic_wave() -> void:
	var s := R.initial()
	s.turn=1
	var before := s.duplicate(true)
	var warning := R.next_turn(s)
	var e: Dictionary = warning.events.filter(func(v):return v.type=="reinforcement_warning")[0]
	assert_lt(e.announced_on,e.turn)
	assert_eq(e.turn,3)
	var arrival := R.next_turn(warning.state)
	assert_eq(arrival,R.next_turn(warning.state))
	assert_eq(s,before)
	for u in arrival.state.units:
		if u.group=="reinforcements": assert_false(R.allowed(arrival.state,u))

func test_bypass_and_real_dash_counterexamples_closed() -> void:
	for name in ["bypass","leader-dash"]:
		var r := H.run(name,1014,"default")
		assert_false(r.bypass_win)
		assert_eq(r.illegal_commands,[])
	var old := H.run("bypass",1014,"spike06")
	assert_true(old.bypass_win)
	assert_eq(old.turns_to_result,6)
	assert_eq(old.ally_deaths,[])

func safety_fixture() -> Dictionary:
	var s := R.initial()
	for y in range(18): s.level.rows[y]=".".repeat(24)
	s.turn=3
	s.units=[R.make_unit("thoma","ally","melee",Vector2i(2,9),"party",s.level),R.make_unit("scout","ally","mobile",Vector2i(5,8),"party",s.level),R.make_unit("foe","enemy","knight",Vector2i(9,8),"front",s.level),R.make_unit("leader","enemy","leader",Vector2i(22,9),"leader",s.level)]
	s.units[1].hp=2
	return s

func test_early_exposure_prefers_safe_position_and_preserves_input() -> void:
	var s := safety_fixture()
	var before := s.duplicate(true)
	var threats := P.scout_threat_counts(s,"scout")
	assert_gte(threats.get(Vector2i(5,8),0),1)
	assert_eq(threats.get(Vector2i(3,8),0),0)
	var command := P.command(s,"scout","flank")
	assert_eq(command.type,"move")
	assert_eq(threats.get(command.to,0),0)
	assert_eq(command,P.command(s,"scout","flank"))
	assert_eq(s,before)

func test_safe_retreat_respects_two_weighted_cost_and_total_six() -> void:
	var s := safety_fixture()
	s.units[1].acted=true
	s.units[1].moved=true
	s.units[1].retreat_left=2
	s.units[1].move_spent=4
	var before := s.duplicate(true)
	var command := P.escape_command(s,"scout")
	assert_eq(command.type,"move")
	assert_lte(int(R.reach(s,"scout").costs[command.to]),2)
	assert_eq(P.scout_threat_counts(s,"scout").get(command.to,0),0)
	var moved := R.move(s,"scout",command.to)
	assert_true(moved.ok)
	assert_lte(int(R.unit(moved.state,"scout").move_spent),6)
	assert_false(R.can_escape(moved.state,R.unit(moved.state,"scout")))
	assert_eq(s,before)
