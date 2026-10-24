extends "res://addons/gut/test.gd"
const SHARED = "res://art/anim-shared/"
const REPO = "res://../"
const E = "res://docs/evidence/spike02-a9/"
const CHECKS = ["face_hair","stole","embroidery","tassels","cuffs","hem","palette","seams","bag_count","feet","mace","landmarks","sequence"]
const TARGETS = [Vector2(192,85),Vector2(259,87),Vector2(449,110),Vector2(455,196),Vector2(421,376)]

func json(path: String):
	return JSON.parse_string(FileAccess.get_file_as_string(path))

func image(path: String) -> Image:
	var im := Image.new()
	assert_eq(im.load_png_from_buffer(FileAccess.get_file_as_bytes(path)),OK)
	return im

func test_a9_immutable_anchors_and_full_manifest_contract() -> void:
	for pair in [["thoma/idle/01.png","c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"],["thoma/swing/05.png","f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"]]:
		assert_eq(FileAccess.get_sha256(SHARED+pair[0]),pair[1])
		assert_eq(FileAccess.get_sha256(REPO+"shared-anim/"+pair[0]),pair[1])
	var m = json(SHARED+"manifest.json")
	assert_eq(m,json(E+"baseline-a8/manifest.json"))
	assert_eq(m.characters.thoma.canvas_size,[512.0,512.0])
	assert_eq(m.characters.thoma.pivot,[256.0,464.0])
	var swing = m.sequences["thoma.swing"]
	assert_eq(swing.contact_frame_index,3.0)
	assert_eq(swing.frames.map(func(f):return f.duration_ms),[180.0,70.0,40.0,80.0,100.0,150.0])
	assert_eq(swing.reduced_frame_indices,[0.0,3.0,5.0])
	for event in swing.events:assert_eq(event.anchor,[455.0,196.0])

func test_a9_canvas_rgba_ground_and_foot_occupancy() -> void:
	for i in range(5):
		var im := image(SHARED+"thoma/swing/%02d.png" % i)
		assert_eq(im.get_size(),Vector2i(512,512))
		assert_eq(im.get_format(),Image.FORMAT_RGBA8)
		assert_eq(im.get_pixel(0,0).a,0.0)
		var bottom := -1
		var grounded := 0
		for y in range(512):
			for x in range(512):
				if im.get_pixel(x,y).a>0.5:bottom=maxi(bottom,y)
				if y==464 and x<410 and im.get_pixel(x,y).a>0.5:grounded+=1
		assert_between(bottom,463,465)
		assert_gt(grounded,4,"Actual boot pixels on ground464")

func test_a9_independent_final_mace_centres_and_opaque_contact() -> void:
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
		assert_gt(count,150)
		if count:assert_lte((total/count).distance_to(target),4.0)
	assert_gt(image(SHARED+"thoma/swing/03.png").get_pixel(455,196).a,0.9)

func test_a9_baselines_are_hashed_and_never_runtime_references() -> void:
	for seq in json(SHARED+"manifest.json").sequences.values():
		for frame in seq.frames:
			for forbidden in ["baseline-a8","baseline-a7","baseline-a6","baseline-a5","baseline-a4","baseline-a3","baseline-a2","attempts/","normalized/"]:
				assert_false(frame.path.contains(forbidden))
	for r in json(E+"baseline-a8/hashes.json"):
		if r.path.ends_with(".png"):assert_eq(r.sha256,FileAccess.get_sha256(REPO+r.path))

func table_row(r: Dictionary) -> String:
	var flags: Array[String] = []
	for name in CHECKS:flags.append(("1 " if name=="bag_count" else "")+r.region_review[name].split(":")[0])
	return "| `%s` | %s | %s | %s |" % [r.path,r.status," | ".join(flags),r.reason]

func test_a9_placeholder_gate_and_handoff_match_every_item() -> void:
	var table := FileAccess.get_file_as_string(E+"frame-status-table.md")
	var handoff := FileAccess.get_file_as_string("res://docs/HANDOFF.md")
	var old = json(E+"baseline-a8/frame-audit.json")
	var old_by_path := {}
	for r in old:old_by_path[r.path]=r
	var count := 0
	for r in json(SHARED+"frame-audit.json"):
		if not r.path.begins_with("thoma/"):continue
		count+=1
		assert_eq(r.sha256,FileAccess.get_sha256(SHARED+r.path))
		assert_eq(r.bag_count,1.0)
		assert_eq(r.weapon_status,"APPROVED")
		var passed: bool = r.technical_check.pass
		for name in CHECKS:
			assert_has(r.region_review,name)
			var result: String = r.region_review[name].split(":")[0]
			assert_true(result in ["PASS","FAIL"])
			passed=passed and result=="PASS"
			if result=="FAIL":assert_gt(r.region_review[name].length(),12)
			assert_true(r.a8_to_a9_change[name] in ["same","improved","worse"])
			if old_by_path[r.path].region_review[name].begins_with("PASS"):
				assert_eq(result,"PASS","No previously passing A8 item regresses")
		assert_eq(r.status,"PASS" if passed else "PLACEHOLDER")
		assert_true(table.contains(table_row(r)))
		if handoff.contains("## spike-02 A9\n"):
			assert_true(handoff.split("## spike-02 A9\n")[1].contains(table_row(r)),"Final handoff matches13-item gate")
	assert_eq(count,7)

func test_a9_every_region_attempt_is_bounded_hash_bound_and_at_most_three() -> void:
	var log = json(E+"a9-fix-log.json")
	assert_eq(log.order,["03","02","04","00","01"])
	var seen := {}
	var counts := {}
	for op in log.operations:
		assert_false(op.whole_frame_regeneration)
		assert_eq(op.tool,"Python Pillow manual donor-pixel compositing")
		assert_true(op.region in ["head","stole","embroidery","tassels","mace","legs_feet"])
		var key: String = op.frame+"/"+op.region
		counts[key]=counts.get(key,0)+1
		assert_false(seen.has(key+str(op.attempt)))
		seen[key+str(op.attempt)]=true
		assert_between(op.attempt,1.0,3.0)
		for pair in [["input","input_sha256"],["output","output_sha256"],["mask","mask_sha256"],["permission_mask","permission_mask_sha256"]]:
			assert_eq(op[pair[1]],FileAccess.get_sha256(REPO+op[pair[0]]))
		if op.changed_pixels>0:assert_gt(op.transform.size(),0)
		for n in CHECKS:assert_has(op.regression_check_13,n)
		var permission := image(REPO+op.permission_mask)
		assert_eq(permission.get_size(),Vector2i(512,512))
		# Grayscale masks have opaque alpha even where RGB is black. Measure
		# actual white permission pixels, not get_used_rect()'s alpha bounds.
		var allowed := 0
		for y in range(512):
			for x in range(512):
				if permission.get_pixel(x,y).r>0.5:allowed+=1
		assert_gt(allowed,0)
		assert_lt(allowed,512*512/2,"No full-frame permission mask")
	for n in counts.values():assert_lte(n,3)
	assert_eq(counts.size(),30,"All6 regions considered on each of5 frames")

func test_a9_final_pixels_outside_kept_masks_are_exactly_a8() -> void:
	var log = json(E+"a9-fix-log.json")
	for f in log.frames:
		var row: Dictionary = log.frames[f]
		assert_eq(row.sha256,FileAccess.get_sha256(REPO+row.path))
		assert_eq(row.kept_mask_sha256,FileAccess.get_sha256(REPO+row.kept_mask))
		var base := image(E+"baseline-a8/"+f+".png")
		var live := image(REPO+row.path)
		var kept := image(REPO+row.kept_mask)
		var outside := 0
		var changed := 0
		for y in range(512):
			for x in range(512):
				if base.get_pixel(x,y)!=live.get_pixel(x,y):
					changed+=1
					if kept.get_pixel(x,y).r<0.5:outside+=1
		assert_eq(outside,0,"All unchanged regions retain exact A8 RGBA")
		assert_gt(changed,0)
		for region in row.kept_regions:
			assert_true(log.operations.any(func(op):return op.frame=="thoma/swing/"+f+".png" and op.region==region and op.kept))

func test_a9_actual_movie_region_flicker_and_landmark_evidence_exist() -> void:
	var p = json(E+"playback-check.json")
	assert_true(p.capture_complete)
	assert_eq(p.fps,60.0)
	assert_gte(p.frames,50.0)
	assert_eq(p.selected.size(),7)
	assert_eq(p.pairs.size(),6)
	for shot in p.selected:
		assert_true(FileAccess.file_exists(E+shot.file))
		for region in ["head","stole","embroidery","tassels","mace","legs_feet"]:assert_has(shot.region_masks,region)
	for pair in p.pairs:
		for region in ["head","stole","embroidery","tassels","mace","legs_feet"]:assert_has(pair.region_mean_rgb_delta,region)
		assert_between(pair.garment_silhouette_iou,0.0,1.0)
		assert_has(pair,"character_height_delta_px")
	for row in json(E+"landmark-deltas.json").per_frame.values():
		for name in ["head_centre","hand_weapon","hand_free","elbow_left","elbow_right","knee_left","knee_right","foot_left","foot_right","mace_head"]:
			assert_has(row,name)
			assert_has(row[name],"measured")
			assert_has(row[name],"target")
