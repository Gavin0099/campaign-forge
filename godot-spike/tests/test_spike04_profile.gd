extends "res://addons/gut/test.gd"
const Old = preload("res://config/impact_profile_spike03.tres")
## W4: historical spike04 profile pins now reference the byte-preserved resource.
const Toned = preload("res://config/impact_profile_spike04.tres")

func test_toned_values_and_preserved_contact_layers() -> void:
	assert_almost_eq(Toned.flash_mix,0.8,0.02)
	assert_lt(Toned.spark_count,Old.spark_count)
	assert_lt(Toned.spoke_count,Old.spoke_count)
	assert_lte(Toned.crit_particle_multiplier,1.35)
	assert_gt(Toned.spark_direction_bias,0.0)
	assert_lte(Toned.flash_mix,1.0)
	for key in ["number_font_px","crit_number_font_px"]:
		assert_between(float(Toned.get(key))/Old.get(key),0.85,0.9)
	for key in ["attacker_hitstop_ms","target_hitstop_ms","reduced_hitstop_ms","crit_hitstop_multiplier","shake_strength_px","crit_shake_multiplier","shake_duration_ms","recoil_px","recoil_ms","dust_on_contact","dust_count","zoom_punch","knockback_ms","streak_length_px","layered_sfx"]:
		assert_eq(Toned.get(key),Old.get(key),key)

func test_all_three_profiles_select_with_user_args() -> void:
	for suffix in ["a9_baseline","spike03",""]:
		var args := PackedStringArray([] if suffix.is_empty() else ["--impact-profile="+suffix])
		var profile := ImpactProfile.from_args(args)
		assert_true(profile is ImpactProfile)
		assert_eq(profile.resource_path,"res://config/impact_profile"+("_"+suffix if suffix else "")+".tres")
	assert_eq(Old.spark_direction_bias,0.0,"old profiles retain radial/upward emission")
