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

## spike-02 Phase A

2026-10-23. Continued from Owner brief commit `9345b0e` on `codex/godot-spike`.
**Engineering checks pass; exact art/weapon identity is not fully satisfied.**
Thoma's specified original crop is empty-handed, so the six generated swing
frames are explicitly PLACEHOLDER for equipment identity and minor costume
variation. Human playtest is **HUMAN_PENDING**, and P010 remains **PROPOSED**.

### Commands actually run

Run from `D:\campaign-forge\scratch\godot-spike`. `godot` is the existing
Owner-provided console wrapper. Tools were run outside the restricted PATH
sandbox where needed; no tool install, credentials, trust change or other
worktree edit. Real exit codes were read immediately after each engine call.
Logs were normalized to UTF-8/LF with trailing whitespace trimmed; outcomes,
errors and assertions are retained. An exit 0 without actual files and a
`CAPTURE_COMPLETE ... pass=true` marker is not accepted.

| Command | Exit | Result |
| --- | ---: | --- |
| `godot --version` | 0 | `4.7.2.stable.official.ed1daf0bf` |
| `git fetch origin` | 0 | No incoming commits on the existing task branch; no pull, branch switch or push |
| `python godot-spike/tools/build_manifest.py` | 0 | Manifest and JSON Schema authored |
| `python godot-spike/tools/prepare_frames.py` | 0 | 21 fixed-pivot runtime frames, source records and contact sheet |
| `godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 | 44 files, `SYNC_SHARED_ANIM ... pass=true` |
| `godot --headless --path godot-spike --import` | 0 | [Import log](evidence/spike02/import-run.log) |
| `godot --headless --path godot-spike -- --smoke` | 0 | All three setups completed during A3/A4/A6 implementation |
| `godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | **24 tests / 624 assertions**, [final log](evidence/spike02/test-run.log) |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --readability` | 0 | Twelve rest/contact captures, refreshed in A8 with complete viewport transforms; marker passes |
| `python godot-spike/tools/measure_readability.py` | 0 | [Overlap measurements](evidence/spike02/readability-overlap.json) |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --capture02` | 0 | Six measured runs, four separately timed screenshot runs, eleven screenshots; [marker and Escape input](evidence/spike02/rendered-run.log) |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie D:\campaign-forge\scratch\godot-spike\godot-spike\.godot\spike02-movie\frame.png -- --movie02` | 0 | 73 actual PNG frames, pass marker; [log](evidence/spike02/movie-run.log) |
| Same movie command with destination `...\spike02-movie\attack.avi` | 0 | 60 frames, 7,660,658 bytes, pass marker and Escape exit; [log](evidence/spike02/movie-avi-run.log) |
| `godot --path godot-spike --resolution 1920x1080 --position 0,0 --borderless --audio-driver Dummy -- --overview02` | 0 | `OVERVIEW 1920x1080 error=0`; [image](evidence/spike02/overview-1080.png) |
| `python godot-spike/tools/package_spike02_evidence.py` | 0 | Actual screenshot dimensions, five identical movie frames, AVI header, timing and original PNG parity checked |
| `jsonschema.Draft202012Validator.check_schema(schema)` and `jsonschema.validate(manifest, schema)` via installed Python package | 0 | `JSON_SCHEMA_VALIDATION pass=true`; no dependency installed |
| `git diff --exit-code 9345b0e -- ui-prototype docs/DECISIONS.md godot-spike/scripts/rules` plus the four original Godot art PNG paths | 0 | Web, rules, P010 and original artwork unchanged |

### Measured timing and whole-world freeze

The ordinary-playback rows below use a rendered window **without synchronous
GPU screenshot readback**. Wall time is from swing start to input-ready and
includes the real hold. The process-delta accumulator excludes paused frames,
then adds the nominal 80ms hold; scheduler/frame boundaries make it slightly
different from wall time. Both measures are under 1.7 seconds.

| Setup | Normal wall / process+hold (s) | Reduced wall / process+hold (s) |
| --- | --- | --- |
| Open | 0.9179 / 0.9529 | 0.7302 / 0.7846 |
| Unit blocked | 0.9127 / 0.9642 | 0.7300 / 0.7934 |
| Terrain blocked | 0.9114 / 0.9613 | 0.7302 / 0.7817 |

Ordinary rendered hitstop: **90.239–91.271ms wall**, requested 80ms; subsequent
process deltas: 90.859–92.130ms. This includes frame quantization. The separate
fixed-60-fps movie holds **five byte-identical frames (83.33ms)** and visibly
resumes on the next frame. Details and every trigger frame are in
[timing.json](evidence/spike02/timing.json) and [movie index](evidence/spike02/movie-index.json).

The screenshot run for open contact measured **122.301ms** during synchronous
GPU readback; it is kept in `screenshot_runs`, not represented as normal playback.
The other screenshot runs were 89.394–91.482ms. Screenshot capture can therefore
perturb the apparent hold on this machine. The unchanged ordinary-playback
acceptance tolerance is 80–107ms; no universal frame-time guarantee is claimed.

The implementation pauses a dedicated World subtree through `SceneTree.paused`.
HUD/root are ALWAYS. All world tweens are bound to world nodes. An always-process,
unscaled timer plus monotonic and subsequent-process-frame guards releases the
pause. The tests compare both frame clocks, a real world tween, actual particle
node processing, camera position/offset/zoom and damage-number position/alpha
across the complete hold, while an ALWAYS HUD probe advances. The movie proves
the rendered world also stays unchanged. Audio starts on contact and rings out.
No Engine.time_scale mutation; audible output remains unverified with Dummy audio.

Spark, SFX and flash are logged on exactly the same process frame as the contact
pose. Reduced Motion records suppressed spark/flash triggers, plays only 0/3/5
swing key poses, has no smear, shake, flash, particles or closing-step offset,
and retains a stationary damage number. Its weapon pose does not spatially
close the full normal-attack gap; that is an explicit reduced-motion limitation.

### Visual evidence and test coverage

[Anticipation](evidence/spike02/anticipation.png),
[held contact](evidence/spike02/contact.png), [recoil](evidence/spike02/recoil.png),
[unit stagger](evidence/spike02/blocked-unit-stagger.png),
[terrain stagger](evidence/spike02/blocked-terrain-stagger.png),
[reduced contact](evidence/spike02/reduced-motion-contact.png),
[camera option](evidence/spike02/readability-option-a.png),
[large units](evidence/spike02/readability-option-b.png),
[label-free runtime grayscale](evidence/spike02/knights-grayscale.png),
[minimal HUD](evidence/spike02/hud-minimal.png),
[debug HUD](evidence/spike02/hud-debug.png).
All eleven are actual 1280×720 viewport captures. Grayscale uses a runtime
screen shader with HUD hidden; no screenshot repainting. Both blocked images
capture reaction frame 1, the buckled pose. [Full AVI and selected movie PNGs](evidence/spike02/MOVIE.md).

The 24 tests retain all ten pure-rule cases and four prior playback/audio cases
(G now requires F1 first), plus manifest/schema contract, existence and dimensions,
invalid duration/contact/path rejection, fixed pivot/mirroring, reduced key poses,
source/copy hashes, world pause, contact synchronization, reordered/unknown event
playback, distinct knight textures and first-frame clock regression. They do not
constitute human input, feel or commercial-art approval. Rendered automated input
uses 1/2/3, R, Space, M, F1, G and Escape; full gamepad/localization/text-size
coverage remains outside this spike.

### Failures retained and corrections

- A3 import initially printed a type-inference parse error despite exit 0;
  an explicit Node2D annotation corrected it. A3's first parity run exited 1
  because virtual `res://../` traversal cannot read the source folder. Resolve
  an absolute source path first; the rerun passed 89 checks.
- [Existing tests](evidence/spike02/attempt-existing-tests.log), exit 1: the old
  G-only diagnostic expectation was updated to the authorized F1 → G behavior.
- [Image loading](evidence/spike02/attempt-image-load-warning.log), exit 1:
  GUT rejected export warnings from Image.load_from_file; tests now load the
  imported Texture2D and inspect its image. No warning suppression added.
- [Pause-clock mutation](evidence/spike02/attempt-pause-clock-mutation.log),
  exit 1: contact residue was reset after the pause began. Move that update
  before contact entry, and prevent pre-start frame delta from skipping wind-up.
- [Relative movie path](evidence/spike02/attempt-movie-relative-path.log),
  exit 0 **but rejected**: Godot interpreted the path relative to its project,
  could not create the WAV/frames, and emitted errors. Absolute paths and actual
  file checks replace exit-code-only acceptance.
- [Movie wall clock](evidence/spike02/attempt-movie-wall-clock.log), exit 1:
  PNG encoding throughput was mistakenly tested as gameplay duration. Fixed-step
  timing is now separate. The same recording exposed a four-frame hold; count
  subsequent process deltas to guarantee at least five frames at 60 fps.
- [Movie path discovery](evidence/spike02/attempt-movie-path-discovery.log),
  exit 1: consumed engine arguments were absent from OS.get_cmdline_args. Use
  [Engine.get_write_movie_path](https://docs.godotengine.org/en/4.4/classes/class_engine.html#class-engine-method-get-write-movie-path), then verify the produced file/header.
- [Readback jitter](evidence/spike02/attempt-rendered-hold-jitter.json) and
  [repeat](evidence/spike02/attempt-rendered-hold-jitter-repeat.json), both exit 1:
  first contact measured 123.804 / 122.042ms while reading GPU pixels. The capture
  runner now separates six ordinary timing runs from four screenshot runs and
  retains both. Thresholds for ordinary playback were not relaxed.
- Evidence logs initially had doubled CR/newline and trailing spaces after
  PowerShell encoding conversion (`git diff --check` exit 2). Normalize only
  encoding/line endings/trailing whitespace; failure messages remain intact.
- Final audit caught an A5 measurement error: global_scale alone loses the
  rotation used to represent a mirrored sprite. Re-record all twelve images
  and use get_global_transform_with_canvas plus inverse affine mask sampling.
  Corrected option b has 16px knight/knight overlap at unit-blocked rest;
  option a has no nonparticipant overlap. Earlier 92px contact and 63/29/81px
  contact claims are invalid. See [corrected comparison](ANIMATION-ADAPTER.md).

### Scope and provenance

[Original PNG hashes](evidence/spike02/original-assets.json),
[executable-source hashes](evidence/spike02/source-hashes.json),
[asset prompts/references/output hashes](../../shared-anim/SOURCES.md),
[contact sheet](../../shared-anim/contact-sheet.png).
Source frames live at repo-root `shared-anim/`; Godot holds byte-identical copies.
Executable-source hashes include both actual working-tree bytes and the LF
normalization used by this repo's Git text attributes.
All Phase A edits are under `shared-anim/` and `godot-spike/`. The diff from
`be9a398` also includes the **pre-existing** Owner brief commit `9345b0e` in
`docs/tasks/`; this run did not edit it. Scope is checked against `9345b0e`.
No main/other worktree edit, push, merge, PR, Actions, deployment, new addon,
formal rules/story change or Phase B work. Task completion is not SessionEnd.
