# A4 native 60 FPS movie

`attack-60fps.avi` is complete Godot `--write-movie` output at `--fixed-fps 60`:
59 frames at 1280x720, 7,270,584 bytes. Under 8 MiB; no frames
subsampled, transcoded or omitted. Six supplementary decoded PNG samples are
in movie-samples; every decoded frame hash is in movie-index.json.

Strike frame 2 to input-ready frame 57: 0.916667 seconds.
Contact frames 20 through 24 have identical full decoded RGB:
83.333 ms; frame 25 visibly resumes.

Encoding wall time is not gameplay latency. Ordinary timing.json and
timing-1080p.json measure six no-readback runs each. Dummy audio is not a
physical-device audition. Human hit-feel playtest remains HUMAN_PENDING.
