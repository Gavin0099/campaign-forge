extends CanvasLayer
## Always-processing presentation: pure rule events supply every forecast number.
const BONE = Color("eee7d6")
const BRASS = Color("d2b777")
const SAGE = Color("b9bbab")
const TEAL = Color("98c9be")
const CLAY = Color("dd9c7e")
const NAMES = {"thoma":"托瑪", "knight-1":"議會騎士・甲", "knight-2":"議會騎士・乙"}
var scene
var root: Control
var selected: Panel
var forecast_panel: Panel
var help_panel: Panel
var debug_panel: Panel
var banner: Panel
var damage_label: Label
var forecast_hp: Label
var outcome_label: Label
var reason_label: Label
var selected_hp: Label
var selected_bar: ProgressBar
var selected_status: Label
var unit_bars: Dictionary = {}
var forecast: Dictionary = {}
var armed := false
var banner_tween: Tween
var hover_tag: Panel
var hover_name: Label

func frame() -> StyleBoxTexture:
	var style := StyleBoxTexture.new()
	style.texture = preload("res://art/ui/field-frame.png")
	for side in [SIDE_LEFT,SIDE_TOP,SIDE_RIGHT,SIDE_BOTTOM]: style.set_texture_margin(side,12)
	return style

func panel(at: Vector2, dimensions: Vector2) -> Panel:
	var p := Panel.new()
	p.position = at
	p.size = dimensions
	p.add_theme_stylebox_override("panel",frame())
	root.add_child(p)
	return p

func text(parent: Node, value: String, at: Vector2, font_size: int = 18, color: Color = BONE) -> Label:
	var label := Label.new()
	label.text = value
	label.position = at
	label.add_theme_font_size_override("font_size",font_size)
	label.add_theme_color_override("font_color",color)
	parent.add_child(label)
	return label

func button(parent: Node, value: String, at: Vector2, dimensions: Vector2) -> Button:
	var control := Button.new()
	control.text = value
	control.position = at
	control.size = dimensions
	control.add_theme_stylebox_override("normal",frame())
	control.add_theme_stylebox_override("hover",scene.panel_style(Color("30372c"),BRASS))
	control.add_theme_stylebox_override("pressed",scene.panel_style(Color("101a19"),BRASS))
	control.add_theme_stylebox_override("disabled",scene.panel_style(Color("1b2421"),Color("776746")))
	var focus: StyleBoxFlat = scene.panel_style(Color(0,0,0,0),TEAL)
	focus.set_border_width_all(2)
	control.add_theme_stylebox_override("focus",focus)
	for state in ["font_color","font_hover_color","font_pressed_color","font_focus_color"]: control.add_theme_color_override(state,BRASS)
	control.add_theme_color_override("font_disabled_color",SAGE)
	parent.add_child(control)
	return control

func portrait(parent: Control, id: String, at: Vector2, dimensions: Vector2) -> void:
	var back := Panel.new()
	back.position = at
	back.size = dimensions
	back.add_theme_stylebox_override("panel",scene.panel_style(Color("30372c"),Color("776746")))
	parent.add_child(back)
	var image := TextureRect.new()
	image.texture = scene.atlas("res://art/l03-party-v1.png",Rect2(1718,0,220,245)) if id=="thoma" else scene.atlas("res://art/l03-enemies-v1.png",Rect2(270,8,265,300))
	if id=="knight-2": image.texture = scene.atlas("res://art/anim-shared/knight-b/idle/00.png",Rect2(255,55,100,140))
	image.position = Vector2(4,4)
	image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	back.add_child(image)
	image.size = dimensions-Vector2(8,8)

func bar(parent: Node, at: Vector2, dimensions: Vector2, maximum: float, ally: bool) -> ProgressBar:
	var b := ProgressBar.new()
	b.position = at
	b.max_value = maximum
	b.value = maximum
	b.show_percentage = false
	b.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var background := StyleBoxFlat.new()
	background.bg_color = Color("101a19")
	background.border_color = Color("776746")
	background.set_border_width_all(1)
	var fill := StyleBoxFlat.new()
	fill.bg_color = BRASS if ally else BONE
	b.add_theme_stylebox_override("background",background)
	b.add_theme_stylebox_override("fill",fill)
	parent.add_child(b)
	b.size = dimensions
	return b

func build(owner_scene) -> void:
	scene = owner_scene
	process_mode = Node.PROCESS_MODE_ALWAYS
	root = Control.new()
	add_child(root)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei","Noto Sans TC","PingFang TC"])
	var theme := Theme.new()
	theme.default_font = font
	theme.default_font_size = 18
	root.theme = theme
	selected = panel(Vector2(28,534),Vector2(386,158))
	selected.name = "SelectedUnit"
	portrait(selected,"thoma",Vector2(14,16),Vector2(102,124))
	text(selected,"托瑪",Vector2(132,14),26,BRASS)
	text(selected,"修士／醫療",Vector2(132,51),16,SAGE)
	selected_hp = text(selected,"",Vector2(132,78),18)
	selected_bar = bar(selected,Vector2(132,108),Vector2(230,8),8,true)
	selected_status = text(selected,"守住同伴的退路",Vector2(132,124),16,SAGE)
	scene.action_button = button(root,"準備攻擊",Vector2(1046,632),Vector2(202,56))
	scene.action_button.pressed.connect(activate_attack)
	scene.action_button.grab_focus.call_deferred()
	forecast_panel = panel(Vector2(878,104),Vector2(370,328))
	forecast_panel.name = "AttackForecast"
	text(forecast_panel,"攻擊預測",Vector2(20,14),20,BRASS)
	portrait(forecast_panel,"thoma",Vector2(22,52),Vector2(90,90))
	portrait(forecast_panel,"knight-1",Vector2(258,52),Vector2(90,90))
	text(forecast_panel,"托瑪",Vector2(42,148),18)
	text(forecast_panel,NAMES["knight-1"],Vector2(226,148),16)
	text(forecast_panel,"→",Vector2(168,72),30,BRASS)
	damage_label = text(forecast_panel,"",Vector2(20,186),22,BRASS)
	forecast_hp = text(forecast_panel,"",Vector2(158,191),18)
	outcome_label = text(forecast_panel,"",Vector2(20,235),22)
	reason_label = text(forecast_panel,"",Vector2(20,277),16,SAGE)
	forecast_panel.hide()
	banner = panel(Vector2(510,-70),Vector2(260,60))
	text(banner,"我方回合",Vector2(67,11),26,BRASS)
	help_panel = panel(Vector2(438,158),Vector2(404,390))
	help_panel.name = "Help"
	text(help_panel,"行軍手冊",Vector2(24,18),26,BRASS)
	text(help_panel,"空白鍵　準備／確認攻擊\nR　重播本次交鋒\n1／2／3　切換交鋒配置\nM　減少動態效果\nTab　移動焦點\nF1／`　開關除錯資訊\nH／?　開關操作說明\nEsc　收起視窗／取消／離開",Vector2(24,70),18)
	button(help_panel,"收起",Vector2(234,320),Vector2(144,46)).pressed.connect(func(): toggle_help(false))
	help_panel.hide()
	debug_panel = panel(Vector2(878,448),Vector2(370,174))
	debug_panel.name = "Diagnostics"
	scene.debug_panel = debug_panel
	scene.scenario_label = text(debug_panel,"",Vector2(14,10),16)
	scene.detail_label = text(debug_panel,"",Vector2(14,35),14)
	scene.hp_label = text(debug_panel,"",Vector2(14,74),14)
	scene.status_label = text(debug_panel,"",Vector2(14,94),14)
	scene.hint_label = text(debug_panel,"1/2/3  SCENARIO | SPACE/R | F1 DEBUG",Vector2(14,145),12)
	# Scenario controls are debug-only; keep keyboard setup mutation locks.
	for i in range(3):
		var b := button(debug_panel,str(i+1),Vector2(230+i*39,8),Vector2(34,28))
		b.pressed.connect(scene.select_setup.bind(i))
		scene.setup_buttons.append(b)
	scene.motion_button = CheckButton.new()
	scene.motion_button.text = "減少動態"
	scene.motion_button.position = Vector2(8,112)
	scene.motion_button.add_theme_font_size_override("font_size",14)
	scene.motion_button.toggled.connect(func(value: bool): scene.reduced_motion = value)
	debug_panel.add_child(scene.motion_button)
	scene.grid_button = CheckButton.new()
	scene.grid_button.text = "格線"
	scene.grid_button.position = Vector2(190,112)
	scene.grid_button.add_theme_font_size_override("font_size",14)
	scene.grid_button.toggled.connect(func(value: bool): scene.diagnostic = value)
	debug_panel.add_child(scene.grid_button)
	debug_panel.hide()
	hover_tag = panel(Vector2.ZERO,Vector2(170,36))
	hover_tag.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hover_name = text(hover_tag,"",Vector2(10,5),16)
	hover_tag.hide()
	show_turn_banner()

func show_turn_banner() -> void:
	if banner_tween: banner_tween.kill()
	banner.show()
	banner.position.y = 22 if scene.reduced_motion else -70
	banner_tween = create_tween()
	if not scene.reduced_motion: banner_tween.tween_property(banner,"position:y",22.0,0.2)
	banner_tween.tween_interval(0.65)
	if not scene.reduced_motion: banner_tween.tween_property(banner,"position:y",-70.0,0.2)
	banner_tween.tween_callback(banner.hide)

func reset_units() -> void:
	for b in unit_bars.values(): b.free()
	unit_bars.clear()
	scene.hp_bars.clear()
	for unit in scene.units:
		var b := bar(root,Vector2.ZERO,Vector2(36,5),unit.max_hp,unit.side=="ally")
		unit_bars[unit.id] = b
		scene.hp_bars[unit.id] = b
	selected_hp.text = "生命　%d / %d" % [scene.units[0].hp,scene.units[0].max_hp]
	selected_bar.max_value = scene.units[0].max_hp
	selected_bar.value = scene.units[0].hp
	disarm()
	refresh_forecast(scene.Rules.attack(scene.units,"thoma","knight-1"))

func refresh_forecast(result: Dictionary) -> void:
	forecast.clear()
	if not result.ok: return
	for event in result.events:
		match event.type:
			"damage":
				forecast.damage = event.amount
				forecast.hp_after = event.hp_after
				forecast.hp_before = event.hp_after + event.amount
			"knockback":
				forecast.outcome = "擊退一格"
				forecast.reason = ""
			"knockback_blocked":
				forecast.outcome = "受阻"
				forecast.reason = "被友軍阻擋" if event.blocker=="unit" else "被斷橋阻擋"
	damage_label.text = "傷害　%d" % forecast.damage
	forecast_hp.text = "生命　%d → %d" % [forecast.hp_before,forecast.hp_after]
	outcome_label.text = forecast.outcome
	reason_label.text = forecast.reason

func arm_attack() -> void:
	if scene.busy: return
	# Replay always starts from the fixture; preview the same fresh state.
	scene.select_setup(scene.setup_index)
	armed = true
	forecast_panel.show()
	scene.action_button.text = "確認攻擊"

func disarm() -> void:
	armed = false
	forecast_panel.hide()
	if is_instance_valid(scene.action_button): scene.action_button.text = "準備攻擊"

func activate_attack() -> void:
	if scene.busy: return
	if armed: scene.play_attack()
	else: arm_attack()

func toggle_help(value: bool) -> void:
	help_panel.visible = value
	if value: help_panel.get_child(help_panel.get_child_count()-1).grab_focus()
	else: scene.action_button.grab_focus()

func _process(_delta: float) -> void:
	if not is_instance_valid(scene): return
	for id in unit_bars:
		var body: Sprite2D = scene.actors[id].get_node("Body")
		var pos: Vector2 = body.get_global_transform_with_canvas()*Vector2(256,70 if id=="knight-2" else 100)
		unit_bars[id].position = pos+Vector2(-18,-10)
	# Names are transient inspection labels; no permanent identity/debug text.
	if scene.busy or help_panel.visible:
		hover_tag.hide()
		return
	var pointer := root.get_local_mouse_position()
	hover_tag.hide()
	for id in scene.actors:
		if id=="thoma": continue
		var body: Sprite2D = scene.actors[id].get_node("Body")
		var local: Vector2 = body.get_global_transform_with_canvas().affine_inverse()*pointer
		if Rect2(80,50,340,420).has_point(local):
			hover_name.text = NAMES[id]
			hover_tag.position = pointer+Vector2(14,-42)
			hover_tag.show()
			break
