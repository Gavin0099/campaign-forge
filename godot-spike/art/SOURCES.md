# Copied original art

Copied byte-for-byte on 2026-10-23; originals remain untouched. Original generated
demonstration art, not confirmed story or commercial art approval. No new license
is granted to these assets. Provenance: `ui-prototype/docs/art-prompts.json` and
`ui-prototype/docs/art-manifest.json` in the repository.

| Local file | Original repository path |
| --- | --- |
| battlefield.png | ui-prototype/public/art/l03-p1v4/battlefield.png |
| props.png | ui-prototype/public/art/l03-p1v4/props.png |
| l03-party-v1.png | ui-prototype/public/art/l03-party-v1.png |
| l03-enemies-v1.png | ui-prototype/public/art/l03-enemies-v1.png |

Character and prop regions are cropped at runtime with AtlasTexture; no source
PNG is edited. No external commercial assets or newly generated images used.

## spike-02 A2 HUD

`ui/field-frame.png` is an original deterministic 64×64 nine-slice texture
created by `tools/build_a2_ui.py`: moss iron fill #1b2421, inset #101a19,
aged-brass edge #d2b777/#776746, seeded edge wear and corner marks. No image
generation, borrowed texture, commercial art or Ferry Dusk palette.
SHA-256 is printed by that script; text contrast is recorded in
`docs/evidence/spike02-a2/contrast.json`.

HUD portraits are runtime AtlasTexture crops from the already byte-identical
originals above: Thoma `l03-party-v1.png rect(1718,0,220,245)`; knight A/B
`l03-enemies-v1.png rect(270,8,265,300)`. No new character illustration or
original PNG edit. Body animation provenance lives in `../../shared-anim/SOURCES.md`.

Traditional Chinese uses Godot SystemFont with Microsoft JhengHei, Noto Sans TC,
PingFang TC fallback names. Microsoft JhengHei is installed on the validation
Windows host; the OS font is used at runtime, not copied or redistributed.
No font file/license grant is added. Other hosts require a matching CJK system
font; glyph availability is verified on this host only.
