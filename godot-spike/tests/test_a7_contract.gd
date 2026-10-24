extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const E = "res://docs/evidence/spike02-a7/"
const REPO = "res://../"
const CHECKS = ["face_hair","stole","embroidery","tassels","cuffs","hem","palette","seams","bag_count","feet","mace","landmarks","sequence"]

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func image(path: String) -> Image:
	var im := Image.new()
	assert_eq(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return im

func test_a7_endpoints_and_manifest_are_exactly_fixed() -> void:
	for pair in [["thoma/idle/01.png","c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"],
		["thoma/swing/05.png","f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"]]:
		assert_eq(FileAccess.get_sha256(SHARED+pair[0]),pair[1])
		assert_eq(FileAccess.get_sha256(REPO+"shared-anim/"+pair[0]),pair[1])
	var manifest = json(SHARED+"manifest.json")
	assert_eq(manifest,json(E+"baseline-a6/manifest.json"))
	assert_eq(manifest.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(manifest.characters.thoma.pivot,[256.0,464.0])
	var swing: Dictionary = manifest.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	assert_does_not_have(swing.reduced_frame_indices,2.0)
	for event in swing.events:assert_eq(event.anchor,[455.0,196.0])
	for sequence in manifest.sequences.values():
		for frame in sequence.frames:
			for forbidden in ["baseline-a6","baseline-a5","baseline-a4","baseline-a3","baseline-a2","attempts/","candidates/","raw/","rejected"]:
				assert_false(frame.path.contains(forbidden))

func test_a7_spec_and_five_complete_pose_targets_bind_anchor_pixels() -> void:
	var spec = json(SHARED+"thoma-appearance-spec.json")
	for section in ["face","hair","costume","mace","body_proportions","palette","outline_brush","pose_targets","swing_arc"]:assert_has(spec,section)
	for section in ["robe","stole","embroidery","tassels","cuffs","hem","bag","belt","shoes"]:assert_has(spec.costume,section)
	assert_eq(spec.appearance_sources.size(),2)
	for ref in spec.appearance_sources:assert_eq(ref.sha256,FileAccess.get_sha256(REPO+ref.path))
	assert_eq(spec.pose_targets.size(),5)
	for key in ["00","01","02","03","04"]:
		var pose: Dictionary = spec.pose_targets[key]
		assert_eq(pose.pivot,[256.0,464.0])
		for name in ["head_centre","eye_near","eye_far","shoulder_left","shoulder_right","elbow_left","elbow_right","hand_weapon","hand_free","hip_left","hip_right","knee_left","knee_right","foot_left","foot_right","mace_head","mace_grip"]:
			assert_has(pose.landmarks,name)
	assert_eq(spec.pose_targets["03"].landmarks.mace_head,[455.0,196.0])
	assert_eq(spec.pose_targets["04"].landmarks.mace_head,[421.0,376.0])
	for entry in spec.palette.values():
		var im := image(SHARED+"thoma/idle/01.png")
		var p: Color = im.get_pixel(int(entry.sample_xy[0]),int(entry.sample_xy[1]))
		assert_eq("#"+p.to_html(false),entry.hex)

func test_a7_attempts_bounded_ordered_and_every_adoption_bound() -> void:
	var counts := {}
	var adopted := {}
	var generated_order: Array = []
	for record in json(SHARED+"a7-swing-prompts.json"):
		counts[record.frame]=counts.get(record.frame,0)+1
		assert_between(record.attempt,1.0,4.0)
		assert_gt(record.prompt.length(),80)
		assert_eq(record.raw_sha256,FileAccess.get_sha256(REPO+record.raw))
		assert_eq(record.spec_sha256,FileAccess.get_sha256(SHARED+"thoma-appearance-spec.json"))
		assert_gte(record.references.size(),3)
		for ref in record.references:assert_eq(ref.sha256,FileAccess.get_sha256(REPO+ref.path))
		assert_false(record.generated_pixels_adopted,"Reframed imagegen returns explicitly rejected")
		if record.tool=="image_gen (built-in)":
			generated_order.append(record.frame.get_file())
			assert_eq(record.settings.seed,"not exposed")
		assert_has(record.settings,"seed")
		for touch in record.touchups:
			for pair in [["input","input_sha256"],["output","output_sha256"],["mask","mask_sha256"]]:
				assert_eq(touch[pair[1]],FileAccess.get_sha256(REPO+touch[pair[0]]))
		if record.adopted:
			assert_false(adopted.has(record.frame))
			adopted[record.frame]=true
			assert_eq(record.runtime_sha256,FileAccess.get_sha256(SHARED+record.frame))
			assert_eq(record.runtime_sha256,FileAccess.get_sha256(REPO+record.runtime))
	assert_eq(generated_order,["01.png","02.png","00.png","03.png","04.png"])
	assert_eq(adopted.size(),5)
	for count in counts.values():assert_lte(count,4)

func table_row(record: Dictionary) -> String:
	var flags: Array[String] = []
	for name in CHECKS:
		flags.append(("1 " if name=="bag_count" else "")+record.region_review[name].split(":")[0])
	return "| `%s` | %s | %s | %s |" % [record.path,record.status," | ".join(flags),record.reason]

func test_a7_honest_placeholder_gates_match_table_and_final_handoff() -> void:
	var table := FileAccess.get_file_as_string(E+"frame-status-table.md")
	var handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var count := 0
	for record in json(SHARED+"frame-audit.json"):
		if not record.path.begins_with("thoma/"):continue
		count+=1
		assert_eq(record.sha256,FileAccess.get_sha256(SHARED+record.path))
		assert_eq(record.bag_count,1.0)
		assert_eq(record.weapon_status,"APPROVED")
		var failed := false
		for name in CHECKS:
			assert_has(record.region_review,name)
			var result: String = record.region_review[name].split(":")[0]
			assert_true(result in ["PASS","FAIL"])
			failed=failed or result=="FAIL"
			if result=="FAIL":assert_gt(record.region_review[name].length(),8)
			if record.status=="PASS":assert_eq(result,"PASS")
		assert_eq(record.status,"PLACEHOLDER" if failed else "PASS")
		assert_true(table.contains(table_row(record)))
		if handoff.contains("## spike-02 A7\n"):
			assert_true(handoff.split("## spike-02 A7\n")[1].contains(table_row(record)),"Final handoff row")
	assert_eq(count,7)

func test_a7_canvas_ground_and_foot_region_preserved() -> void:
	for i in range(5):
		var name := "%02d.png" % i
		var before := image(E+"baseline-a6/"+name)
		var after := image(SHARED+"thoma/swing/"+name)
		assert_eq(after.get_size(),Vector2i(512,512))
		assert_true(before.get_region(Rect2i(0,420,512,92)).get_data()==after.get_region(Rect2i(0,420,512,92)).get_data(),"Exact lower leg/boot source pixels")
		var bottom := 0
		for y in range(512):
			for x in range(512):
				if after.get_pixel(x,y).a>0.5:bottom=maxi(bottom,y)
		assert_between(bottom,463,465)
	for item in json(E+"baseline-a6/hashes.json"):
		if item.path.ends_with(".png"):assert_eq(item.sha256,FileAccess.get_sha256(REPO+item.path))

func test_a7_contact_and_lowered_mace_pixels_are_preserved() -> void:
	var contact := image(SHARED+"thoma/swing/03.png")
	var old_contact := image(E+"baseline-a6/03.png")
	assert_true(contact.get_region(Rect2i(340,175,140,46)).get_data()==old_contact.get_region(Rect2i(340,175,140,46)).get_data())
	assert_gt(contact.get_pixel(455,196).a,0.9)
	var follow := image(SHARED+"thoma/swing/04.png")
	var old_follow := image(E+"baseline-a6/04.png")
	var opaque_count := 0
	for y in range(338,379):
		for x in range(398,445):
			if old_follow.get_pixel(x,y).a>0.9:
				opaque_count+=1
				assert_eq(follow.get_pixel(x,y+19),old_follow.get_pixel(x,y),"Exact head pixels translated19px")
	assert_gt(opaque_count,200)
	assert_lt(json(E+"geometry-check.json").mace_before_after_04.error_px,1.0)

func test_a7_real_playback_and_all_adjacent_measured_proxies_exist() -> void:
	var playback = json(E+"playback-check.json")
	assert_true(playback.capture_complete)
	assert_eq(playback.fps,60.0)
	assert_eq(playback.selected.size(),7)
	assert_eq(playback.frames,playback.traced_frames+playback.untraced_terminal_frames)
	assert_true(playback.terminal_pixels_equal_previous_ready)
	for shot in playback.selected:assert_true(FileAccess.file_exists(E+shot.file))
	var pairs: Array = json(E+"sequence-check.json").pairs
	assert_eq(pairs.size(),6)
	for pair in pairs:
		for name in CHECKS:assert_has(pair.region_mean_rgb_delta,name)
		assert_between(pair.garment_silhouette_iou,0.0,1.0)
		assert_has(pair,"character_height_delta_px")
		assert_true(pair.iou_source.contains("NOT"))
		assert_eq(pair.visual_result,"FAIL")
	assert_eq(json(E+"landmark-deltas.json").pairs.size(),6)

func test_a7_failures_are_not_disguised_by_geometry_pass() -> void:
	var audit: Array = json(SHARED+"frame-audit.json")
	for index in range(5):
		var path := "thoma/swing/%02d.png" % index
		var rec: Dictionary = audit.filter(func(r):return r.path==path)[0]
		assert_eq(rec.status,"PLACEHOLDER")
		for name in ["face_hair","stole","embroidery","tassels","cuffs","hem","seams","landmarks","sequence"]:
			assert_true(rec.region_review[name].begins_with("FAIL:"))
		for name in ["palette","bag_count","feet","mace"]:
			assert_true(rec.region_review[name].begins_with("PASS:"))
