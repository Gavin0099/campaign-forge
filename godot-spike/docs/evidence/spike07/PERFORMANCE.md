# Native 720p performance

Three repetitions per cell; GL Compatibility, AMD780M, max60FPS, VSync off. No movie/readbacks/concurrent Godot. Exact git exports; same reached spike06 flank24018 T2 and waveT8, same enemy event replay. AI evaluated separately. CPU scopes inclusive and overlapping; wall minus process is not GPU time. No GPU timer is claimed.

| Build | Workload | Mean / p95 / worst ms | Sampled TIME_PROCESS monitor ms | Draw calls mean | Pure AI ms mean |
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
| after | scroll-T2 | 16.67 / 27.30 / 30.80 | 59.68 | 2245.0 | — |
| after | scroll-wave | 16.64 / 29.65 / 31.17 | 45.33 | 2214.2 | — |
| after | enemy-normal | 16.71 / 29.77 / 42.23 | 59.54 | 2257.1 | 27.557333333333332 |
| after | enemy-2x | 16.77 / 29.50 / 39.09 | 144.69 | 2259.6 | 29.208333333333332 |

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

## Fix → measured result (W5)

| Measured cause | Fix | Same workload before → after |
| --- | --- | --- |
| minimap terrain rebuild12.42ms/frame | Retained static Node2D commands + precomputed exact vertex transforms; only invalidate on size/bounds/terrain/goal change. Live dots/camera rectangle remain live | wave scroll24.36→16.64ms, T2scroll23.58→16.67ms |
| distance_map repeated linear occupant and terrain/stat queries | Call-local first-living occupancy and terrain-cost indexes; same Dijkstra order/ties/parents. reach also call-local occupancy/ZoC/terrain | own wave AI61.62→27.56ms (normal repeats); no global mutable cache |
| action playback telemetry/rebuild plus draw submission | same local reach optimization, no telemetry removed | normal25.04→16.71ms,2x24.95→16.77ms |

PASS minimum means20.7scroll/23.5enemy; **FAIL strict <=16.67ms all workloads
and worst<33ms**. Enemy normalworst42.23,2x39.09ms; scrollworst30.80/31.17.
One-time terrain _draw/setup and synchronous action telemetry/rebuild remain;
own AI still27–29ms/action, ~2200 retained draw calls/frame. Frame-cap/host jitter
and render submission remain mixed in wall samples; no GPU elapsed measurement,
so GPU-fill bottleneck or necessity of art/renderer changes is NOT established.
No claim that further improvement is impossible; no renderer/art changes made.

Exact same runtime frozen-idle frames: deployment,V,O each0 differing RGBpixels
(pixel-diff.json and six PNGs). Same draw order/coordinates/colors/font/labels;
static geometry retained as commands, not baked textures. All five profiles and
impact code untouched. W2's truthful T3 warning is present both before/after.
Tests compare optimized reach costs+parents,threat,AIevents/states vs full W4 rule
snapshot across reached states,moves,attack and nextturn;483assertions/2tests,exit0.
Minimap mutation/resize/goal and forced-fresh invalidation checked; units/turn
correctly leave terrain cache intact. Golden snapshot exact d6455d3 field_rules;
it is a test fixture, not a selectable gameplay rules variant.

Native no-capture field normal/crit/reduced0.949/1.017/0.747s,all<=1.7s;
Skirmish all9 setups×modes pass<=1.7s with Reduced<=normal (hitfeel/timing-runtime).
Readbacks0; both commands exit0. Dedicated full verification followsW7.

## W6 supplemental native viewport render timers

Same common states/event replay,3 repetitions/cell, separate sequential native720p runs. RenderingServer viewport measurement enabled explicitly; no movie/readback. Samples are previous completed viewport render CPU/GPU milliseconds, not whole-frame CPU; scopes overlap and must not be added. W4/W5 original tables remain unchanged.

| Build | Workload | Wall mean / p95 / worst | Render CPU mean / p95 / worst | Render GPU mean / p95 / worst |
| --- | --- | --- | --- | --- |
| spike05 | scroll-T2 | 24.00 / 29.58 / 50.30 | 8.69 / 11.04 / 37.32 | 5.72 / 11.81 / 18.64 |
| spike05 | scroll-wave | 24.80 / 29.30 / 30.88 | 9.05 / 10.94 / 11.46 | 5.83 / 12.05 / 17.73 |
| spike05 | enemy-normal | 25.22 / 30.11 / 38.53 | 8.82 / 10.93 / 11.51 | 5.81 / 11.21 / 18.74 |
| spike05 | enemy-2x | 25.88 / 30.53 / 33.53 | 9.18 / 11.08 / 11.65 | 6.01 / 12.31 / 15.69 |
| spike06 | scroll-T2 | 24.32 / 29.32 / 31.23 | 8.63 / 10.95 / 40.26 | 5.66 / 11.13 / 18.16 |
| spike06 | scroll-wave | 25.10 / 29.11 / 30.32 | 9.04 / 10.81 / 11.67 | 5.92 / 12.28 / 18.95 |
| spike06 | enemy-normal | 25.66 / 29.89 / 39.70 | 8.99 / 11.06 / 11.61 | 6.07 / 10.73 / 18.65 |
| spike06 | enemy-2x | 26.11 / 31.07 / 34.31 | 9.13 / 11.15 / 11.43 | 6.45 / 13.77 / 17.41 |
| before | scroll-T2 | 24.08 / 29.10 / 54.39 | 8.49 / 10.86 / 40.52 | 5.52 / 10.95 / 22.94 |
| before | scroll-wave | 24.28 / 29.07 / 30.79 | 8.40 / 10.70 / 11.69 | 5.62 / 12.36 / 18.24 |
| before | enemy-normal | 25.31 / 29.59 / 48.97 | 8.55 / 10.85 / 11.34 | 5.82 / 10.03 / 17.90 |
| before | enemy-2x | 25.92 / 30.60 / 46.38 | 8.87 / 11.12 / 11.54 | 6.27 / 13.36 / 17.37 |
| after | scroll-T2 | 16.69 / 27.76 / 38.24 | 7.59 / 10.41 / 36.84 | 4.06 / 10.91 / 21.29 |
| after | scroll-wave | 16.67 / 29.27 / 31.13 | 7.63 / 10.27 / 16.32 | 4.03 / 10.98 / 16.46 |
| after | enemy-normal | 16.71 / 28.17 / 46.07 | 8.25 / 10.47 / 12.27 | 4.47 / 11.19 / 16.20 |
| after | enemy-2x | 16.76 / 29.75 / 37.37 | 8.01 / 10.58 / 11.37 | 4.46 / 11.02 / 17.83 |

### Actual enemy phases including synchronous AI

Same reached input wave state; each build plays its own AI result, and measurement begins BEFORE AI evaluation. First-frame CPU/action spikes are included. Three repeats per speed; no readback/movie/concurrent Godot. Pre-kit05 results may differ; original matched-event table isolates rendering separately.

| Build | Workload | Mean / p95 / worst ms | Render CPU mean | Render GPU mean |
| --- | --- | --- | --- | --- |
| spike05 | enemy-normal | 24.80 / 30.25 / 99.16 | 8.24 | 5.62 |
| spike05 | enemy-2x | 24.79 / 30.21 / 92.21 | 8.07 | 5.92 |
| spike06 | enemy-normal | 25.23 / 30.73 / 88.89 | 8.78 | 6.00 |
| spike06 | enemy-2x | 26.69 / 31.26 / 87.58 | 9.06 | 6.35 |
| after | enemy-normal | 16.85 / 28.99 / 64.28 | 7.67 | 4.23 |
| after | enemy-2x | 17.03 / 29.70 / 66.80 | 8.00 | 4.49 |

Final native actual enemy-phase check includes synchronous AI in frame intervals:
normal16.85ms mean,p95 28.99,worst64.28;2x17.03,p95 29.70,worst66.80.
Minimum23.5mean PASS, strict16.67/all-worst33 FAIL. These supersede any inference
of full enemy-phase worst from the matched-animation replay39–42ms table. GPU
render mean4.23/4.49ms,CPU viewport7.67/8.00ms; scoped action AI27–29ms plus
telemetry/rebuild/draw work cause CPU action boundaries; rendering/host frame
pacing also varies. GPU sample peaks16–22ms show jitter; no claim stable60FPS,
GPU-only bottleneck, or that art/renderer changes are necessary/sufficient.

W6 supplement05 scroll was rerun clean after a1.7s offline AVI extraction might
have overlapped the first supplement's setup/early frames. Summary uses all3 clean
scroll repeats; original raw attempted run retained. No other Godot ran in any
native measurement. MovieMaker's CPU/GPU/encoding timings are capture-only and
never substituted for native performance.
