# P1v4 visual style — playable L03 only

Successor to [P1v3 STYLE](../playable-l03-p1v3/STYLE.md). This is a presentation
proposal, not final story, worldbuilding or Owner art approval. The visual thesis
is a continuous hand-painted ferry crossing, framed by dark field equipment
and aged brass. Characters, legal movement and the winch take priority over
ornament. The 11×9 rules, camera coordinates and input polygons are unchanged.

## Palette, type and frame

Retain P1v3's river shadow `#101a19`, moss metal `#1b2421` / `#30372c`,
brass `#d2b777`, bone `#eee7d6`, sage `#b9bbab`, ally teal `#98c9be`
and enemy clay `#dd9c7e`. Existing system serif headings and Chinese sans-serif
body stacks remain unchanged; no fonts or dependencies added. Frame, counters,
roster, responsive stacking, focus and 200% text behavior retain P1v3.

## Continuous battlefield

- Use exactly one `public/art/l03-p1v4/battlefield.png` for ground, river,
  banks, road, bridge stone foundations and peripheral foliage.
- No terrain patterns or repeated diamond bitmaps. The same image supplies
  the soft blurred surrounding backdrop; `ferry-scene-v2.png` is unused here.
- Camera: `project(x,y) = (550 + 44(x−y), 70 + 26(x+y))`.
  Each tile is 88×52 scene units. Land remains columns 0–3 and 6–10; water
  columns 4–5, including the destroyed crossing, remains impassable.
- Generation used [layout-guide.svg](layout-guide.svg), rendered as
  [layout-guide.png](layout-guide.png). This is a geometry diagram, explicitly
  **not a game screenshot**. The 1536×1024 reference used xMidYMid meet for a
  940×590 viewBox. Its inverse image rectangle is x=130, y=13.666667,
  width=940, height=626.666667. This aligns the painting to the original
  projection instead of changing rules to fit generated art.
- Generated edges are organic and approximate; painted reeds, vegetation and
  stone foundations are decoration, never navigation/collision data.
  The exact interactive grid is authoritative. Diagnostic screenshots reveal
  all polygons for alignment inspection; normal gameplay does not.
- A narrow SVG edge mask blends fog into the surrounding board. It does not
  change original image bytes or input areas. The map viewport clips image
  overflow before the footer.
- Idle grid polygons are transparent. Hover, keyboard focus, selection and
  legal move range expose them. Intent remains two predicted arrows. Move
  range tint is light enough to retain painted ground detail.

## Painted props and portraits

| Original | Presentation |
| --- | --- |
| `l03-p1v4/props.png` | True-alpha atlas: winch, splintered bridge end, cargo wagon |
| `l03-p1v4/knight-2-portrait.png` | Open-face kettle-helmet portrait for existing second knight |
| `l03-party-v1.png` | Existing three figures and distinct close portrait crops |
| `l03-enemies-v1.png` | Existing first portrait and both knight figures; tighter crop excludes neighboring creature |

Winch, two bridge remnants and wagon use non-destructive nested SVG viewport
crops of the painted atlas. No SVG machine/plank/wheel silhouettes remain;
small ground shadows, the objective diamond and labels remain vector overlays.
Winch stays at (2,1), wagon at (8,4), bridge remnants at (3,4)/(6,4).
All decorations ignore pointer input. Original atlas PNGs are never edited.

There are five unique portrait source/crop signatures. Both knight battlefield
bodies still reuse the existing closed-helmet figure; the new open-face portrait
is not yet a matching full-body variant. It is an anonymous visual proposal,
not a new story identity.

Every generation, including the rejected wide-river attempt, is recorded in
[art-prompts](../art-prompts.json) and [art-manifest](../art-manifest.json).
No commercial imagery, external code or third-party art was imported.

## Unit scale: measured exception

Requested 1.3 × full diamond height = 67.6 units. The real P1v2 browser test
failed with `figures overlap: lace/thoma`; the original report and screenshot
are retained in `rejected-scale-1.3/`. No overlap assertion was removed.

The fixed winch cluster also puts figures on the same screen X with feet 52
units apart. **52 is therefore the geometric maximum shared viewport height**
under the required zero-overlap rule. Final viewport height is 52, up from 50;
party width 39.52, knight width 44. Feet stay at the exact cell centre.
This is **1.00 full tile height**, not the requested 1.2–1.5 range.

Do not mistake transparent viewport height for visible artwork. Browser canvas
measurement at alpha ≥128 gives:

| Figure | Visible height / 52 | 720p / 1080p viewport height |
| --- | --- | --- |
| Karen | 0.97887 | 39.31px / 66.98px |
| Lace | 0.97324 | 39.31px / 66.98px |
| Thoma | 0.97890 | 39.31px / 66.98px |
| Both knights | 0.95973 | 39.31px / 66.98px |

The tighter knight crop `15 8 745 863` removes unused atlas width and the
neighboring creature's fringe; no stretch or source bitmap edits. Relative
to P1v3's crop, the knight artwork is about 24.7% taller, while party art is
4% taller. P1v2's original all-five-unit, 100 pointer-hit, foot-anchor,
cluster/separation and animated depth-order checks remain intact.

## Motion and limits

Retain existing 230ms step playback, 180ms arrival, 900ms phase banner, selection
pulse and subtle water glints. All obey Reduced Motion; effects never calculate
rule outcomes. Optional extra animation frames were skipped to avoid inconsistent
identity/pose frames in this presentation pass. Single-frame bodies still slide
and bob; no new attack, hit, audio or rule behavior is claimed.

79 final automated checks establish the tested presentation and behavior only.
Human playtest, 3–5 minute pacing, 720p recognition and Owner art approval remain
HUMAN_PENDING. See [VERIFICATION](VERIFICATION.md) for command evidence and limits.
