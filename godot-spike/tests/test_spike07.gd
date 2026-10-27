extends "res://addons/gut/test.gd"
const H = preload("res://tools/field_harness.gd")
const P = preload("res://tools/field_policy.gd")
const D06 = preload("res://data/levels/field_24x18_spike06.gd")
const D = preload("res://data/levels/field_24x18.gd")
func test_fixed_seed_extension_preserves_original_twenty() -> void:
	assert_gte(H.SEEDS.size(),40)
	assert_eq(H.SEEDS.slice(0,20),H.SPIKE06_SEEDS)
	var seen := {}
	for n in H.SEEDS: seen[n]=true
	assert_eq(seen.size(),H.SEEDS.size())
func test_spike06_preserves_baseline_data() -> void:
	assert_eq(D06.build(),D.build()) # W2 will pin immutable snapshot against source hash.
	assert_eq(P.start("road",1014,"spike06").level.stats,D06.STATS)
func test_leader_dash_deterministic_from_real_deployment() -> void:
	var s := P.start("leader-dash",1014,"spike06")
	assert_eq(s.turn,1)
	assert_eq(s.units[0].cell,D06.DEPLOYMENT[0][3])
	assert_eq(P.command(s,"thoma","leader-dash"),P.command(s,"thoma","leader-dash"))
