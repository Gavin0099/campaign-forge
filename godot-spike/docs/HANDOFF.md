# Godot spike 01 — Thoma hits a knight

**Ready for review; engine adoption is PROPOSED. Human playtest is HUMAN_PENDING.**
Branch `codex/godot-spike`, base `ff46faa` above web P1v7 `ff87682`.
Owner's [isolated-spike brief](../../docs/tasks/godot-spike-01-hit-feel.md) and
2026-10-23 worktree confirmation govern this delivery. Commit only; no push,
merge, PR, deployment, Actions, story changes or additional slice work.

## Run it

In Godot **4.7.2 standard**, import `godot-spike/project.godot` and press F6 on
`scenes/Skirmish.tscn`, or F5 for the project. The scene builds its children in
GDScript at runtime; the editor canvas alone is not the running presentation.

From the repository worktree root:

```powershell
godot --headless --path godot-spike --import
godot --path godot-spike --resolution 1280x720
```

Use **1 / 2 / 3** or the three HUD buttons to select open ground, a unit blocker,
or the destroyed crossing. **R** replays the selected setup from clean state.
**Space** activates the focused control (Strike is initially focused and regains
focus after an attack); with no control consuming it, Space also strikes.
**M** toggles Reduced Motion, **G** shows the diagnostic grid, **Esc** exits.
Tab can reach controls. While striking, attack/setup/motion controls are locked;
repeated input cannot resolve another attack. Grid inspection remains available.

Tests and evidence regeneration:

```powershell
godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
godot --path godot-spike --resolution 1280x720 --audio-driver Dummy -- --capture
```

Capture runs four automated sequences, writes eight 720p images and a JSON
report, then exits. It must print `CAPTURE_COMPLETE runs=4 screenshots=8 pass=true`;
do not accept exit 0 alone or add `--quit-after` to the acceptance command.
Dummy audio is for reproducible capture in this environment. Omit that flag for
normal audition on a PC with a working sound device.

`.godot/` and all `*.import` descriptors are ignored; no import descriptor was
needed in Git. Run the import command after a fresh checkout. Stable `.uid`
sidecars are committed. GUT's MIT and its bundled fonts' OFL notices are retained
under [addons](../addons/README.md); none licenses this project's story or art.

## Delivered and verified

The model is a node-free `RefCounted` with copied 11×9 rows, source open-route
walkability, deterministic UP/LEFT/RIGHT/DOWN BFS and occupied-cell blocking.
It returns fresh state and ordered attack → damage → knockback/blocked events.
The scene resolves once and only plays those events. No web runtime is imported.

All requested setups use their original brief cells; no placement exception was
needed. Projection is the web camera multiplied by **0.94**, offset by **(−20,42)**.
The painting rectangle has the same transform; body height is **52 × 0.94 = 48.88
px** at 720p, exactly one projected full tile height. Atlas regions match the
P1v4 crops. The grid, not decorative trees or bridge artwork, determines legality.

The strike has anticipation, lunge, 80 ms local actor hitstop, decaying Camera2D
shake, white shader flash, eased displacement or bounded shove/recoil, a floating
damage number, CPU sparks/dust and procedural sound. Reduced Motion suppresses
shake/flash/lean/lunge/particles and retains short displacement and a stationary
damage number. No global time-scale mutation is used.

**14 tests / 344 assertions passed**, including scene timing and replay.
Rendered normal attacks measured **0.9270 / 0.9502 / 0.9663 s**; rendered reduced
setup (a) took **0.8444 s**. All include the contact hold and remain below 1.7 s.

- [Verification, commands, failures and limits](VERIFICATION.md)
- [Hit frame](evidence/hit-frame.png), [knockback end](evidence/knockback-end.png)
- [Unit block](evidence/knockback-blocked-unit.png), [terrain block](evidence/knockback-blocked.png)
- [Reduced motion](evidence/reduced-motion.png), [grid](evidence/grid-diagnostic.png)
- [1080p rendered overview](evidence/overview-1080.png)
- [Four-frame sequence, 3.72 MiB](evidence/SEQUENCE.md)
- [Test log](evidence/test-run.log), [capture measurements](evidence/capture-report.json)

## Placeholders and limitations

- **Spike-only:** Thoma HP 8, knight HP 6, base damage 2, no blocked-impact bonus.
  Constants live together in `scripts/rules/grid_rules.gd`. They do not amend
  G005 or any formal combat design. Thoma's attack is an isolated demonstration,
  not a new story role or class ability.
- Both knights reuse one body crop; every character is a single static body.
  Whole-body translation/lean does not provide footwork, a weapon arc, joint
  animation, directional poses or bespoke stagger frames. Contact silhouettes
  can overlap; the small native figure scale limits detail at 720p.
- Original copied PNGs are unchanged ([hash proof](evidence/asset-copy-hashes.json)).
  No image generation was needed. Sparks and dust are engine primitives, not
  newly commissioned hand-painted VFX. [SFX](../audio/SOURCES.md) is deterministic
  in-memory synthesis. No usable audio device was available during capture;
  triggering and PCM were tested, but the audible mix was not heard or approved.
- BFS exists in the pure model; there is no click-to-move gameplay, turn loop,
  enemy AI, victory/defeat, campaign UI, persistence, Ink runtime or export build.
  Replaying always resets the demonstration rather than continuing combat.
- English HUD, fixed 16:9 reference coordinates and `canvas_items` / `keep` scaling
  suit this spike. Localized layout, text enlargement, gamepad behavior and other
  aspect ratios are not validated. No claim of full accessibility compliance.
- The committed motion evidence is sampled PNG frames, not a full-rate movie.
  Automated input and model visual inspection do not replace Owner playtesting.

## Comparison and migration recommendation

Compared with the current web rules, this spike has actual damage/displacement
events and contact-timed audiovisual feedback. The measured event-to-animation
path is compact and testable in Godot. Visual inspection confirms a clear flash,
different displaced/blocked endings and a return to rest. **It does not prove
that Gavin will find the hit weight convincing.** The baseline has no equivalent
attack, so this is not a controlled engine-only comparison. React/canvas or a web
game engine could also implement these effects; the Godot result demonstrates
convenient built-in facilities, not an exclusive capability.

Recommendation: **retain this isolated study for Owner comparison; defer a full
migration decision.** Keep the direction only if Gavin can trigger/replay it
unaided and finds the contact and blocked recoil meaningfully clearer. Retune or
reject it if the effect still reads as sliding paper or visual noise. Do not
promote the spike's constants and assumptions directly into production rules.

If later authorized, migrate one battle slice first: port the approved pure
rules with canonical event/state fixtures, reuse original PNGs and atlas regions,
replace DOM/SVG presentation with Godot nodes/tweens/materials, and port meaningful
rule and interaction tests to GUT. Preserve the web implementation for parity
comparison. Scenario/deployment data should remain separate from presentation.

Planning estimate for an experienced developer, **not a commitment or authorization**:
2–4 days for rule/fixture parity; 4–7 days for one battle's controls and presentation;
2–4 days for regression/capture/export checks; 2–4 days for a separate Ink
compatibility spike. Roughly **10–19 engineering days** before a useful migration
decision, excluding production character animation, new story, save systems,
accessibility/localization completion and content conversion. Full-game migration
cannot be estimated responsibly from one attack.

Ink is a material risk under the GDScript-only standard-build constraint.
[GodotInk](https://github.com/paulloz/godot-ink/blob/main/README.md) targets Godot 4
but its installation requires .NET and a C# project; a GDScript API does not remove
that runtime dependency. [inkgd's godot4 branch](https://github.com/ephread/inkgd/tree/godot4)
offers a pure GDScript implementation and documents 4.2+ support without an
official release. Godot 4.7.2 behavior, actual story JSON, variable observers,
external functions and save/restore parity need a pinned-version test before
adoption. Neither integration was installed or validated here.

For the Codex / Claude / GPT review loop, GDScript and `.tscn` remain text-reviewable;
reviewers should run the pinned engine and headless suite, compare event fixtures,
then inspect rendered evidence and the source hashes. Browser/Playwright tests
cannot simply be reused as Godot interaction tests. GPU/window/audio variation
requires reproducible capture commands and an explicit human playtest gate.
No independent model review was launched in this task; review is the next Owner
step, not an approval inferred from automated tests.

## Resource self-check

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md). PASS below is
limited to the isolated spike's technical scope, never full-game acceptance.

| Section / resource | Status | Evidence or scoped exception |
| --- | --- | --- |
| A — prototype-fast | PASS (scope) | One attack, isolated folder, fixed budget/stop point; keep/reject decision belongs to Owner. Skill read during verification, not claimed as a pre-coding skill load. |
| A — level-design | N/A (full level) | No level design or route/win objective changes. Terrain/BFS/edge behavior is covered by rules tests. |
| A — game-ai | N/A | No enemy AI authorized by this brief. |
| A — game-ui-ux | PASS (spike controls) | Setup/replay hints, HP, keyboard dispatch, focus, Reduced Motion and two rendered sizes. Fixed reference layout / no localization or gamepad validation are explicit limitations. |
| A — game-feel | **PASS (technical)** | Contact flash/hold, bounded recoil, camera reset, same-event feedback, under-1.7 s timings; linked rendered frames and scene tests. **Human feel: HUMAN_PENDING.** |
| B — Grid-Tactics separation | PASS (architecture criterion) | Pure model emits events; view does not compute knockback. No code or assets borrowed from that unlicensed repo. |
| B — HopeMetal attribution | N/A | No code or assets borrowed. |
| B — new engine/dependency | PASS | Explicit Owner-approved isolated Godot PoC; only requested GUT added, with licenses. |
| C — full 3–5 minute battle | N/A | Deliberately one attack; no claim of full battle completion. |
| C — understandable enemy AI | N/A | Staged target, no AI. |
| C — player can win/lose | N/A | No battle objective or terminal result. |
| C — two tactical choices | N/A | Three setups are demonstrations, not player tactical choices. |
| C — restart/change strategy | PASS (replay only) | Clean-state replay tested; strategy loop excluded. |
| C — no duplicate/stuck/illegal resolution | PASS | Replay spam, setup lock, BFS and blocked-foot-position tests; fresh capture completes. |
| C — 720p / 1080p / keyboard | PASS (observed paths) | Eight 720p images, actual 1080p overview, synthetic Godot input dispatch; no human keyboard test claimed. |
| C — automation vs human | PASS | 14/344 automated pass; human playtest and Owner art judgment explicitly pending. |
| D — SRD / rule attribution | N/A (SRD) / PASS (scope) | No SRD/WotC content used; brief-authorized original spike numbers are separate from G005. |
| D — project boundaries | PASS | Only `godot-spike/` plus the required proposal row; no web/story changes, push, main merge, PR or external checkout work. |

Read-only skill methods were consulted at pinned commit
[`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd`](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd):
[prototype-fast](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/workflows/prototype-fast/SKILL.md),
[game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md)
and its feedback recipes,
[game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md)
and its layout/flow reference. They were read, not installed or copied. The local
external-executable-trust-audit skill informed the limited tooling provenance
record; it does not establish full launcher hardening.

## Commit sequence and shared-file handling

| Step | Commit |
| --- | --- |
| 1 — skeleton and original PNG copies | `f99eb4c` |
| 2 — pure rules and ordered events | `02b6274` |
| 3 — painted scene / three setups | `5741fc9` |
| 4 — impact playback / motion preference | `0979807` |
| 5 — GUT / rules and scene tests | `7c1023c` |
| 6 — final verification and rendered evidence | `775d764` |
| 7 — this handoff and P010 proposal | This commit |

Shared-file: `docs/DECISIONS.md`, one new **P010 PROPOSED** row; D-rows unchanged.
P001–P009 were the highest fetched remote proposal IDs before editing. Fetch
succeeded; there were no incoming task-branch commits. Bare `git pull --ff-only`
exited 1 because no upstream was configured; explicit
`git pull --ff-only origin codex/godot-spike` exited 0, already up to date.
No tracking configuration was changed.

The latest Owner instruction prohibits touching the main checkout or other
scratch worktrees, so the central `scratch/locks` path was not written. A
create-exclusive lock at `godot-spike/.godot/DECISIONS.md.lock` protects this
isolated worktree edit; Owner already confirmed a sole agent here. It is not
claimed to be the cross-worktree coordination lock. The shared-edit marker and
commit trailer identify the edit; the local lock is released after this commit.
No shared memory/PLAN edits or canonical daily closeout were performed, because
the brief limits writes and task DONE is not session end.

## Open questions for review

Does Gavin find the contact weight and blocked recoil convincing at normal size?
Is the current static-body art sufficient to test the engine direction, or should
an independently authorized animation-art spike come first? If Godot is retained,
which pinned GDScript Ink route and battle parity slice should be investigated?
These are review decisions, not work automatically continued by this handoff.

Stop here after the handoff commit. No push; wait for Owner review.

## spike-02 Phase A

2026-10-23, branch `codex/godot-spike`, starting at brief commit `9345b0e`.
**A1–A9 delivered for review. Engineering checks pass; exact art and weapon
identity remain incomplete.** Human playtest is **HUMAN_PENDING** and P010 is
**PROPOSED**. This section supersedes spike-01's controls, animation and evidence
claims for the current build. Phase B has not started. All nine commits are local.

### Run and inspect

From this worktree's root, with the Owner's existing Godot 4.7.2 console wrapper:

```powershell
godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd
godot --headless --path godot-spike --import
godot --path godot-spike --resolution 1280x720
godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
```

Use **1/2/3** for open / unit-blocked / terrain-blocked, **Space or R** to strike
from reset state, **M** for Reduced Motion, **Esc** to exit. **F1 or backtick**
reveals diagnostics; **G** toggles the grid while diagnostics are open. Debug is
off by default. Strike regains keyboard focus after completion; attack/setup/
motion changes remain locked during playback. HUD/debug processing stays live
during hitstop. Normal runs use the available audio device; audition is pending.

To reproduce rendered evidence, use `--audio-driver Dummy -- --capture02`
after the 1280×720 run command, or `-- --readability` for the twelve-image
comparison. Both require their `CAPTURE_COMPLETE ... pass=true` marker and
actual files. Do not use spike-01's `--capture` for this evidence. The native
movie command, absolute output path, packaging commands, real exit codes and
retained failed attempts are in [VERIFICATION](VERIFICATION.md#spike-02-phase-a).
[Watch the 60 fps AVI](evidence/spike02/attack-60fps.avi), or inspect the
[six retained native movie frames](evidence/spike02/MOVIE.md).

### What changed against the four P1 findings

| Finding | Phase A change and evidence |
| --- | --- |
| Sliding paper / no swing | Six articulated sword poses, fixed foot pivot, manifest-driven texture swaps and a small diagonal closing step; three hit and three blocked-stagger poses per knight. [Anticipation](evidence/spike02/anticipation.png), [contact](evidence/spike02/contact.png), [buckled stagger](evidence/spike02/blocked-unit-stagger.png), [contact sheet](../../shared-anim/contact-sheet.png). Thoma's weapon identity is PLACEHOLDER. |
| Local hitstop | Dedicated pausable World subtree, node-bound world tweens and always-processing HUD; same-frame contact, flash, immediate spark geometry and SFX. [24-test log](evidence/spike02/test-run.log), [timing](evidence/spike02/timing.json), [five identical held movie frames](evidence/spike02/movie-index.json). |
| Small / identical units | Attack zoom selected over permanent enlargement; knight B has a lighter shield field across all seven frames. [Camera contact](evidence/spike02/readability-a-setup2-contact.png), [label-free grayscale](evidence/spike02/knights-grayscale.png). |
| Test-tool UI | Scenario title, bone/brass HP bars, small key line and one strike control. Phase/timing/grid/identity diagnostics require F1/backtick. [Default](evidence/spike02/hud-minimal.png), [debug](evidence/spike02/hud-debug.png), [1080p](evidence/spike02/overview-1080.png). ASH SHIELD / PALE SHIELD are temporary UI descriptors, not setting names. |

### Shared assets and frame status

The canonical root is **`shared-anim/`**, outside either engine. The committed
sync script copies 44 files into `godot-spike/art/anim-shared/`, with source/copy
SHA-256 parity checked by GUT. Godot loads only its local copy. The web copy is
deferred to Phase B; `ui-prototype/` is unchanged. All four original PNGs retain
their original bytes ([proof](evidence/spike02/original-assets.json)).

| Runtime sequence | Frames | Status |
| --- | --- | --- |
| `thoma/idle` | `00` | Original specified crop, normalized to the shared canvas |
| `thoma/swing` | `00` anticipation, `01` raised blade, `02` sweep, `03` contact, `04` follow-through, `05` recover | **All six PLACEHOLDER**: weapon identity and minor costume variation |
| `knight-a/idle` | `00` | Original specified crop, normalized |
| `knight-a/hit` | `00` flinch, `01` recoil, `02` settle | Generated candidates, awaiting art judgment |
| `knight-a/stagger` | `00` brace, `01` buckle, `02` recover | Generated candidates, awaiting art judgment |
| `knight-b/idle`, `hit`, `stagger` | `00`; `00–02`; `00–02` | Same seven A frames with consistent light shield-field edit; candidates |

Total **21 RGBA PNGs**, each 512×512, pivot `[256,464]`, reference body height
360 frame pixels. Native facing is right for Thoma and left for knights;
opposite facing mirrors the image, offsets and anchors about that pivot.
There were twelve generated outputs, one attempt each, then scripted alpha
cleanup, registration, source-derived palette mapping and B's shield edit.
No additional characters, battlefield or props were generated. Every full
prompt, reference, raw/runtime hash and cleanup is in
[SOURCES](../../shared-anim/SOURCES.md); raw images remain available for audit.

**Style self-assessment:** the muted robe/metal colors, top-left illumination
and dark painted edges broadly follow the original crops. Palette mapping
and fixed registration improve consistency; they cannot prove exact stroke,
garment folds, armor contours or proportions. Some detail drifts between poses.
The specified Thoma crop is visibly empty-handed. The demonstration therefore
references the sword of the first warrior in the same original party atlas;
it cannot satisfy “the sword Thoma carries” literally. The sword appears during
the swing and disappears on returning to the original idle. This is a disclosed
placeholder, not approved equipment or story. No Ferry Dusk palette was adopted.
The [contact sheet](../../shared-anim/contact-sheet.png) supports model inspection,
not Owner commercial-art acceptance.

### Readability and impact decision

Keep **option a**, baseline body height `48.88 × 0.98 = 47.9024px`, with **1.5×**
attack zoom (71.85px reference body at contact). Enter over 240ms, return over
180ms; move camera focus 40% toward the attacker/target midpoint. Reduced Motion
keeps the camera still. Option b uses permanent 1.3× units without attack zoom.

The corrected [twelve-capture matrix](evidence/spike02/readability.json) and
[silhouette measurements](evidence/spike02/readability-overlap.json) show no
nonparticipant overlap for option a. Option b has **16 screen pixels of
knight/knight overlap at unit-blocked rest**. Intended attacker/target contact
overlap in a is 80 / 166 / 171 screen pixels across the setups. Thus a improves
attack readability while preserving separation; it does not eliminate intended
contact overlap or make small idle details large. These measurements use alpha
≥128 and full viewport transforms, not final-image VFX segmentation.

A8 corrected A5's use of decomposed global_scale, which omitted the rotation
Godot uses for mirrored sprites. Earlier 92px and 63/29/81px claims are invalid.
All twelve screenshots/transform records were refreshed. The 0.98 scale remains,
but the earlier claim that a specific 2% reduction was necessary is withdrawn.
See [adapter details](ANIMATION-ADAPTER.md).

Hitstop sets `SceneTree.paused` with World PAUSABLE and HUD/root ALWAYS. Every
world tween is node-bound. An always-processing, unscaled 80ms timer plus wall
clock and subsequent-process-delta guards prevents early resume. Both frame
players, world tweens, particles, camera and damage number are tested across the
complete hold while a HUD probe advances. Contact pose, flash, spark and SFX
share a process-frame index. Audio rings out during the visual hold.

Normal rendered attacks measured **0.9114–0.9179s**; Reduced Motion
**0.7300–0.7302s**, including real hitstop. Ordinary holds were 90.239–91.271ms
on this runner. The fixed-60-fps PNG movie proves **five identical frames,
83.33ms**, then visible resume; strike-to-ready is 55/60 = 0.9167s. Synchronous
screenshot readback can stall rendering: one separate capture hold was 122.301ms.
This is retained separately, not hidden in ordinary-playback measurements.

### Limits and Phase B requirements

Reduced Motion uses swing poses 0/3/5 at 100ms each, no closing offsets, smear,
shake, flash, particles or zoom, and minimal displacement. The stationary
contact pose does not close the full weapon-to-target gap. Hitstop and the
stationary damage number remain. Normal audio triggering/PCM are tested, but
the audible mix was not heard. Generated art and hit feel need human review.

This remains one scripted attack with three fixture setups: no turn loop,
enemy AI, win/lose, persistence, export or Ink integration. The pure rules and
G005 are unchanged. Type-based event dispatch preserves order within attack,
damage and movement queues and stages their causal presentation; it handles
reordered/unknown events, but is not a general multi-attack scheduler. Fixed
16:9 layouts were rendered at 720p/1080p; localization, enlarged text, gamepad
and other aspect ratios remain unverified.

**For a separately authorized Phase B**, copy the exact shared files into the
web public folder and enforce SHA-256 parity. Honor version, character canvas,
pivot, native facing, frame paths/durations/offsets, loop behavior, contact index,
events and anchors, scenario reactions, all impact/recovery durations, camera
zoom/focus/timing and reduced-motion fields. Use the same 47.9024px body scale,
battlefield projection and fixtures. Canvas frame swaps or a Web Animations
adapter can implement the player; pause every world animation/particle/camera/
damage-label clock for hitstop while DOM HUD/focus stays live. Verify actual
frame timings and same-frame triggers in both engines. Preserve existing web
scenes/rules and use the isolated `?scene=anim-ab` route specified in the brief.
No engine-comparison verdict is justified before that equivalent implementation.

### Resource self-check and review state

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md). Relevant
prototype-fast, game-feel and game-ui-ux methods were read at the pinned URLs
listed in spike-01 above; nothing was installed or copied. The imagegen and
external-executable-trust-audit skills informed asset provenance and use of the
existing tools. This is not a full executable trust attestation.

| Checklist item | Status | Evidence / scoped exception |
| --- | --- | --- |
| A — prototype-fast | PASS | Isolated one-attack study; shared README states keep/reject criteria; stop before Phase B. |
| A — level-design | N/A | No routes, objectives, placements or level changes; existing rules tests retained. |
| A — game-ai | N/A | No enemy AI in the authorized spike. |
| A — game-ui-ux | PASS (scope) | Minimal HUD, keyboard/focus locks, explicit debug state, reduced motion and two rendered sizes; no full-battle intent/objective UI claimed. |
| A — game-feel | PASS (engineering) / HUMAN_PENDING | Articulated poses, contact sync, tested whole-world pause, measured pacing; exact weapon/style match remains incomplete as disclosed above. |
| B — Grid-Tactics separation | PASS (criterion) | Untouched pure model emits events; presentation consumes typed events. No borrowed code/art. |
| B — HopeMetal attribution | N/A | No code or assets borrowed. |
| B — new engine/dependency | PASS | Owner-authorized isolated Godot continuation; existing vendored GUT only, no new addon. |
| C — full 3–5 minute battle | N/A | One-attack brief; no complete battle claim. |
| C — understandable enemy actions | N/A | Staged targets, no AI. |
| C — win/lose | N/A | No terminal battle states authorized. |
| C — two tactical choices | N/A | Three demonstration setups, not a strategy loop. |
| C — restart/change strategy | PASS (replay) / N/A (strategy) | Reset/replay and setup switching tested; no strategy system. |
| C — no duplicate/stuck/invalid resolution | PASS (covered paths) | Existing rules/replay/input-lock tests retained; reordered/unknown events and complete captures pass. |
| C — 720p/1080p/keyboard | PASS (automated) | Actual captures at both sizes; synthetic input for 1/2/3, R, Space, M, F1, G and Esc; human keyboard play remains pending. |
| C — automation vs human | PASS | 24 tests / 624 assertions, exit 0, separately recorded from HUMAN_PENDING; model inspection is not approval. |
| D — SRD/rule sources | N/A (new SRD content) / PASS (scope) | No new rules or WotC content; original spike-only constants and G005 untouched. |
| D — authorization | PASS | Only shared-anim/ and godot-spike/ changed after 9345b0e; no ui-prototype, original PNG, story, main, other-worktree, push, PR, merge, Actions or deployment work. |

| Step | Commit |
| --- | --- |
| A1 — spec/schema | `140c612` |
| A2 — original-reference frames | `ec55e17` |
| A3 — sync/manifest/event player | `64d4f8e` |
| A4 — world pause / live HUD | `7d14a5e` |
| A5 — readability candidates | `9c3961b` (measurement corrected in A8) |
| A6 — minimal HUD | `f066b11` |
| A7 — GUT tests | `8ae855c` |
| A8 — final verification/evidence | `5eea140` |
| A9 — Phase A handoff | This commit |

No shared PLAN/memory/DECISIONS edits were made under this brief's narrow write
scope. The diff from `be9a398` includes the pre-existing brief commit in
`docs/tasks/`; the Phase A implementation scope is checked against `9345b0e`.
Normal commit hooks ran and reported only the nonblocking
`missing_canonical_memory` advisory; no hook bypass. No independent agent review
was launched. Review should decide whether the candidate swing/reactions and
camera improve the feel, and how to resolve the empty-handed source/weapon gap.
Those are review inputs, not model approval or authorization to continue.

**Stop after this handoff commit. No push. Await Owner review. Task DONE is not
SessionEnd; Phase B remains unstarted.**

## spike-02 A2

**Ready for review of this fix segment.** Thoma now carries the same proposed
short mace in idle and all six swing poses; the default screen has a Traditional
Chinese battle HUD; knight B has a consistent bone crest/light shield. Final
engineering checks pass. **Human playtest is HUMAN_PENDING; weapon and P010 are
PROPOSED.** Five motion frames remain PLACEHOLDER for detailed costume drift.
These results do not grant equipment, story, commercial-art or engine approval.

Owner's 2026-10-23 confirmation authorized this worktree/session and W1–W6 only,
starting clean at `4b9cea4` over Phase A `46edbc6`. Branch: `codex/godot-spike`.
Commit only; **no push**. The earlier Phase A sections describe historical states
and are superseded by this section where A2 changes them. **Phase B unstarted.**

### Run and inspect

From `D:\campaign-forge\scratch\godot-spike`, using the installed Godot 4.7.2
standard build and its existing console wrapper:

```powershell
godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd
godot --headless --path godot-spike --import
godot --path godot-spike --resolution 1280x720
```

Or open `godot-spike/project.godot` and press F5. **Space** first prepares the
attack/forecast, then a second press confirms; the focused action button also
works with the mouse. **R** directly replays the current fixture. **1 / 2 / 3**
select open / unit-blocked / terrain-blocked setups. **M** toggles Reduced Motion
while idle. **F1 / backtick** toggles debug; **G** toggles its grid only while
debug is open. **H / ?** opens the dismissable Chinese controls overlay. **Tab**
moves focus; **Esc** closes help, debug or armed forecast before exiting.
Attack/setup/motion changes remain locked during playback. Help responds during
hitstop. Knight names appear in forecast/hover inspection, not permanent labels.

SystemFont uses the installed Microsoft JhengHei with Noto Sans TC / PingFang TC
fallbacks. No font file is bundled or redistributed. Other PCs need a suitable
CJK system font. Test and capture commands with actual exits are in
[VERIFICATION — spike-02 A2](VERIFICATION.md#spike-02-a2).

### GPT P1 responses

| Review issue | Change | Evidence and remaining limit |
| --- | --- | --- |
| Weapon identity / weak swing | Replaced borrowed sword with proposed own mace; persistent weapon idle; 180 ms wind-up, 40 ms swing, articulated contact and recovery; head anchor [455,196] | [Style sheet](evidence/spike02-a2/thoma-weapon-style-check.png), [movie](evidence/spike02-a2/attack-60fps.avi), [prompts/hashes](../../shared-anim/SOURCES.md). Identity gap is resolved as a proposal; five detailed costume checks remain PLACEHOLDER and human weight/readability judgement is pending. |
| UI NOT FIXED / tool appearance | Selected portrait/name/role/HP/status at bottom-left; event-driven paired-portrait forecast while armed; transient turn banner; unit HP bars; brass/moss nine-slice frames; debug/help off initially | [Default](evidence/spike02-a2/default-view.png), [forecast](evidence/spike02-a2/attack-forecast.png), [blocked unit](evidence/spike02-a2/forecast-blocked-unit.png), [blocked terrain](evidence/spike02-a2/forecast-blocked-terrain.png), [help](evidence/spike02-a2/help-overlay.png), [F1](evidence/spike02-a2/debug-f1.png). Model visual inspection, not Owner approval. |
| Knight readability / zoom overlap | Bone crest and light shield across every B pose; 1.4× zoom with 0.52 focus weight; current-frame HP anchors and separated damage numbers | [Unlabeled default](evidence/spike02-a2/knights-default-view.png), [zoom](evidence/spike02-a2/knights-zoomed.png), [grayscale](evidence/spike02-a2/knights-grayscale.png), [overlap JSON](evidence/spike02-a2/readability-overlap.json). Zero measured nonparticipant overlap; finite sampled poses, human distance recognition pending. |

The GPT review's separate concern about human attack-weight validation remains
**HUMAN_PENDING**. The complete movie is supplied as review material, not as a
replacement for human playtest. No Phase B comparison or engine verdict follows.

### Thoma weapon — PROPOSED, Owner confirmation pending

**Short one-handed flanged mace:** blunt dark iron head, worn oak haft, small
brass collar echoing the medallion; forearm length, carried in his right hand.
It provides a compact, weighty blunt silhouette suitable for the medical friar
proposal without becoming a staff. The medallion remains a holy symbol, never
the weapon. No sword/blade/staff/book/glow or borrowed party-member equipment.

Canon names no weapon; the brief's evidence is retained without silently turning
the proposal into canon:

- `ui-prototype/docs/l03/character-prompt.txt:1`: older medical friar, teal robe,
  ivory stole, medical satchel, brass medallion; explicitly empty hands and no
  staff/book/glow. Original crop remains unedited.
- `ui-prototype/docs/l03/ART-DIRECTION.md:9` and `ui-prototype/src/l03Scene.ts:51–54`:
  medical satchel/teal, medical and support role.
- `ui-prototype/docs/playable-l03-research/DEMO-CONTRACT.md:17`: melee 3 and heal 3
  in a proposed demo kit. This segment leaves actual spike damage 2 untouched.
- On `origin/story/strengthen-narrative`, `docs/story/STORY.md:56` and
  `COMPANION-ARCS.md:28` describe the medical friar/cleric. `COMPANION-ARCS.md:34`,
  `docs/story/script/ch01.ink:306` / `ch02.ink:250` describe his held holy symbol;
  `CREATIVE-BIBLE.md:74` calls out age, robes and symbol for separate review.
  These are source locations cited in the brief, not newly authored story.
- Brief-cited `docs/DECISIONS.md` U003 concerns the original class frame, not
  weapon assignment. Phase A README explicitly identified the borrowed sword
  as placeholder rather than an equipment/story decision.

Manifest uses **`thoma/idle/01.png`**; `idle/00.png` remains reference-only. All
runtime frames are 512×512 with pivot [256,464]. The original crop and new weapon
idle constrain generation; no Karen/sword reference was used for A2. One attempt
per frame except swing 02: attempt 1 descended too far before contact, attempt 2
replaced it. The rejected original is archived outside runtime sequences.
Complete prompts, references, raw/runtime SHA-256 and cleanup are in
[SOURCES](../../shared-anim/SOURCES.md) and
[generation-prompts.json](../../shared-anim/generation-prompts.json).

| Frame | Pose | Model style check |
| --- | --- | --- |
| `thoma/idle/01.png` | Weapon at rest | **PASS** — face/costume/near-idle silhouette retained at review scale |
| `thoma/swing/00.png` | Anticipation | **PLACEHOLDER** — stole motif, cuffs and hem drift |
| `thoma/swing/01.png` | Raise/start | **PLACEHOLDER** — same costume-detail mismatch |
| `thoma/swing/02.png` | Descending swing / painted smear | **PLACEHOLDER** — corrected arc, costume-detail mismatch remains |
| `thoma/swing/03.png` | Forward-weight contact | **PLACEHOLDER** — own mace/head anchor, costume-detail mismatch remains |
| `thoma/swing/04.png` | Follow-through | **PLACEHOLDER** — trailing stole/hem differs from source |
| `thoma/swing/05.png` | Recover | **PASS** — near-idle shape and equipment continuity at review scale |

[Per-frame face/costume/proportion/palette/light/stroke audit](../../shared-anim/frame-audit.json).
The [same-scale and native-720p-size sheet](../../shared-anim/thoma-weapon-style-check.png)
is an asset review sheet, explicitly not a runtime screenshot. PASS is a model
check, not Owner/commercial approval. **Weapon stays PROPOSED for every frame.**
Knight B edits are deterministic source-derived candidates, not a new named
story character; original A and source atlases remain unchanged.

### HUD, readability and timing

Selected panel shows 托瑪 / 修士／醫療, portrait, numeric HP/bar and the short
status line. Forecast shows attacker/target portraits, damage, target HP before
→ after and event outcome: 擊退一格 or 受阻 + 被友軍阻擋 / 被斷橋阻擋. The unit-blocked
forecast names 議會騎士・乙 as blocker. Damage/HP/blocker data comes from pure rule
events; a changed 1-HP input is tested to rule out fixed-number copy.

The HUD is an always-processing CanvasLayer. HP bars remain visible at hitstop;
the world, camera, animation clocks, damage-number tween and VFX stay paused.
All player-facing labels are Traditional Chinese. Default hides technical
scenario/phase/timing/hotkey text; F1 contains those diagnostics. Text uses the
P1v3/P1v4 bone/brass/sage/teal/clay colors over opaque moss/iron backings.
[Contrast table](evidence/spike02-a2/contrast.json): minimum **5.344:1**, all normal
text pairs pass WCAG AA. Original procedural frame provenance is in
[art/SOURCES](../art/SOURCES.md). No new portrait generation or Ferry Dusk palette.

At alpha ≥128, with full affine viewport transforms including mirroring and
weapons, all three rest/contact setups have **0** nonparticipant overlap. At rest,
attacker/target overlap is also **0**; intended contact intersections are
**71 / 157 / 164 px**. Zoom/grayscale/default label-free samples are separate.
These are sampled setup measurements, not proof across unimplemented battles.
Camera tuning changes presentation only; rule cells and outcomes remain fixed.

| Setup | Normal rendered | Reduced Motion |
| --- | --- | --- |
| Open | 0.914639 s | 0.729160 s |
| Unit-blocked | 0.915426 s | 0.730027 s |
| Terrain-blocked | 0.911700 s | 0.730169 s |

All are below **1.7 s**, close to Phase A's normal 0.91–0.92 s. Fixed-60-fps
movie strike→input-ready is **0.916667 s**, with **5 identical held frames /
83.333 ms**, then visible resume. [AVI](evidence/spike02-a2/attack-60fps.avi)
is 60 frames / 7,365,366 bytes. [Movie notes and samples](evidence/spike02-a2/MOVIE.md)
separate encoding time from gameplay timing. Reduced Motion omits smear frame 2,
zoom/shake/flash/particles/closing offsets; its stationary weapon-to-target gap
remains a known Phase A limitation, with damage/HP feedback still delivered.

Final **33 tests / 924 assertions**, clean exit 0. W5 found and fixed physical
Space double dispatch; a separate test-teardown-on-signal error also required
correction. Earlier exit-0/error-bearing runs are preserved and rejected in
[VERIFICATION](VERIFICATION.md#spike-02-a2), not hidden behind pass summaries.

### Limits and resource self-check

This is still one scripted attack with three fixtures, not a complete battle,
turn loop, AI, win/lose system, formal equipment design or engine migration.
Actual 720p and 1080p renders plus synthetic keyboard input are verified;
other aspect ratios, enlarged text, gamepad and audible-device audition remain
unverified. All human playtest, hit feel, commercial art and Owner judgement
are **HUMAN_PENDING**. No independent agent was launched in this segment.

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md):

| Item | Status | Evidence / scoped exception |
| --- | --- | --- |
| A — prototype-fast | PASS (criterion) | Same one-attack scope and keep/reject readability question in shared README; no Phase B or new mechanics |
| A — level-design | N/A | No map, routes, objective or placement changes; original rule tests retained |
| A — game-ai | N/A | No AI authorized in this segment |
| A — game-ui-ux | PASS (scope) | Read pinned [skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md); event-driven values, confirmation, focus, overlay exit and reference-canvas scaling; actual 720p/1080p evidence. Full movement/threat/objective systems are N/A to this spike |
| A — game-feel | PASS (engineering) / HUMAN_PENDING | Read pinned [skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md); same-event feedback, articulated poses, measured hold/recovery and Reduced Motion; human weight judgement pending |
| B — Grid-Tactics separation | PASS (criterion) | Rules unchanged; HUD/playback consume event dictionaries. No reference-repo code or art copied |
| B — HopeMetal attribution | N/A | No patterns/code/assets borrowed in this segment |
| B — new engine/dependency | PASS | Already-authorized isolated Godot 4.7.2/GDScript/GUT; no new addon/dependency |
| C — full 3–5 minute battle | N/A | Explicit one-attack spike; no complete battle claim |
| C — understandable enemy actions | N/A | Fixture targets; no autonomous enemy turns |
| C — win/lose | N/A | No terminal battle states authorized |
| C — two tactical choices | N/A | Three demonstration fixtures, not a tactical decision loop |
| C — restart/change strategy | PASS (replay) / N/A (strategy) | Clean fixture reset/replay and setup-switch locks; no strategy system |
| C — no duplicate/stuck/invalid resolution | PASS (tested paths) | 24 old tests retained plus A2 coverage; real Space regression and capture pass markers |
| C — 720p/1080p/keyboard | PASS (automated scope) | Real [720p](evidence/spike02-a2/default-view.png), [1080p](evidence/spike02-a2/overview-1080.png), synthetic input and focus tests; not human playtest |
| C — automation vs human | PASS | Clean 33/924 result and model visual checks explicitly separate from HUMAN_PENDING |
| D — SRD/rule sources | N/A (new SRD content) / PASS (scope) | No rule change, no new SRD/WotC content, G005 unchanged |
| D — authorization | PASS | Only shared-anim/ and godot-spike/ implementation changes; base diff also contains pre-existing brief. No original PNG/web/story/shared-memory edits, other worktree, push, main merge, PR, Actions, deployment or Phase B |

The built-in imagegen skill was used for the seven permitted Thoma frames;
knight edits and the nine-slice frame are deterministic scripts. No commercial
art, reference-repo code, original source modification or new licensed font.
No shared PLAN/memory edits were made under this narrow authorization; this
handoff and verification record the milestone. Normal commit hooks ran and
reported the nonblocking `missing_canonical_memory` advisory. That does not
mean a SessionEnd callback or canonical closeout occurred.

| Step | Commit |
| --- | --- |
| W1 — own weapon / frames | `d64ef92` |
| W2 — battle HUD | `03d2ca3` |
| W3 — knight identity / overlap | `2eb3165` |
| W4 — tests | `229a820` (error-bearing cleanup log superseded by W5) |
| W5 — final verification / evidence | `9ce03b8` |
| W6 — A2 handoff | This commit |

**Stop after this W6 handoff commit and wait for review. No push. Phase B remains
unstarted. Task DONE is not SessionEnd.**
