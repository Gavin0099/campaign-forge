# A9 method and limits

A8 is the byte-archived base. No frame, sheet, body or face was regenerated.
The explicitly authorized Python/manual-paint option was used throughout;
there were **zero image_gen calls**. No third-party assets, new palette or
gameplay changes. All coordinates refer to the original512px source grid.

W1 freezes A8 PNGs, manifest and audit under baseline-a8/, with SHA-256.
The48 initial masks cover six regions on five frames and two donors (42 masks,
not48: the W1 console message incorrectly counted eight images instead of seven).
W1 measurements distinguish anchor observations, manual anatomical estimates
and binding guide targets. Hidden knees/elbows cannot be measured to4px.

Frames were processed03,02,04,00,01. Each region has at most three attempts.
`prepare_a9_regions.py` defines bounded permissions; `fix_a9_regions.py`
enforces them by compositing every candidate over A8 with the destination mask.
Every attempt PNG, actual changed-pixel mask, transform matrix, input/output/
donor SHA and model decision survives under attempts/ and a9-fix-log.json.
SOURCES.md contains operation records and explicit superseding corrections.

Head trials transplant idle01 pixels at scale1, rotation0, translating the
observed head centre to each guide target. Trial1 carved too much collar.
Trial2 erases only warm old crown pixels above ear height and retains collar
underpainting. These heads were kept on03,02,04,00. Facial interiors were
never painted. 01's W1 head mask underestimated the old nose/hair extent;
trial2 leaves a visible old-face fragment. Trial3 records a new bounded mask
but erases some ivory collar, so all01 head trials are rejected. A8 head01 stays.
These partial improvements do not imply complete temporal identity acceptance.

Separate anchor stole/terminal motif/fringe transplants were tried with rigid
rotations and narrow RGB feather blends. Wider A8 panels leave open strips
around narrow donor panels; motif crops can contain the anchor weapon or
overlap residual larger leaves. All are rejected. 03 motif2 was initially
kept, then withdrawn after adjacent/source review; operation3 restores A8
pixels. Its superseded installed.png remains evidence, never a runtime input.
No source motifs, fringe counts or ownership status were invented.

00/01 mace trial1 used too broad a recover05 mask (robe contamination) and00
missed the independent alpha-centroid gate. Trial2 tightly traces the original
canon weapon, rotates/translates at scale1, restores A8 gripping fingers, and
keeps its head/haft uncompressed. The donor is centred at the target plus1px
to compensate its asymmetric alpha shape. The actual final-PNG centroids,
not the intended transform centre, are the acceptance metric. Integration and
projection remain separate art checks. Some clipped edge highlights/joins
remain; no final canon-art acceptance is claimed.

03 boots/lower legs were translated toward120/354 (A8~59/319);04 toward165,455
and334,464 (A8~93,464/351,464). They improve target positions but open abrupt
hem-to-leg boundaries. Both repairs are rejected under the A8 regression gate:
continuous hem and attached feet take precedence over a falsely reported pose
PASS. Original stance/foot defects remain explicitly open.

Each regional decision records13 checklist states and a technical scan. W3
performs the complete installed-frame audit. A8's PASS cuffs, hem, palette,
one satchel/roll and attached grounded boots are protected; rejected trials
never reach runtime. Final edits lie inside the union of KEPT recorded masks;
the rest of each A8 frame is pixel-identical, including failed cloth regions.
No global alpha/RGB rewrite was applied. Pillow uses straight RGBA; alpha is
preserved for unchanged pixels and resampled only inside transformed regions.

Model visual inspection and test success are not Owner art approval. Remaining
PLACEHOLDER frames, human hit-feel and the artist commission fallback remain
open. Read-only process inspection through Win32_Process was denied; fallback
Get-Process exposed no other Codex/Claude executable, which cannot certify
absence of a desktop session. No other worktree was read or written. Python
and Git required scoped sandbox escalation; ordinary commit hooks still run.
No trust store/config changes, subprocess launcher or dependency was added.
