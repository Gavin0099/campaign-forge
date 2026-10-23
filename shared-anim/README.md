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
Thoma faces screen-right; knight artwork faces screen-left, as recorded per
character. The opposite direction mirrors around the fixed pivot,
including offsets and contact anchors. No vertical mirroring or facing-dependent
rule changes. Feet use the pivot, never an opaque bounding-box center.

Sequences: Thoma weapon idle + six swing poses (anticipation, raised
mace, sweep, contact, follow-through, recover); each knight idle + three hit
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
Swing frame offsets encode a short diagonal closing step (maximum 32.8 reference
pixels), matching the isometric neighbor projection without rotating the body.
`scenarios` bind the existing setups to reaction sequences; no new combat rules.

## Weapon proposal — spike-02 A2

**PROPOSED, Owner confirmation pending:** a short one-handed flanged mace,
dark iron head, worn oak haft and small brass collar, carried in the right hand.
Its blunt head fits the medical friar role and gives a readable weighty impact;
forearm length avoids a staff silhouette, brass echoes the existing medallion.
The holy symbol remains a medallion. No sword, blade, staff, book or magic glow.

Evidence cited by the Owner brief: `ui-prototype/docs/l03/character-prompt.txt:1`
specifies empty hands/no staff/book/glow; `ART-DIRECTION.md:9` names medical
satchel/teal; `ui-prototype/src/l03Scene.ts:51–54` names medical/support;
`playable-l03-research/DEMO-CONTRACT.md:17` permits melee 3 and heal 3.
On `origin/story/strengthen-narrative`, `docs/story/STORY.md:56` and
`COMPANION-ARCS.md:28,34` describe the friar/holy symbol; `ch01.ink:306`,
`ch02.ink:250` and `CREATIVE-BIBLE.md:74` reinforce that symbol, not a weapon.
`docs/DECISIONS.md` U003 is only a class frame. Canon names no weapon.

Manifest rest pose is `thoma/idle/01.png`; `idle/00.png` is the unchanged
original empty-handed crop for reference only. All six runtime swings now use
the proposed mace. Historical Phase A sword prompts remain provenance history,
and were NOT references for A2. Full attempts/hashes are in SOURCES.md and
generation-prompts.json. Review `thoma-weapon-style-check.png` and frame-audit.json:
idle/recover pass the model style check; five motion poses retain PLACEHOLDER
for costume-detail drift. Neither style PASS nor weapon PROPOSED is Owner approval.
Use `godot-spike/tools/prepare_a2_frames.py` for A2 cleanup, not the historical
Phase A `prepare_frames.py` / `build_manifest.py` which recreate the old candidates.

## Distribution

Godot syncs this folder to `godot-spike/art/anim-shared/`; byte parity is tested.
Source remains here. Phase B may later sync to the web public folder, with the
same parity test. Phase A does not edit the web project. Import caches and rejected
attempts are not runtime assets; sync copies manifest/schema/docs/contact sheet,
reference crops and runtime frames, excluding `rejected/` and build tools.
Full prompts, references, cleanup and output SHA-256 belong in SOURCES.md.
