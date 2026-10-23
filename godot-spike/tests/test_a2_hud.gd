extends "res://addons/gut/test.gd"
const Scene = preload("res://scenes/Skirmish.tscn")
var scene

func before_each() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	scene = add_child_autofree(Scene.instantiate())
	await get_tree().process_frame

func key(code: Key, shift: bool = false) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.shift_pressed = shift
	event.pressed = true
	scene._unhandled_key_input(event)

func visible_text(node: Node) -> String:
	var result := ""
	if node is Control and not node.is_visible_in_tree(): return result
	if node is Label or node is BaseButton: result += node.text+"\n"
	for child in node.get_children(): result += visible_text(child)
	return result

func test_default_hud_has_no_diagnostics_and_f1_reveals_them() -> void:
	var shown := visible_text(scene.hud)
	for token in ["SCENARIO","SPACE","DEBUG","Ready","Anticipation","THOMA","OPEN GROUND","SHIELD WALL","BROKEN CROSSING","KNIGHT I","Settled","1 / 2 / 3","0.0 s"]:
		assert_false(shown.contains(token),"default diagnostic leak: "+token)
	assert_true(shown.contains("托瑪"))
	assert_true(shown.contains("修士／醫療"))
	assert_false(scene.scenario_label.is_visible_in_tree())
	assert_false(scene.status_label.is_visible_in_tree())
	assert_false(scene.hint_label.is_visible_in_tree())
	key(KEY_F1)
	shown = visible_text(scene.hud)
	for token in ["SCENARIO","SPACE","DEBUG","OPEN GROUND","Ready"]: assert_true(shown.contains(token),"F1 reveals "+token)
	key(KEY_QUOTELEFT)
	assert_false(scene.debug_visible)
	assert_true(scene.action_button.has_focus())

func test_help_hidden_and_h_question_shift_slash_escape_toggle() -> void:
	assert_false(scene.hud.help_panel.visible)
	key(KEY_H)
	assert_true(scene.hud.help_panel.visible)
	assert_true(visible_text(scene.hud.help_panel).contains("空白鍵"))
	key(KEY_ESCAPE)
	assert_false(scene.hud.help_panel.visible)
	key(KEY_QUESTION)
	assert_true(scene.hud.help_panel.visible)
	key(KEY_SLASH,true)
	assert_false(scene.hud.help_panel.visible)
	assert_true(scene.action_button.has_focus())

func test_forecast_matches_each_rules_result_and_rendered_labels() -> void:
	for index in range(3):
		scene.select_setup(index)
		scene.hud.arm_attack()
		var result: Dictionary = scene.Rules.attack(scene.units,"thoma","knight-1")
		var damage: Dictionary = result.events.filter(func(e): return e.type=="damage")[0]
		var movement: Dictionary = result.events.filter(func(e): return e.type in ["knockback","knockback_blocked"])[0]
		var forecast: Dictionary = scene.hud.forecast
		assert_true(scene.hud.forecast_panel.visible)
		assert_eq(forecast.damage,damage.amount)
		assert_eq(forecast.hp_before,scene.units[1].hp)
		assert_eq(forecast.hp_after,damage.hp_after)
		assert_eq(scene.hud.damage_label.text,"傷害　%d" % damage.amount)
		assert_eq(scene.hud.forecast_hp.text,"生命　%d → %d" % [scene.units[1].hp,damage.hp_after])
		var expected := "擊退一格" if movement.type=="knockback" else "受阻"
		var reason := "" if movement.type=="knockback" else ("被友軍阻擋" if movement.blocker=="unit" else "被斷橋阻擋")
		assert_eq(forecast.outcome,expected)
		assert_eq(forecast.reason,reason)
		assert_eq(scene.hud.outcome_label.text,expected)
		assert_eq(scene.hud.reason_label.text,reason)
		assert_true(visible_text(scene.hud.forecast_panel).contains("議會騎士・甲"))
		key(KEY_ESCAPE)
		assert_false(scene.hud.forecast_panel.visible)
		assert_false(scene.hud.armed)
	# A different legal HP state proves the display is not fixture literals.
	var injured: Array = scene.Rules.setup(0)
	injured[1].hp = 1
	scene.hud.refresh_forecast(scene.Rules.attack(injured,"thoma","knight-1"))
	assert_eq(scene.hud.damage_label.text,"傷害　1")
	assert_eq(scene.hud.forecast_hp.text,"生命　1 → 0")

func test_armed_confirmation_locks_and_forecast_hides_at_contact() -> void:
	scene.hud.activate_attack()
	assert_true(scene.hud.armed)
	assert_false(scene.busy)
	scene.hud.activate_attack()
	assert_true(scene.busy)
	assert_true(scene.hud.forecast_panel.visible)
	await scene.hitstop_started
	assert_false(scene.hud.forecast_panel.visible)
	assert_true(scene.action_button.disabled)
	key(KEY_H)
	assert_true(scene.hud.help_panel.visible,"HUD responds inside hitstop")
	key(KEY_H)
	await scene.attack_finished
	assert_false(scene.hud.armed)
	assert_eq(scene.hp_bars["knight-1"].value,4.0)

func test_weapon_manifest_schema_fields_hashes_and_no_smear_in_reduced() -> void:
	var schema = JSON.parse_string(FileAccess.get_file_as_string("res://art/anim-shared/manifest.schema.json"))
	for field in schema.required: assert_has(scene.manifest,field)
	var idle: Dictionary = scene.manifest.sequences["thoma.idle"]
	assert_eq(idle.frames[0].path,"thoma/idle/01.png")
	var swing: Dictionary = scene.manifest.sequences["thoma.swing"]
	assert_gte(swing.contact_frame_index,0.0)
	assert_lt(swing.contact_frame_index,float(swing.frames.size()))
	assert_does_not_have(swing.reduced_frame_indices,2.0)
	for sequence in scene.manifest.sequences.values():
		for f in sequence.frames:
			var source: String = ProjectSettings.globalize_path("res://../shared-anim/"+f.path)
			var copied: String = "res://art/anim-shared/"+f.path
			assert_true(FileAccess.file_exists(source))
			assert_true(FileAccess.file_exists(copied))
			assert_eq(FileAccess.get_sha256(source),FileAccess.get_sha256(copied))
	var audit = JSON.parse_string(FileAccess.get_file_as_string("res://art/anim-shared/frame-audit.json"))
	var count := 0
	for record in audit:
		if record.path.begins_with("thoma/"):
			count += 1
			assert_eq(record.weapon_status,"PROPOSED")
			assert_eq(record.sha256,FileAccess.get_sha256("res://art/anim-shared/"+record.path))
	assert_eq(count,7)

func test_knight_textures_differ_in_every_idle_hit_and_stagger_frame() -> void:
	for sequence in ["idle","hit","stagger"]:
		var a: Array = scene.manifest.sequences["knight-a."+sequence].frames
		var b: Array = scene.manifest.sequences["knight-b."+sequence].frames
		assert_eq(a.size(),b.size())
		for i in range(a.size()):
			assert_ne(a[i].path,b[i].path)
			assert_ne(FileAccess.get_sha256("res://art/anim-shared/"+a[i].path),FileAccess.get_sha256("res://art/anim-shared/"+b[i].path))

func test_a2_timing_all_setups_normal_and_reduced_under_budget() -> void:
	for reduced in [false,true]:
		scene.motion_button.button_pressed = reduced
		for index in range(3):
			scene.select_setup(index)
			scene.play_attack()
			var deadline := Time.get_ticks_msec()+2200
			while scene.busy and Time.get_ticks_msec()<deadline: await get_tree().process_frame
			assert_false(scene.busy,"watchdog catches incomplete playback")
			assert_gt(scene.last_elapsed,0.0)
			assert_lte(scene.last_elapsed,1.7,"strike to input-ready includes hold")
			assert_gte(scene.last_hold_ms,80.0)
			assert_false(scene.action_button.disabled)

func test_cjk_glyphs_and_transient_banner() -> void:
	var font: Font = scene.hud.root.theme.default_font
	for char in "托瑪修士醫療生命攻擊預測議會騎甲乙傷害退格受阻被友軍斷橋操作說明我方回合":
		assert_true(font.has_char(char.unicode_at(0)),"CJK glyph "+char)
	assert_true(scene.hud.banner.visible)
	await get_tree().create_timer(1.2).timeout
	assert_false(scene.hud.banner.visible,"turn banner must not persist")
