# W1 — A9 impact gaps / planned changes

Measured from clean `20d9844` on `b2f460b`, Godot 4.7.2 / AMD 780M GL
Compatibility, native 1280×720, fixed 60 FPS, setup 1. `before/timeline.json`
is the post-draw record; `before/impact-strip.png` labels contact ±8 frames.
Contact F19 (300 ms), hold F19–23, movement F24, input-ready F56:
**0.916667 s simulation**, 1.296902 s wall time including readbacks/movie.
Hitstop measured 83.333 ms process / 122.993 ms wall; requested minimum 80 ms.
Wall capture cost is not player latency. No source frame/timing changes.

The following are design hypotheses about weak readability, not human review
results or a claim that a universal genre standard specifies exact numbers.
The planned values are tunable starting points for W2.

| Layer | Measured A9 | Why it can read weak | Planned spike-03 |
| --- | --- | --- | --- |
| Hitstop | 80 ms requested, 5 rendered frames | Little distinction between ordinary and important blows | 110 ms normal, 170 ms presentation crit; retain real-time guard, pausable world and responsive HUD |
| Shake | first (3.4,−1.7) px, 200 ms, power decay 2; then non-directional sin/cos | Does not communicate force from attacker to target | First kick 8 px on hit vector, 3 exponential-decay oscillations over 200 ms; crit 12 px |
| Flash | uniform 1, actual white mix 0.65, 35 ms fade after hold | Pale sprite detail rather than a clear impact accent | Full warm-white mix, 1 extra frame hold then 80 ms fade; Reduced Motion remains suppressed |
| Target recoil | zero target delta throughout F19–23 | Contact pose is frozen before force visibly reaches the target | Immediate 9 px visual-only pivot nudge on contact, eased back separately from rules knockback |
| Sparks | 7 thin 1.2 px brass spokes, 24 CPU sparks, 300 ms lifetime | Thin strokes at ~48 px unit scale have limited emphasis | 11 brighter 2 px spokes plus directional streak, 36 sparks |
| Clean-hit dust | zero dust emitter at contact; dust only on blocked recoil | Feet look disconnected from the ground | 18-particle dust puff on every contact, frozen with world |
| Number | 18 px; contact scale (1,1); rise 30 px / 380 ms | No immediate size accent | 28 px, scale 1.6 → overshoot → 1 in 120 ms; crit 34 px/clay accent |
| Zoom punch | zoom 1.4, constant across contact hold | Framing has no contact accent | +0.06 instantaneous punch returning over 100 ms after hold; Reduced Motion none |
| Sound | one 240 ms deterministic hit, −7 dB, contact only | No preparation or landing cue | Named whoosh, impact/crit, knockback/blocked thud hooks; deterministic PLACEHOLDER synthesis |
| Crit read | absent (fixed damage 2) | Cannot compare impact tiers | Debug C / capture-only presentation variant, same HP and cell outcome |

## Resource criteria / evidence limits

Read-only [game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md)
and [game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md)
methods: discrete event layers; transient effects return to rest; presentation
does not alter simulation; real-time pause guard; bounded pacing; motion
accessibility; HUD and focus remain usable. No code/assets copied or installed.

Keep if same-frame sync, all 3 unchanged rule outcomes, no stuck inputs,
normal/crit ≤1.7 s (target ≤1.2), reduced ≤normal and existing tests pass.
Discard/tune layers if they obscure actors or delay return to input. Human
hit-feel is **HUMAN_PENDING**, regardless of automated success.

CPU particles do not expose exact live counts. Timeline reports live emitter
count and their summed capacity as an explicitly labelled upper bound; immediate
spokes are separate burst nodes. This is not an exact per-particle census.
All frames from contact −8 through ready are PNGs (thus including required −6).
W1 did not modify gameplay or the shared animation manifest/PNG bytes.
