# Sound provenance

`impact_synth.gd` synthesizes a 0.24-second, 22050 Hz mono 16-bit PCM
AudioStreamWAV in memory: descending low sine, deterministic noise transient,
and a short metallic sine. Seed 90117. No recording, sample library, download,
voice or third-party dependency. This is original placeholder SFX written for
this spike, under the repository's existing rights (no new open-source license).

The player runs at -7 dB. It is a timing placeholder, not final sound design or
a human-verified mix. To audition, run the scene and press Space.

## spike-03 — all hooks are PLACEHOLDER

`make_hook()` adds original deterministic mono 22050 Hz / 16-bit PCM:
`swing_whoosh` (180 ms shaped noise, −14 dB), `impact` (unchanged A9 240 ms,
−7 dB), `impact_crit` (280 ms lower sine/noise/metal, −6 dB),
`knockback_thud` (280 ms low thud, −12 dB), `blocked_thud` (280 ms higher thud,
−12 dB). Seed = 90117 + Godot String hash of hook, with no external samples.
These timbres are temporary, not final sound design. Layer volumes and hook
names are tunable in `config/impact_profile.tres` / `ImpactProfile`.
Whoosh fires on swing frame 1 (frame 0 for Reduced Motion, which omits 1/2).
Impact/crit fires on frame 3; thud fires on landing or blocked recoil onset.
Dummy audio captures prove event timing/PCM, not device audition or human mix
approval. No download, package, sample library or licensing change.
