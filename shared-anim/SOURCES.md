# Animation sources — spike 02 Phase A

Original atlases remain unchanged. All generated frames: built-in `image_gen`, one attempt per frame. No rejected attempt. No commercial art or Ferry Dusk grading.

## Original reference crops

| Reference | Original | SHA-256 |
| --- | --- | --- |
| references/thoma.png | godot-spike/art/l03-party-v1.png rect(1558,0,520,711) | `ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90` |
| references/sword-reference.png | godot-spike/art/l03-party-v1.png rect(175,0,475,711) | `e25f94a801ed7573cacaa3c128cf98716e59bcd647c50c314bfcc5904ff91f23` |
| references/knight-a.png | godot-spike/art/l03-enemies-v1.png rect(15,8,745,863) | `d8243331a939ea2359ec5dd6549e99a152d8eebb53481221ecbabc4cc77f4576` |

## Full generation prompts and raw outputs

### raw/thoma-swing-00.png
Tool: image_gen; attempt 1/3. References: references/thoma.png, references/sword-reference.png
Raw SHA-256: `9b9abc677d83bdb671515bf64953acb3d85eddac73b7d96118aba20862a7ca97`

Use case: identity-preserve. Create ONE transparent full-body animation sprite of the elderly grey-haired man in reference 1, in an anticipation/wind-up pose facing screen right, feet planted, torso turned back slightly, right forearm raised holding the short straight sword shown in reference 2 behind his shoulder ready to swing. Preserve EXACTLY reference 1's weathered face, grey hair/beard, muted blue-green robe, bone/ivory stole with plant embroidery, leather belt pouch, round pendant, brown boots, head/body proportions, subdued top-left lighting, painterly ink edges and worn fabric texture. Reference 2 is ONLY for the sword, not the man/armor/shield. No redesign, no palette change, no new accessories. Isometric-ish three-quarter full figure, same camera angle as reference 1. All feet, head and blade entirely visible. Single figure centered on transparent 1024x1024 canvas, body height about 700 pixels, feet bottom at y=900, clear margins for weapon. No text, labels, grid, shadow or scenery. This is frame 00 of a six-frame sword swing, not a whole-body rotated idle. Real shoulder/elbow articulation. Absolutely match the source painting.

### raw/thoma-swing-01.png
Tool: image_gen; attempt 1/3. References: references/thoma.png, raw/thoma-swing-00.png
Raw SHA-256: `fb72c1459e526cfbdfe93555edbcf1e626fd00d28cc7c7a1702d01ba753ae788`

Use case: identity-preserve. ONE transparent full-body animation sprite, 1024x1024 requested. Reference 1 is the exact elderly grey-haired man to preserve: same weathered face, grey hair/beard, muted blue-green robe, bone ivory stole with plant embroidery, belt pouch, round pendant, brown boots, original proportions, subdued top-left lighting, dark painterly ink edges and worn fabric texture. Reference 2 is his previous wind-up frame, use EXACT SAME short straight steel sword with brass hilt, clothing, drawing style and body proportions. Same three-quarter view, facing SCREEN RIGHT. Full figure and all of sword entirely inside canvas. NO text, labels, grid, shadow, scenery, new accessories, armor, palette changes. True transparent background. Keep feet on a shared level and similar stance to reference 2. This must be a genuinely articulated pose, not a whole-figure rotation. Frame 01 raised blade: right shoulder forward, right elbow flexed, sword raised nearly vertical above his head as torso rotates toward screen-right. Left arm counterbalances, robe still follows windup. Anticipation before downswing.

### raw/thoma-swing-02.png
Tool: image_gen; attempt 1/3. References: references/thoma.png, raw/thoma-swing-00.png
Raw SHA-256: `8a94a4e381d89005669c9200f925054a8e1aa53d7bbca76d4f0aadb22aff50ae`

Use case: identity-preserve. ONE transparent full-body animation sprite, 1024x1024 requested. Reference 1 is the exact elderly grey-haired man to preserve: same weathered face, grey hair/beard, muted blue-green robe, bone ivory stole with plant embroidery, belt pouch, round pendant, brown boots, original proportions, subdued top-left lighting, dark painterly ink edges and worn fabric texture. Reference 2 is his previous wind-up frame, use EXACT SAME short straight steel sword with brass hilt, clothing, drawing style and body proportions. Same three-quarter view, facing SCREEN RIGHT. Full figure and all of sword entirely inside canvas. NO text, labels, grid, shadow, scenery, new accessories, armor, palette changes. True transparent background. Keep feet on a shared level and similar stance to reference 2. This must be a genuinely articulated pose, not a whole-figure rotation. Frame 02 swing: sword sweeps DOWN and RIGHT in a very readable broad diagonal arc. Right shoulder and elbow extend strongly toward screen-right, blade diagonal up-right in mid-sweep. Add a SHORT restrained translucent painted bone-grey blade smear behind the blade, no magic effect. Torso twists, knees brace.

### raw/thoma-swing-03.png
Tool: image_gen; attempt 1/3. References: references/thoma.png, raw/thoma-swing-00.png
Raw SHA-256: `e1007e646772e9b5b3d7f56aa8cb4e770249724b0e4699ff864e1d2f46747c06`

Use case: identity-preserve. ONE transparent full-body animation sprite, 1024x1024 requested. Reference 1 is the exact elderly grey-haired man to preserve: same weathered face, grey hair/beard, muted blue-green robe, bone ivory stole with plant embroidery, belt pouch, round pendant, brown boots, original proportions, subdued top-left lighting, dark painterly ink edges and worn fabric texture. Reference 2 is his previous wind-up frame, use EXACT SAME short straight steel sword with brass hilt, clothing, drawing style and body proportions. Same three-quarter view, facing SCREEN RIGHT. Full figure and all of sword entirely inside canvas. NO text, labels, grid, shadow, scenery, new accessories, armor, palette changes. True transparent background. Keep feet on a shared level and similar stance to reference 2. This must be a genuinely articulated pose, not a whole-figure rotation. Frame 03 CONTACT: right arm fully extended horizontally to screen-right at chest level, sword pointing horizontally screen-right, blade tip reaching an unseen opponent. No actual opponent, sparks or glow. Wrist and elbow strongly braced, shoulder compressed, robe pulled by torso twist. Feet planted, no smear; this is the held contact pose.

### raw/thoma-swing-04.png
Tool: image_gen; attempt 1/3. References: references/thoma.png, raw/thoma-swing-00.png
Raw SHA-256: `c4bf92b69f8bee4bc8dd4dccdc9bed90fcf00ac17806b76d0155d8f1a28b827c`

Use case: identity-preserve. ONE transparent full-body animation sprite, 1024x1024 requested. Reference 1 is the exact elderly grey-haired man to preserve: same weathered face, grey hair/beard, muted blue-green robe, bone ivory stole with plant embroidery, belt pouch, round pendant, brown boots, original proportions, subdued top-left lighting, dark painterly ink edges and worn fabric texture. Reference 2 is his previous wind-up frame, use EXACT SAME short straight steel sword with brass hilt, clothing, drawing style and body proportions. Same three-quarter view, facing SCREEN RIGHT. Full figure and all of sword entirely inside canvas. NO text, labels, grid, shadow, scenery, new accessories, armor, palette changes. True transparent background. Keep feet on a shared level and similar stance to reference 2. This must be a genuinely articulated pose, not a whole-figure rotation. Frame 04 follow-through: sword passes DOWN across the right side of the body toward screen-right, blade tip lowered, elbow beginning to bend; torso leaned a little forward and left hand counterbalancing. Robe and stole trail the swing. Show clearly different arm/blade pose from contact.

### raw/thoma-swing-05.png
Tool: image_gen; attempt 1/3. References: references/thoma.png, raw/thoma-swing-00.png
Raw SHA-256: `9a8e01df6a7e3273664fc9536f5a0dd74ef43180bba69c684ba3061eac998851`

Use case: identity-preserve. ONE transparent full-body animation sprite, 1024x1024 requested. Reference 1 is the exact elderly grey-haired man to preserve: same weathered face, grey hair/beard, muted blue-green robe, bone ivory stole with plant embroidery, belt pouch, round pendant, brown boots, original proportions, subdued top-left lighting, dark painterly ink edges and worn fabric texture. Reference 2 is his previous wind-up frame, use EXACT SAME short straight steel sword with brass hilt, clothing, drawing style and body proportions. Same three-quarter view, facing SCREEN RIGHT. Full figure and all of sword entirely inside canvas. NO text, labels, grid, shadow, scenery, new accessories, armor, palette changes. True transparent background. Keep feet on a shared level and similar stance to reference 2. This must be a genuinely articulated pose, not a whole-figure rotation. Frame 05 recover: torso upright again facing right, right arm and short sword lowered at his right side with blade pointing downward, left arm relaxed, weight settles on both feet. Return to a pose close to the original reference 1 idle. No smear.

### raw/knight-a-hit-00.png
Tool: image_gen; attempt 1/3. References: references/knight-a.png
Raw SHA-256: `10260a5c1dd3cfdc7ed5eb70da250e74c7f7d1b36543bfee56d078eaff900a79`

Use case: identity-preserve. ONE full-body hand-painted transparent animation sprite of the EXACT armored knight in reference. Preserve precisely the pointed closed steel helm with slit visor, battered silver armor, muted mauve tabard, dark leather straps, round mauve wood shield with metal rim and boss, and the short spear. Same proportions, muted palette, worn brush texture, thin dark ink edges, top-left light, three-quarter camera as original. Facing screen LEFT toward incoming hit; do not redesign. All extremities, shield, spear and boots inside 1024x1024 transparent canvas, substantial margin. No text, labels, background, ground shadow, other character, sparks or VFX. Feet stay planted on a common baseline. Pose must bend joints and react through shoulders/neck/knees, NOT rotate the whole idle image. FLINCH: a blow arrives from screen-left, head snaps slightly back toward screen-right, left shoulder compresses, shield arm tucks toward chest, spear hand loosens outward, knees soften. First impact pose, small braced recoil.

### raw/knight-a-hit-01.png
Tool: image_gen; attempt 1/3. References: references/knight-a.png
Raw SHA-256: `f528b4c5b14bd1dbc5eeba2e6a3e0c8e889c4bce684b0cab16ec3a506cfb592b`

Use case: identity-preserve. ONE full-body hand-painted transparent animation sprite of the EXACT armored knight in reference. Preserve precisely the pointed closed steel helm with slit visor, battered silver armor, muted mauve tabard, dark leather straps, round mauve wood shield with metal rim and boss, and the short spear. Same proportions, muted palette, worn brush texture, thin dark ink edges, top-left light, three-quarter camera as original. Facing screen LEFT toward incoming hit; do not redesign. All extremities, shield, spear and boots inside 1024x1024 transparent canvas, substantial margin. No text, labels, background, ground shadow, other character, sparks or VFX. Feet stay planted on a common baseline. Pose must bend joints and react through shoulders/neck/knees, NOT rotate the whole idle image. RECOIL: weight shifts backward screen-right, one knee deeply bent, shoulders lean back, shield lifted defensively across torso, spear extended away to screen-left. Clear body recoil, grounded feet, no falling.

### raw/knight-a-hit-02.png
Tool: image_gen; attempt 1/3. References: references/knight-a.png
Raw SHA-256: `1596e1e438609947b652f20302c8735233247bd400c495125b18eb7743cce376`

Use case: identity-preserve. ONE full-body hand-painted transparent animation sprite of the EXACT armored knight in reference. Preserve precisely the pointed closed steel helm with slit visor, battered silver armor, muted mauve tabard, dark leather straps, round mauve wood shield with metal rim and boss, and the short spear. Same proportions, muted palette, worn brush texture, thin dark ink edges, top-left light, three-quarter camera as original. Facing screen LEFT toward incoming hit; do not redesign. All extremities, shield, spear and boots inside 1024x1024 transparent canvas, substantial margin. No text, labels, background, ground shadow, other character, sparks or VFX. Feet stay planted on a common baseline. Pose must bend joints and react through shoulders/neck/knees, NOT rotate the whole idle image. SETTLE: regains upright stance, head lowered slightly, knees mostly straight, shield and spear lower toward original idle positions. Tension easing after being pushed back, near original idle.

### raw/knight-a-stagger-00.png
Tool: image_gen; attempt 1/3. References: references/knight-a.png
Raw SHA-256: `2f32cc1dc5d47df2f0e40df3bc7790e38c26a2f5dd86ec778f52ee5559a9d299`

Use case: identity-preserve. ONE full-body hand-painted transparent animation sprite of the EXACT armored knight in reference. Preserve precisely the pointed closed steel helm with slit visor, battered silver armor, muted mauve tabard, dark leather straps, round mauve wood shield with metal rim and boss, and the short spear. Same proportions, muted palette, worn brush texture, thin dark ink edges, top-left light, three-quarter camera as original. Facing screen LEFT toward incoming hit; do not redesign. All extremities, shield, spear and boots inside 1024x1024 transparent canvas, substantial margin. No text, labels, background, ground shadow, other character, sparks or VFX. Feet stay planted on a common baseline. Pose must bend joints and react through shoulders/neck/knees, NOT rotate the whole idle image. BLOCKED IMPACT: body tries to recoil screen-right but rear foot is braced against unseen obstruction. Torso arches, shield tight against chest, forward knee bends sharply. More compressed pose than normal flinch.

### raw/knight-a-stagger-01.png
Tool: image_gen; attempt 1/3. References: references/knight-a.png
Raw SHA-256: `b7bc8fd69682eda80f00c74a26d7993726add31bf1b678323bc968b55399bbc2`

Use case: identity-preserve. ONE full-body hand-painted transparent animation sprite of the EXACT armored knight in reference. Preserve precisely the pointed closed steel helm with slit visor, battered silver armor, muted mauve tabard, dark leather straps, round mauve wood shield with metal rim and boss, and the short spear. Same proportions, muted palette, worn brush texture, thin dark ink edges, top-left light, three-quarter camera as original. Facing screen LEFT toward incoming hit; do not redesign. All extremities, shield, spear and boots inside 1024x1024 transparent canvas, substantial margin. No text, labels, background, ground shadow, other character, sparks or VFX. Feet stay planted on a common baseline. Pose must bend joints and react through shoulders/neck/knees, NOT rotate the whole idle image. BUCKLE / STUMBLE IN PLACE: knees buckle low and body folds forward at the hips toward screen-left, helmet chin down, shield dips low, spear angled down-left as balance aid. Both feet remain near starting spots, no full fall. Strong unmistakable stagger silhouette.

### raw/knight-a-stagger-02.png
Tool: image_gen; attempt 1/3. References: references/knight-a.png
Raw SHA-256: `7fa1a592fce21df8a5b08076f666b5e77db0cc29fc02b1521ffc931729cfc2cf`

Use case: identity-preserve. ONE full-body hand-painted transparent animation sprite of the EXACT armored knight in reference. Preserve precisely the pointed closed steel helm with slit visor, battered silver armor, muted mauve tabard, dark leather straps, round mauve wood shield with metal rim and boss, and the short spear. Same proportions, muted palette, worn brush texture, thin dark ink edges, top-left light, three-quarter camera as original. Facing screen LEFT toward incoming hit; do not redesign. All extremities, shield, spear and boots inside 1024x1024 transparent canvas, substantial margin. No text, labels, background, ground shadow, other character, sparks or VFX. Feet stay planted on a common baseline. Pose must bend joints and react through shoulders/neck/knees, NOT rotate the whole idle image. STAGGER RECOVERY: pushing back upright from bent knees, shield arm slightly wide and spear planted at a diagonal to screen-left for balance, head turns back to attacker. Stance still wider and lower than idle.

## Cleanup and runtime frames

Tool: Python 3.12 / Pillow 12.2, `godot-spike/tools/prepare_frames.py`. Per-frame manual registration coordinates are in frame-audit.json. Clear alpha below 24; Lanczos resize to fixed 512px canvas and [256,464] pivot; map generated RGB to 128 colors sampled from its original crop. This removes stray colored edge pixels. Original idles are scaled source crops. Knight B uses manually located shield-field ellipse masks and the same texture-preserving bone-value remap across all seven frames. Armor and shield boss are excluded. No geometric redraw of armor or source originals.

PLACEHOLDER: all six Thoma swing frames have an equipment-reference gap (the specified original crop is empty-handed), and generated hems/sleeves have small deviations. They are functional motion candidates, not exact costume/weapon approval. Knight frames are candidates with head/armor contour variation; same source palette is measurable, exact stroke identity is not proven. No claim of commercial or Owner art acceptance.

| Runtime frame | Status | Input | Output SHA-256 |
| --- | --- | --- | --- |
| thoma/idle/00.png | SOURCE_DERIVED | references/thoma.png | `4214584c64eb57e3d63bdbb9975a2a0d41ee76cd4c6087b61485e795abe23400` |
| knight-a/idle/00.png | SOURCE_DERIVED | references/knight-a.png | `0ca4807cc16f63dba0b3a15bfaaa1d1a534892151db7dfb339e6c5c2b6edf791` |
| thoma/swing/00.png | PLACEHOLDER | raw/thoma-swing-00.png | `d0740fdd74e8b05ca82b1a5c01347cfb87427a696579776e20b528d152062a7c` |
| thoma/swing/01.png | PLACEHOLDER | raw/thoma-swing-01.png | `d918c3338afd97fc1c4661fc6b2bcf3a2d5dc6c70e4c9ae8686da81ff124807e` |
| thoma/swing/02.png | PLACEHOLDER | raw/thoma-swing-02.png | `e12435f7ddb3c2e16476d4499c0f6038444c511c05251aaa0f2e601b9637fe48` |
| thoma/swing/03.png | PLACEHOLDER | raw/thoma-swing-03.png | `78b273af36cfd0ae8078544ff616537b58afeea09e074f79e6096d9c7b32e6d6` |
| thoma/swing/04.png | PLACEHOLDER | raw/thoma-swing-04.png | `ff3347dcdb411e6e11d54c6e8e295ddd4cc86a7c0d4011edf97ce29fea757140` |
| thoma/swing/05.png | PLACEHOLDER | raw/thoma-swing-05.png | `8d264eebae4e67133337d31194b13d036c9a0a1ef4e30a6566e5ef6bec2c8828` |
| knight-a/hit/00.png | CANDIDATE | raw/knight-a-hit-00.png | `6ebef74b6cf9520b5f5a243fb4d9bf669bf78bc6c52f9d6b99ce8202619d2b41` |
| knight-a/hit/01.png | CANDIDATE | raw/knight-a-hit-01.png | `9fbf4a41ffcc16d7c0e75a1f74a182ef33eed4c869f934341cf81e2692b85179` |
| knight-a/hit/02.png | CANDIDATE | raw/knight-a-hit-02.png | `0465fee5877109acb6723c56ebe71134f0d3fcc9ab6e6b9505d7be534f4523bb` |
| knight-a/stagger/00.png | CANDIDATE | raw/knight-a-stagger-00.png | `2cfe6ceb5de5380888937e1ec790102372b4efe5a2f7126a711780915f2948b6` |
| knight-a/stagger/01.png | CANDIDATE | raw/knight-a-stagger-01.png | `b4ec94ff31941285ebd450a706d0565c23745ad2757bcd9229c55797a4b1773b` |
| knight-a/stagger/02.png | CANDIDATE | raw/knight-a-stagger-02.png | `62594f3aaef1f3a70fdae0a1965c7649f8badf0a112afced863cf85b44e24dd6` |
| knight-b/idle/00.png | SOURCE_DERIVED | knight-a/idle/00.png | `a25d3f08eec7fc8fea555b0b1388dd7f9fe5788af4cb97a468fbb1c512192710` |
| knight-b/hit/00.png | SOURCE_DERIVED | knight-a/hit/00.png | `fb744efd3bc1d810b35a487c516f211fefacb886c68d6e2308b41166ddec99cc` |
| knight-b/hit/01.png | SOURCE_DERIVED | knight-a/hit/01.png | `d588a836cec46b2d47bf0cc8d35f66cab05fd49073bca07d53778e2a1b808e29` |
| knight-b/hit/02.png | SOURCE_DERIVED | knight-a/hit/02.png | `221cdfcc637317754223e077eb8f7fab3aa9921cec8bfe17b93ca2ff383ebc0e` |
| knight-b/stagger/00.png | SOURCE_DERIVED | knight-a/stagger/00.png | `e1e189506fc35b8ed51e4b9e4e38c9b4b9c3c75519936a0294cdf348ff674a61` |
| knight-b/stagger/01.png | SOURCE_DERIVED | knight-a/stagger/01.png | `c0c766976ec43f3f82f194348f95bb41f2b6d66d590d4366d542ff4087aa2374` |
| knight-b/stagger/02.png | SOURCE_DERIVED | knight-a/stagger/02.png | `dd1b809d33a596f673b0454910e6ed6d5cd0e8306c83ae8aae0d549ff4154b42` |

Contact sheet: `contact-sheet.png`, SHA-256 `71636c6ee5dbdde5849471146930ec18b1c1f90f9f2ffad6580743e538a9d26e`. Generated by Pillow from every runtime frame plus original crops; red crosses mark pivots. It is an asset review sheet, not a game screenshot.

## spike-02 A2

**Weapon APPROVED (Owner, 2026-10-24):** short one-handed flanged mace, dark iron head, worn oak haft and brass collar. Earlier weapon-pending status is superseded by the Owner decision. It fits a medical friar silhouette, provides blunt impact and is too short to read as a staff. Historical Phase A sword records above are superseded, not runtime provenance for A2. Original PNGs are untouched; original empty-handed idle remains reference-only.

Evidence: character-prompt.txt:1 (empty hands, no staff/book/glow); ART-DIRECTION.md:9 (medical satchel/teal); l03Scene.ts:51–54 (medical/support); DEMO-CONTRACT.md:17 (melee 3, heal 3); narrative branch STORY.md:56 and COMPANION-ARCS.md:28,34 (friar, holy medallion), ch01.ink:306 / ch02.ink:250 and CREATIVE-BIBLE.md:74; DECISIONS U003 (class frame). These are brief-cited source facts, not a new canon claim.

Tool: built-in image_gen; 1 attempt each except swing 02 (2). Rejected 02 attempt 1 is archived under rejected/ because it passes below the waist before chest-high contact. No rejected output is a runtime frame. Full reproducible cleanup: godot-spike/tools/prepare_a2_frames.py. No other character, prop or battlefield generation.

### thoma/idle/01.png attempt 1
Raw: raw/thoma-mace-idle-01.png SHA-256 `54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90"}
Use case: identity-preserve. Edit target: attached original Thoma crop. Create ONE transparent full-body idle sprite of EXACTLY this elderly medical friar, facing screen right in the identical three-quarter stance. Change ONLY his right hand to hold at rest a short ONE-HANDED FLANGED MACE, forearm length, dark iron blunt flanged head, worn oak haft, small brass collar. No blade, sword, staff, book or magic. Preserve identical weathered face, grey short hair/beard, muted teal robe, ivory embroidered stole, satchel with linen rolls, brass medallion, brown boots, proportions, top-left lighting, painted ink edges, textured brushwork and source palette. Mace head beside his right hip, visible silhouette, hand wraps haft naturally. Whole body and mace inside transparent square canvas with generous margins; no floor/shadow/text. Body top approximately y=200, soles y=900 on 1024 square. Do not redesign or add costume. This is weapon idle for a fixed-pivot 512x512 tactics sprite; retain source body proportions.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808

### thoma/swing/00.png attempt 1
Raw: raw/thoma-mace-swing-00.png SHA-256 `3bc1b5ef510e6b24ebd9625becd39c8370293fa23747c082a29e380e3997ff20`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5"}
Use case: identity-preserve. One transparent full-body tactics animation sprite. Reference 1: ORIGINAL Thoma identity, costume, palette and top-left lighting, preserve exactly. Reference 2: new weapon idle, preserve EXACT same short forearm-length one-handed FLANGED MACE, dark iron blunt head, worn oak haft, small brass collar, in anatomical RIGHT hand (near arm on left in idle). No swords, blades, staff, book, magic, new accessories or other characters. Same older grey-haired medical friar, grey beard, teal robe, ivory plant-embroidered stole, linen satchel, medallion, boots, weathered painted ink edges. Face and garment proportions match original; no heroic muscular redesign. Same three-quarter perspective facing SCREEN RIGHT. Real articulated joints, NOT rotation of whole idle. ANTICIPATION: weight clearly shifted to rear foot, knees braced, torso coiled back. Right shoulder and elbow lift the SAME mace cocked HIGH behind his head with head far to screen-left, readable broad negative space between raised arm and face. Left arm counterbalances. Strong wind-up silhouette, no smear. Full figure including mace and boots on transparent square canvas with generous margins; no shadow, text or scenery. Preserve source brush texture and muted palette. Body head-to-ground same length as reference, feet on common baseline.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: 77a0b6857abd1be551fe3b2aec2783f84ab03253df4b09565606c2c5294cc5d4

### thoma/swing/01.png attempt 1
Raw: raw/thoma-mace-swing-01.png SHA-256 `0e138449eaa3634f1af7ee8944b6b2273921d12b58452b7cf7f112d93e8fd8ba`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5"}
Use case: identity-preserve. One transparent full-body tactics animation sprite. Reference 1: ORIGINAL Thoma identity, costume, palette and top-left lighting, preserve exactly. Reference 2: new weapon idle, preserve EXACT same short forearm-length one-handed FLANGED MACE, dark iron blunt head, worn oak haft, small brass collar, in anatomical RIGHT hand (near arm on left in idle). No swords, blades, staff, book, magic, new accessories or other characters. Same older grey-haired medical friar, grey beard, teal robe, ivory plant-embroidered stole, linen satchel, medallion, boots, weathered painted ink edges. Face and garment proportions match original; no heroic muscular redesign. Same three-quarter perspective facing SCREEN RIGHT. Real articulated joints, NOT rotation of whole idle. RAISE / START OF SWING: rotate chest toward screen RIGHT, right upper arm high, elbow starting to open and mace head nearly above forehead at top of downswing. Distinct from the backwards-cocked anticipation. Left hand near chest counterbalances. No smear. Full figure including mace and boots on transparent square canvas with generous margins; no shadow, text or scenery. Preserve source brush texture and muted palette. Body head-to-ground same length as reference, feet on common baseline.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: 1388d405ee128a78f6103d4fc233ff6692b86fe391d53a588f6ba1a307473985

### thoma/swing/02.png attempt 1
Raw: rejected/thoma-mace-swing-02-attempt1.png SHA-256 `6cfdb628aac040081ecca0544a9faae3946731510c6f4669951a9a3e87055c7c`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5"}
Use case: identity-preserve. One transparent full-body tactics animation sprite. Reference 1: ORIGINAL Thoma identity, costume, palette and top-left lighting, preserve exactly. Reference 2: new weapon idle, preserve EXACT same short forearm-length one-handed FLANGED MACE, dark iron blunt head, worn oak haft, small brass collar, in anatomical RIGHT hand (near arm on left in idle). No swords, blades, staff, book, magic, new accessories or other characters. Same older grey-haired medical friar, grey beard, teal robe, ivory plant-embroidered stole, linen satchel, medallion, boots, weathered painted ink edges. Face and garment proportions match original; no heroic muscular redesign. Same three-quarter perspective facing SCREEN RIGHT. Real articulated joints, NOT rotation of whole idle. SWING: weight advances toward screen RIGHT, torso twists, right elbow extends, short mace sweeping DOWN toward right. Add a SHORT muted iron-grey hand-painted translucent smear ONLY behind the mace head along its descending arc; broken dry-brush stroke, not a vector streak, no glow. Keep actual single mace head and hand readable. Full figure including mace and boots on transparent square canvas with generous margins; no shadow, text or scenery. Preserve source brush texture and muted palette. Body head-to-ground same length as reference, feet on common baseline.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: REJECTED (no runtime output)

### thoma/swing/03.png attempt 1
Raw: raw/thoma-mace-swing-03.png SHA-256 `aca010f6472a7aff8b164ee9ea0ae92e12f2f62b44eb19d286b1ba5ca5380ea8`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5"}
Use case: identity-preserve. One transparent full-body tactics animation sprite. Reference 1 ORIGINAL Thoma defines exact identity, costume, muted palette and top-left lighting. Reference 2 weapon idle defines EXACT short forearm-length one-handed FLANGED MACE: blunt dark iron head, worn oak haft, small brass collar, anatomical RIGHT hand. Preserve weathered elderly face, short grey hair/beard, teal robe, ivory plant-embroidered stole, linen satchel, medallion, boots, body proportions and dark painterly ink edges. No sword, blade, staff, book, glow, new costume, accessory, scenery, shadow, text or second character. Same three-quarter perspective facing screen RIGHT. Truly articulate joints, no whole-sprite rotation. CONTACT: weight FULLY FORWARD on front boot toward SCREEN RIGHT, right shoulder driving forward, anatomical right arm straight across chest EXTENDED HORIZONTALLY toward right at chest height. Grip the SAME short mace, haft horizontal to RIGHT, iron head furthest RIGHT at chest height near x=1120, y=470. Arm and weapon together form a clear horizontal line into unseen target. Left hand counterbalances near ribs. Torso forward lean, planted wide stance. No smear or effects; this frame is held at impact. Whole figure and all weapon visible on transparent square canvas, generous margins. Match the source's subdued brush texture and lighting.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: f0d75409967bd662469f80ad524d58e74f1eb87a3eb252ef01891a7b616d340c

### thoma/swing/04.png attempt 1
Raw: raw/thoma-mace-swing-04.png SHA-256 `eacc1d40c1b6e70d14d265ec57b81a9bcfcc44406f19afa1e84e44029a89a7bf`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5"}
Use case: identity-preserve. One transparent full-body tactics animation sprite. Reference 1 ORIGINAL Thoma defines exact identity, costume, muted palette and top-left lighting. Reference 2 weapon idle defines EXACT short forearm-length one-handed FLANGED MACE: blunt dark iron head, worn oak haft, small brass collar, anatomical RIGHT hand. Preserve weathered elderly face, short grey hair/beard, teal robe, ivory plant-embroidered stole, linen satchel, medallion, boots, body proportions and dark painterly ink edges. No sword, blade, staff, book, glow, new costume, accessory, scenery, shadow, text or second character. Same three-quarter perspective facing screen RIGHT. Truly articulate joints, no whole-sprite rotation. FOLLOW THROUGH: weight remains forward to screen RIGHT, right arm extended then elbow beginning to bend as short mace drops below right knee toward screen right, finishing the downward blow. Head follows weapon, cloth trails behind. Distinct low weapon silhouette from chest-high contact. No smear, no glow. Whole figure and all weapon visible on transparent square canvas, generous margins. Match the source's subdued brush texture and lighting.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: 2f51e1b2dbffb759874efd43af283e90d2d4116276e52056e8bc51745aea3d7c

### thoma/swing/05.png attempt 1
Raw: raw/thoma-mace-swing-05.png SHA-256 `e89296c8cd0a799e8d5302caf1f611aaa241e84f2a2c4ff56f8b77f4153f31dd`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5"}
Use case: identity-preserve. One transparent full-body tactics animation sprite. Reference 1 ORIGINAL Thoma defines exact identity, costume, muted palette and top-left lighting. Reference 2 weapon idle defines EXACT short forearm-length one-handed FLANGED MACE: blunt dark iron head, worn oak haft, small brass collar, anatomical RIGHT hand. Preserve weathered elderly face, short grey hair/beard, teal robe, ivory plant-embroidered stole, linen satchel, medallion, boots, body proportions and dark painterly ink edges. No sword, blade, staff, book, glow, new costume, accessory, scenery, shadow, text or second character. Same three-quarter perspective facing screen RIGHT. Truly articulate joints, no whole-sprite rotation. RECOVER: same stance almost as reference 2 idle, torso upright facing right, right arm lowers the same short mace beside hip, elbow slightly flexed, weight returning balanced on both boots, left hand relaxed. Recover smoothly into reference 2 idle, no smear. Whole figure and all weapon visible on transparent square canvas, generous margins. Match the source's subdued brush texture and lighting.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf

### thoma/swing/02.png attempt 2
Raw: raw/thoma-mace-swing-02-attempt2.png SHA-256 `274edae4742a67aedd787cb20e6e8b6ff12dce900a2797ac11d22300608b0551`
References: {"references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "raw/thoma-mace-idle-01.png": "54196207e94c527120a44642e0ad68c79f9424e93d52e378d8268faf45a37db5", "raw/thoma-mace-swing-03.png": "aca010f6472a7aff8b164ee9ea0ae92e12f2f62b44eb19d286b1ba5ca5380ea8"}
Use case: identity-preserve. Create ONE corrected SWING frame of Thoma for transparent tactics sprite animation. Ref1 original Thoma identity/costume/palette; ref2 weapon idle defines SAME short flanged iron mace, oak haft, brass collar; ref3 is CONTACT which this frame must PRECEDE. IMPORTANT swing weapon head is ABOVE contact, at UPPER RIGHT of face (around x=1030 y=240), NOT below waist. Right shoulder drives forward, right elbow partly straight, hand around x=830 y=400, short mace angled 40 degrees UP-RIGHT toward head at x=1030 y=240, descending next into ref3 horizontal contact. Weight transitioning forward; torso not yet as leaned as ref3. Add short subtle dry-brush iron grey smear ABOVE/BEHIND mace head from overhead to upper-right; not below it. Preserve EXACT elderly face grey hair/beard, teal robe, ivory embroidered stole, linen satchel, brass medallion, boots, original proportions, muted palette, top-left lighting and painted ink texture. Anatomical right hand holds mace. No blades/sword/staff/book/magic/glow, scenery, shadow or text. Full figure and weapon entirely visible with margins on transparent square canvas.
Cleanup: alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering
Runtime SHA-256: f13cb9690130b2b5ba3a49f2af5f16808122102e83b5bc4845809ef1e53fe96c

| Frame | Style verdict | SHA-256 |
| --- | --- | --- |
| thoma/idle/01.png | PASS: Identity and near-idle silhouette retained at review scale; not Owner art approval. | `c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808` |
| thoma/swing/00.png | PLACEHOLDER: Stole embroidery, cuff folds and hem contour drift from original; motion candidate only. | `77a0b6857abd1be551fe3b2aec2783f84ab03253df4b09565606c2c5294cc5d4` |
| thoma/swing/01.png | PLACEHOLDER: Stole embroidery, cuff folds and hem contour drift from original; motion candidate only. | `1388d405ee128a78f6103d4fc233ff6692b86fe391d53a588f6ba1a307473985` |
| thoma/swing/03.png | PLACEHOLDER: Stole embroidery, cuff folds and hem contour drift from original; motion candidate only. | `f0d75409967bd662469f80ad524d58e74f1eb87a3eb252ef01891a7b616d340c` |
| thoma/swing/04.png | PLACEHOLDER: Stole embroidery, cuff folds and hem contour drift from original; motion candidate only. | `2f51e1b2dbffb759874efd43af283e90d2d4116276e52056e8bc51745aea3d7c` |
| thoma/swing/05.png | PASS: Identity and near-idle silhouette retained at review scale; not Owner art approval. | `f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf` |
| thoma/swing/02.png | PLACEHOLDER: Stole embroidery, cuff folds and hem contour drift from original; motion candidate only. | `f13cb9690130b2b5ba3a49f2af5f16808122102e83b5bc4845809ef1e53fe96c` |

Weapon identity is APPROVED (Owner, 2026-10-24); style PASS is a separate model judgement. Detailed frame review: frame-audit.json. Style sheet SHA-256 `d41b38e02fea3ddda07be31cdb2a82fa201a581bf686cede8913c622018c80ad`. Contact sheet SHA-256 `31f921ca4801a6bc3f1e26587e1ef8fc4167003e6f3f5b616f647938de2e74bd`.

## A2 knight B

Scripted edit preferred by the brief, one pass per frame, no image generation. Reproducible script: godot-spike/tools/prepare_a2_knight.py. Identical short bone horsehair crest and light shield field across idle/hit/stagger. Original atlases and knight A unchanged. Detailed anchors, input/output SHA-256 and exact edit instruction: knight-a2-edits.json. Model inspection is not Owner art approval.

| Frame | Input SHA-256 | Output SHA-256 |
| --- | --- | --- |
| knight-b/idle/00.png | `0ca4807cc16f63dba0b3a15bfaaa1d1a534892151db7dfb339e6c5c2b6edf791` | `e71644dfef36fcb0cc1babd3db63ab9791ade1d1fbd7445601b77f51612e97b5` |
| knight-b/hit/00.png | `6ebef74b6cf9520b5f5a243fb4d9bf669bf78bc6c52f9d6b99ce8202619d2b41` | `cc853f78528c4c8391d70606eb4e4da39565ea5d73e568664620ba06c39ab5bd` |
| knight-b/hit/01.png | `9fbf4a41ffcc16d7c0e75a1f74a182ef33eed4c869f934341cf81e2692b85179` | `2b54bc88debb009b1a15164a6c40e07f1438eb5be33cb7bb0b0c632e85a7ae9e` |
| knight-b/hit/02.png | `0465fee5877109acb6723c56ebe71134f0d3fcc9ab6e6b9505d7be534f4523bb` | `e14b7ba82c075fef7a4f94d14c0309fec15316c73eddd0c3437e0d39b8e4a7cd` |
| knight-b/stagger/00.png | `2cfe6ceb5de5380888937e1ec790102372b4efe5a2f7126a711780915f2948b6` | `e5164c1a931d13ffdfcabffb345a2c2ff57f6f6f87e115aae3bc19c1fc7538e6` |
| knight-b/stagger/01.png | `b4ec94ff31941285ebd450a706d0565c23745ad2757bcd9229c55797a4b1773b` | `aaea5183f82ec03d531770331835530bfb841d3909bcf88875d2f2301d8a49cf` |
| knight-b/stagger/02.png | `62594f3aaef1f3a70fdae0a1965c7649f8badf0a112afced863cf85b44e24dd6` | `4c2dc1cad19b6a6f11a6727d689e53ea124d0644e698925311db4fdb6290e138` |

## spike-02 A3

Weapon APPROVED (Owner, 2026-10-24). Five image_gen attempts total, one per swing 00-04. Raw originals retained unchanged. Only garment patches are accepted; generated full-figure geometry is not adopted. No rejected attempt was discarded. No other character or environment generated.
Reproduction: `godot-spike/tools/prepare_a3_frames.py`. A2 byte-copy baseline and hashes: `godot-spike/docs/evidence/spike02-a3/baseline-a2/`. No baseline path is in the manifest. Exact original embroidery is composited rather than invented. Canvas/pivot, mace/head/grip/contact geometry, source silhouette and timing stay fixed. Remaining contour/style drift is assessed separately in W3.

### thoma/swing/00.png attempt 1
Tool: image_gen (built-in).
Use case: identity-preserve / precise-object-edit. Repaint ONLY the garment details of image 4, Thoma anticipation swing frame 00. Image 1 original Thoma is costume ground truth. Images 2 (weapon idle) and 3 (recover) define passing costume, face, stroke, palette and approved weapon. Image 4 is the exact pose and registration to KEEP. Output one transparent 512x512 sprite, same framing, same foot pivot [256,464]. Preserve image 4's every joint, boots, face, hands, mace silhouette/length/head size/grip and all positions, keep weapon cocked high behind head and coiled torso. Change only stole/cape ivory band embroidery to sparse small sage leafy sprigs at lower ends as image 1, correct linen cuff folds and layered teal robe over ivory underskirt hem to match image 1/2/3, preserve brown medical satchel, round brass medallion holy symbol, grey beard. Match muted teal/ivory/brown, top-left light and weathered fine painted contours; no new trim or ornamental border, no new geometry. Do not enlarge body or auto-crop. No text, background, shadow, glow, blade, staff, book or other person. Genuine transparent alpha, generous unchanged canvas. This is a surgical costume repaint, exact A2 pose and mace must remain.
References and SHA-256: {"shared-anim/references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "shared-anim/thoma/idle/01.png": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808", "shared-anim/thoma/swing/05.png": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf", "godot-spike/docs/evidence/spike02-a3/baseline-a2/00.png": "77a0b6857abd1be551fe3b2aec2783f84ab03253df4b09565606c2c5294cc5d4"}
Raw: `raw/thoma-a3-swing-00-attempt1.png` SHA-256 `e0f0159ed683807366afe3350b3944a147e6565e5b576b39a8dd9f0e6efd00e0` ([1254, 1254]); full generated figure is not a runtime asset.
Cleanup: Perspective-warp interior cuff/hem patches; transplant original sprig; feather 0.65px; discard alpha <=240 at patch edges; quantize edited pixels to original 128-color palette; preserve entire A2 alpha and all unmasked pixels.
Runtime SHA-256: `8026a8871b1b72fc7e9846d564a1e689d8dbecb6605bebccd9911baa9ef43c17`.

### thoma/swing/01.png attempt 1
Tool: image_gen (built-in).
Use case: identity-preserve / precise-object-edit. Repaint ONLY the garment details of image 4, Thoma raise/start swing frame 01. Image 1 original Thoma is costume ground truth. Images 2 (weapon idle) and 3 (recover) define passing costume, face, stroke, palette and approved weapon. Image 4 is the exact pose and registration to KEEP. Output one transparent 512x512 sprite, same framing, same foot pivot [256,464]. Preserve image 4's every joint, boots, face, hands, mace silhouette/length/head size/grip and all positions, keep raised weapon nearly above forehead, chest rotating right, left hand near chest, exact A2 pose. Change only stole/cape ivory band embroidery to sparse small sage leafy sprigs at lower ends as image 1, correct linen cuff folds and layered teal robe over ivory underskirt hem to match image 1/2/3, preserve brown medical satchel, round brass medallion holy symbol, grey beard. Match muted teal/ivory/brown, top-left light and weathered fine painted contours; no new trim or ornamental border, no new geometry. Do not enlarge body or auto-crop. No text, background, shadow, glow, blade, staff, book or other person. Genuine transparent alpha, generous unchanged canvas. This is a surgical costume repaint, exact A2 pose and mace must remain.
References and SHA-256: {"shared-anim/references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "shared-anim/thoma/idle/01.png": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808", "shared-anim/thoma/swing/05.png": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf", "godot-spike/docs/evidence/spike02-a3/baseline-a2/01.png": "1388d405ee128a78f6103d4fc233ff6692b86fe391d53a588f6ba1a307473985"}
Raw: `raw/thoma-a3-swing-01-attempt1.png` SHA-256 `804668a246aeb3330726d7dca2f9f270d393cd70a30496efb49dc12a48ce51ca` ([1254, 1254]); full generated figure is not a runtime asset.
Cleanup: Perspective-warp interior cuff/hem patches; transplant original sprig; feather 0.65px; discard alpha <=240 at patch edges; quantize edited pixels to original 128-color palette; preserve entire A2 alpha and all unmasked pixels.
Runtime SHA-256: `3722d0272e821c323ef913fd4cabe2a56a140b279fe07878c8db716c013d0acd`.

### thoma/swing/02.png attempt 1
Tool: image_gen (built-in).
Use case: identity-preserve / precise-object-edit. Repaint ONLY the garment details of image 4, Thoma descending swing frame 02. Image 1 original Thoma is costume ground truth. Images 2 (weapon idle) and 3 (recover) define passing costume, face, stroke, palette and approved weapon. Image 4 is the exact pose and registration to KEEP. Output one transparent 512x512 sprite, same framing, same foot pivot [256,464]. Preserve image 4's every joint, boots, face, hands, mace silhouette/length/head size/grip and all positions, keep mace diagonally up-right, its short hand-painted iron-grey smear behind/above head, exact A2 articulated swing pose. Change only stole/cape ivory band embroidery to sparse small sage leafy sprigs at lower ends as image 1, correct linen cuff folds and layered teal robe over ivory underskirt hem to match image 1/2/3, preserve brown medical satchel, round brass medallion holy symbol, grey beard. Match muted teal/ivory/brown, top-left light and weathered fine painted contours; no new trim or ornamental border, no new geometry. Do not enlarge body or auto-crop. No text, background, shadow, glow, blade, staff, book or other person. Genuine transparent alpha, generous unchanged canvas. This is a surgical costume repaint, exact A2 pose and mace must remain.
References and SHA-256: {"shared-anim/references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "shared-anim/thoma/idle/01.png": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808", "shared-anim/thoma/swing/05.png": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf", "godot-spike/docs/evidence/spike02-a3/baseline-a2/02.png": "f13cb9690130b2b5ba3a49f2af5f16808122102e83b5bc4845809ef1e53fe96c"}
Raw: `raw/thoma-a3-swing-02-attempt1.png` SHA-256 `ba4fa98a9585520c21c9ab64dedd592578b7cd6bab75d2a700f5d64a52628525` ([1254, 1254]); full generated figure is not a runtime asset.
Cleanup: Perspective-warp interior cuff/hem patches; transplant original sprig; feather 0.65px; discard alpha <=240 at patch edges; quantize edited pixels to original 128-color palette; preserve entire A2 alpha and all unmasked pixels.
Runtime SHA-256: `f38de24651841d855a4d14040838b9a33bd2050f7bffe4f5eb1ffdd206a9b7a2`.

### thoma/swing/03.png attempt 1
Tool: image_gen (built-in).
Use case: identity-preserve / precise-object-edit. Repaint ONLY the garment details of image 4, Thoma contact swing frame 03. Image 1 original Thoma is costume ground truth. Images 2 (weapon idle) and 3 (recover) define passing costume, face, stroke, palette and approved weapon. Image 4 is the exact pose and registration to KEEP. Output one transparent 512x512 sprite, same framing, same foot pivot [256,464]. Preserve image 4's every joint, boots, face, hands, mace silhouette/length/head size/grip and all positions, keep extended right arm and horizontal mace at chest height, mace head center exactly [455,196] on the 512x512 canvas, forward planted weight, exact A2 contact pose. Change only stole/cape ivory band embroidery to sparse small sage leafy sprigs at lower ends as image 1, correct linen cuff folds and layered teal robe over ivory underskirt hem to match image 1/2/3, preserve brown medical satchel, round brass medallion holy symbol, grey beard. Match muted teal/ivory/brown, top-left light and weathered fine painted contours; no new trim or ornamental border, no new geometry. Do not enlarge body or auto-crop. No text, background, shadow, glow, blade, staff, book or other person. Genuine transparent alpha, generous unchanged canvas. This is a surgical costume repaint, exact A2 pose and mace must remain.
References and SHA-256: {"shared-anim/references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "shared-anim/thoma/idle/01.png": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808", "shared-anim/thoma/swing/05.png": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf", "godot-spike/docs/evidence/spike02-a3/baseline-a2/03.png": "f0d75409967bd662469f80ad524d58e74f1eb87a3eb252ef01891a7b616d340c"}
Raw: `raw/thoma-a3-swing-03-attempt1.png` SHA-256 `beb43bf73db79d2c91103c0550dc9ca92421f8bc0fa7fc255b8d31209aa883b6` ([1254, 1254]); full generated figure is not a runtime asset.
Cleanup: Perspective-warp interior cuff/hem patches; transplant original sprig; feather 0.65px; discard alpha <=240 at patch edges; quantize edited pixels to original 128-color palette; preserve entire A2 alpha and all unmasked pixels.
Runtime SHA-256: `32034e392720ad04f2294ddc74f02b142050761a4adbed01bc7aa2d11de0b10a`.

### thoma/swing/04.png attempt 1
Tool: image_gen (built-in).
Use case: identity-preserve / precise-object-edit. Repaint ONLY the garment details of image 4, Thoma follow-through swing frame 04. Image 1 original Thoma is costume ground truth. Images 2 (weapon idle) and 3 (recover) define passing costume, face, stroke, palette and approved weapon. Image 4 is the exact pose and registration to KEEP. Output one transparent 512x512 sprite, same framing, same foot pivot [256,464]. Preserve image 4's every joint, boots, face, hands, mace silhouette/length/head size/grip and all positions, keep right hand lowering mace down-right below knee, torso forward, cloth trailing back-left, exact A2 follow-through pose. Change only stole/cape ivory band embroidery to sparse small sage leafy sprigs at lower ends as image 1, correct linen cuff folds and layered teal robe over ivory underskirt hem to match image 1/2/3, preserve brown medical satchel, round brass medallion holy symbol, grey beard. Match muted teal/ivory/brown, top-left light and weathered fine painted contours; no new trim or ornamental border, no new geometry. Do not enlarge body or auto-crop. No text, background, shadow, glow, blade, staff, book or other person. Genuine transparent alpha, generous unchanged canvas. This is a surgical costume repaint, exact A2 pose and mace must remain.
References and SHA-256: {"shared-anim/references/thoma.png": "ae5897b5037e60d99c057ce389b767ef4ecff766e531df1a44c55478cd28af90", "shared-anim/thoma/idle/01.png": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808", "shared-anim/thoma/swing/05.png": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf", "godot-spike/docs/evidence/spike02-a3/baseline-a2/04.png": "2f51e1b2dbffb759874efd43af283e90d2d4116276e52056e8bc51745aea3d7c"}
Raw: `raw/thoma-a3-swing-04-attempt1.png` SHA-256 `5ebcce2dd61852d41056f79f86a625add621994cd5fff3a56a4526b1b6115738` ([1254, 1254]); full generated figure is not a runtime asset.
Cleanup: Perspective-warp interior cuff/hem patches; transplant original sprig; feather 0.65px; discard alpha <=240 at patch edges; quantize edited pixels to original 128-color palette; preserve entire A2 alpha and all unmasked pixels.
Runtime SHA-256: `b2d64c00944131073dccde2c7399a3d638abd83d3101431d6f9d3bfbf23274ce`.

### A3 W3 style verdict

Model inspection, not Owner/commercial approval. All five repaints remain PLACEHOLDER: exact source sprigs improve costume continuity but composite seams/cuffs and A2 hem contours still fail the detailed criterion. One generation attempt per frame; further whole-frame regeneration was not adopted because it moved protected geometry. Idle/recover remain unchanged PASS.

| Frame | Status | Reason |
| --- | --- | --- |
| thoma/idle/01.png | PASS | Recognizable original face, paired ivory leafy stole, layered cuffs/hem and equipment continuity at review and runtime scale; not Owner art approval. |
| thoma/swing/00.png | PLACEHOLDER | Leaf sprigs now come from the original, but doubled border/leaf density remains at patch edges; raised cuff transition and broad fan hem still differ from idle/recover. |
| thoma/swing/01.png | PLACEHOLDER | Original sprigs improve identity, but stole border blending and raised cuff folds still differ; the bell-shaped hem is retained from A2. |
| thoma/swing/03.png | PLACEHOLDER | Contact geometry is byte-preserved; stole seam/leaf density and broad underskirt hem remain inconsistent at detail scale. |
| thoma/swing/04.png | PLACEHOLDER | Trailing sprigs reuse original pixels, but stretched diagonal embroidery, front cuff transition and trailing hem remain visibly different. |
| thoma/swing/05.png | PASS | Recognizable original face, paired ivory leafy stole, layered cuffs/hem and equipment continuity at review and runtime scale; not Owner art approval. |
| thoma/swing/02.png | PLACEHOLDER | Original sprigs and cuff cloth improve continuity, but compressed leaf detail, cuff patch boundary and swept underskirt contour still drift. |

Style sheet SHA-256 `04926a2dd63e6d63c36b797d22cc9d13bd539061aceccd03ea605f4ed40fcbbe`.

## spike-02 A4 — reference pixel transfer

Tool: offline Pillow cutout rig, godot-spike/tools/prepare_a4_frames.py.
No image generation requests, prompts, raw outputs or rejected generation attempts in A4 (0/3 per frame). No external assets introduced. Full controls, source masks and region library: godot-spike/docs/evidence/spike02-a4/reference-regions/. A3 live frames were archived as byte copies in baseline-a3 before replacement. Original/reference PNGs are unchanged.

Costume comes from idle/01 and swing/05 with continuous-body affine transfer, reference cuff quadrilaterals and translated reference face/hair. Existing A3 motion arms/torso twist, feet and mace are retained; small reference-mace occlusion patches clone plain reference cloth/bag. Old fan hem alpha is removed. This changes method; it does not by itself establish art acceptance. W3 per-region and sequence verdicts control PLACEHOLDER.

Full per-frame input hashes, output hashes, controls, zero-attempt provenance, cleanup and before/after palette distances are in a4-swing-prompts.json. Historical A3 runtime hashes refer to the preserved baseline-a3 frames, not the A4 live files.

| Frame | A4 runtime SHA-256 | Palette distance before / after |
| --- | --- | --- |
| thoma/swing/00.png | 93d1f3bb044d06c459236b79af4b4c09d16bf8bf7f67aaa1cc7d6ea2bd523853 | 0.0 / 2.154391 |
| thoma/swing/01.png | c4951e886bdaf6f49a72531e27c0db37254aabda071f4304d951c45d85c496cf | 0.0 / 2.239122 |
| thoma/swing/02.png | 7ac71805794546f0bb85ba38257fa76c4aa802f6b15531792e491e5a19d2973d | 0.0 / 2.244537 |
| thoma/swing/03.png | 04795f7b3a137c171033f1bae1578ee47e6700ffad3f8fd573bd9895175eb1cf | 0.0 / 2.272082 |
| thoma/swing/04.png | e2d809bd1b7ab0d371a125532260b092d0372635af6cbd31e2cb695ed4df3f18 | 0.0 / 2.211167 |

### A4 W3 model verdict

Five motion frames remain PLACEHOLDER. Reference transfer fixes provenance and replaces the old contour, but shoulder/cuff/bag seams and hem-to-feet continuity fail. See frame-audit.json region_review and spike02-a4/sequence-check.json. Two immutable references retain PASS. No human or Owner art approval is claimed.

## spike-02 A5 — deterministic seam and foot repair

Tool: offline Pillow 12.2.0, godot-spike/tools/prepare_a5_frames.py. Uses the
unmodified A4 reference cutout helpers/pose controls. Zero AI calls (0/3 per
frame), prompt/raw=null, no rejected AI output. Full source, reference, mask
and runtime SHA-256 records: a5-swing-prompts.json. No original PNGs moved or
edited. Both immutable references match A4 hashes. A4 frames archived as byte
copies in godot-spike/docs/evidence/spike02-a5/baseline-a4/ with hashes.json.

One continuous recover body replaces A4 bag-bearing clone patches. Two plain
cloth source/target quads remove the reference mace occlusion; no bag pixels
or motifs are cloned. Final mask-limited 0.75px smoothing, upper silhouette
retention, unit embroidery scale and below-motif hem mesh are reproducible.
Mace, grip, head/face and feet are protected raw A4 bytes. Palette is unmapped.
Coordinates/width/area/hashes: seam-masks/coordinates.json and rig-controls.json
under the A5 evidence folder. The first W2 inspection found a surviving
reference mace-head fragment; W3 corrected its occlusion support and protected
face pixels. W1 proof remains the original draft, not silently regenerated.

| Frame | Runtime SHA-256 | Mask SHA-256 | Palette distance A4 / A5 |
| --- | --- | --- | --- |
| thoma/swing/00.png | 578b460defc4c53ba632002e405d40e2b6d40282a85da7db192e0b75be7d9663 | e169aecfa50fe7359bde2e87225a5a071157ef6864f8313d74f2076d55067654 | 2.154391 / 2.292463 |
| thoma/swing/01.png | b06121b366fe9c126d8bcf40c3ffbff974446282d0f22a844776347ad3a14243 | 5193766e897af5ae2be8c3768e1a3eafe84f1f89c11c558ec1b0f6019e5318d1 | 2.239122 / 2.400236 |
| thoma/swing/02.png | 91a68c71be081b72fef49a0c90ec010f1fe6a456b64b9ecda1940ae4a0867818 | e7ce806c8e54d41b7df191b1a947416e2f3dfb93f3605e5cc9503286d0a1d7eb | 2.244537 / 2.318793 |
| thoma/swing/03.png | f4b590dc492705067948bc9c31fcfdbdfa01a5b424f75cda5a0e6d28cf319d88 | 9ecf1c2e2b4f2c27c4afab90f324b336fc196f6c0d14f7c14b9ee7c8a760950a | 2.272082 / 2.344525 |
| thoma/swing/04.png | cccce1128daf423eb337a88d8dae5fe507524b448ca140d5c57bc488841c96e9 | a87ddcc2184e31f0d2e3c8981690d91d5551bac5f3cdc3659134041faf5f01c2 | 2.211167 / 2.286251 |

### A5 model verdict

Single-bag count and unit local motif scale pass. Shoulder/waist/cuff folds,
plain-cloth repair boundary and hem-to-boot/sequence continuity still fail.
All five motion frames remain PLACEHOLDER; two unchanged reference endpoints
retain PASS. Per-check reasons in frame-audit.json, same-scale crops in A5
region-check.png and six pair proxies in sequence-check.json. No Owner or
commercial art approval. Human hit-feel remains HUMAN_PENDING.

## spike-02 A6 — complete per-frame regeneration

Built-in image_gen. Exactly idle/01 + swing/05 for identity/costume/style/mace; A5 same-index ONLY for pose. No rig/region compositing. Seed/model/quality: not exposed. Transparent background requested. Maximum 4 attempts per frame. Every unchanged raw candidate retained under godot-spike/docs/evidence/spike02-a6/candidates/. Full normalization transforms, cleanup masks, palette distances and hashes in a6-swing-prompts.json. Uniform scale/translate, alpha<24 cleanup, idle/01 nearest-128-colour remap only. See A6 METHOD.md for gate and limits. Human playtest HUMAN_PENDING; model checks are not Owner art approval.

### thoma/swing/02.png attempt 1

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1280, 1280]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "shared-anim/thoma/swing/02.png", "role": "A5 pose/silhouette ONLY", "sha256": "91a68c71be081b72fef49a0c90ec010f1fe6a456b64b9ecda1940ae4a0867818"}]

Use case: stylized-concept. Asset: ONE complete newly painted full-body 2D animation sprite, frame swing/02, real transparent background, square 512x512 canvas (if higher resolution output, preserve these normalized coordinates). Reference image 1 idle/01 and reference image 2 swing/05 are the ONLY authorities for ALL costume detail, face, grey hair/beard, muted teal/ivory/brown palette, brush/ink style, exact short one-handed flanged mace (dark iron flanges, worn oak haft, small brass collar). Reference image 3 A5 swing/02 defines POSE AND SILHOUETTE ONLY: never copy its broken cloth fragments, gaps, costume patches or detached shoes. Regenerate the ENTIRE man coherently in a single painting, no cutout parts or collage. Same elderly weathered man in three-quarter view facing right. Head near x296 y145, head-to-ground height about 350 pixels, planted ground y464, stance centered on foot pivot [256,464], left boot x128 y444 and right boot x370 y430. Braced mid-swing torso; right arm extends diagonally up/right, hand around [371,166], short mace head around [443,111], SAME mace proportions as references 1/2, not a long pole weapon. Left arm counterbalances with one naturally attached hand. Coherent shoulder and sleeves, ivory wide inner cuffs; unbroken teal robe over ivory underskirt, continuous scalloped hem, both legs visibly connect to brown boots. Exactly ONE brown satchel at left hip with single rolled cloth, one belt and round bronze pendant. Two continuous ivory stole bands, simple small botanical embroidery only at their lower ends, same motif scale as references 1/2; no embroidery added to robe/hem. Do not add accessories, magic, scenery, props, other figures, labels, shadow, platform or background. Full head, both feet and mace entirely inside canvas. Match worn painterly fine ink edges, subdued top-left light and precise costume detail of references 1/2. A restrained short grey-teal motion smear behind mace only. Avoid triangular hem scraps, floating sleeve pieces, disconnected limbs, cloned bag, redesigned face, chibi proportions, bright grading.

Raw: godot-spike/docs/evidence/spike02-a6/candidates/02/attempt-1.png SHA-256 `4d462f01ef8327c8a309613dfc4e92fd7681742eeed35f5d4793ea0715376942`

Runtime SHA-256: `None` (null = not adopted). Pick=True, adopted=False. Best W1 proof: continuous sleeve/hem, both boots attached, consistent two-band stole and one satchel; retains recognizable botanical costume. Remaining motif/texture drift is a W3 failure, not waived.

Normalization and cleanup: {"raw_sha256": "4d462f01ef8327c8a309613dfc4e92fd7681742eeed35f5d4793ea0715376942", "normalized_sha256": "0f76a0f68e6ea294146accdba635fa999a5fb6db532bc2b957461dd2e2050624", "settings": {"scale": 0.37155, "translate": [25.0, 35.2], "palette_remap": true}, "palette_distance": {"before": 6.622218, "after": 0.576556, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/02-attempt-1-cleanup-mask.png", "cleanup_mask_sha256": "ba5802b9c17d40dc8b6cff279d789ffd69cd9fe9528bcb5430bdb23cd9ffc7b5", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}

### thoma/swing/02.png attempt 2

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1280, 1280]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "shared-anim/thoma/swing/02.png", "role": "A5 pose/silhouette ONLY", "sha256": "91a68c71be081b72fef49a0c90ec010f1fe6a456b64b9ecda1940ae4a0867818"}]

Use case: stylized-concept. Asset: ONE complete newly painted full-body 2D animation sprite, frame swing/02, real transparent background, square 512x512 canvas (if higher resolution output, preserve these normalized coordinates). Reference image 1 idle/01 and reference image 2 swing/05 are the ONLY authorities for ALL costume detail, face, grey hair/beard, muted teal/ivory/brown palette, brush/ink style, exact short one-handed flanged mace (dark iron flanges, worn oak haft, small brass collar). Reference image 3 A5 swing/02 defines POSE AND SILHOUETTE ONLY: never copy its broken cloth fragments, gaps, costume patches or detached shoes. Regenerate the ENTIRE man coherently in a single painting, no cutout parts or collage. Same elderly weathered man in three-quarter view facing right. Head near x296 y145, head-to-ground height about 350 pixels, planted ground y464, stance centered on foot pivot [256,464], left boot x128 y444 and right boot x370 y430. Braced mid-swing torso; right arm extends diagonally up/right, hand around [371,166], short mace head around [443,111], SAME mace proportions as references 1/2, not a long pole weapon. Left arm counterbalances with one naturally attached hand. Coherent shoulder and sleeves, ivory wide inner cuffs; unbroken teal robe over ivory underskirt, continuous scalloped hem, both legs visibly connect to brown boots. Exactly ONE brown satchel at left hip with single rolled cloth, one belt and round bronze pendant. Two continuous ivory stole bands, simple small botanical embroidery only at their lower ends, same motif scale as references 1/2; no embroidery added to robe/hem. Do not add accessories, magic, scenery, props, other figures, labels, shadow, platform or background. Full head, both feet and mace entirely inside canvas. Match worn painterly fine ink edges, subdued top-left light and precise costume detail of references 1/2. A restrained short grey-teal motion smear behind mace only. Avoid triangular hem scraps, floating sleeve pieces, disconnected limbs, cloned bag, redesigned face, chibi proportions, bright grading.
Correction for this independent attempt: match the SMALL, understated botanical sprigs of references 1/2 exactly; preserve their ivory stole's short fringe and restrained dark-grey embroidered leaves, not a large decorative plant. Avoid excessive crisp texture, saturated teal, reddish trim or a youthful face; the reference has a slender weathered elderly face and soft fine brushwork. Keep the swing silhouette but render costume with the exact unornamented worn surfaces of reference 1. No bright orange embroidery borders. One small original-size satchel only.

Raw: godot-spike/docs/evidence/spike02-a6/candidates/02/attempt-2.png SHA-256 `5cb4d19822b571cc7f7416c3dddcf45d9ed3bfeeab50873611af07515e1e7756`

Runtime SHA-256: `None` (null = not adopted). Pick=False, adopted=False. Rejected in favor of 1: shoulder/stole drape more bulbous, embroidery simplification and wrist/hand pose drift; structural feet are improved but fidelity is not better.

Normalization and cleanup: {"raw_sha256": "5cb4d19822b571cc7f7416c3dddcf45d9ed3bfeeab50873611af07515e1e7756", "normalized_sha256": "114651c14b10026b237833d59ea1faff15c0c3c3cb3047675737428eed196bc3", "settings": {"scale": 0.3893, "translate": [17.0, 19.5], "palette_remap": true}, "palette_distance": {"before": 5.661234, "after": 0.692524, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/02-attempt-2-cleanup-mask.png", "cleanup_mask_sha256": "3cf61441d31a6a8ad05fd23b2d8b2c653d4f8a31e08583efa2ba80218a277575", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}
