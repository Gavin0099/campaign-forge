# A9 defects, recorded masks and measured targets

A8 baseline is byte-archived; anchors are immutable. Fix order: 03,02,04,00,01.

Anchor head centre (256,138), about60x70px, hair bbox(227,103)-(285,149), brow(258,132)-(281,136), squared beard(249,151)-(281,174). Visible manual uncertainty +/-2px; hidden joints +/-12px.
Stole widths L24-30 / R12-22px; two sprigs at L(230,340)-(248,371), R(291,302)-(306,345). Fringes10/8 +/-1; one cord. Canon head37x36px, exposed haft39px, grip-to-head~55px (recover~52.5); collar7px.
Full per-height panel edges, target joints, foot stance widths, donor regions and SHA-256 are in defects-and-targets.json. RGB/alpha donors are exact; manual picks are estimates.

## swing/00
Head [260, 143]; feet [145, 464] / [342, 439]; stance 197px; mace [192, 85].
Pose repair: replace compressed mace with rigid canon donor.

| Item | A8 regression baseline |
| --- | --- |
| face_hair | FAIL: common sheet improves similarity, but broader grey crown, softer beard/cheek and changed brow differ from anchor identity. |
| stole | FAIL: generated panels are wider and more symmetrical at the ends than the narrow asymmetric anchor stole. |
| embroidery | FAIL: two sprigs remain, but leaf scale, branch spacing and shape differ from the exact anchor motifs. |
| tassels | FAIL: dense fairly regular generated fringe does not establish10/8 uneven tips within1; long cord attachment shifts. |
| cuffs | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| hem | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| palette | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| seams | FAIL: reconstructed mace/haft joins and changed hand overlap remain visible at1x; seamless painted integration not achieved. |
| bag_count | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| feet | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| mace | FAIL: target centre and impact opacity pass, but local reconstruction changes projected shaft length and head/haft brush continuity; not canon-design acceptance. |
| landmarks | FAIL: several observed hands, elbows and feet exceed brief targets by4px; cloth-hidden knees have larger uncertainty and are not certified. |
| sequence | FAIL: face, stole ends and hem/stance still jump from anchors to sheet and between action panels; all-same-painting requirement unmet. |

Masks: [head](masks/00/head.png), [stole](masks/00/stole.png), [embroidery](masks/00/embroidery.png), [tassels](masks/00/tassels.png), [mace](masks/00/mace.png), [legs_feet](masks/00/legs_feet.png)

## swing/01
Head [260, 141]; feet [167, 464] / [326, 443]; stance 159px; mace [259, 87].
Pose repair: replace compressed mace with rigid canon donor.

| Item | A8 regression baseline |
| --- | --- |
| face_hair | FAIL: common sheet improves similarity, but broader grey crown, softer beard/cheek and changed brow differ from anchor identity. |
| stole | FAIL: generated panels are wider and more symmetrical at the ends than the narrow asymmetric anchor stole. |
| embroidery | FAIL: two sprigs remain, but leaf scale, branch spacing and shape differ from the exact anchor motifs. |
| tassels | FAIL: dense fairly regular generated fringe does not establish10/8 uneven tips within1; long cord attachment shifts. |
| cuffs | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| hem | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| palette | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| seams | FAIL: reconstructed mace/haft joins and changed hand overlap remain visible at1x; seamless painted integration not achieved. |
| bag_count | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| feet | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| mace | FAIL: target centre and impact opacity pass, but local reconstruction changes projected shaft length and head/haft brush continuity; not canon-design acceptance. |
| landmarks | FAIL: several observed hands, elbows and feet exceed brief targets by4px; cloth-hidden knees have larger uncertainty and are not certified. |
| sequence | FAIL: face, stole ends and hem/stance still jump from anchors to sheet and between action panels; all-same-painting requirement unmet. |

Masks: [head](masks/01/head.png), [stole](masks/01/stole.png), [embroidery](masks/01/embroidery.png), [tassels](masks/01/tassels.png), [mace](masks/01/mace.png), [legs_feet](masks/01/legs_feet.png)

## swing/02
Head [282, 145]; feet [135, 464] / [372, 448]; stance 237px; mace [449, 110].
Pose repair: identity/terminal cloth only.

| Item | A8 regression baseline |
| --- | --- |
| face_hair | FAIL: common sheet improves similarity, but broader grey crown, softer beard/cheek and changed brow differ from anchor identity. |
| stole | FAIL: generated panels are wider and more symmetrical at the ends than the narrow asymmetric anchor stole. |
| embroidery | FAIL: two sprigs remain, but leaf scale, branch spacing and shape differ from the exact anchor motifs. |
| tassels | FAIL: dense fairly regular generated fringe does not establish10/8 uneven tips within1; long cord attachment shifts. |
| cuffs | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| hem | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| palette | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| seams | FAIL: reconstructed mace/haft joins and changed hand overlap remain visible at1x; seamless painted integration not achieved. |
| bag_count | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| feet | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| mace | FAIL: target centre and impact opacity pass, but local reconstruction changes projected shaft length and head/haft brush continuity; not canon-design acceptance. |
| landmarks | FAIL: several observed hands, elbows and feet exceed brief targets by4px; cloth-hidden knees have larger uncertainty and are not certified. |
| sequence | FAIL: face, stole ends and hem/stance still jump from anchors to sheet and between action panels; all-same-painting requirement unmet. |

Masks: [head](masks/02/head.png), [stole](masks/02/stole.png), [embroidery](masks/02/embroidery.png), [tassels](masks/02/tassels.png), [mace](masks/02/mace.png), [legs_feet](masks/02/legs_feet.png)

## swing/03
Head [264, 140]; feet [120, 464] / [354, 447]; stance 234px; mace [455, 196].
Pose repair: narrow left stance 59 ->120, right319 ->354.

| Item | A8 regression baseline |
| --- | --- |
| face_hair | FAIL: common sheet improves similarity, but broader grey crown, softer beard/cheek and changed brow differ from anchor identity. |
| stole | FAIL: generated panels are wider and more symmetrical at the ends than the narrow asymmetric anchor stole. |
| embroidery | FAIL: two sprigs remain, but leaf scale, branch spacing and shape differ from the exact anchor motifs. |
| tassels | FAIL: dense fairly regular generated fringe does not establish10/8 uneven tips within1; long cord attachment shifts. |
| cuffs | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| hem | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| palette | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| seams | FAIL: reconstructed mace/haft joins and changed hand overlap remain visible at1x; seamless painted integration not achieved. |
| bag_count | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| feet | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| mace | FAIL: target centre and impact opacity pass, but local reconstruction changes projected shaft length and head/haft brush continuity; not canon-design acceptance. |
| landmarks | FAIL: several observed hands, elbows and feet exceed brief targets by4px; cloth-hidden knees have larger uncertainty and are not certified. |
| sequence | FAIL: face, stole ends and hem/stance still jump from anchors to sheet and between action panels; all-same-painting requirement unmet. |

Masks: [head](masks/03/head.png), [stole](masks/03/stole.png), [embroidery](masks/03/embroidery.png), [tassels](masks/03/tassels.png), [mace](masks/03/mace.png), [legs_feet](masks/03/legs_feet.png)

## swing/04
Head [310, 141]; feet [165, 455] / [334, 464]; stance 169px; mace [421, 376].
Pose repair: front foot351 ->334, rear93,464 ->165,455.

| Item | A8 regression baseline |
| --- | --- |
| face_hair | FAIL: common sheet improves similarity, but broader grey crown, softer beard/cheek and changed brow differ from anchor identity. |
| stole | FAIL: generated panels are wider and more symmetrical at the ends than the narrow asymmetric anchor stole. |
| embroidery | FAIL: two sprigs remain, but leaf scale, branch spacing and shape differ from the exact anchor motifs. |
| tassels | FAIL: dense fairly regular generated fringe does not establish10/8 uneven tips within1; long cord attachment shifts. |
| cuffs | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| hem | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| palette | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| seams | FAIL: reconstructed mace/haft joins and changed hand overlap remain visible at1x; seamless painted integration not achieved. |
| bag_count | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| feet | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| mace | FAIL: target centre and impact opacity pass, but local reconstruction changes projected shaft length and head/haft brush continuity; not canon-design acceptance. |
| landmarks | FAIL: several observed hands, elbows and feet exceed brief targets by4px; cloth-hidden knees have larger uncertainty and are not certified. |
| sequence | FAIL: face, stole ends and hem/stance still jump from anchors to sheet and between action panels; all-same-painting requirement unmet. |

Masks: [head](masks/04/head.png), [stole](masks/04/stole.png), [embroidery](masks/04/embroidery.png), [tassels](masks/04/tassels.png), [mace](masks/04/mace.png), [legs_feet](masks/04/legs_feet.png)

