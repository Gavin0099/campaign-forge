# P1v3 visual style — playable L03 only

This is a presentation proposal, not final story or Owner art approval. The
visual thesis is a painted river crossing on a raised tactical board, framed
by dark field equipment and aged brass. Characters, legal movement and the
winch objective take priority over ornament. Keep the 11×9 rules unchanged.

## Palette and type

| Role | Colour | Use |
| --- | --- | --- |
| River shadow | `#101a19` | Page and deepest shadows |
| Dark moss metal | `#1b2421` / `#30372c` | Panel base and restrained upper lighting |
| Aged brass | `#d2b777` | Heading details, counters, selection and primary action |
| Bone | `#eee7d6` | Primary text |
| Desaturated sage | `#b9bbab` | Secondary text |
| Ally teal | `#98c9be` | Ally rings, ready state, friendly phase |
| Enemy clay | `#dd9c7e` | Enemy diamonds, intent arrows, hostile phase |

Headings use the existing system serif stack `Noto Serif TC`, `PMingLiU`,
Georgia, serif. Body uses `Microsoft JhengHei`, `Noto Sans TC`, sans-serif.
No font download or dependency. Use rem for meaningful UI text; names stay
1rem and scale with 200% root text. Existing Chinese serif availability can
vary by machine. Coordinates remain in accessible cell labels, and appear
visually only with 開發資訊 enabled.

## Frame and hierarchy

Use a thin brass outside edge, dark inset bevel, small corner marks and
restrained top-left lighting. Avoid round dashboard cards. Portrait cards
have the same square crop/frame treatment as enemy intent cards. A diamond
means ready; a check means used; full action state stays in the accessible
name. Keep the compact phase indicator even after the transient banner fades.

At 720p, compress card padding rather than hide controls. At 1080p, allow more
portrait and board space. At 200% text, vertical scrolling is allowed and
controls remain reachable. Narrow screens stack the panel below the board.
Focus rings must remain visible, including Retry in the terminal overlay.

## Board, assets and unit scale

| Existing original asset | Reuse |
| --- | --- |
| `public/art/terrain-v2.png` | Four quadrants: grass, stone, water, forest; SVG patterns clipped to diamonds |
| `public/art/props-v2.png` | Outer forest trees and wagon cargo, cropped in SVG |
| `public/art/ferry-scene-v2.png` | Low-opacity, blurred and desaturated board backdrop |
| `public/art/l03-party-v1.png` | Three foot-anchored figures and close portrait crops |
| `public/art/l03-enemies-v1.png` | Existing knight figure and intent portraits |

No original bitmap is modified. No generated or third-party commercial art
is added. Existing asset provenance remains in the L03 and visual-sprint
documents. `landmarks-v3.png` was inspected but deliberately not used: its
compass stones, survey equipment, lantern and brazier are not a winch or a
broken bridge. Winch, bridge remnants and wagon undercarriage are small SVG
presentation geometry; cargo/trees provide matching painterly detail.

The local camera projects a cell step by ±44 horizontally and +26 vertically.
Diamonds are 88×52 scene units; figures are 50 units high, up from 26, with
38/42-unit crop widths. Their feet remain at cell centres. This is a deliberate
compromise with P1v2's zero-overlap requirement: the nearest same-screen-column
pair has 52 units between feet. **The brief's literal 1.2–1.5 full diamond-height
target is not met**; that would overlap this pair. Close portrait crops supply
face recognition without weakening the original overlap tests. Final figure
scale and the remaining small details at 720p need Owner review.

The ground has 18-unit side faces; water is shown 12 units below the grass.
These heights are visual only. Logical coordinates, passability and click
areas never change. Trees are decorations, not new blockers. Depth order uses
the actual animated foot position, with stable X/id tie-breakers. Artwork,
paths, shadows and landmarks never receive pointer input.

## Motion

- Water: five-second CSS opacity drift, .02–.14, with no displaced hit areas.
- Selection: 1.5-second subtle ring pulse; hover uses a stable tile outline.
- Movement: existing 230ms step clock; preview reads the same pure command's
  returned path and numbers the steps. Pointer and keyboard focus both work.
- Arrival: 180ms small squash/rebound, then rest; no gameplay delay.
- Phase banner: 900ms fade, followed by the persistent phase indicator.
- Reduced Motion: no water drift, pulse, arrival bounce or banner fading;
  movement settles through the existing skip-safe path.

Do not imply hit feedback, skeletal walking, sound, new rules, 3D models or
commercial art acceptance. There is no attack mechanic in this authorized pass.
