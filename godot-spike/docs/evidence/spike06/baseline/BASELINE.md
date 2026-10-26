# W1 — unchanged spike05, 20 fixed seeds × five policies

`autoplay_field.gd -- --seeds=fixed --variant=spike05
--output=res://docs/evidence/spike06/baseline/` then
`Python312/python.exe godot-spike/tools/summarize_spike06.py docs/evidence/spike06/baseline`.
Both exit0. `index.json` binds seed list, policies and run paths;
`aggregate.json` has rates, turn median/range, casualties/classes, wave engagement,
idle per group, LOS and length ranges. `runs/` contains all 100 traces/commands.

Seed24018 exactly reproduces road lose8, flank lose7, turtle lose6,
scout-retreat lose9; scripted bypass lose7. Fixed enemy mean3.456164s.
Other seeds vary the existing AI coordinate ties AND policy same-class action
order/equal-HP target ties (seed+turn+ID hash). Damage fixed; no deployment jitter.
No game behaviour changes for seed24018. Trace hash excludes report metadata.
Distinctness counts are in aggregate.json; variation is verified, not inferred
from unique seed numbers. These closely related seeds explore deterministic
tie sensitivity, not the full distribution of human tactics or random combat.

All five policies lose all seeds. The bypass policy is a scripted turn5
infiltration probe and its duration is not deployment-to-result pacing.
True idle uses spike05's corrected eligible+observed actor definition; inactive
guards count, deliberate holds and unprocessed terminal-tail actors do not.
Wave first attack and first attacked are separately recorded; legal ranged
shots remain unblocked, while blocked at-phase-start range opportunities are counted.

W1 tests: 4/4,18 assertions, exit0 (`w1-tests.log` at parent).
Same seed compares the entire deterministic report, not only outcome.
