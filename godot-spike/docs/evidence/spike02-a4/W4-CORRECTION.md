# W4 protected RGBA correction

First full GUT run: exit 1, 41/42 tests, 1572/1583 assertions. The complete
8,877,476-byte log is retained losslessly as attempt-test-protected-rgba.log.gz.
No diagnostic lines were dropped; GUT printed large differing pixel arrays.

Cause: the offline compositor zeroed hidden RGB beneath transparent pixels,
including protected weapon/ground regions; repeated alpha compositing also
changed some foot-edge alpha. Exact raw RGBA comparisons correctly failed.

Correction: after all cleanup, paste A3 raw bytes through the recorded weapon,
hand and foot masks, plus the bottom ground-contact rows. This restores hidden
RGB and edge alpha as well as visible pixels. The manifest, geometry and timing
remain unchanged. Assertions still require exact equality; only their failure
format changes from dumping arrays to a boolean with a named region.

All five frames, provenance hashes, region checks, sequence checks, asset sheets
and synced copies were regenerated. Art flags remain PLACEHOLDER. The W1 proof
is preserved as the earlier draft, not silently replaced by the W4 correction.

Historical A3 tests now read A3 archival frames/audit when testing the historical
repaint alpha and A3 handoff. The live manifest assertion remains live. The new
A4 suite tests current pixels and current per-region/handoff status separately.
