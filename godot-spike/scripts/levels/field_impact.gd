extends Node
## Small field adapter; avoids extracting/changing Skirmish's validated timeline.
signal contact
signal contact_started
var battle
var profile: ImpactProfile
var crit := false
var sfx_trace: Array = []
var last_seconds := 0.0
var current_event := {}
var active := false
var process_seconds := 0.0

func _process(delta: float) -> void:
	if active: process_seconds+=delta

func _exit_tree() -> void:
	for voice in get_children():
		if voice is AudioStreamPlayer:
			voice.stop()
			voice.stream=null

func sound(hook: String) -> void:
	var voice := AudioStreamPlayer.new()
	voice.stream=preload("res://audio/impact_synth.gd").make_hook(hook)
	voice.volume_db=profile.whoosh_db if hook==profile.whoosh_hook else (profile.thud_db if hook in [profile.knockback_hook,profile.blocked_hook] else profile.impact_db)
	add_child(voice)
	voice.finished.connect(voice.queue_free)
	voice.play()
	sfx_trace.append({"hook":hook,"frame":Engine.get_process_frames()})

func particles(at: Vector2, direction: Vector2, dust: bool) -> void:
	var emitter := CPUParticles2D.new()
	emitter.position=at
	emitter.z_index=2000
	emitter.use_fixed_seed=profile.fixed_particle_seed
	emitter.seed=profile.particle_seed
	emitter.amount=roundi((profile.dust_count if dust else profile.spark_count)*(profile.crit_particle_multiplier if crit else 1.0))
	emitter.lifetime=profile.particle_lifetime_ms/1000
	emitter.one_shot=true
	emitter.explosiveness=1
	emitter.direction=Vector2.UP if dust else Vector2.UP.lerp(direction,profile.spark_direction_bias).normalized()
	emitter.spread=profile.particle_spread*(1.0 if dust else 1.0-.65*profile.spark_direction_bias)
	emitter.gravity=Vector2(0,profile.particle_gravity)
	emitter.initial_velocity_min=profile.dust_velocity_min if dust else profile.spark_velocity_min
	emitter.initial_velocity_max=profile.dust_velocity_max if dust else profile.spark_velocity_max
	emitter.scale_amount_min=profile.dust_scale_min if dust else profile.spark_scale_min
	emitter.scale_amount_max=profile.dust_scale_max if dust else profile.spark_scale_max
	emitter.color=profile.dust_color if dust else profile.spark_color
	emitter.preprocess=profile.particle_preprocess_ms/1000
	battle.world.add_child(emitter)
	emitter.finished.connect(emitter.queue_free)
	emitter.emitting=true
	if dust:
		var puff := Polygon2D.new()
		var points := PackedVector2Array()
		for i in range(18): points.append(Vector2.from_angle(i*TAU/18)*Vector2(profile.dust_puff_radius_px,profile.dust_puff_radius_px*profile.dust_puff_flatten))
		puff.polygon=points
		puff.position=at
		puff.color=Color(profile.dust_color,profile.dust_puff_alpha)
		battle.world.add_child(puff)
		var fade := puff.create_tween()
		fade.tween_property(puff,"modulate:a",0.0,profile.particle_lifetime_ms/1000)
		fade.tween_callback(puff.queue_free)
	else:
		var burst := Node2D.new()
		burst.position=at
		burst.z_index=2001
		battle.world.add_child(burst)
		var count := roundi(profile.spoke_count*(profile.crit_particle_multiplier if crit else 1.0))
		for i in range(count+1):
			var line := Line2D.new()
			var radial := Vector2.from_angle(i*TAU/maxi(1,count)+profile.spoke_angle)
			var dir := radial.lerp(direction.rotated((float(i)/maxi(count-1,1)-.5)*1.2),profile.spark_direction_bias).normalized()
			line.points=PackedVector2Array([-direction*profile.streak_length_px,direction*profile.streak_length_px]) if i==count else PackedVector2Array([dir*profile.spoke_inner_px,dir*(profile.spoke_outer_px+i%3*profile.spoke_variation_px)])
			line.width=profile.spoke_width
			line.default_color=profile.spoke_color
			burst.add_child(line)
		var fade := burst.create_tween()
		fade.tween_property(burst,"modulate:a",0.0,profile.spoke_fade_ms/1000)
		fade.tween_callback(burst.queue_free)

func number(at: Vector2, amount: int) -> void:
	var label: Label = battle.make_label(battle.world,"−%d" % amount,at+Vector2(profile.number_offset_x,profile.number_offset_y),profile.crit_number_font_px if crit else profile.number_font_px,profile.crit_number_color if crit else profile.number_color)
	label.z_index=2002
	label.add_theme_constant_override("outline_size",profile.number_outline_px)
	label.scale=Vector2.ONE*profile.number_scale*(profile.crit_number_scale_multiplier if crit else 1.0)
	var tween := label.create_tween().set_parallel(true)
	tween.tween_property(label,"scale",Vector2.ONE,profile.number_pop_ms/1000).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(label,"position:y",label.position.y-(0 if battle.reduced_motion else profile.number_rise_px),profile.number_lifetime_ms/1000)
	tween.tween_property(label,"modulate:a",0.0,profile.number_fade_ms/1000).set_delay(profile.number_fade_delay_ms/1000)
	tween.chain().tween_callback(label.queue_free)

func play(event: Dictionary, damage: Dictionary, movement: Dictionary) -> void:
	current_event=event.duplicate(true)
	active=true
	process_seconds=0
	var started := Time.get_ticks_usec()
	var attacker: Node2D = battle.actors[event.unit]
	var victim: Node2D = battle.actors[event.target]
	var player = battle.players[event.unit]
	var target_player = battle.players[event.target]
	var direction: Vector2 = (victim.position-attacker.position).normalized()
	var origin: Vector2 = victim.position
	battle.attack_focus((attacker.position+victim.position)/2)
	var swing: bool = player.character=="thoma" and event.kind!="ranged"
	var listener := func(index):
		if index==profile.whoosh_frame: sound(profile.whoosh_hook)
		if index==3: contact.emit()
	if swing:
		player.facing_right=direction.x>=0
		player.frame_entered.connect(listener)
		player.play("thoma.swing",battle.reduced_motion)
		await contact
	else:
		sound(profile.whoosh_hook)
		if event.kind=="ranged":
			var projectile := Line2D.new()
			projectile.points=PackedVector2Array([Vector2(-20,0),Vector2.ZERO])
			projectile.width=2
			projectile.default_color=Color("d2b777")
			projectile.position=attacker.position+Vector2(0,-50)
			projectile.rotation=direction.angle()
			battle.world.add_child(projectile)
			var fly := projectile.create_tween()
			fly.tween_property(projectile,"position",victim.position+Vector2(0,-50),.18/battle.playback_speed())
			await fly.finished
			projectile.queue_free()
		else:
			var lunge := attacker.create_tween()
			lunge.tween_method(player.set_visual_offset,Vector2.ZERO,direction*12,.12/battle.playback_speed())
			await lunge.finished
	var at: Vector2 = victim.position+Vector2(0,-55)
	var material: ShaderMaterial = victim.get_node("Body").material
	sound(profile.crit_hook if crit else profile.impact_hook)
	number(origin,damage.amount)
	battle.set_actor_hp(event.target,damage.hp_after)
	if target_player.character!="thoma": target_player.play(target_player.character+(".stagger" if movement.get("type")=="knockback_blocked" else ".hit"),battle.reduced_motion)
	if not battle.reduced_motion:
		material.set_shader_parameter("flash",1.0)
		target_player.set_visual_offset(direction*profile.recoil_px)
		particles(at,direction,false)
		if profile.dust_on_contact: particles(origin,direction,true)
		battle.impact_kick(direction,profile,crit)
	# Freeze pausable world including particles, frames and tweens; HUD stays live.
	get_tree().paused=true
	contact_started.emit()
	var hold_start := Time.get_ticks_usec()
	var process_ms := 0.0
	var minimum := profile.hitstop_ms(crit,battle.reduced_motion)
	while process_ms<minimum or (Time.get_ticks_usec()-hold_start)/1000.0<minimum:
		await get_tree().process_frame
		process_ms+=get_process_delta_time()*1000
	get_tree().paused=false
	if not battle.reduced_motion:
		var fade := victim.create_tween()
		fade.tween_interval(profile.flash_hold_ms/1000)
		fade.tween_method(func(value):material.set_shader_parameter("flash",value),1.0,0.0,profile.flash_ms/1000)
		victim.create_tween().tween_method(target_player.set_visual_offset,target_player.visual_offset,Vector2.ZERO,profile.recoil_ms/1000).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	if movement.get("type")=="knockback":
		await battle.animate_move(event.target,[movement.from,movement.to],profile.reduced_knockback_ms/1000 if battle.reduced_motion else profile.knockback_ms/1000)
		sound(profile.knockback_hook)
	elif movement.get("type")=="knockback_blocked":
		if not battle.reduced_motion:
			var shove := victim.create_tween()
			shove.tween_property(victim,"position",origin+direction*profile.blocked_shove_px,profile.blocked_shove_ms/1000)
			shove.tween_property(victim,"position",origin,profile.blocked_recoil_ms/1000)
			await shove.finished
		sound(profile.blocked_hook)
	while player.playing or target_player.playing: await get_tree().process_frame
	if swing: player.frame_entered.disconnect(listener)
	player.show_idle()
	target_player.show_idle()
	player.set_visual_offset(Vector2.ZERO)
	target_player.set_visual_offset(Vector2.ZERO)
	material.set_shader_parameter("flash",0.0)
	battle.attack_return()
	await get_tree().create_timer(profile.settle_ms/1000,false).timeout
	battle.camera.finish_return()
	last_seconds=(Time.get_ticks_usec()-started)/1000000.0
	active=false
	battle.attack_timings.append({"kind":event.kind,"reduced":battle.reduced_motion,"crit":crit,"wall_seconds":last_seconds,"process_seconds":process_seconds})
