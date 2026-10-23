# A3 native 60 FPS movie

`attack-60fps.avi` is Godot --write-movie output: 59 complete 1280x720 frames, 7,272,134 bytes. No subsampling or transcoding. Six PNGs in movie-samples are decoded supplementary frames.

Strike frame 2 to input-ready frame 57: **0.916667 s**. Contact frames 20–24: **83.333 ms**, with identical decoded full-frame RGB hashes. Frame 25 visibly resumes. `movie-index.json` records every decoded frame hash and retained samples.

The engine's printed elapsed_wall_s includes offline movie encoding and is not gameplay latency. The fixed-60-fps timeline is the movie measurement; ordinary real-time runs are separately in timing.json. Audio-driver Dummy was used: no physical audio-device audition or human hit-feel verdict is claimed. Human playtest remains HUMAN_PENDING.
