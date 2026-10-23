extends "res://addons/gut/test.gd"

const Scene = preload("res://scenes/Skirmish.tscn")
var scene

func before_each() -> void:
	scene = add_child_autofree(Scene.instantiate())
	await get_tree().process_frame

func run_and_observe(index: int, reduced: bool) -> Dictionary:
	scene.select_setup(index)
	scene.motion_button.button_pressed = reduced
	var phases: Array = []
	var times: Dictionary = {}
	var listener = func(value: String):
		phases.append(value)
		times[value] = Time.get_ticks_usec()
	scene.phase_changed.connect(listener)
	scene.play_attack()
	assert_true(scene.busy)
	# Spam cannot re-resolve, reset a setup, or toggle reduced motion mid-flight.
	scene.play_attack()
	scene.select_setup((index+1)%3)
	assert_eq(scene.setup_index, index)
	assert_true(scene.action_button.disabled)
	assert_true(scene.motion_button.disabled)
	var target_start: Vector2 = scene.center(scene.units[1].cell)
	var max_displacement := 0.0
	var max_shake := 0.0
	var max_flash := 0.0
	var deadline := Time.get_ticks_msec() + 2400
	while scene.busy and Time.get_ticks_msec() < deadline:
		max_displacement = maxf(max_displacement, scene.actors["knight-1"].position.distance_to(target_start))
		max_shake = maxf(max_shake, scene.camera.offset.length())
		max_flash = maxf(max_flash, scene.actors["knight-1"].get_node("Body").material.get_shader_parameter("flash"))
		await get_tree().process_frame
	assert_false(scene.busy, "Sequence has a watchdog; no stuck lock")
	assert_lt(scene.last_elapsed, 1.7, "Measured wall time INCLUDES 80ms local hitstop")
	assert_eq(scene.units[1].hp, 4, "Exactly one resolution despite spam")
	assert_eq(scene.actors["knight-1"].position, scene.center(scene.units[1].cell))
	assert_eq(scene.actors.thoma.position, scene.center(scene.units[0].cell))
	assert_eq(scene.actors.thoma.rotation, 0.0)
	assert_eq(scene.camera.offset, Vector2.ZERO)
	assert_eq(Engine.time_scale, 1.0)
	assert_false(scene.action_button.disabled)
	assert_eq(phases, ["windup", "lunge", "contact", "knockback", "settled", "ready"] if index == 0 else ["windup", "lunge", "contact", "blocked", "blocked_recoil", "settled", "ready"])
	var reaction_phase := "knockback" if index == 0 else "blocked"
	var hold: float = (times[reaction_phase] - times.contact) / 1000000.0
	assert_gte(hold, 0.07, "Real-time local contact hold is about 80ms")
	assert_lt(hold, 0.16)
	if index != 0:
		assert_lte(max_displacement, 6.01, "Blocked target never crosses into blocker")
	if reduced:
		assert_eq(max_shake, 0.0)
		assert_eq(max_flash, 0.0)
	else:
		assert_gt(max_shake, 0.0)
		assert_eq(max_flash, 1.0)
	scene.phase_changed.disconnect(listener)
	return {"phases": phases, "hold": hold}

func test_all_three_normal_sequences_and_replay() -> void:
	for index in range(3):
		await run_and_observe(index, false)
	# Replay current scenario must reset health before resolving again.
	await run_and_observe(2, false)

func test_all_three_reduced_motion_sequences() -> void:
	for index in range(3):
		await run_and_observe(index, true)

func test_keyboard_controls_and_diagnostic_default() -> void:
	assert_false(scene.diagnostic)
	for key in [KEY_2, KEY_G, KEY_M]:
		var event := InputEventKey.new()
		event.keycode = key
		event.pressed = true
		scene._unhandled_key_input(event)
	assert_eq(scene.setup_index, 1)
	assert_true(scene.diagnostic)
	assert_true(scene.reduced_motion)
	var replay := InputEventKey.new()
	replay.keycode = KEY_R
	replay.pressed = true
	scene._unhandled_key_input(replay)
	assert_true(scene.busy)
	await scene.attack_finished
	await get_tree().process_frame
	assert_eq(scene.units[1].hp, 4)
