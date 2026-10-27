extends RefCounted
## Inclusive, diagnostic CPU scopes; never used by gameplay decisions.
static var enabled := false
static var scopes := {}
static func add(label: String, started: int) -> void:
	if not enabled: return
	if not scopes.has(label): scopes[label]={"calls":0,"usec":0,"max_usec":0}
	var elapsed := Time.get_ticks_usec()-started
	scopes[label].calls+=1
	scopes[label].usec+=elapsed
	scopes[label].max_usec=maxi(scopes[label].max_usec,elapsed)
