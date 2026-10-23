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
