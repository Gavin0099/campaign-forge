# Test-only dependency

GUT **9.7.1**, compatible with Godot 4.7.x according to upstream's version table.
Source: https://github.com/bitwes/Gut/releases/tag/v9.7.1
Downloaded: https://github.com/bitwes/Gut/archive/refs/tags/v9.7.1.zip
ZIP SHA-256: `14969aa46adc84aa08cdd21b9f6d1a64addd92ae60b36f02d0521ed305aa4086`

Only upstream `addons/gut/` is vendored, without source edits. License: MIT,
Copyright (c) 2018 Tom "Butch" Wesley; full notice in [gut/LICENSE.md](gut/LICENSE.md).
This license covers GUT, not the project's story, original art or other files.
The editor plugin is not enabled; the headless CLI loads it for tests only.
The download succeeded, so no fallback runner was needed.

Run an import before tests to regenerate class/import caches:

```powershell
godot --headless --path godot-spike --import
godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
```
