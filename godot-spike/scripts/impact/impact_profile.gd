class_name ImpactProfile
extends Resource
## Presentation only. Defaults reproduce A9; the tuned .tres overrides them.
## Milliseconds use pausable world time, except hitstop's guarded real-time clock.
@export_group("Hitstop")
@export_range(1, 250, 1) var attacker_hitstop_ms: float = 80
@export_range(1, 250, 1) var target_hitstop_ms: float = 80
@export_range(1, 250, 1) var reduced_hitstop_ms: float = 80
@export_range(1, 2, 0.001) var crit_hitstop_multiplier: float = 1
@export_group("Shake")
@export var directional_shake: bool = false
@export_range(0, 16, 0.1) var shake_strength_px: float = 3.4
@export_range(1, 400, 1) var shake_duration_ms: float = 200
@export_range(1, 8, 0.1) var shake_decay: float = 2
@export_range(2, 4, 1) var shake_cycles: float = 3
@export_range(1, 2, 0.01) var crit_shake_multiplier: float = 1
@export_range(1, 150, 1) var legacy_shake_frequency: float = 110
@export_range(1, 2, 0.1) var legacy_shake_y_frequency: float = 1.3
@export_range(-1, 1, 0.1) var legacy_first_y: float = -0.5
@export_group("Flash / visual recoil")
@export_range(0, 1, 0.01) var flash_mix: float = 0.65
@export var flash_color: Color = Color.WHITE
@export_range(0, 40, 0.1) var flash_hold_ms: float = 0
@export_range(1, 150, 1) var flash_ms: float = 35
@export_range(1, 2, 0.01) var crit_flash_multiplier: float = 1
@export_range(0, 12, 0.1) var recoil_px: float = 0
@export_range(1, 250, 1) var recoil_ms: float = 120
@export_group("Movement / settle")
@export_range(1, 400, 1) var knockback_ms: float = 220
@export_range(1, 200, 1) var reduced_knockback_ms: float = 30
@export_range(1, 150, 1) var blocked_shove_ms: float = 60
@export_range(1, 250, 1) var blocked_recoil_ms: float = 160
@export_range(0, 12, 0.1) var blocked_shove_px: float = 6
@export_range(0, 24, 0.1) var blocked_dust_offset_px: float = 12
@export_range(1, 250, 1) var settle_ms: float = 180
@export_group("Camera")
@export_range(1, 2, 0.01) var attack_zoom: float = 1.4
@export_range(1, 400, 1) var camera_in_ms: float = 240
@export_range(1, 300, 1) var camera_out_ms: float = 180
@export_range(0, 1, 0.01) var focus_weight: float = 0.52
@export_range(0, 0.1, 0.01) var zoom_punch: float = 0
@export_range(1, 200, 1) var zoom_punch_ms: float = 100
@export_group("Damage number")
@export var number_from_target: bool = false
@export_range(12, 40, 1) var number_font_px: int = 18
@export_range(12, 48, 1) var crit_number_font_px: int = 18
@export_range(-100, 100, 1) var number_offset_x: float = -8
@export_range(-120, 0, 1) var number_offset_y: float = -58
@export var number_color: Color = Color("d2b777")
@export var crit_number_color: Color = Color("dd9c7e")
@export var number_backing_color: Color = Color("101a19")
@export var number_backing: bool = true
@export_range(0, 8, 1) var number_margin_px: int = 3
@export_range(0, 8, 1) var number_outline_px: int = 3
@export_range(1, 2.2, 0.01) var number_scale: float = 1
@export_range(1, 1.3, 0.01) var crit_number_scale_multiplier: float = 1
@export_range(1, 250, 1) var number_pop_ms: float = 120
@export_range(0, 60, 1) var number_rise_px: float = 30
@export_range(1, 700, 1) var number_lifetime_ms: float = 380
@export_range(0, 500, 1) var number_fade_delay_ms: float = 180
@export_range(1, 400, 1) var number_fade_ms: float = 200
@export_group("Particles / immediate flare")
@export_range(0, 24, 1) var spoke_count: int = 7
@export_range(0, 4, 0.1) var spoke_width: float = 1.2
@export_range(0, 8, 1) var spoke_inner_px: float = 3
@export_range(1, 24, 1) var spoke_outer_px: float = 8
@export_range(0, 6, 1) var spoke_variation_px: float = 2
@export_range(0, 1, 0.1) var spoke_angle: float = 0.2
@export var spoke_color: Color = Color("d2b777")
@export_range(1, 250, 1) var spoke_fade_ms: float = 120
@export_range(0, 36, 1) var streak_length_px: float = 0
@export_range(1, 100, 1) var spark_count: int = 24
@export_range(1, 80, 1) var dust_count: int = 18
@export_range(1, 3, 0.1) var crit_particle_multiplier: float = 1
@export var dust_on_contact: bool = false
@export_range(1, 600, 1) var particle_lifetime_ms: float = 300
@export_range(0, 180, 1) var particle_spread: float = 100
## 0 preserves A9/spike03 upward spray; 1 aims sparks along attacker → target.
@export_range(0, 1, 0.01) var spark_direction_bias: float = 0
@export_range(0, 400, 1) var particle_gravity: float = 150
@export_range(0, 200, 1) var spark_velocity_min: float = 55
@export_range(0, 300, 1) var spark_velocity_max: float = 125
@export_range(0, 100, 1) var dust_velocity_min: float = 25
@export_range(0, 150, 1) var dust_velocity_max: float = 55
@export_range(0.1, 4, 0.1) var spark_scale_min: float = 0.6
@export_range(0.1, 6, 0.1) var spark_scale_max: float = 1.5
@export_range(0.1, 4, 0.1) var dust_scale_min: float = 1.4
@export_range(0.1, 6, 0.1) var dust_scale_max: float = 2.8
@export var spark_color: Color = Color("f3dca0")
@export var dust_color: Color = Color("aa956e")
@export_range(0, 40, 0.1) var particle_preprocess_ms: float = 16
@export var fixed_particle_seed: bool = false
@export_range(0, 2147483647, 1) var particle_seed: int = 90117
@export_range(1, 24, 1) var dust_puff_radius_px: float = 12
@export_range(0.1, 1, 0.01) var dust_puff_flatten: float = 0.35
@export_range(0, 1, 0.01) var dust_puff_alpha: float = 0.35
@export_group("SFX hooks / original placeholder synthesis")
@export var layered_sfx: bool = false
@export_enum("swing_whoosh") var whoosh_hook: String = "swing_whoosh"
@export_enum("impact") var impact_hook: String = "impact"
@export_enum("impact_crit") var crit_hook: String = "impact_crit"
@export_enum("knockback_thud") var knockback_hook: String = "knockback_thud"
@export_enum("blocked_thud") var blocked_hook: String = "blocked_thud"
@export_range(1, 2, 1) var whoosh_frame: int = 1
@export_range(-40, 0, 1) var whoosh_db: float = -14
@export_range(-40, 0, 1) var impact_db: float = -7
@export_range(-40, 0, 1) var crit_db: float = -6
@export_range(-40, 0, 1) var thud_db: float = -12

func hitstop_ms(crit: bool, reduced: bool) -> float:
	if reduced: return reduced_hitstop_ms
	return maxf(attacker_hitstop_ms,target_hitstop_ms) * (crit_hitstop_multiplier if crit else 1.0)

static func from_args(args: PackedStringArray) -> ImpactProfile:
	for arg in args:
		if arg == "--impact-profile=a9_baseline": return load("res://config/impact_profile_a9_baseline.tres")
		if arg == "--impact-profile=spike03": return load("res://config/impact_profile_spike03.tres")
	return load("res://config/impact_profile.tres")
