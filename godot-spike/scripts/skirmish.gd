extends Node2D

signal phase_changed(phase: String)
signal attack_finished(elapsed: float)
signal contact_released

const Rules = preload("res://scripts/rules/grid_rules.gd")
const Manifest = preload("res://scripts/anim/anim_manifest.gd")
const FramePlayer = preload("res://scripts/anim/frame_player.gd")
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
var grid_overlay: Node2D
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
var manifest: Dictionary = {}
var players: Dictionary = {}
var contact_triggers: Array = []
var last_hold_ms := 0.0
var contact_point := Vector2.ZERO
var current_plan: Dictionary = {}
var world: Node2D
var ui_process_ticks := 0
var hold_active := false

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
	process_mode = Node.PROCESS_MODE_ALWAYS
	world = Node2D.new()
	world.name = "World"
	world.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(world)
	var loader := Manifest.new()
	if not loader.read():
		get_tree().quit(1)
		return
	manifest = loader.data
	camera = Camera2D.new()
	camera.position = Vector2(640, 360)
	world.add_child(camera)
	board = Node2D.new()
	world.add_child(board)
	sprite(board, load("res://art/battlefield.png"), MAP_OFFSET + Vector2(130, 13.666667) * MAP_SCALE, Vector2(940, 626.666667) * MAP_SCALE)
	# Runtime crops match the web's preserveAspectRatio meet / foot anchoring.
	for cell in [Vector2i(3, 4), Vector2i(6, 4)]:
		var bridge := sprite(board, atlas("res://art/props.png", Rect2(530, 310, 490, 510)), center(cell) + Vector2(-23, -31) * MAP_SCALE, Vector2(46.12, 48) * MAP_SCALE)
		bridge.flip_h = cell.x == 6
	sprite(board, atlas("res://art/props.png", Rect2(1020, 290, 516, 510)), center(Vector2i(8, 4)) + Vector2(-34, -57) * MAP_SCALE, Vector2(68.8, 68) * MAP_SCALE)
	grid_overlay = Node2D.new()
	grid_overlay.z_index = 1
	world.add_child(grid_overlay)
	grid_overlay.draw.connect(draw_grid)
	build_hud()
	sound = AudioStreamPlayer.new()
	sound.stream = preload("res://audio/impact_synth.gd").make_hit()
	sound.volume_db = -7
	add_child(sound)
	select_setup(0)
	if "--overview" in OS.get_cmdline_user_args():
		# Windows startup clamps oversized windows to the work area; request the
		# validation render size explicitly, without changing the display mode.
		get_window().min_size = Vector2i(1920, 1080)
		get_window().size = Vector2i(1920, 1080)
		await get_tree().create_timer(0.3).timeout
		await RenderingServer.frame_post_draw
		var overview_image: Image = get_viewport().get_texture().get_image()
		var overview_error := overview_image.save_png("res://docs/evidence/overview-1080.png")
		print("OVERVIEW %dx%d error=%d" % [overview_image.get_width(), overview_image.get_height(), overview_error])
		get_tree().quit(0 if overview_error == OK else 1)
	if "--capture" in OS.get_cmdline_user_args():
		await preload("res://scripts/capture_run.gd").new().run(self)
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
	ui_process_ticks += 1
	if get_tree().paused: return
	for actor in actors.values():
		actor.z_index = int(actor.position.y)
	shake_left = maxf(0, shake_left - delta)
	shake_phase += delta * 110.0
	var duration: float = manifest.impact.shake.duration_ms / 1000.0
	camera.offset = Vector2(sin(shake_phase), cos(shake_phase * 1.3)) * shake_strength * pow(shake_left / duration, manifest.impact.shake.decay) if shake_left > 0 and not reduced_motion else Vector2.ZERO
	grid_overlay.queue_redraw()

func draw_grid() -> void:
	if diagnostic:
		for y in range(9):
			for x in range(11):
				var points := PackedVector2Array([project(x,y), project(x+1,y), project(x+1,y+1), project(x,y+1), project(x,y)])
				var color := Color(0.6, 0.79, 0.74, 0.45) if Rules.walkable(Vector2i(x,y)) else Color(0.9, 0.48, 0.35, 0.65)
				grid_overlay.draw_polyline(points, color, 1.0, true)

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
	hud.process_mode = Node.PROCESS_MODE_ALWAYS
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
	action_button.grab_focus.call_deferred()
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
	players.clear()
	for unit in units:
		var actor := Node2D.new()
		actor.name = unit.id
		actor.position = center(unit.cell)
		world.add_child(actor)
		var ally: bool = unit.side == "ally"
		var body := Sprite2D.new()
		actor.add_child(body)
		body.name = "Body"
		var player := FramePlayer.new()
		actor.add_child(player)
		var character: String = "thoma" if ally else ("knight-a" if unit.id == "knight-1" else "knight-b")
		player.facing_right = index == 2 if ally else index != 2
		player.configure(manifest, character, body)
		players[unit.id] = player
		var flash_material := ShaderMaterial.new()
		flash_material.shader = preload("res://shaders/hit_flash.gdshader")
		flash_material.set_shader_parameter("flash", 0.0)
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

func event_plan(events: Array) -> Dictionary:
	# Group by causal role, retaining order within each group; unknown events are
	# ignored. Transport ordering never supplies magic [0]/[1]/[2] positions.
	var plan := {"attacks": [], "damage": [], "movement": [], "unknown": []}
	for event in events:
		match event.get("type", ""):
			"attack": plan.attacks.append(event)
			"damage": plan.damage.append(event)
			"knockback", "knockback_blocked": plan.movement.append(event)
			_: plan.unknown.append(event)
	return plan

func play_attack(event_override: Array = []) -> void:
	if busy: return
	select_setup(setup_index)
	var result: Dictionary = Rules.attack(units, "thoma", "knight-1")
	if not result.ok:
		status_label.text = result.reason
		return
	last_events = result.events if event_override.is_empty() else event_override
	current_plan = event_plan(last_events)
	if current_plan.attacks.is_empty(): return
	set_busy(true)
	contact_triggers.clear()
	var started := Time.get_ticks_usec()
	for attack in current_plan.attacks:
		var attacker_player = players[attack.unit]
		var listener := on_swing_frame.bind(attack)
		attacker_player.frame_entered.connect(listener)
		attacker_player.animation_event.connect(on_animation_event)
		set_phase("windup", "Anticipation")
		attacker_player.play("thoma.swing", reduced_motion)
		await contact_released
		for event in current_plan.movement:
			await play_movement(event, attack)
		# Both the weapon recovery and reaction must finish before input returns.
		while attacker_player.playing or players[attack.target].playing:
			await get_tree().process_frame
		attacker_player.frame_entered.disconnect(listener)
		attacker_player.animation_event.disconnect(on_animation_event)
	set_phase("settled", "Settled")
	await get_tree().create_timer(manifest.impact.settle_ms / 1000.0, false).timeout
	for player in players.values(): player.show_idle()
	units = result.units
	for actor in actors.values(): actor.get_node("Body").material.set_shader_parameter("flash", 0.0)
	camera.offset = Vector2.ZERO
	last_elapsed = (Time.get_ticks_usec() - started) / 1000000.0
	set_busy(false)
	set_phase("ready", "%s / %.3f s" % [SETUP_NAMES[setup_index], last_elapsed])
	print("SEQUENCE setup=%d reduced=%s elapsed_wall_s=%.4f limit=1.700 hp=%d cell=%s" % [setup_index+1, reduced_motion, last_elapsed, units[1].hp, units[1].cell])
	attack_finished.emit(last_elapsed)

func on_animation_event(event: Dictionary, at: Vector2) -> void:
	contact_point = at
	match event.type:
		"sfx":
			sound.play()
			contact_triggers.append({"type": "sfx", "frame": Engine.get_process_frames()})
		"spark":
			if not reduced_motion: emit_particles(at, false)
			contact_triggers.append({"type": "spark", "frame": Engine.get_process_frames(), "suppressed": reduced_motion})
		"dust":
			if not reduced_motion: emit_particles(at, true)

func on_swing_frame(index: int, attack: Dictionary) -> void:
	if index == 1 or (reduced_motion and index == 3): set_phase("lunge", "Swing")
	if index != int(manifest.sequences["thoma.swing"].contact_frame_index): return
	var target: Node2D = actors[attack.target]
	var material: ShaderMaterial = target.get_node("Body").material
	material.set_shader_parameter("flash", 0.0 if reduced_motion else 1.0)
	contact_triggers.append({"type": "flash", "frame": Engine.get_process_frames(), "suppressed": reduced_motion})
	for damage in current_plan.damage:
		hp_label.text = "KNIGHT I   %d / 6 HP" % damage.hp_after
		show_damage(contact_point, damage.amount)
	var scenario: Dictionary = manifest.scenarios[["open", "unit-blocked", "terrain-blocked"][setup_index]]
	players[attack.target].play(players[attack.target].character + "." + scenario.reaction, reduced_motion)
	if not reduced_motion: shake(manifest.impact.shake.strength_px)
	set_phase("contact", "Contact")
	await hold_contact()
	if not reduced_motion:
		var fade := target.create_tween()
		fade.tween_method(func(value: float): material.set_shader_parameter("flash", value), 1.0, 0.0, manifest.impact.flash_ms / 1000.0)
	contact_released.emit()

func hold_contact() -> void:
	var began := Time.get_ticks_usec()
	hold_active = true
	get_tree().paused = true
	await get_tree().create_timer(manifest.impact.hitstop_ms / 1000.0, true, false, true).timeout
	# SceneTreeTimer can be one scheduler quantum early. Never resume before the
	# specified real-time minimum, including on a fast headless runner.
	while Time.get_ticks_usec() - began < manifest.impact.hitstop_ms * 1000:
		await get_tree().process_frame
	last_hold_ms = (Time.get_ticks_usec() - began) / 1000.0
	get_tree().paused = false
	hold_active = false

func play_movement(event: Dictionary, attack: Dictionary) -> void:
	var target: Node2D = actors[event.unit]
	var origin := target.position
	var direction: Vector2 = (origin - actors[attack.unit].position).normalized()
	var reaction := target.create_tween()
	if event.type == "knockback":
		set_phase("knockback", "Giving ground")
		var duration: float = manifest.impact.reduced_knockback_ms if reduced_motion else manifest.impact.knockback_ms
		reaction.tween_property(target, "position", center(event.to), duration / 1000.0).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	else:
		set_phase("blocked", "Blocked")
		reaction.tween_property(target, "position", origin + direction * (0 if reduced_motion else manifest.impact.blocked_shove_px), manifest.impact.blocked_shove_ms / 1000.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		await reaction.finished
		set_phase("blocked_recoil", "Stagger")
		if not reduced_motion: emit_particles(origin + direction * 12, true)
		reaction = target.create_tween()
		reaction.tween_property(target, "position", origin, manifest.impact.blocked_recoil_ms / 1000.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	await reaction.finished

func set_busy(value: bool) -> void:
	busy = value
	action_button.disabled = value
	motion_button.disabled = value
	for button in setup_buttons:
		button.disabled = value
	action_button.text = "STRIKING…" if value else "REPLAY  /  SPACE"
	if not value:
		action_button.grab_focus()

func set_phase(value: String, text: String) -> void:
	phase = value
	status_label.text = text
	phase_changed.emit(value)

func shake(strength: float) -> void:
	shake_strength = strength
	shake_left = manifest.impact.shake.duration_ms / 1000.0
	shake_phase = 0
	# First offset is visible on the contact frame, then held during hitstop.
	camera.offset = Vector2(strength, -strength * 0.5) if not reduced_motion else Vector2.ZERO

func show_damage(at: Vector2, amount: int) -> void:
	var number := label_at(world, "−%d" % amount, at + Vector2(-12, -25), 27, BRASS)
	number.z_index = 1000
	number.add_theme_constant_override("outline_size", 7)
	var tween := number.create_tween().set_parallel(true)
	tween.tween_property(number, "position:y", number.position.y - (0 if reduced_motion else 30), 0.38).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(number, "modulate:a", 0.0, 0.20).set_delay(0.18)
	tween.chain().tween_callback(number.queue_free)

func emit_particles(at: Vector2, dust: bool) -> void:
	var particles := preload("res://scripts/anim/world_particles.gd").new()
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
	particles.preprocess = 0.016
	world.add_child(particles)
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
