extends Node2D

signal phase_changed(phase: String)
signal attack_finished(elapsed: float)

const Rules = preload("res://scripts/rules/grid_rules.gd")
const BONE = Color("eee7d6")
const BRASS = Color("d2b777")
const TEAL = Color("98c9be")
const CLAY = Color("dd9c7e")
const MAP_SCALE = 0.94
const MAP_OFFSET = Vector2(-20, 42)
const SETUP_NAMES = ["OPEN GROUND", "SHIELD WALL", "BROKEN CROSSING"]
const SETUP_DETAILS = [
	"One clean hit.\nThe knight yields one tile.",
	"A second knight holds the line.\nThe target recoils in place.",
	"The crossing has fallen.\nThe river stops the shove.",
]
var units: Array = []
var actors: Dictionary = {}
var setup_index := 0
var diagnostic := false
var reduced_motion := false
var busy := false
var camera: Camera2D
var board: Node2D
var hud: CanvasLayer
var status_label: Label
var detail_label: Label
var hp_label: Label
var action_button: Button
var setup_buttons: Array[Button] = []
var motion_button: CheckButton
var grid_button: CheckButton
var sound: AudioStreamPlayer
var shake_left := 0.0
var shake_strength := 0.0
var shake_phase := 0.0
var last_elapsed := 0.0
var last_events: Array = []
var phase := "ready"

func project(x: float, y: float) -> Vector2:
	return MAP_OFFSET + Vector2(550 + 44 * (x - y), 70 + 26 * (x + y)) * MAP_SCALE

func center(cell: Vector2i) -> Vector2:
	return project(cell.x + 0.5, cell.y + 0.5)

func atlas(path: String, region: Rect2) -> AtlasTexture:
	var texture := AtlasTexture.new()
	texture.atlas = load(path)
	texture.region = region
	texture.filter_clip = true
	return texture

func sprite(parent: Node, texture: Texture2D, at: Vector2, size: Vector2) -> Sprite2D:
	var node := Sprite2D.new()
	node.texture = texture
	node.centered = false
	node.position = at
	node.scale = size / texture.get_size()
	parent.add_child(node)
	return node

func _ready() -> void:
	camera = Camera2D.new()
	camera.position = Vector2(640, 360)
	add_child(camera)
	board = Node2D.new()
	add_child(board)
	sprite(board, load("res://art/battlefield.png"), MAP_OFFSET + Vector2(130, 13.666667) * MAP_SCALE, Vector2(940, 626.666667) * MAP_SCALE)
	# Runtime crops match the web's preserveAspectRatio meet / foot anchoring.
	for cell in [Vector2i(3, 4), Vector2i(6, 4)]:
		var bridge := sprite(board, atlas("res://art/props.png", Rect2(530, 310, 490, 510)), center(cell) + Vector2(-23, -31) * MAP_SCALE, Vector2(46.12, 48) * MAP_SCALE)
		bridge.flip_h = cell.x == 6
	sprite(board, atlas("res://art/props.png", Rect2(1020, 290, 516, 510)), center(Vector2i(8, 4)) + Vector2(-34, -57) * MAP_SCALE, Vector2(68.8, 68) * MAP_SCALE)
	build_hud()
	sound = AudioStreamPlayer.new()
	sound.stream = preload("res://audio/impact_synth.gd").make_hit()
	sound.volume_db = -7
	add_child(sound)
	select_setup(0)
	if "--smoke" in OS.get_cmdline_user_args():
		for index in range(3):
			select_setup(index)
			await play_attack()
		get_tree().quit()
	if "--stage-capture" in OS.get_cmdline_user_args():
		await get_tree().create_timer(0.3).timeout
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("res://.godot/stage.png")
		get_tree().quit()

func _process(delta: float) -> void:
	for actor in actors.values():
		actor.z_index = int(actor.position.y)
	shake_left = maxf(0, shake_left - delta)
	shake_phase += delta * 110.0
	camera.offset = Vector2(sin(shake_phase), cos(shake_phase * 1.3)) * shake_strength * (shake_left / 0.2) if shake_left > 0 and not reduced_motion else Vector2.ZERO
	queue_redraw()

func _draw() -> void:
	if diagnostic:
		for y in range(9):
			for x in range(11):
				var points := PackedVector2Array([project(x,y), project(x+1,y), project(x+1,y+1), project(x,y+1), project(x,y)])
				var color := Color(0.6, 0.79, 0.74, 0.45) if Rules.walkable(Vector2i(x,y)) else Color(0.9, 0.48, 0.35, 0.65)
				draw_polyline(points, color, 1.0, true)

func label_at(parent: Node, text: String, at: Vector2, font_size: int, color: Color = BONE) -> Label:
	var label := Label.new()
	label.text = text
	label.position = at
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_outline_color", Color("101a19"))
	label.add_theme_constant_override("outline_size", 3)
	parent.add_child(label)
	return label

func panel_style(color: Color, border: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.border_color = border
	style.set_border_width_all(1)
	style.content_margin_left = 14
	style.content_margin_right = 14
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	return style

func build_hud() -> void:
	hud = CanvasLayer.new()
	add_child(hud)
	var frame := Panel.new()
	frame.position = Vector2(1000, 104)
	frame.size = Vector2(248, 490)
	frame.add_theme_stylebox_override("panel", panel_style(Color("1b2421"), Color("776746")))
	hud.add_child(frame)
	label_at(hud, "C A M P A I G N   F O R G E", Vector2(32, 18), 15, BRASS)
	label_at(hud, "The weight of a single blow", Vector2(32, 40), 28)
	label_at(hud, "ISOLATED GODOT STUDY   /   SPIKE RULES ONLY", Vector2(820, 36), 14, BRASS)
	label_at(hud, "THOMA  /  IMPACT STUDY", Vector2(1016, 122), 16, BRASS)
	for i in range(3):
		var button := Button.new()
		button.text = "%d   %s" % [i+1, SETUP_NAMES[i]]
		button.position = Vector2(1016, 160 + i*50)
		button.size = Vector2(216, 42)
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.add_theme_font_size_override("font_size", 15)
		button.add_theme_stylebox_override("normal", panel_style(Color("25312b"), Color("776746")))
		button.add_theme_stylebox_override("focus", panel_style(Color(0,0,0,0), BRASS))
		button.pressed.connect(select_setup.bind(i))
		hud.add_child(button)
		setup_buttons.append(button)
	detail_label = label_at(hud, "", Vector2(1016, 320), 15)
	hp_label = label_at(hud, "", Vector2(1016, 382), 16, CLAY)
	action_button = Button.new()
	action_button.text = "STRIKE  /  SPACE"
	action_button.position = Vector2(1016, 422)
	action_button.size = Vector2(216, 48)
	action_button.add_theme_stylebox_override("normal", panel_style(Color("514931"), BRASS))
	action_button.pressed.connect(play_attack)
	hud.add_child(action_button)
	motion_button = CheckButton.new()
	motion_button.text = "Reduced motion  [M]"
	motion_button.position = Vector2(1010, 484)
	motion_button.add_theme_font_size_override("font_size", 15)
	motion_button.toggled.connect(func(value: bool): reduced_motion = value)
	hud.add_child(motion_button)
	grid_button = CheckButton.new()
	grid_button.text = "Grid diagnostic  [G]"
	grid_button.position = Vector2(1010, 532)
	grid_button.add_theme_font_size_override("font_size", 15)
	grid_button.toggled.connect(func(value: bool): diagnostic = value)
	hud.add_child(grid_button)
	status_label = label_at(hud, "Ready", Vector2(32, 636), 22, BRASS)
	label_at(hud, "1–3  SETUP     SPACE / R  REPLAY     M  MOTION     G  GRID     ESC  QUIT", Vector2(32, 680), 15)
	label_at(hud, "Damage 2   •   Knight HP 6   •   No impact bonus", Vector2(690, 640), 15, CLAY)
	label_at(hud, "Original demonstration art. Engine choice remains proposed.", Vector2(690, 664), 13)

func select_setup(index: int) -> void:
	if busy:
		return
	setup_index = index
	units = Rules.setup(index)
	for actor in actors.values():
		actor.free()
	actors.clear()
	for unit in units:
		var actor := Node2D.new()
		actor.name = unit.id
		actor.position = center(unit.cell)
		add_child(actor)
		var ally: bool = unit.side == "ally"
		var region := Rect2(1558, 0, 520, 711) if ally else Rect2(15, 8, 745, 863)
		var height := 52.0 * MAP_SCALE
		var width := height * region.size.x / region.size.y
		var body := sprite(actor, atlas("res://art/l03-party-v1.png" if ally else "res://art/l03-enemies-v1.png", region), Vector2(-width/2, -height), Vector2(width, height))
		body.name = "Body"
		var flash_material := ShaderMaterial.new()
		flash_material.shader = preload("res://shaders/hit_flash.gdshader")
		body.material = flash_material
		var ring := Polygon2D.new()
		var points := PackedVector2Array()
		for j in range(24):
			points.append(Vector2(cos(j*TAU/24)*19, sin(j*TAU/24)*7))
		ring.polygon = points
		ring.color = Color(TEAL if ally else CLAY, 0.35)
		ring.z_index = -1
		actor.add_child(ring)
		label_at(actor, "THOMA" if ally else ("I" if unit.id == "knight-1" else "II"), Vector2(-20, 10), 12, TEAL if ally else CLAY)
		actors[unit.id] = actor
	detail_label.text = SETUP_DETAILS[index]
	hp_label.text = "KNIGHT I   6 / 6 HP"
	status_label.text = SETUP_NAMES[index] + "   /   Ready"
	for i in range(3):
		setup_buttons[i].modulate = BONE if i == index else Color("a4a99b")

func play_attack() -> void:
	if busy:
		return
	# Every replay starts from clean spike state. The pure result is resolved once.
	select_setup(setup_index)
	var result: Dictionary = Rules.attack(units, "thoma", "knight-1")
	if not result.ok:
		status_label.text = result.reason
		return
	set_busy(true)
	last_events = result.events
	var started := Time.get_ticks_usec()
	var attacker: Node2D = actors[result.events[0].unit]
	var target: Node2D = actors[result.events[0].target]
	var start := attacker.position
	var target_start := target.position
	var direction := (target_start - start).normalized()
	var target_material: ShaderMaterial = target.get_node("Body").material
	set_phase("windup", "Thoma braces for the strike")
	var windup := create_tween().set_parallel(true)
	windup.tween_property(attacker, "position", start - direction * (0 if reduced_motion else 9), 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	windup.tween_property(attacker, "rotation", 0.0 if reduced_motion else -direction.x * 0.12, 0.18)
	await windup.finished
	set_phase("lunge", "Closing the distance")
	var lunge := create_tween().set_parallel(true)
	lunge.tween_property(attacker, "position", start + direction * (0 if reduced_motion else 25), 0.085).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN)
	lunge.tween_property(attacker, "rotation", 0.0 if reduced_motion else direction.x * 0.18, 0.085)
	await lunge.finished
	# Damage is presented at contact, before the knockback event is played.
	var damage: Dictionary = result.events[1]
	hp_label.text = "KNIGHT I   %d / 6 HP" % damage.hp_after
	target_material.set_shader_parameter("flash", 0.0 if reduced_motion else 1.0)
	sound.play()
	var contact := target_start + Vector2(0, -25)
	if not reduced_motion:
		emit_particles(contact, false)
	set_phase("contact", "CONTACT   /   −%d HP" % damage.amount)
	# Local hitstop: no actor tween is active during this real-time 80 ms hold.
	# Engine.time_scale stays 1; HUD, audio and particles remain responsive.
	await get_tree().create_timer(0.08, true, false, true).timeout
	if not reduced_motion:
		shake(3.4)
		create_tween().tween_method(func(value: float): target_material.set_shader_parameter("flash", value), 1.0, 0.0, 0.035)
	show_damage(contact, damage.amount)
	var displacement: Dictionary = result.events[2]
	var reaction := create_tween()
	if displacement.type == "knockback":
		set_phase("knockback", "The knight gives ground   /   1 tile")
		reaction.tween_property(target, "position", center(displacement.to), 0.03 if reduced_motion else 0.22).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	else:
		set_phase("blocked", "BLOCKED   /   %s holds the line" % ("Knight II" if displacement.blocker == "unit" else "Broken crossing"))
		# Six pixels is < 1/4 tile step: feet never reach the blocker boundary.
		reaction.tween_property(target, "position", target_start + direction * (0 if reduced_motion else 6), 0.015 if reduced_motion else 0.06).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		await reaction.finished
		if not reduced_motion:
			shake(5.0)
			emit_particles(target_start + direction * 12, true)
		set_phase("blocked_recoil", "BLOCKED   /   Recoil, no displacement")
		reaction = create_tween()
		reaction.tween_property(target, "position", target_start, 0.015 if reduced_motion else 0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	await reaction.finished
	set_phase("settled", "−2 HP   /   " + ("Knocked back one tile" if displacement.type == "knockback" else "Knockback blocked"))
	var recovery := create_tween().set_parallel(true)
	recovery.tween_property(attacker, "position", start, 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	recovery.tween_property(attacker, "rotation", 0.0, 0.18)
	await recovery.finished
	await get_tree().create_timer(0.22).timeout
	units = result.units
	target_material.set_shader_parameter("flash", 0.0)
	camera.offset = Vector2.ZERO
	last_elapsed = (Time.get_ticks_usec() - started) / 1000000.0
	set_busy(false)
	set_phase("ready", "%s   /   %.3f s   /   Space to replay" % [SETUP_NAMES[setup_index], last_elapsed])
	print("SEQUENCE setup=%d reduced=%s elapsed_wall_s=%.4f limit=1.700 hp=%d cell=%s" % [setup_index+1, reduced_motion, last_elapsed, units[1].hp, units[1].cell])
	attack_finished.emit(last_elapsed)

func set_busy(value: bool) -> void:
	busy = value
	action_button.disabled = value
	motion_button.disabled = value
	for button in setup_buttons:
		button.disabled = value
	action_button.text = "STRIKING…" if value else "REPLAY  /  SPACE"

func set_phase(value: String, text: String) -> void:
	phase = value
	status_label.text = text
	phase_changed.emit(value)

func shake(strength: float) -> void:
	shake_strength = strength
	shake_left = 0.2
	shake_phase = 0

func show_damage(at: Vector2, amount: int) -> void:
	var number := label_at(self, "−%d" % amount, at + Vector2(-12, -25), 27, BRASS)
	number.z_index = 1000
	number.add_theme_constant_override("outline_size", 7)
	var tween := create_tween().set_parallel(true)
	tween.tween_property(number, "position:y", number.position.y - (0 if reduced_motion else 30), 0.52).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(number, "modulate:a", 0.0, 0.20).set_delay(0.32)
	tween.chain().tween_callback(number.queue_free)

func emit_particles(at: Vector2, dust: bool) -> void:
	var particles := CPUParticles2D.new()
	particles.position = at
	particles.z_index = 900
	particles.amount = 18 if dust else 24
	particles.lifetime = 0.30
	particles.one_shot = true
	particles.explosiveness = 1
	particles.direction = Vector2(0, -1)
	particles.spread = 100
	particles.gravity = Vector2(0, 150)
	particles.initial_velocity_min = 25 if dust else 55
	particles.initial_velocity_max = 55 if dust else 125
	particles.scale_amount_min = 1.4 if dust else 0.6
	particles.scale_amount_max = 2.8 if dust else 1.5
	particles.color = Color("aa956e") if dust else Color("f3dca0")
	var gradient := Gradient.new()
	gradient.set_color(0, particles.color)
	gradient.set_color(1, Color(particles.color, 0))
	particles.color_ramp = gradient
	add_child(particles)
	particles.finished.connect(particles.queue_free)
	particles.emitting = true

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	match event.keycode:
		KEY_1, KEY_2, KEY_3:
			select_setup(event.keycode - KEY_1)
		KEY_G:
			grid_button.button_pressed = not grid_button.button_pressed
		KEY_M:
			if not busy:
				motion_button.button_pressed = not motion_button.button_pressed
		KEY_SPACE, KEY_R:
			play_attack()
		KEY_ESCAPE:
			get_tree().quit()
