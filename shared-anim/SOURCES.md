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

Model verdict: structural sleeve/hem/foot continuity improves, but all five
motion frames remain PLACEHOLDER for motif/fringe, face and sequence drift.
04 also fails the requested exact mace pose geometry (head about19px high).
Contact03 transform retains [455,196]; fixed manifest/timing and reference PNGs
are unchanged. See A6 W3-OBSERVATIONS.md, geometry-check.json and frame-audit.json.
Godot is Owner-selected; React and Phase B are CANCELLED. Human playtest remains
HUMAN_PENDING. Exact painted A5 mace/grip pixels are not claimed preserved.

Built-in image_gen. Exactly idle/01 + swing/05 for identity/costume/style/mace; A5 same-index ONLY for pose. No rig/region compositing. Seed/model/quality: not exposed. Transparent background requested. Maximum 4 attempts per frame. Every unchanged raw candidate retained under godot-spike/docs/evidence/spike02-a6/candidates/. Full normalization transforms, cleanup masks, palette distances and hashes in a6-swing-prompts.json. Uniform scale/translate, alpha<24 cleanup, idle/01 nearest-128-colour remap only. See A6 METHOD.md for gate and limits. Human playtest HUMAN_PENDING; model checks are not Owner art approval.

### thoma/swing/02.png attempt 1

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1280, 1280]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/02.png", "role": "A5 pose/silhouette ONLY", "sha256": "91a68c71be081b72fef49a0c90ec010f1fe6a456b64b9ecda1940ae4a0867818"}]

Use case: stylized-concept. Asset: ONE complete newly painted full-body 2D animation sprite, frame swing/02, real transparent background, square 512x512 canvas (if higher resolution output, preserve these normalized coordinates). Reference image 1 idle/01 and reference image 2 swing/05 are the ONLY authorities for ALL costume detail, face, grey hair/beard, muted teal/ivory/brown palette, brush/ink style, exact short one-handed flanged mace (dark iron flanges, worn oak haft, small brass collar). Reference image 3 A5 swing/02 defines POSE AND SILHOUETTE ONLY: never copy its broken cloth fragments, gaps, costume patches or detached shoes. Regenerate the ENTIRE man coherently in a single painting, no cutout parts or collage. Same elderly weathered man in three-quarter view facing right. Head near x296 y145, head-to-ground height about 350 pixels, planted ground y464, stance centered on foot pivot [256,464], left boot x128 y444 and right boot x370 y430. Braced mid-swing torso; right arm extends diagonally up/right, hand around [371,166], short mace head around [443,111], SAME mace proportions as references 1/2, not a long pole weapon. Left arm counterbalances with one naturally attached hand. Coherent shoulder and sleeves, ivory wide inner cuffs; unbroken teal robe over ivory underskirt, continuous scalloped hem, both legs visibly connect to brown boots. Exactly ONE brown satchel at left hip with single rolled cloth, one belt and round bronze pendant. Two continuous ivory stole bands, simple small botanical embroidery only at their lower ends, same motif scale as references 1/2; no embroidery added to robe/hem. Do not add accessories, magic, scenery, props, other figures, labels, shadow, platform or background. Full head, both feet and mace entirely inside canvas. Match worn painterly fine ink edges, subdued top-left light and precise costume detail of references 1/2. A restrained short grey-teal motion smear behind mace only. Avoid triangular hem scraps, floating sleeve pieces, disconnected limbs, cloned bag, redesigned face, chibi proportions, bright grading.

Raw: godot-spike/docs/evidence/spike02-a6/candidates/02/attempt-1.png SHA-256 `4d462f01ef8327c8a309613dfc4e92fd7681742eeed35f5d4793ea0715376942`

Runtime SHA-256: `0f76a0f68e6ea294146accdba635fa999a5fb6db532bc2b957461dd2e2050624` (null = not adopted). Pick=True, adopted=True. W1 best candidate: continuous sleeve, hem and both boots; recognizable reference costume. Motif and finer stylistic drift remain W3 checks.

Normalization and cleanup: {"raw_sha256": "4d462f01ef8327c8a309613dfc4e92fd7681742eeed35f5d4793ea0715376942", "normalized_sha256": "0f76a0f68e6ea294146accdba635fa999a5fb6db532bc2b957461dd2e2050624", "settings": {"scale": 0.37155, "translate": [25.0, 35.2], "palette_remap": true}, "palette_distance": {"before": 6.622218, "after": 0.576556, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/02-attempt-1-cleanup-mask.png", "cleanup_mask_sha256": "ba5802b9c17d40dc8b6cff279d789ffd69cd9fe9528bcb5430bdb23cd9ffc7b5", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}

### thoma/swing/02.png attempt 2

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1280, 1280]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/02.png", "role": "A5 pose/silhouette ONLY", "sha256": "91a68c71be081b72fef49a0c90ec010f1fe6a456b64b9ecda1940ae4a0867818"}]

Use case: stylized-concept. Asset: ONE complete newly painted full-body 2D animation sprite, frame swing/02, real transparent background, square 512x512 canvas (if higher resolution output, preserve these normalized coordinates). Reference image 1 idle/01 and reference image 2 swing/05 are the ONLY authorities for ALL costume detail, face, grey hair/beard, muted teal/ivory/brown palette, brush/ink style, exact short one-handed flanged mace (dark iron flanges, worn oak haft, small brass collar). Reference image 3 A5 swing/02 defines POSE AND SILHOUETTE ONLY: never copy its broken cloth fragments, gaps, costume patches or detached shoes. Regenerate the ENTIRE man coherently in a single painting, no cutout parts or collage. Same elderly weathered man in three-quarter view facing right. Head near x296 y145, head-to-ground height about 350 pixels, planted ground y464, stance centered on foot pivot [256,464], left boot x128 y444 and right boot x370 y430. Braced mid-swing torso; right arm extends diagonally up/right, hand around [371,166], short mace head around [443,111], SAME mace proportions as references 1/2, not a long pole weapon. Left arm counterbalances with one naturally attached hand. Coherent shoulder and sleeves, ivory wide inner cuffs; unbroken teal robe over ivory underskirt, continuous scalloped hem, both legs visibly connect to brown boots. Exactly ONE brown satchel at left hip with single rolled cloth, one belt and round bronze pendant. Two continuous ivory stole bands, simple small botanical embroidery only at their lower ends, same motif scale as references 1/2; no embroidery added to robe/hem. Do not add accessories, magic, scenery, props, other figures, labels, shadow, platform or background. Full head, both feet and mace entirely inside canvas. Match worn painterly fine ink edges, subdued top-left light and precise costume detail of references 1/2. A restrained short grey-teal motion smear behind mace only. Avoid triangular hem scraps, floating sleeve pieces, disconnected limbs, cloned bag, redesigned face, chibi proportions, bright grading.
Correction for this independent attempt: match the SMALL, understated botanical sprigs of references 1/2 exactly; preserve their ivory stole's short fringe and restrained dark-grey embroidered leaves, not a large decorative plant. Avoid excessive crisp texture, saturated teal, reddish trim or a youthful face; the reference has a slender weathered elderly face and soft fine brushwork. Keep the swing silhouette but render costume with the exact unornamented worn surfaces of reference 1. No bright orange embroidery borders. One small original-size satchel only.

Raw: godot-spike/docs/evidence/spike02-a6/candidates/02/attempt-2.png SHA-256 `5cb4d19822b571cc7f7416c3dddcf45d9ed3bfeeab50873611af07515e1e7756`

Runtime SHA-256: `None` (null = not adopted). Pick=False, adopted=False. Rejected in favor of 1: shoulder/stole drape more bulbous, embroidery simplification and wrist/hand pose drift; structural feet are improved but fidelity is not better.

Normalization and cleanup: {"raw_sha256": "5cb4d19822b571cc7f7416c3dddcf45d9ed3bfeeab50873611af07515e1e7756", "normalized_sha256": "114651c14b10026b237833d59ea1faff15c0c3c3cb3047675737428eed196bc3", "settings": {"scale": 0.3893, "translate": [17.0, 19.5], "palette_remap": true}, "palette_distance": {"before": 5.661234, "after": 0.692524, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/02-attempt-2-cleanup-mask.png", "cleanup_mask_sha256": "3cf61441d31a6a8ad05fd23b2d8b2c653d4f8a31e08583efa2ba80218a277575", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}

### thoma/swing/00.png attempt 1

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1254, 1254]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/00.png", "role": "A5 pose/silhouette ONLY", "sha256": "578b460defc4c53ba632002e405d40e2b6d40282a85da7db192e0b75be7d9663"}]

Use case: stylized-concept. Generate ONE complete new full-body 2D animation frame of the elderly grey-haired bearded man. Transparent square canvas 512x512 requested (coordinates below are normalized to 512 if output larger). Image 1 idle/01 and image 2 swing/05 are the ONLY sources for costume, face/hair identity, muted teal/ivory/brown palette, subdued top-left light, fine painterly ink/brush style and the exact short one-handed flanged mace: dark iron head, worn oak haft, small brass collar. Image 3 is A5 of the target index: POSE/SILHOUETTE GUIDE ONLY. All costume detail comes from images 1/2; DO NOT reproduce image3's pasted patches, sleeve fragments, leg gaps or floating hem. Paint the ENTIRE figure coherently in one pass, no rig/composite parts. Preserve exact two ivory stole bands and their small grey botanical sprigs, ivory wide cuffs, teal robe and hood, continuous ivory underskirt, single round bronze pendant, belt, exactly ONE brown satchel containing one rolled cloth, brown boots. Keep short fringe, small subtle motifs only on lower stole ends; no ornament on hem or robe. No redesign, new accessory, extra figure, scenery, text, platform or cast shadow. Full body/mace entirely visible. Natural shoulders, cuffs, knees/legs connected to both boots, continuous coherent scalloped hem. Foot pivot [256,464], ground y464, head-to-ground roughly 350-360px, same character proportions as image1. Match soft detailed worn painting of images1/2; no bright palette or Ferry Dusk. Target swing/00 ANTICIPATION: match image3's broad braced stance and raised one-handed mace behind the head, preparing to swing right. Hand at [130,125], mace head at [192,91], oak haft short (hand-to-head around 75px) angled upward-right. Face center [256,143], head top about114, left boot at[148,446], right boot [351,416]. Left free arm extends toward right with a complete natural hand around[377,250]. Robe follows bent torso; maintain attachment of both boots to natural lower legs under continuous underskirt. No smear in this frame. Mace dimensions/head/grip orientation match A5 pose; costume entirely from first two reference images.


Raw: godot-spike/docs/evidence/spike02-a6/candidates/00/attempt-1.png SHA-256 `7e4c391cb17a0c074d5d19faef17f74285205349d6732bc45f05b55402749641`

Runtime SHA-256: `9b677f91691d3a23786f6d82aac949a00973901cbea96b225f275e1ba4332bf7` (null = not adopted). Pick=True, adopted=True. Complete raised-arm figure removes detached right shoe and broken hem. Botanical sprigs/fringe and face rendering remain fidelity checks in W3.

Normalization and cleanup: {"raw_sha256": "7e4c391cb17a0c074d5d19faef17f74285205349d6732bc45f05b55402749641", "normalized_sha256": "9b677f91691d3a23786f6d82aac949a00973901cbea96b225f275e1ba4332bf7", "settings": {"scale": 0.371, "translate": [15.0, 37.0], "palette_remap": true}, "palette_distance": {"before": 5.71192, "after": 0.666352, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/00-attempt-1-cleanup-mask.png", "cleanup_mask_sha256": "f176fcd827a2863105766613290ecaf7ad7a034db3ad83e2f3fb54d12918e9fb", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}

### thoma/swing/03.png attempt 1

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1254, 1254]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/03.png", "role": "A5 pose/silhouette ONLY", "sha256": "f4b590dc492705067948bc9c31fcfdbdfa01a5b424f75cda5a0e6d28cf319d88"}]

Use case: stylized-concept. Generate ONE complete new full-body 2D animation frame of the elderly grey-haired bearded man. Transparent square canvas 512x512 requested (coordinates below are normalized to 512 if output larger). Image 1 idle/01 and image 2 swing/05 are the ONLY sources for costume, face/hair identity, muted teal/ivory/brown palette, subdued top-left light, fine painterly ink/brush style and the exact short one-handed flanged mace: dark iron head, worn oak haft, small brass collar. Image 3 is A5 of the target index: POSE/SILHOUETTE GUIDE ONLY. All costume detail comes from images 1/2; DO NOT reproduce image3's pasted patches, sleeve fragments, leg gaps or floating hem. Paint the ENTIRE figure coherently in one pass, no rig/composite parts. Preserve exact two ivory stole bands and their small grey botanical sprigs, ivory wide cuffs, teal robe and hood, continuous ivory underskirt, single round bronze pendant, belt, exactly ONE brown satchel containing one rolled cloth, brown boots. Keep short fringe, small subtle motifs only on lower stole ends; no ornament on hem or robe. No redesign, new accessory, extra figure, scenery, text, platform or cast shadow. Full body/mace entirely visible. Natural shoulders, cuffs, knees/legs connected to both boots, continuous coherent scalloped hem. Foot pivot [256,464], ground y464, head-to-ground roughly 350-360px, same character proportions as image1. Match soft detailed worn painting of images1/2; no bright palette or Ferry Dusk. Target swing/03 CONTACT, NO motion smear: faithfully match image3's contact silhouette. Entire head of mace is a small iron flanged head CENTERED at [455,196], horizontally held. Hand grips short oak haft at [355,196]; mace head dimension about40x34px, hand-to-head distance100px. Exact contact geometry is critical. The right arm reaches horizontally to screen-right at chest height; wrist/elbow anatomically braced, shoulder compressed. Face center around [279,143], head top114, boots planted at [135,447] and[357,427], ground464. Torso twists forward, left free arm counterbalances near belt at[329,255] with a natural complete hand. Continuous teal sleeve over ivory cuff, no unnatural sleeve fragment below extended arm. Natural single robe and underskirt with both boots connected, no horizontal waist seam from cutout. Small original-size embroidery sprigs from images1/2, no added large pattern. No weapon distortion, no sparks/effects or opponent.


Raw: godot-spike/docs/evidence/spike02-a6/candidates/03/attempt-1.png SHA-256 `4083388200a2954d2df0511e3481b66d328712bbffe5e1c609ded94efa00b718`

Runtime SHA-256: `418676b008e19d4aa36114e2f01fef35967b2f896833ae43ed62522d947468e1` (null = not adopted). Pick=True, adopted=True. Coherent contact arm and continuous lower body, no pasted underarm fragment. Uniform transform maps raw mace head center [1170,424] to [455,196] and ground1143 to464. Motif fringe and style fidelity still need W3.

Normalization and cleanup: {"raw_sha256": "4083388200a2954d2df0511e3481b66d328712bbffe5e1c609ded94efa00b718", "normalized_sha256": "418676b008e19d4aa36114e2f01fef35967b2f896833ae43ed62522d947468e1", "settings": {"scale": 0.372739916550765, "translate": [18.8942976356, 37.9582753825], "palette_remap": true}, "palette_distance": {"before": 5.760951, "after": 0.70966, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/03-attempt-1-cleanup-mask.png", "cleanup_mask_sha256": "0e0143ac42e33affe9a7cf37ee125a975a7ccab0816c0c0345b8d4583b976dc1", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}

### thoma/swing/04.png attempt 1

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1254, 1254]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/04.png", "role": "A5 pose/silhouette ONLY", "sha256": "cccce1128daf423eb337a88d8dae5fe507524b448ca140d5c57bc488841c96e9"}]

Use case: stylized-concept. Generate ONE complete new full-body 2D animation frame of the elderly grey-haired bearded man. Transparent square canvas 512x512 requested (coordinates below are normalized to 512 if output larger). Image 1 idle/01 and image 2 swing/05 are the ONLY sources for costume, face/hair identity, muted teal/ivory/brown palette, subdued top-left light, fine painterly ink/brush style and the exact short one-handed flanged mace: dark iron head, worn oak haft, small brass collar. Image 3 is A5 of the target index: POSE/SILHOUETTE GUIDE ONLY. All costume detail comes from images 1/2; DO NOT reproduce image3's pasted patches, sleeve fragments, leg gaps or floating hem. Paint the ENTIRE figure coherently in one pass, no rig/composite parts. Preserve exact two ivory stole bands and their small grey botanical sprigs, ivory wide cuffs, teal robe and hood, continuous ivory underskirt, single round bronze pendant, belt, exactly ONE brown satchel containing one rolled cloth, brown boots. Keep short fringe, small subtle motifs only on lower stole ends; no ornament on hem or robe. No redesign, new accessory, extra figure, scenery, text, platform or cast shadow. Full body/mace entirely visible. Natural shoulders, cuffs, knees/legs connected to both boots, continuous coherent scalloped hem. Foot pivot [256,464], ground y464, head-to-ground roughly 350-360px, same character proportions as image1. Match soft detailed worn painting of images1/2; no bright palette or Ferry Dusk. Target swing/04 FOLLOW-THROUGH, no motion smear: match image3's downward-right swing silhouette, distinct from contact. Right hand at[348,315], short mace iron head at[421,376], haft angled down/right about40 degrees, same head 40x34px and short hand-to-head length about100px. Face center[307,154], top120, body leans forward; free left hand extends behind toward left around[172,240]. Feet at[147,437] and[350,447], planted ground y464, natural stance and two legs continuous into boots under continuous scalloped ivory underskirt. Robe/stole trail subtly with torso twist. Do not copy A5's floating hem strip, ankle gap or sharp pasted shoulder. Same exact small botanical sprigs and short stole fringe, slim elderly face, muted worn brushwork as first two images. No detached garment fragment, no extra weapon, no background.


Raw: godot-spike/docs/evidence/spike02-a6/candidates/04/attempt-1.png SHA-256 `5f66d43bb64e9d4570ee2fa187bd63db14dc226d2fa6c644bab7d25e82c99108`

Runtime SHA-256: `e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0` (null = not adopted). Pick=True, adopted=True. Whole follow-through repaint removes floating hem strip and leg gaps. Same short flanged mace design, continuous natural cuffs and one satchel. Finer motif/texture continuity remains W3.

Normalization and cleanup: {"raw_sha256": "5f66d43bb64e9d4570ee2fa187bd63db14dc226d2fa6c644bab7d25e82c99108", "normalized_sha256": "e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0", "settings": {"scale": 0.352, "translate": [30.0, 61.0], "palette_remap": true}, "palette_distance": {"before": 5.630703, "after": 0.660794, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/04-attempt-1-cleanup-mask.png", "cleanup_mask_sha256": "08c28cb85f9dba8c0bdaaf63c991621db4bfb26eb65fd19216341e932d4d5069", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}

### thoma/swing/01.png attempt 1

Tool: image_gen (built-in); settings: {"transparent_background": true, "seed": "not exposed", "model": "not exposed", "quality": "not exposed", "requested_size": "512x512 via prompt", "returned_size": [1254, 1254]}

References: [{"path": "shared-anim/thoma/idle/01.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808"}, {"path": "shared-anim/thoma/swing/05.png", "role": "costume/face/hair/palette/painting/mace", "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf"}, {"path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/01.png", "role": "A5 pose/silhouette ONLY", "sha256": "b06121b366fe9c126d8bcf40c3ffbff974446282d0f22a844776347ad3a14243"}]

Use case: stylized-concept. Generate ONE complete new full-body 2D animation frame of the elderly grey-haired bearded man. Transparent square canvas 512x512 requested (coordinates below are normalized to 512 if output larger). Image 1 idle/01 and image 2 swing/05 are the ONLY sources for costume, face/hair identity, muted teal/ivory/brown palette, subdued top-left light, fine painterly ink/brush style and the exact short one-handed flanged mace: dark iron head, worn oak haft, small brass collar. Image 3 is A5 of the target index: POSE/SILHOUETTE GUIDE ONLY. All costume detail comes from images 1/2; DO NOT reproduce image3's pasted patches, sleeve fragments, leg gaps or floating hem. Paint the ENTIRE figure coherently in one pass, no rig/composite parts. Preserve exact two ivory stole bands and their small grey botanical sprigs, ivory wide cuffs, teal robe and hood, continuous ivory underskirt, single round bronze pendant, belt, exactly ONE brown satchel containing one rolled cloth, brown boots. Keep short fringe, small subtle motifs only on lower stole ends; no ornament on hem or robe. No redesign, new accessory, extra figure, scenery, text, platform or cast shadow. Full body/mace entirely visible. Natural shoulders, cuffs, knees/legs connected to both boots, continuous coherent scalloped hem. Foot pivot [256,464], ground y464, head-to-ground roughly 350-360px, same character proportions as image1. Match soft detailed worn painting of images1/2; no bright palette or Ferry Dusk. Target swing/01 RAISE. Match ONLY image3's raised pose: right upper arm lifted on screen-left, bent elbow, right hand at[192,112], short mace held above head sloping up/right with iron head center[257,88], grip-to-head about75px, head small40x30px. Face center [260,140], head top110, body upright but preparing downstroke. Free left forearm folds near chest/right shoulder at[315,240] with naturally attached hand, not an extra folded sleeve patch. Boots at[175,445] and[340,411], ground464. Exact same single satchel, continuous scalloped ivory hem and two botanical stole bands from images1/2. Full coherent complete figure, no seam lines from collage, no motion smear. Match source's fine grey hair, narrow weathered face and subdued worn teal robe, ivory cuffs, short fringe and SMALL sparse sprig motifs.


Raw: godot-spike/docs/evidence/spike02-a6/candidates/01/attempt-1.png SHA-256 `35e3adf1c64609328155792dcf3fb5920da0a6ab0da8909cdb0e0e7fa4895dbd`

Runtime SHA-256: `af72787e963038cc4e15ce7ded953a9c9202aabda110c8792e519b97460812b8` (null = not adopted). Pick=True, adopted=True. Exception to retain01: 01-neighbours-before.png shows old wider satchel/hem and cuff construction popping between new00/02. Repainted complete figure restores coherent drape, one satchel and attached boots. Motif/texture fidelity remains W3.

Normalization and cleanup: {"raw_sha256": "35e3adf1c64609328155792dcf3fb5920da0a6ab0da8909cdb0e0e7fa4895dbd", "normalized_sha256": "af72787e963038cc4e15ce7ded953a9c9202aabda110c8792e519b97460812b8", "settings": {"scale": 0.3546, "translate": [25.4, 44.8628], "palette_remap": true}, "palette_distance": {"before": 5.457934, "after": 0.696423, "metric": "mean nearest idle/01 128-color Euclidean RGB, alpha>240"}, "cleanup_mask": "godot-spike/docs/evidence/spike02-a6/normalized/01-attempt-1-cleanup-mask.png", "cleanup_mask_sha256": "1940283aee2c1bad15f8ad8864d74237a60b8195174dc14ac577b94cf56c1b89", "operations": "single uniform scale/translate; alpha<24 cleared; nearest idle/01 128-color remap, no dither; transparent RGB cleared; no costume compositing", "runtime_sha256": null, "adopted": false}


## spike-02 A7 — constrained edits and anchor touch-ups

### A7 swing/01, attempt 1

Exact attempt record (all prompts, inputs, masks, intermediate hashes, settings): `godot-spike/docs/evidence/spike02-a7/attempts/01/attempt-1.json`.

{
  "frame": "thoma/swing/01.png",
  "attempt": 1,
  "tool": "image_gen (built-in)",
  "mode": "edit existing A6 target with two immutable anchors, not independent regeneration",
  "prompt": "Use case: identity-preserve / precise-object-edit. EDIT the FIRST image, an EXISTING swing/01 animation frame. Do NOT generate an independent new full-body pose. Images 2 and 3 are immutable appearance anchors: same elderly man, angular weathered face, close grey swept hair, short grey beard, narrow dark eyes, teal cowl and robe, ivory stole/undersleeves, brown single satchel with one cloth roll, bronze medallion. Retain the FIRST image exact canvas framing, scale, complete silhouette, pose, hands/grip, connected feet and ONE bag. Preserve its fine worn hand-painted edges and muted original colours. Make only small controlled identity and costume corrections to the first image: match the anchor face/hair features, narrow ivory stole falls and their exact small grey-green botanical sprigs, short irregular ivory fringes, cuff edge and layered continuous hem. There are TWO sprigs total, one at each stole end: a simple central stem with alternating oblique leaf strokes, about 18x31px left and 15x43px right on 512px canvas, no new motifs or trim. Short fringe tips 4-9px, approximately 10 left/8 right visible, plus ONE long waist rope, no long new tassels. Match exact anchor motif scale, not a large decorative plant. Use the anchors to restore the SAME character, not a younger/redesigned face. Repair local details while retaining all already-correct structure. 512x512 transparent canvas, pivot [256,464]. Pose intent: raise; mace head target [259, 87], grip [194, 109]. Keep existing A6 mace head/haft/collar/grip dimensions and orientation, single short one-handed dark iron flanged mace on worn oak haft with small brass collar. Do not move the weapon, hands, body or feet. No scene, other figures, labels, cast shadow, new ornament, duplicate bag, detached footwear, geometric fragments, bright recolouring or Ferry Dusk palette. Output ONLY the edited first sprite on genuine alpha.",
  "references": [
    {
      "path": "godot-spike/docs/evidence/spike02-a7/baseline-a6/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/01/edit-target.png",
      "sha256": "af72787e963038cc4e15ce7ded953a9c9202aabda110c8792e519b97460812b8",
      "role": "EDIT TARGET: A6 structure/pose; retain feet, bag, weapon"
    },
    {
      "path": "shared-anim/thoma/idle/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/01/anchor-idle.png",
      "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "role": "APPEARANCE MASTER ONLY"
    },
    {
      "path": "shared-anim/thoma/swing/05.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/01/anchor-recover.png",
      "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
      "role": "APPEARANCE corroboration ONLY"
    }
  ],
  "spec_sha256": "bb0c9ff5949c659f35a892ad4e2b38aa28bb645fd8b4a81fbdf6f76c01ddb163",
  "base_selection": {
    "structure": "A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.",
    "face_hair": "idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.",
    "embroidery_tassels": "idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.",
    "cuffs_hem_bag_feet_weapon": "A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.",
    "a5_considered": {
      "path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/01.png",
      "sha256": "b06121b366fe9c126d8bcf40c3ffbff974446282d0f22a844776347ad3a14243",
      "reason": "01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps."
    },
    "a6_raw_considered": [
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/01/attempt-1.png",
        "sha256": "35e3adf1c64609328155792dcf3fb5920da0a6ab0da8909cdb0e0e7fa4895dbd",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      }
    ]
  },
  "settings": {
    "transparent_background": true,
    "seed": "not exposed",
    "model": "not exposed",
    "quality": "not exposed",
    "requested_size": [
      512,
      512
    ],
    "returned_size": [
      1254,
      1254
    ]
  },
  "status": "FINISHED",
  "adopted": true,
  "touchups": [
    {
      "name": "anchor face/hair interior",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-01-input.png",
      "input_sha256": "af72787e963038cc4e15ce7ded953a9c9202aabda110c8792e519b97460812b8",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-01-output.png",
      "output_sha256": "0fbf08576c4749ae462c520d4ba7e3a9be781ce6a06974aacaa67223798aa0b7",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-01-mask.png",
      "mask_sha256": "88a6ec7fead3af34d3aee4703090188384906d07152883405ed92a78e77acf8e",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            232,
            118
          ],
          [
            239,
            109
          ],
          [
            252,
            106
          ],
          [
            270,
            110
          ],
          [
            281,
            121
          ],
          [
            283,
            149
          ],
          [
            273,
            163
          ],
          [
            258,
            169
          ],
          [
            244,
            158
          ],
          [
            236,
            145
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          4,
          3
        ],
        "feather_px": 1.25,
        "limit": "Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor left sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-02-input.png",
      "input_sha256": "0fbf08576c4749ae462c520d4ba7e3a9be781ce6a06974aacaa67223798aa0b7",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-02-output.png",
      "output_sha256": "fb7e060bb0ae629509437b16d15e56251b2916ca5cae21f7d2faef3514b292fd",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-02-mask.png",
      "mask_sha256": "07aafa81fe0b610cc8450285f4648e42969546bcbd24b7d2f76958fc1513222f",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            224,
            349
          ],
          [
            251,
            349
          ],
          [
            254,
            377
          ],
          [
            247,
            383
          ],
          [
            221,
            381
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          0,
          0
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor right sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-03-input.png",
      "input_sha256": "fb7e060bb0ae629509437b16d15e56251b2916ca5cae21f7d2faef3514b292fd",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-03-output.png",
      "output_sha256": "04e70b804a28124bee6c9f6b3c38070336c6e44ea6f646899826f4fe1317f4da",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/01/touchup-03-mask.png",
      "mask_sha256": "726ea95afe226a66cf1b551d32d639c0b9ec5f6d2b53d34e429fe2b6be13fe58",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            288,
            300
          ],
          [
            305,
            299
          ],
          [
            310,
            348
          ],
          [
            309,
            358
          ],
          [
            289,
            364
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          0,
          -4
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    }
  ],
  "raw": "godot-spike/docs/evidence/spike02-a7/attempts/01/attempt-1.png",
  "raw_sha256": "f76199d4fa3cdc4c0933f0b0d74f35dbf0664ee0b8310ea2ef97e0eb7f9cf180",
  "normalization": {
    "scale": 0.4082934609250399,
    "translate": [
      0,
      0
    ],
    "method": "uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif",
    "output": "godot-spike/docs/evidence/spike02-a7/attempts/01/attempt-1-normalized-preview.png",
    "sha256": "a336b7800a99616d1dcd14e90e4f61f5065e5e0f9a3481a8e3b089752bae39a2"
  },
  "generated_pixels_adopted": false,
  "raw_result": "REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.",
  "runtime": "godot-spike/docs/evidence/spike02-a7/attempts/01/attempt-1-runtime.png",
  "runtime_sha256": "04e70b804a28124bee6c9f6b3c38070336c6e44ea6f646899826f4fe1317f4da",
  "placeholder": true,
  "reason": "Anchor interior texture corrections only. Outer silhouette/drape and remaining motif fringes are not proven consistent; retain PLACEHOLDER.",
  "completed_order": 1,
  "previous_frame": null,
  "neighbour_check": {
    "role": "consistency check ONLY, never appearance source",
    "previous_frame": null,
    "sha256": null
  }
}


### A7 swing/02, attempt 1

Exact attempt record (all prompts, inputs, masks, intermediate hashes, settings): `godot-spike/docs/evidence/spike02-a7/attempts/02/attempt-1.json`.

{
  "frame": "thoma/swing/02.png",
  "attempt": 1,
  "tool": "image_gen (built-in)",
  "mode": "edit existing A6 target with two immutable anchors, not independent regeneration",
  "prompt": "Use case: identity-preserve / precise-object-edit. EDIT the FIRST image, an EXISTING swing/02 animation frame. Do NOT generate an independent new full-body pose. Images 2 and 3 are immutable appearance anchors: same elderly man, angular weathered face, close grey swept hair, short grey beard, narrow dark eyes, teal cowl and robe, ivory stole/undersleeves, brown single satchel with one cloth roll, bronze medallion. Retain the FIRST image exact canvas framing, scale, complete silhouette, pose, hands/grip, connected feet and ONE bag. Preserve its fine worn hand-painted edges and muted original colours. Make only small controlled identity and costume corrections to the first image: match the anchor face/hair features, narrow ivory stole falls and their exact small grey-green botanical sprigs, short irregular ivory fringes, cuff edge and layered continuous hem. There are TWO sprigs total, one at each stole end: a simple central stem with alternating oblique leaf strokes, about 18x31px left and 15x43px right on 512px canvas, no new motifs or trim. Short fringe tips 4-9px, approximately 10 left/8 right visible, plus ONE long waist rope, no long new tassels. Match exact anchor motif scale, not a large decorative plant. Use the anchors to restore the SAME character, not a younger/redesigned face. Repair local details while retaining all already-correct structure. 512x512 transparent canvas, pivot [256,464]. Pose intent: swing (smear hidden under Reduced Motion); mace head target [449, 110], grip [372, 160]. Keep existing A6 mace head/haft/collar/grip dimensions and orientation, single short one-handed dark iron flanged mace on worn oak haft with small brass collar. Do not move the weapon, hands, body or feet. No scene, other figures, labels, cast shadow, new ornament, duplicate bag, detached footwear, geometric fragments, bright recolouring or Ferry Dusk palette. Output ONLY the edited first sprite on genuine alpha.",
  "references": [
    {
      "path": "godot-spike/docs/evidence/spike02-a7/baseline-a6/02.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/02/edit-target.png",
      "sha256": "0f76a0f68e6ea294146accdba635fa999a5fb6db532bc2b957461dd2e2050624",
      "role": "EDIT TARGET: A6 structure/pose; retain feet, bag, weapon"
    },
    {
      "path": "shared-anim/thoma/idle/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/02/anchor-idle.png",
      "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "role": "APPEARANCE MASTER ONLY"
    },
    {
      "path": "shared-anim/thoma/swing/05.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/02/anchor-recover.png",
      "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
      "role": "APPEARANCE corroboration ONLY"
    }
  ],
  "spec_sha256": "bb0c9ff5949c659f35a892ad4e2b38aa28bb645fd8b4a81fbdf6f76c01ddb163",
  "base_selection": {
    "structure": "A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.",
    "face_hair": "idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.",
    "embroidery_tassels": "idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.",
    "cuffs_hem_bag_feet_weapon": "A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.",
    "a5_considered": {
      "path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/02.png",
      "sha256": "91a68c71be081b72fef49a0c90ec010f1fe6a456b64b9ecda1940ae4a0867818",
      "reason": "01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps."
    },
    "a6_raw_considered": [
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/02/attempt-1.png",
        "sha256": "4d462f01ef8327c8a309613dfc4e92fd7681742eeed35f5d4793ea0715376942",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/02/attempt-2.png",
        "sha256": "5cb4d19822b571cc7f7416c3dddcf45d9ed3bfeeab50873611af07515e1e7756",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      }
    ]
  },
  "settings": {
    "transparent_background": true,
    "seed": "not exposed",
    "model": "not exposed",
    "quality": "not exposed",
    "requested_size": [
      512,
      512
    ],
    "returned_size": [
      1254,
      1254
    ]
  },
  "status": "FINISHED",
  "adopted": true,
  "touchups": [
    {
      "name": "anchor face/hair interior",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-01-input.png",
      "input_sha256": "0f76a0f68e6ea294146accdba635fa999a5fb6db532bc2b957461dd2e2050624",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-01-output.png",
      "output_sha256": "c8c921970728dd8d995075b8d2c910d7831ae5cc3a8fa4c3691c691ad560eaab",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-01-mask.png",
      "mask_sha256": "787cf6340158905dd72a516cb96dfa356970cb4502b3370addf039f870ca93af",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            232,
            118
          ],
          [
            239,
            109
          ],
          [
            252,
            106
          ],
          [
            270,
            110
          ],
          [
            281,
            121
          ],
          [
            283,
            149
          ],
          [
            273,
            163
          ],
          [
            258,
            169
          ],
          [
            244,
            158
          ],
          [
            236,
            145
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          26,
          7
        ],
        "feather_px": 1.25,
        "limit": "Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor left sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-02-input.png",
      "input_sha256": "c8c921970728dd8d995075b8d2c910d7831ae5cc3a8fa4c3691c691ad560eaab",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-02-output.png",
      "output_sha256": "1a4cf8550bdc255e494a57392724e1d52d830f2867af3eecb2608571bffb01ca",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-02-mask.png",
      "mask_sha256": "07aafa81fe0b610cc8450285f4648e42969546bcbd24b7d2f76958fc1513222f",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            224,
            349
          ],
          [
            251,
            349
          ],
          [
            254,
            377
          ],
          [
            247,
            383
          ],
          [
            221,
            381
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          0,
          0
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor right sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-03-input.png",
      "input_sha256": "1a4cf8550bdc255e494a57392724e1d52d830f2867af3eecb2608571bffb01ca",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-03-output.png",
      "output_sha256": "fcad56a9948ecb7ca9608354ecc2dbddccce2fb941275e0c982b123a04788af4",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/02/touchup-03-mask.png",
      "mask_sha256": "9b0513c77d94305fcc77c4202d4a2827cd77865d9600b973e71659f741c1bc6a",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            288,
            300
          ],
          [
            305,
            299
          ],
          [
            310,
            348
          ],
          [
            309,
            358
          ],
          [
            289,
            364
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          0,
          -5
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    }
  ],
  "raw": "godot-spike/docs/evidence/spike02-a7/attempts/02/attempt-1.png",
  "raw_sha256": "e365138c504538f3b54821925324c4c70b37f44e05bdfcbaa31a991a7e0d3968",
  "normalization": {
    "scale": 0.4082934609250399,
    "translate": [
      0,
      0
    ],
    "method": "uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif",
    "output": "godot-spike/docs/evidence/spike02-a7/attempts/02/attempt-1-normalized-preview.png",
    "sha256": "f9c09d5e17d20e0f1fe818456da51caf8b499b35fce0bcf2a0de0e7d7063f4d4"
  },
  "generated_pixels_adopted": false,
  "raw_result": "REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.",
  "runtime": "godot-spike/docs/evidence/spike02-a7/attempts/02/attempt-1-runtime.png",
  "runtime_sha256": "fcad56a9948ecb7ca9608354ecc2dbddccce2fb941275e0c982b123a04788af4",
  "placeholder": true,
  "reason": "Anchor interior texture corrections only. Outer silhouette/drape and remaining motif fringes are not proven consistent; retain PLACEHOLDER.",
  "completed_order": 2,
  "previous_frame": "01",
  "neighbour_check": {
    "role": "consistency check ONLY, never appearance source",
    "previous_frame": "01",
    "sha256": "04e70b804a28124bee6c9f6b3c38070336c6e44ea6f646899826f4fe1317f4da"
  }
}


### A7 swing/00, attempt 1

Exact attempt record (all prompts, inputs, masks, intermediate hashes, settings): `godot-spike/docs/evidence/spike02-a7/attempts/00/attempt-1.json`.

{
  "frame": "thoma/swing/00.png",
  "attempt": 1,
  "tool": "image_gen (built-in)",
  "mode": "edit existing A6 target with two immutable anchors, not independent regeneration",
  "prompt": "Use case: identity-preserve / precise-object-edit. EDIT the FIRST image, an EXISTING swing/00 animation frame. Do NOT generate an independent new full-body pose. Images 2 and 3 are immutable appearance anchors: same elderly man, angular weathered face, close grey swept hair, short grey beard, narrow dark eyes, teal cowl and robe, ivory stole/undersleeves, brown single satchel with one cloth roll, bronze medallion. Retain the FIRST image exact canvas framing, scale, complete silhouette, pose, hands/grip, connected feet and ONE bag. Preserve its fine worn hand-painted edges and muted original colours. Make only small controlled identity and costume corrections to the first image: match the anchor face/hair features, narrow ivory stole falls and their exact small grey-green botanical sprigs, short irregular ivory fringes, cuff edge and layered continuous hem. There are TWO sprigs total, one at each stole end: a simple central stem with alternating oblique leaf strokes, about 18x31px left and 15x43px right on 512px canvas, no new motifs or trim. Short fringe tips 4-9px, approximately 10 left/8 right visible, plus ONE long waist rope, no long new tassels. Match exact anchor motif scale, not a large decorative plant. Use the anchors to restore the SAME character, not a younger/redesigned face. Repair local details while retaining all already-correct structure. 512x512 transparent canvas, pivot [256,464]. Pose intent: anticipation; mace head target [192, 85], grip [127, 117]. Keep existing A6 mace head/haft/collar/grip dimensions and orientation, single short one-handed dark iron flanged mace on worn oak haft with small brass collar. Do not move the weapon, hands, body or feet. No scene, other figures, labels, cast shadow, new ornament, duplicate bag, detached footwear, geometric fragments, bright recolouring or Ferry Dusk palette. Output ONLY the edited first sprite on genuine alpha.",
  "references": [
    {
      "path": "godot-spike/docs/evidence/spike02-a7/baseline-a6/00.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/00/edit-target.png",
      "sha256": "9b677f91691d3a23786f6d82aac949a00973901cbea96b225f275e1ba4332bf7",
      "role": "EDIT TARGET: A6 structure/pose; retain feet, bag, weapon"
    },
    {
      "path": "shared-anim/thoma/idle/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/00/anchor-idle.png",
      "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "role": "APPEARANCE MASTER ONLY"
    },
    {
      "path": "shared-anim/thoma/swing/05.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/00/anchor-recover.png",
      "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
      "role": "APPEARANCE corroboration ONLY"
    }
  ],
  "spec_sha256": "bb0c9ff5949c659f35a892ad4e2b38aa28bb645fd8b4a81fbdf6f76c01ddb163",
  "base_selection": {
    "structure": "A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.",
    "face_hair": "idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.",
    "embroidery_tassels": "idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.",
    "cuffs_hem_bag_feet_weapon": "A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.",
    "a5_considered": {
      "path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/00.png",
      "sha256": "578b460defc4c53ba632002e405d40e2b6d40282a85da7db192e0b75be7d9663",
      "reason": "01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps."
    },
    "a6_raw_considered": [
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/00/attempt-1.png",
        "sha256": "7e4c391cb17a0c074d5d19faef17f74285205349d6732bc45f05b55402749641",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      }
    ]
  },
  "settings": {
    "transparent_background": true,
    "seed": "not exposed",
    "model": "not exposed",
    "quality": "not exposed",
    "requested_size": [
      512,
      512
    ],
    "returned_size": [
      1254,
      1254
    ]
  },
  "status": "FINISHED",
  "adopted": true,
  "touchups": [
    {
      "name": "anchor face/hair interior",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-01-input.png",
      "input_sha256": "9b677f91691d3a23786f6d82aac949a00973901cbea96b225f275e1ba4332bf7",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-01-output.png",
      "output_sha256": "46104b11ef956e45620a2e1d65a97dda54a69f278121a5a88b29e36981c08c22",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-01-mask.png",
      "mask_sha256": "fccc6dbd16ec83369c25ccad24c723a9c22d38f3edb5097d3bc6ac686f4c53be",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            232,
            118
          ],
          [
            239,
            109
          ],
          [
            252,
            106
          ],
          [
            270,
            110
          ],
          [
            281,
            121
          ],
          [
            283,
            149
          ],
          [
            273,
            163
          ],
          [
            258,
            169
          ],
          [
            244,
            158
          ],
          [
            236,
            145
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          4,
          5
        ],
        "feather_px": 1.25,
        "limit": "Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor left sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-02-input.png",
      "input_sha256": "46104b11ef956e45620a2e1d65a97dda54a69f278121a5a88b29e36981c08c22",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-02-output.png",
      "output_sha256": "a3da250b76a7ed5a256eb452fb283cd0624338f3d383641face78671f2b2e5da",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-02-mask.png",
      "mask_sha256": "28c8b33f768e178bbec34d6a5aa630aa52e27894f274fd099b2a70c4e3058ec0",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            224,
            349
          ],
          [
            251,
            349
          ],
          [
            254,
            377
          ],
          [
            247,
            383
          ],
          [
            221,
            381
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -10,
          0
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor right sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-03-input.png",
      "input_sha256": "a3da250b76a7ed5a256eb452fb283cd0624338f3d383641face78671f2b2e5da",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-03-output.png",
      "output_sha256": "15de2abfa371f64128cdbf2fb8cf25175cc4ca33edd07c4c1aebe72872195c2f",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/00/touchup-03-mask.png",
      "mask_sha256": "636c994bcb03197b0567703f686e5280f4b9c73b0c429c81b36fb948c15ffd03",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            288,
            300
          ],
          [
            305,
            299
          ],
          [
            310,
            348
          ],
          [
            309,
            358
          ],
          [
            289,
            364
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          2,
          -1
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    }
  ],
  "raw": "godot-spike/docs/evidence/spike02-a7/attempts/00/attempt-1.png",
  "raw_sha256": "152b5de3847270cb5c9461068684af3ff1300009292b92f87b5c70409a9fc4cd",
  "normalization": {
    "scale": 0.4082934609250399,
    "translate": [
      0,
      0
    ],
    "method": "uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif",
    "output": "godot-spike/docs/evidence/spike02-a7/attempts/00/attempt-1-normalized-preview.png",
    "sha256": "be1edf521b7c8082d857514adbcf03f2940fa6f675f4fada050e4d69e9ac2367"
  },
  "generated_pixels_adopted": false,
  "raw_result": "REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.",
  "runtime": "godot-spike/docs/evidence/spike02-a7/attempts/00/attempt-1-runtime.png",
  "runtime_sha256": "15de2abfa371f64128cdbf2fb8cf25175cc4ca33edd07c4c1aebe72872195c2f",
  "placeholder": true,
  "reason": "Anchor interior texture corrections only. Outer silhouette/drape and remaining motif fringes are not proven consistent; retain PLACEHOLDER.",
  "completed_order": 3,
  "previous_frame": "02",
  "neighbour_check": {
    "role": "consistency check ONLY, never appearance source",
    "previous_frame": "02",
    "sha256": "fcad56a9948ecb7ca9608354ecc2dbddccce2fb941275e0c982b123a04788af4"
  }
}


### A7 swing/03, attempt 1

Exact attempt record (all prompts, inputs, masks, intermediate hashes, settings): `godot-spike/docs/evidence/spike02-a7/attempts/03/attempt-1.json`.

{
  "frame": "thoma/swing/03.png",
  "attempt": 1,
  "tool": "image_gen (built-in)",
  "mode": "edit existing A6 target with two immutable anchors, not independent regeneration",
  "prompt": "Use case: identity-preserve / precise-object-edit. EDIT the FIRST image, an EXISTING swing/03 animation frame. Do NOT generate an independent new full-body pose. Images 2 and 3 are immutable appearance anchors: same elderly man, angular weathered face, close grey swept hair, short grey beard, narrow dark eyes, teal cowl and robe, ivory stole/undersleeves, brown single satchel with one cloth roll, bronze medallion. Retain the FIRST image exact canvas framing, scale, complete silhouette, pose, hands/grip, connected feet and ONE bag. Preserve its fine worn hand-painted edges and muted original colours. Make only small controlled identity and costume corrections to the first image: match the anchor face/hair features, narrow ivory stole falls and their exact small grey-green botanical sprigs, short irregular ivory fringes, cuff edge and layered continuous hem. There are TWO sprigs total, one at each stole end: a simple central stem with alternating oblique leaf strokes, about 18x31px left and 15x43px right on 512px canvas, no new motifs or trim. Short fringe tips 4-9px, approximately 10 left/8 right visible, plus ONE long waist rope, no long new tassels. Match exact anchor motif scale, not a large decorative plant. Use the anchors to restore the SAME character, not a younger/redesigned face. Repair local details while retaining all already-correct structure. 512x512 transparent canvas, pivot [256,464]. Pose intent: contact; mace head target [455, 196], grip [358, 196]. Keep existing A6 mace head/haft/collar/grip dimensions and orientation, single short one-handed dark iron flanged mace on worn oak haft with small brass collar. Do not move the weapon, hands, body or feet. No scene, other figures, labels, cast shadow, new ornament, duplicate bag, detached footwear, geometric fragments, bright recolouring or Ferry Dusk palette. Output ONLY the edited first sprite on genuine alpha.",
  "references": [
    {
      "path": "godot-spike/docs/evidence/spike02-a7/baseline-a6/03.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/03/edit-target.png",
      "sha256": "418676b008e19d4aa36114e2f01fef35967b2f896833ae43ed62522d947468e1",
      "role": "EDIT TARGET: A6 structure/pose; retain feet, bag, weapon"
    },
    {
      "path": "shared-anim/thoma/idle/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/03/anchor-idle.png",
      "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "role": "APPEARANCE MASTER ONLY"
    },
    {
      "path": "shared-anim/thoma/swing/05.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/03/anchor-recover.png",
      "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
      "role": "APPEARANCE corroboration ONLY"
    }
  ],
  "spec_sha256": "bb0c9ff5949c659f35a892ad4e2b38aa28bb645fd8b4a81fbdf6f76c01ddb163",
  "base_selection": {
    "structure": "A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.",
    "face_hair": "idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.",
    "embroidery_tassels": "idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.",
    "cuffs_hem_bag_feet_weapon": "A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.",
    "a5_considered": {
      "path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/03.png",
      "sha256": "f4b590dc492705067948bc9c31fcfdbdfa01a5b424f75cda5a0e6d28cf319d88",
      "reason": "01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps."
    },
    "a6_raw_considered": [
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/03/attempt-1.png",
        "sha256": "4083388200a2954d2df0511e3481b66d328712bbffe5e1c609ded94efa00b718",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      }
    ]
  },
  "settings": {
    "transparent_background": true,
    "seed": "not exposed",
    "model": "not exposed",
    "quality": "not exposed",
    "requested_size": [
      512,
      512
    ],
    "returned_size": [
      1254,
      1254
    ]
  },
  "status": "FINISHED",
  "adopted": true,
  "touchups": [
    {
      "name": "anchor face/hair interior",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-01-input.png",
      "input_sha256": "418676b008e19d4aa36114e2f01fef35967b2f896833ae43ed62522d947468e1",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-01-output.png",
      "output_sha256": "b82bb104d69af90fadc8acea15602562200b709e953bee8f23fe45e928e6023f",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-01-mask.png",
      "mask_sha256": "b51183b6eb3457afb4c9672196fe9ad92dd44941a6900e89f7fdc434b98fadd5",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            232,
            118
          ],
          [
            239,
            109
          ],
          [
            252,
            106
          ],
          [
            270,
            110
          ],
          [
            281,
            121
          ],
          [
            283,
            149
          ],
          [
            273,
            163
          ],
          [
            258,
            169
          ],
          [
            244,
            158
          ],
          [
            236,
            145
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          8,
          2
        ],
        "feather_px": 1.25,
        "limit": "Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor left sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-02-input.png",
      "input_sha256": "b82bb104d69af90fadc8acea15602562200b709e953bee8f23fe45e928e6023f",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-02-output.png",
      "output_sha256": "b653a43fd09dc6cc1b44cb189693029067a9cb2c1faed7ff0f761db1ed01330b",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-02-mask.png",
      "mask_sha256": "028e1878fbf963cc7fbaab573f3765f324ea5f123d3c1c1bac44f32c39319a16",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            224,
            349
          ],
          [
            251,
            349
          ],
          [
            254,
            377
          ],
          [
            247,
            383
          ],
          [
            221,
            381
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -20,
          12
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor right sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-03-input.png",
      "input_sha256": "b653a43fd09dc6cc1b44cb189693029067a9cb2c1faed7ff0f761db1ed01330b",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-03-output.png",
      "output_sha256": "746d8ebb880b1065fa9565856d75d128860e677cb59ad01fd61c232a556c7712",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/03/touchup-03-mask.png",
      "mask_sha256": "b8b163cab58b1ee8c473c3e2ae60b4e56963c10db599e86b1bd2fa5cac76729e",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            288,
            300
          ],
          [
            305,
            299
          ],
          [
            310,
            348
          ],
          [
            309,
            358
          ],
          [
            289,
            364
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -12,
          9
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    }
  ],
  "raw": "godot-spike/docs/evidence/spike02-a7/attempts/03/attempt-1.png",
  "raw_sha256": "bd12428303a7261d87f675386458d187ad83fb435d6b0c7acdac6d6595c82c7d",
  "normalization": {
    "scale": 0.4082934609250399,
    "translate": [
      0,
      0
    ],
    "method": "uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif",
    "output": "godot-spike/docs/evidence/spike02-a7/attempts/03/attempt-1-normalized-preview.png",
    "sha256": "5b42110f15a85e02da12c1ef77c4e18ecf1edc38a5b9d516bc60333db193ee41"
  },
  "generated_pixels_adopted": false,
  "raw_result": "REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.",
  "runtime": "godot-spike/docs/evidence/spike02-a7/attempts/03/attempt-1-runtime.png",
  "runtime_sha256": "746d8ebb880b1065fa9565856d75d128860e677cb59ad01fd61c232a556c7712",
  "placeholder": true,
  "reason": "Anchor interior texture corrections only. Outer silhouette/drape and remaining motif fringes are not proven consistent; retain PLACEHOLDER.",
  "completed_order": 4,
  "previous_frame": "00",
  "neighbour_check": {
    "role": "consistency check ONLY, never appearance source",
    "previous_frame": "00",
    "sha256": "15de2abfa371f64128cdbf2fb8cf25175cc4ca33edd07c4c1aebe72872195c2f"
  }
}


### A7 swing/04, attempt 1

Exact attempt record (all prompts, inputs, masks, intermediate hashes, settings): `godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-1.json`.

{
  "frame": "thoma/swing/04.png",
  "attempt": 1,
  "tool": "image_gen (built-in)",
  "mode": "edit existing A6 target with two immutable anchors, not independent regeneration",
  "prompt": "Use case: identity-preserve / precise-object-edit. EDIT the FIRST image, an EXISTING swing/04 animation frame. Do NOT generate an independent new full-body pose. Images 2 and 3 are immutable appearance anchors: same elderly man, angular weathered face, close grey swept hair, short grey beard, narrow dark eyes, teal cowl and robe, ivory stole/undersleeves, brown single satchel with one cloth roll, bronze medallion. Retain the FIRST image exact canvas framing, scale, complete silhouette, pose, hands/grip, connected feet and ONE bag. Preserve its fine worn hand-painted edges and muted original colours. Make only small controlled identity and costume corrections to the first image: match the anchor face/hair features, narrow ivory stole falls and their exact small grey-green botanical sprigs, short irregular ivory fringes, cuff edge and layered continuous hem. There are TWO sprigs total, one at each stole end: a simple central stem with alternating oblique leaf strokes, about 18x31px left and 15x43px right on 512px canvas, no new motifs or trim. Short fringe tips 4-9px, approximately 10 left/8 right visible, plus ONE long waist rope, no long new tassels. Match exact anchor motif scale, not a large decorative plant. Use the anchors to restore the SAME character, not a younger/redesigned face. Repair local details while retaining all already-correct structure. 512x512 transparent canvas, pivot [256,464]. Pose intent: follow-through; mace head target [421, 376], grip [347, 324]. Keep existing A6 mace head/haft/collar/grip dimensions and orientation, single short one-handed dark iron flanged mace on worn oak haft with small brass collar. For this follow-through ONLY, lower the connected weapon hand/forearm AND mace about19px so head centre moves from [421,357] to [421,376]; keep weapon dimensions; blend the sleeve naturally. No scene, other figures, labels, cast shadow, new ornament, duplicate bag, detached footwear, geometric fragments, bright recolouring or Ferry Dusk palette. Output ONLY the edited first sprite on genuine alpha.",
  "references": [
    {
      "path": "godot-spike/docs/evidence/spike02-a7/baseline-a6/04.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/04/edit-target.png",
      "sha256": "e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0",
      "role": "EDIT TARGET: A6 structure/pose; retain feet, bag, weapon"
    },
    {
      "path": "shared-anim/thoma/idle/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/04/anchor-idle.png",
      "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "role": "APPEARANCE MASTER ONLY"
    },
    {
      "path": "shared-anim/thoma/swing/05.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/04/anchor-recover.png",
      "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
      "role": "APPEARANCE corroboration ONLY"
    }
  ],
  "spec_sha256": "bb0c9ff5949c659f35a892ad4e2b38aa28bb645fd8b4a81fbdf6f76c01ddb163",
  "base_selection": {
    "structure": "A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.",
    "face_hair": "idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.",
    "embroidery_tassels": "idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.",
    "cuffs_hem_bag_feet_weapon": "A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.",
    "a5_considered": {
      "path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/04.png",
      "sha256": "cccce1128daf423eb337a88d8dae5fe507524b448ca140d5c57bc488841c96e9",
      "reason": "01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps."
    },
    "a6_raw_considered": [
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/04/attempt-1.png",
        "sha256": "5f66d43bb64e9d4570ee2fa187bd63db14dc226d2fa6c644bab7d25e82c99108",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      }
    ]
  },
  "settings": {
    "transparent_background": true,
    "seed": "not exposed",
    "model": "not exposed",
    "quality": "not exposed",
    "requested_size": [
      512,
      512
    ],
    "returned_size": [
      1254,
      1254
    ]
  },
  "status": "FINISHED",
  "adopted": true,
  "touchups": [
    {
      "name": "anchor face/hair interior",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-01-input.png",
      "input_sha256": "e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-01-output.png",
      "output_sha256": "7609011140645d72872ebeb8c5d23b6c2526f5e1af8a44ad9e668747f661e1dd",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-01-mask.png",
      "mask_sha256": "2d07699c44eb14db411c6d287fc74c7e677ba662d78c851c53922f2f5654b81f",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            232,
            118
          ],
          [
            239,
            109
          ],
          [
            252,
            106
          ],
          [
            270,
            110
          ],
          [
            281,
            121
          ],
          [
            283,
            149
          ],
          [
            273,
            163
          ],
          [
            258,
            169
          ],
          [
            244,
            158
          ],
          [
            236,
            145
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          54,
          3
        ],
        "feather_px": 1.25,
        "limit": "Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor left sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-02-input.png",
      "input_sha256": "7609011140645d72872ebeb8c5d23b6c2526f5e1af8a44ad9e668747f661e1dd",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-02-output.png",
      "output_sha256": "bd6dcce5ef89ef9579e925d65277750e94c200bbaa88b1aeffb81757625d6403",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-02-mask.png",
      "mask_sha256": "d3884ad730300db8c94412f4267dfb2b50d52b4fa1fe2daba393e4d715a35180",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            224,
            349
          ],
          [
            251,
            349
          ],
          [
            254,
            377
          ],
          [
            247,
            383
          ],
          [
            221,
            381
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -26,
          0
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor right sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-input.png",
      "input_sha256": "bd6dcce5ef89ef9579e925d65277750e94c200bbaa88b1aeffb81757625d6403",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-output.png",
      "output_sha256": "7599d918ebeee0446071ae23251db8751e66702b1423c53df62e93dc0f81afa7",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-mask.png",
      "mask_sha256": "1df411fb83523f1515b3497d86af5537a3e31e7af6c057c2bf654b1374351bf1",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            288,
            300
          ],
          [
            305,
            299
          ],
          [
            310,
            348
          ],
          [
            309,
            358
          ],
          [
            289,
            364
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -14,
          8
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "connected follow-through hand/weapon translation",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-output.png",
      "input_sha256": "7599d918ebeee0446071ae23251db8751e66702b1423c53df62e93dc0f81afa7",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-04-output.png",
      "output_sha256": "9851d82b80b6c6cac1055896fcc173d9b3b4cc051c2b5b83cfcc078ca3d58539",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-04-mask.png",
      "mask_sha256": "b639a2d5ca7fbc8f3bf16f409cccfe07e4563e38d24460fff786a2c2fd7af4fd",
      "source": "godot-spike/docs/evidence/spike02-a7/baseline-a6/04.png",
      "source_sha256": "e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0",
      "details": {
        "polygon": [
          [
            331,
            286
          ],
          [
            354,
            297
          ],
          [
            385,
            321
          ],
          [
            444,
            344
          ],
          [
            452,
            373
          ],
          [
            427,
            388
          ],
          [
            389,
            363
          ],
          [
            352,
            331
          ],
          [
            334,
            319
          ]
        ],
        "scale": 1,
        "translate": [
          0,
          19
        ],
        "cuff_join_polygon": [
          [
            331,
            289
          ],
          [
            347,
            297
          ],
          [
            355,
            321
          ],
          [
            339,
            330
          ],
          [
            327,
            309
          ]
        ],
        "feather_px": 2
      },
      "limit": "Weapon geometry unchanged; cuff continuity must be inspected; no automatic seam PASS."
    }
  ],
  "raw": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-1.png",
  "raw_sha256": "a276781ef166cf4e4b4f2767a00450125f3fca9ed5d4aabaf21b71d13bbd187d",
  "normalization": {
    "scale": 0.4082934609250399,
    "translate": [
      0,
      0
    ],
    "method": "uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif",
    "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-1-normalized-preview.png",
    "sha256": "8a48f5212226f92e5ff086a6ec88eff6530510cd69c5238a730c40d3e62324f8"
  },
  "generated_pixels_adopted": false,
  "raw_result": "REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.",
  "runtime": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-1-runtime.png",
  "runtime_sha256": "9851d82b80b6c6cac1055896fcc173d9b3b4cc051c2b5b83cfcc078ca3d58539",
  "placeholder": true,
  "reason": "Anchor interior texture corrections only. Outer silhouette/drape and remaining motif fringes are not proven consistent; retain PLACEHOLDER.",
  "completed_order": 5,
  "previous_frame": "03",
  "neighbour_check": {
    "role": "consistency check ONLY, never appearance source",
    "previous_frame": "03",
    "sha256": "746d8ebb880b1065fa9565856d75d128860e677cb59ad01fd61c232a556c7712"
  }
}


### A7 swing/04 attempt2 — local duplicate-weapon correction

Attempt1 runtime is REJECTED, not live. Historical record above is superseded by this attempt and a7-swing-prompts.json.

{
  "frame": "thoma/swing/04.png",
  "attempt": 2,
  "tool": "Pillow authorized targeted touch-up",
  "mode": "local correction of attempted weapon extraction, no new generation",
  "prompt": "Correct failed 04 attempt1 duplicate weapon: start from saved pre-weapon touchup03, extract ALL connected hand/weapon pixels using larger polygon, translate exactly [0,19], bridge cuff with cloth-only A6 patch. No weapon scale/rotation or new paint design.",
  "references": [
    {
      "path": "godot-spike/docs/evidence/spike02-a7/baseline-a6/04.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/04/edit-target.png",
      "sha256": "e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0",
      "role": "EDIT TARGET: A6 structure/pose; retain feet, bag, weapon"
    },
    {
      "path": "shared-anim/thoma/idle/01.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/04/anchor-idle.png",
      "sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "role": "APPEARANCE MASTER ONLY"
    },
    {
      "path": "shared-anim/thoma/swing/05.png",
      "input_copy": "godot-spike/docs/evidence/spike02-a7/attempts/04/anchor-recover.png",
      "sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
      "role": "APPEARANCE corroboration ONLY"
    },
    {
      "path": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-output.png",
      "sha256": "7599d918ebeee0446071ae23251db8751e66702b1423c53df62e93dc0f81afa7",
      "role": "pre-weapon A7 touchup source"
    }
  ],
  "spec_sha256": "bb0c9ff5949c659f35a892ad4e2b38aa28bb645fd8b4a81fbdf6f76c01ddb163",
  "base_selection": {
    "structure": "A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.",
    "face_hair": "idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.",
    "embroidery_tassels": "idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.",
    "cuffs_hem_bag_feet_weapon": "A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.",
    "a5_considered": {
      "path": "godot-spike/docs/evidence/spike02-a6/baseline-a5/04.png",
      "sha256": "cccce1128daf423eb337a88d8dae5fe507524b448ca140d5c57bc488841c96e9",
      "reason": "01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps."
    },
    "a6_raw_considered": [
      {
        "path": "godot-spike/docs/evidence/spike02-a6/candidates/04/attempt-1.png",
        "sha256": "5f66d43bb64e9d4570ee2fa187bd63db14dc226d2fa6c644bab7d25e82c99108",
        "reason": "Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole."
      }
    ]
  },
  "settings": {
    "seed": "not applicable; deterministic",
    "model": "not applicable",
    "transparent_background": true,
    "canvas": [
      512,
      512
    ]
  },
  "status": "FINISHED",
  "adopted": true,
  "touchups": [
    {
      "name": "anchor face/hair interior",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-01-input.png",
      "input_sha256": "e4e661e76e29d52754971a68f7d879b4a68a7b0d0750b52e66ceb164a88961c0",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-01-output.png",
      "output_sha256": "7609011140645d72872ebeb8c5d23b6c2526f5e1af8a44ad9e668747f661e1dd",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-01-mask.png",
      "mask_sha256": "2d07699c44eb14db411c6d287fc74c7e677ba662d78c851c53922f2f5654b81f",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            232,
            118
          ],
          [
            239,
            109
          ],
          [
            252,
            106
          ],
          [
            270,
            110
          ],
          [
            281,
            121
          ],
          [
            283,
            149
          ],
          [
            273,
            163
          ],
          [
            258,
            169
          ],
          [
            244,
            158
          ],
          [
            236,
            145
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          54,
          3
        ],
        "feather_px": 1.25,
        "limit": "Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor left sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-02-input.png",
      "input_sha256": "7609011140645d72872ebeb8c5d23b6c2526f5e1af8a44ad9e668747f661e1dd",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-02-output.png",
      "output_sha256": "bd6dcce5ef89ef9579e925d65277750e94c200bbaa88b1aeffb81757625d6403",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-02-mask.png",
      "mask_sha256": "d3884ad730300db8c94412f4267dfb2b50d52b4fa1fe2daba393e4d715a35180",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            224,
            349
          ],
          [
            251,
            349
          ],
          [
            254,
            377
          ],
          [
            247,
            383
          ],
          [
            221,
            381
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -26,
          0
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "anchor right sprig/fringe",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-input.png",
      "input_sha256": "bd6dcce5ef89ef9579e925d65277750e94c200bbaa88b1aeffb81757625d6403",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-output.png",
      "output_sha256": "7599d918ebeee0446071ae23251db8751e66702b1423c53df62e93dc0f81afa7",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-mask.png",
      "mask_sha256": "1df411fb83523f1515b3497d86af5537a3e31e7af6c057c2bf654b1374351bf1",
      "source": "shared-anim/thoma/idle/01.png",
      "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
      "details": {
        "source_polygon": [
          [
            288,
            300
          ],
          [
            305,
            299
          ],
          [
            310,
            348
          ],
          [
            309,
            358
          ],
          [
            289,
            364
          ]
        ],
        "uniform_scale": 1,
        "translate": [
          -14,
          8
        ],
        "feather_px": 1.2,
        "limit": "Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred."
      },
      "alpha_policy": "A6 silhouette alpha retained exactly; inward blend; no body/limb warping"
    },
    {
      "name": "corrected complete connected weapon translation",
      "input": "godot-spike/docs/evidence/spike02-a7/attempts/04/touchup-03-output.png",
      "input_sha256": "7599d918ebeee0446071ae23251db8751e66702b1423c53df62e93dc0f81afa7",
      "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-2.png",
      "output_sha256": "9f2c7c110199648b853b7e1e472d6c4425e5fc4dbaa3cafdc15845d15d7e86cc",
      "mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-2-weapon-mask.png",
      "mask_sha256": "9aebc4d7ddc334d89fac87b865d9d9bf813c0b7d963eaa0c48d520390c479741",
      "join_mask": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-2-join-mask.png",
      "join_mask_sha256": "b66b5786cc4ea07e9abf4e24cac3b1afb0459ce2f902b812b64a296fceb15c1f",
      "details": {
        "source_polygon": [
          [
            324,
            280
          ],
          [
            358,
            291
          ],
          [
            461,
            335
          ],
          [
            466,
            404
          ],
          [
            391,
            405
          ],
          [
            345,
            350
          ],
          [
            326,
            331
          ]
        ],
        "translate": [
          0,
          19
        ],
        "scale": 1,
        "cuff_cloth_translate": [
          14,
          24
        ],
        "cuff_polygon": [
          [
            318,
            282
          ],
          [
            331,
            285
          ],
          [
            342,
            300
          ],
          [
            333,
            311
          ],
          [
            318,
            298
          ]
        ],
        "feather_px": 1.5
      }
    }
  ],
  "raw": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-2.png",
  "raw_sha256": "9f2c7c110199648b853b7e1e472d6c4425e5fc4dbaa3cafdc15845d15d7e86cc",
  "normalization": {
    "scale": 0.4082934609250399,
    "translate": [
      0,
      0
    ],
    "method": "uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif",
    "output": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-1-normalized-preview.png",
    "sha256": "8a48f5212226f92e5ff086a6ec88eff6530510cd69c5238a730c40d3e62324f8"
  },
  "generated_pixels_adopted": false,
  "raw_result": "REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.",
  "runtime": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-2.png",
  "runtime_sha256": "9f2c7c110199648b853b7e1e472d6c4425e5fc4dbaa3cafdc15845d15d7e86cc",
  "placeholder": true,
  "reason": "Single mace restored and 04 head lowered19px. Cloth bridge/face/stole continuity remains unproven: PLACEHOLDER.",
  "completed_order": 5,
  "previous_frame": "03",
  "neighbour_check": {
    "role": "consistency check ONLY, never appearance source",
    "previous_frame": "03",
    "sha256": "746d8ebb880b1065fa9565856d75d128860e677cb59ad01fd61c232a556c7712"
  },
  "origin_imagegen_raw": "godot-spike/docs/evidence/spike02-a7/attempts/04/attempt-1.png",
  "origin_imagegen_raw_sha256": "a276781ef166cf4e4b4f2767a00450125f3fca9ed5d4aabaf21b71d13bbd187d"
}


## spike-02 A8 — brief-driven shared sheet

Built-in image_gen EDIT, three whole-sheet attempts; attempt3 adopted for all five frames. No per-frame generation/fallback. Full prompts, input/reference/mask SHA-256, raw/runtime hashes, tool settings (seed/model not exposed), slice transforms and local weapon fix input/output/mask/donor hashes: `a8-swing-prompts.json`. Raw sheets are immutable under `godot-spike/docs/evidence/spike02-a8/sheet-attempts/`. The tool has no explicit mask argument; supporting mask + prompt requested fixed endpoints, but it repainted them. Runtime endpoints remain original byte-identical files. All five remain PLACEHOLDER pending the full13-item audit.
{
  "sheet_attempts": [
    {
      "attempt": 1,
      "tool": "image_gen (built-in)",
      "mode": "edit one shared seven-panel sheet",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n",
      "prompt_path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-1.prompt.txt",
      "prompt_sha256": "864580b5ce064f4cc991c95dd943a0a526c30bbd3f597830faa3aabf4504b94d",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-canvas.png",
          "sha256": "e58a487b69ab5d3ecf283754a4b9c63fa7084fc25493ab1261d61ebdc7fd2454"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "adjustment": "Initial brief scaffold",
      "fallback": false,
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-1.png",
      "raw_sha256": "213edfabc234ff72f163d87912a0c09c767763aec401e2b92c735629a0921987",
      "returned_size": [
        1774,
        887
      ]
    },
    {
      "attempt": 2,
      "tool": "image_gen (built-in)",
      "mode": "edit one shared seven-panel sheet",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt2 correction: same design and painting across ALL five frames remains first priority. The middle cells now contain FAINT FLAT SILHOUETTES ONLY, no face or costume texture. Follow their exact arm/leg placement and the joint guide; use the two fixed ANCHOR figures for every surface detail. Do not reframe, enlarge the figures or fill the cell. Keep head top at103 and foot line464 in each512px cell. In panel4 (02) the mace is ABOVE and RIGHT at449,110, not horizontally in front of the chest. In panel6 (04) mace is DOWN at421,376, not at waist level. Do not make the mace bigger than the anchor. Keep the two fixed panel figures their original360px height and keep all seven heads the same size. Return the original2048x1024 grid including empty margins.\n",
      "prompt_path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2.prompt.txt",
      "prompt_sha256": "acad09bfb8d043a84efc6a66635bd18929c3e3c538cffbca7c90cf48f2533cc4",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "adjustment": "22% flat A7 alpha silhouette for pose only; prompt corrects reframe and02/04 arc",
      "fallback": false,
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2.png",
      "raw_sha256": "18cc6a23c4df0c55d60310c2319e32801f1474a395bbc66e412a63e4ea19e319",
      "returned_size": [
        1774,
        887
      ]
    },
    {
      "attempt": 3,
      "tool": "image_gen (built-in)",
      "mode": "edit one shared seven-panel sheet",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
      "prompt_path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.prompt.txt",
      "prompt_sha256": "209089ccb7dcc9a44223383560af984ece91c4e753b2c0839bf9b8c8c4ab1374",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "adjustment": "Same pose scaffold; prompt prioritizes anchor-scale narrow stole, tiny sprigs, uneven short fringe and hair/beard",
      "fallback": false,
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
      "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
      "returned_size": [
        1774,
        887
      ]
    }
  ],
  "frames": [
    {
      "frame": "thoma/swing/00.png",
      "adopted": true,
      "sheet_attempt": 3,
      "fallback": false,
      "tool": "image_gen (built-in)",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
      "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
      "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-runtime.png",
      "runtime_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
      "slice": {
        "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
        "uniform_sheet_scale": 1.1544532130777903,
        "panel": 2
      },
      "normalization": {
        "scale": 0.8534278959810875,
        "translate": [
          34.6950354609929,
          32.16548463356975
        ],
        "head_top_before": 83,
        "lowest_opaque_before": 506,
        "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
      },
      "local_fixes": [
        {
          "scope": "exposed mace only; hand/forearm/body kept",
          "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-normalized.png",
          "input_sha256": "69cb6531aa91d42d7b488b7a070ecd8e28419fdc0021ed61d5f7a3c8272ce40b",
          "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-runtime.png",
          "output_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
          "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-weapon-fix-mask.png",
          "mask_sha256": "945cf083e8cf210d1b1060c51bfea259e387577c6a5af2b7ebaa1ac84ca9dd5c",
          "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
          "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
          "source": "shared-anim/thoma/idle/01.png",
          "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
          "before_mace_head": [
            219.88888888888889,
            73.13002364066195
          ],
          "target": [
            192,
            85
          ],
          "measured_head_alpha_centroid": [
            191.589,
            84.551
          ],
          "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
          "head_output_position": [
            166,
            58
          ],
          "head_rotation_degrees": 66.04965718662262,
          "grip": [
            150.7612293144208,
            109.8274231678487
          ]
        }
      ],
      "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
      "placeholder": true
    },
    {
      "frame": "thoma/swing/01.png",
      "adopted": true,
      "sheet_attempt": 3,
      "fallback": false,
      "tool": "image_gen (built-in)",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
      "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
      "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-runtime.png",
      "runtime_sha256": "790e174e38b830d08c668275870b0926c8ddd3fb33230195df352134c6b75a98",
      "slice": {
        "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
        "uniform_sheet_scale": 1.1544532130777903,
        "panel": 3
      },
      "normalization": {
        "scale": 0.8574821852731591,
        "translate": [
          30.194774346793366,
          30.114014251781498
        ],
        "head_top_before": 85,
        "lowest_opaque_before": 506,
        "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
      },
      "local_fixes": [
        {
          "scope": "exposed mace only; hand/forearm/body kept",
          "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-normalized.png",
          "input_sha256": "30688b133ee5874a532525c9789a016dd1f8e78078235074ddc0ee78288d2039",
          "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-runtime.png",
          "output_sha256": "790e174e38b830d08c668275870b0926c8ddd3fb33230195df352134c6b75a98",
          "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-weapon-fix-mask.png",
          "mask_sha256": "7aae43f20c56d6d34626cb7bf581bc75fc1e9ca58c261180912de1fabd93eeb8",
          "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
          "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
          "source": "shared-anim/thoma/idle/01.png",
          "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
          "before_mace_head": [
            305.44655581947745,
            57.55344418052259
          ],
          "target": [
            259,
            87
          ],
          "measured_head_alpha_centroid": [
            259.195,
            87.447
          ],
          "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
          "head_output_position": [
            236,
            63
          ],
          "head_rotation_degrees": 15.073392916764721,
          "grip": [
            217.9833729216152,
            72.1306413301663
          ]
        }
      ],
      "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
      "placeholder": true
    },
    {
      "frame": "thoma/swing/02.png",
      "adopted": true,
      "sheet_attempt": 3,
      "fallback": false,
      "tool": "image_gen (built-in)",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
      "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
      "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-runtime.png",
      "runtime_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
      "slice": {
        "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
        "uniform_sheet_scale": 1.1544532130777903,
        "panel": 4
      },
      "normalization": {
        "scale": 0.8957816377171216,
        "translate": [
          1.6203473945409428,
          10.734491315136495
        ],
        "head_top_before": 103,
        "lowest_opaque_before": 506,
        "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
      },
      "local_fixes": [
        {
          "scope": "exposed mace only; hand/forearm/body kept",
          "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-normalized.png",
          "input_sha256": "f1b97491f774bf30188961e36c57d5c7dab129ea1ce6dccdc296b4db2d9fe2f8",
          "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-runtime.png",
          "output_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
          "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-weapon-fix-mask.png",
          "mask_sha256": "6fe713466170c4244158f46ce6639d2392143eaf96eed3f1646c86aaa1e4c3b5",
          "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
          "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
          "source": "shared-anim/thoma/idle/01.png",
          "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
          "before_mace_head": [
            421.741935483871,
            103.00000000000001
          ],
          "target": [
            449,
            110
          ],
          "measured_head_alpha_centroid": [
            448.731,
            110.486
          ],
          "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
          "head_output_position": [
            425,
            85
          ],
          "head_rotation_degrees": 73.246468394085,
          "grip": [
            376.0570719602978,
            167.4962779156328
          ]
        }
      ],
      "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
      "placeholder": true
    },
    {
      "frame": "thoma/swing/03.png",
      "adopted": true,
      "sheet_attempt": 3,
      "fallback": false,
      "tool": "image_gen (built-in)",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
      "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
      "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-runtime.png",
      "runtime_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
      "slice": {
        "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
        "uniform_sheet_scale": 1.1544532130777903,
        "panel": 5
      },
      "normalization": {
        "scale": 0.9280205655526992,
        "translate": [
          -7.910025706940871,
          38.038560411311096
        ],
        "head_top_before": 70,
        "lowest_opaque_before": 459,
        "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
      },
      "local_fixes": [
        {
          "scope": "exposed mace only; hand/forearm/body kept",
          "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-normalized.png",
          "input_sha256": "98e4e29f3d67d803c7d8e43071e9950b56ef64aad1ea28ceeeccd98a2ac637fa",
          "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-runtime.png",
          "output_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
          "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-weapon-fix-mask.png",
          "mask_sha256": "53311b79dd09cc38cb8f45a69b3149f7ca0010829f9e742c4efe8a4d09d111e4",
          "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
          "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
          "source": "shared-anim/thoma/idle/01.png",
          "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
          "before_mace_head": [
            445.89203084832906,
            178.16966580976867
          ],
          "target": [
            455,
            196
          ],
          "measured_head_alpha_centroid": [
            455.43,
            195.552
          ],
          "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
          "head_output_position": [
            430,
            169
          ],
          "head_rotation_degrees": 27.14814409100297,
          "grip": [
            366.0822622107969,
            183.73778920308487
          ]
        }
      ],
      "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
      "placeholder": true
    },
    {
      "frame": "thoma/swing/04.png",
      "adopted": true,
      "sheet_attempt": 3,
      "fallback": false,
      "tool": "image_gen (built-in)",
      "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
      "inputs": [
        {
          "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
          "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
          "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
          "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
        },
        {
          "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
          "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
        }
      ],
      "settings": {
        "transparent_background": true,
        "seed": "not exposed",
        "model": "not exposed",
        "quality": "not exposed",
        "mask_parameter": "not exposed; supplied as supporting image + prompt only"
      },
      "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
      "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
      "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-runtime.png",
      "runtime_sha256": "afff39a5272b2f187b86128edc191714c26b7b784191b21ded0a70f854bb5a91",
      "slice": {
        "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
        "uniform_sheet_scale": 1.1544532130777903,
        "panel": 6
      },
      "normalization": {
        "scale": 0.9425587467362925,
        "translate": [
          4.61096605744126,
          33.25065274151433
        ],
        "head_top_before": 74,
        "lowest_opaque_before": 457,
        "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
      },
      "local_fixes": [
        {
          "scope": "exposed mace only; hand/forearm/body kept",
          "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-normalized.png",
          "input_sha256": "7235a01e4f7600e4dd2238d51b7ae5f2988ebaedaf930d649ae7a88630fd1021",
          "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-runtime.png",
          "output_sha256": "afff39a5272b2f187b86128edc191714c26b7b784191b21ded0a70f854bb5a91",
          "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-weapon-fix-mask.png",
          "mask_sha256": "d66894e6dd5e487abd8eaa9f577c6a34d634c6970f6f5d949627a6efc889bb89",
          "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
          "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
          "source": "shared-anim/thoma/idle/01.png",
          "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
          "before_mace_head": [
            456.0966057441253,
            369.74412532637075
          ],
          "target": [
            421,
            376
          ],
          "measured_head_alpha_centroid": [
            421.46,
            375.635
          ],
          "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
          "head_output_position": [
            398,
            351
          ],
          "head_rotation_degrees": -19.209410709025114,
          "grip": [
            375.0365535248042,
            312.2480417754569
          ]
        }
      ],
      "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
      "placeholder": true
    }
  ]
}

### A8 W2 final local cleanup revision

First local normalization retained old shaft slivers on01 and04. Original runtime and masks preserved. Final local erasure masks and input/output hashes follow; no further imagegen or body changes. The live final hashes in a8-swing-prompts.json supersede the first W2 runtime entries above.
[
  {
    "frame": "thoma/swing/00.png",
    "adopted": true,
    "sheet_attempt": 3,
    "fallback": false,
    "tool": "image_gen (built-in)",
    "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
    "inputs": [
      {
        "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
        "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
        "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
        "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
        "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
      }
    ],
    "settings": {
      "transparent_background": true,
      "seed": "not exposed",
      "model": "not exposed",
      "quality": "not exposed",
      "mask_parameter": "not exposed; supplied as supporting image + prompt only"
    },
    "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
    "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
    "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-runtime.png",
    "runtime_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "slice": {
      "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
      "uniform_sheet_scale": 1.1544532130777903,
      "panel": 2
    },
    "normalization": {
      "scale": 0.8534278959810875,
      "translate": [
        34.6950354609929,
        32.16548463356975
      ],
      "head_top_before": 83,
      "lowest_opaque_before": 506,
      "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
    },
    "local_fixes": [
      {
        "scope": "exposed mace only; hand/forearm/body kept",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-normalized.png",
        "input_sha256": "69cb6531aa91d42d7b488b7a070ecd8e28419fdc0021ed61d5f7a3c8272ce40b",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-runtime.png",
        "output_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/00-weapon-fix-mask.png",
        "mask_sha256": "945cf083e8cf210d1b1060c51bfea259e387577c6a5af2b7ebaa1ac84ca9dd5c",
        "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
        "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
        "source": "shared-anim/thoma/idle/01.png",
        "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
        "before_mace_head": [
          219.88888888888889,
          73.13002364066195
        ],
        "target": [
          192,
          85
        ],
        "measured_head_alpha_centroid": [
          191.589,
          84.551
        ],
        "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
        "head_output_position": [
          166,
          58
        ],
        "head_rotation_degrees": 66.04965718662262,
        "grip": [
          150.7612293144208,
          109.8274231678487
        ]
      }
    ],
    "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
    "placeholder": true
  },
  {
    "frame": "thoma/swing/01.png",
    "adopted": true,
    "sheet_attempt": 3,
    "fallback": false,
    "tool": "image_gen (built-in)",
    "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
    "inputs": [
      {
        "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
        "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
        "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
        "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
        "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
      }
    ],
    "settings": {
      "transparent_background": true,
      "seed": "not exposed",
      "model": "not exposed",
      "quality": "not exposed",
      "mask_parameter": "not exposed; supplied as supporting image + prompt only"
    },
    "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
    "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
    "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-runtime-2.png",
    "runtime_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "slice": {
      "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
      "uniform_sheet_scale": 1.1544532130777903,
      "panel": 3
    },
    "normalization": {
      "scale": 0.8574821852731591,
      "translate": [
        30.194774346793366,
        30.114014251781498
      ],
      "head_top_before": 85,
      "lowest_opaque_before": 506,
      "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
    },
    "local_fixes": [
      {
        "scope": "exposed mace only; hand/forearm/body kept",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-normalized.png",
        "input_sha256": "30688b133ee5874a532525c9789a016dd1f8e78078235074ddc0ee78288d2039",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-runtime.png",
        "output_sha256": "790e174e38b830d08c668275870b0926c8ddd3fb33230195df352134c6b75a98",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-weapon-fix-mask.png",
        "mask_sha256": "7aae43f20c56d6d34626cb7bf581bc75fc1e9ca58c261180912de1fabd93eeb8",
        "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
        "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
        "source": "shared-anim/thoma/idle/01.png",
        "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
        "before_mace_head": [
          305.44655581947745,
          57.55344418052259
        ],
        "target": [
          259,
          87
        ],
        "measured_head_alpha_centroid": [
          259.195,
          87.447
        ],
        "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
        "head_output_position": [
          236,
          63
        ],
        "head_rotation_degrees": 15.073392916764721,
        "grip": [
          217.9833729216152,
          72.1306413301663
        ]
      },
      {
        "scope": "old exposed mace shaft residual ONLY",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-runtime.png",
        "input_sha256": "790e174e38b830d08c668275870b0926c8ddd3fb33230195df352134c6b75a98",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-runtime-2.png",
        "output_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/01-residual-cleanup-mask.png",
        "mask_sha256": "eeb9acea16786a1a309d07aa9d7e3e762f8647513737c0ea057764f1803e2034",
        "description": "1x inspection found small remnant of superseded shaft outside first mask; erase exact residual polygon without changing body/head/hand/new mace."
      }
    ],
    "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
    "placeholder": true
  },
  {
    "frame": "thoma/swing/02.png",
    "adopted": true,
    "sheet_attempt": 3,
    "fallback": false,
    "tool": "image_gen (built-in)",
    "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
    "inputs": [
      {
        "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
        "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
        "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
        "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
        "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
      }
    ],
    "settings": {
      "transparent_background": true,
      "seed": "not exposed",
      "model": "not exposed",
      "quality": "not exposed",
      "mask_parameter": "not exposed; supplied as supporting image + prompt only"
    },
    "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
    "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
    "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-runtime.png",
    "runtime_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "slice": {
      "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
      "uniform_sheet_scale": 1.1544532130777903,
      "panel": 4
    },
    "normalization": {
      "scale": 0.8957816377171216,
      "translate": [
        1.6203473945409428,
        10.734491315136495
      ],
      "head_top_before": 103,
      "lowest_opaque_before": 506,
      "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
    },
    "local_fixes": [
      {
        "scope": "exposed mace only; hand/forearm/body kept",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-normalized.png",
        "input_sha256": "f1b97491f774bf30188961e36c57d5c7dab129ea1ce6dccdc296b4db2d9fe2f8",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-runtime.png",
        "output_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/02-weapon-fix-mask.png",
        "mask_sha256": "6fe713466170c4244158f46ce6639d2392143eaf96eed3f1646c86aaa1e4c3b5",
        "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
        "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
        "source": "shared-anim/thoma/idle/01.png",
        "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
        "before_mace_head": [
          421.741935483871,
          103.00000000000001
        ],
        "target": [
          449,
          110
        ],
        "measured_head_alpha_centroid": [
          448.731,
          110.486
        ],
        "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
        "head_output_position": [
          425,
          85
        ],
        "head_rotation_degrees": 73.246468394085,
        "grip": [
          376.0570719602978,
          167.4962779156328
        ]
      }
    ],
    "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
    "placeholder": true
  },
  {
    "frame": "thoma/swing/03.png",
    "adopted": true,
    "sheet_attempt": 3,
    "fallback": false,
    "tool": "image_gen (built-in)",
    "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
    "inputs": [
      {
        "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
        "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
        "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
        "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
        "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
      }
    ],
    "settings": {
      "transparent_background": true,
      "seed": "not exposed",
      "model": "not exposed",
      "quality": "not exposed",
      "mask_parameter": "not exposed; supplied as supporting image + prompt only"
    },
    "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
    "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
    "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-runtime.png",
    "runtime_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "slice": {
      "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
      "uniform_sheet_scale": 1.1544532130777903,
      "panel": 5
    },
    "normalization": {
      "scale": 0.9280205655526992,
      "translate": [
        -7.910025706940871,
        38.038560411311096
      ],
      "head_top_before": 70,
      "lowest_opaque_before": 459,
      "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
    },
    "local_fixes": [
      {
        "scope": "exposed mace only; hand/forearm/body kept",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-normalized.png",
        "input_sha256": "98e4e29f3d67d803c7d8e43071e9950b56ef64aad1ea28ceeeccd98a2ac637fa",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-runtime.png",
        "output_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/03-weapon-fix-mask.png",
        "mask_sha256": "53311b79dd09cc38cb8f45a69b3149f7ca0010829f9e742c4efe8a4d09d111e4",
        "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
        "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
        "source": "shared-anim/thoma/idle/01.png",
        "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
        "before_mace_head": [
          445.89203084832906,
          178.16966580976867
        ],
        "target": [
          455,
          196
        ],
        "measured_head_alpha_centroid": [
          455.43,
          195.552
        ],
        "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
        "head_output_position": [
          430,
          169
        ],
        "head_rotation_degrees": 27.14814409100297,
        "grip": [
          366.0822622107969,
          183.73778920308487
        ]
      }
    ],
    "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
    "placeholder": true
  },
  {
    "frame": "thoma/swing/04.png",
    "adopted": true,
    "sheet_attempt": 3,
    "fallback": false,
    "tool": "image_gen (built-in)",
    "prompt": "Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.\nPanel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.\nLocal cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.\nSame elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.\nApproved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.\nMatch the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.\n\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n",
    "inputs": [
      {
        "path": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-2-canvas.png",
        "sha256": "7275b08482de93edec2057d2410ff5cb4aa14bc98a8208ae84ad48c08b226628"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-mask.png",
        "sha256": "5322f385d5e1b7cdace3649a5b22d54e1d0e87046f6c84553817f97147b26201"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/anchors-2x.png",
        "sha256": "fa1eea52c8367f2b36f5ac7fc0c271991fe725d30129658c383f9d1fdb48a603"
      },
      {
        "path": "godot-spike/docs/evidence/spike02-a8/inputs/spec-crops.png",
        "sha256": "90cbfe6c72fddc924283aeadd0b4f7c4fe2ba5f345de157b556337eaed431599"
      }
    ],
    "settings": {
      "transparent_background": true,
      "seed": "not exposed",
      "model": "not exposed",
      "quality": "not exposed",
      "mask_parameter": "not exposed; supplied as supporting image + prompt only"
    },
    "raw": "godot-spike/docs/evidence/spike02-a8/sheet-attempts/attempt-3.png",
    "raw_sha256": "5ba4a3fd04b9a87378d0978fe38737e5a9c5557ae1b7cec88fbfd33836755c18",
    "runtime": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-runtime-2.png",
    "runtime_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "slice": {
      "layout": "godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json",
      "uniform_sheet_scale": 1.1544532130777903,
      "panel": 6
    },
    "normalization": {
      "scale": 0.9425587467362925,
      "translate": [
        4.61096605744126,
        33.25065274151433
      ],
      "head_top_before": 74,
      "lowest_opaque_before": 457,
      "method": "uniform scale and translation ONLY; alpha cleanup, no body warping"
    },
    "local_fixes": [
      {
        "scope": "exposed mace only; hand/forearm/body kept",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-normalized.png",
        "input_sha256": "7235a01e4f7600e4dd2238d51b7ae5f2988ebaedaf930d649ae7a88630fd1021",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-runtime.png",
        "output_sha256": "afff39a5272b2f187b86128edc191714c26b7b784191b21ded0a70f854bb5a91",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-weapon-fix-mask.png",
        "mask_sha256": "d66894e6dd5e487abd8eaa9f577c6a34d634c6970f6f5d949627a6efc889bb89",
        "donor": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/mace-head-donor.png",
        "donor_sha256": "6b26f6139583cc3dff6b11f6b32b16c71bb22e0823638342c97f2480c53c35f9",
        "source": "shared-anim/thoma/idle/01.png",
        "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
        "before_mace_head": [
          456.0966057441253,
          369.74412532637075
        ],
        "target": [
          421,
          376
        ],
        "measured_head_alpha_centroid": [
          421.46,
          375.635
        ],
        "description": "Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.",
        "head_output_position": [
          398,
          351
        ],
        "head_rotation_degrees": -19.209410709025114,
        "grip": [
          375.0365535248042,
          312.2480417754569
        ]
      },
      {
        "scope": "old exposed mace shaft residual ONLY",
        "input": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-runtime.png",
        "input_sha256": "afff39a5272b2f187b86128edc191714c26b7b784191b21ded0a70f854bb5a91",
        "output": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-runtime-2.png",
        "output_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
        "mask": "godot-spike/docs/evidence/spike02-a8/normalized/attempt-3/04-residual-cleanup-mask.png",
        "mask_sha256": "fc77ab20ae40bb88df64e5b64c1e077c2d0ead094a25a7118300acb49d468890",
        "description": "1x inspection found small remnant of superseded shaft outside first mask; erase exact residual polygon without changing body/head/hand/new mace."
      }
    ],
    "alpha_policy": "Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0",
    "placeholder": true
  }
]


### spike-02 A9 targeted frame 03

A8 base; Python/Pillow manual anchor transplants, enforced region masks. No image generation, whole-frame repaint or new external material. Model regression review only; Owner approval pending. Complete operation records:

```json
[
  {
    "frame": "thoma/swing/03.png",
    "region": "head",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/03.png",
    "input_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/head-2.png",
    "output_sha256": "14b9fa2ca183db29908f1b0b30dde7b4386df26987b03f8ab9aa1e269c20e644",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/head-2-mask.png",
    "mask_sha256": "5cfd6af20ac650255aff675a7dc693f2e51dfb19568988a6ce1672a93ad208c4",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/head.png",
    "permission_mask_sha256": "4259298b65e730077e7d96a8374842c54032312756ec5e701fddd27298b24b85",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "head",
        "matrix": [
          1.0,
          -0.0,
          8.0,
          0.0,
          1.0,
          2.0
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/masks/idle-01/head.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exact donor face/hair; remove warm old crown only above ears, retain teal collar underpainting; no face repaint.",
    "changed_pixels": 3572,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 18,
      "mace_centre": [
        454.50970873786406,
        195.39320388349515
      ],
      "mace_error": 0.7801198938190365,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: identity/motif improves; protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/03.png",
    "region": "stole",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/03.png",
    "input_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/stole-1.png",
    "output_sha256": "c20b1d1c879544851b77762e471bf7906ae95e247ac45081371bfac148958601",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/stole-1-mask.png",
    "mask_sha256": "f39d37d0f6d8fad6062c145783a30eb3ea709c4a07424c18b026c85bb9411723",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/stole.png",
    "permission_mask_sha256": "05db87433c1853c4c3f12c9361d526fa0be5e194f34c41b31420e068fa1348d1",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          272,
          255,
          386
        ],
        "matrix": [
          0.9455185755993168,
          -0.3255681544571567,
          53.54327383965321,
          0.3255681544571567,
          0.9455185755993168,
          -44.14431509856081
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          266,
          313,
          366
        ],
        "matrix": [
          1.0,
          -0.0,
          -39.0,
          0.0,
          1.0,
          11.0
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 7799,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 18,
      "mace_centre": [
        454.50970873786406,
        195.39320388349515
      ],
      "mace_error": 0.7801198938190365,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/03.png",
    "region": "embroidery",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/03.png",
    "input_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/embroidery-2.png",
    "output_sha256": "282a28b2cccf509afe99e8a7bc7dbb87479d5f6d785b47d71a6a7d695cdebd8f",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/embroidery-2-mask.png",
    "mask_sha256": "0162dec9439039188d46fec4cebf68bee2daeb0d3aaaecc304eb4def5831f33b",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/embroidery.png",
    "permission_mask_sha256": "912b18e19dcbf70160f9adfe1cb0339eb786941d3223dbfad9abd32825dd8955",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          225,
          349,
          251,
          373
        ],
        "matrix": [
          0.9455185755993168,
          -0.3255681544571567,
          53.54327383965321,
          0.3255681544571567,
          0.9455185755993168,
          -44.14431509856081
        ]
      },
      {
        "part": "right",
        "source_box": [
          289,
          300,
          307,
          347
        ],
        "matrix": [
          1.0,
          -0.0,
          -39.0,
          0.0,
          1.0,
          11.0
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exclude anchor weapon occlusion and teal edge from motif crops; retain original alpha and feather1px. Larger A8 motifs may remain around patch.",
    "changed_pixels": 2014,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 18,
      "mace_centre": [
        454.50970873786406,
        195.39320388349515
      ],
      "mace_error": 0.7801198938190365,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: identity/motif improves; protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/03.png",
    "region": "tassels",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/03.png",
    "input_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/tassels-1.png",
    "output_sha256": "28b834403f7892ee55890125596614dd357987155f626e9a80ba40fbe36c5731",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/tassels-1-mask.png",
    "mask_sha256": "f906159cfd8e336ce1263f768a853d245bb182dfc39b025e99f1da1767a5cd6c",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/tassels.png",
    "permission_mask_sha256": "c95fa96f6c542268290d7467e19fd98fc72195d89c44efa2d7641ee3ad8e7634",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          369,
          255,
          386
        ],
        "matrix": [
          0.9455185755993168,
          -0.3255681544571567,
          53.54327383965321,
          0.3255681544571567,
          0.9455185755993168,
          -44.14431509856081
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          346,
          313,
          366
        ],
        "matrix": [
          1.0,
          -0.0,
          -39.0,
          0.0,
          1.0,
          11.0
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 1313,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 18,
      "mace_centre": [
        454.50970873786406,
        195.39320388349515
      ],
      "mace_error": 0.7801198938190365,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/03.png",
    "region": "mace",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/03.png",
    "input_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/mace-1.png",
    "output_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/mace-1-mask.png",
    "mask_sha256": "65795a5b91030a2a433dae510d1edf494082a9cfa1153cd94f3797759f68f257",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/mace.png",
    "permission_mask_sha256": "958bc7aeaef37be893faaaa72e965debac82dcf81c1f7d7fcb3148c060e984a6",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "matrix": [
          1,
          0,
          0,
          0,
          1,
          0
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "No pose repair prescribed for this mace; A8 target/opaque contact protected.",
    "changed_pixels": 0,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 18,
      "mace_centre": [
        454.50970873786406,
        195.39320388349515
      ],
      "mace_error": 0.7801198938190365,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No change required here; A8 pixels retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/03.png",
    "region": "legs_feet",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/03.png",
    "input_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/legs_feet-1.png",
    "output_sha256": "452b72e35d9fb4e8a93718b95f52e2a5dd38ffe1716fb1c68872e869f3bdb5fd",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/legs_feet-1-mask.png",
    "mask_sha256": "83670e5248ce63d01203ddc8dce6befcf02077bbabe644d920aeb4a1f8cf8992",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/legs_feet.png",
    "permission_mask_sha256": "220b19d6bff97894414402aaee69b2911bf020cb0e30527d2ac659873680d646",
    "source_anchor": "thoma/swing/03.png (baseline A8)",
    "source_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
    "transform": [
      {
        "part": "boot_and_lower_leg",
        "source_box": [
          29,
          404,
          111,
          467
        ],
        "matrix": [
          1,
          0,
          61,
          0,
          1,
          0
        ]
      },
      {
        "part": "boot_and_lower_leg",
        "source_box": [
          261,
          410,
          349,
          451
        ],
        "matrix": [
          1,
          0,
          35,
          0,
          1,
          3
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Translate intact boot/lower-leg pixels toward brief feet; inspect hem and leg attachment; no whole-body warp.",
    "changed_pixels": 9696,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 18,
      "mace_centre": [
        454.50970873786406,
        195.39320388349515
      ],
      "mace_error": 0.7801198938190365,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: foot translation opens a gap or abrupt hem-to-leg boundary; A8 feet/hem PASS would be lost. Keep attached A8 legs/feet, acknowledge target FAIL.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "FAIL: candidate attachment is less continuous than A8; reverted.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  }
]
```

A9 corrective regression withdrawal (supersedes prior kept motif decision):
```json
{
  "frame": "thoma/swing/03.png",
  "region": "embroidery",
  "attempt": 3,
  "input": "godot-spike/docs/evidence/spike02-a9/attempts/03/embroidery-3-input.png",
  "input_sha256": "dd8bf3801f46a071bf602c52665244dbb6ca8b521f25471202271db463ee1ad0",
  "output": "godot-spike/docs/evidence/spike02-a9/attempts/03/embroidery-3.png",
  "output_sha256": "14b9fa2ca183db29908f1b0b30dde7b4386df26987b03f8ab9aa1e269c20e644",
  "mask": "godot-spike/docs/evidence/spike02-a9/attempts/03/embroidery-2-mask.png",
  "mask_sha256": "0162dec9439039188d46fec4cebf68bee2daeb0d3aaaecc304eb4def5831f33b",
  "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/03/embroidery.png",
  "permission_mask_sha256": "912b18e19dcbf70160f9adfe1cb0339eb786941d3223dbfad9abd32825dd8955",
  "source_anchor": "baseline-a8/03.png",
  "source_sha256": "5e26004a23c014dee7a4ff0b90bf25fcd3341910355c9f91ac1ed4fd711cb3bd",
  "transform": [
    {
      "matrix": [
        1,
        0,
        0,
        0,
        1,
        0
      ]
    }
  ],
  "tool": "Python Pillow manual donor-pixel compositing",
  "prompt": null,
  "whole_frame_regeneration": false,
  "description": "Explicit regional rollback to A8 following sequential comparison; no generation.",
  "changed_pixels": 2014,
  "technical": {
    "size": [
      512,
      512
    ],
    "mode": "RGBA",
    "bottom": 464,
    "ground": 18,
    "mace_centre": [
      454.50970873786406,
      195.39320388349515
    ],
    "mace_error": 0.7801198938190365,
    "contact_opaque": true
  },
  "decision": "reverted_to_a8",
  "kept": false,
  "reason": "REGRESSION: overlapping motif patches do not improve anchor consistency. Restore exact A8 motif pixels; original candidates retained.",
  "regression_check_13": {
    "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
    "stole": "FAIL: not certified by this local operation; full W3 audit required.",
    "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
    "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
    "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
    "hem": "PASS: A8 passing feature remains intact in native candidate review.",
    "palette": "PASS: A8 passing feature remains intact in native candidate review.",
    "seams": "FAIL: not certified by this local operation; full W3 audit required.",
    "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
    "feet": "PASS: A8 passing feature remains intact in native candidate review.",
    "mace": "FAIL: not certified by this local operation; full W3 audit required.",
    "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
    "sequence": "FAIL: not certified by this local operation; full W3 audit required."
  },
  "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
}
```


### spike-02 A9 targeted frame 02

A8 base; Python/Pillow manual anchor transplants, enforced region masks. No image generation, whole-frame repaint or new external material. Model regression review only; Owner approval pending. Complete operation records:

```json
[
  {
    "frame": "thoma/swing/02.png",
    "region": "head",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/02.png",
    "input_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/02/head-2.png",
    "output_sha256": "f7c4067e4b781eb491a2b6747478c90b8df1b937aca3b714c524b471f852c5b0",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/02/head-2-mask.png",
    "mask_sha256": "40363a0bc2106fd302043aa409304111cb55d4875cbf8b3f308c926e8a317598",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/02/head.png",
    "permission_mask_sha256": "1dd534c32800fe881d10dc6de5850ab2dded427696d92fccd9758f609399a441",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "head",
        "matrix": [
          1.0,
          -0.0,
          26.0,
          0.0,
          1.0,
          7.0
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/masks/idle-01/head.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exact donor face/hair; remove warm old crown only above ears, retain teal collar underpainting; no face repaint.",
    "changed_pixels": 3762,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 15,
      "mace_centre": [
        447.3775038520801,
        111.56702619414484
      ],
      "mace_error": 2.255673922168485,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: identity/motif improves; protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/02.png",
    "region": "stole",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/02.png",
    "input_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/02/stole-1.png",
    "output_sha256": "2c0410bceff378d1973550337405516e0d5c6f6a60246c0bd93cad098527b259",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/02/stole-1-mask.png",
    "mask_sha256": "9eb07022e8873c48ec06aef4366391fb9b5e5584ce2131e0cc8b9f130319487d",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/02/stole.png",
    "permission_mask_sha256": "6d4d900782b31bbb9b1634314db8ef9b33bac09f4fe9dc771e61656126254387",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          272,
          255,
          386
        ],
        "matrix": [
          0.9781476007338057,
          -0.20791169081775934,
          50.00952126565882,
          0.20791169081775934,
          0.9781476007338057,
          -31.72538067512778
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          266,
          313,
          366
        ],
        "matrix": [
          0.9945218953682733,
          0.10452846326765347,
          -17.344753486364525,
          -0.10452846326765347,
          0.9945218953682733,
          45.825337595804285
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 5865,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 15,
      "mace_centre": [
        447.3775038520801,
        111.56702619414484
      ],
      "mace_error": 2.255673922168485,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/02.png",
    "region": "embroidery",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/02.png",
    "input_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/02/embroidery-2.png",
    "output_sha256": "a9d6f091a7d6919ceb609e5e9523fa4ba6e3f82cb485cfa2a70e26e5ca6c96fc",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/02/embroidery-2-mask.png",
    "mask_sha256": "023eb8f33ec590d27563729896e4b9e0d24c6b0fa25ade720f612f8fda615438",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/02/embroidery.png",
    "permission_mask_sha256": "912b18e19dcbf70160f9adfe1cb0339eb786941d3223dbfad9abd32825dd8955",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          225,
          349,
          251,
          373
        ],
        "matrix": [
          0.9781476007338057,
          -0.20791169081775934,
          50.00952126565882,
          0.20791169081775934,
          0.9781476007338057,
          -31.72538067512778
        ]
      },
      {
        "part": "right",
        "source_box": [
          289,
          300,
          307,
          347
        ],
        "matrix": [
          0.9945218953682733,
          0.10452846326765347,
          -17.344753486364525,
          -0.10452846326765347,
          0.9945218953682733,
          45.825337595804285
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exclude anchor weapon occlusion and teal edge from motif crops; retain original alpha and feather1px. Larger A8 motifs may remain around patch.",
    "changed_pixels": 1983,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 15,
      "mace_centre": [
        447.3775038520801,
        111.56702619414484
      ],
      "mace_error": 2.255673922168485,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No demonstrated improvement without new edge/lighting seam; A8 region retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/02.png",
    "region": "tassels",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/02.png",
    "input_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/02/tassels-1.png",
    "output_sha256": "3c6690b9f2665bf341d2ea966f5d762ec89ef4f2a21bcad89ca9a14edbe993c2",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/02/tassels-1-mask.png",
    "mask_sha256": "4ca1e32fd14527e2e4a2ef9ded30178fc905ee43a3a9bfa4ecf300a064d7274d",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/02/tassels.png",
    "permission_mask_sha256": "c95fa96f6c542268290d7467e19fd98fc72195d89c44efa2d7641ee3ad8e7634",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          369,
          255,
          386
        ],
        "matrix": [
          0.9781476007338057,
          -0.20791169081775934,
          50.00952126565882,
          0.20791169081775934,
          0.9781476007338057,
          -31.72538067512778
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          346,
          313,
          366
        ],
        "matrix": [
          0.9945218953682733,
          0.10452846326765347,
          -17.344753486364525,
          -0.10452846326765347,
          0.9945218953682733,
          45.825337595804285
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 1366,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 15,
      "mace_centre": [
        447.3775038520801,
        111.56702619414484
      ],
      "mace_error": 2.255673922168485,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/02.png",
    "region": "mace",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/02.png",
    "input_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/02/mace-1.png",
    "output_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/02/mace-1-mask.png",
    "mask_sha256": "65795a5b91030a2a433dae510d1edf494082a9cfa1153cd94f3797759f68f257",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/02/mace.png",
    "permission_mask_sha256": "2f53db4965ef3f3220e53866a2f3e152eabdb123f159ca42784b01c8cc85016c",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "matrix": [
          1,
          0,
          0,
          0,
          1,
          0
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "No pose repair prescribed for this mace; A8 target/opaque contact protected.",
    "changed_pixels": 0,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 15,
      "mace_centre": [
        447.3775038520801,
        111.56702619414484
      ],
      "mace_error": 2.255673922168485,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No change required here; A8 pixels retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/02.png",
    "region": "legs_feet",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/02.png",
    "input_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/02/legs_feet-1.png",
    "output_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/02/legs_feet-1-mask.png",
    "mask_sha256": "65795a5b91030a2a433dae510d1edf494082a9cfa1153cd94f3797759f68f257",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/02/legs_feet.png",
    "permission_mask_sha256": "220b19d6bff97894414402aaee69b2911bf020cb0e30527d2ac659873680d646",
    "source_anchor": "thoma/swing/02.png (baseline A8)",
    "source_sha256": "fdcdd0aa2ff102c70909f5e97105d6ba36f1c33bca127d9381fdca2610d5dd8c",
    "transform": [],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "No stance repair prescribed; retain A8 grounded boots.",
    "changed_pixels": 0,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 15,
      "mace_centre": [
        447.3775038520801,
        111.56702619414484
      ],
      "mace_error": 2.255673922168485,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No change required here; A8 pixels retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  }
]
```


### spike-02 A9 targeted frame 04

A8 base; Python/Pillow manual anchor transplants, enforced region masks. No image generation, whole-frame repaint or new external material. Model regression review only; Owner approval pending. Complete operation records:

```json
[
  {
    "frame": "thoma/swing/04.png",
    "region": "head",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/04.png",
    "input_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/04/head-2.png",
    "output_sha256": "4769f2a8d31f03dd9757aaf5ead37609cd025a4f4ead8b9746f6b5f1c531acdc",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/04/head-2-mask.png",
    "mask_sha256": "c3832a0addc109ec8880e3f2a0d591d87b7fbbcd2ad3952f188e62c4379cb4b1",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/04/head.png",
    "permission_mask_sha256": "64d6e83ed2dd41a44d370412696f6d9088f3ab77b6364d8a733e51cbc491e222",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "head",
        "matrix": [
          1.0,
          -0.0,
          54.0,
          0.0,
          1.0,
          3.0
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/masks/idle-01/head.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exact donor face/hair; remove warm old crown only above ears, retain teal collar underpainting; no face repaint.",
    "changed_pixels": 3640,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 8,
      "mace_centre": [
        420.49295774647885,
        374.4600938967136
      ],
      "mace_error": 1.6212349162889705,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: identity/motif improves; protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/04.png",
    "region": "stole",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/04.png",
    "input_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/04/stole-1.png",
    "output_sha256": "e63d8335515ba958609771f3eb09d5c2edbad9745d051631669977bc83e09165",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/04/stole-1-mask.png",
    "mask_sha256": "e4f254e1a3e0fa9f05a3db20bc8bd4e0179b6eaa26d9d3df41a1d4094a5fb117",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/04/stole.png",
    "permission_mask_sha256": "e4f254e1a3e0fa9f05a3db20bc8bd4e0179b6eaa26d9d3df41a1d4094a5fb117",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          272,
          255,
          386
        ],
        "matrix": [
          0.9510565162951535,
          -0.3090169943749474,
          65.3495821248598,
          0.3090169943749474,
          0.9510565162951535,
          -57.171107946017
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          266,
          313,
          366
        ],
        "matrix": [
          0.9876883405951378,
          0.15643446504023087,
          -37.18463829483093,
          -0.15643446504023087,
          0.9876883405951378,
          83.4623254235288
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 8600,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 8,
      "mace_centre": [
        420.49295774647885,
        374.4600938967136
      ],
      "mace_error": 1.6212349162889705,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/04.png",
    "region": "embroidery",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/04.png",
    "input_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/04/embroidery-2.png",
    "output_sha256": "25492b25f08db08ba6099c76b832dddb4c284059600c8971fc055801b1b11a38",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/04/embroidery-2-mask.png",
    "mask_sha256": "f8a7d6d0bfa5aa0d8a21bd3388e37f4fb20f51f3d69e70c2f06bb4583df2a8bc",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/04/embroidery.png",
    "permission_mask_sha256": "912b18e19dcbf70160f9adfe1cb0339eb786941d3223dbfad9abd32825dd8955",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          225,
          349,
          251,
          373
        ],
        "matrix": [
          0.9510565162951535,
          -0.3090169943749474,
          65.3495821248598,
          0.3090169943749474,
          0.9510565162951535,
          -57.171107946017
        ]
      },
      {
        "part": "right",
        "source_box": [
          289,
          300,
          307,
          347
        ],
        "matrix": [
          0.9876883405951378,
          0.15643446504023087,
          -37.18463829483093,
          -0.15643446504023087,
          0.9876883405951378,
          83.4623254235288
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exclude anchor weapon occlusion and teal edge from motif crops; retain original alpha and feather1px. Larger A8 motifs may remain around patch.",
    "changed_pixels": 1997,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 8,
      "mace_centre": [
        420.49295774647885,
        374.4600938967136
      ],
      "mace_error": 1.6212349162889705,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No demonstrated improvement without new edge/lighting seam; A8 region retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/04.png",
    "region": "tassels",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/04.png",
    "input_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/04/tassels-1.png",
    "output_sha256": "ebc434d26d4ba31df7e5fd0feba2f6c387f5149b51ec4e3a0fe9d2967bc94a2e",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/04/tassels-1-mask.png",
    "mask_sha256": "5499dcd245735cb839a366411d6e7eb37acac7431512a60dbb5ea05f28d890df",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/04/tassels.png",
    "permission_mask_sha256": "c95fa96f6c542268290d7467e19fd98fc72195d89c44efa2d7641ee3ad8e7634",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          369,
          255,
          386
        ],
        "matrix": [
          0.9510565162951535,
          -0.3090169943749474,
          65.3495821248598,
          0.3090169943749474,
          0.9510565162951535,
          -57.171107946017
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          346,
          313,
          366
        ],
        "matrix": [
          0.9876883405951378,
          0.15643446504023087,
          -37.18463829483093,
          -0.15643446504023087,
          0.9876883405951378,
          83.4623254235288
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 1365,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 8,
      "mace_centre": [
        420.49295774647885,
        374.4600938967136
      ],
      "mace_error": 1.6212349162889705,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/04.png",
    "region": "mace",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/04.png",
    "input_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/04/mace-1.png",
    "output_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/04/mace-1-mask.png",
    "mask_sha256": "65795a5b91030a2a433dae510d1edf494082a9cfa1153cd94f3797759f68f257",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/04/mace.png",
    "permission_mask_sha256": "eacf65ecaca34e9ec6f0dedb7148f672ce531412731fa5b8bbabe9667d5bebcf",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "matrix": [
          1,
          0,
          0,
          0,
          1,
          0
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "No pose repair prescribed for this mace; A8 target/opaque contact protected.",
    "changed_pixels": 0,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 8,
      "mace_centre": [
        420.49295774647885,
        374.4600938967136
      ],
      "mace_error": 1.6212349162889705,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No change required here; A8 pixels retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/04.png",
    "region": "legs_feet",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/04.png",
    "input_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/04/legs_feet-1.png",
    "output_sha256": "7aebb9ff3f956273afc4cf2e545a6352200f80216804a654ea07df496a0a553a",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/04/legs_feet-1-mask.png",
    "mask_sha256": "a4dc5ab453d52d329a0c5517eb2ca8744fa842c4dcbf1e758e0f55b3f43a2e4d",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/04/legs_feet.png",
    "permission_mask_sha256": "220b19d6bff97894414402aaee69b2911bf020cb0e30527d2ac659873680d646",
    "source_anchor": "thoma/swing/04.png (baseline A8)",
    "source_sha256": "c3e40e2485f31e60bd1aa1d21c8cbc452e7a359db92d2e58d6391395adc167b0",
    "transform": [
      {
        "part": "boot_and_lower_leg",
        "source_box": [
          316,
          430,
          389,
          467
        ],
        "matrix": [
          1,
          0,
          -17,
          0,
          1,
          0
        ]
      },
      {
        "part": "boot_and_lower_leg",
        "source_box": [
          55,
          405,
          134,
          467
        ],
        "matrix": [
          1,
          0,
          72,
          0,
          1,
          -9
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Translate intact boot/lower-leg pixels toward brief feet; inspect hem and leg attachment; no whole-body warp.",
    "changed_pixels": 7400,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 462,
      "ground": 0,
      "mace_centre": [
        420.49295774647885,
        374.4600938967136
      ],
      "mace_error": 1.6212349162889705,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: foot translation opens a gap or abrupt hem-to-leg boundary; A8 feet/hem PASS would be lost. Keep attached A8 legs/feet, acknowledge target FAIL.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "FAIL: candidate attachment is less continuous than A8; reverted.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  }
]
```


### spike-02 A9 targeted frame 00

A8 base; Python/Pillow manual anchor transplants, enforced region masks. No image generation, whole-frame repaint or new external material. Model regression review only; Owner approval pending. Complete operation records:

```json
[
  {
    "frame": "thoma/swing/00.png",
    "region": "head",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/00.png",
    "input_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/00/head-2.png",
    "output_sha256": "724137f816359c83fc0353c09b9a65b1a8871d6d35740c8759176f9e92d8ec4a",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/head-2-mask.png",
    "mask_sha256": "9c8e1944d708a4178b980814b16005d034fae3146213bd9dead6b3c35a68f837",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/00/head.png",
    "permission_mask_sha256": "284158923f60ab8c9e3380f6d185af2e6b647a075f58c6a467dc2408008f6e74",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "head",
        "matrix": [
          1.0,
          -0.0,
          4.0,
          0.0,
          1.0,
          5.0
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/masks/idle-01/head.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exact donor face/hair; remove warm old crown only above ears, retain teal collar underpainting; no face repaint.",
    "changed_pixels": 3570,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 13,
      "mace_centre": [
        190.41148325358853,
        85.2153110047847
      ],
      "mace_error": 1.6030421960794052,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: anchor face identity improves; collar underpainting preserved. Protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/00.png",
    "region": "stole",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/00.png",
    "input_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/00/stole-1.png",
    "output_sha256": "3523f46151f33c4779bd2fd3a39d7a73a494f36cb2d2f5baa82462013c440aad",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/stole-1-mask.png",
    "mask_sha256": "2b5a257595e3d8935e92bc0528f3a1c3f95d682eb2185addf992f27a7051187a",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/00/stole.png",
    "permission_mask_sha256": "01a1b626a071eb557c22adb41970ed4329e415ef41dc0ebc757f2d959d445897",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          272,
          255,
          386
        ],
        "matrix": [
          1.0,
          -0.0,
          1.0,
          0.0,
          1.0,
          12.0
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          266,
          313,
          366
        ],
        "matrix": [
          0.9659258262890683,
          0.25881904510252074,
          -44.99616006617255,
          -0.25881904510252074,
          0.9659258262890683,
          106.94336285150143
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 6373,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 13,
      "mace_centre": [
        190.41148325358853,
        85.2153110047847
      ],
      "mace_error": 1.6030421960794052,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/00.png",
    "region": "embroidery",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/00.png",
    "input_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/00/embroidery-2.png",
    "output_sha256": "076dd47aec1eaea57ba8c32b30254c9f635859672128f656f81d20c08bedd885",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/embroidery-2-mask.png",
    "mask_sha256": "6d332cb6b93915ac8a2d956d3d4a25557d76529301f5bf6daa81031468d86250",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/00/embroidery.png",
    "permission_mask_sha256": "912b18e19dcbf70160f9adfe1cb0339eb786941d3223dbfad9abd32825dd8955",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          225,
          349,
          251,
          373
        ],
        "matrix": [
          1.0,
          -0.0,
          1.0,
          0.0,
          1.0,
          12.0
        ]
      },
      {
        "part": "right",
        "source_box": [
          289,
          300,
          307,
          347
        ],
        "matrix": [
          0.9659258262890683,
          0.25881904510252074,
          -44.99616006617255,
          -0.25881904510252074,
          0.9659258262890683,
          106.94336285150143
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exclude anchor weapon occlusion and teal edge from motif crops; retain original alpha and feather1px. Larger A8 motifs may remain around patch.",
    "changed_pixels": 1999,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 13,
      "mace_centre": [
        190.41148325358853,
        85.2153110047847
      ],
      "mace_error": 1.6030421960794052,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION/NO IMPROVEMENT: residual A8 leaves and donor sprig overlap or show patch boundaries; two exact anchor motifs not established; preserve A8 pixels.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/00.png",
    "region": "tassels",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/00.png",
    "input_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/00/tassels-1.png",
    "output_sha256": "bfcc798dac9783e761d2dd9f74e46900d63e920add62cfbf54b08c8e7d4b4d74",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/tassels-1-mask.png",
    "mask_sha256": "df628772724f40a7942e00550866c0de761cbcb5d441521849a467a6aa362f89",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/00/tassels.png",
    "permission_mask_sha256": "c95fa96f6c542268290d7467e19fd98fc72195d89c44efa2d7641ee3ad8e7634",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          369,
          255,
          386
        ],
        "matrix": [
          1.0,
          -0.0,
          1.0,
          0.0,
          1.0,
          12.0
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          346,
          313,
          366
        ],
        "matrix": [
          0.9659258262890683,
          0.25881904510252074,
          -44.99616006617255,
          -0.25881904510252074,
          0.9659258262890683,
          106.94336285150143
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 1294,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 13,
      "mace_centre": [
        190.41148325358853,
        85.2153110047847
      ],
      "mace_error": 1.6030421960794052,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/00.png",
    "region": "mace",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/00.png",
    "input_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/00/mace-2.png",
    "output_sha256": "080b4ac4d11b1de7e0d032bb4c0311ecdd300d77bbaecf2e816881da12fba488",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/mace-2-mask.png",
    "mask_sha256": "b4f978faf7fd37b07cbb92ebd1528bc685d224f6d8c388f3dc07de58a2ab78b8",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/00/mace.png",
    "permission_mask_sha256": "5fbc4aaa1624b02339d3a08bc618f4723a5ad520944cddd7a17768fd0aa3df1b",
    "source_anchor": "thoma/swing/05.png",
    "source_sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
    "transform": [
      {
        "part": "canon_mace",
        "matrix": [
          0.3133702998751301,
          0.9496310100013431,
          -193.1087032026013,
          -0.9496310100013431,
          0.3133702998751301,
          193.41540537188115
        ],
        "scale": 1,
        "original_grip": [
          151,
          110
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/mace-2-source-mask.png",
        "source_mask_sha256": "f9ee2cf69b57171f88698f6c5f52e7d0858b7adfb3f0ab7e930784ff70b73815"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: tightly traced recover05 weapon mask excludes ivory robe/bag contamination; rigid scale1, original fingers restored, +1px centroid allowance.",
    "changed_pixels": 1050,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 13,
      "mace_centre": [
        191.29245283018867,
        85.33018867924528
      ],
      "mace_error": 0.7807993093041088,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: rigid canon head/haft size and straightness improve; original fingers/cuff retained; integration still needs W3 review. Protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/00.png",
    "region": "legs_feet",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/00.png",
    "input_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/00/legs_feet-1.png",
    "output_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/00/legs_feet-1-mask.png",
    "mask_sha256": "65795a5b91030a2a433dae510d1edf494082a9cfa1153cd94f3797759f68f257",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/00/legs_feet.png",
    "permission_mask_sha256": "220b19d6bff97894414402aaee69b2911bf020cb0e30527d2ac659873680d646",
    "source_anchor": "thoma/swing/00.png (baseline A8)",
    "source_sha256": "59eb02428446c5ed9c69d0673a3f7c41dd06163dc878f5d9f53e21fa7baae55b",
    "transform": [],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "No stance repair prescribed; retain A8 grounded boots.",
    "changed_pixels": 0,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 13,
      "mace_centre": [
        190.41148325358853,
        85.2153110047847
      ],
      "mace_error": 1.6030421960794052,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No change required here; A8 pixels retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  }
]
```


### spike-02 A9 targeted frame 01

A8 base; Python/Pillow manual anchor transplants, enforced region masks. No image generation, whole-frame repaint or new external material. Model regression review only; Owner approval pending. Complete operation records:

```json
[
  {
    "frame": "thoma/swing/01.png",
    "region": "head",
    "attempt": 3,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/01.png",
    "input_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/01/head-3.png",
    "output_sha256": "fa4e3c1365986e14699f6c496eb143bbbeb3db176a5d22f81317943b22f2359f",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/head-3-mask.png",
    "mask_sha256": "9f39fc79b26e6fd931606659d07d40ff78e18115a79b88aacaffc04ea71f0c70",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/head-3-permission-mask.png",
    "permission_mask_sha256": "6f06bebf7cdae5ea3381d35230a8138b1bd4e0f38275ef139da434308cebad60",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "matrix": [
          1.0,
          -0.0,
          4.0,
          0.0,
          1.0,
          3.0
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/masks/idle-01/head.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision3: correct underestimated old01 nose/hair mask; erase warm original head above collar and composite unchanged anchor face. Explicit revised region permission, not whole-frame edit.",
    "changed_pixels": 4851,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 12,
      "mace_centre": [
        258.69924812030075,
        85.70375939849625
      ],
      "mace_error": 1.3306732845178213,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No demonstrated improvement without new edge/lighting seam; A8 region retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/01.png",
    "region": "stole",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/01.png",
    "input_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/01/stole-1.png",
    "output_sha256": "afd4fa091f7d5ab9aee09f0ee729552b72d7cfb8f97eaabeecd1b1f58cf2f016",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/stole-1-mask.png",
    "mask_sha256": "72fcb943517c032c12f5f1ae1d05b671c779912f718d65eb53839f49a020cab8",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/01/stole.png",
    "permission_mask_sha256": "1f5069c7af7e3ff0ea9200190d76061059c073286eaac8c5d4afd8e0e9bc55bf",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          272,
          255,
          386
        ],
        "matrix": [
          1.0,
          -0.0,
          4.0,
          0.0,
          1.0,
          12.0
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          266,
          313,
          366
        ],
        "matrix": [
          0.9702957262759965,
          0.24192189559966773,
          -37.80244677386294,
          -0.24192189559966773,
          0.9702957262759965,
          100.50469195340247
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 6331,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 12,
      "mace_centre": [
        258.7473997028232,
        85.88558692421991
      ],
      "mace_error": 1.1426825515441514,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/01.png",
    "region": "embroidery",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/01.png",
    "input_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/01/embroidery-2.png",
    "output_sha256": "84ae973014a26fbc810d3390f42569a76dd771ef183c596bc9a089fb960baaf7",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/embroidery-2-mask.png",
    "mask_sha256": "f45b20b14a7f38169e94320bf07337b97bdad7d8ed01c877228530a774b8a9d8",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/01/embroidery.png",
    "permission_mask_sha256": "912b18e19dcbf70160f9adfe1cb0339eb786941d3223dbfad9abd32825dd8955",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          225,
          349,
          251,
          373
        ],
        "matrix": [
          1.0,
          -0.0,
          4.0,
          0.0,
          1.0,
          12.0
        ]
      },
      {
        "part": "right",
        "source_box": [
          289,
          300,
          307,
          347
        ],
        "matrix": [
          0.9702957262759965,
          0.24192189559966773,
          -37.80244677386294,
          -0.24192189559966773,
          0.9702957262759965,
          100.50469195340247
        ]
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: exclude anchor weapon occlusion and teal edge from motif crops; retain original alpha and feather1px. Larger A8 motifs may remain around patch.",
    "changed_pixels": 2013,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 12,
      "mace_centre": [
        258.7473997028232,
        85.88558692421991
      ],
      "mace_error": 1.1426825515441514,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION/NO IMPROVEMENT: residual A8 leaves and donor sprig overlap or show patch boundaries; two exact anchor motifs not established; preserve A8 pixels.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/01.png",
    "region": "tassels",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/01.png",
    "input_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/01/tassels-1.png",
    "output_sha256": "806386276f2bb295de0722e055c5c8d09d3661311cc387da37d95869e010fb95",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/tassels-1-mask.png",
    "mask_sha256": "802d8545ea38741c45f9e793fab5bf2e4a76e0262a40daa4b5b8ca386c44475d",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/01/tassels.png",
    "permission_mask_sha256": "c95fa96f6c542268290d7467e19fd98fc72195d89c44efa2d7641ee3ad8e7634",
    "source_anchor": "thoma/idle/01.png",
    "source_sha256": "c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808",
    "transform": [
      {
        "part": "left",
        "source_box": [
          220,
          369,
          255,
          386
        ],
        "matrix": [
          1.0,
          -0.0,
          4.0,
          0.0,
          1.0,
          12.0
        ],
        "source_anchor": "thoma/idle/01.png"
      },
      {
        "part": "right",
        "source_box": [
          285,
          346,
          313,
          366
        ],
        "matrix": [
          0.9702957262759965,
          0.24192189559966773,
          -37.80244677386294,
          -0.24192189559966773,
          0.9702957262759965,
          100.50469195340247
        ],
        "source_anchor": "thoma/idle/01.png"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Two separate rigid anchor terminal patches; test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.",
    "changed_pixels": 1247,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 12,
      "mace_centre": [
        258.7473997028232,
        85.88558692421991
      ],
      "mace_error": 1.1426825515441514,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "FAIL: candidate breaks previously continuous lower garment; reverted.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/01.png",
    "region": "mace",
    "attempt": 2,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/01.png",
    "input_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/01/mace-2.png",
    "output_sha256": "a8ef6a45e86722a5526ddf85ca03862e08b18d2f6313ead2e7a41c86b76805f6",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/mace-2-mask.png",
    "mask_sha256": "0e14ed6cd0722292198a8e1732079199c015b93670f26b4f762b3993675322b4",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/01/mace.png",
    "permission_mask_sha256": "20ad04ae39716f4f7d5bda265dcbbc4c75aad4b0dad6121123310a91e5927d4e",
    "source_anchor": "thoma/swing/05.png",
    "source_sha256": "f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf",
    "transform": [
      {
        "part": "canon_mace",
        "matrix": [
          0.8718676537854534,
          0.4897415586640047,
          -97.51042582926968,
          -0.4897415586640047,
          0.8718676537854534,
          -93.11956112848293
        ],
        "scale": 1,
        "original_grip": [
          218,
          79
        ],
        "source_mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/mace-2-source-mask.png",
        "source_mask_sha256": "f9ee2cf69b57171f88698f6c5f52e7d0858b7adfb3f0ab7e930784ff70b73815"
      }
    ],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "Revision2: tightly traced recover05 weapon mask excludes ivory robe/bag contamination; rigid scale1, original fingers restored, +1px centroid allowance.",
    "changed_pixels": 1102,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 12,
      "mace_centre": [
        259.1111111111111,
        86.61191626409018
      ],
      "mace_error": 0.4036764361342638,
      "contact_opaque": true
    },
    "decision": "kept",
    "kept": true,
    "reason": "Native-size model inspection: rigid canon head/haft size and straightness improve; original fingers/cuff retained; integration still needs W3 review. Protected A8 PASS items remain visually intact. No Owner approval.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  },
  {
    "frame": "thoma/swing/01.png",
    "region": "legs_feet",
    "attempt": 1,
    "input": "godot-spike/docs/evidence/spike02-a9/baseline-a8/01.png",
    "input_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "output": "godot-spike/docs/evidence/spike02-a9/attempts/01/legs_feet-1.png",
    "output_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "mask": "godot-spike/docs/evidence/spike02-a9/attempts/01/legs_feet-1-mask.png",
    "mask_sha256": "65795a5b91030a2a433dae510d1edf494082a9cfa1153cd94f3797759f68f257",
    "permission_mask": "godot-spike/docs/evidence/spike02-a9/masks/01/legs_feet.png",
    "permission_mask_sha256": "220b19d6bff97894414402aaee69b2911bf020cb0e30527d2ac659873680d646",
    "source_anchor": "thoma/swing/01.png (baseline A8)",
    "source_sha256": "cf37fc5b439cd639e447f4b3a3ae0b5665b2cb8923896e3f560a63067c0566d4",
    "transform": [],
    "tool": "Python Pillow manual donor-pixel compositing",
    "prompt": null,
    "whole_frame_regeneration": false,
    "description": "No stance repair prescribed; retain A8 grounded boots.",
    "changed_pixels": 0,
    "technical": {
      "size": [
        512,
        512
      ],
      "mode": "RGBA",
      "bottom": 464,
      "ground": 12,
      "mace_centre": [
        258.7473997028232,
        85.88558692421991
      ],
      "mace_error": 1.1426825515441514,
      "contact_opaque": true
    },
    "decision": "reverted_to_a8",
    "kept": false,
    "reason": "No change required here; A8 pixels retained.",
    "regression_check_13": {
      "face_hair": "FAIL: not certified by this local operation; full W3 audit required.",
      "stole": "FAIL: not certified by this local operation; full W3 audit required.",
      "embroidery": "FAIL: not certified by this local operation; full W3 audit required.",
      "tassels": "FAIL: not certified by this local operation; full W3 audit required.",
      "cuffs": "PASS: A8 passing feature remains intact in native candidate review.",
      "hem": "PASS: A8 passing feature remains intact in native candidate review.",
      "palette": "PASS: A8 passing feature remains intact in native candidate review.",
      "seams": "FAIL: not certified by this local operation; full W3 audit required.",
      "bag_count": "PASS: A8 passing feature remains intact in native candidate review.",
      "feet": "PASS: A8 passing feature remains intact in native candidate review.",
      "mace": "FAIL: not certified by this local operation; full W3 audit required.",
      "landmarks": "FAIL: not certified by this local operation; full W3 audit required.",
      "sequence": "FAIL: not certified by this local operation; full W3 audit required."
    },
    "regression_authority": "model native source comparison; A8 PASS items protected; not human approval"
  }
]
```
