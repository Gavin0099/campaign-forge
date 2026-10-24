# Runtime movies and strips

ffmpeg is unavailable. Godot Movie Maker recorded native 1280×720 MJPEG AVI at
60 simulation frames/s; Pillow only decodes frames and lays out PNG strips.
`movie-index.json` verifies AVI headers, every frame dimension and SHA-256.

- [Scroll/select/move/attack AVI](scroll-select-move-attack-60fps.avi): parsed D,
  middle-drag, O, F, actual mouse select → preview → confirm move. The subsequent
  attack resumes the exact first-attack state of the road policy at turn2;
  it is a staged operating sequence, not a continuous battle movie.
- [Enemy-phase AVI](enemy-phase-60fps.avi): real normal-speed playback of the
  road policy's turn2 enemy phase, no rule changes.
- [Camera follow/return strip](camera-follow-return-strip.png),
  [native extracted frames](camera-frames/), [per-frame camera data](camera-sequence.json).
- [Hit-feel comparison](hitfeel/impact-strip-spike03-vs-spike04.png): normal/crit
  spike03 vs toned spike04, contact ±8 frames; four AVIs in `hitfeel/`.

`capture-sequence.json` requires every parsed input check. Failed attempts and
logs remain under `attempts/` and `w6-sequence*.log`; final verified run is
`w6-sequence-verified.log`. An early script aborted on an empty timing array
yet reported pass; those rejected results are not acceptance evidence.

`capture-stills.json` instead drives a continuous deployment-to-turn12-win
battle through scene UI commands. Its images include first contact, ranged,
melee, turn4 warning, turn5 arrival, overview, enemy phase and win. This is an
automated operator, not a human playtest. Native 1080p deployment is separate.

AVI encoding and PNG readback stretch wall time. Fixed-fps process time is
the movie clock; it is not real input latency or a 60 FPS performance claim.
Unrecorded runtime timings and frame samples are in PERFORMANCE.md. Placeholder
audio was driven through Dummy, not listened to. HUMAN_PENDING remains.

