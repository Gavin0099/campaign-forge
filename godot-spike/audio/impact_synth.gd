extends RefCounted
## Original deterministic mono PCM synthesis. No external audio or packages.
static func make_hit() -> AudioStreamWAV:
	const RATE = 22050
	const LENGTH = 0.24
	var bytes := PackedByteArray()
	bytes.resize(int(RATE * LENGTH) * 2)
	var rng := RandomNumberGenerator.new()
	rng.seed = 90117
	for i in range(bytes.size() / 2):
		var t := float(i) / RATE
		var body := sin(TAU * (105.0 * t - 90.0 * t * t)) * exp(-t * 24.0)
		var crack := rng.randf_range(-1, 1) * exp(-t * 82.0)
		var metal := sin(TAU * 1430.0 * t) * exp(-t * 38.0)
		var sample := clampf((body * 0.58 + crack * 0.31 + metal * 0.11) * 0.78, -1, 1)
		bytes.encode_s16(i * 2, int(sample * 32767))
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = RATE
	stream.data = bytes
	return stream

static func make_hook(hook: String) -> AudioStreamWAV:
	# Original deterministic PLACEHOLDER timbres; no external sample or download.
	# Keep make_hit() byte-identical for the A9 baseline and PCM regression.
	if hook == "impact": return make_hit()
	const RATE = 22050
	var length := 0.18 if hook == "swing_whoosh" else 0.28
	var bytes := PackedByteArray()
	bytes.resize(int(RATE*length)*2)
	var rng := RandomNumberGenerator.new()
	rng.seed = 90117 + hook.hash()
	for i in range(bytes.size()/2):
		var t := float(i)/RATE
		var sample: float
		if hook == "swing_whoosh":
			sample = rng.randf_range(-1,1)*sin(PI*t/length)*exp(-t*12.0)*0.45
		elif hook == "impact_crit":
			sample = (sin(TAU*(82*t-60*t*t))*exp(-t*18)*0.65 + rng.randf_range(-1,1)*exp(-t*95)*0.25 + sin(TAU*1730*t)*exp(-t*32)*0.1)*0.8
		else:
			var pitch := 68.0 if hook == "knockback_thud" else 125.0
			sample = (sin(TAU*pitch*t)*exp(-t*28)*0.7 + rng.randf_range(-1,1)*exp(-t*65)*0.15)*0.7
		bytes.encode_s16(i*2,int(clampf(sample,-1,1)*32767))
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = RATE
	stream.data = bytes
	return stream
