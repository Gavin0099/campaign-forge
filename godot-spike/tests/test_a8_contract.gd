extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const E = "res://docs/evidence/spike02-a8/"
const REPO = "res://../"
const CHECKS = ["face_hair","stole","embroidery","tassels","cuffs","hem","palette","seams","bag_count","feet","mace","landmarks","sequence"]
const TARGETS = [Vector2(192,85),Vector2(259,87),Vector2(449,110),Vector2(455,196),Vector2(421,376)]

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func image(path: String) -> Image:
	var im := Image.new()
	assert_eq(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return im

func test_a8_anchors_and_all_mechanics_remain_exact() -> void:
	for pair in [["thoma/idle/01.png","c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"],
		["thoma/swing/05.png","f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"]]:
		assert_eq(FileAccess.get_sha256(SHARED+pair[0]),pair[1])
		assert_eq(FileAccess.get_sha256(REPO+"shared-anim/"+pair[0]),pair[1])
	var manifest = json(SHARED+"manifest.json")
	assert_eq(manifest,json(E+"baseline-a7/manifest.json"))
	assert_eq(manifest.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(manifest.characters.thoma.pivot,[256.0,464.0])
	var swing = manifest.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	assert_eq(swing.reduced_frame_indices,[0.0,3.0,5.0])
	for event in swing.events:assert_eq(event.anchor,[455.0,196.0])

func test_a8_canvas_rgba_ground_and_nonempty_foot_pixels() -> void:
	for i in range(5):
		var im := image(SHARED+"thoma/swing/%02d.png" % i)
		assert_eq(im.get_size(),Vector2i(512,512))
		assert_eq(im.get_format(),Image.FORMAT_RGBA8)
		assert_eq(im.get_pixel(0,0).a,0.0)
		var bottom := -1
		var grounded := 0
		for y in range(512):
			for x in range(512):
				var p := im.get_pixel(x,y)
				if p.a>0.5:bottom=maxi(bottom,y)
				if y==464 and x>=30 and x<410 and p.a>0.5:grounded+=1
		assert_between(bottom,463,465)
		assert_gt(grounded,4,"Actual boot occupancy on ground line")

func test_a8_mace_centres_are_measured_from_final_pixels_and_contact_is_opaque() -> void:
	# Independent final-PNG binary-alpha centroid in37x37 target-head ROI;
	# catches missing/moved weapon, does not trust generator or claimed coordinate.
	for i in range(5):
		var im := image(SHARED+"thoma/swing/%02d.png" % i)
		var target: Vector2 = TARGETS[i]
		var total := Vector2.ZERO
		var count := 0
		for y in range(int(target.y)-18,int(target.y)+19):
			for x in range(int(target.x)-18,int(target.x)+19):
				if im.get_pixel(x,y).a>0.9:
					total+=Vector2(x,y)
					count+=1
		assert_gt(count,150,"Opaque flanged head footprint exists")
		if count>0:assert_lte((total/count).distance_to(target),4.0,"Final head centroid within brief tolerance")
	assert_gt(image(SHARED+"thoma/swing/03.png").get_pixel(455,196).a,0.9)

func test_a8_live_manifest_never_references_any_archived_baseline() -> void:
	for sequence in json(SHARED+"manifest.json").sequences.values():
		for frame in sequence.frames:
			for forbidden in ["baseline-a7","baseline-a6","baseline-a5","baseline-a4","baseline-a3","baseline-a2","sheet-attempts","normalized/"]:
				assert_false(frame.path.contains(forbidden))
	for entry in json(E+"baseline-a7/hashes.json"):
		if entry.path.ends_with(".png"):assert_eq(entry.sha256,FileAccess.get_sha256(REPO+entry.path))

func table_row(record: Dictionary) -> String:
	var flags: Array[String] = []
	for name in CHECKS:flags.append(("1 " if name=="bag_count" else "")+record.region_review[name].split(":")[0])
	return "| `%s` | %s | %s | %s |" % [record.path,record.status," | ".join(flags),record.reason]

func test_a8_placeholder_is_exactly_the_complete_brief_gate_and_matches_handoff() -> void:
	var table := FileAccess.get_file_as_string(E+"frame-status-table.md")
	var handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var count := 0
	for record in json(SHARED+"frame-audit.json"):
		if not record.path.begins_with("thoma/"):continue
		count+=1
		assert_eq(record.sha256,FileAccess.get_sha256(SHARED+record.path))
		assert_eq(record.bag_count,1.0)
		assert_eq(record.weapon_status,"APPROVED")
		var passed: bool = record.technical_check.pass
		for name in CHECKS:
			assert_has(record.region_review,name)
			var result: String = record.region_review[name].split(":")[0]
			assert_true(result in ["PASS","FAIL"])
			passed=passed and result=="PASS"
			if result=="FAIL":assert_gt(record.region_review[name].length(),12)
		assert_eq(record.status,"PASS" if passed else "PLACEHOLDER")
		assert_true(table.contains(table_row(record)))
		if handoff.contains("## spike-02 A8\n"):
			assert_true(handoff.split("## spike-02 A8\n")[1].contains(table_row(record)),"Final handoff must match all13 audit items")
	assert_eq(count,7)

func test_a8_one_shared_sheet_inputs_and_every_final_adoption_are_hash_bound() -> void:
	var provenance = json(SHARED+"a8-swing-prompts.json")
	assert_between(provenance.sheet_attempts.size(),1,4)
	var selected := false
	for attempt in provenance.sheet_attempts:
		assert_eq(attempt.mode,"edit one shared seven-panel sheet")
		assert_eq(attempt.raw_sha256,FileAccess.get_sha256(REPO+attempt.raw))
		assert_gte(attempt.inputs.size(),4)
		for ref in attempt.inputs:assert_eq(ref.sha256,FileAccess.get_sha256(REPO+ref.path))
		assert_eq(attempt.settings.seed,"not exposed")
		assert_gt(attempt.prompt.length(),1000)
		selected=selected or attempt.attempt==provenance.selected_attempt
	assert_true(selected)
	assert_eq(provenance.frames.size(),5)
	var seen := {}
	for record in provenance.frames:
		assert_false(seen.has(record.frame))
		seen[record.frame]=true
		assert_eq(record.sheet_attempt,provenance.selected_attempt)
		assert_eq(record.raw_sha256,FileAccess.get_sha256(REPO+record.raw))
		assert_eq(record.runtime_sha256,FileAccess.get_sha256(REPO+record.runtime))
		assert_eq(record.runtime_sha256,FileAccess.get_sha256(SHARED+record.frame))
		for fix in record.local_fixes:
			for pair in [["input","input_sha256"],["output","output_sha256"],["mask","mask_sha256"]]:
				assert_eq(fix[pair[1]],FileAccess.get_sha256(REPO+fix[pair[0]]))
	var fallback_counts := {}
	for edit in provenance.fallback_edits:fallback_counts[edit.frame]=fallback_counts.get(edit.frame,0)+1
	for n in fallback_counts.values():assert_lte(n,2)

func test_a8_real_playback_and_every_requested_landmark_have_evidence() -> void:
	var playback = json(E+"playback-check.json")
	assert_true(playback.capture_complete)
	assert_eq(playback.fps,60.0)
	assert_eq(playback.selected.size(),7)
	for shot in playback.selected:assert_true(FileAccess.file_exists(E+shot.file))
	var pairs = json(E+"sequence-check.json").pairs
	assert_eq(pairs.size(),6)
	for pair in pairs:
		for name in CHECKS:assert_has(pair.region_mean_rgb_delta,name)
		assert_between(pair.garment_silhouette_iou,0.0,1.0)
		assert_has(pair,"character_height_delta_px")
	var landmarks = json(E+"landmark-deltas.json")
	assert_eq(landmarks.pairs.size(),6)
	for row in landmarks.per_frame.values():
		for name in ["head_centre","hand_weapon","hand_free","elbow_left","elbow_right","knee_left","knee_right","foot_left","foot_right","mace_head"]:
			assert_has(row,name)
			assert_has(row[name],"measured")
			assert_has(row[name],"target")

func test_a8_sheet_layout_contains_exact_fixed_anchor_pixels_and_five_open_cells() -> void:
	var layout = json(E+"inputs/sheet-layout.json")
	var sheet := image(E+"inputs/sheet-canvas.png")
	var mask := image(E+"inputs/sheet-mask.png")
	assert_eq(layout.panels.size(),7)
	assert_eq(sheet.get_size(),Vector2i(2048,1024))
	var fixed := 0
	for panel in layout.panels:
		var rect := Rect2i(int(panel.rect[0]),int(panel.rect[1]),512,512)
		var centre := rect.position+Vector2i(256,256)
		if panel.fixed:
			fixed+=1
			assert_true(sheet.get_region(rect).get_data()==image(REPO+panel.source).get_data())
			assert_eq(mask.get_pixelv(centre).r,0.0)
		else:assert_eq(mask.get_pixelv(centre).r,1.0)
	assert_eq(fixed,2)
