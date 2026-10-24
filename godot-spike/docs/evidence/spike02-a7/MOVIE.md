# A7 native60FPS capture

`attack-60fps.avi` is complete Godot `--write-movie` output at `--fixed-fps60`,
59 frames,1280x720,7,272,394 bytes. No subsampling/transcoding.
This is the same native movie used for W3 playback/trace/region measurements.

Strike frame2 → input-ready57: 0.916667s.
Full decodedRGB is identical on contact frames20–24:
83.333ms hold; frame25 resumes. Every decoded frame
hash is in movie-index.json; six supplementary PNGs in movie-samples/.

The movie-run wall time includes rendering/encoding and is NOT attack latency.
Normal and Reduced Motion real-time runs are in timing.json/timing-1080p.json,
with synchronous screenshot replays excluded. Dummy audio is not an audition
through physical speakers/headphones. GIF timing is quantized. Art FAIL;
human hit-feel remains HUMAN_PENDING, Owner art approval pending.
