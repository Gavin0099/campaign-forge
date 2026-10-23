extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const EVIDENCE = "res://docs/evidence/spike02-a3/"

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func png_bytes(path: String) -> Image:
	var image := Image.new()
	assert_eq(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return image

func test_entire_manifest_matches_preserved_a2_contract() -> void:
	var current = json(SHARED+"manifest.json")
	var baseline = json(EVIDENCE+"baseline-a2/manifest.json")
	assert_eq(current,baseline,"All canvas/pivot/contact/timing/offset/camera fields unchanged")
	assert_eq(current.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(current.characters.thoma.pivot,[256.0,464.0])
	var swing: Dictionary = current.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	for event in swing.events: assert_eq(event.anchor,[455.0,196.0])
	for sequence in current.sequences.values():
		for frame in sequence.frames:
			assert_false(frame.path.contains("baseline-a2"))
			assert_false(frame.path.contains("rejected"))

func test_approved_weapon_and_handoff_table_match_audit() -> void:
	var table := FileAccess.get_file_as_string(EVIDENCE+"frame-status-table.md")
	var final_handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var count := 0
	for record in json(SHARED+"frame-audit.json"):
		if not record.path.begins_with("thoma/"):continue
		count += 1
		assert_eq(record.weapon_status,"APPROVED")
		assert_eq(record.weapon_approval,"Owner, 2026-10-24")
		assert_eq(record.sha256,FileAccess.get_sha256(SHARED+record.path))
		var line := "| `%s` | %s | %s |" % [record.path,record.status,record.reason]
		assert_true(table.contains(line),"W5 handoff table must reflect audited status/reason")
		if final_handoff.contains("## spike-02 A3\n"):
			assert_true(final_handoff.split("## spike-02 A3\n")[1].contains(line),"W6 final table matches audit")
		for criterion in ["face","stole_cape_embroidery","cuffs","hem_silhouette","palette","proportions","light_direction","stroke"]:
			assert_has(record.style_review,criterion)
			if record.status=="PASS": assert_true(record.style_review[criterion].begins_with("PASS"),criterion)
	assert_eq(count,7)

func test_five_repaints_preserve_alpha_and_protected_contact_geometry() -> void:
	for index in range(5):
		var name := "%02d.png" % index
		var original := png_bytes(EVIDENCE+"baseline-a2/"+name)
		var current := png_bytes(SHARED+"thoma/swing/"+name)
		assert_eq(current.get_size(),Vector2i(512,512))
		assert_ne(FileAccess.get_sha256(SHARED+"thoma/swing/"+name),FileAccess.get_sha256(EVIDENCE+"baseline-a2/"+name))
		var mask := png_bytes(EVIDENCE+"repaint-masks/"+name)
		var alpha_equal := true
		var outside_equal := true
		for y in range(512):
			for x in range(512):
				var a := original.get_pixel(x,y)
				var b := current.get_pixel(x,y)
				alpha_equal = alpha_equal and a.a==b.a
				if mask.get_pixel(x,y).r==0: outside_equal = outside_equal and a==b
		assert_true(alpha_equal,"Fixed A2 silhouette/pivot/feet: "+name)
		assert_true(outside_equal,"No unmasked mace, grip, hand, face or boot changed: "+name)
	var contact := png_bytes(SHARED+"thoma/swing/03.png")
	var old_contact := png_bytes(EVIDENCE+"baseline-a2/03.png")
	assert_eq(contact.get_region(Rect2i(340,170,140,55)).get_data(),old_contact.get_region(Rect2i(340,170,140,55)).get_data(),"Contact grip/haft/head stay byte-exact")

func test_baseline_hashes_and_bounded_generation_attempts() -> void:
	for record in json(EVIDENCE+"baseline-a2/hashes.json"):
		var path: String = "res://../"+record.path
		# JSON line endings vary across checkouts; PNG byte baselines never do.
		if path.ends_with(".png"): assert_eq(FileAccess.get_sha256(path),record.sha256)
	var counts := {}
	for attempt in json(SHARED+"a3-swing-prompts.json"):
		counts[attempt.frame] = counts.get(attempt.frame,0)+1
		assert_eq(attempt.runtime_sha256,FileAccess.get_sha256(SHARED+attempt.frame))
		assert_eq(attempt.raw_sha256,FileAccess.get_sha256(SHARED+attempt.raw))
		assert_eq(attempt.references.size(),4)
		assert_lte(attempt.attempt,3.0)
	assert_eq(counts.size(),5)
	for count in counts.values():assert_lte(count,3)
