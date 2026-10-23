# Actual 60 fps engine capture

[Full native AVI](attack-60fps.avi): **7,660,658 bytes (7.31 MiB)**, 1280×720,
60 frames at 60 fps, including the strike, return to ready and a short lead/tail.
Godot's built-in MJPEG/PCM movie writer produced it; no screen reconstruction or
generated movie frames. Audio content is present; audible audition is unverified.

The separate lossless PNG run recorded **73 frames**. The attack begins at frame
16 and input is ready at frame 71: **55/60 = 0.9167 seconds**. The full sequence
is about 91 MiB and stays in the ignored `.godot/spike02-movie/` folder. Six
unchanged PNGs are committed under `movie-samples/` (7.68 MiB):

- [16 — anticipation](movie-samples/frame00000016.png)
- [26 — raised blade](movie-samples/frame00000026.png)
- [34 — contact / first held frame](movie-samples/frame00000034.png)
- [38 — last held frame](movie-samples/frame00000038.png)
- [45 — recoil](movie-samples/frame00000045.png)
- [71 — input ready](movie-samples/frame00000071.png)

All five contact frames **34–38 are byte-identical**; frame 39 differs. The
held image is therefore 5/60 = **83.33 ms** at playback rate, quantized from the
manifest's 80ms. The full-frame comparison includes every rendered world effect.
The HUD can still process during this freeze, proven separately by GUT.

[Movie index](movie-index.json) retains every raw PNG's frame number, byte count
and SHA-256, plus the AVI header/hash, selected-frame sizes and timing boundaries.
[PNG log](movie-run.log), [PNG timings](movie-timing.json),
[AVI log](movie-avi-run.log), [AVI timings](movie-avi-timing.json).

PNG encoding took about 21.5 seconds; its wall-clock attack time of about 18.3
seconds is **capture throughput**, not 18 seconds of gameplay. The fixed-step
game-time accumulator was 0.93 seconds. Normal rendered wall times are measured
separately in [timing.json](timing.json). AVI omits the PNG inspection pre-roll
to keep the complete clip under 8 MiB. Both runs use the same assets and timing.
