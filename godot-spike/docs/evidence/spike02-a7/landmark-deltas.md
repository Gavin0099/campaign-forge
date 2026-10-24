# A7 landmark deltas

Coordinates: source512px, top-left origin. Manual visible landmarks ±2px. Deltas are destination minus origin. Targets are design targets, never measured success.

| Pair | Face | Weapon hand | Free hand | Mace head | Left foot | Right foot | Height | Target-error flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01.png → 00.png | [2, 4] | [-57, -180] | [68, -16] | [-38.033, -242.77] | [-56, 1] | [39, 19] | -12.631 | hand_free delta differs from target >4px; foot_right delta differs from target >4px; character height changes >10px |
| 00.png → 01.png | [0, -1] | [66, -8] | [-105, -36] | [67.469, 2.1848] | [22, 0] | [-16, -12] | 1.6212 | hand_free delta differs from target >4px; foot_right delta differs from target >4px |
| 01.png → 02.png | [24, 2] | [178, 51] | [97, 47] | [189.131, 22.0952] | [-32, 0] | [36, 21] | -0.3616 | hand_free delta differs from target >4px; foot_right delta differs from target >4px |
| 02.png → 03.png | [-18, -4] | [-14, 36] | [-71, 11] | [6.433, 86.49] | [-15, 0] | [-29, 4] | 5.2198 | hand_free delta differs from target >4px; foot_right delta differs from target >4px |
| 03.png → 04.png | [45, 1] | [-11, 129] | [-177, -37] | [-34.28, 180.384] | [5, -7] | [-8, 18] | 1.3756 | hand_free delta differs from target >4px; foot_left delta differs from target >4px; foot_right delta differs from target >4px |
| 04.png → 05.png | [-60, -12] | [-164, -26] | [184, 31] | [-197.72, -43.384] | [73, 7] | [-23, -39] | 14.776 | hand_free delta differs from target >4px; foot_left delta differs from target >4px; character height changes >10px |

04 mace head: A6 [420.72,357.384] → A7 [420.72,376.384], target [421,376], error0.475px. The moved head/haft/grip is not rescaled. The cuff bridge still fails appearance/seam acceptance.

Full per-pair target deltas and errors, and actual visible-point picks, are in landmark-deltas.json. Body joints not visible beneath cloth cannot be measured precisely from pixels; no hidden joint PASS is claimed.
