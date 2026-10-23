# Godot hit-feel spike — verification

2026-10-23, Windows, Godot `4.7.2.stable.official.ed1daf0bf`, standard build,
GDScript, Compatibility renderer / AMD Radeon 780M. Base: `ff46faa` on
`codex/godot-spike`, above P1v7 `ff87682`.

**Technical acceptance passes. Human feel, audible mix, and engine adoption remain
HUMAN_PENDING.** This is one staged attack, not a playable campaign or G005 rules.

## Actual commands and exit codes

Commands below ran from the worktree root. Stdout/stderr were redirected into
the linked logs; `$LASTEXITCODE` was read immediately after each engine invocation.
Logs retain terminal escape sequences and are stored as UTF-8.

| Command | Exit | Evidence / result |
| --- | --- | --- |
| `godot --version` | 0 | `4.7.2.stable.official.ed1daf0bf` |
| `godot --headless --path godot-spike --import` | 0 | [Import log](evidence/import-run.log); imports regenerated, not committed |
| `godot --headless --path godot-spike --quit-after 3` | 0 | Step 3 / 4 startup smoke, no script errors |
| `godot --headless --path godot-spike -- --smoke` | 0 | Step 4: all three sequences completed, 0.8236 / 0.9251 / 0.9251 s |
| `godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | [Final test log](evidence/test-run.log): **14 tests, 344 assertions, zero failures** |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --capture` | 0 | [Rendered log](evidence/rendered-run.log), [completion report](evidence/capture-report.json): four runs, eight fresh 1280×720 PNGs, all writes OK |
| `godot --path godot-spike --resolution 1920x1080 --position 0,0 --borderless --audio-driver Dummy --quit-after 180 -- --overview` | 0 | [Overview log](evidence/overview-run.log), actual **1920×1080** image |
| `git diff --exit-code ff46faa -- ui-prototype` | 0 | No original web code, tests, rules or art changed |
| `git diff --check` | 0 | Whitespace check on first-party changes |

GUT 9.7.1 download succeeded (PowerShell exit 0); version, ZIP hash, MIT license
and bundled font notices are in [addons/README](../addons/README.md).

## Timing and behavior

The clock is `Time.get_ticks_usec()` from immediately before wind-up until the
input lock is released. **Wall time includes the 80 ms local hitstop**, frame
scheduling and capture GPU readback. PNG encoding occurs after playback and is
excluded. No fixed-FPS movie clock or shortened capture animation is used.

| Setup | Rendered normal | Headless normal | Headless reduced |
| --- | ---: | ---: | ---: |
| (a) (1,4) → knight (1,5), displaced to (1,6) | 0.9270 s | 0.8018 s | 0.5970 s |
| (b) same attack, knight-2 at (1,6) blocks | 0.9502 s | 0.9254 s | 0.6976 s |
| (c) (2,4) → knight (3,4), crossing (4,4) blocks | 0.9663 s | 0.9195 s | 0.6925 s |

Rendered reduced-motion setup (a): **0.8444 s**. Additional headless replay and
keyboard runs: 0.8949 s normal (c), 0.6027 s reduced (b). Every measured run is
below 1.7 s. This is measured local performance, not a guarantee on every PC.

Nominal playback: 180 ms anticipation, 85 ms lunge, 80 ms contact hold,
220 ms ease-out knockback (or 60 + 160 ms shove/recoil), 180 ms recovery,
220 ms settle. Engine frame boundaries quantize the observed stages; per-phase
wall timestamps are in the capture report. Flash is held at contact and fades
over 35 ms after hitstop; shake decays over 200 ms. No actor tween is active
during the contact hold; `Engine.time_scale` remains 1. Audio, HUD and particles
continue. Reduced motion removes lean/lunge/shake/flash/particles, makes
knockback 30 ms, and keeps a stationary fading damage number and the sound.

Rules tests cover event order, exact HP loss, immutable inputs, nonadjacency,
water, destroyed crossing, another unit, all four map edges, BFS occupancy and
tie order, unreachable bank, dead/missing/same-side combatants and HP flooring.
The source map has **no wall tile**; forest remains walkable. Tests do not invent
wall terrain to satisfy a case that does not exist in the source.

Scene tests cover all three setups in both motion modes, replay from clean
state, repeated input, setup/settings lock, final foot positions, ≤6 px blocked
shove, phase order, real-time contact hold, camera/rotation reset, shader values,
keyboard handlers, and deterministic, non-silent, unclipped synthesized PCM.
Rendered capture additionally dispatches 1–3, R, Space, M and G through Godot's
input system. This is synthetic input automation, not human keyboard playtesting.

## Rendered evidence

- [Contact / hitstop / white flash](evidence/hit-frame.png)
- [Knockback end](evidence/knockback-end.png)
- [Unit-blocked recoil](evidence/knockback-blocked-unit.png)
- [Terrain-blocked recoil](evidence/knockback-blocked.png)
- [Reduced motion](evidence/reduced-motion.png)
- [Diagnostic grid](evidence/grid-diagnostic.png), off by default
- [1920×1080 overview](evidence/overview-1080.png)
- [Four-frame normal-strike sequence](evidence/SEQUENCE.md), **3,895,706 bytes**

All images come from the running OpenGL viewport. Capture forces a GPU redraw
before readback so an occluded desktop window cannot leave a pending capture
waiting forever. No generated screenshot, compositing, resizing or postprocessing
is used. The short sequence is four timed frames, not a 60 FPS movie; no AVI is
claimed. Full animation remains available by running the scene.

## Failures found and corrected

1. Sandbox shell could not resolve Godot/Python and could not write worktree Git
   metadata. Approved escalated tool calls found the existing Winget wrapper;
   no install, credential or trust change. `git fetch origin` then exited 0.
2. First GUT run exited **1**, 11/13 passing: unset shader parameter read back as
   null; test teardown freed a node while its signal was emitting. Explicit
   initialization and one-frame teardown delay fixed both. [Original failed log](evidence/attempt-tests-before-fix.log).
3. Initial rendered capture had two missing type annotations and was terminated;
   there is no valid successful engine exit for that attempt. One log redirection
   failed before launching the engine (missing directory), another found a locked
   log. Stale shell `$LASTEXITCODE=0` was not accepted as engine evidence.
   [Incomplete banner-only log](evidence/attempt-incomplete-render.log) is retained
   as incomplete, not a complete error trace.
4. A subsequent capture exited **1**: immediate checking after queued input
   dispatch was too early. Awaiting the next process frame fixed it. WASAPI also
   reported no usable device; subsequent capture commands explicitly use Dummy
   audio. Sound playback is scheduled and PCM tested; **audible output is unverified**.
5. Visual inspection found a grid behind the painting and double-multiplied
   shader color. A separate overlay and the correct fragment `COLOR` fixed them;
   final images and tests reflect both fixes.
6. Two early overview commands exited 0 but rendered **1875×1055** because Windows
   constrained the startup window. The overview-only minimum/window size now
   requests 1920×1080 explicitly, without changing the monitor's display mode.
7. An early `--quit-after 900` capture exited 0 without completing all images.
   [Early-exit log](evidence/attempt-early-quit.log). The final command omits that
   flag, forces redraw, has a 12-second failure watchdog, checks eight screenshots
   and four runs, and emits `CAPTURE_COMPLETE ... pass=true`. File completeness
   was checked separately; the early exit is not counted as a pass.

## Scope and reproducibility

[Source hashes](evidence/source-hashes.json) bind the first-party executable inputs
and tests. [Asset hashes](evidence/asset-copy-hashes.json) prove all four PNG copies
match the untouched originals. [Engine provenance](evidence/engine-provenance.json)
records the observed wrapper, console exe and engine exe bytes. This is tooling
provenance, not a hardened launcher or full executable trust attestation: commands
still use the Owner's existing PATH/wrapper and shell environment.

All authored project/evidence changes are under `godot-spike/`; the final handoff
adds only the requested proposal row outside it. Godot/GUT also use their normal
OS application cache/log directory (visible in the test log); no other project
checkout was read or edited. Git operations use this worktree's necessary shared
Git metadata. Hooks ran normally and emitted only the existing report-only
`missing_canonical_memory` advisory. No hook bypass or lifecycle completion claim.
The latest restricted task scope takes precedence over older PLAN/memory updates.
