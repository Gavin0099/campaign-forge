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

## spike-02 A2

2026-10-23 Owner brief `4b9cea4` on Phase A `46edbc6`, worktree
`D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`.
Final engineering checks pass; human playtest and Owner art acceptance remain
**HUMAN_PENDING**. Weapon is APPROVED (Owner, 2026-10-24), superseding the A2 pending status; engine decision P010 remains **PROPOSED**.

Final headless GUT: **33/33 tests, 924 assertions, zero failures, no script
errors or GUT warnings**, exit 0. All 24 existing tests remain; nine A2 tests
cover HUD visibility, help/focus, event-derived forecasts (including lethal
1-HP input), arm/confirm/contact transitions, manifest/schema-required fields,
weapon idle, source/copy parity, every knight frame, six timing cases, CJK
glyphs and banner expiry, plus physical Space press/release. The package checker
rejects error-bearing logs even when GUT's aggregate summary says pass.

### Actual commands and exits

Run from the worktree root with the existing Owner Godot wrapper and Python.
No dependency/addon installed. Restricted-shell PATH could not resolve these
tools (exit 1); approved escalated calls used the existing Godot/Python install.
Initial fetch also could not write the linked worktree Git metadata (exit 1);
the authorized fetch then succeeded outside that restriction. No main-checkout
source or other worktree was read or written.

| Command actually run | Exit | Evidence / result |
| --- | --- | --- |
| `git fetch origin review/gpt-godot-spike` | 0 | Requested review branch fetched with existing auth; no push |
| `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a.md` | 0 | Read the specified independent GPT review |
| `godot --version`; `python --version` | 0 | `4.7.2.stable.official.ed1daf0bf`; Python 3.12.10 |
| `python godot-spike/tools/prepare_a2_frames.py` | 0 | Seven fixed-pivot Thoma frames, attempt records, style sheet; source PNGs untouched |
| `python godot-spike/tools/build_a2_ui.py` | 0 | Original 9-slice texture; minimum text contrast 5.344:1 |
| `python godot-spike/tools/prepare_a2_knight.py` | 0 | Seven consistent knight-B scripted edits, per-input/output SHA-256 |
| `godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 | Final `SYNC_SHARED_ANIM files=57 pass=true`; hash parity independently tested |
| `godot --headless --path godot-spike --import` | 0 | [Import log](evidence/spike02-a2/import-run.log); no script errors |
| `godot --headless --path godot-spike -- --smoke` | 0 | W2: all three existing attacks completed |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --stage-capture` | 0 | W2 rendered iteration: fixed portrait minimum-size overflow and thick HP bars |
| `godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | Final **33 / 924**, [clean test log](evidence/spike02-a2/test-run.log) |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --capture-a2` | 0 | [Rendered log](evidence/spike02-a2/rendered-run.log): `CAPTURE_COMPLETE A2 movie=false runs=6 shots=9 pass=true` |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --readability-a2` | 0 | [Readability log](evidence/spike02-a2/readability-run.log): nine actual images, pass marker |
| `python godot-spike/tools/measure_readability.py --a2` | 0 | [Full-affine alpha-mask overlap](evidence/spike02-a2/readability-overlap.json) |
| `godot --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie D:\campaign-forge\scratch\godot-spike\godot-spike\.godot\spike02-a2-movie\attack.avi -- --movie-a2` | 0 | 60-frame native AVI, 7,365,366 bytes; [log](evidence/spike02-a2/movie-avi-run.log), pass marker |
| Same native movie command with destination `D:\campaign-forge\scratch\godot-spike\godot-spike\.godot\spike02-a2-movie\frame.png` | 0 | 60 native PNG frames; [log](evidence/spike02-a2/movie-png-run.log), pass marker |
| `godot --path godot-spike --resolution 1920x1080 --position 0,0 --borderless --audio-driver Dummy -- --overview-a2` | 0 | Actual [1080p forecast](evidence/spike02-a2/overview-1080.png); [pass marker](evidence/spike02-a2/overview-run.log) |
| `python godot-spike/tools/package_a2_evidence.py` | 0 | Actual screenshots, AVI header, hold hashes, JSON Schema, all shared file hashes, original PNG parity; `EVIDENCE_PACKAGE_COMPLETE ... pass=true` |
| `git diff --exit-code 46edbc6 -- ui-prototype docs/DECISIONS.md godot-spike/scripts/rules godot-spike/art/battlefield.png godot-spike/art/props.png godot-spike/art/l03-party-v1.png godot-spike/art/l03-enemies-v1.png` | 0 | Web, rules, decision file and all four original copied PNGs unchanged |
| `git diff --check` | 0 | No whitespace errors |

### Measurements and visual inspection

Normal rendered attacks: **0.914639 / 0.915426 / 0.911700 s** (open / unit-blocked /
terrain-blocked). Reduced Motion: **0.729160 / 0.730027 / 0.730169 s**. All six
include real hitstop and satisfy ≤1.7 s. [Timing JSON](evidence/spike02-a2/timing.json)
separates ordinary playback from GPU-readback screenshot runs. Movie timing is
**0.916667 s** with **five identical frames / 83.333 ms** at contact; movie wall
times measure encoding throughput. [Movie, retained samples and full index](evidence/spike02-a2/MOVIE.md).

[Default](evidence/spike02-a2/default-view.png),
[selected unit](evidence/spike02-a2/selected-unit.png),
[open forecast](evidence/spike02-a2/attack-forecast.png),
[unit-blocked forecast](evidence/spike02-a2/forecast-blocked-unit.png),
[terrain-blocked forecast](evidence/spike02-a2/forecast-blocked-terrain.png),
[contact during hitstop](evidence/spike02-a2/contact.png),
[actual stagger frame 1](evidence/spike02-a2/blocked-stagger.png),
[help](evidence/spike02-a2/help-overlay.png),
[F1](evidence/spike02-a2/debug-f1.png) are real 1280×720 captures.
The first two show the same selected state, captured separately; they are not
distinct modes. No scenario/hotkey/technical status appears by default.
Help/debug are off initially, and attack forecast is visible while armed until
contact. HP remains visible through hitstop. CJK glyph tests and actual renders
verify the available Windows system font; no font was redistributed.

[Contrast](evidence/spike02-a2/contrast.json) covers all six text-role colors on
the three opaque backings: minimum **5.344:1**, all normal-text WCAG AA pass.
Transient damage numbers have a dark backplate; their intentional fade is not
a claim of sustained readability. Layout is a fixed 1280×720 reference canvas
scaled/letterboxed to 16:9; other aspect ratios, enlarged text and gamepad remain
outside this small acceptance pass.

[Knight default](evidence/spike02-a2/knights-default-view.png),
[zoomed](evidence/spike02-a2/knights-zoomed.png),
[grayscale](evidence/spike02-a2/knights-grayscale.png) are label-free real renders;
grayscale is an in-engine shader, not screenshot editing. Bone crest/light shield
distinguish B at both scales in model inspection. All three rest/contact
measurements have **0 nonparticipant opaque overlapping pixels**; intended
attacker/target contact is **71 / 157 / 164 pixels**, threshold alpha ≥128,
including weapons, excluding rings, HUD and VFX. These sampled transforms do
not prove all possible positions/frames in a full battle.

[Style sheet](evidence/spike02-a2/thoma-weapon-style-check.png) is explicitly an
asset sheet (not a game screenshot). Weapon identity is APPROVED (Owner, 2026-10-24), superseding A2 pending status; idle and
recover pass the model style check, five articulated motion frames remain
PLACEHOLDER for costume-detail drift. [Prompt/attempt/hash provenance](../../shared-anim/SOURCES.md),
[per-frame audit](../../shared-anim/frame-audit.json),
[original PNG parity](evidence/spike02-a2/original-assets.json),
[first-party source hashes](evidence/spike02-a2/source-hashes.json),
[artifact audit](evidence/spike02-a2/evidence-audit.json).

### Retained failures and corrections

- Swing 02 attempt 1 already put the weapon below the waist before horizontal
  contact. Rejected copy and full prompt/hash remain in shared-anim/rejected
  and SOURCES; attempt 2 supplies the descending upper-right smear. Other
  frames used one attempt. No rejected attempt is a runtime sequence frame.
- First rendered capture exited **0 but failed acceptance**: physical Space
  armed on global press and confirmed on focused Button release, then Escape
  exited before the completion marker. [Original log](evidence/spike02-a2/attempt-space-double-dispatch.log).
  Both Space edges now have one owner, with real press/release regression coverage.
- W4's 32/918 summary and the first 33/924 rerun both exited **0 but included
  an error during GUT cleanup**. The test freed the scene while its signal was
  still emitting. The earlier W4 log remains in commit `229a820`; the later
  [error-bearing log](evidence/spike02-a2/attempt-test-signal-teardown.log) is retained.
  Tests now await the next process frame before teardown. Final 33/924 log has
  no ERROR or GUT WARNING; the package checker rejects those strings.
- First 1080p observer sampled immediately after rebuilding HP widgets, before
  their process callback placed them. The observer now waits two frames; final
  image was inspected. This was capture scheduling, not a claimed runtime fix.
- W2 render iteration found TextureRect/ProgressBar minimum sizes applied before
  size policies; final code applies requested dimensions after configuring them.

No original atlas, battlefield, props, ui-prototype file, rules, G005/P010, story
or other worktree content changed. No push, main merge, PR, Actions, dependency,
deployment or Phase B work. Normal hooks ran; missing-canonical-memory is an
advisory, not an actual session-end event or claim of complete governance closeout.

## spike-02 A3

Engineering verification passes; the five repainted motion frames still fail
detailed costume consistency and remain **PLACEHOLDER**. Weapon identity is
**APPROVED (Owner, 2026-10-24)**. Owner art approval is not claimed; human hit-feel
playtest stays **HUMAN_PENDING** and P010 stays **PROPOSED**. Phase B is unstarted.

Commands below ran from `D:\campaign-forge\scratch\godot-spike` on
`codex/godot-spike`, Godot **4.7.2.stable.official.ed1daf0bf**, AMD Radeon 780M
OpenGL Compatibility renderer. `GODOT` below denotes the actual executable:
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`.
`PYTHON` denotes `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`.
These explicit installed paths were executed through approved sandbox escalation;
no installer, credentials, trust bypass or global setting was changed.

| Actual command (executable aliases expanded above) | Exit | Evidence / result |
| --- | --- | --- |
| `git fetch origin review/gpt-godot-spike` | 0 | Read GPT A2 review with `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a2.md` (0) |
| `PYTHON godot-spike/tools/prepare_a3_frames.py` | 0 | Five garment-only repaints; source sprigs, masks, exact A2 alpha and protected geometry |
| `PYTHON godot-spike/tools/a3_style_check.py` | 0 | Seven-frame full/detail/native-size sheet; two PASS, five PLACEHOLDER |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy -s res://tools/readability_a3.gd` | 0 | 12 captures, `CAPTURE_COMPLETE A3 readability shots=12 pass=true`; [log](evidence/spike02-a3/readability-run.log) |
| `PYTHON godot-spike/tools/measure_a3_readability.py` | 0 | Per-image verdicts, projected region area/luminance; [JSON](evidence/spike02-a3/knight-readability.json) |
| `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 | 63 source/synced files byte-equal; [log](evidence/spike02-a3/sync-run.log) |
| `GODOT --headless --path godot-spike --import` | 0 | [Headless import log](evidence/spike02-a3/import-run.log) |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | **37 tests / 1162 assertions**, no engine errors or GUT warnings; [log](evidence/spike02-a3/test-run.log) |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a3.gd` | 0 | `CAPTURE_COMPLETE A3 movie=false runs=6 shots=13 pass=true`; [log](evidence/spike02-a3/rendered-run.log) |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a3-movie/attack.avi -s res://tools/capture_a3.gd -- --movie-a3` | 0 | Complete native AVI, `CAPTURE_COMPLETE A3 movie=true runs=1 shots=0 pass=true`; [log](evidence/spike02-a3/movie-run.log) |
| `PYTHON godot-spike/tools/package_a3_evidence.py` | 0 | Validates logs, actual pixels, PNG provenance/parity, timing and decoded movie hashes; [audit](evidence/spike02-a3/evidence-audit.json) |

An inline Pillow contact-sheet regeneration and handoff-table preparation command
also exited 0 before sync/import. The table is retained as
[frame-status-table.md](evidence/spike02-a3/frame-status-table.md). W5 tests compare
its exact rows with the audit; W6 embeds those rows and reruns the targeted test
against the final A3 handoff section. This distinguishes W5 preparation from W6
handoff completion, rather than claiming a future section was already tested.

### Timing, actual pixels and invariant checks

| Setup | Normal wall time | Reduced Motion wall time |
| --- | --- | --- |
| 1 — open | 0.936505 s | 0.752470 s |
| 2 — unit-blocked | 0.948820 s | 0.747849 s |
| 3 — terrain-blocked | 0.927993 s | 0.729133 s |

All six ordinary runs exclude GPU readbacks, include hitstop and end with input
unlocked, below **1.7 s**. Full manifest equality against the A2 baseline proves
no timing, camera, offsets, canvas **512×512**, pivot **[256,464]**, contact index
**3** or anchor **[455,196]** changed. Swing durations stay
**180/70/40/80/100/150 ms**; Reduced Motion still omits smear frame 2. A2's recorded
ordinary normal times were 0.911700–0.915426 s: this run has small scheduler
variation, not a changed timing contract. [Timing JSON](evidence/spike02-a3/timing.json).

[Movie](evidence/spike02-a3/attack-60fps.avi): **59 complete 1280×720 frames**,
**7,272,134 bytes**, no subsampling. Strike frame 2 to input-ready frame 57 is
**0.916667 s**; frames 20–24 have identical decoded RGB hashes, **83.333 ms** of
held contact, with visible resume at frame 25. Offline encoding wall time is
not gameplay latency. [Movie notes](evidence/spike02-a3/MOVIE.md) and
[frame hashes](evidence/spike02-a3/movie-index.json).

Rendered evidence: [anticipation](evidence/spike02-a3/swing-anticipation.png),
[smear](evidence/spike02-a3/swing-smear.png),
[contact during hold](evidence/spike02-a3/contact.png),
[follow-through](evidence/spike02-a3/follow-through.png),
[idle](evidence/spike02-a3/idle.png). The
[old/new comparison](evidence/spike02-a3/contact-sheet-old-vs-new.png) uses native
320×320 crops of actual rendered captures; separate replay camera sampling may
vary slightly. The [asset sheet](evidence/spike02-a3/asset-sheet-old-vs-new.png)
compares exactly equal sprite scale and is explicitly not a runtime screenshot.

Knight inspection: all 12 native 720p unlabeled color/grayscale samples received
model PASS; no clear failure requiring a silhouette proposal was observed.
Shield B-minus-A screen-luma difference is **50.337–69.548 / 255**. Same-pose helm
silhouette differences are **16 px** at rest and **34 px** at 1.4×. These proxies
do not measure human recognition speed. W4 ran before the Thoma W5 sync; knight
and environment bytes are unchanged. No knight art, scale or gameplay was edited.

Four original PNGs match their read-only React sources byte for byte. The A2
baseline is archived with hashes; its five old motion frames are not live.
Tests verify each repaint differs, all alpha and unmasked pixels remain exact,
and the contact grip/haft/head region is unchanged. Source/code fingerprints:
[source-hashes.json](evidence/spike02-a3/source-hashes.json). Raw generated images,
full prompts, four reference hashes per attempt and cleanup are in
[A3 prompts](../../shared-anim/a3-swing-prompts.json) and
[SOURCES](../../shared-anim/SOURCES.md). One attempt per frame; full generated
figures were not adopted because they moved geometry. Costume patches only.

### Preserved failed or rejected attempts

- W4 initial capture exited **1**, six rest images only: subscription was attached
  to a player subsequently replaced by fixture reset. Observer now subscribes
  after `play_attack`; [log](evidence/spike02-a3/attempt-readability-old-player.log).
- First GUT run exited **1**, 36/37: new raw-pixel test used `Image.load_from_file`
  on imported resources, triggering warnings. It now decodes explicit PNG bytes;
  [log](evidence/spike02-a3/attempt-test-image-loader.log). No warnings suppressed.
- First W5 capture exited **1**, five shots: physical key dispatch rebuilt the
  player after subscription. Observer now waits for dispatch;
  [log](evidence/spike02-a3/attempt-render-input-dispatch.log).
- Next capture exited **0** and printed pass, but **was rejected on visual
  inspection**: `force_draw` inside a frame signal could show the previous canvas
  state. Final observer waits for `RenderingServer.frame_post_draw`; final smear,
  contact and follow-through images were re-inspected. The rejected
  [log](evidence/spike02-a3/attempt-render-stale-canvas.log) is retained.
- Initial environment attempts could not resolve `python` or access the installed
  Godot inside the sandbox. Installed explicit paths succeeded under escalation.
  A library probe found Pillow installed and NumPy absent; cleanup uses Pillow and
  a small local perspective solver, with no dependency installed. Log packaging
  normalizes UTF-16/CRLF and strips ANSI colors without dropping diagnostic lines.
- One packaging invocation exited **1** because stdout was redirected into a log
  the package tool was normalizing, causing a Windows open-file lock. The rerun
  buffers output until the tool exits and passed; the
  [failed log](evidence/spike02-a3/attempt-package-open-log.log) is retained.

No React edits, formal story/engine decision, Phase B, push, merge or PR. No
physical audio-device audition, human playtest or commercial art approval.

## spike-02 A4

**Engineering checks pass; costume completion remains PARTIAL.** Five swing
frames now use a reference-pixel cutout rig instead of newly generated figures.
The old fan/bell hem alpha is replaced. Visible shoulder/waist/cuff joins and
hem-to-foot continuity still fail, so all five retain **PLACEHOLDER**. Immutable
idle/01 and swing/05 retain model PASS. The short one-handed flanged mace remains
**APPROVED (Owner, 2026-10-24)**; human playtest is **HUMAN_PENDING** and P010 is
**PROPOSED**. Phase B was not started.

Commands ran in `D:\campaign-forge\scratch\godot-spike` on `codex/godot-spike`,
starting clean at `8197026` over A3 `bd80c5e`. `GODOT` below means
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`;
`PYTHON` means `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`.
Version: **4.7.2.stable.official.ed1daf0bf**, OpenGL Compatibility on AMD Radeon
780M. Installed tools required sandbox escalation; no installation, credential,
trust or global configuration change was made.

| Actual command | Exit | Result |
| --- | --- | --- |
| `git fetch origin review/gpt-godot-spike` | 1 then 0 | Initial sandbox FETCH_HEAD permission error; authorized escalation fetched the specified branch |
| `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a3.md` | 0 | Read CONDITIONAL ACCEPT review; its ending is explicitly incomplete |
| `PYTHON godot-spike/tools/prepare_a4_frames.py --proof` | 0 | Reference library, masks, palette, one-frame proof; rejected rigid proof retained |
| `PYTHON godot-spike/tools/prepare_a4_frames.py --build` | 0 | Five frames, archived A3 bytes, zero generation attempts; repeated for the W4 RGBA correction |
| `PYTHON godot-spike/tools/a4_style_check.py` | 1, 1, then 0 | First two sheet layouts rejected unscaled crops larger than their cells; enlarged cells, never rescaled crops. Final 1:1 region sheet and per-region/sequence verdicts |
| `GODOT --version` | 0 | Exact approved version above |
| `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 | Initial sync, then final resync after contact-sheet regeneration/correction; 64 source/copied files byte-equal |
| `PYTHON godot-spike/tools/a4_contact_sheet.py` | 0 | Contact sheet regenerated from live manifest |
| `GODOT --headless --path godot-spike --import` | 0 | Final headless import; [log](evidence/spike02-a4/import-run.log) |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 1 then 0 | Protected RGBA defect corrected; **42/42 tests, 1,583 assertions**, no engine errors or GUT warnings; [final log](evidence/spike02-a4/test-run.log) |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a4.gd` | 0 | 13 rendered shots + six no-readback timing runs, `CAPTURE_COMPLETE A4 movie=false runs=6 shots=13 pass=true` |
| `GODOT --path godot-spike --resolution 1920x1080 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a4.gd -- --1080p` | 1 then 0 | Windows initially clamped to 1875x1055; capture-only minimum size correction yields native 1920x1080, 13 shots and six timing runs, same completion marker with pass=true |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a4-movie/attack.avi -s res://tools/capture_a4.gd -- --movie-a4` | 0 | Complete native movie; `CAPTURE_COMPLETE A4 movie=true runs=1 shots=0 pass=true` |
| `PYTHON godot-spike/tools/check_a4_reproduction.py` | 0 | Rebuilding in memory reproduces all five PNGs byte for byte and exact protection masks |
| `PYTHON godot-spike/tools/package_a4_evidence.py` | 0 | Checks actual decoded pixels, dimensions, completion logs, timing, original PNG parity, source hashes and movie hold |

### Actual timing and immutable contracts

These are ordinary rendered runs without GPU readback. Screenshot replays are
excluded. All times run from strike to input-ready and include hitstop.

| Setup | 720p normal | 720p Reduced Motion | 1080p normal | 1080p Reduced Motion |
| --- | --- | --- | --- | --- |
| Open | 0.917815 s | 0.650812 s | 0.919160 s | 0.684374 s |
| Unit-blocked | 0.917651 s | 0.684154 s | 0.917966 s | 0.667565 s |
| Terrain-blocked | 0.917613 s | 0.667759 s | 0.917747 s | 0.684457 s |

All twelve runs finish below **1.7 s**, with contact events on the same process
frame, >=80 ms hitstop and unlocked input. The full manifest equals archived A3:
canvas **512x512**, pivot **[256,464]**, contact index **3**, anchor **[455,196]**,
durations **180/70/40/80/100/150 ms**, offsets, camera and Reduced Motion indices
unchanged. Both references match fixed A3 SHA-256 values. No baseline path is
referenced by the live manifest. Protected weapon/hand/foot masks and ground
contact pixels compare exact RGBA, including hidden RGB beneath alpha=0.

[720p timing](evidence/spike02-a4/timing.json),
[1080p timing](evidence/spike02-a4/timing-1080p.json),
[source hashes](evidence/spike02-a4/source-hashes.json),
[package audit](evidence/spike02-a4/evidence-audit.json).

### Rendered evidence and visual limits

[Native 60 FPS movie](evidence/spike02-a4/attack-60fps.avi): **59 complete frames,
7,270,584 bytes**, no subsampling. Strike frame 2 to input-ready frame 57 is
**0.916667 s**. Decoded contact frames 20-24 are identical (**83.333 ms**), then
frame 25 visibly resumes. [MOVIE](evidence/spike02-a4/MOVIE.md) and
[decoded frame hashes](evidence/spike02-a4/movie-index.json). Encoding wall time
is not gameplay latency; Dummy audio is not physical-device audition.

| Pose | 720p | 1080p |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a4/swing-anticipation.png) | [PNG](evidence/spike02-a4/swing-anticipation-1080p.png) |
| Smear | [PNG](evidence/spike02-a4/swing-smear.png) | [PNG](evidence/spike02-a4/swing-smear-1080p.png) |
| Contact in hitstop | [PNG](evidence/spike02-a4/contact.png) | [PNG](evidence/spike02-a4/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a4/follow-through.png) | [PNG](evidence/spike02-a4/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a4/idle.png) | [PNG](evidence/spike02-a4/idle-1080p.png) |

[Rendered A3/A4 comparison](evidence/spike02-a4/contact-sheet-a3-vs-a4.png) uses
native 320x320 viewport crops without resizing; camera/tween sampling can vary
slightly between replays. [Separate asset comparison](evidence/spike02-a4/asset-sheet-a3-vs-a4.png)
uses exactly equal sprite scale and is explicitly not a runtime screenshot.
[Region sheet](evidence/spike02-a4/region-check.png) uses 1:1 source crops;
[sequence strip](evidence/spike02-a4/sequence-strip.png) shows seven poses,
native-size approximations and adjacent onion overlays. Six adjacent pairs
retain visual FAIL despite generally small mean-color deltas: those metrics do
not detect spatial seams. Full [region/sequence reasons](../../shared-anim/frame-audit.json)
control PLACEHOLDER; numerical checks do not approve the art.

### Retained failures and boundaries

- W1 rigid cutout proof had cuff holes and detached stance; retained as
  [rejected proof](evidence/spike02-a4/proof-rejected-rigid.png). Revised method
  uses actual cuff corners and modest garment ease, but seams remain unfinished.
- W4 first suite: **41/42**, **1572/1583**, exit **1**. Transparent-RGB cleanup
  and repeated alpha composition changed protected raw pixels. Final raw overwrite
  corrects that; [full lossless failed log](evidence/spike02-a4/attempt-test-protected-rgba.log.gz)
  and [correction detail](evidence/spike02-a4/W4-CORRECTION.md). Equality assertions
  were retained, not weakened to visible-only comparisons.
- Initial 1080p run: exit **1**, `pass=false`, actual **1875x1055**. Retained
  [log](evidence/spike02-a4/attempt-1080p-window-clamped.log),
  [dimensions/phase trace](evidence/spike02-a4/attempt-1080p-window-clamped.json)
  and [rejected screenshot](evidence/spike02-a4/attempt-contact-1875x1055.png).
  Only the capture observer now sets its minimum viewport size; game HUD and
  gameplay scripts are unchanged. No image upscaling used for acceptance.
- A sandbox Python probe failed to resolve the installed executable; the
  explicitly installed path succeeded with escalation. No dependency installed.

A3 historical alpha/audit tests now target the preserved A3 archive; new A4
contract tests cover current frames. The W4 table was prepared before the W6
handoff; the final handoff section is checked separately when written.

No React, battlefield, props, knight, rules, HUD, timing, story, G005 or P010
change. No push, main merge, PR, Actions, deployment or Phase B. Shared PLAN and
memory are outside this narrow authorization, so the milestone is recorded here
and in HANDOFF. Normal hooks ran with a nonblocking missing_canonical_memory
advisory; no SessionEnd or canonical-closeout completion is claimed.

## spike-02 A5

2026-10-24. Worktree `D:\campaign-forge\scratch\godot-spike`, branch
`codex/godot-spike`, start cc164b2 above A4 8592fbb. **Engineering passes;
art repair is partial, five motion frames remain PLACEHOLDER.** Single-satchel
count and unit local embroidery scale are corrected. Shoulder/waist/cuff
folds, repair-edge visibility and hem/boot/sequence continuity still fail.
These are model observations, not Owner art approval. Human hit-feel remains
**HUMAN_PENDING**. Owner chose Godot directly on 2026-10-24; **Phase B is
CANCELLED**, no React work remains. P010 was not edited; Owner should update it.

### Actual commands and exit codes

Run from this worktree root. `GODOT` means
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`;
`PYTHON` means `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`.
Existing installed versions: Godot **4.7.2.stable.official.ed1daf0bf**, Python
**3.12.10**, Pillow **12.2.0**; no package installed. Actual rendered adapter:
AMD Radeon 780M, OpenGL Compatibility. Installed executable access and linked
worktree Git metadata required sandbox escalation; no trust/credential change.

| Command | Exit | Evidence / result |
| --- | --- | --- |
| `git fetch origin review/gpt-godot-spike` | 0 (escalated retry) | Initial sandbox attempt reported FETCH_HEAD permission denial; specified review fetched, no push |
| `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a4.md` | 0 | A4 art REJECT, engineering accepted; React suggestion superseded by Owner |
| `PYTHON --version`; `GODOT --version` | 0 | Versions above; installed Pillow import also exited 0 |
| `PYTHON godot-spike/tools/prepare_a5_frames.py --proof` | 1 then 0 | Initial union area budget too small for 00; final fixed-width bands total <4% of canvas; draft saved without changing live PNGs |
| `PYTHON godot-spike/tools/prepare_a5_frames.py --build` | 0 | Five frames, A4 byte archive, hashes, palette distances; rerun during W3 to remove a remaining source-mace fragment and protect exact face pixels |
| `PYTHON godot-spike/tools/a5_style_check.py` | 0 | 200 same-scale region crops, seven-pose strip, six pair colour/garment-IoU proxies |
| `PYTHON godot-spike/tools/a5_audit.py` | 0 | Explicit per-check audit: 5 motion PLACEHOLDER, 2 immutable reference PASS, bag_count=1 on all seven |
| `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 twice | Sync, contact-sheet refresh, final sync; [log](evidence/spike02-a5/sync-run.log); **65** source/copied files byte-equal |
| `PYTHON godot-spike/tools/a5_contact_sheet.py` | 0 | Live manifest contact sheet; no manifest edit |
| `GODOT --headless --path godot-spike --import` | 0 | [Import log](evidence/spike02-a5/import-run.log) |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | **48/48 tests, 2,126 assertions**; [full log](evidence/spike02-a5/test-run.log), no script errors/GUT warnings |
| `PYTHON godot-spike/tools/check_a5_reproduction.py` | 0 | [Log](evidence/spike02-a5/reproduction.log): 5 exact reconstructed PNGs/protection masks/seam masks; zero opaque pixels below y=464 in every motion frame |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a5.gd` | 0 | [720p log](evidence/spike02-a5/rendered-run.log), 13 screenshots, 6 isolated timing runs; `CAPTURE_COMPLETE A5 movie=false runs=6 shots=13 pass=true` |
| `GODOT --path godot-spike --resolution 1920x1080 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a5.gd -- --1080p` | 0 | [1080p log](evidence/spike02-a5/rendered-1080p-run.log), actual 1920x1080 readbacks, same successful completion marker; capture observer sets minimum viewport size |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a5-movie/attack.avi -s res://tools/capture_a5.gd -- --movie-a5` | 0 | [Movie log](evidence/spike02-a5/movie-run.log), `CAPTURE_COMPLETE A5 movie=true runs=1 shots=0 pass=true` |
| `PYTHON godot-spike/tools/package_a5_evidence.py` | 1 then 0 | First attempt tried normalizing its actively redirected Windows log; [retained failure](evidence/spike02-a5/attempt-package-locked-log.log). Exclude active redirect, successful [package log](evidence/spike02-a5/package-run.log): markers, dimensions, timing, parity and decoded movie hold checked |
| `git diff --exit-code cc164b2 -- ui-prototype docs/DECISIONS.md shared-anim/manifest.json shared-anim/thoma/idle/01.png shared-anim/thoma/swing/05.png godot-spike/scripts godot-spike/art/battlefield.png godot-spike/art/props.png` | 0 | React, decisions, reference PNGs, manifest, gameplay, battlefield and props unchanged |
| `git diff --cached --check` before W4 | 2 then 0 | Import progress had trailing spaces; trimmed log whitespace only, all lines retained; no test failure |

Log normalization removes ANSI colour, normalizes UTF-8/LF and trims trailing
progress whitespace; no diagnostic lines are discarded. Initial area rejection
occurred before a draft/live build. W1 draft is preserved; final W3 build uses
two recorded plain-cloth occlusion transfers, no bag-bearing patches. A4
historical tests now use the immutable A4 archive; live A5 assertions are in
test_a5_contract.gd. Assertions were retained, including exact raw RGBA.

### Timing and movie

Manifest remains byte/structure equivalent to A4: 512x512 canvas, pivot
[256,464], contact index 3, head anchor [455,196], swing durations
**180 / 70 / 40 / 80 / 100 / 150 ms**, all other fields unchanged.

| Resolution / mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.956431 s | 0.951041 s | 0.943756 s |
| 720p Reduced Motion | 0.754909 s | 0.720051 s | 0.763822 s |
| 1080p normal | 0.925129 s | 0.956433 s | 0.923250 s |
| 1080p Reduced Motion | 0.743256 s | 0.734362 s | 0.766221 s |

[timing.json](evidence/spike02-a5/timing.json) and
[1080p timing](evidence/spike02-a5/timing-1080p.json) contain all phase/contact
traces. All 12 runs are <=1.7s, return input-ready, and fire spark/SFX/contact
in the same process frame. Hitstop wall time 91.094–93.496ms; process hold
87.5–100ms. Screenshot replays are excluded from these timing measurements.

[attack-60fps.avi](evidence/spike02-a5/attack-60fps.avi) is the complete native
59-frame, 1280x720, 60fps Godot movie, **7,269,540 bytes**, no subsampling.
Strike frame 2 → input-ready frame 57: **0.916667s**. Contact frames 20–24 have
identical complete decoded RGB; frame 25 resumes: **83.333ms** hold. Full
frame hashes, native AVI hash and six PNG samples are in
[movie-index.json](evidence/spike02-a5/movie-index.json) and
[MOVIE.md](evidence/spike02-a5/MOVIE.md). Movie encoding wall time (3.0911s
reported for the attack) is not playback latency; gameplay budget uses the
fixed frame clock and separate real-time runs. Dummy audio was used, so no
physical speaker/headphone audition is claimed.

### Visual evidence and limits

| Pose | 1280x720 | 1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a5/swing-anticipation.png) | [PNG](evidence/spike02-a5/swing-anticipation-1080p.png) |
| Smear | [PNG](evidence/spike02-a5/swing-smear.png) | [PNG](evidence/spike02-a5/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a5/contact.png) | [PNG](evidence/spike02-a5/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a5/follow-through.png) | [PNG](evidence/spike02-a5/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a5/idle.png) | [PNG](evidence/spike02-a5/idle-1080p.png) |

[A4 vs A5](evidence/spike02-a5/contact-sheet-a4-vs-a5.png) is actual native
rendered crops at the same scale, with camera sampling variation between
replays. [Asset comparison](evidence/spike02-a5/asset-sheet-a4-vs-a5.png) is
explicitly separate. [Region sheet](evidence/spike02-a5/region-check.png)
contains idle/recover/A4/A5 source crops at 1:1 and an added row of actual native
720p screenshot crops. [Seven-pose strip](evidence/spike02-a5/sequence-strip.png),
[pair metrics](evidence/spike02-a5/sequence-check.json) and
[audited table](evidence/spike02-a5/frame-status-table.md) retain all failures.
Colour means/IoU cannot establish fold continuity or human acceptance.

[source-hashes.json](evidence/spike02-a5/source-hashes.json) records actual
working-tree and normalized Git LF hashes of gameplay/test/tool code, shared
assets, baseline, rig controls, masks and audit evidence. Original Godot
battlefield/props/party/enemy PNGs match recorded A4 hashes without accessing
React assets. No generated whole-frame art or rejected AI attempt; 0/3 attempts
for every frame. Thoma's mace remains APPROVED canon, unchanged in design.

Executable audit ceiling: explicit Owner-installed console and Python paths
were inspected (console 198,152 bytes, SHA-256
`c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643`;
Python 104,952 bytes, SHA-256
`4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`).
This is local tool identification, not a hardened launcher claim: native child
resolution and inherited process environment were not adversarially audited.
No global trust edits, credential creation, external service or subprocess
launcher added to game code.

Only shared-anim/ and godot-spike/ were edited; Owner brief outside them is
pre-existing. No other worktree, root PLAN/memory, story, P010, ui-prototype,
S4, PR, Actions, merge, deployment or push. Hooks ran normally with the same
report-only missing_canonical_memory advisory. Task DONE is not SessionEnd;
canonical closeout is not claimed. W6 final handoff/table check is recorded
with the handoff, not inferred from this verification commit.

## spike-02 A6

2026-10-24, worktree `D:\campaign-forge\scratch\godot-spike`, branch
`codex/godot-spike`, clean start `438e801` above A5 `78bb38a`. **Engineering
checks pass; art remains PARTIAL.** Complete per-frame generation removes
A5's floating sleeve/hem scraps and disconnected boots. Botanical motifs,
fringe/face fidelity and sequence pops still fail on all five motion frames;
04's mace head is about19px above A5's follow-through pose. All five remain
**PLACEHOLDER**. Exact A5 painted weapon/grip geometry is NOT fully preserved;
that unmet requirement is a recorded art failure, not an engineering PASS.
Human playtest is **HUMAN_PENDING**. Owner chose Godot/P010 accepted; React and
Phase B are **CANCELLED**. No decision record changed.

### Actual commands and exits

Run from this worktree root. `GODOT` means
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`;
`PYTHON` means `C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`.
Godot **4.7.2.stable.official.ed1daf0bf**, OpenGL Compatibility, AMD Radeon780M;
Python3.12.10/Pillow12.2.0 already installed. No installation/global trust edit.
Built-in image_gen returned six unchanged1280x1280 PNGs, true alpha requested;
seed/model/quality not exposed. Exact prompts, settings, three input image
hashes, raw/normalized/runtime hashes and touch-up masks are in
[a6-swing-prompts.json](../../shared-anim/a6-swing-prompts.json) and
[SOURCES](../../shared-anim/SOURCES.md#spike-02-a6--complete-per-frame-regeneration).

| Actual command / operation | Exit | Evidence / result |
| --- | --- | --- |
| `git fetch origin review/gpt-godot-spike`; `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a5.md` and A4 review | 0 | A5 art REJECT, only01 single-frame PASS with playback check pending; obsolete React suggestion superseded by Owner |
| Built-in `image_gen` with idle01/swing05/A5 same-index image references | Returned successfully6 times | 02 two attempts; 00/03/04/01 one each; every raw retained in [candidates](evidence/spike02-a6/candidates/), no rig reconstruction |
| `PYTHON --version` | 0 | Installed absolute path works with authorized sandbox escalation; sandbox name/path lookup denied access first, no fallback installation |
| `PYTHON godot-spike/tools/prepare_a6_frames.py --frame 02 --attempt 1 --scale 0.37155 --tx 25 --ty 35.2 --proof` | 0 | W1 [proof](evidence/spike02-a6/proof-02.png), candidate1 clearly beats broken A5 anatomy; W1 committed before more frames |
| Same normalization tool:02 attempt2, then `--archive`, then00/03/04/01; `adopt_a6_frame.py` per adopted frame | 0 | Exact per-frame scale/translate in JSON; byte-copy A5 archive, alpha<24 cleanup and recorded nearest idle palette remap only |
| `PYTHON godot-spike/tools/record_a6_provenance.py` and `a6_w2_compare.py [--after]` | 0 | Exact prompts/hashes;01 regeneration exception demonstrated in before/after equal-scale neighbours |
| `PYTHON godot-spike/tools/create_a6_capture.py` | 0 | Reuses A5 capture observer, changes evidence/baseline paths, adds post-draw trace; no gameplay changes |
| `GODOT --version`; W3 `--headless --path godot-spike -s res://tools/sync_shared_anim.gd`; `--headless --path godot-spike --import` | 0 | Real-playback prerequisites; [W3 import](evidence/spike02-a6/w3-import.log) |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a6-movie/attack.avi -s res://tools/capture_a6.gd -- --movie-a6` | 0 | W3 movie is retained unchanged as W5 clip; [log](evidence/spike02-a6/w3-playback.log), `CAPTURE_COMPLETE A6 movie=true runs=1 shots=0 pass=true` |
| `PYTHON godot-spike/tools/a6_playback_check.py` | 1 then0 | Initial59-vs58 trace-count failure [retained](evidence/spike02-a6/attempt-playback-trace-count.log); corrected accounting keeps58 observed records, one untraced terminal image exactly equals preceding ready RGB; no invented trace |
| `PYTHON godot-spike/tools/a6_style_check.py` | 0 | [200 source crops](evidence/spike02-a6/region-check.png), seven-frame strip, geometry landmarks, six pair colour/IoU/height proxies, explicit eleven-check audit |
| `PYTHON godot-spike/tools/update_a6_historical_tests.py`; `a6_contact_sheet.py` | 0 | Historical A5 raw-protection assertions retained against A5 archive; contact sheet regenerated from unchanged live manifest |
| `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 | [Final sync log](evidence/spike02-a6/sync-run.log);66 byte-identical source/copied files |
| `GODOT --headless --path godot-spike --import` | 0 | [Final headless import](evidence/spike02-a6/import-run.log) |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | **55/55 tests,2772 assertions**, [complete log](evidence/spike02-a6/test-run.log), no script errors/GUT warnings |
| `PYTHON godot-spike/tools/check_a6_reproduction.py` | 0 | [Reproduction](evidence/spike02-a6/reproduction.log): five exact runtime PNGs and cleanup masks rebuilt from unchanged raw candidates/settings; fixed references, manifest and66-file parity |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a6.gd` | 0 | [720p rendered log](evidence/spike02-a6/rendered-run.log):13 shots,6 separate timing runs; `CAPTURE_COMPLETE A6 movie=false runs=6 shots=13 pass=true` |
| `GODOT --path godot-spike --resolution 1920x1080 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a6.gd -- --1080p` | 0 | [1080p rendered log](evidence/spike02-a6/rendered-1080p-run.log):actual native1920x1080,13 shots,6 runs, same pass marker; no upscaling |
| `PYTHON godot-spike/tools/create_a6_package.py`; `package_a6_evidence.py` | 0 | [Package log](evidence/spike02-a6/package-run.log):actual sizes, pose/hold markers, movie/trace binding, decoded hold, original assets, shared parity and input hashes checked |
| `PYTHON godot-spike/tools/normalize_a6_logs.py` | 0 | UTF8/LF, ANSI/trailing progress-whitespace cleanup only; no diagnostic lines dropped. W3 diff-check reported a blank final log line (exit2); corrected inW4, subsequent check0 |

Sandbox Python probes without escalation failed to locate/access the installed
path, including one package-generator invocation (PowerShell exit1); authorized
explicit-path reruns succeeded. This is tooling access, not package/test failure.
No API key, CLI image fallback, new account or external service was configured.

### Timing and fixed contracts

All durations include hitstop and return to input-ready. These ordinary
rendered runs have no synchronous readback; screenshot replays are excluded.

| Resolution/mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.947969s | 0.945312s | 0.951975s |
| 720p Reduced Motion | 0.752756s | 0.761012s | 0.752048s |
| 1080p normal | 0.942829s | 0.943195s | 0.949734s |
| 1080p Reduced Motion | 0.756074s | 0.760203s | 0.756672s |

All12 are below1.7s; contact spark/SFX/flash share a process frame, input returns,
hitstop wall91.803–106.804ms. [720p timing](evidence/spike02-a6/timing.json),
[1080p timing](evidence/spike02-a6/timing-1080p.json). Fixed manifest unchanged:
512x512, pivot[256,464], contact index3/anchor[455,196], durations
**180/70/40/80/100/150ms**, same offsets/camera/impact/scenarios and Reduced
Motion indices[0,3,5] omit smear02. Immutable idle01 and swing05 match the
fixed A5 SHA-256 values byte for byte. No baseline path in live manifest.

[Native movie](evidence/spike02-a6/attack-60fps.avi):59 complete1280x720 frames,
60FPS, **7,272,456 bytes**, no subsampling/transcoding. Strike frame2 → ready57
is **0.916667s**; contact frames20–24 have identical complete decodedRGB for
**83.333ms**, frame25 resumes. [MOVIE](evidence/spike02-a6/MOVIE.md),
[decoded hashes](evidence/spike02-a6/movie-index.json). W3 playback checks and
W5 clip have the same native movie hash. Encoding wall time is not latency;
Dummy audio is not physical-device audition. The post-draw trace has58 actual
records and one explicitly untraced final equal-pixel movie frame.

### Visual evidence and limits

| Pose | 1280x720 | 1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a6/swing-anticipation.png) | [PNG](evidence/spike02-a6/swing-anticipation-1080p.png) |
| Smear | [PNG](evidence/spike02-a6/swing-smear.png) | [PNG](evidence/spike02-a6/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a6/contact.png) | [PNG](evidence/spike02-a6/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a6/follow-through.png) | [PNG](evidence/spike02-a6/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a6/idle.png) | [PNG](evidence/spike02-a6/idle-1080p.png) |

[A5-vs-A6](evidence/spike02-a6/contact-sheet-a5-vs-a6.png) uses native320px
viewport crops from actual replays at identical resolution/crop; camera
sampling varies between replays. [Asset comparison](evidence/spike02-a6/asset-sheet-a5-vs-a6.png)
is separately labeled. [Region sheet](evidence/spike02-a6/region-check.png)
contains1:1 crops for stole, embroidery, cuffs, hem, seams, bag, feet, face/hair,
palette and mace against idle01/recover05/A5, plus actual native720p crops.
[Sequence strip](evidence/spike02-a6/sequence-strip.png),
[every actual rendered frame](evidence/spike02-a6/playback-every-frame.png),
[keyposes](evidence/spike02-a6/playback-keyframes.png),
[sequence metrics](evidence/spike02-a6/sequence-check.json) and
[observations](evidence/spike02-a6/W3-OBSERVATIONS.md) preserve failures.
Colour/IoU/height proxies include pose/occlusion and cannot approve anatomy.

55 passing tests prove their covered engine/data contracts, **not** commercial
art, exact generated mace geometry, complete sequence fidelity or human feel.
[Source hashes](evidence/spike02-a6/source-hashes.json) bind working-tree/GitLF
code, reference/raw/adopted frames, masks and evidence inputs.
[Package audit](evidence/spike02-a6/evidence-audit.json) explicitly records
art PARTIAL, five PLACEHOLDER,04 geometry failure and HUMAN_PENDING.
No other character, knight, battlefield, prop, HUD, rules, game script, source
atlas, ui-prototype, story, P010 or other worktree changed. No push/PR/merge/
Actions/deploy/stash/PhaseB. Hooks ran normally; report-only memory advisory
does not prove SessionEnd or canonical closeout. W6 records the final handoff
table check; this verification is not a session-end claim.

## spike-02 A7

2026-10-24, `codex/godot-spike`, only worktree
`D:\campaign-forge\scratch\godot-spike`; clean start at brief `645ede1` over
A6 `e233171`. W1–W4 commits: `b711b3f`, `34e1260`, `40ced11`, `926e006`.
**Engineering/data checks pass; art FAIL. All five motion frames remain
PLACEHOLDER.** The unified anchor spec and source-interior corrections do not
achieve stable full face/hair, exact stole/motif/fringe, seam-free transfers or
continuous motion. 02 has a misregistered right sprig; 04 has a visible cuff
bridge, a seam regression from A6. These failures are recorded, not excused by
native sprite size or passing tests. Human feel remains **HUMAN_PENDING**.

Owner chose Godot directly (P010 accepted in Owner instruction), cancelled
React/Phase B, and approved Thoma's short one-handed flanged mace as canon.
The stale P010 text in this worktree's decision file was **not edited**.

### Actual commands, results and retained failures

Commands below ran from this worktree. `GODOT` abbreviates the exact installed
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`;
`PYTHON` abbreviates
`C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`.
Versions: Godot **4.7.2.stable.official.ed1daf0bf**, Python **3.12.10**.

| Command / operation actually run | Exit / result | Evidence |
| --- | --- | --- |
| `git fetch origin review/gpt-godot-spike`, then `git show` A6 and A5 reviews | Escalated fetch0; both shows0 | Review head `3f29156`; A6 REJECT0/5, A5 only01 single-frame PASS. Initial sandbox fetch denied FETCH_HEAD access; individual exit not retained in the combined read command |
| `PYTHON --version`; `GODOT --version` | 0 | Existing installed tools, no installation/API key/global trust edit |
| `PYTHON godot-spike/tools/build_a7_spec.py` | 0 | [Spec](../../shared-anim/thoma-appearance-spec.md), JSON, [source crops](evidence/spike02-a7/spec-crops.png), [pose overlay](evidence/spike02-a7/pose-targets.png); only two anchor PNGs determine appearance |
| Built-in `image_gen` EDIT with A6 target and two appearance anchors | Five successful returns | Order01,02,00,03,04; all unchanged1254x1254 returns retained in [attempts](evidence/spike02-a7/attempts/). Reframed target geometry: raw generated pixels NOT adopted |
| `PYTHON godot-spike/tools/prepare_a7_frames.py --archive --prepare 01`, then per-frame `--record`, `--finish`, next `--prepare` | 0 except initial01 finish1 | Missing `json` import at SOURCES append, after saving PNG/attempt JSON; repaired missing append without new generation. [Operations record](evidence/spike02-a7/W2-OPERATIONS.md) |
| `PYTHON godot-spike/tools/refine_a7_followthrough.py` | 0 | First04 extraction left duplicate head/haft; rejected image retained. Local second attempt removes duplicate and translates original connected weapon19px, no rescale; cuff bridge still FAIL |
| `PYTHON godot-spike/tools/a7_style_check.py`; `create_a7_capture.py` | 0 | [Every required check](evidence/spike02-a7/spec-check.json), [landmark deltas](evidence/spike02-a7/landmark-deltas.md), [method](evidence/spike02-a7/METHOD.md); capture observer changes evidence/baseline paths only |
| W3 `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd`; `--headless --path godot-spike --import` | 0 /0 | Prerequisites for real rendered playback; w3-sync.log /w3-import.log |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a7-movie/attack.avi -s res://tools/capture_a7.gd -- --movie-a7` | 0 | [W3 log](evidence/spike02-a7/w3-playback.log), `CAPTURE_COMPLETE A7 movie=true runs=1 shots=0 pass=true`; retained unchanged for W5 |
| `PYTHON godot-spike/tools/a7_playback_check.py` | 0 | Actual59 rendered frames,58 post-draw traces, one terminal frame equal to preceding ready pixels; [playback](evidence/spike02-a7/playback-check.json) art FAIL. Pillow getdata deprecation warning retained in tool output; not an execution failure |
| `PYTHON godot-spike/tools/update_a7_historical_tests.py`; `a7_contact_sheet.py` | 0 | All historical A6 assertions retained against byte-copy archive; live A7 has eight new tests |
| W4 `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 | [Sync log](evidence/spike02-a7/sync-run.log), **69** copied files byte-equal |
| `GODOT --headless --path godot-spike --import` | 0 | [Import log](evidence/spike02-a7/import-run.log) |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | 0 | **63/63 tests,4,883 assertions**, [complete log](evidence/spike02-a7/test-run.log), no script errors/GUT warnings |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a7.gd` | 0 | [Rendered720p log](evidence/spike02-a7/rendered-run.log),13 shots/6 timing runs, successful completion marker |
| `GODOT --path godot-spike --resolution 1920x1080 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a7.gd -- --1080p` | 0 | [Rendered1080p log](evidence/spike02-a7/rendered-1080p-run.log),13 real native1920x1080 readbacks,6 timing runs, successful marker |
| `PYTHON godot-spike/tools/package_a7_evidence.py` | 0 | [Package log](evidence/spike02-a7/package-run.log): markers, timing, dimensions, byte parity, input hashes, movie decoding/hold verified; integrity PASS, art FAIL |
| `PYTHON godot-spike/tools/normalize_a7_logs.py` | 0 | UTF8/LF, ANSI/trailing whitespace only; diagnostic lines retained |

### Fixed contracts, timing and movie

The full manifest is unchanged: canvas512x512, registration pivot[256,464],
contact index3 and anchor[455,196], durations **180/70/40/80/100/150ms**, original
offsets/impact/camera/scenarios. Reduced Motion[0,3,5] still omits smear02.
Both anchor SHA-256 values are fixed and tested. Both boots/lower leg pixels
below y420 are byte-identical to A6; all poses retain one satchel. Contact
weapon pixels are unchanged. 04's original head/haft/grip translate19px without
resizing: head[420.72,357.384] → [420.72,376.384], target[421,376], error0.475px.
Full joint/hand/foot target compliance and cuff continuity still FAIL.

| Resolution / mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.925297s | 0.928701s | 0.905224s |
| 720p Reduced Motion | 0.727183s | 0.722318s | 0.747849s |
| 1080p normal | 0.923951s | 0.907859s | 0.931091s |
| 1080p Reduced Motion | 0.729055s | 0.748579s | 0.725249s |

All12 no-readback runs return input-ready and are below1.7s. Contact
spark/SFX/flash share the same process frame; hitstop wall82.526–99.136ms.
[720p timing](evidence/spike02-a7/timing.json),
[1080p timing](evidence/spike02-a7/timing-1080p.json).

[Native movie](evidence/spike02-a7/attack-60fps.avi): **59 frames,1280x720,60FPS,
7,272,394 bytes**, no subsampling/transcoding. Strike2 → ready57 =0.916667s.
Contact20–24 full decodedRGB identical, **83.333ms** hold; frame25 resumes.
[MOVIE notes](evidence/spike02-a7/MOVIE.md), [frame hashes](evidence/spike02-a7/movie-index.json).
The movie log's2.5476s encoding/render wall time is not gameplay latency.
Dummy audio is not a physical-device audition; human feel is HUMAN_PENDING.

### Visual evidence and limits

| Pose | 1280x720 | 1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a7/swing-anticipation.png) | [PNG](evidence/spike02-a7/swing-anticipation-1080p.png) |
| Smear | [PNG](evidence/spike02-a7/swing-smear.png) | [PNG](evidence/spike02-a7/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a7/contact.png) | [PNG](evidence/spike02-a7/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a7/follow-through.png) | [PNG](evidence/spike02-a7/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a7/idle.png) | [PNG](evidence/spike02-a7/idle-1080p.png) |

[A6 vs A7](evidence/spike02-a7/contact-sheet-a6-vs-a7.png) uses equal native
rendered crops; camera sampling can vary across replays. The separately labelled
[512px source comparison](evidence/spike02-a7/asset-sheet-a6-vs-a7.png),
[spec crops/checks](evidence/spike02-a7/spec-check.png),
[transparent sheet](evidence/spike02-a7/equal-scale-transparent-sheet.png),
[sequence strip](evidence/spike02-a7/sequence-strip.png),
[every rendered frame](evidence/spike02-a7/playback-every-frame.png) retain the
failures. Region RGB deltas measure real readbacks under source-alpha masks;
IoU is labelled source silhouette occupancy, not a rendered segmentation.
Manual landmarks/height and proxy values cannot establish stable anatomy.

[Provenance](../../shared-anim/a7-swing-prompts.json) records every raw prompt,
three inputs/hashes, seed/settings not exposed, all local masks/intermediate
hashes and raw/runtime hashes. Counts01/02/00/03=1,04=2 (one image_gen EDIT per
frame, plus one local04 correction). Attempt2's inherited normalization preview
describes its origin imagegen return; the local operation is unit-scale19px
translation, not that preview transform. No generated raw return is adopted.
[Source hashes](evidence/spike02-a7/source-hashes.json) bind code, anchors,
raw/edited frames, baseline and audit inputs (working-tree and GitLF hashes).
[Evidence audit](evidence/spike02-a7/evidence-audit.json) explicitly reports art
FAIL/seam regression/five PLACEHOLDER/HUMAN_PENDING. Tests prove covered engine
and provenance contracts; they do not prove art acceptance.

Executable identification: Python104,952 bytes/SHA-256
`4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`;
Godot console198,152 bytes/SHA-256
`c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbE846643`
(hex case immaterial). Explicit absolute installed paths used; sandbox
escalation allowed local tools and linked-worktree Git metadata. This is
tool identification, not adversarial launcher/environment hardening or global
trust approval. No process launcher was added to game code.

No ui-prototype, story/decision records, game scripts/HUD/rules, knights,
battlefield/props or original PNG/evidence was changed. Only shared-anim/ and
godot-spike/ plus the pre-existing task brief differ from e233171. No push,
PR, main merge, Actions, deploy, stash or PhaseB. Normal commit hooks emitted
report-only missing_canonical_memory advisory; commit is not SessionEnd and no
canonical closeout is claimed. W6 independently checks final handoff/table.

## spike-02 A8

**Engineering/evidence PASS; complete art acceptance FAIL,0/5.** A single
brief-driven seven-panel sheet generated all five middle poses together in
each of three built-in EDIT calls. Attempt3 supplies every adopted body. The
shared painting improves cross-panel surface consistency over A7's texture
patches, but it still changes anchor face/hair, stole, embroidery/fringe and
stance. Local weapon reconstruction meets target locations but not all design/
brush-continuity requirements. Every middle frame remains PLACEHOLDER.
Human hit-feel is HUMAN_PENDING; Owner art approval is pending. The human
commission brief remains valid and needed as a fallback, untouched.

### Actual commands and exit codes

Worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`,
clean initial commit `a1cba50` above `fdc796b`. No remote operation was run.
`PYTHON` means
`C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`;
`GODOT` means
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`.
Godot identifies itself as4.7.2.stable.official.ed1daf0bf, Compatibility/
AMD Radeon780M. No executable launcher or dependency was added to game code.

| Command / operation actually run | Exit / observed result | Evidence |
| --- | --- | --- |
| Initial sandbox Python and git add/commit attempt | Combined1; denied installed Python and linked gitdir index.lock; no commit | Scoped approved escalation used thereafter |
| `PYTHON godot-spike/tools/prepare_a8_sheet.py` | 0 | [W1 inputs](evidence/spike02-a8/inputs/), exact anchor pixels, guides, mask, layout/prompt hashes; archived A7 PNGs |
| `PYTHON godot-spike/tools/adopt_a8_sheet.py --prepare 1`, then2, then3 | 0 | [Three attempt records](evidence/spike02-a8/sheet-attempts/); flat A7 alpha silhouette for pose only in2/3 |
| Built-in `image_gen` EDIT with sheet, mask, anchor/crop references | Three successful1774×887 returns | [Provenance](../../shared-anim/a8-swing-prompts.json); all whole sheets saved; seed/model not exposed; no per-frame fallback |
| `PYTHON godot-spike/tools/adopt_a8_sheet.py --slice 3 --adopt 3` (slice and adoption executed in separate calls) | 0/0 | Uniform scale/translate only; local mace fixes have input/output/mask/donor hashes |
| `PYTHON godot-spike/tools/adopt_a8_sheet.py --cleanup-residuals` | Initial1 (missing Path import), corrected0 | Original outputs preserved;01/04 old shaft slivers removed; correction commit precedes W3 |
| Exploratory `PYTHON -c "import numpy; ..."`; read nonexistent `check_a7_frames.py` | 1/1 | No numpy installed; no installation, Pillow/stdlib used; existing tools read instead |
| `PYTHON godot-spike/tools/a8_style_check.py` | 0 | [Checklist](evidence/spike02-a8/checklist.json), crops, landmark table, transparent sequence, source comparison; five honest PLACEHOLDER |
| W3 `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd`; `GODOT --headless --path godot-spike --import` | 0/0 | w3-sync.log / w3-import.log; prerequisites for actual flicker evidence |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a8-movie/attack.avi -s res://tools/capture_a8.gd -- --movie-a8` | First process0 but writer errors: REJECTED; after creating output directory,0 and valid movie | [Failed writer log](evidence/spike02-a8/w3-playback-failed-1.log), [successful log](evidence/spike02-a8/w3-playback.log); completion marker alone was insufficient |
| `PYTHON godot-spike/tools/a8_playback_check.py` | Initial1 missing explicit imports, corrected0 | [Actual720p flicker](evidence/spike02-a8/playback-check.json),59 decoded frames, seven poses/six pairs, RGB/source-IoU/height proxies; art FAIL |
| `PYTHON godot-spike/tools/update_a8_historical_tests.py`; `PYTHON godot-spike/tools/a8_contact_sheet.py` | 0/0 | All eight A7 tests retained against archived frames/audit; live contact sheet regenerated |
| W4 `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd`; `GODOT --headless --path godot-spike --import` | 0/0 | [Sync](evidence/spike02-a8/sync-run.log),70 files; [import](evidence/spike02-a8/import-run.log) |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | **0,71/71 tests,5729 assertions,12 scripts** | [Full GUT log](evidence/spike02-a8/test-run.log), no script errors/GUT warnings |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a8.gd` | 0;6 timing runs/13 shots; marker pass=true | [720p log](evidence/spike02-a8/rendered-run.log), native readbacks |
| `GODOT --path godot-spike --resolution 1920x1080 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a8.gd -- --1080p` | 0;6 timing runs/13 shots; marker pass=true | [1080p log](evidence/spike02-a8/rendered-1080p-run.log), root viewport explicitly1920×1080, no upscaling |
| `PYTHON godot-spike/tools/package_a8_evidence.py` | 0 | [Integrity audit](evidence/spike02-a8/evidence-audit.json),70 byte-equal shared files,26 native shots, movie/hold/centroids/provenance/hash checks |
| `git diff --check`; restricted-path/engine diff checks against `fdc796b` | 0; no protected-path or game-code changes | Changes only shared-anim/, godot-spike/ and pre-existing A8 task brief |

W3 reused the successful movie for W5 rather than recording another identical
asset state. The two real-time screenshot processes overlapped while running;
their separate suffixes/output files avoid collisions. Resource contention may
affect wall time; no isolated performance-benchmark claim. Both still meet the
1.7s budget. Pillow getdata deprecation warnings are retained, not hidden errors.

### Fixed mechanics and measured timing

Full manifest data unchanged:512×512, registration pivot[256,464], contact index3,
anchor[455,196],180/70/40/80/100/150ms, same offsets/events/scenarios,80ms hitstop,
Reduced Motion[0,3,5]. Runtime idle01/recover05 retain exact original SHA-256.
All five middle PNGs are RGBA/transparent,361px normalized head-to-ground, feet
on464, and opaque bottom463–465. No archived frame is referenced by manifest.

| Resolution / mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.917871s | 0.916045s | 0.943971s |
| 720p Reduced Motion | 0.754644s | 0.745684s | 0.747847s |
| 1080p normal | 0.930527s | 0.944785s | 0.938591s |
| 1080p Reduced Motion | 0.780435s | 0.815044s | 0.768823s |

All12 no-readback timing runs return input-ready with same-frame feedback.
Hitstop wall91.069–107.246ms. [Timing720p](evidence/spike02-a8/timing.json) /
[1080p](evidence/spike02-a8/timing-1080p.json). No screenshot readback is included
in these elapsed times. The native60FPS movie is59 frames,7,273,022 bytes,
strike2→ready57 =0.916667s, contact20–24 identical decodedRGB =83.333ms;25 resumes.
No subsampling/transcoding. [AVI](evidence/spike02-a8/attack-60fps.avi),
[movie index](evidence/spike02-a8/movie-index.json), [notes](evidence/spike02-a8/MOVIE.md).

### Visual evidence and limitations

| Pose | Native1280×720 | Native1920×1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a8/swing-anticipation.png) | [PNG](evidence/spike02-a8/swing-anticipation-1080p.png) |
| Swing/smear | [PNG](evidence/spike02-a8/swing-smear.png) | [PNG](evidence/spike02-a8/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a8/contact.png) | [PNG](evidence/spike02-a8/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a8/follow-through.png) | [PNG](evidence/spike02-a8/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a8/idle.png) | [PNG](evidence/spike02-a8/idle-1080p.png) |

All captures include CAPTURE_COMPLETE checks, pose indices, resolution and
hold-active evidence. The original-asset comparison is separately labelled:
[checklist crops](evidence/spike02-a8/checklist.png),
[A7 above A8](evidence/spike02-a8/contact-sheet-a7-vs-a8.png),
[transparent sequence](evidence/spike02-a8/sequence-strip.png),
[style sheet](../../shared-anim/thoma-weapon-style-check.png),
[landmarks](evidence/spike02-a8/landmark-deltas.md).
W3 reports the transformed donor-head centroid; W5 additionally measures
independent final-PNG head-ROI alpha centroids in
[final-mace-centres.json](evidence/spike02-a8/final-mace-centres.json), all within4px.
That ROI includes small shaft/antialiasing overlap; neither metric certifies
weapon projection or brush consistency. Hidden joints are estimates±12px,
visible picks±2px, so full4px pose compliance remains FAIL.

The image tool has no independent mask parameter: W1 mask was supplied as an
image/prose constraint. It repainted both anchor panels in all three attempts.
Original runtime anchors are byte-identical; generated copies are never used.
No per-frame fallback, no final artist-editable layered source, no human art/
feel approval. This AI pass does not establish a successful production pipeline.

No ui-prototype/, docs/art-briefs/, story/decision records, game scripts/HUD,
knights, battlefield, props or previous-segment evidence changed. G005 unchanged.
No push, main merge, PR, deployment, Actions, stash, new slice or engine rule.
Normal commit hooks emitted report-only missing_canonical_memory advisory;
task handoff is not SessionEnd. Explicit segment scope excludes PLAN/memory edits.


## spike-02 A9

**Engineering/evidence PASS; full art acceptance FAIL,0/5.** A8 is the base,
with enforced local masks and original anchor-pixel transplants. The authorized
Python/manual-blend option was used: zero image_gen calls, zero whole-frame or
whole-sheet regeneration. Four head identities and two uncompressed mace
regions improve; costume/pose repairs did not integrate and were rolled back.
All five motion frames remain PLACEHOLDER. HUMAN_PENDING; Owner art approval
pending. The commission brief is untouched and still needed as the fallback.

### Actual environment and commands

Worktree D:\campaign-forge\scratch\godot-spike; branch codex/godot-spike;
clean start8b6d957 on A8 dcc949c. No fetch/push/remote mutation or branch change.
`PYTHON` = C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe
(Pillow12.2.0); `GODOT` =
C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe.
Installed binaries required scoped sandbox escalation. No trust store/config,
launcher, install, new addon or external material changed.

| Command actually run | Real exit / result | Evidence |
| --- | --- | --- |
| `PYTHON godot-spike/tools/prepare_a9_regions.py` | 0 | baseline-a8/,42 initial masks, full13-item regression baseline/targets |
| `PYTHON godot-spike/tools/fix_a9_regions.py --prepare NN`, `--refine NN`, `--decide NN --accept ...` | All0; order03,02,04,00,01 |44 initial operation records; source/head/motif trial PNGs/masks/transforms |
| Same tool `--withdraw 03 embroidery` | 0 | Third operation explicitly restores A8 motif after adjacent review |
| Same tool `--mace-refine 00` / `01`; `--head-final 01` | 0 /0 /0 | Canon rigid mace2 kept; head01 trial3 rejected |
| `PYTHON godot-spike/tools/a9_style_check.py` | 0, rerun after measurement/alpha corrections | checklist, A8->A9 item changes, landmark deltas, comparison/style sheets |
| `PYTHON godot-spike/tools/prepare_a9_capture.py` | 0 | Proven A8 post-draw capture reused with A9 output and A8 comparison |
| `GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd` | 0 each;70 files | w3-sync.log / sync-run.log, final parity independently verified |
| `GODOT --headless --path godot-spike --import` | 0 each | w3-import.log / import-run.log |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike02-a9-movie/attack.avi -s res://tools/capture_a9.gd -- --movie-a9` | 0 before and after alpha cleanup; pass=true marker, valid decodable AVI | w3-playback.log; prior movie under pre-alpha-cleanup/ |
| `PYTHON godot-spike/tools/a9_playback_check.py` | 0 each | Real59-frame720p RGB under recorded masks, seven poses/six adjacent pairs; art FAIL |
| `PYTHON godot-spike/tools/update_a9_historical_tests.py`; `PYTHON godot-spike/tools/a9_contact_sheet.py` | 0 /0 | All eight A8 historical tests retained; live contact sheet regenerated |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | First1 (78/79); second0 with type warning; third0,79/79; after alpha correction0,79/79 | Final test-run.log: 7948 assertions,13 scripts, no warnings/errors; prior runs retained |
| Independent Python alpha component scans, then `PYTHON godot-spike/tools/fix_a9_regions.py --alpha-final` | Scans0; cleanup0 | Detected new1px01 mace /2px04 head fragments; two recorded final regional attempt3 operations;46 total |
| `GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a9.gd` | 0 before/after cleanup;6 runs/13 shots/pass=true | rendered-run.log / timing.json; original capture retained |
| `GODOT --path godot-spike --resolution 1920x1080 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a9.gd -- --1080p` | 0 before/after cleanup;6 runs/13 shots/pass=true | rendered-1080p-run.log / timing-1080p.json; actual1920x1080 root viewport, no upscaling |
| `PYTHON godot-spike/tools/package_a9_evidence.py` | 0 before cleanup and final0 | Every changed attempted pixel inside its mask, complete kept-region reconstruction,70 byte-equal shared files,26 native shots, hold/movie/timing verification |
| `git diff --check`; protected-path/engine/manifest/anchor diff against dcc949c | 0; no protected-path changes | Only shared-anim/,godot-spike/ and pre-existing task brief differ |

First new test failure was test authoring: grayscale masks have opaque alpha
on black too; get_used_rect() was replaced by actual white-pixel counting.
Recorded no-op regions may have empty transform lists. JSON movie frame-count
threshold was made float to remove a Float/Int warning. All prior failures
are retained, no old assertions deleted. Read-only Win32_Process access was
denied; Get-Process fallback did not expose another Codex/Claude executable,
which cannot certify absence of desktop sessions. Initial sandbox Python probe
failed1; scoped authorized execution then worked. No permissions/trust changed.

### Final alpha, mechanics and timing

The independent W5 alpha scan found two new tiny detached opaque clusters.
Their tiny recorded rectangle cleanups consume the final allowed attempt on01
mace and04 head; they never change face interiors, the body or weapon scale.
Original candidates/captures survive in attempts/ and pre-alpha-cleanup/.
All assets/audits, full GUT and both rendered captures were regenerated after
this finding. alpha-components.json reports the final4-neighbour alpha>127
scan: zero new tiny fragments;02 retains only its exact A8 diagonal-edge pixels.
This scan is a regression proxy, not a universal halo detector.

Full manifest equality preserved:512x512, straight RGBA, pivot[256,464],
ground464, contact index3, anchor[455,196],180/70/40/80/100/150ms,80ms hitstop,
Reduced Motion[0,3,5], same offsets/events/setups. Both anchor SHA-256 unchanged.
All final mace centroids within4px; contact455,196 opaque. Original stance
targets still fail; tests do not turn that into art approval.01 headtop reuses
A8's manual103px because the raised mace crosses the automatic head ROI.

| Resolution / mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.909355s | 0.929085s | 0.946548s |
| 720p Reduced Motion | 0.749362s | 0.680090s | 0.717853s |
| 1080p normal | 0.919576s | 0.919482s | 0.918028s |
| 1080p Reduced Motion | 0.717850s | 0.735911s | 0.717906s |

All12 no-readback runs return input-ready with same-frame contact feedback,
under1.7s. Native60FPS AVI: 59 frames,7,273,008 bytes,
strike2 ->ready57 =
0.916667s. Identical decoded contact RGB
frames20-24 = 83.333ms;
next frame resumes. No transcoding/subsampling; movie wall time includes
encoding, not game latency.720p/1080p real-time processes ran sequentially.

### Evidence / claim ceiling

[Integrity audit](evidence/spike02-a9/evidence-audit.json), [source hashes](evidence/spike02-a9/source-hashes.json),
[movie](evidence/spike02-a9/attack-60fps.avi), [movie index](evidence/spike02-a9/movie-index.json),
[timing720p](evidence/spike02-a9/timing.json), [1080p](evidence/spike02-a9/timing-1080p.json).

| Pose | Native1280x720 | Native1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a9/swing-anticipation.png) | [PNG](evidence/spike02-a9/swing-anticipation-1080p.png) |
| Swing/smear | [PNG](evidence/spike02-a9/swing-smear.png) | [PNG](evidence/spike02-a9/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a9/contact.png) | [PNG](evidence/spike02-a9/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a9/follow-through.png) | [PNG](evidence/spike02-a9/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a9/idle.png) | [PNG](evidence/spike02-a9/idle-1080p.png) |

Source comparison sheets are labelled separately from actual run captures.
Rendered region RGB is measured through transformed W1/source-alpha masks;
silhouette IoU is SOURCE occupancy, not segmentation of rendered RGB. Hidden
joints remain estimates+/-12px. Full pose/sequence FAIL and all five
PLACEHOLDERs remain; no final layered artist source, no full battle, no human
feel test or Owner art approval. Dummy audio is not a hardware audition.
The human commission brief remains needed and unchanged.

No original anchor, earlier A2-A8 evidence, ui-prototype/, art-brief, story,
decision, rule, HUD, timing, environment, knight or G005 change. No push,
merge, PR, stash, Actions, deployment, new task or session-end claim.
Commit hooks run normally; report-only missing_canonical_memory advisory is
documented, not bypassed. Explicit segment scope excludes PLAN/memory edits.

W6 final table check: GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a9_contract.gd -gexit returned0,8/8,2219 assertions,no warnings. See evidence/spike02-a9/handoff-table-check.log. Final metadata-only source/raw hash binding was synchronized (w6-sync.log,0) and independently rechecked by package_a9_evidence.py (0); no PNG or game code changed after W5 capture. W5 full suite remains79/79,7948 assertions.

## spike-03

Implemented layered hit feedback without touching A9 animation art or rules;
big-map work is a proposal plus a separate throwaway camera scene. The larger
map is not connected to gameplay. Human hit-feel is **HUMAN_PENDING** and the
map option is **OWNER_PENDING**, independent of the automated results below.

Worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`,
clean start `20d9844` on `b2f460b`. The Owner explicitly named this base and
authorized W1–W7 local commits, no push. Initial sandbox fetch failed because
FETCH_HEAD is outside the writable root; scoped `git fetch origin` then exited
0, remote task branch also `20d9844`. No conflicting remote commits, branch
switch, other worktree writes, main merge, PR, stash, deployment or Actions.
Process command-line inspection was denied; process names alone cannot certify
other desktop-session worktree ownership. Work proceeded under the Owner's
explicit autonomous worktree confirmation; no absence-of-other-sessions claim.

### Tools and actual commands

From the worktree root, `GODOT` below abbreviates the exact executable actually
called with PowerShell `&`:

`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`

It reports `4.7.2.stable.official.ed1daf0bf`. `PYTHON` abbreviates the existing
`C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe`, Pillow 12.2.0.
Installed executables needed scoped sandbox execution; no installation, launcher,
global trust/config, dependency or addon was changed. ffmpeg was not on PATH;
Pillow builds the review GIF and decodes existing MJPEG AVI chunks.

| Command actually run (same flags; stdout/stderr saved) | Real exit / result | Evidence |
| --- | --- | --- |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike03-before/attack.avi -s res://tools/capture_spike03.gd -- --output=before` | 0; W1 original code,56 sampled frames | `before/w1-timeline.json`, W1 commit `4ca7bfb` |
| Same with `-- --output=before --impact-profile=a9_baseline` after W2 | 0;58 AVI frames,56 sampled frames | `before/capture.log`, baseline profile recorded in JSON |
| Same movie command with `.godot/spike03-after/attack.avi` / `--output=after` | 0 initial and repeat;60 AVI frames | `pre-number-placement/after/`, final `after/` |
| Same movie command with `.godot/spike03-after-crit/attack.avi` / `--output=after-crit --crit` | 0 initial and repeat;64 AVI frames | trial and final `after-crit/` |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --max-fps 60 -s res://tools/capture_spike03.gd -- --timing` | 0;9 runs,0 readbacks,pass=true | `timing-run.log`, `timing.json` |
| `GODOT --path godot-spike --resolution 1920x1080 --audio-driver Dummy --max-fps 60 -s res://tools/capture_spike03.gd -- --still1080` | 0 initial and repeat;actual1920×1080 | `still1080-inline-encoding.log` then `still1080-run.log`, `contact-1080.png` |
| `PYTHON godot-spike/tools/package_spike03.py` | 0 | Strips, 5,262,076-byte GIF, unchanged AVI copies/indices, rejected trial retention |
| `GODOT --headless --path godot-spike --import` | 0 each W2/W3/W5/W6 | `w2-import.log`, `import-run.log`, `w5-import.log`, `w6-import.log` |
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | W2 0:79/79;W3 0:88/88 twice;W6 first1:88/89,final0:**89/89**,8958 assertions,15 scripts | `w2-test-run.log`, W3 logs, `w6-tests-pre-hintfix.log`, final `test-run.log` |
| Same GUT command with `-gtest=res://tests/test_spike02.gd -gexit` | First1 (compile error);final0,6/6 | `w2-pause-test.log`, `w2-pause-test-final.log` |
| Same with `-gtest=res://tests/test_spike03_impact.gd -gexit` | 0;9/9 after crit-indicator correction | `w3-final-impact-test.log` |
| Same with `-gtest=res://tests/test_big_map_mockup.gd -gexit` | 0;one smoke,34 assertions | `w5-mockup-test.log` |
| `GODOT --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_big_map.gd` | First0 with directory error,not accepted;repeat0,no error,7 screenshots/7 true checks | `w5-capture-pre-pathfix.log`, final `w5-capture.log`, proposal `capture.json` |
| `PYTHON godot-spike/tools/audit_spike03.py` | First1 refused failing suite;next1 indentation error;then0 (Pillow deprecation notice),final clean repeat0 | Historical audit logs retained; `audit.json`, `audit-run.log`, `source-hashes.json` |
| `git diff --stat b2f460b..HEAD`; protected-path `git diff --name-only b2f460b` and `git diff --check` | Scope0,protected paths empty; whitespace first2 from raw-log trailing spaces/blank EOF,final0 after log normalization | `changed-paths.txt`, source hashes and scope records |

All evidence paths in the table are under `docs/evidence/spike03/` unless noted.
PowerShell capture logs were normalized from UTF-16/ANSI to readable UTF-8 text,
trimming trailing spaces and excess blank EOF lines;
actual results and failures were retained. No earlier test was deleted,
re-pointed, or weakened. Final import/test/capture logs contain no engine errors.

### What changed and what the evidence proves

`ImpactProfile` exports all layer tuning; the baseline resource preserves every
A9 impact/camera/number/particle/SFX constant, and manifest.impact remains the
historical record. Normal uses110ms and crit170ms whole-world hitstop; Reduced
Motion keeps80ms. Attacker and target minima are both110ms, with the larger
configured minimum governing the pausable world; the HUD/root remains always
processing. Native still/movie freezes, clocks and UI regression tests agree.
The real-time and process-time minimum guard stays in place.

Shake is an8px first kick along attacker→target (crit12), three deterministic
oscillations over200ms with exponential decay4, then exact zero. These are
Camera2D offset units at the reference canvas; attack zoom scales their visible
screen displacement. Full warm flash, visual-only9px recoil, immediate flare,
sparks plus contact dust, number pop and +0.06 zoom punch share frame03. Named
whoosh/impact/crit/landing hooks are original PLACEHOLDER synthesis.
Reduced Motion has no shake/zoom/recoil/flash/sparks/dust; it keeps00/03/05 and
the stationary number can scale. Rules damage stays2 even with C crit on.

Final actual720p normal/crit AVIs are60/64 frames; their strike→ready spans are
57/61 frames (0.950000/1.016667s), compared with A9 baseline55 (0.916667s).
Frame-indexed decoded AVI and native PNGs hold identically for5/7/11 frames.
AVI is lossy MJPEG: mean absolute RGB difference vs indexed native PNG is below
4/255 per channel; this is an alignment check, not lossless pixel equality.
146 native PNGs cover contact−8 through ready across the three final sequences.

| Mode | Fixed60FPS seconds, open / unit / terrain | No-readback wall seconds |
| --- | --- | --- |
| Normal | .950000 / .950000 / .950000 | .928577 / .918207 / .920291 |
| Crit presentation | 1.016667 / 1.016667 / 1.016667 | .987982 / .983269 / .975860 |
| Reduced Motion | .716667 / .716667 / .716667 | .683442 / .676853 / .681805 |

All nine runs ≤1.7s, normal/crit ≤1.2s, reduced ≤normal. HP/cells remain
4HP at (1,6)/(1,5)/(3,4), with the two blocked setups staying put. Swing timing
180/70/40/80/100/150ms, contact index3/anchor455,196, source PNGs and A9 flags
are unchanged. Auditing verifies70 shared runtime files against source and the
historical A9 hashes, plus unchanged rule bytes. Exact native CPU live-particle
counts are unavailable: timelines label capacity upper bounds; tests verify
frozen clocks and eventual deletion rather than inventing a count.

The first number box hid the impact; final placement moves above the target and
removes only the tuned backing. The first1080 still encoded synchronously during
the hold and took2.0214s including encoding; the repeated tool saves after ready
and reports.9486s. These capture costs are separated from the primary0-readback
timing. The final diagnostic hint preserves legacy SCENARIO/SPACE/DEBUG tokens
and appends C status; the full existing HUD test caught the earlier replacement.

The mockup has768 decorative cells,12 repeated idle sprites, camera pan/drag/
edge/wheel/overview/centre controls, bounds clamp and a display-only minimap.
Seven native1280×720 screenshots show whole map, three positions and three
tile sizes. It is not reachable from main game code, imports no rules/real HUD,
and does not validate pathfinding, AI, combat, objectives, fog or production art.
The proposal recommends C (iso160×94.5px/96px people/32×24), keeps L03 small,
and leaves8 numbered one-line decisions to Gavin.

### Failures and claim ceiling

The dust-layer explicit Vector2 fixes a compile error; the auditor's indentation
was corrected without changing acceptance conditions. A deprecated Pillow
getdata call was replaced with its supported equivalent. The initial mockup
mkdir API mishandled res://../ on Windows despite exit0; the tool now globalizes
the path and aborts on failure, and its error-free repeat is authoritative.
No hook was bypassed. Normal commits report the existing report-only
missing_canonical_memory advisory; the brief excludes shared PLAN/memory edits.
No governance code changed, no native lifecycle/full-adoption claim is made,
and a task handoff is not SessionEnd.

The [evidence index](evidence/spike03/README.md), [movie notes](evidence/spike03/MOVIE.md),
[big-map proposal](../../docs/proposals/big-map-proposal.md) and W7 handoff carry
the review trail. No human feel/scale/art approval, production audio, commercial
quality, full battle or migration is claimed. W7 refreshes source hashes after
the metadata-only handoff addition, then commits and stops without push.

## spike-04

Binding brief: `docs/tasks/godot-spike-04-bigmap-24x18.md`, Owner confirmation
2026-10-24 21:26 Asia/Taipei. Clean start `cbf3608` on `a0ae42c`;
branch `codex/godot-spike`, worktree `D:\campaign-forge\scratch\godot-spike`.
W1–W8 local commits only. Main scene remains11×9 Skirmish. Field24x18 uses a
new pure rules module and no mockup dependency. No shared PLAN/memory changes.

Commands below use the actual full executable paths because PATH/sandbox access
was insufficient. Scoped elevation was used; no tools were installed or trust
settings changed. Initial `git fetch origin` failed sandbox metadata access;
the scoped elevated retry exited0 with no unexpected remote commits. No push.

```powershell
$godotExe = 'C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
$pyExe = 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe'
& $godotExe --headless --path godot-spike --import
& $godotExe --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
& $godotExe --headless --path godot-spike -s res://tools/autoplay_field.gd
& $godotExe --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_field.gd -- --mode=stills
& $godotExe --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike04-field/sequence.avi -s res://tools/capture_field.gd -- --mode=sequence
& $godotExe --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike04-field/enemy.avi -s res://tools/capture_field.gd -- --mode=enemy
& $godotExe --path godot-spike --resolution 1920x1080 --audio-driver Dummy --max-fps 60 -s res://tools/capture_field.gd -- --mode=1080
& $godotExe --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_field.gd -- --mode=perf
& $godotExe --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_field.gd -- --mode=debug
& $pyExe godot-spike/tools/package_field_evidence.py
& $pyExe godot-spike/tools/audit_spike04.py
git diff --stat a0ae42c..HEAD
git diff --exit-code a0ae42c -- shared-anim ui-prototype docs/art-briefs docs/proposals godot-spike/art/anim-shared godot-spike/scripts/rules/grid_rules.gd
git diff --check
```

| Check actually run | Result / exit | Evidence under `docs/evidence/spike04/` |
| --- | --- | --- |
| W1 import / complete GUT | 0 /0;91/91,8,996 assertions | `w1-import.log`, `w1-tests.log` |
| Default,crit,Reduced × three Skirmish setups; fixed60FPS `capture_spike04.gd -- --timing` | 0;9/9≤1.7s,Reduced≤normal,HP4/cells identical | `hitfeel/timing.json` and its logs |
| W1 movies with `--impact-profile=spike03` versus default, normal/crit | all0; four native720p AVIs/±8 strips | `hitfeel/` |
| Rules / battle / camera / UI / policies focused GUT | final0;12/12,5/5,6/6,6/6,3/3 respectively | `w2-rules.log`, `w6-battle-handler-final.log`, `w4-camera-final.log`, `w5-ui.log`, `w6-policy-tests.log` |
| Initial and retuned headless autoplay | both0;initial lose7/6/3;final win12/lose7/lose3,contact2 | `autoplay/initial/`, `autoplay/*.json`, `w6-autoplay*.log` |
| Continuous real scene road battle | 0;win12,warning4,arrival5;48 normal attack wall samples≤.893s | `capture-stills.json`, `runtime-battle.json`, `runtime-attack-timings.json`, `w6-full-battle-final.log` |
| Final parsed operating sequence, enemy AVI, native1080p,debug,unrecorded perf | all0;sequence requires every input check | `w6-sequence-verified.log`, `w6-enemy-final.log`, `w6-1080-final.log`, `w6-debug.log`, `w6-performance-clean.log` |
| W7 final headless import / full GUT | **0 /0;123/123,10,310 assertions,21 scripts** | `w7-import.log`, `test-run.log`, `w7-exit-codes.json` |
| Offline packaging / audit | 0 /0;native AVI headers/dimensions,scope,profiles,70 copied shared files and A9 rules hashes | `movie-index.json`, `audit.json`, `source-hashes.json`, `git-scope.json` |
| Git protected diff / whitespace | 0 /0 after raw-log whitespace normalization | `git-scope.json`, `changed-paths.txt`, `diff-stat.txt` |

The preserved `impact_profile_spike03.tres` has the same Git blob as the original
`a0ae42c` tuned profile. Baseline unchanged; old profile tests re-point only to
that preserved resource and explicitly select it for their historical behavior.
Separate new tests enforce .8 flash,22 sparks/7 spokes/crit1.3,fonts24/30,
direction bias. Hitstop/shake/recoil/dust/zoom/SFX retain original configuration;
crit dust count shares the required lower global particle multiplier.
Skirmish changes are limited to profile selection/directional spark emission.
Its HUD, animation manifest, frames,11×9 rules/results/timings and G005 stay.

Runtime capture is an automated operator. The continuous battle uses actual
scene select/choose/confirm/wait/end-turn, and the operating movie parses real
keyboard/mouse events. Movie combat resumes a reachable turn2 road snapshot;
it is explicitly not a continuous movie. PNGs are runtime readbacks; camera
strip decodes native AVI frames. ffmpeg unavailable, so AVI+PNG supplied.
Performance was separately sampled without recording/readback: scroll19.666ms
mean/42.897ms worst,normal enemy22.776/30.366ms,fast22.521/32.135ms. Enemy
turn2 normal2.188s /2×1.433s. These short AMD780M GL samples do not prove steady60.

Failures are retained, not counted as acceptance: first W3 smoke exited0 despite
a parse error; initial teardown and float/input test failures were fixed. An
early movie used encoder wall time as attack time. A later synthetic click run
failed because global mouse position was stale and aborted on an empty timing
array while claiming success. The scene now uses event.position, capture guards
empty timings and requires every check; the final parsed movie is clean.
The added GUT mouse test calls the scene handler because GUT's own headless GUI
intercepts viewport clicks; full event routing is proven by the rendered movie.
Early shutdown audio leaks were diagnosed as unfinished placeholder playback;
final captures wait/free audio and have clean logs. All final logs are checked
for errors as well as exit codes. PowerShell UTF16/ANSI logs were normalized
to UTF8 with error text/results retained.

Road estimate12.9–21.2min assumes15–25s think/living ally phase and measured
normal enemy mean1.999s; fixed six allies instead yields18.4–30.4min. The two
losing policies end sooner. This is no human pacing/balance validation; ranged
60% kill share, early scout deaths and bypassable reinforcement guards remain
risks. Gavin's full battle, camera comfort,96px legibility, toned impact and art
judgment are **HUMAN_PENDING**. Dummy audio was not auditioned.

No governance code changed. Normal commits report only the existing nonblocking
`missing_canonical_memory` advisory; no hooks bypassed. No lifecycle/full
automatic-adoption claim, session closeout, other-worktree identity claim,
push,PR,merge,32×24,S4 or formal story/rules approval is made. W8 refreshes only
evidence hashes/scope after the handoff addition, commits and stops.

## spike-05

Owner2026-10-26 10:19授權；worktree `scratch/godot-spike`，branch
`codex/godot-spike`，baseline905c0ce，brief commit db47f3a。只改godot-spike/，
保留24×18與spike04未答預設。W1–W8逐步本地commit，不push。

### 實際命令與結果

以下PowerShell變數只為呈現實際使用的完整路徑，沒有PATH fallback。
Godot sandbox初次解析失敗後，以同一路徑escalation執行；Git metadata在本worktree
外的共用.git，fetch與commit也需escalation。沒有改全域信任、登入或hook。

```powershell
$godot='C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
$python='C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe'
& $godot --headless --path godot-spike --import
& $godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
& $python godot-spike/tools/package_spike05_hitfeel.py
& $python godot-spike/tools/package_spike05_field.py
& $python godot-spike/tools/audit_spike05.py
git diff --check
git diff --stat 905c0ce..HEAD
git diff --exit-code 905c0ce -- shared-anim ui-prototype docs/art-briefs docs/proposals godot-spike/art godot-spike/scripts/rules/grid_rules.gd godot-spike/scripts/skirmish.gd godot-spike/scenes/Skirmish.tscn godot-spike/config/impact_profile_a9_baseline.tres godot-spike/config/impact_profile_spike03.tres
```

| Check | Actual result / evidence |
| --- | --- |
| W7 import | exit0, evidence/spike05/w7-import.log |
| W7 full GUT | exit0; **25 scripts /147 tests /147 passing /11,492 assertions /99.538s**; test-run.log, w7-exit-codes.json |
| W4/W6 offline packaging | exit0; native PNG/AVI, timing and reports; w4/w6 logs |
| W6 capture modes | qa/sight/sequence/enemy/intercept-final/result/1080/runtime/perf/autoplay exit0; w6-exit-codes.json |
| Preserved failed capture | first full-probe intercept exit1 (ally attacked first); attempts/ keeps failed JSON/log; later isolated pursuit capture exit0 |
| W7 offline audit | initial exit1: audit expected nonexistent shot.file, corrected to real shot.name+'.png'; failed log retained attempts/w7-audit-schema-failed.log. Final exit0 in w7-audit-run.log; audit.json |
| Git protected scope / whitespace | exit0 / exit0; git-scope.json + changed-paths.txt/untracked-paths.txt/diff-stat.txt |
| Historical profile | spike04 copy Git blob exactly equals905c0ce default `07e34c5ccb0c9ca08fd0d32b63d543e35796d363` |

Audit verifies actual capture dimensions/checks/zero label overlaps, W6 source freeze,
AVI hashes60FPS720p, three baseline results, five after results, nine Skirmish timing
cases,40 field attack samples and protected A9 bytes. `source-hashes.json` includes
working SHA256 and normalized-LF SHA256; excludes self-hash/audit stdout. Scope snapshot
HEAD is the preceding commit; changed-paths also includes the current uncommitted diff.
W8 refreshes metadata after handoff without changing runtime code/evidence conditions.

### Regression and behavioral pin changes

All previous123 tests retained, plus24. Recorded migrations: historical default values
now assert preservedspike04 profile; old roadwin assertions still run on reproducedW1
JSON, while a new live test checks pressure/contact/terminal; live damage sums actual
events because cover/overkill can yield1 instead of2; old fixed leaderdamage10 remains
on baseline. Generic leader alert asserts explicit counter/step-back/hold states;
camera exact-center expectations now use HUD-aware safe_position, with clamps and
return checks retained. JSON numeric casts remove type warnings without changing bounds.
See WORK.md and test diff. No test deleted to obtain the new count.

New tests cover each activation, latching, focus, regroup/cohesion, bodyguard, leader,
wave rest/pursuit, determinism/immutability; LOS forest/cliff/deepbank/unit/corner/range;
profile selection/preserved layers; every edge/zoom and preview-before-confirmation,
overview/marker/label avoidance; terminal-tail idle accounting and five final traces.

Skirmish three setups: HP4, cells(1,6)/(1,5)/(3,4); fixed60Hz input-ready normal.950s,
crit1.016667s,Reduced.716667s; all wall times≤1.7s, Reduced≤normal. Field40 actual
attacks maxwall.902s. All target≤1.2s. Frame durations180/70/40/80/100/150,contact3,
anchor(455,196), grid_rules, all authoredfield terrain/deployment/stats unchanged.
Historical a9/spike03 untouched, spike04 loadable, crit effective mix≤.72.

### Limits

All three initial policies now lose8/7/6. No complete initial-deployment winning policy
was established; staged terminalwin proves result handling only. Road idle66/97→20/77,
but stronger pressure plusLOS confounds policy quality and difficulty. Wave engagement7
in scripted bypass and isolated enemy pursuit do not prove unavoidable engagement.
15–25min target unverified; road estimate10.0–16.3min. No terrain/stat/objective changes
to manufacture wins. Performance mean regresses+1.037/.733/.603ms for scroll/normal/2×;
short scheduling-inclusive samples do not isolate AI cost or establish60FPS.

All screenshots/AVIs are runtime, automated operator only. HUMAN_PENDING: full battles,
readability/camera comfort/feel, art and sound. No governance code, canonical memory,
SessionEnd receipt, external reviewer, other-worktree write,32×24,formal story/S4,
push/merge/PR/Actions/stash is claimed. Resource self-check and open questions in HANDOFF.

## spike-06

Owner2026-10-26 19:17授權，brief8010bde／base6ee5cb7，worktree
`scratch/godot-spike`、branch `codex/godot-spike`。僅godot-spike/；W1–W8
逐步本地commit，沒有push。24×18與已答defaults保持，無新美術／HP填充。

### 實際執行與exit codes

Godot／Python均以Owner指定完整路徑執行；sandbox解析失敗後用同路徑escalation。
共用.git metadata的正常commit也需escalation；沒有全域trust或hooks bypass。

```powershell
$godot='C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
$python='C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe'
& $godot --headless --path godot-spike --import
& $godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
& $godot --headless --path godot-spike -s res://tools/autoplay_field.gd -- --variant=spike05 --seeds=fixed --output=res://docs/evidence/spike06/baseline-recheck/
& $godot --headless --path godot-spike -s res://tools/autoplay_field.gd -- --seeds=fixed --enemy-mean=1.47633625 --output=res://docs/evidence/spike06/after/
& $godot --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_field06.gd -- --mode=measure
& $godot --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_field06.gd -- --mode=perf
# 其他實際mode: runtime,lose,qa,1080；1080以--resolution1920x1080
& $godot --path godot-spike --resolution 1280x720 --audio-driver Dummy --fixed-fps 60 --write-movie res://.godot/spike06-field/enemy.avi -s res://tools/capture_field06.gd -- --mode=enemy
# 同命令scout.avi / --mode=scout
& $godot --path godot-spike --resolution 1280x720 --audio-driver Dummy --max-fps 60 -s res://tools/capture_spike06.gd -- --wall-timing
# 固定模擬時鐘另用--fixed-fps60及--timing，不加--wall-timing
& $python godot-spike/tools/package_spike06_hitfeel.py
& $python godot-spike/tools/package_spike06_field.py
& $python godot-spike/tools/audit_spike06.py
git diff --check
git diff --stat 6ee5cb7..HEAD
git diff --exit-code 6ee5cb7 -- shared-anim ui-prototype docs/art-briefs docs/proposals godot-spike/art godot-spike/scripts/rules/grid_rules.gd godot-spike/scripts/skirmish.gd godot-spike/scenes/Skirmish.tscn godot-spike/config/impact_profile_a9_baseline.tres godot-spike/config/impact_profile_spike03.tres godot-spike/config/impact_profile_spike04.tres
```

| 驗證 | 真實結果／證據 |
| --- | --- |
| W7 import | exit0；evidence/spike06/w7-import.log |
| W7 full GUT | exit0，**30 scripts /165 tests /165 passing /11,749 assertions /104.245s**；test-run.log、w7-exit-codes.json |
| W1與W6舊版 | 各100組；W6全部trace／commands／outcomes／casualties／archetypes／unit-turns／wave與W1相同；baseline-recheck/comparison.json |
| W6 tuned | 100組exit0、零illegal commands；after/，20固定種子×5policy |
| W6 runtime | measure/perf/runtime/lose/qa/1080/enemy/scout全exit0；w6-exit-codes.json、capture-*.json |
| W5 hitfeel | 四normal／crit前後AVI＋strips、九組固定時鐘＋九組獨立real-time；w5-*.log與hitfeel/ |
| W6 packaging | 首次exit1：Windows鎖定自身stdout；attempts/w6-package-active-log-failed.log保留；排除live log後exit0，w6-package.log |
| W7 offline audit／scope | audit exit0，w7-audit-run.log／audit.json；protected diff0／whitespace0，git-scope.json；final source freeze全部一致 |
| Preserved profile | 6ee5cb7 default與spike05 copy Git blob均65883cfef205855bfef691380b5dc7d09beb5a07 |

### 回歸與測試pin遷移

舊147tests全部保留，新增18。歷史18-actor／舊部署／T4 march／NE wave／autoplay
結果fixture明指保留spike05資料／operator；舊profile值明指spike05 resource。
未知profile fallback仍檢查current default。新default另測部署可走、領袖／入口可達、
wave整場交戰、kit閾值／移動預算／不可重複／ZoC／AI／immutability與UI實際預覽。
沒有刪斷言或改成虛構結果。W4中途有fixture／fullremaining候選的失敗log，
WORK已區分；最終165全綠才算本輪驗收。

Skirmish規則與三setup維持HP4、cell(1,6)/(1,5)/(3,4)，damage2、G005、
knockback、walkability、180/70/40/80/100/150ms、contact3／anchor(455,196)未改。
九組固定60Hz input-ready normal.950／crit1.016667／Reduced.716667s；
**固定模擬時鐘wall normal／crit即使單獨跑也會超1.7s**，最長1.971366s，
保留timing-fixed60-alone.json與觀察紀錄，沒有隱去或歸因為已證實的並行問題。
獨立無錄影／readback的real-time九組wall maxima normal.8570／crit.9276／
Reduced.6681s，各setup Reduced≤normal；field另41次max.943979s。
實際遊戲時鐘均過hard1.7／target1.2；錄影模擬時鐘wall不可冒充實際輸入延遲。

default僅flash_mix .6→.5；其他exported值全部相等測試。五profiles selectable。
修正舊說法：field crit沒有乘亮度，實際normal／crit mix均.5；.6是.5×1.2理論乘積，
Skirmish crit multiplier用於fade duration。保留adapter現況，不改額外效果。

### 已知未通過與限制

flank70%勝率、14勝全部援軍交戰、idle29.97%、scout61收割／87攔截且25.05%
傷害非最高。真人難度與理解未驗；turtle／scout-retreat仍全敗。scriptedT5 bypass
100%勝、85%交戰，其中1014/1015/1017勝T6零死且沒碰wave，是保留反例，
不能宣稱不可繞過或最佳路線已證明。

15–25min全面估算門檻**FAIL：0/20區間完全落內**；flank中位17.2–28.4min，
全範圍9.9–33.7。使用新實測enemy mean1.47633625s與15–25s／living ally假設；
不是人類實際分鐘，未填HP。效能亦有明顯退步：scroll34.007/46.443ms、
normal34.053/47.043、2×34.585/45.572（mean/worst），舊mean20.703/23.509/23.124。
前後工作量不同，不能單獨歸因或宣稱穩定60FPS。

PNG／AVI均執行畫面；兩段AVI從真實可達snapshot續播，win／lose則整場從初始部署
連續操作。終局world plates擋文字已最小修正、重錄，零plate間重疊不等於全部UI驗收。
source-hashes包含working bytes／normalizedLF；capture freeze固定W6 runtime，W7/W8
僅驗證／文件；scope HEAD是包含檔案之前commit，另含uncommitted paths。

HUMAN_PENDING：blind road/flank/turtle、實際分鐘、傷亡／困惑／勝敗理由、scout／wave
理解、鏡頭／標籤／閃白／legend／SFX。無新SRD／IP；checklist引用的
docs/design/RULE-ADAPTATION-CONTRACT.md在本checkout不存在，本輪僅自創spike kit，
不宣稱已通過不存在文件的審核。無global trust、canonical SessionEnd、另一worktree
寫入、代理／外部reviewer、main／push／merge／PR／stash／Actions／部署／32×24／S4。
