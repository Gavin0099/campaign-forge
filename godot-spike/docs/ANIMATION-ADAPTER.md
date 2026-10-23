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
clock guard prevents early release. Sound starts at contact and is allowed to
ring out, while visual world motion is frozen. UI remains live and attack/setup/
motion preference mutations remain locked. This does not claim audible audition.

Reduced Motion uses only swing key poses 0,3,5 at 100ms each. There is no smear,
offset closing step, camera shake, flash or particle emission. Logical knockback
uses 30ms and blocked shove is zero; the damage number is stationary and fades.
Hitstop is unchanged. Sequence events still record suppressed visual triggers,
so contact scheduling can be compared without claiming an emitted effect.
