# Spike 02 adapter notes

The pure rules model is unchanged. `event_plan` dispatches event dictionaries by
type into attack, damage and movement queues, retaining order within each queue.
Causal presentation stages are swing → contact damage → displacement; transport
order and unknown informational events do not change that dependency. This is a
single-attack spike, not a general multi-attacker scheduler.

Every actor uses the shared fixed-pivot frame player; source native facing is
recorded in the manifest. The diagonal closing step is a manifest frame offset,
not whole-body rotation. Generated armor and cloth are candidates; Thoma weapon
identity remains PLACEHOLDER because his original crop has no weapon.

## Whole-frame hitstop (A4)

`World` is explicitly PROCESS_MODE_PAUSABLE. Actors, frame players, camera,
painting, grid, particles and damage numbers descend from it. All world tweens
are created by the animated world node. The root and HUD are ALWAYS so keyboard
focus and debug input keep working. The root's camera/depth update exits while
the tree is paused. No Engine.time_scale mutation.

Frame entry swaps the contact texture, emits manifest spark and SFX events, then
starts flash, reaction frame zero, damage number and initial shake offset on the
same process frame. `get_tree().paused = true` freezes the complete world. A
process-always, ignore-time-scale SceneTreeTimer releases the pause; a monotonic
clock guard prevents early release. A second guard counts subsequent process
frame deltas, excluding the timer's creation frame; fixed-60-fps capture therefore
holds five frames (83.33ms), rather than four. Sound starts at contact and is allowed to
ring out, while visual world motion is frozen. UI remains live and attack/setup/
motion preference mutations remain locked. This does not claim audible audition.

Reduced Motion uses only swing key poses 0,3,5 at 100ms each. There is no smear,
offset closing step, camera shake, flash or particle emission. Logical knockback
uses 30ms and blocked shove is zero; the damage number is stationary and fades.
Hitstop is unchanged. Sequence events still record suppressed visual triggers,
so contact scheduling can be compared without claiming an emitted effect.

## Readability choice (A5)

Keep option **a**: 0.98 × baseline 48.88px body height, with 1.5× attack zoom
(71.85px reference body at contact). Zoom enters over 240ms and returns over
180ms, concurrent with swing and settle. Camera focus moves 40% toward the
attacker/target midpoint to avoid exposing blank space outside the painting.
Reduced Motion leaves the camera unchanged.

Option b, 1.3× persistent unit scale without zoom, has **16 opaque overlapping
screen pixels between the two knights at rest in the unit-blocked setup**.
Chosen option a has zero nonparticipant overlap in all six rest/contact checks.
Deliberate attacker/target contact overlaps 80 / 166 / 171 screen pixels in
setups a / b / c; no zero contact-intersection claim is made. Source alpha
threshold is 128, counting weapons as part of the silhouette, excluding rings,
labels, flash and VFX. Full viewport transforms include mirroring and camera
zoom; these are silhouette estimates, not a segmentation of the final VFX image.

A8 corrected an A5 measurement error: decomposed global_scale omitted the
rotation that Godot uses to represent a negative X scale. The earlier 92px,
63/29/81px and preliminary 1px claims are invalid and superseded here. The
selected 0.98 scale is retained; no claim is made that exactly 2% reduction is
necessary. The corrected evidence still supports the camera choice.

[Twelve actual 720p captures and transforms](evidence/spike02/readability.json),
[opaque-mask measurements](evidence/spike02/readability-overlap.json),
[camera contact](evidence/spike02/readability-a-setup2-contact.png),
[large-unit rest](evidence/spike02/readability-b-setup2-rest.png).
These twelve captures were refreshed during A8 with the final HUD and complete
viewport transforms; earlier versions remain in the A5 commit history.
Knight B's light shield field supplies value contrast independently of labels;
the final grayscale, label-free runtime proof is part of A8.

The A8 capture also measures source frame 1 for blocked stagger (the actual
buckled pose), rather than sampling the phase label before the next texture swap.
Contact spokes are immediate world-space geometry, so the spark onset is visible
before CPUParticles2D's first simulation tick; the secondary emitter and spokes
both pause. Flash blends 65% white, retaining pose detail, and the damage number
uses an 18px reference font to avoid covering the weapon.

## spike-02 A2 overrides

The earlier sections are Phase A history. A2 uses `thoma/idle/01.png` and six
mace frames; the weapon is **APPROVED (Owner, 2026-10-24)**; art approval is separate.
Durations are 180/70/40/80/100/150 ms (620 total), contact remains index 3,
and the registered mace head anchor is [455,196]. Fixed pivot and offsets are
unchanged, preserving the existing mirror/foot tests. Reduced Motion still
omits smear frame 2 and retains poses 0/3/5; its stationary spatial contact
limitation remains disclosed.

Camera zoom is now **1.4×**, focus weight **0.52**, with existing timing and
unchanged rule positions. Opaque-mask measurements at all three rest/contact
setups find zero nonparticipant overlap; intended attacker/target contact
intersections are **71/157/164 pixels**. The label-free grayscale/zoom/rest
captures also have no silhouette overlap. These are measured sampled poses,
not proof of every possible battle placement.

Knight B carries a textured short bone crest and light shield across all seven
frames. Frame source hashes and edit coordinates are in the shared sources.
HP bars follow the current sprite transform in the always-processing CanvasLayer;
they remain visible during hitstop. Damage numbers sit above the bars.

The HUD previews the pure rules result before contact and updates HP on damage
events. Space arms first and confirms on the next physical press. `_input`
consumes both Space edges for the attack action to prevent global press plus
focused Button release from performing both actions. Help/debug/forecast unwind
with Escape before exit. Scene/setup/reduced-motion mutations remain locked
during playback; help still responds during the world pause. All default
player-facing labels are Traditional Chinese; technical English is debug-only.

Final evidence and limits: [spike02-a2](evidence/spike02-a2/),
[verification](VERIFICATION.md#spike-02-a2), [handoff](HANDOFF.md#spike-02-a2).
