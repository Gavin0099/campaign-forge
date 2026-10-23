# Campaign Forge — Ferry Dusk / 渡口暮色 (L03 color-identity probe)

Status: **PROPOSAL / OPT-IN POC / HUMAN ART REVIEW REQUIRED**  
Base: codex/playable-l03-research at ff87682 (P1v7).  
Scope: playable L03 presentation only, not rules, map geometry, timing, image generation, or game balance.  
Source PNG atlases remain unchanged. Existing origin/provenance is retained.

## Why this work exists

P1v4 already specified river shadow, moss metal, brass, bone, ally teal and enemy clay. Those were useful individual CSS swatches, but world/HUD/PNG atlases still used independently chosen color ranges. Repeated prompts saying "dark fantasy hand-painted" cannot guarantee the same lighting, value structure, materials and texture.

**Hypothesis to test, not a claim:** unifying the existing images and UI around a cool blue-green iron shadow + aged brass focal light should reduce collage/AI inconsistency and preserve tactical readability.

Do not evaluate "less AI-looking" by saturation alone. Repeated symmetric details, unrelated brush textures, facial proportions, inconsistent top-left lighting, and disconnected object shadows require an asset paint-over or redraw; CSS filters cannot fix them.

## Palette v0.1: roles before exact RGB

| Role | HEX | Usage / limits |
| --- | --- | --- |
| Deep iron shadow | #101B1E | Deepest screen/body shadow, never all midtones |
| Cold panel | #1D2929 | HUD and peripheral darkness |
| Mossed metal | #293832 | HUD upper planes, armor-environment bridge |
| Wet metal | #3E504B | Midtone secondary planes |
| River slate | #355259 | Water body; not bright cyan |
| River stone | #596B68 | Damp stone and desaturated river-bank edges |
| Rope / weathered wood | #816954 | Winch/rope wood; warmer than background |
| Bone / readable text | #EEE4CE | Text, pale cloth highlights |
| Muted text | #B9BDAD | Secondary text; verify contrast at 720p |
| Tarnished brass | #C5A873 | Winch objective and important HUD cues |
| Ally sage | #9DBCB0 | Ally identity, traversable cells; also use shapes |
| Enemy rust | #D28A73 | Enemy intentions and threats; also use shape/dashes |
| Active focus | #EFCF8E | Selection, keyboard focus, confirmation |

Illustration colors are **not** restricted to thirteen literal hex values. Each role has a controlled value/chroma ramp; skin, fire, cloth and metal need their own transitions. Pixel-art nearest-color quantization is inappropriate for these painterly images.

### Material ramp suggestions (shadow → middle → highlight)

- River / wet stone: #14282F → #355259 → #83958C
- Aged metal: #172426 → #3E504B → #A3AC9B
- Rope / wood / brass: #342920 → #816954 → #C5A873
- Human warmth (limited to characters): #493430 → #A47B66 → #D6B59A
- Emissive/importance: no global bloom; reserve #EFCF8E for objective/selection highlights and hotter warnings for failure danger.

Directional lighting: weak warm upper-left source; cold green-slate lower-right shadow. World is mainly cool-neutral, not globally brown and not pitch black. Value readability overrides hue preference.

## Implementation and A/B

- Added src/playable-l03/palette-ferry-dusk.css, loaded **after** the P1v7 stylesheet.
- Component reads an initial query parameter; root data-p1v-palette switches the style.
- **Baseline, unchanged:** /?scene=playable-l03
- **Color experiment:** /?scene=playable-l03&palette=ferry-dusk
- **In-session toggle:** /?scene=playable-l03&palette=ferry-dusk&palette-lab=1; enable existing **開發資訊**, then toggle **渡口暮色（調色實驗）**.
- Existing test entry point remains baseline until explicitly opted in.
- CSS scopes background and UI color separately; generated battlefield, props, character bodies and portraits have different strengths. Actors stay brighter than scenery. Tactical cues are not desaturated with painted scenery.
- No PNG replacement, rule logic, animation sequencing, pointer geometry, text copy, licensing, or network dependency changes.

**Caveat:** browser CSS filter changes displayed pixels, not files. Browsers can differ for nested SVG filters/clips; verify in browser. The POC does not create a 3D LUT or prove assets have converged.

## Repeatable review procedure

1. Same commit: open original and experiment in 1280×720 with identical turn, selected unit, progress, and animation fully settled. Repeat at 1920×1080.
2. Capture untouched PNG screenshots plus mode and commit SHA. Name files original-720, ferry-dusk-720, original-1080, ferry-dusk-1080.
3. Compare in grayscale: units distinguishable from background; enemy intent and winch 2/3 visible; selection and focus still obvious; map/foot anchors unchanged.
4. Compare in color: water recedes; three ally silhouettes remain distinguishable; winch is a focal point; not every decorative line becomes gold.
5. Review 100%-scale HUD and controls, keyboard focus, Reduced Motion, 200% text, color-blind readability. Measure contrast rather than assuming visual impression equals conformance.
6. Owner rates **art cohesion** and **tactical readability** independently; mood improvement that hides interaction fails.
7. After approval, bake grade via reversible adjustment layers or LUT; paint over mismatched anatomy, inconsistent materials/brushwork and cast shadows. Preserve original PNG + graded output + recipe + provenance.

### Constraint for new generated images

> Original hand-painted dark fantasy tactical-RPG illustration for Campaign Forge, Ferry Dusk color script: deep iron shadow #101B1E, river slate #355259, moss metal #3E504B, worn rope #816954, aged brass #C5A873, bone highlights #EEE4CE, ally sage #9DBCB0, enemy rust #D28A73. Restrained low-chroma background with clear value steps; upper-left warm practical light and lower-right cold ambient shadow; material-specific rough dry-brush texture, asymmetrical wear and silhouette. Match supplied L03 camera/layout/foot anchor and style sheet. No neon blue/purple glow, no smooth plastic gradients, no hyperreal photographic lighting, no floating decorative clutter, no copied character likeness or game IP. Generate characters separately from environment where needed.

A prompt is **not** a complete production art specification without dimensions, alpha, outline, material, light vector, pose/crop, existing-asset reference, and same-screen comparison.

## Internet references (methods only; no borrowed art)

- Game Developer — Color in games: value, chroma and visual hierarchy:
  https://www.gamedeveloper.com/design/color-in-games-an-in-depth-look-at-one-of-game-design-s-most-useful-tools
- Krita official manual — Gradient Map and Palettize (reviewed source art can use reversible adjustments):
  https://docs.krita.org/en/reference_manual/filters/map.html
- Unity Learn — 2D in Unity: Tech Art Essentials (plan whether lighting is painted in or a separate pass):
  https://learn.unity.com/article/2d-in-unity-tech-art-essentials
- Lospec palette list: inspiration for controlling ramps, not a mandate to quantize painterly source:
  https://lospec.com/palette-list

Darkest Dungeon is a study of selective warm highlights against dark environments, not source art to copy or a mandate to imitate its exact rendering.

## Current evidence and limits

- Reviewable source code and palette committed on a separate branch; default remains original.
- Remote text edits and exact insertion anchors can be checked.
- **NOT YET VERIFIED:** Vite/TypeScript build, automated browser snapshots, SVG filter behavior, actual 720p/1080p captures, perceived artistic effectiveness or Owner approval.
- This is a **color-direction POC**, not an accepted art pass.