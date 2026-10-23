extends "res://addons/gut/test.gd"

func test_shared_copy_hash_parity() -> void:
	var source := ProjectSettings.globalize_path("res://../shared-anim")
	assert_true(DirAccess.dir_exists_absolute(source), "source directory must exist")
	compare_tree(source, "res://art/anim-shared")

func compare_tree(source: String, destination: String) -> void:
	for copied in DirAccess.get_files_at(destination):
		if copied.ends_with(".import") or copied.ends_with(".uid"): continue
		assert_true(FileAccess.file_exists(source.path_join(copied)), "no stale copied file " + copied)
	for name in DirAccess.get_files_at(source):
		if name.ends_with(".import") or name.ends_with(".uid"): continue
		assert_true(FileAccess.file_exists(destination.path_join(name)), name)
		assert_eq(FileAccess.get_sha256(source.path_join(name)), FileAccess.get_sha256(destination.path_join(name)), name + " exact bytes")
	for directory in DirAccess.get_directories_at(source):
		if directory in ["rejected", "tools"] or directory.begins_with("."): continue
		compare_tree(source.path_join(directory), destination.path_join(directory))
