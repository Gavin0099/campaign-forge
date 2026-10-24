extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const EVIDENCE = "res://docs/evidence/spike02-a5/"
const CHECKS = ["stole","embroidery","cuffs","hem","face_hair","palette","seams","bag_count","feet","sequence"]

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func png(path: String) -> Image:
	var image := Image.new()
	assert_eq(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return image

func test_a5_immutable_references_and_entire_manifest_match_a4() -> void:
	for item in [["thoma/idle/01.png","idle-01.png","c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"],
		["thoma/swing/05.png","05.png","f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"]]:
		assert_eq(FileAccess.get_sha256(SHARED+item[0]),item[2])
		assert_eq(FileAccess.get_sha256(EVIDENCE+"baseline-a4/"+item[1]),item[2])
	var manifest = json(SHARED+"manifest.json")
	assert_eq(manifest,json(EVIDENCE+"baseline-a4/manifest.json"))
	assert_eq(manifest.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(manifest.characters.thoma.pivot,[256.0,464.0])
	var swing: Dictionary = manifest.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	for event in swing.events:assert_eq(event.anchor,[455.0,196.0])
	for sequence in manifest.sequences.values():
		for frame in sequence.frames:
			for forbidden in ["baseline-a4","baseline-a3","baseline-a2","raw/","rejected"]:
				assert_false(frame.path.contains(forbidden))

func test_a5_raw_mace_grip_face_feet_protection_and_rebuilt_canvas() -> void:
	for index in range(5):
		var name := "%02d.png" % index
		var before := png(EVIDENCE+"baseline-a4/"+name)
		var after := png(SHARED+"thoma/swing/"+name)
		var protection := png(EVIDENCE+"protected-masks/"+name)
		assert_eq(after.get_size(),Vector2i(512,512))
		assert_ne(FileAccess.get_sha256(SHARED+"thoma/swing/"+name),FileAccess.get_sha256(EVIDENCE+"baseline-a4/"+name))
		var identical := true
		for y in range(512):
			for x in range(512):
				if protection.get_pixel(x,y).r>0:
					identical = identical and before.get_pixel(x,y)==after.get_pixel(x,y)
		assert_true(identical,"Raw A4 protected RGBA: "+name)
		assert_true(after.get_region(Rect2i(0,444,512,68)).get_data()==before.get_region(Rect2i(0,444,512,68)).get_data(),"Planted ground bytes: "+name)
	var contact := png(SHARED+"thoma/swing/03.png")
	var before_contact := png(EVIDENCE+"baseline-a4/03.png")
	assert_true(contact.get_region(Rect2i(340,170,140,55)).get_data()==before_contact.get_region(Rect2i(340,170,140,55)).get_data(),"Exact contact head/haft/grip at [455,196]")

func table_row(record: Dictionary) -> String:
	var flags: Array[String] = []
	for name in CHECKS:
		var verdict: String = record.region_review[name].split(":")[0]
		flags.append((str(int(record.bag_count))+" ") + verdict if name=="bag_count" else verdict)
	return "| `%s` | %s | %s | %s |" % [record.path,record.status," | ".join(flags),record.reason]

func test_a5_all_pass_gates_and_table_agreement() -> void:
	var table := FileAccess.get_file_as_string(EVIDENCE+"frame-status-table.md")
	var handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var count := 0
	for record in json(SHARED+"frame-audit.json"):
		if not record.path.begins_with("thoma/"):continue
		count += 1
		assert_eq(record.sha256,FileAccess.get_sha256(SHARED+record.path))
		assert_eq(record.weapon_status,"APPROVED")
		assert_eq(record.bag_count,1.0)
		var failed := false
		for name in CHECKS:
			assert_has(record.region_review,name)
			var result: String = record.region_review[name].split(":")[0]
			assert_true(result in ["PASS","FAIL"])
			failed = failed or result=="FAIL"
			if record.status=="PASS":assert_eq(result,"PASS",name)
		if failed:assert_eq(record.status,"PLACEHOLDER")
		assert_true(table.contains(table_row(record)),"Prepared handoff row")
		if handoff.contains("## spike-02 A5\n"):
			assert_true(handoff.split("## spike-02 A5\n")[1].contains(table_row(record)),"Actual A5 handoff row")
	assert_eq(count,7)

func point_segment_distance(point: Vector2, a: Vector2, b: Vector2) -> float:
	var segment := b-a
	var t := clampf((point-a).dot(segment)/segment.length_squared(),0,1) if segment.length_squared()>0 else 0.0
	return point.distance_to(a+segment*t)

func test_a5_seam_masks_are_narrow_declared_bands_with_bounded_area() -> void:
	for record in json(EVIDENCE+"seam-masks/coordinates.json"):
		var path: String = EVIDENCE+"seam-masks/"+record.mask
		var image := png(path)
		assert_eq(image.get_size(),Vector2i(512,512))
		assert_eq(FileAccess.get_sha256(path),record.sha256)
		assert_lte(record.max_area,10000.0)
		assert_lte(record.max_band_width,8.0)
		var area := 0
		var outside := 0
		for band in record.bands:assert_lte(band.width,record.max_band_width)
		for y in range(512):
			for x in range(512):
				if image.get_pixel(x,y).r==0:continue
				area += 1
				var covered := false
				for band in record.bands:
					for i in range(band.points.size()-1):
						var a := Vector2(band.points[i][0],band.points[i][1])
						var b := Vector2(band.points[i+1][0],band.points[i+1][1])
						# Pillow's integer line rasterization and round joins add <=1px.
						covered = covered or point_segment_distance(Vector2(x,y),a,b)<=band.width/2+1
				if not covered:outside += 1
		assert_eq(outside,0,"No support outside actual declared join bands: "+record.frame)
		assert_eq(area,int(record.total_pixel_area))
		assert_lte(area,int(record.max_area))

func test_a5_baseline_provenance_and_unit_embroidery_scale() -> void:
	for record in json(EVIDENCE+"baseline-a4/hashes.json"):
		if record.path.ends_with(".png"):assert_eq(FileAccess.get_sha256("res://../"+record.path),record.sha256)
	var records = json(SHARED+"a5-swing-prompts.json")
	assert_eq(records.size(),5)
	for record in records:
		assert_eq(record.generation_attempts,0.0)
		assert_lte(record.generation_attempts,3.0)
		assert_eq(record.runtime_sha256,FileAccess.get_sha256(SHARED+record.frame))
		assert_eq(record.baseline_sha256,FileAccess.get_sha256(EVIDENCE+"baseline-a4/"+record.frame.get_file()))
		assert_eq(record.mask_sha256,FileAccess.get_sha256("res://../"+record.mask))
		for path in record.references:assert_eq(record.references[path],FileAccess.get_sha256(SHARED+path))
	assert_eq(json(EVIDENCE+"rig-controls.json").body_horizontal_scale,1.0)
	for record in json(EVIDENCE+"scale-measurement.json"):
		assert_eq(record.horizontal_spacing_scale,1.0)
		assert_eq(record.a5_width_px,record.reference_motif_roi_width_px)
		assert_lte(record.horizontal_change_percent,record.tolerance_percent)

func test_a5_six_sequence_pairs_have_colour_and_outline_evidence() -> void:
	var pairs: Array = json(EVIDENCE+"sequence-check.json").pairs
	assert_eq(pairs.size(),6)
	for pair in pairs:
		for name in CHECKS.slice(0,6):assert_has(pair.region_mean_rgb_delta,name)
		assert_gte(pair.garment_silhouette_iou,0.0)
		assert_lte(pair.garment_silhouette_iou,1.0)
		assert_true(pair.visual_result in ["PASS","FAIL"])
		assert_false(pair.reason.is_empty())
