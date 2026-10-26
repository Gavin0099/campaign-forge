extends Node2D
signal action_finished
signal state_changed
const Rules = preload("res://scripts/rules/field_rules.gd")
const FramePlayer = preload("res://scripts/anim/frame_player.gd")
const Manifest = preload("res://scripts/anim/anim_manifest.gd")
const HALF = Vector2(80,47.25)
const BONE = Color("eee7d6")
const BRASS = Color("d2b777")
const TEAL = Color("98c9be")
const CLAY = Color("dd9c7e")
var state := Rules.initial()
var actors := {}
var players := {}
var props: Array = []
var world: Node2D
var ground: Node2D
var camera: Camera2D
var hud
var impact
var manifest := {}
var selected_id := "thoma"
var cursor_cell := Vector2i(3,9)
var move_cells := {}
var attack_targets: Array = []
var threat_cells := {}
var preview_path: Array = []
var pending := {}
var busy := false
var reduced_motion := false
var fast_forward := false
var skip_enemy_movement := false
var grid_visible := true
var threat_visible := false
var debug_visible := false
var next_crit := false
var attack_timings: Array = []
var enemy_times: Array = []
var last_events: Array = []
var telemetry = preload("res://scripts/levels/field_telemetry.gd").new()

func center(cell: Vector2i) -> Vector2:
	return Vector2(state.level.size.y*HALF.x+(cell.x-cell.y)*HALF.x,(cell.x+cell.y+1)*HALF.y)

func diamond(cell: Vector2i) -> PackedVector2Array:
	var p := center(cell)
	return PackedVector2Array([p+Vector2(0,-HALF.y),p+Vector2(HALF.x,0),p+Vector2(0,HALF.y),p-Vector2(HALF.x,0)])

func world_cell(at: Vector2) -> Vector2i:
	var x: float = (at.x-state.level.size.y*HALF.x)/HALF.x
	var y := at.y/HALF.y
	return Vector2i(floori((x+y)/2),floori((y-x)/2))

func world_bounds() -> Rect2:
	# Empty perimeter is part of the authored navigable bounds: HUD-safe access
	# to edge tiles without ever exposing outside the battlefield camera bounds.
	return Rect2(Vector2(-120,-180),HALF*(state.level.size.x+state.level.size.y)+Vector2(240,360))

func make_label(parent: Node, text: String, at: Vector2, size: int, color: Color = BONE) -> Label:
	var label := Label.new()
	label.text=text
	label.position=at
	label.mouse_filter=Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size",size)
	label.add_theme_color_override("font_color",color)
	label.add_theme_color_override("font_outline_color",Color("101a19"))
	label.add_theme_constant_override("outline_size",3)
	parent.add_child(label)
	return label

func display_name(u: Dictionary) -> String:
	return "托瑪" if u.id=="thoma" else ("領袖" if u.kind=="leader" else u.id)

func kind_name(kind: String) -> String:
	return {"melee":"近戰 ⚔","ranged":"弓手 〉","mobile":"斥候 ⇥","knight":"騎士 ×","leader":"領袖 ◆"}[kind]

func _ready() -> void:
	process_mode=Node.PROCESS_MODE_ALWAYS
	var loader := Manifest.new()
	if not loader.read():
		get_tree().quit(1)
		return
	manifest=loader.data
	world=Node2D.new()
	world.process_mode=Node.PROCESS_MODE_PAUSABLE
	add_child(world)
	ground=preload("res://scripts/levels/field_ground.gd").new()
	ground.battle=self
	world.add_child(ground)
	camera=preload("res://scripts/levels/field_camera.gd").new()
	camera.battle=self
	world.add_child(camera)
	impact=preload("res://scripts/levels/field_impact.gd").new()
	impact.battle=self
	impact.profile=ImpactProfile.from_args(OS.get_cmdline_user_args())
	add_child(impact)
	build_props()
	build_units()
	hud=preload("res://scripts/levels/field_hud.gd").new()
	hud.battle=self
	add_child(hud)
	pan_to(center(cursor_cell))
	telemetry.register(state,"ally")
	refresh()

func build_props() -> void:
	for specification in [["bank",Vector2i(15,8),Vector2(.7,.7)],["bank",Vector2i(15,11),Vector2(.7,.7)],["crossing",Vector2i(15,9),Vector2.ONE]]:
		var chunk := Sprite2D.new()
		chunk.texture=load("res://art/bigmap/"+specification[0]+".png")
		chunk.position=center(specification[1])
		chunk.scale=specification[2]
		world.add_child(chunk)
	for specification in [["tree",Vector2i(8,5)],["tree",Vector2i(11,6)],["tree",Vector2i(9,14)],["tree",Vector2i(12,13)],["rock",Vector2i(16,7)],["rock",Vector2i(6,12)],["banner",Vector2i(20,9)]]:
		var prop := Sprite2D.new()
		prop.texture=load("res://art/bigmap/"+specification[0]+".png")
		prop.centered=false
		prop.offset=Vector2(-80,-195)
		prop.position=center(specification[1])+Vector2(25,12)
		prop.z_index=int(prop.position.y)
		world.add_child(prop)
		props.append(prop)

func build_units() -> void:
	for actor in actors.values(): actor.free()
	actors.clear()
	players.clear()
	for u in state.units:
		if u.hp<=0: continue
		var actor := Node2D.new()
		actor.position=center(u.cell)
		actor.z_index=int(actor.position.y)
		world.add_child(actor)
		var base := Polygon2D.new()
		base.polygon=PackedVector2Array([Vector2(-26,0),Vector2(0,-10),Vector2(26,0),Vector2(0,10)]) if u.side=="enemy" else PackedVector2Array([Vector2(-24,-5),Vector2(24,-5),Vector2(24,6),Vector2(-24,6)])
		base.color=Color(TEAL if u.side=="ally" else CLAY,.55)
		actor.add_child(base)
		var body := Sprite2D.new()
		body.name="Body"
		actor.add_child(body)
		var material := ShaderMaterial.new()
		material.shader=preload("res://shaders/hit_flash.gdshader")
		material.set_shader_parameter("flash",0.0)
		material.set_shader_parameter("flash_mix",impact.profile.flash_mix)
		material.set_shader_parameter("flash_color",impact.profile.flash_color)
		body.material=material
		var player := FramePlayer.new()
		player.pixels_per_frame_pixel=96.0/360.0
		player.facing_right=u.side=="ally"
		actor.add_child(player)
		player.configure(manifest,"thoma" if u.side=="ally" else ("knight-a" if u.id.hash()%2==0 else "knight-b"),body)
		var badge: String = {"melee":"M","ranged":"BOW 〉","mobile":"BOOT ⇥","knight":"×","leader":"◆ LEADER"}[u.kind]
		var tag := make_label(actor,badge,Vector2(-66,-68),14,TEAL if u.side=="ally" else CLAY)
		tag.name="Badge"
		var hp := make_label(actor,"%d/%d" % [u.hp,u.max_hp],Vector2(-22,-112),14)
		hp.name="HP"
		actors[u.id]=actor
		players[u.id]=player

func refresh() -> void:
	move_cells.clear()
	attack_targets.clear()
	threat_cells.clear()
	var u := Rules.unit(state,selected_id)
	if not busy and Rules.allowed(state,u) and u.side=="ally":
		if not u.moved: move_cells=Rules.reach(state,selected_id).costs
		attack_targets=Rules.targets(state,selected_id)
	if threat_visible:
		for enemy in state.units:
			if enemy.side!="enemy" or enemy.hp<=0: continue
			threat_cells.merge(Rules.threat(state,enemy.id))
	ground.queue_redraw()
	hud.update_state()
	hud.hover(cursor_cell)
	state_changed.emit()

func select_unit(id: String) -> void:
	if busy: return
	var u := Rules.unit(state,id)
	if u.is_empty() or u.hp<=0: return
	selected_id=id
	cursor_cell=u.cell
	cancel()
	camera.follow(center(u.cell))

func cancel() -> void:
	pending.clear()
	preview_path.clear()
	refresh()

func choose(cell: Vector2i) -> void:
	if busy or state.status!="playing" or not Rules.inside(state.level,cell): return
	cursor_cell=cell
	var u := Rules.occupant(state,cell)
	if not u.is_empty() and u.side=="ally":
		select_unit(u.id)
		return
	if not u.is_empty() and u.id in attack_targets:
		if pending.get("target")==u.id:
			confirm()
			return
		pending={"type":"attack","target":u.id}
		preview_path.clear()
		var info := Rules.attack_info(state,Rules.unit(state,selected_id),u)
		hud.notice.text="攻擊：%s → %s　傷害 %d · %s　Enter 確認" % [selected_id,display_name(u),info.damage,info.reason]
	elif move_cells.has(cell) and Rules.unit(state,selected_id).cell!=cell:
		if pending.get("to")==cell:
			confirm()
			return
		pending={"type":"move","to":cell}
		preview_path=Rules.path_to(Rules.reach(state,selected_id),Rules.unit(state,selected_id).cell,cell)
		hud.notice.text="移動成本 %d／%d　Enter／再點確認；Esc 取消" % [move_cells[cell],state.level.stats[Rules.unit(state,selected_id).kind].move]
	else:
		cancel()
	refresh()

func confirm() -> void:
	if busy or pending.is_empty(): return
	var command := pending.duplicate(true)
	var resolved := Rules.move(state,selected_id,command.to) if command.type=="move" else Rules.attack(state,selected_id,command.target)
	await accept(resolved)

func wait_selected() -> void:
	if busy: return
	await accept(Rules.wait(state,selected_id))

func accept(resolved: Dictionary) -> void:
	if busy or not resolved.ok: return
	telemetry.record(state,resolved.events,resolved.state)
	busy=true
	pending.clear()
	preview_path.clear()
	last_events=resolved.events.duplicate(true)
	refresh()
	await play_events(resolved.events)
	state=resolved.state
	busy=false
	build_units()
	refresh()
	telemetry.write("res://.godot/spike04/live-telemetry.json")
	action_finished.emit()

func playback_speed() -> float:
	return 2.0 if fast_forward or Input.is_key_pressed(KEY_SHIFT) else 1.0

func animate_move(id: String, path: Array, total_seconds: float = -1) -> void:
	if not actors.has(id): return
	var actor: Node2D = actors[id]
	if reduced_motion or (state.phase=="enemy" and skip_enemy_movement):
		actor.position=center(path.back())
		await get_tree().process_frame
		return
	var duration: float = .075 if total_seconds<0 else total_seconds/maxi(path.size()-1,1)
	var tween := actor.create_tween()
	for cell in path.slice(1): tween.tween_property(actor,"position",center(cell),duration/playback_speed()).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	await tween.finished

func set_actor_hp(id: String, hp: int) -> void:
	if actors.has(id): actors[id].get_node("HP").text=str(hp)+"/"+str(Rules.unit(state,id).max_hp)

func play_events(events: Array) -> void:
	for i in range(events.size()):
		var event: Dictionary = events[i]
		hud.on_event(event)
		match event.type:
			"phase":
				state.phase=event.phase
				hud.notice.text="敵方回合　B／Shift 加速 · X 略過移動" if event.phase=="enemy" else "我方回合"
				hud.update_state()
			"move":
				if state.phase=="player": camera.follow(center(event.path.back()))
				await animate_move(event.unit,event.path)
			"intent":
				if event.state!="guard": hud.notice.text="%s：%s" % [event.unit,event.get("reason",event.state)]
			"attack":
				if state.phase=="enemy":
					hud.notice.text="敵方攻擊：%s → %s" % [event.unit,event.target]
					camera.follow(actors[event.target].position)
					if not reduced_motion: await get_tree().create_timer(.24/playback_speed(),false).timeout
				var damage: Dictionary = events[i+1]
				var movement: Dictionary = events[i+2] if i+2<events.size() and events[i+2].type in ["knockback","knockback_blocked"] else {}
				impact.crit=next_crit
				next_crit=false
				await impact.play(event,damage,movement)
			"reinforcement_warning":
				hud.notice.text="增援預告：第 %d 回合，東北入口，3 名騎士；到場當回合不行動" % event.turn
				camera.follow(center(event.entries[0]))
			"reinforcement_arrival":
				hud.notice.text="增援到場：%s（本回合休息）" % event.unit
				camera.follow(center(event.cell))

func end_turn() -> void:
	if busy or state.status!="playing": return
	var started := Time.get_ticks_usec()
	var resolved := Rules.enemy_phase(state)
	await accept(resolved)
	var metric := {"turn":state.turn-1,"seconds":(Time.get_ticks_usec()-started)/1000000.0,"fast":fast_forward,"skip_move":skip_enemy_movement}
	enemy_times.append(metric)
	telemetry.enemy_phases.append(metric)
	telemetry.write("res://.godot/spike04/live-telemetry.json")

func restart() -> void:
	if busy: return
	state=Rules.initial()
	selected_id="thoma"
	cursor_cell=Rules.unit(state,"thoma").cell
	pending.clear()
	preview_path.clear()
	attack_timings.clear()
	enemy_times.clear()
	telemetry=preload("res://scripts/levels/field_telemetry.gd").new()
	telemetry.register(state,"ally")
	hud.warning.clear()
	build_units()
	pan_to(center(cursor_cell))
	hud.notice.text="重新部署：主道路或北側森林淺灘"
	refresh()

func pan_to(at: Vector2) -> void:
	camera.pan_to(at)

func attack_focus(at: Vector2) -> void:
	camera.begin_attack(at,impact.profile)

func attack_return() -> void:
	camera.end_attack()

func impact_kick(direction: Vector2, profile: ImpactProfile, crit: bool) -> void:
	camera.kick(direction,profile,crit)

func _process(_delta: float) -> void:
	if get_tree().paused: return
	for actor in actors.values(): actor.z_index=int(actor.position.y)
	for prop in props:
		var occluded := false
		for actor in actors.values():
			if absf(actor.position.x-prop.position.x)<58 and actor.position.y<prop.position.y and actor.position.y>prop.position.y-150: occluded=true
		prop.modulate.a=.32 if occluded else 1.0
	if debug_visible: hud.update_state()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT and event.pressed and camera.overview:
		var clicked := world_cell(world.get_global_transform_with_canvas().affine_inverse()*event.position)
		camera.toggle_overview()
		if Rules.inside(state.level,clicked):
			camera.follow(center(clicked))
			var u := Rules.occupant(state,clicked)
			if not u.is_empty() and u.side=="ally": select_unit(u.id)
		return
	if event is InputEventMouseButton and event.pressed:
		if event.button_index==MOUSE_BUTTON_RIGHT and not busy: cancel()
		if event.button_index==MOUSE_BUTTON_LEFT: choose(world_cell(world.get_global_transform_with_canvas().affine_inverse()*event.position))
	if event is InputEventMouseMotion:
		var cell := world_cell(world.get_global_transform_with_canvas().affine_inverse()*event.position)
		if Rules.inside(state.level,cell): hud.hover(cell)
	if not event is InputEventKey or not event.pressed or event.echo: return
	match event.keycode:
		KEY_B: fast_forward=not fast_forward
		KEY_X: skip_enemy_movement=not skip_enemy_movement
		KEY_F1: debug_visible=not debug_visible
		KEY_P: hud.toggle_minimap()
	if busy: return
	match event.keycode:
		KEY_TAB:
			var allies: Array = state.units.filter(func(u):return u.side=="ally" and u.hp>0)
			var index := allies.find(Rules.unit(state,selected_id))
			select_unit(allies[(index+1)%allies.size()].id)
		KEY_I,KEY_J,KEY_K,KEY_L:
			var direction: Vector2i = {KEY_I:Vector2i.UP,KEY_J:Vector2i.LEFT,KEY_K:Vector2i.DOWN,KEY_L:Vector2i.RIGHT}[event.keycode]
			cursor_cell=(cursor_cell+direction).clamp(Vector2i.ZERO,state.level.size-Vector2i.ONE)
			ground.queue_redraw()
			hud.hover(cursor_cell)
		KEY_T:
			if not attack_targets.is_empty():
				var index: int = attack_targets.find(pending.get("target",""))
				choose(Rules.unit(state,attack_targets[(index+1)%attack_targets.size()]).cell)
		KEY_ENTER,KEY_KP_ENTER:
			if pending.is_empty(): choose(cursor_cell)
			else: confirm()
		KEY_SPACE: wait_selected()
		KEY_N: end_turn()
		KEY_ESCAPE: cancel()
		KEY_G: grid_visible=not grid_visible
		KEY_V: threat_visible=not threat_visible
		KEY_M: reduced_motion=not reduced_motion
		KEY_C: next_crit=not next_crit
		KEY_R: restart()
	refresh()

func _input(event: InputEvent) -> void:
	# Tactical keys own both edges so a focused Button cannot also confirm them.
	if event is InputEventKey and event.keycode in [KEY_TAB,KEY_I,KEY_J,KEY_K,KEY_L,KEY_T,KEY_ENTER,KEY_KP_ENTER,KEY_SPACE,KEY_N,KEY_ESCAPE,KEY_G,KEY_V,KEY_M,KEY_C,KEY_R,KEY_B,KEY_X,KEY_F1,KEY_P]:
		if state.status!="playing" and event.keycode not in [KEY_R,KEY_F1]: return
		get_viewport().set_input_as_handled()
		_unhandled_input(event)
