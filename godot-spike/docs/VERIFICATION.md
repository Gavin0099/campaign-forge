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
