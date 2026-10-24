# W4 regression verification

Final full GUT run: exit0,79/79 tests,7894 assertions,13 scripts, zero warnings.
Existing71 tests retained; eight A9 tests added. All eight historical A8 tests
still assert their original checklist/pose/provenance against byte-archived
A8 middle PNGs and audit. Immutable endpoints and unchanged manifest remain
tested live. No old assertion was removed to accommodate new art.

A9 covers fixed anchor SHA, complete manifest equality/pivot/contact/events/
timing/Reduced Motion, RGBA/ground/foot occupancy, independent mace centroids,
opaque03 contact, no archived runtime inputs, audit/placeholder/table agreement,
every regional attempt's masks/hashes/budget, exact A8 pixels outside final
kept masks, actual movie-mask metrics and complete landmark fields.

First full run exit1 (78/79): the new grayscale-mask test used Godot's
get_used_rect(), which measures opaque alpha and therefore returns the whole
canvas for an L8 mask even at black pixels. Corrected it to count white RGB
permission pixels. Also allowed an empty transform list on recorded no-op
regions only. Original failed log retained as test-run-failed-1.log.
Second run exit0,79/79, but one Float/Int comparison warning in the JSON movie
frame count assertion. Changed threshold50 to50.0; retained warning run as
test-run-warning-2.log. Final third run is test-run.log.

W4 sync/import exit0; contact sheet regenerated from live manifest, source /
Godot-copy hash parity passes. Inspection caught01's raised mace in the
headtop ROI: evidence-only height corrected to A8's original361px because
the head is unchanged. Other copied manual joints and exact source PNGs were
unchanged; movie RGB/trace did not change. Delta tables and flicker height
metrics regenerated exit0. Final W6 A9 contract also verifies the final table.

No game script, rules/HUD, timing, endpoint or environment changed. Tests are
engineering evidence, not human art/hit-feel approval.
