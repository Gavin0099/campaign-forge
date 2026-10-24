# Thoma unified appearance spec — spike-02 A7

Anchor pixel observations and model-defined pose targets; NOT Owner art approval.

Only the two immutable PNGs below determine appearance. All numbers refer to source pixels. Manual anatomy ±2px (cloth-hidden joints ±5px); visible fringe/branch counts ±1. Crop pixels take precedence over a verbal count. No hidden design is invented.

- `shared-anim/thoma/idle/01.png` — SHA-256 `c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808`
- `shared-anim/thoma/swing/05.png` — SHA-256 `f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf`

idle/01 appearance master; recover05 corroborates brush/materials, but 10px taller head and ~7px higher right sprig are documented disagreements.

[Annotated per-item crops](../godot-spike/docs/evidence/spike02-a7/spec-crops.png) · [crop rectangles](../godot-spike/docs/evidence/spike02-a7/spec-crops.json) · [pose overlay](../godot-spike/docs/evidence/spike02-a7/pose-targets.png)

## Face

```json
{
  "shape": "Right-facing three-quarter angular long face; heavy brow, deep eye socket, projecting nose, short squared grey beard and moustache.",
  "landmarks_idle": {
    "eyes": [
      [
        263,
        137
      ],
      [
        279,
        138
      ]
    ],
    "nose_tip": [
      281,
      148
    ],
    "mouth": [
      271,
      158
    ],
    "chin": [
      264,
      170
    ],
    "ear": [
      241,
      145
    ]
  },
  "eye_brow": "Dark 1-2px eyes beneath 2-3px oblique brows; no bright round cartoon iris.",
  "mouth": "Closed, short dark horizontal mouth under pale moustache; no smile.",
  "skin_hex": {
    "skin_light": "#d5b99f",
    "skin_mid": "#9e856c",
    "skin_shadow": "#5d4f40"
  }
}
```

## Hair

```json
{
  "silhouette": "Close cropped irregular grey cap, receding at temple, swept right; small textured curls. Exposes ear; ends at nape above teal collar.",
  "bbox_idle": [
    227,
    103,
    285,
    149
  ],
  "bbox_recover": [
    222,
    93,
    280,
    140
  ],
  "parting": "No clean graphic part line resolvable; rightward brushed crown, not invented centre part.",
  "colours": {
    "hair_light": "#b29d84",
    "hair_mid": "#806b56",
    "hair_shadow": "#5b4938"
  }
}
```

## Costume (every element)

```json
{
  "robe": {
    "description": "Desaturated dark teal short outer sleeve and long divided outer skirt over ivory ankle-length underrobe; textured broad shaded folds.",
    "outer_hem_idle_y": [
      370,
      397
    ],
    "inner_hem_idle_y": [
      397,
      421
    ]
  },
  "stole": {
    "description": "Two ivory hanging panels, broad near shoulder, narrow at waist, widening toward embroidered ends; teal cowl crosses above.",
    "idle_left_width_px_at_y": {
      "185": 27,
      "225": 24,
      "362": 30
    },
    "idle_right_width_px_at_y": {
      "185": 12,
      "225": 15,
      "330": 22
    },
    "folds": "Left shoulder diagonal to waist at (235,250), left vertical fall to (237,379); right fall (286,161) to (299,357), narrow dark fold on inner edge.",
    "endpoint_choice": "idle/01 panel shapes and motif spacing; swing/05 confirms construction but right sprig/fringe sits ~7px higher."
  },
  "embroidery": {
    "description": "One muted grey-green botanical sprig on EACH ivory panel (2 total); single central stem, alternating oblique leaf strokes; pale ochre short bottom border. No repeated floral diamonds.",
    "count": 2,
    "left_bbox": [
      230,
      340,
      248,
      371
    ],
    "right_bbox": [
      291,
      302,
      306,
      345
    ],
    "visible_branch_pairs": {
      "left": 4,
      "right": 6
    },
    "count_uncertainty": "~1 branch at 512px: left upper stem obscured by mace; do not reconstruct hidden pattern.",
    "vertical_spacing_px": {
      "left": [
        4,
        6
      ],
      "right": [
        5,
        7
      ]
    },
    "motif_centre_separation_px": [
      60,
      -31
    ],
    "source_rule": "Use anchor crop pixels, not newly invented leaves. Left partial occlusion remains legitimate.",
    "colour_sample": {
      "hex": "#8d7862",
      "sample_xy": [
        300,
        329
      ],
      "source": "idle/01",
      "rgba": [
        141,
        120,
        98,
        253
      ]
    }
  },
  "tassels": {
    "description": "Short irregular pale fringe strands at each stole end, plus ONE long knotted waist cord end; fringe is not the waist cord.",
    "left_visible_tips": 10,
    "right_visible_tips": 8,
    "tip_count_uncertainty": 1,
    "left_length_px": [
      4,
      9
    ],
    "right_length_px": [
      4,
      9
    ],
    "left_attachment": [
      222,
      374,
      254,
      380
    ],
    "right_attachment": [
      288,
      347,
      310,
      357
    ],
    "waist_cord_bbox": [
      256,
      251,
      270,
      346
    ],
    "colour": "#d8c4ad",
    "rule": "Preserve sampled anchor edge, including uneven tips; no uniform extra 20px fringe."
  },
  "cuffs": {
    "description": "Ivory undersleeves flare from short teal sleeves, narrow near wrist; dark interior crease, continuous arm/hand junction.",
    "idle_weapon_side_bbox": [
      156,
      232,
      204,
      281
    ],
    "idle_free_side_bbox": [
      297,
      214,
      332,
      259
    ]
  },
  "hem": {
    "description": "Continuous ivory inner bell with several long shaded pleats beneath teal split panels; no detached triangles.",
    "idle_outline_points": [
      [
        178,
        366
      ],
      [
        173,
        391
      ],
      [
        178,
        405
      ],
      [
        194,
        414
      ],
      [
        236,
        422
      ],
      [
        269,
        417
      ],
      [
        307,
        391
      ]
    ],
    "layers": 2,
    "source_disagreement": "recover inner hem bottom ~2px lower and right shoe ~10px lower; retain idle as proportion standard, allow recover endpoint as immutable."
  },
  "bag": {
    "count": 1,
    "idle_bbox": [
      183,
      249,
      243,
      324
    ],
    "description": "One brown flap satchel at screen-left hip with a single pale rolled cloth under flap; roll is not a second pouch."
  },
  "belt": {
    "idle_bbox": [
      198,
      236,
      281,
      266
    ],
    "description": "Brown belt with pale rope knot screen-right of centre; small bronze round medallion above belt at [265,214]."
  },
  "shoes": {
    "description": "Two worn brown rounded ankle boots, dark seams and laces; both visibly join legs under inner robe.",
    "idle_left_ground": [
      201,
      462
    ],
    "idle_right_ground": [
      312,
      414
    ],
    "recover_left_ground": [
      198,
      463
    ],
    "recover_right_ground": [
      311,
      425
    ],
    "pivot_note": "[256,464] is the unchanged actor registration origin, NOT the centre of each shoe; two feet cannot both occupy one pivot."
  }
}
```

## Mace

```json
{
  "canon": "APPROVED short one-handed flanged mace; no canon edit.",
  "idle_head_bbox": [
    211,
    310,
    248,
    346
  ],
  "idle_head_centre": [
    230,
    328
  ],
  "idle_grip": [
    185,
    297
  ],
  "recover_head_centre": [
    223,
    333
  ],
  "recover_grip": [
    183,
    299
  ],
  "idle_grip_to_head_px": 54.644,
  "exposed_haft_px": 39,
  "head_size_px": [
    37,
    36
  ],
  "collar_width_px": 7,
  "grip_width_px": 17,
  "shape": "Angular dark iron flanged star head with projecting triangular fins, worn oak haft, small brass collar before head; rounded pommel.",
  "projection_limit": "Lengths are anchor projections, not a 3D length. Preserve each A6 pose weapon/grip geometry where projected length differs; no global length invention.",
  "colours": {
    "oak": "#120a06",
    "iron": "#685a48",
    "brass": "#503323"
  }
}
```

## Body proportions

```json
{
  "head_height_px": 70,
  "shoulder_width_px": 99,
  "torso_length_px": 104,
  "leg_and_skirt_to_ground_px": 204,
  "character_height_from_pivot_px": 361,
  "head_top_y": 103,
  "shoulder_y": 156,
  "hip_y": 260,
  "ground_y": 464,
  "measurement_limit": "Manual anatomical estimates +/-2px (shoulders/hips under cloth +/-5px); anchor face/hair crop is exact pixel evidence.",
  "recover_head_top_y": 93,
  "recover_character_height_px": 371,
  "policy": "idle proportions preferred; recover is immutable 10px taller, do not pretend anchors agree."
}
```

## Outline and brush

```json
{
  "description": "Thin broken dark brown/teal contour, 1-2px most boundaries and up to 3px under sleeve/bag; mottled hand-painted low-contrast highlights, no black vector edge.",
  "outline_sample": {
    "hex": "#121210",
    "sample_xy": [
      187,
      379
    ],
    "source": "idle/01",
    "rgba": [
      18,
      18,
      16,
      253
    ]
  },
  "normalization": "Uniform scale/translate only. Any anchor-region touch-up separately recorded with masks; no whole-body warp."
}
```

## Sampled palette

| Region | Hex | idle/01 pixel |
| --- | --- | --- |
| skin_light | #d5b99f | [265, 128] |
| skin_mid | #9e856c | [251, 151] |
| skin_shadow | #5d4f40 | [254, 134] |
| hair_light | #b29d84 | [253, 114] |
| hair_mid | #806b56 | [239, 116] |
| hair_shadow | #5b4938 | [242, 113] |
| teal_light | #4f635f | [183, 226] |
| teal_mid | #405350 | [178, 215] |
| teal_shadow | #2d3835 | [188, 185] |
| ivory_light | #e8d6c1 | [216, 185] |
| ivory_mid | #d8c4ad | [218, 185] |
| ivory_shadow | #c4ac92 | [215, 194] |
| embroidery | #8d7862 | [300, 329] |
| leather | #503323 | [202, 295] |
| oak | #120a06 | [202, 312] |
| iron | #685a48 | [232, 328] |
| brass | #503323 | [215, 318] |
| outline | #121210 | [187, 379] |

These are actual individual pixel samples, not uniform paint fills or a new palette. Pixel grain/shading is part of the anchor appearance.

## Pose targets and single arc

Pose targets are proposed motion controls, not measured appearance. A6 pose intent is retained. A single C1 cubic Hermite path goes through all five head targets; it is not asserted to be a rigid circular shoulder trajectory. 03 is exactly [455,196]. 04 targets [421,376], down 18.616px from A6 [420.72,357.384]. The per-frame JSON includes eyes, shoulders, elbows, hands, hips, knees, both feet, grip and head.

The actor pivot stays [256,464]. It is the registration origin; each shoe has its own source-pixel position. At least one foot meets the ground line. Recovery is the immutable endpoint and retracts the weapon. Targets are checked against actual measured results, with failures retained.

| Frame | Head centre | Weapon hand | Mace head | Feet |
| --- | --- | --- | --- | --- |
| 00 | [260, 143] | [127, 117] | [192, 85] | [145, 464] / [342, 439] |
| 01 | [260, 141] | [194, 109] | [259, 87] | [167, 464] / [326, 443] |
| 02 | [282, 145] | [372, 160] | [449, 110] | [135, 464] / [372, 448] |
| 03 | [264, 140] | [358, 196] | [455, 196] | [120, 464] / [354, 447] |
| 04 | [310, 141] | [347, 324] | [421, 376] | [165, 455] / [334, 464] |
