extends "res://addons/gut/test.gd"
const Manifest = preload("res://scripts/anim/anim_manifest.gd")

func test_valid_manifest_and_every_frame_contract() -> void:
	var loader := Manifest.new()
	assert_true(loader.read())
	for sequence in loader.data.sequences.values():
		var character: Dictionary = loader.data.characters[sequence.character]
		for frame in sequence.frames:
			assert_true(FileAccess.file_exists(Manifest.ROOT + frame.path), frame.path)
			assert_true(loader.positive_int(frame.duration_ms), "positive integer milliseconds")
			var texture: Texture2D = load(Manifest.ROOT + frame.path)
			var image := texture.get_image()
			assert_eq(image.get_size(), Vector2i(character.canvas_size[0],character.canvas_size[1]), "fixed per-character canvas")
		if sequence.has("contact_frame_index"):
			assert_true(loader.valid_index(sequence.contact_frame_index, sequence.frames.size()))

func test_invalid_manifest_rejected_without_partial_data() -> void:
	var loader := Manifest.new()
	assert_true(loader.read())
	var valid := loader.data.duplicate(true)
	for key in ["version","characters","sequences","impact","camera","scenarios"]:
		var broken := valid.duplicate(true)
		broken.erase(key)
		assert_false(loader.validate(broken), "missing " + key)
		assert_true(loader.data.is_empty(), "bad parse cannot leave usable stale data")
	for duration in [0,-1,0.5,"80"]:
		var broken := valid.duplicate(true)
		broken.sequences["thoma.swing"].frames[0].duration_ms = duration
		assert_false(loader.validate(broken), "invalid duration")
	for index in [-1,6,1.2]:
		var broken := valid.duplicate(true)
		broken.sequences["thoma.swing"].contact_frame_index = index
		assert_false(loader.validate(broken), "bad contact index")
	var missing := valid.duplicate(true)
	missing.sequences["thoma.swing"].frames[0].path = "thoma/swing/99.png"
	assert_false(loader.validate(missing), "missing frame rejected")
	missing.sequences["thoma.swing"].frames[0].path = "../art/battlefield.png"
	assert_false(loader.validate(missing), "path escape rejected")

func test_reduced_keyposes_keep_contact_and_omit_smear() -> void:
	var loader := Manifest.new()
	assert_true(loader.read())
	var swing: Dictionary = loader.data.sequences["thoma.swing"]
	assert_has(swing.reduced_frame_indices, swing.contact_frame_index)
	assert_does_not_have(swing.reduced_frame_indices, 2.0)
	assert_eq(swing.reduced_frame_indices.size(),3)
