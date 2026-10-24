extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const EVIDENCE = "res://docs/evidence/spike02-a6/"
const REPO = "res://../"
const CHECKS = ["stole","embroidery","cuffs","hem","face_hair","palette","seams","bag_count","feet","mace","sequence"]

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func image(path: String) -> Image:
	var im := Image.new()
	assert_eq(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return im

func test_a6_immutable_endpoints_match_fixed_a5_sha256() -> void:
	for pair in [["thoma/idle/01.png","c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"],
		["thoma/swing/05.png","f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"]]:
		assert_eq(FileAccess.get_sha256(SHARED+pair[0]),pair[1])
		assert_eq(FileAccess.get_sha256(REPO+"shared-anim/"+pair[0]),pair[1])

func test_a6_complete_manifest_matches_a5_and_excludes_all_baselines() -> void:
	var manifest = json(SHARED+"manifest.json")
	assert_eq(manifest,json(EVIDENCE+"baseline-a5/manifest.json"),"Entire timing, camera, offsets, impact and scenario data unchanged")
	assert_eq(manifest.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(manifest.characters.thoma.pivot,[256.0,464.0])
	var swing: Dictionary = manifest.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	assert_does_not_have(swing.reduced_frame_indices,2.0)
	for event in swing.events:assert_eq(event.anchor,[455.0,196.0])
	for sequence in manifest.sequences.values():
		for frame in sequence.frames:
			for forbidden in ["baseline-a5","baseline-a4","baseline-a3","baseline-a2","raw/","candidates/","rejected"]:
				assert_false(frame.path.contains(forbidden))

func test_a6_every_attempt_retained_three_reference_hashes_bounded_and_runtime_bound() -> void:
	var counts := {}
	var adopted := {}
	for row in json(SHARED+"a6-swing-prompts.json"):
		counts[row.frame] = counts.get(row.frame,0)+1
		assert_gte(row.attempt,1.0)
		assert_lte(row.attempt,4.0)
		assert_eq(row.tool,"image_gen (built-in)")
		assert_true(row.prompt.contains("POSE"),"Prompt labels pose-only reference")
		assert_eq(row.references.size(),3)
		assert_eq(row.references[0].path,"shared-anim/thoma/idle/01.png")
		assert_eq(row.references[1].path,"shared-anim/thoma/swing/05.png")
		assert_eq(row.references[2].path,"godot-spike/docs/evidence/spike02-a6/baseline-a5/"+row.frame.get_file())
		assert_true(row.references[2].role.contains("ONLY"))
		for ref in row.references:assert_eq(ref.sha256,FileAccess.get_sha256(REPO+ref.path))
		assert_eq(row.raw_sha256,FileAccess.get_sha256(REPO+row.raw))
		assert_true(row.settings.transparent_background)
		assert_eq(row.settings.seed,"not exposed")
		if row.adopted:
			assert_false(adopted.has(row.frame),"Exactly one adopted candidate per frame")
			adopted[row.frame] = true
			assert_true(row.pick)
			assert_eq(row.runtime_sha256,FileAccess.get_sha256(SHARED+row.frame))
			assert_eq(row.runtime_sha256,row.normalization.normalized_sha256)
			assert_eq(row.normalization.raw_sha256,row.raw_sha256)
			assert_eq(row.normalization.cleanup_mask_sha256,FileAccess.get_sha256(REPO+row.normalization.cleanup_mask))
			assert_true(row.normalization.operations.contains("no costume compositing"))
			assert_lt(row.normalization.palette_distance.after,row.normalization.palette_distance.before)
	assert_eq(adopted.size(),5)
	for count in counts.values():assert_lte(count,4)

func table_row(record: Dictionary) -> String:
	var flags: Array[String] = []
	for name in CHECKS:
		var verdict: String = record.region_review[name].split(":")[0]
		flags.append((str(int(record.bag_count))+" ")+verdict if name=="bag_count" else verdict)
	return "| `%s` | %s | %s | %s |" % [record.path,record.status," | ".join(flags),record.reason]

func test_a6_pass_requires_every_check_and_table_handoff_agreement() -> void:
	var table := FileAccess.get_file_as_string(EVIDENCE+"frame-status-table.md")
	var handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var count := 0
	for record in json(SHARED+"frame-audit.json"):
		if not record.path.begins_with("thoma/"):continue
		count += 1
		assert_eq(record.sha256,FileAccess.get_sha256(SHARED+record.path))
		assert_eq(record.weapon_status,"APPROVED")
		assert_eq(record.bag_count,1.0)
		var any_failed := false
		for name in CHECKS:
			assert_has(record.region_review,name)
			var result: String = record.region_review[name].split(":")[0]
			assert_true(result in ["PASS","FAIL"])
			any_failed = any_failed or result=="FAIL"
			if result=="FAIL":assert_gt(record.region_review[name].length(),6,"Failure must explain why")
			if record.status=="PASS":assert_eq(result,"PASS",name)
		assert_eq(record.status,"PLACEHOLDER" if any_failed else "PASS")
		assert_true(table.contains(table_row(record)))
		if handoff.contains("## spike-02 A6\n"):
			assert_true(handoff.split("## spike-02 A6\n")[1].contains(table_row(record)),"Final handoff row")
	assert_eq(count,7)

func test_a6_canvas_ground_scale_contact_anchor_and_honest_geometry_limit() -> void:
	var geometry = json(EVIDENCE+"geometry-check.json")
	assert_eq(geometry.contact_anchor,[455.0,196.0])
	for row in json(SHARED+"a6-swing-prompts.json"):
		if not row.adopted:continue
		var im := image(SHARED+row.frame)
		assert_eq(im.get_size(),Vector2i(512,512))
		var bottom := 0
		for y in range(512):
			for x in range(512):
				if im.get_pixel(x,y).a>0.5:bottom=maxi(bottom,y)
		assert_between(bottom,463,465,"Foot ground within one-pixel rasterization tolerance")
		var measured: Dictionary = geometry.frames[row.frame]
		assert_almost_eq(measured.head_to_ground_px,360.0,18.0)
	var contact := image(SHARED+"thoma/swing/03.png")
	assert_gt(contact.get_pixel(455,196).a,0.9,"Painted head covers unchanged contact anchor")
	assert_eq(geometry.frames["thoma/swing/03.png"].mapped_landmarks.mace_head,[455.0,196.0])
	assert_true(geometry.frames["thoma/swing/03.png"].contact_anchor_exact_transform)
	var follow = json(SHARED+"frame-audit.json").filter(func(r):return r.path=="thoma/swing/04.png")[0]
	assert_true(follow.region_review.mace.begins_with("FAIL:"),"Do not disguise 04 weapon pose drift as geometry pass")

func test_a6_a5_byte_baselines_are_evidence_only() -> void:
	for row in json(EVIDENCE+"baseline-a5/hashes.json"):
		if row.path.ends_with(".png"):assert_eq(FileAccess.get_sha256(REPO+row.path),row.sha256)
	for i in range(5):
		var file := "%02d.png" % i
		assert_ne(FileAccess.get_sha256(SHARED+"thoma/swing/"+file),FileAccess.get_sha256(EVIDENCE+"baseline-a5/"+file))

func test_a6_real_playback_trace_and_six_proxy_pairs_preserve_failures() -> void:
	var playback = json(EVIDENCE+"playback-check.json")
	assert_true(playback.capture_complete)
	assert_eq(playback.fps,60.0)
	assert_eq(playback.selected.size(),7)
	assert_eq(playback.frames,playback.traced_frames+playback.untraced_terminal_frames)
	assert_lte(playback.untraced_terminal_frames,1.0)
	assert_true(playback.terminal_pixels_equal_previous_ready)
	for shot in playback.selected:assert_true(FileAccess.file_exists(EVIDENCE+shot.file))
	var pairs: Array = json(EVIDENCE+"sequence-check.json").pairs
	assert_eq(pairs.size(),6)
	for pair in pairs:
		for name in ["stole","embroidery","cuffs","hem","face_hair","palette"]:assert_has(pair.region_mean_rgb_delta,name)
		assert_between(pair.garment_silhouette_iou,0.0,1.0)
		assert_has(pair,"character_height_delta_px")
		assert_eq(pair.visual_result,"FAIL","Known style pops remain open")
