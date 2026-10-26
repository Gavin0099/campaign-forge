extends "res://addons/gut/test.gd"
const Old = preload("res://config/impact_profile_spike05.tres")
const Current = preload("res://config/impact_profile.tres")
func test_only_flash_mix_changes_among_all_exported_impact_values() -> void:
	assert_almost_eq(Current.flash_mix,.5,.00001)
	assert_eq(Current.flash_hold_ms,0.0)
	assert_eq(Current.flash_ms,60.0)
	assert_almost_eq(Current.flash_mix*Current.crit_flash_multiplier,.6,.00001)
	for property in Current.get_property_list():
		if property.usage & PROPERTY_USAGE_SCRIPT_VARIABLE and property.name!="flash_mix": assert_eq(Current.get(property.name),Old.get(property.name),property.name)
func test_all_five_profiles_select_and_unknown_is_default() -> void:
	for suffix in ["a9_baseline","spike03","spike04","spike05",""]:
		var p := ImpactProfile.from_args(PackedStringArray([] if suffix=="" else ["--impact-profile="+suffix]))
		assert_eq(p.resource_path,"res://config/impact_profile"+("_"+suffix if suffix else "")+".tres")
	assert_eq(ImpactProfile.from_args(PackedStringArray(["--impact-profile=invalid"])),Current)

func test_threat_legend_is_visible_with_overlay_and_hidden_without() -> void:
	var field = add_child_autofree(preload("res://scenes/levels/Field24x18.tscn").instantiate())
	await get_tree().process_frame
	assert_false(field.hud.threat_legend.visible)
	field.threat_visible=true
	field.refresh()
	assert_true(field.hud.threat_legend.visible)
	assert_eq(field.hud.threat_legend.get_child_count(),6)
	assert_true(field.hud.threat_legend.get_child(5).text.contains("攔截"))
