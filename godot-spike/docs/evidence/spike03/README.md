# spike-03 evidence index

Godot 4.7.2 / GDScript / GL Compatibility / AMD Radeon 780M. Owner-authorized
worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`,
clean start `20d9844` on A9 `b2f460b`. Seven local W commits; no push/PR/merge/stash.
Human hit-feel remains **HUMAN_PENDING**; big-map option **OWNER_PENDING**.

| Evidence | What it establishes |
| --- | --- |
| [GAPS](GAPS.md) | W1 measurements and planned feedback; [original trace](before/w1-timeline.json) is retained after W3 baseline regeneration |
| [Before timeline](before/timeline.md) / [JSON](before/timeline.json) | A9-baseline profile; every strike frame, contact F19, five frozen frames, native PNGs from contact −8 through ready |
| [After timeline](after/timeline.md) / [JSON](after/timeline.json) | Tuned normal; seven frozen frames, same-frame bundle, visual recoil and hooks |
| [Crit timeline](after-crit/timeline.md) / [JSON](after-crit/timeline.json) | Presentation-only crit; eleven frozen frames, unchanged HP/cell |
| [Comparison](impact-strip-before-vs-after.png) / [GIF](before-vs-after.gif) | Matched native crop layouts and contact-aligned motion; [MOVIE](MOVIE.md) explains all crops/timing |
| [Before AVI](before/attack-60fps.avi) / [after AVI](after/attack-60fps.avi) / [crit AVI](after-crit/attack-60fps.avi) | Actual 720p/60 FPS movies, copied byte-identically; each folder has movie index/hash |
| [Contact](contact.png) / [crit](contact-crit.png) / [number pop](number-pop.png) / [1080p](contact-1080.png) | Runtime stills, no upscaled source proxies |
| [Timing](timing.json) / [log](timing-run.log) | Nine separate no-readback runs: normal/crit/Reduced Motion × three setups; wall and process-frame clocks |
| [Final GUT](test-run.log) | Complete existing and new impact tests plus one mockup smoke test; actual run summary is authoritative |
| [Audit](audit.json) / [source hashes](source-hashes.json) | Decoded movie/native frame alignment and freezes, protected A9 parity, rule parity, dimensions, budget, allowed scope |
| [Big-map proposal](../../../../docs/proposals/big-map-proposal.md) / [capture data](../../../../docs/proposals/big-map/capture.json) | Seven 720p mockup views and actual camera controls; no gameplay integration |
| [Verification](../../VERIFICATION.md) / [handoff](../../HANDOFF.md) | Real commands/exits, limits, tuning/run instructions and Owner decision boundary |

## Primary timing

| Mode | Open / unit-blocked / terrain-blocked, fixed 60 FPS | No-readback wall seconds |
| --- | --- | --- |
| Normal | 0.950000 / 0.950000 / 0.950000 | 0.928577 / 0.918207 / 0.920291 |
| Crit presentation | 1.016667 / 1.016667 / 1.016667 | 0.987982 / 0.983269 / 0.975860 |
| Reduced Motion | 0.716667 / 0.716667 / 0.716667 | 0.683442 / 0.676853 / 0.681805 |

All are ≤1.7 s; normal/crit also ≤1.2 s; reduced is shorter than normal.
Every result has target HP 4; target cells are (1,6), (1,5), (3,4).
Movie wall times include readback/encoding; they are not these latency numbers.
CPU particles expose emitter capacities rather than exact native live counts;
timeline fields explicitly say upper bound. Tests also verify eventual cleanup.

## Iterations kept for review

- `w2-test-run.log`: all original 79 pass. `w2-pause-test.log` is a failed
  dust-layer type-inference compile; explicit Vector2 fixes it, final pause log
  is 6/6. No earlier tests were deleted or re-pointed.
- `test-run-pre-number-placement.log` and `w3-88-tests.log`: 88-test W3 runs;
  [rejected number render](pre-number-placement/README.md) preserves contact,
  full AVIs and raw timelines. Final number is clear of contact, without a box.
- `still1080-inline-encoding.log`: first still encoded during hold, artificially
  taking 2.0214 s. Final tool saves after ready; repeated 1080p replay is 0.9486 s.
- `w5-capture-pre-pathfix.log`: initial directory API error despite exit 0;
  final path handling fails closed, repeat `w5-capture.log` has no error.
- `w6-tests-pre-hintfix.log`: 88/89; new crit diagnostics had replaced legacy
  hints. Original SCENARIO/SPACE/DEBUG wording is restored alongside C status.
  The unchanged earlier test caught this; the final suite was rerun.
- `audit-pre-hintfix.log`: audit correctly refused the failing suite. Historical
  failed attempts do not count as acceptance; final audit/test logs govern.

Logs retain actual command output with ANSI removed, trailing whitespace trimmed
and encoding normalized to UTF-8 for Git. Source hashes record raw working-tree bytes and LF-normalized
text bytes. The active audit stdout logs are excluded from hashes to avoid a
self-changing snapshot; `source-hashes.json` excludes itself. W7 refreshes the
snapshot after adding the handoff. No asset/source file is modified by auditing.

The mockup has no combat, AI, objectives, fog, game-camera migration or production
terrain. SFX, VFX and A9 swing frames remain development placeholders. Dummy
audio is not hardware audition. Automated checks and model visual inspection
are separate from Gavin's feel/art/scale decision. Shared PLAN/memory/story files
are excluded by the explicit brief; this index/handoff records the milestone.
