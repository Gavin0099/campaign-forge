extends Camera2D
## Three independent layers: base (pan/follow), attack focus, impact offset only.
var battle
const STEPS = [0.8,1.0,1.2]
const VIEW = Vector2(1280,720)
var base_position := Vector2.ZERO
var base_zoom := 1.0
var zoom_index := 1
var overview := false
var overview_saved := {}
var edge_scroll := false
var dragging := false
var pan_speed := 620.0
var keys := {}
var interactive := true
var focus_offset := Vector2.ZERO
var focus_zoom := 1.0
var attack_saved := {}
var focusing := false
var follow_tween: Tween
var focus_tween: Tween
var shake_remaining := 0.0
var shake_direction := Vector2.RIGHT
var shake_strength := 0.0
var shake_profile: ImpactProfile
var punch := 0.0

func clamp_at(at: Vector2, zoom_value: float = -1) -> Vector2:
	var bounds: Rect2 = battle.world_bounds()
	var half := VIEW/(zoom.x if zoom_value<0 else zoom_value)/2
	var clamped := at
	for axis in range(2):
		clamped[axis]=bounds.get_center()[axis] if half[axis]*2>=bounds.size[axis] else clampf(at[axis],bounds.position[axis]+half[axis],bounds.end[axis]-half[axis])
	return clamped

func sync() -> void:
	zoom=Vector2.ONE*(focus_zoom+punch if focusing else base_zoom)
	base_position=clamp_at(base_position,base_zoom)
	position=clamp_at(base_position+focus_offset)
	var raw := Vector2.ZERO
	if shake_remaining>0 and not battle.reduced_motion and shake_profile!=null:
		var t := 1.0-shake_remaining/(shake_profile.shake_duration_ms/1000)
		raw=shake_direction*shake_strength*cos(TAU*shake_profile.shake_cycles*t)*exp(-shake_profile.shake_decay*t)
	offset=clamp_at(position+raw)-position
	force_update_scroll()

func pan_to(at: Vector2) -> void:
	if follow_tween: follow_tween.kill()
	base_position=clamp_at(at,base_zoom)
	sync()

func follow(at: Vector2) -> void:
	if overview: toggle_overview()
	if follow_tween: follow_tween.kill()
	if battle.reduced_motion:
		pan_to(at)
		return
	follow_tween=create_tween()
	follow_tween.tween_property(self,"base_position",clamp_at(at,base_zoom),.22).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)

func toggle_overview() -> void:
	if focusing: return
	if follow_tween: follow_tween.kill()
	if not overview:
		overview_saved={"position":base_position,"zoom":base_zoom,"index":zoom_index}
		overview=true
		var bounds: Rect2 = battle.world_bounds()
		base_zoom=minf(1180/bounds.size.x,430/bounds.size.y)
		base_position=bounds.get_center()
	else:
		overview=false
		base_zoom=overview_saved.zoom
		zoom_index=overview_saved.index
		base_position=overview_saved.position
	sync()

func wheel(step: int, cursor: Vector2) -> void:
	if focusing: return
	if overview: toggle_overview()
	var before := screen_to_world(cursor)
	zoom_index=clampi(zoom_index+step,0,STEPS.size()-1)
	base_zoom=STEPS[zoom_index]
	base_position=before-(cursor-VIEW/2)/base_zoom
	sync()

func screen_to_world(screen: Vector2) -> Vector2:
	return position+offset+(screen-VIEW/2)/zoom

func begin_attack(at: Vector2, profile: ImpactProfile) -> void:
	if follow_tween: follow_tween.kill()
	attack_saved={"position":base_position,"zoom":base_zoom,"overview":overview}
	if battle.reduced_motion: return
	focusing=true
	focus_zoom=base_zoom
	focus_offset=Vector2.ZERO
	if focus_tween: focus_tween.kill()
	focus_tween=create_tween().set_parallel(true)
	focus_tween.tween_property(self,"focus_offset",(at-base_position)*profile.focus_weight,profile.camera_in_ms/1000).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	focus_tween.tween_property(self,"focus_zoom",base_zoom*profile.attack_zoom,profile.camera_in_ms/1000)

func end_attack() -> void:
	if focus_tween: focus_tween.kill()
	if attack_saved.is_empty(): return
	# Return targets the exact pre-attack base, never a fixed canvas centre.
	base_position=attack_saved.position
	base_zoom=attack_saved.zoom
	shake_remaining=0
	punch=0
	if battle.reduced_motion:
		focusing=false
		focus_offset=Vector2.ZERO
		sync()
		return
	focus_tween=create_tween().set_parallel(true)
	focus_tween.tween_property(self,"focus_offset",Vector2.ZERO,.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	focus_tween.tween_property(self,"focus_zoom",base_zoom,.18)
	focus_tween.chain().tween_callback(func():
		focusing=false
		focus_offset=Vector2.ZERO
		sync())

func kick(direction: Vector2, profile: ImpactProfile, crit: bool) -> void:
	if battle.reduced_motion: return
	shake_profile=profile
	shake_direction=direction
	shake_strength=profile.shake_strength_px*(profile.crit_shake_multiplier if crit else 1.0)
	shake_remaining=profile.shake_duration_ms/1000
	punch=profile.zoom_punch
	sync()
	create_tween().tween_property(self,"punch",0.0,profile.zoom_punch_ms/1000)

func finish_return() -> void:
	if focus_tween: focus_tween.kill()
	focusing=false
	focus_offset=Vector2.ZERO
	shake_remaining=0
	punch=0
	sync()

func _process(delta: float) -> void:
	if get_tree().paused: return
	if interactive and not focusing and not dragging:
		var move := Vector2(float(keys.has(KEY_D) or keys.has(KEY_RIGHT))-float(keys.has(KEY_A) or keys.has(KEY_LEFT)),float(keys.has(KEY_S) or keys.has(KEY_DOWN))-float(keys.has(KEY_W) or keys.has(KEY_UP)))
		if edge_scroll and DisplayServer.window_is_focused():
			var mouse := get_viewport().get_mouse_position()
			if Rect2(0,112,1280,450).has_point(mouse): move+=Vector2(float(mouse.x>1264)-float(mouse.x<16),float(mouse.y>546)-float(mouse.y<128))
		if move!=Vector2.ZERO: pan_to(base_position+move.normalized()*pan_speed*delta/base_zoom)
	shake_remaining=maxf(0,shake_remaining-delta)
	sync()

func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_FOCUS_OUT:
		keys.clear()
		dragging=false

func _input(event: InputEvent) -> void:
	if not interactive: return
	if event is InputEventKey:
		if event.keycode in [KEY_W,KEY_A,KEY_S,KEY_D,KEY_UP,KEY_LEFT,KEY_DOWN,KEY_RIGHT]:
			if event.pressed: keys[event.keycode]=true
			else: keys.erase(event.keycode)
			get_viewport().set_input_as_handled()
		if event.pressed and not event.echo:
			match event.keycode:
				KEY_O:
					toggle_overview()
					get_viewport().set_input_as_handled()
				KEY_F,KEY_HOME:
					if overview: toggle_overview()
					follow(battle.center(battle.Rules.unit(battle.state,battle.selected_id).cell))
					get_viewport().set_input_as_handled()
				KEY_E:
					edge_scroll=not edge_scroll
					battle.hud.camera_hints.text="WASD／方向鍵 捲動 · 中鍵 拖曳 · 滾輪 縮放 · O 全圖 · F 定位 · E 邊緣 "+("ON" if edge_scroll else "OFF")
	if event is InputEventMouseButton:
		if event.button_index==MOUSE_BUTTON_MIDDLE:
			dragging=event.pressed
			if follow_tween: follow_tween.kill()
			get_viewport().set_input_as_handled()
		if event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP,MOUSE_BUTTON_WHEEL_DOWN] and event.position.y>110 and event.position.y<570:
			wheel(1 if event.button_index==MOUSE_BUTTON_WHEEL_UP else -1,event.position)
			get_viewport().set_input_as_handled()
	if event is InputEventMouseMotion and dragging and not focusing:
		pan_to(base_position-event.relative/base_zoom)
		get_viewport().set_input_as_handled()
