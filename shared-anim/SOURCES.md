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
