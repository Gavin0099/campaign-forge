extends "res://addons/gut/test.gd"
const H = preload("res://tools/field_harness.gd")
const P = preload("res://tools/field_policy.gd")
func test_fixed_seeds_and_range_parser() -> void:
	assert_eq(H.SEEDS,[24018,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019])
	assert_eq(H.seeds_from("3:5"),[3,4,5])
	assert_eq(H.seeds_from("24018,8"),[24018,8])
func test_same_seed_same_commands_events_and_result() -> void:
	assert_eq(H.run("turtle",1001,"spike05"),H.run("turtle",1001,"spike05"))
func test_default_seed_reproduces_historical_results() -> void:
	for pair in [["road",8],["flank",7],["turtle",6],["scout-retreat",9]]:
		var report := H.run(pair[0],24018,"spike05")
		assert_eq(report.status,"lose")
		assert_eq(report.turns_to_result,pair[1])
		assert_eq(report.illegal_commands,[])
func test_nondefault_seeds_vary_only_equal_class_order() -> void:
	assert_eq(P.order(P.start("road")),["thoma","guard","bow-1","bow-2","scout-1","scout-2"])
	var orders := {}
	for seed_value in H.SEEDS: orders[str(P.order(P.start("road",seed_value)))]=true
	assert_gt(orders.size(),1)
