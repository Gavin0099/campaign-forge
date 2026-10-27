# Native 720p performance

Three repetitions per cell; GL Compatibility, AMD780M, max60FPS, VSync off. No movie/readbacks/concurrent Godot. Exact git exports; same reached spike06 flank24018 T2 and waveT8, same enemy event replay. AI evaluated separately. CPU scopes inclusive and overlapping; wall minus process is not GPU time. No GPU timer is claimed.

| Build | Workload | Mean / p95 / worst ms | CPU process mean | Draw calls mean | Pure AI ms mean |
| --- | --- | --- | --- | --- | --- |
| spike05 | scroll-T2 | 23.65 / 29.21 / 32.61 | 66.90 | 2245.0 | — |
| spike05 | scroll-wave | 23.73 / 29.00 / 49.04 | 53.31 | 2214.2 | — |
| spike05 | enemy-normal | 25.19 / 30.04 / 66.16 | 84.93 | 2257.3 | 66.84166666666667 |
| spike05 | enemy-2x | 23.77 / 29.88 / 35.09 | 156.28 | 2260.0 | 59.245666666666665 |
| spike06 | scroll-T2 | 23.92 / 29.23 / 31.64 | 62.46 | 2245.0 | — |
| spike06 | scroll-wave | 24.81 / 29.31 / 31.23 | 51.26 | 2214.2 | — |
| spike06 | enemy-normal | 24.66 / 30.41 / 46.04 | 74.12 | 2257.4 | 68.26366666666667 |
| spike06 | enemy-2x | 25.29 / 30.54 / 49.33 | 158.98 | 2260.0 | 64.07933333333332 |
| before | scroll-T2 | 23.58 / 28.87 / 30.70 | 61.49 | 2245.0 | — |
| before | scroll-wave | 24.36 / 28.67 / 30.21 | 49.25 | 2214.2 | — |
| before | enemy-normal | 25.04 / 29.75 / 53.51 | 72.00 | 2257.2 | 61.619 |
| before | enemy-2x | 24.95 / 30.37 / 45.47 | 160.61 | 2259.8 | 67.47033333333333 |
| diagnostic | scroll-wave-no-minimap | 16.69 / 28.63 / 31.32 | 37.91 | 1771.8 | — |

## Cause (W4, measurement before fixes)

The original34ms mean is NOT reproduced as a code regression. Exact05→06 on
identical T2 scroll:23.65→23.92ms; same wave scroll23.73→24.81ms. In06 changing
T2→wave adds0.89ms here. Thus neither these measured code nor workload deltas
explain the old10–13ms delta; old host/session conditions were not recorded well
enough to attribute the remainder. Do not claim the scout kit caused34ms.

Top steady CPU scope: field_minimap._draw rebuilds432 polygons/1728 vertex
transforms every frame, ~11–12ms/frame (raw per-repeat scopes in JSON); repeated
world_bounds/factor/origin arithmetic dominates. Identical implementation in05/06.
Wave-scroll diagnostic with minimap processing+rendering disabled:24.36→16.69ms
mean; both compute AND drawing removed, so this is a bound, not an attribution of
all7.67ms to either CPU or GPU. Labels/indicators ~0.2–0.4ms each; world actor
updates~0.1ms. Terrain _draw only on refresh; minimap/labels/indicators queue a
redraw each processed frame. Draw-call monitor ~2214→1772 in diagnostic. Ground
and minimap retained canvas items still submit draws even when _draw isn't called.

No per-scroll-frame AI/pathfinding/threat/retreat evaluation. In common wave AI,
3 distance_map calls cost53.687ms of57.335ms inclusive ai_plan in one repeat;
7 reach calls4.626ms. Own enemy_phase CPU means05~63/06~66/current~65ms per
ACTION, separately from identical22-event playback. Playback telemetry also calls
reach35 times (~22ms in one repeat), causing action-frame spikes. V threat/LOS,
ZoC and retreat preview are event-driven; previews-before.json records12 explicit
refresh samples and a synthetic legal-budget retreat preview. Legend work is
inside HUD.update_state (not separately additive); LOS inside attack_info/threat.

Performance.TIME_PROCESS/TIME_PHYSICS_PROCESS are sampled raw engine monitors,
coarsely updated/contaminated by setup/action peaks; column is monitor samples,
NOT a per-frame CPU sum (some exceed wall mean). Scoped microseconds are actual
CPU timings. Render thread/GPU elapsed is unavailable in this harness: no valid
GPU-time claim and wall minus monitor is NOT render time. Draw/objects/nodes
reported instead. Inclusive scopes overlap. No movie/readbacks/concurrentGodot.

Method caveat: common states are real spike06 flank24018 T2 and waveT8, both
loaded byte-identically in all exports. Same precomputed event replay removes
pre-kit semantics differences; own AI CPU/result hashes measured separately.
This compares code+archived authored data but shared-state runs intentionally
replace level/unit dictionaries. Native-design balance is tested separately in
W1/W6; do not confuse this with05's own much larger deployment. Exact archives
and pre-instrument LF hashes in perf/export-*.json. Export-only wrappers identical;
no change to gameplay source inW4. Temporary exports removed byW8.

All native/import/diagnostic/pixel/preview commands exit0. Before export exit has
an engine cleanup warning for2objects (no script error; performance report valid);
retain raw log, not silent normalization. Not a production memory-leak certification.
