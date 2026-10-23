extends RefCounted
## Engine-side validation. No scene nodes and no combat decisions.
const ROOT := "res://art/anim-shared/"
var data: Dictionary = {}
var errors: Array[String] = []

func read(path: String = ROOT + "manifest.json") -> bool:
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		errors.assign(["manifest must be a JSON object"])
		push_error(errors[0])
		return false
	var valid := validate(parsed)
	if not valid:
		push_error("Invalid animation manifest: " + "; ".join(errors))
	return valid

func positive_int(value: Variant) -> bool:
	return (value is int or value is float) and value > 0 and value == floor(value)

func point(value: Variant) -> bool:
	return value is Array and value.size() == 2 and (value[0] is float or value[0] is int) and (value[1] is float or value[1] is int)

func number_between(value: Variant, low: float, high: float) -> bool:
	return (value is int or value is float) and value >= low and value <= high

func validate(candidate: Dictionary, check_files: bool = true) -> bool:
	errors.clear()
	data = {}
	for key in ["version", "characters", "sequences", "impact", "camera", "scenarios"]:
		if not candidate.has(key): errors.append("missing " + key)
	if not errors.is_empty(): return false
	if candidate.version != 1: errors.append("unsupported version")
	for key in ["characters", "sequences", "impact", "camera", "scenarios"]:
		if not candidate[key] is Dictionary or candidate[key].is_empty(): errors.append(key + " must be a nonempty object")
	if not errors.is_empty(): return false
	for id in candidate.characters:
		var c = candidate.characters[id]
		if not c is Dictionary or not point(c.get("canvas_size")) or not point(c.get("pivot")) or not positive_int(c.get("reference_height_px")) or c.get("facing") not in ["left", "right"]:
			errors.append("invalid character " + id)
	for id in candidate.sequences:
		var s = candidate.sequences[id]
		if not s is Dictionary or not s.get("frames") is Array or s.get("frames", []).is_empty() or s.get("loop", true) != false or not candidate.characters.has(s.get("character", "")):
			errors.append("invalid sequence " + id)
			continue
		for f in s.frames:
			if not f is Dictionary or not positive_int(f.get("duration_ms")) or not f.get("path") is String:
				errors.append("invalid frame in " + id)
				continue
			var path: String = f.path
			if path.is_absolute_path() or ".." in path or not path.ends_with(".png") or (check_files and not FileAccess.file_exists(ROOT + path)):
				errors.append("invalid/missing frame path " + path)
			if f.has("offset") and not point(f.offset): errors.append("invalid frame offset")
		if id.ends_with(".swing") and not s.has("contact_frame_index"): errors.append("swing missing contact index")
		if s.has("contact_frame_index") and not valid_index(s.contact_frame_index, s.frames.size()): errors.append("contact index out of range")
		for event in s.get("events", []):
			if not event is Dictionary or not valid_index(event.get("frame"), s.frames.size()) or event.get("type") not in ["sfx", "spark", "dust"] or not point(event.get("anchor")):
				errors.append("invalid sequence event")
		for index in s.get("reduced_frame_indices", []):
			if not valid_index(index, s.frames.size()): errors.append("invalid reduced frame index")
		if s.has("reduced_frame_indices") and not positive_int(s.get("reduced_duration_ms")): errors.append("missing reduced duration")
	for key in ["hitstop_ms", "flash_ms", "knockback_ms", "blocked_shove_ms", "blocked_recoil_ms", "blocked_shove_px", "settle_ms", "reduced_knockback_ms"]:
		if not positive_int(candidate.impact.get(key)): errors.append("invalid impact " + key)
	var shake = candidate.impact.get("shake", {})
	if not shake is Dictionary or not positive_int(shake.get("duration_ms")) or not (shake.get("strength_px") is float or shake.get("strength_px") is int) or not positive_int(shake.get("decay")):
		errors.append("invalid shake")
	if not positive_int(candidate.camera.get("in_ms")) or not positive_int(candidate.camera.get("out_ms")) or candidate.camera.get("focus") != "attacker_target_midpoint" or not number_between(candidate.camera.get("zoom"),1,2) or not number_between(candidate.camera.get("focus_weight"),0,1):
		errors.append("invalid camera")
	for key in ["open", "unit-blocked", "terrain-blocked"]:
		var scenario = candidate.scenarios.get(key, {})
		if not scenario is Dictionary or not valid_index(scenario.get("setup_index"), 3) or scenario.get("reaction") not in ["hit", "stagger"] or scenario.get("movement") not in ["knockback", "knockback_blocked"]:
			errors.append("invalid scenario " + key)
	if errors.is_empty(): data = candidate.duplicate(true)
	return errors.is_empty()

func valid_index(value: Variant, count: int) -> bool:
	return (value is float or value is int) and value == floor(value) and value >= 0 and value < count
