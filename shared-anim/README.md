# Shared impact animation — spike 02 Phase A

Engine-neutral demonstration assets; no engine adoption or character equipment
decision. P010 remains PROPOSED. Question: do actual weapon poses and distinct
reactions make this one hit readable? Keep for comparison only if the Owner can
recognize the swing, contact and blocked recoil without explanation; reject or
retune if it still reads as sliding paper. Human playtest is HUMAN_PENDING.

## Contract v1

`manifest.json` is the single playback source. `manifest.schema.json` describes
its structure; the engine adapter additionally validates files and references.
Paths are relative, forward-slash `<character>/<sequence>/<nn>.png`, zero based.
All PNGs are straight-alpha RGBA, **512 × 512**, fixed ground pivot **[256,464]**.
No per-frame auto-fit: a character's head-to-ground reference height is 360 px.
Thoma's original 711px crop scales by 360/711; knight's 863px crop by 360/863.
Body board scale is 48.88/360 world pixels per frame pixel before A5's experiment.
The extra canvas accommodates the weapon arc; it does not enlarge the body.
Facing is screen-right; the opposite direction mirrors around the fixed pivot,
including offsets and contact anchors. No vertical mirroring or facing-dependent
rule changes. Feet use the pivot, never an opaque bounding-box center.

Sequences: Thoma idle (original crop) + six swing poses (anticipation, raised
blade, sweep, contact, follow-through, recover); each knight idle + three hit
poses (flinch, recoil, settle) + three stagger poses (brace, buckle, recover).
Knight B has a pale shield field, retained in all poses; its value
contrast is intended to remain visible in grayscale without identity labels.
Every sequence is non-looping. Returning to idle is the adapter's responsibility.
`offset` is a frame-pixel visual offset and defaults to [0,0]. Durations are
positive integer milliseconds; indices start at zero. `events.anchor` belongs
to the sequence character's frame. Spark and sound fire at contact entry.

Six swing durations total 620ms; contact hold adds 80ms; target reactions run
concurrently after contact; final settle is 180ms. Expected attack ~880ms before
frame quantization, capped at 1700ms INCLUDING hitstop. No rule waits for artwork.
Reduced Motion omits smear frames using `reduced_frame_indices`, retains contact
and event delivery, disables flash/shake/particles/camera, and uses minimal shove
and a 30ms logical knockback. `reduced_duration_ms` controls key-pose time.

Camera and displacement are presentation in reference 1280×720 pixels; camera
focus is attacker/target midpoint, zoom and return times are in the manifest.
Camera selection and larger-unit candidates are engine adapter options.
`scenarios` bind the existing setups to reaction sequences; no new combat rules.

## Provenance caveat

The specified Thoma crop (1558,0,520,711) is empty-handed. The brief's reference
to his existing sword cannot be satisfied literally. The demonstration uses the
straight sword visible on the first figure of the SAME original party atlas as
a weapon reference, while preserving Thoma's identity. **Weapon identity is
PLACEHOLDER**, not an equipment or story decision. No source PNG is edited.

## Distribution

Godot syncs this folder to `godot-spike/art/anim-shared/`; byte parity is tested.
Source remains here. Phase B may later sync to the web public folder, with the
same parity test. Phase A does not edit the web project. Import caches and rejected
attempts are not runtime assets; sync copies manifest/schema/docs/contact sheet,
reference crops and runtime frames, excluding `rejected/` and build tools.
Full prompts, references, cleanup and output SHA-256 belong in SOURCES.md.
