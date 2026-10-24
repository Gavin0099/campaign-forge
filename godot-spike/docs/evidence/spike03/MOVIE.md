# spike-03 — actual rendered comparison

Godot 4.7.2 standard / GL Compatibility / AMD Radeon 780M, native 1280×720,
fixed 60 FPS. No animation source PNG or manifest changes. All three final
captures exited 0 and printed `CAPTURE_COMPLETE … pass=true`.

| Render | Profile | AVI | Strike → ready (process frames / 60) |
| --- | --- | --- | --- |
| Before | `impact_profile_a9_baseline.tres` | [58 frames](before/attack-60fps.avi) | 0.916667 s |
| After | `impact_profile.tres` | [60 frames](after/attack-60fps.avi) | 0.950000 s |
| After crit | tuned + `--crit` | [64 frames](after-crit/attack-60fps.avi) | 1.016667 s |

AVI includes startup/terminal frames; attack times use the timeline's actual
windup and input-ready process frames. Capture wall times include movie encoding
and synchronous GPU readbacks. Use [timing.json](timing.json) for nine separate
no-readback rendered runs; all wall and fixed-FPS times are below 1.7 s.
Normal/crit target of 1.2 s passes, Reduced Motion is shorter than normal.

- [Before/after GIF](before-vs-after.gif): contact-aligned, 720×382, 30 FPS,
  5,262,076 bytes (~5.02 MiB). Two **native 360×360 crops**, no upscaling;
  crop is (260,150)–(620,510), contact −8 through ready. The earlier-ready side
  holds its last real frame. It compares the contact event, not identical absolute
  start timestamps. GIF palette compression affects colour; PNG/AVI are primary.
- [Stacked strips](impact-strip-before-vs-after.png): contact ±8, native 320×320
  crops (260,150)–(580,470), five columns, labelled process frame/time/phase.
  [Before](before/impact-strip.png), [after](after/impact-strip.png),
  [crit](after-crit/impact-strip.png) use identical layout.
- Native stills: [contact](contact.png), [crit contact](contact-crit.png),
  [number pop, first resumed frame](number-pop.png), [1080p contact](contact-1080.png).
- Every native PNG from contact −8 through ready is delivered under each
  final render's `frames/`; JSON includes every strike frame and its clocks,
  transforms, pause, flash, visual recoil, number, emitter capacities and hooks.
  Exact CPU live-particle counts are unavailable; the labelled upper bound is
  emitter capacity, not an exact census.

No ffmpeg was found on PATH and none was installed. Existing Python 3.12 /
Pillow 12.2 decoded the Godot AVI's MJPEG chunks and built the GIF/strips.
Original AVI bytes are copied intact; each `movie-index.json` records its hash.
No commercial/reference-game material or generated art was used this segment.

## Visual iteration and timing separation

The first after/crit capture exposed a number backing that obscured contact.
[Rejected trial](pre-number-placement/README.md) retains contacts, full AVIs,
raw timelines and logs. Final numbers move −88 → −112 world px above the target
and remove the tuned backing. The baseline keeps A9's box and placement.
This is a W3 evidence-led readability correction to W2, not a HUD layout change.

The first 1080p still wrote PNG during hitstop and therefore took 2.0214 s
including synchronous encoding (`still1080-inline-encoding.log`). That is a
capture-instrumentation stall, not a no-readback performance measurement. The
tool now saves after ready; `still1080-run.log` records the repeated parsed-R
keyboard replay. Full 720p PNGs were always encoded after ready. All nine primary
timing runs have **zero** readbacks. Dummy audio verifies trigger/PCM timing,
not an audible-device mix or human hit-feel approval: **HUMAN_PENDING**.
