extends SceneTree
## Copy the complete source tree, excluding tooling/rejected/import byproducts.
func _initialize() -> void:
	var source := ProjectSettings.globalize_path("res://../shared-anim")
	var destination := ProjectSettings.globalize_path("res://art/anim-shared")
	var count := copy_tree(source, destination)
	print("SYNC_SHARED_ANIM files=%d pass=%s" % [count, count > 0])
	quit(0 if count > 0 else 1)

func copy_tree(source: String, destination: String) -> int:
	if DirAccess.make_dir_recursive_absolute(destination) != OK:
		return -100000
	var count := 0
	for name in DirAccess.get_files_at(source):
		if name.ends_with(".import") or name.ends_with(".uid"):
			continue
		var error := DirAccess.copy_absolute(source.path_join(name), destination.path_join(name))
		if error != OK:
			push_error("Shared animation copy failed: " + name)
			return -100000
		count += 1
	for directory in DirAccess.get_directories_at(source):
		if directory in ["rejected", "tools"] or directory.begins_with("."):
			continue
		count += copy_tree(source.path_join(directory), destination.path_join(directory))
	return count
