extends CPUParticles2D
## Observable world clock for the pause regression; actual particles inherit
## the same pausable process mode and cannot process during tree pause.
var processed_seconds := 0.0
func _process(delta: float) -> void:
	processed_seconds += delta
