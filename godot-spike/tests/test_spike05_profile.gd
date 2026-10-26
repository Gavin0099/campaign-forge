extends "res://addons/gut/test.gd"
const Old = preload("res://config/impact_profile_spike04.tres")
const Toned = preload("res://config/impact_profile_spike05.tres") # historical .6 byte-preserved

func test_flash_and_numbers_lower_but_other_layers_identical() -> void:
	assert_almost_eq(Toned.flash_mix,.6,.001)
	assert_lte(Toned.flash_mix*Toned.crit_flash_multiplier,.8)
	assert_lt(Toned.flash_hold_ms+Toned.flash_ms,Old.flash_hold_ms+Old.flash_ms)
	for key in ["number_font_px","crit_number_font_px"]: assert_between(float(Toned.get(key))/Old.get(key),.85,.9)
	for key in ["attacker_hitstop_ms","target_hitstop_ms","reduced_hitstop_ms","crit_hitstop_multiplier","directional_shake","shake_strength_px","shake_duration_ms","shake_decay","crit_shake_multiplier","recoil_px","recoil_ms","dust_count","dust_on_contact","dust_puff_alpha","zoom_punch","knockback_ms","layered_sfx","streak_length_px","spark_direction_bias"]: assert_eq(Toned.get(key),Old.get(key),key)
	assert_lt(Toned.spark_count,Old.spark_count)

func test_four_profiles_are_selectable_without_changing_unknown_arg_fallback() -> void:
	for suffix in ["a9_baseline","spike03","spike04",""]:
		var profile := ImpactProfile.from_args(PackedStringArray([] if suffix=="" else ["--impact-profile="+suffix]))
		assert_eq(profile.resource_path,"res://config/impact_profile"+("_"+suffix if suffix else "")+".tres")
	assert_eq(ImpactProfile.from_args(PackedStringArray(["--impact-profile=invalid"])),load("res://config/impact_profile.tres"))
