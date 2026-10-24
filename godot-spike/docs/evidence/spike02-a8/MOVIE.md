# A8 native60FPS capture

`attack-60fps.avi` is complete Godot `--write-movie` output at `--fixed-fps60`,
59 frames,1280×720,7,273,022 bytes. No subsampling/transcoding.
It is the same successful native movie decoded for W3 flicker measurements.
The initial failed writer run is excluded and retained in w3-playback-failed-1.log.

Strike frame2 → input-ready57: 0.916667s.
Full decodedRGB is identical on contact frames20–24:
83.333ms hold; frame25 resumes. Every decoded frame hash
is in movie-index.json; six supplementary PNGs are in movie-samples/.

Movie-run wall time includes encoding/rendering and is not attack latency.
Normal and Reduced Motion real-time timing uses six no-readback runs per
resolution; screenshot replays are excluded. Dummy audio is not a physical
audition. GIF quantizes60FPS timing. Art FAIL,0/5; human feel HUMAN_PENDING,
Owner art approval pending. No complete-battle or commercial-quality claim.
