extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const EVIDENCE = "res://docs/evidence/spike02-a4/"
const REGIONS = ["stole","embroidery","cuffs","hem","face_hair","palette","sequence"]

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func png(path: String) -> Image:
	var image := Image.new()
	assert_eq(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return image

func test_immutable_references_match_a3_fixed_hashes() -> void:
	for item in [["thoma/idle/01.png","c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"],
		["thoma/swing/05.png","f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"]]:
		assert_eq(FileAccess.get_sha256(SHARED+item[0]),item[1])
		assert_eq(FileAccess.get_sha256("res://../shared-anim/"+item[0]),item[1])

func test_complete_a3_manifest_and_no_archived_frames() -> void:
	var current = json(SHARED+"manifest.json")
	assert_eq(current,json(EVIDENCE+"baseline-a3/manifest.json"))
	assert_eq(current.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(current.characters.thoma.pivot,[256.0,464.0])
	var swing: Dictionary = current.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	for event in swing.events: assert_eq(event.anchor,[455.0,196.0])
	for sequence in current.sequences.values():
		for frame in sequence.frames:
			for forbidden in ["baseline-a2","baseline-a3","rejected","raw/"]:
				assert_false(frame.path.contains(forbidden))

func test_rebuilt_frames_preserve_mace_grip_contact_and_grounded_feet() -> void:
	for index in range(5):
		var name := "%02d.png" % index
		var old := png(EVIDENCE+"baseline-a3/"+name)
		var current := png(SHARED+"thoma/swing/"+name)
		var protected := png(EVIDENCE+"protected-masks/"+name)
		assert_eq(current.get_size(),Vector2i(512,512))
		assert_ne(current.get_data(),old.get_data(),"Rebuilt costume: "+name)
		var same := true
		for y in range(512):
			for x in range(512):
				if protected.get_pixel(x,y).r>0:
					same = same and current.get_pixel(x,y)==old.get_pixel(x,y)
		assert_true(same,"Exact motion weapon/hand mask: "+name)
		assert_true(current.get_region(Rect2i(0,444,512,68)).get_data()==old.get_region(Rect2i(0,444,512,68)).get_data(),"Ground-contact pixels remain exact: "+name)
		assert_ne(current.get_region(Rect2i(110,350,290,80)).get_data(),old.get_region(Rect2i(110,350,290,80)).get_data(),"Old fan hem actually replaced")
	var contact := png(SHARED+"thoma/swing/03.png")
	var old_contact := png(EVIDENCE+"baseline-a3/03.png")
	assert_true(contact.get_region(Rect2i(340,170,140,55)).get_data()==old_contact.get_region(Rect2i(340,170,140,55)).get_data(),"Contact grip/haft/head exact RGBA")

func test_region_status_and_handoff_table_cannot_claim_partial_pass() -> void:
	var table := FileAccess.get_file_as_string(EVIDENCE+"frame-status-table.md")
	var handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var count := 0
	for record in json(SHARED+"frame-audit.json"):
		if not record.path.begins_with("thoma/"):continue
		count += 1
		assert_eq(record.sha256,FileAccess.get_sha256(SHARED+record.path))
		assert_eq(record.weapon_status,"APPROVED")
		var flags: Array[String] = []
		for name in REGIONS:
			assert_has(record.region_review,name)
			var verdict: String = record.region_review[name].split(":")[0]
			assert_true(verdict in ["PASS","FAIL"])
			flags.append(verdict)
			if record.status=="PASS":assert_eq(verdict,"PASS",name)
		if "FAIL" in flags:assert_eq(record.status,"PLACEHOLDER")
		var line := "| `%s` | %s | %s | %s |" % [record.path,record.status," | ".join(flags),record.reason]
		assert_true(table.contains(line),"W4 prepared handoff row")
		if handoff.contains("## spike-02 A4\n"):
			assert_true(handoff.split("## spike-02 A4\n")[1].contains(line),"W6 actual handoff row")
	assert_eq(count,7)

func test_provenance_archive_masks_and_generation_bounds() -> void:
	for record in json(EVIDENCE+"baseline-a3/hashes.json"):
		if record.path.ends_with(".png"):
			assert_eq(FileAccess.get_sha256("res://../"+record.path),record.sha256)
	var records = json(SHARED+"a4-swing-prompts.json")
	assert_eq(records.size(),5)
	for record in records:
		assert_eq(record.generation_attempts,0.0)
		assert_lte(record.generation_attempts,3.0)
		assert_eq(record.runtime_sha256,FileAccess.get_sha256(SHARED+record.frame))
		assert_eq(record.baseline_sha256,FileAccess.get_sha256(EVIDENCE+"baseline-a3/"+record.frame.get_file()))
		for path in record.references:assert_eq(record.references[path],FileAccess.get_sha256(SHARED+path))
	for region in json(EVIDENCE+"reference-regions/regions.json"):
		assert_eq(region.reference_sha256,FileAccess.get_sha256(SHARED+region.reference))
		assert_true(FileAccess.file_exists(EVIDENCE+"reference-regions/"+region.mask))
		assert_true(FileAccess.file_exists(EVIDENCE+"reference-regions/"+region.pixels))
	var pairs: Array = json(EVIDENCE+"sequence-check.json").pairs
	assert_eq(pairs.size(),6)
	for pair in pairs:
		for region in REGIONS.slice(0,6):assert_has(pair.region_mean_rgb_delta,region)
