extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/Skirmish.tscn")
var scene
class UIProbe extends Node:
	var ticks := 0
	func _process(_delta: float) -> void:
		ticks += 1

func before_each() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	scene = add_child_autofree(Scene.instantiate())
	await get_tree().process_frame

func after_each() -> void:
	get_tree().paused = false
	await get_tree().process_frame

func snapshot(probe: Node2D, particle: CPUParticles2D) -> Dictionary:
	var numbers: Array = []
	for child in scene.world.get_children():
		if child is Label: numbers.append([child.position,child.modulate])
	return {"tween":probe.position, "frame":scene.players.thoma.frame_index,
		"frame_ms":scene.players.thoma.frame_time_ms, "target_frame":scene.players["knight-1"].frame_index,
		"target_ms":scene.players["knight-1"].frame_time_ms,
		"particles":particle.processed_seconds, "particle_can_process":particle.can_process(),
		"camera":scene.camera.offset,"zoom":scene.camera.zoom,"camera_position":scene.camera.position,"damage_numbers":numbers}

func test_whole_frame_hitstop_and_ui_progress_over_real_hold() -> void:
	var probe := Node2D.new()
	scene.world.add_child(probe)
	probe.create_tween().tween_property(probe,"position:x",100.0,1.5)
	var particle := preload("res://scripts/anim/world_particles.gd").new()
	scene.world.add_child(particle)
	particle.emitting = true
	var samples: Array = []
	var ui_probe := UIProbe.new()
	ui_probe.process_mode = Node.PROCESS_MODE_ALWAYS
	scene.hud.add_child(ui_probe)
	var stamps: Array = []
	var ui_ticks: Array = []
	var on_start := func():
		samples.append(snapshot(probe,particle))
		stamps.append(Time.get_ticks_usec())
		ui_ticks.append(ui_probe.ticks)
	var on_end := func():
		samples.append(snapshot(probe,particle))
		stamps.append(Time.get_ticks_usec())
		ui_ticks.append(ui_probe.ticks)
	scene.hitstop_started.connect(on_start)
	scene.hitstop_finished.connect(on_end)
	scene.play_attack()
	await scene.hitstop_started
	assert_true(scene.busy)
	assert_true(get_tree().paused)
	# F1 is dispatched while the world is frozen; HUD controls remain responsive.
	var key := InputEventKey.new()
	key.keycode = KEY_F1
	key.pressed = true
	scene._unhandled_key_input(key)
	assert_true(scene.debug_visible)
	assert_true(scene.debug_panel.visible)
	await scene.hitstop_finished
	assert_eq(samples.size(),2)
	assert_eq(samples[0],samples[1],"tween, both frame clocks, particles and camera all frozen")
	assert_false(samples[0].damage_numbers.is_empty(),"real damage number is included in freeze comparison")
	assert_false(samples[1].particle_can_process,"native emitter inherits world pause")
	assert_gte((stamps[1]-stamps[0])/1000.0,79.9,"two snapshots span entire >=80ms hold")
	assert_gte(scene.hold_process_ms,80.0,"pause also covers at least 80ms of process time")
	assert_gt(ui_ticks[1],ui_ticks[0],"always-process UI/root clock advances")
	await get_tree().process_frame
	await get_tree().process_frame
	assert_gt(probe.position.x,samples[1].tween.x,"world tween resumes")
	assert_gt(particle.processed_seconds,samples[1].particles,"particle processing resumes")
	await scene.attack_finished
	await get_tree().process_frame
	assert_false(get_tree().paused)
	assert_false(scene.hold_active)
	assert_eq(scene.camera.offset,Vector2.ZERO)
	assert_eq(scene.camera.zoom,Vector2.ONE)

func test_contact_triggers_share_exact_process_frame() -> void:
	for reduced in [false,true]:
		scene.motion_button.button_pressed = reduced
		scene.play_attack()
		await scene.hitstop_started
		assert_eq(scene.players.thoma.frame_index,3,"contact pose is active at hold onset")
		assert_eq(scene.contact_triggers.size(),3)
		var frame: int = scene.contact_triggers[0].frame
		var types: Array = []
		for trigger in scene.contact_triggers:
			assert_eq(trigger.frame,frame,trigger.type+" same-frame contact")
			types.append(trigger.type)
		assert_has(types,"spark")
		assert_has(types,"sfx")
		assert_has(types,"flash")
		assert_eq(scene.actors["knight-1"].get_node("Body").material.get_shader_parameter("flash"),0.0 if reduced else 1.0)
		assert_eq(scene.camera.offset==Vector2.ZERO,reduced,"shake starts at contact only when enabled")
		await scene.attack_finished
		await get_tree().process_frame

func test_generic_event_dispatch_reordered_and_unknown_event() -> void:
	var result: Dictionary = scene.Rules.attack(scene.units,"thoma","knight-1")
	var events: Array = result.events.duplicate(true)
	events.reverse()
	events.insert(1,{"type":"future_annotation","anything":"ignored"})
	await scene.play_attack(events)
	await get_tree().process_frame
	assert_eq(scene.units[1].hp,4)
	assert_eq(scene.units[1].cell,Vector2i(1,6))
	assert_eq(scene.actors["knight-1"].position,scene.center(Vector2i(1,6)))
	assert_eq(scene.current_plan.unknown.size(),1)
	assert_false(scene.busy)
	assert_eq(scene.contact_triggers.size(),3,"one impact despite transport reorder")

func test_knight_identity_and_debug_visibility() -> void:
	var a: Sprite2D = scene.actors["knight-1"].get_node("Body")
	var b: Sprite2D = scene.actors["knight-2"].get_node("Body")
	assert_ne(a.texture.resource_path,b.texture.resource_path)
	assert_ne(FileAccess.get_sha256(a.texture.resource_path),FileAccess.get_sha256(b.texture.resource_path))
	assert_false(scene.debug_panel.visible)
	for actor in scene.actors.values(): assert_false(actor.get_node("DebugLabel").visible)
	scene.set_debug_visible(true)
	scene.grid_button.button_pressed = true
	scene.set_debug_visible(false)
	assert_false(scene.diagnostic,"grid cannot leak from closed debug panel")
	assert_true(scene.action_button.has_focus())

func test_frame_player_offsets_and_mirror_are_pivot_relative() -> void:
	var player = scene.players.thoma
	player.facing_right = true
	player.play("thoma.swing")
	player.playing = false
	player.enter_frame(3)
	var body: Sprite2D = player.body
	var foot := body.to_global(Vector2(256,464))
	var expected: Vector2 = scene.actors.thoma.position + Vector2(100,220)*player.pixels_per_frame_pixel
	assert_almost_eq(foot,expected,Vector2(0.001,0.001))
	player.facing_right = false
	player.apply_frame()
	foot = body.to_global(Vector2(256,464))
	expected = scene.actors.thoma.position + Vector2(-100,220)*player.pixels_per_frame_pixel
	assert_almost_eq(foot,expected,Vector2(0.001,0.001))
	player.show_idle()

func test_first_frame_uses_only_time_after_play() -> void:
	var player = scene.players.thoma
	player.play("thoma.swing")
	player._process(0.8)
	assert_eq(player.frame_index,0,"same-frame pre-start delta must not skip anticipation")
	assert_eq(player.frame_time_ms,0.0)
	player.show_idle()
