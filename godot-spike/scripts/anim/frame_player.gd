extends Node
## Fixed-foot-pivot texture swaps; frame time is pausable world time.
signal frame_entered(index: int)
signal animation_event(event: Dictionary, world_anchor: Vector2)
signal finished
const Manifest = preload("res://scripts/anim/anim_manifest.gd")
var manifest: Dictionary
var character: String
var body: Sprite2D
var sequence: Dictionary = {}
var frame_index := 0
var frame_time_ms := 0.0
var playing := false
var held := false
var reduced := false
var facing_right := true
var pixels_per_frame_pixel := 48.88 / 360.0
var indices: Array = []
var cursor := 0
var textures: Dictionary = {}
var started_process_frame := -1

func configure(source: Dictionary, id: String, sprite: Sprite2D) -> void:
	manifest = source
	character = id
	body = sprite
	for s in manifest.sequences.values():
		if s.character == id:
			for f in s.frames: textures[f.path] = load(Manifest.ROOT + f.path)
	show_idle()

func play(key: String, low_motion: bool = false) -> void:
	sequence = manifest.sequences[key]
	reduced = low_motion
	indices = sequence.get("reduced_frame_indices", range(sequence.frames.size())) if reduced else range(sequence.frames.size())
	cursor = 0
	frame_time_ms = 0
	playing = true
	started_process_frame = Engine.get_process_frames()
	enter_frame(int(indices[0]))

func show_idle() -> void:
	playing = false
	sequence = manifest.sequences[character + ".idle"]
	frame_index = 0
	frame_time_ms = 0
	apply_frame()

func _process(delta: float) -> void:
	if not playing or held or Engine.get_process_frames() == started_process_frame: return
	frame_time_ms += delta * 1000.0
	while playing and frame_time_ms >= duration_ms():
		frame_time_ms -= duration_ms()
		cursor += 1
		if cursor >= indices.size():
			playing = false
			finished.emit()
		else:
			if int(indices[cursor]) == int(sequence.get("contact_frame_index", -1)):
				frame_time_ms = 0
			enter_frame(int(indices[cursor]))
			# Contact can pause the tree synchronously from a frame signal.
			if held or get_tree().paused:
				break

func duration_ms() -> float:
	return sequence.get("reduced_duration_ms", sequence.frames[frame_index].duration_ms) if reduced else sequence.frames[frame_index].duration_ms

func enter_frame(index: int) -> void:
	frame_index = index
	apply_frame()
	for event in sequence.get("events", []):
		if int(event.frame) == index:
			animation_event.emit(event, anchor_world(event.anchor))
	frame_entered.emit(index)

func signed_scale() -> Vector2:
	var native_right: bool = manifest.characters[character].facing == "right"
	return Vector2(pixels_per_frame_pixel * (1 if facing_right == native_right else -1), pixels_per_frame_pixel)

func apply_frame() -> void:
	var f: Dictionary = sequence.frames[frame_index]
	var c: Dictionary = manifest.characters[character]
	var offset: Array = [0,0] if reduced else f.get("offset", [0,0])
	body.centered = false
	body.texture = textures[f.path]
	body.scale = signed_scale()
	body.position = (Vector2(offset[0],offset[1]) - Vector2(c.pivot[0],c.pivot[1])) * signed_scale()

func anchor_world(anchor: Array) -> Vector2:
	return body.to_global(Vector2(anchor[0],anchor[1]))
