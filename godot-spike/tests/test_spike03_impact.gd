extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/Skirmish.tscn")
const Tuned = preload("res://config/impact_profile.tres")
const Baseline = preload("res://config/impact_profile_a9_baseline.tres")
var scene

func before_each() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	scene = add_child_autofree(Scene.instantiate())
	await get_tree().process_frame

func after_each() -> void:
	get_tree().paused = false
	await get_tree().process_frame

func test_both_profiles_load_and_every_export_is_in_range() -> void:
	for profile in [Tuned,Baseline]:
		assert_true(profile is ImpactProfile)
		for field in profile.get_property_list():
			if not field.usage & PROPERTY_USAGE_SCRIPT_VARIABLE: continue
			var value = profile.get(field.name)
			if field.hint == PROPERTY_HINT_RANGE:
				var limits: PackedStringArray = field.hint_string.split(",")
				assert_between(float(value),float(limits[0]),float(limits[1]),field.name)
			elif value is Color:
				for channel in [value.r,value.g,value.b,value.a]: assert_between(channel,0.0,1.0,field.name)
			elif value is String: assert_false(value.is_empty(),field.name)
		assert_lte(profile.number_pop_ms,profile.number_fade_delay_ms)
		assert_lte(profile.number_fade_delay_ms+profile.number_fade_ms,profile.number_lifetime_ms)
		assert_lte(profile.spark_velocity_min,profile.spark_velocity_max)
		assert_lte(profile.dust_velocity_min,profile.dust_velocity_max)
		assert_lte(profile.reduced_hitstop_ms,profile.hitstop_ms(false,false))

func test_baseline_reproduces_the_a9_manifest_and_all_visual_audio_constants() -> void:
	var impact: Dictionary = scene.manifest.impact
	assert_eq(Baseline.attacker_hitstop_ms,float(impact.hitstop_ms))
	assert_eq(Baseline.target_hitstop_ms,float(impact.hitstop_ms))
	assert_eq(Baseline.shake_strength_px,float(impact.shake.strength_px))
	assert_eq(Baseline.shake_duration_ms,float(impact.shake.duration_ms))
	assert_eq(Baseline.shake_decay,float(impact.shake.decay))
	for key in ["flash_ms","knockback_ms","reduced_knockback_ms","blocked_shove_ms","blocked_recoil_ms","blocked_shove_px","settle_ms"]:
		assert_eq(Baseline.get(key),float(impact[key]),key)
	assert_eq(Baseline.attack_zoom,float(scene.manifest.camera.zoom))
	assert_eq(Baseline.camera_in_ms,float(scene.manifest.camera.in_ms))
	assert_eq(Baseline.camera_out_ms,float(scene.manifest.camera.out_ms))
	assert_eq(Baseline.focus_weight,float(scene.manifest.camera.focus_weight))
	var constants := {"directional_shake":false,"legacy_shake_frequency":110.0,"legacy_shake_y_frequency":1.3,"legacy_first_y":-0.5,
		"flash_mix":0.65,"flash_color":Color.WHITE,"flash_hold_ms":0.0,"recoil_px":0.0,"zoom_punch":0.0,
		"number_from_target":false,"number_font_px":18,"number_offset_x":-8.0,"number_offset_y":-58.0,"number_scale":1.0,
		"number_rise_px":30.0,"number_lifetime_ms":380.0,"number_fade_delay_ms":180.0,"number_fade_ms":200.0,
		"number_color":Color("d2b777"),"number_backing_color":Color("101a19"),"number_backing":true,"number_margin_px":3,"number_outline_px":3,
		"spoke_count":7,"spoke_width":1.2,"spoke_inner_px":3.0,"spoke_outer_px":8.0,"spoke_variation_px":2.0,"spoke_angle":0.2,
		"spoke_color":Color("d2b777"),"spoke_fade_ms":120.0,"streak_length_px":0.0,"spark_count":24,"dust_count":18,
		"dust_on_contact":false,"particle_lifetime_ms":300.0,"particle_spread":100.0,"particle_gravity":150.0,
		"spark_velocity_min":55.0,"spark_velocity_max":125.0,"dust_velocity_min":25.0,"dust_velocity_max":55.0,
		"spark_scale_min":0.6,"spark_scale_max":1.5,"dust_scale_min":1.4,"dust_scale_max":2.8,
		"spark_color":Color("f3dca0"),"dust_color":Color("aa956e"),"particle_preprocess_ms":16.0,"layered_sfx":false,"impact_db":-7.0}
	for key in constants: assert_eq(Baseline.get(key),constants[key],key)
	# A9's source manifest remains the historical record, not live tuning data.
	assert_eq(FileAccess.get_file_as_string("res://art/anim-shared/manifest.json"),FileAccess.get_file_as_string("res://../shared-anim/manifest.json"))

func test_contact_bundle_same_frame_and_both_hitstop_minimums() -> void:
	for crit in [false,true]:
		scene.next_hit_crit = crit
		scene.play_attack()
		await scene.hitstop_started
		assert_eq(scene.players.thoma.frame_index,3)
		assert_eq(scene.impact_layers.size(),9)
		var frame: int = Engine.get_process_frames()
		for layer in scene.impact_layers: assert_eq(layer.frame,frame,layer.type)
		for trigger in scene.contact_triggers: assert_eq(trigger.frame,frame,trigger.type)
		assert_eq(scene.players["knight-1"].visual_offset,scene.hit_direction*Tuned.recoil_px)
		assert_true(get_tree().paused)
		assert_almost_eq(scene.camera.zoom.x,Tuned.attack_zoom+Tuned.zoom_punch,0.00001)
		await scene.hitstop_finished
		assert_gte(scene.last_hold_ms,Tuned.hitstop_ms(crit,false))
		assert_gte(scene.hold_process_ms,Tuned.hitstop_ms(crit,false))
		await scene.attack_finished
		await get_tree().process_frame

func test_directional_first_kick_envelope_decays_and_ends_at_zero() -> void:
	for direction in [Vector2(1,0),Vector2(-1,0),Vector2(0.6,0.8)]:
		scene.hit_direction = direction
		scene.shake(Tuned.shake_strength_px)
		assert_almost_eq(scene.camera.offset,direction*Tuned.shake_strength_px,Vector2(0.0001,0.0001))
		var duration: float = Tuned.shake_duration_ms/1000.0
		for t in [0.1,0.3,0.6,0.9]:
			var offset: Vector2 = scene.shake_offset(duration*(1-t))
			assert_almost_eq(offset.cross(direction),0.0,0.0001)
			assert_lte(offset.length(),Tuned.shake_strength_px*exp(-Tuned.shake_decay*t)+0.0001)
		assert_eq(scene.shake_offset(0),Vector2.ZERO)
	await get_tree().create_timer(Tuned.shake_duration_ms/1000.0+0.05).timeout
	assert_eq(scene.camera.offset,Vector2.ZERO)

func test_reduced_motion_never_changes_camera_or_recoils() -> void:
	scene.motion_button.button_pressed = true
	scene.next_hit_crit = true
	scene.play_attack()
	while scene.busy:
		assert_eq(scene.camera.offset,Vector2.ZERO)
		assert_eq(scene.camera.zoom,Vector2.ONE)
		assert_eq(scene.camera.position,scene.camera_home)
		assert_eq(scene.players["knight-1"].visual_offset,Vector2.ZERO)
		assert_eq(scene.actors["knight-1"].get_node("Body").material.get_shader_parameter("flash"),0.0)
		assert_true(get_tree().get_nodes_in_group("impact_particles").is_empty())
		await get_tree().process_frame
	assert_lte(scene.last_elapsed,1.7)

func test_flash_number_recoil_and_particles_return_to_rest_and_free() -> void:
	scene.play_attack()
	await scene.hitstop_started
	var number: Label = get_tree().get_first_node_in_group("impact_numbers")
	assert_eq(number.scale,Vector2.ONE*Tuned.number_scale)
	assert_gt(get_tree().get_nodes_in_group("impact_particles").size(),1)
	await scene.hitstop_finished
	await get_tree().create_timer(0.15).timeout
	assert_true(is_instance_valid(number))
	assert_almost_eq(number.scale,Vector2.ONE,Vector2(0.001,0.001))
	assert_eq(scene.players["knight-1"].visual_offset,Vector2.ZERO)
	assert_eq(scene.actors["knight-1"].get_node("Body").material.get_shader_parameter("flash"),0.0)
	await scene.attack_finished
	await get_tree().create_timer(0.35).timeout
	assert_false(is_instance_valid(number))
	assert_true(get_tree().get_nodes_in_group("impact_particles").is_empty())
	assert_eq(scene.camera.zoom,Vector2.ONE)
	assert_eq(scene.camera.offset,Vector2.ZERO)

func test_sfx_hooks_once_at_preparation_contact_and_landing() -> void:
	for setup in range(3):
		for crit in [false,true]:
			scene.select_setup(setup)
			scene.next_hit_crit = crit
			await scene.play_attack()
			assert_eq(scene.sfx_trace.size(),3)
			assert_eq(scene.sfx_trace[0].hook,"swing_whoosh")
			assert_eq(scene.sfx_trace[0].swing_frame,1)
			assert_eq(scene.sfx_trace[1].hook,"impact_crit" if crit else "impact")
			assert_eq(scene.sfx_trace[1].swing_frame,3)
			assert_eq(scene.sfx_trace[1].frame,scene.contact_triggers[0].frame)
			assert_eq(scene.sfx_trace[2].hook,"knockback_thud" if setup==0 else "blocked_thud")
			assert_gt(scene.sfx_trace[2].frame,scene.sfx_trace[1].frame)
			await get_tree().process_frame
	for hook in ["swing_whoosh","impact","impact_crit","knockback_thud","blocked_thud"]:
		var synth = preload("res://audio/impact_synth.gd")
		assert_eq(synth.make_hook(hook).data,synth.make_hook(hook).data,hook)

func test_all_modes_three_setups_budget_rules_and_reduced_no_slower() -> void:
	var normal: Array = []
	for mode in ["normal","crit","reduced"]:
		for setup in range(3):
			scene.select_setup(setup)
			scene.motion_button.button_pressed = mode=="reduced"
			scene.next_hit_crit = mode=="crit"
			var expected: Dictionary = scene.Rules.attack(scene.Rules.setup(setup),"thoma","knight-1")
			await scene.play_attack()
			assert_eq(scene.units,expected.units,"presentation does not change rules")
			assert_eq(scene.actors["knight-1"].position,scene.center(expected.units[1].cell))
			assert_lte(scene.last_elapsed,1.7)
			assert_false(scene.busy)
			if mode=="normal": normal.append(scene.last_elapsed)
			if mode=="reduced": assert_lte(scene.last_elapsed,float(normal[setup]),"reduced <= normal")
			await get_tree().process_frame

func test_crit_key_is_next_hit_only_and_locked_during_attack() -> void:
	var key := InputEventKey.new()
	key.keycode = KEY_C
	key.pressed = true
	scene._unhandled_key_input(key)
	assert_true(scene.next_hit_crit)
	assert_true(scene.hint_label.text.ends_with("ON"))
	scene.play_attack()
	assert_true(scene.hit_is_crit)
	assert_false(scene.next_hit_crit)
	assert_true(scene.hint_label.text.ends_with("OFF"),"consumed next-hit flag cannot leave stale diagnostics")
	scene._unhandled_key_input(key)
	assert_false(scene.next_hit_crit)
	await scene.attack_finished
	await scene.play_attack()
	assert_false(scene.hit_is_crit)
