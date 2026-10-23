# spike-02 A2 rendered movie

[Play/download the native 60 fps AVI](attack-60fps.avi): 1280×720, 60 frames,
7,365,366 bytes (7.02 MiB). Complete Godot `--write-movie` output, no retiming,
reconstruction, interpolation or omitted attack frames. First two frames are
pre-roll; strike starts at frame 2, input-ready at 57: **55/60 = 0.916667 s**.
Recording begins in the post-banner state so the transient opening banner is
not irrelevant pre-roll. It is a normal open attack with the same live HUD.

A second native PNG movie has 60 frames. Contact frames **20–24** have identical
SHA-256 (five frames / **83.333 ms**); frame 25 visibly resumes. Six exact PNGs
are retained in [movie-samples](movie-samples): strike, raise/start of swing,
contact, final held contact, recoil, input-ready. The full raw PNG set stays in
the ignored worktree-local `.godot/spike02-a2-movie/`; no raw frames were edited.
The compact AVI preserves the complete sequence; the large PNG set is sampled
for repository size only. All 60 PNG hashes, byte totals and retained indices
are recorded in [movie-index.json](movie-index.json).

AVI metadata and hashes are validated from the RIFF/AVI header, not inferred
from the extension. Both actual commands and their completion markers are in
[movie-avi-run.log](movie-avi-run.log) and [movie-png-run.log](movie-png-run.log).
Encoding wall time was 2.4199 s / 17.0355 s for the attack, respectively; it is
**not gameplay duration**. Fixed 60 fps frame differences supply movie timing.
Ordinary rendered timing is separately recorded in [timing.json](timing.json).

Dummy audio driver was used for capture. The native movie records the engine
audio track; audible-device mix and human hit-feel acceptance remain pending.
