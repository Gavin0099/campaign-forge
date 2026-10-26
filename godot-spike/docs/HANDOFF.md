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

**Ready for review of this fix segment.** Thoma now carries the same approved
short mace in idle and all six swing poses; the default screen has a Traditional
Chinese battle HUD; knight B has a consistent bone crest/light shield. Final
engineering checks pass. **Human playtest is HUMAN_PENDING; weapon is APPROVED (Owner, 2026-10-24); P010 remains
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

### Thoma weapon — APPROVED (Owner, 2026-10-24) — superseded by Owner decision 2026-10-24

**Short one-handed flanged mace:** blunt dark iron head, worn oak haft, small
brass collar echoing the medallion; forearm length, carried in his right hand.
It provides a compact, weighty blunt silhouette suitable for the medical friar
proposal without becoming a staff. The medallion remains a holy symbol, never
the weapon. No sword/blade/staff/book/glow or borrowed party-member equipment.

Historically, canon named no weapon (superseded by Owner decision 2026-10-24); the brief's evidence is retained without silently turning
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
check, not Owner/commercial approval. **Weapon is APPROVED (Owner, 2026-10-24) for every frame; superseded by Owner decision 2026-10-24.**
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

## spike-02 A3

**W1–W6 delivered for review; art completion is PARTIAL.** Thoma's short mace is
now Owner-approved. Five swing frames received garment repaints while retaining
A2 weapon/hand/foot geometry, but all five still have visible costume-detail
problems and remain **PLACEHOLDER**. Idle and recover retain model PASS. The
engineering checks and sampled knight readability checks pass; neither is a
human art or hit-feel verdict. **Human playtest: HUMAN_PENDING. P010: PROPOSED.**

Owner confirmation (Gavin, 2026-10-24) authorized this session/worktree and this
segment only. Started clean at brief `33e38d3` over A2 handoff `98c735e`, on
`codex/godot-spike` in `D:\campaign-forge\scratch\godot-spike`. No other checkout
was touched. **Commit only, no push. Phase B remains unstarted.**

### Run and review

From this worktree, Godot 4.7.2 standard / GDScript:

```powershell
godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd
godot --headless --path godot-spike --import
godot --path godot-spike --resolution 1280x720
```

If `godot` is absent from PATH, use the Owner-specified console executable at
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`.
Alternatively open `godot-spike/project.godot` and press F5. **Space** arms then
confirms; **R** replays; **1/2/3** select open/unit-blocked/terrain-blocked;
**M** toggles Reduced Motion; **H/?** opens help; **F1** opens debug; **Esc** closes
an overlay/forecast before exiting. Existing controls and rules are unchanged.

See [A3 verification](VERIFICATION.md#spike-02-a3) for exact commands, real exit
codes, retained failures, current source hashes and rendered evidence. The
[full 60fps movie](evidence/spike02-a3/attack-60fps.avi) is under 8 MiB and contains
all 59 frames; no subsampling. [Movie notes](evidence/spike02-a3/MOVIE.md).

### Thoma's weapon: APPROVED (Owner, 2026-10-24)

Gavin: 「就用單手短釘頭錘，開始補 5 格揮擊」. Canon weapon is a **short one-handed
flanged mace**, dark iron flanged head, worn oak haft, small brass collar echoing
the medallion, about forearm length, carried in his right hand. The brass
medallion stays his **holy symbol (聖徽)**, not a weapon. No staff, blade, book or
magic glow. This approval supersedes A2's weapon-pending status; it does not
approve the five motion drawings, combat rules, engine choice or other story.

W1 updated source and synced metadata, tests and A2 status notes. No confirmed
art/equipment section exists in `docs/DECISIONS.md`, so it was left untouched;
no D-row was invented and P010 remains PROPOSED. Historical equipment proposals
in the A2 narrative remain history under this explicit superseding decision.

### Frame audit and repaint limits

| Frame | Status | Reason |
| --- | --- | --- |
| `thoma/idle/01.png` | PASS | Recognizable original face, paired ivory leafy stole, layered cuffs/hem and equipment continuity at review and runtime scale; not Owner art approval. |
| `thoma/swing/00.png` | PLACEHOLDER | Leaf sprigs now come from the original, but doubled border/leaf density remains at patch edges; raised cuff transition and broad fan hem still differ from idle/recover. |
| `thoma/swing/01.png` | PLACEHOLDER | Original sprigs improve identity, but stole border blending and raised cuff folds still differ; the bell-shaped hem is retained from A2. |
| `thoma/swing/02.png` | PLACEHOLDER | Original sprigs and cuff cloth improve continuity, but compressed leaf detail, cuff patch boundary and swept underskirt contour still drift. |
| `thoma/swing/03.png` | PLACEHOLDER | Contact geometry is byte-preserved; stole seam/leaf density and broad underskirt hem remain inconsistent at detail scale. |
| `thoma/swing/04.png` | PLACEHOLDER | Trailing sprigs reuse original pixels, but stretched diagonal embroidery, front cuff transition and trailing hem remain visibly different. |
| `thoma/swing/05.png` | PASS | Recognizable original face, paired ivory leafy stole, layered cuffs/hem and equipment continuity at review and runtime scale; not Owner art approval. |

[New style check](../../shared-anim/thoma-weapon-style-check.png) includes original,
idle and all six swing frames, enlarged stole/cuff/hem rows and native-720p-size
row. [A2 style sheet](evidence/spike02-a3/style-check-a2.png) remains archived.
[Rendered old/new comparison](evidence/spike02-a3/contact-sheet-old-vs-new.png)
uses unscaled crops of actual 720p captures; camera sampling varies slightly
between separate replays. [Exact-scale asset comparison](evidence/spike02-a3/asset-sheet-old-vs-new.png)
is explicitly an asset sheet. [Per-criterion audit](../../shared-anim/frame-audit.json)
records palette-distance measurements and model findings separately from Owner
approval. All five repaints have FAIL criteria, so none was promoted to PASS.

Built-in image_gen was used once for each allowed frame 00–04, with all four
required references: original Thoma, weapon idle, recover and same-index A2
pose. Generated full figures changed proportions, so only cuff/hem cloth patches
were adopted, with original leafy sprigs transplanted into the stole. A2 alpha
and every unmasked pixel were preserved. This protects the pose, mace length,
head size/grip, feet and contact anchor but leaves the old motion-hem contour
unresolved. Further whole-figure regeneration was not adopted; one attempt per
frame is below the three-attempt cap. No idle/recover regeneration was needed.

All generated originals are immutable under `shared-anim/raw/`; no completely
rejected attempt was discarded. [Full prompts/reference/raw/runtime SHA-256](../../shared-anim/a3-swing-prompts.json),
[source record](../../shared-anim/SOURCES.md),
[cleanup implementation](../tools/prepare_a3_frames.py),
[exact masks](evidence/spike02-a3/repaint-masks/) and
[A2 byte-copy baseline/hashes](evidence/spike02-a3/baseline-a2/) support review.
Baseline frames are evidence-only; the manifest references the new live paths.
No original PNG was moved or edited, and no other character/environment was
generated. No Ferry Dusk palette was adopted.

### Knight B readability

All captures are rendered at native **1280×720**, with the HUD, name/role labels,
debug labels and damage text hidden. Grayscale is a live screen shader. Zoom
captures are actual attacks at follow-through after flash, at **1.4×**, not a
larger character-scale substitution. No knight art was changed.

| Setup | Rest color | Rest gray | Attack zoom color | Attack zoom gray | Model observation |
| --- | --- | --- | --- | --- | --- |
| 1 — open | PASS | PASS | PASS | PASS | B's pale shield and raised pale crest distinguish it from A's dark shield/plain helm even across separated positions |
| 2 — unit-blocked | PASS | PASS | PASS | PASS | Adjacent B remains distinct by shield value and crest while A reacts; labels are unnecessary in these samples |
| 3 — terrain-blocked | PASS | PASS | PASS | PASS | B remains identifiable on the lower bank; A's dark shield/plain helm remains different near the crossing |

[Per-image reasons, filenames, hashes and measured proxies](evidence/spike02-a3/knight-readability.json).
Shield B-minus-A screenshot luma difference: **50.337–69.548 / 255**. Same-pose
helm-mask difference: **16 px** at rest, **34 px** at attack zoom. The crest is
small at rest and shield value is the strongest cue. These are supporting
measurements, not human glance-latency evidence. **No clear sampled failure was
observed, so no silhouette-change proposal is made.** W4 preceded the W5 Thoma
sync; knight/environment bytes were unchanged. The result is limited to these
12 images and does not prove recognition across every animation or future map.

### Timing and engineering result

| Setup | Normal, strike to input-ready | Reduced Motion |
| --- | --- | --- |
| 1 — open | 0.936505 s | 0.752470 s |
| 2 — unit-blocked | 0.948820 s | 0.747849 s |
| 3 — terrain-blocked | 0.927993 s | 0.729133 s |

All are below **1.7 s**, including hitstop. Ordinary timing runs contain no GPU
readback. Movie strike-to-ready is **0.916667 s**, with five identical decoded
contact frames (**83.333 ms**). The offline encoder's wall time is not gameplay
latency. [Timing](evidence/spike02-a3/timing.json),
[movie hashes](evidence/spike02-a3/movie-index.json).

Full manifest equality against A2 is tested: canvas **512×512**, pivot
**[256,464]**, contact index **3**, anchor **[455,196]**, durations
**180/70/40/80/100/150 ms**, Reduced Motion keyframes, offsets and camera settings
remain unchanged. Tests also compare source/synced bytes, A2 baseline hashes,
approved weapon metadata, attempt bounds, exact alpha/unmasked pixels and the
protected contact grip/haft/head region. **37/37 GUT tests, 1162 assertions,
exit 0**; [test log](evidence/spike02-a3/test-run.log). After adding this section,
`godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a3_contract.gd -gexit`
passed **4/4 tests, 220 assertions, exit 0**, including the final handoff rows.
Its separate log is
[handoff-table-check.log](evidence/spike02-a3/handoff-table-check.log).

### Open items for Phase B and limits

- **HUMAN_PENDING:** actual human assessment of weapon weight, contact timing,
  continuity, input responsiveness and sound. Model review and automation do not
  substitute for it; Dummy audio does not verify physical-device audition.
- Shared **React/Godot asset-and-timing comparison rule** and React integration
  remain unimplemented and outside this segment. No React file was edited.
- Five motion frames still need costume/seam/hem cleanup before art completion
  can be claimed. Weapon approval is complete; frame-art approval is not.
- This remains one attack and three fixed setups, with no new AI, win/lose loop,
  formal battle rules, deployment, persistence, story or engine adoption. A3
  captures are 720p; A2's 1080p evidence is historical, not a new A3 1080p check.

### Resource self-check

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md):

| Item | Status | Evidence / scoped exception |
| --- | --- | --- |
| A — prototype-fast | PASS (criterion) | Bounded five-frame correction; unchanged one-attack mechanic; keep/partial criteria are explicit |
| A — level-design | N/A | No map, route, placement or objective edits; existing rule tests retained |
| A — game-ai | N/A | No enemy AI work authorized |
| A — game-ui-ux | PASS (scoped check) | Read pinned [skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md); actual native-resolution evidence and existing focus/Space/overlay tests retained; no HUD redesign |
| A — game-feel | PASS (engineering), HUMAN_PENDING | Read pinned [skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md); event/hold/recovery/Reduced Motion verified, human feel untested |
| B — Grid-Tactics separation | PASS (criterion) | No rule/view coupling changes; no reference-repo code or art copied |
| B — HopeMetal attribution | N/A | Nothing newly borrowed |
| B — new engine/dependency | PASS | Existing authorized Godot/GDScript/GUT only; no addon or dependency installed |
| C — full 3–5 minute battle | N/A, explicit exception | One-attack spike, no complete battle claim |
| C — understandable enemy actions | N/A, explicit exception | Fixed targets, no autonomous turns |
| C — win/lose | N/A, explicit exception | Not authorized in this spike |
| C — two tactical choices | N/A, explicit exception | Three fixtures are not a tactical choice loop |
| C — restart/change strategy | PASS (replay), N/A (strategy) | Real R replay captures and existing fixture-reset tests |
| C — no duplicate/stuck/invalid resolution | PASS (tested paths) | Existing rules/input tests plus complete captures, ready-state and geometry checks |
| C — 720p/1080p/keyboard | PASS (A3 720p/keyboard); A3 1080p N/A | A3 scope requires native 720p; prior A2 1080p is not represented as new evidence |
| C — automation vs human | PASS | Model results, 37-test suite and HUMAN_PENDING are separately identified |
| D — SRD/rule sources | N/A (new rules), PASS (scope) | No new SRD/WotC content; no G005/formal rule changes |
| D — authorization | PASS | Only shared-anim/ and godot-spike/ implementation/evidence; Owner's brief already present; no React/shared story edits, other worktree, push, main merge, PR, Actions, deployment or Phase B |

Imagegen skill used for the five permitted raster edits; cleanup and evidence
sheets use Pillow. No commercial assets or reference-repo code copied. Shared
PLAN/memory files were intentionally not edited under this narrow task scope;
this handoff records the milestone. No additional agent was spawned. Normal
commit hooks ran with only the nonblocking `missing_canonical_memory` advisory;
this is not evidence of a SessionEnd callback or canonical closeout.

| Step | Commit |
| --- | --- |
| W1 — mace APPROVED | `66665c1` |
| W2 — five repaints / A2 baseline | `e860b1e` |
| W3 — detailed style check / honest flags | `def261a` |
| W4 — knight readability evidence | `542e08b` |
| W5 — sync / tests / rendered verification | `a039a04` |
| W6 — A3 handoff | This commit |

**Stop after this W6 handoff commit and wait for review. No push. Phase B
remains unstarted. Task completion is not SessionEnd.**

## spike-02 A4

**W1-W6 delivered for review; art completion remains PARTIAL.** The five motion
costumes were rebuilt from the accepted idle/recover pixels using a reproducible
cutout rig, with no new image generation. This replaces the old fan/bell skirt
contour and avoids adding extra leaf rows, but visible costume joins and
sequence discontinuities remain. All five are honestly **PLACEHOLDER**; this is
not a completed costume-art pass. Engineering checks and rendered evidence pass.

Owner Gavin confirmed this session is the only agent in this worktree and
explicitly authorized A4 on 2026-10-24. Started clean at `8197026` (brief) over
A3 `bd80c5e`, branch `codex/godot-spike`, only in
`D:\campaign-forge\scratch\godot-spike`. **Commit only, no push.** The short
one-handed flanged mace remains **APPROVED**, P010 remains **PROPOSED**, human
hit-feel remains **HUMAN_PENDING**, and **Phase B is unstarted**.

### Run and reproduce

From this worktree, using installed Godot 4.7.2 standard/GDScript:

```powershell
godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd
godot --headless --path godot-spike --import
godot --path godot-spike --resolution 1280x720
```

If the wrapper is not on PATH, use
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`.
Space arms/confirms, R replays, 1/2/3 change fixture, M toggles Reduced Motion,
H/? opens help, F1 shows diagnostics, Esc closes the current overlay/forecast.
All existing gameplay/HUD behavior is unchanged.

Offline Python/Pillow: `godot-spike/tools/prepare_a4_frames.py --build`, then
`a4_style_check.py`, `a4_contact_sheet.py`, and sync/import. The separate
`check_a4_reproduction.py` reconstructs in memory without rewriting files and
proves exact live PNG bytes and protection masks. Scripts install nothing.

[Method and one-frame proof](evidence/spike02-a4/METHOD.md),
[reference region coordinates/masks](evidence/spike02-a4/reference-regions/regions.json),
[rig controls](evidence/spike02-a4/reference-regions/rig-controls.json),
[measured reference palette](evidence/spike02-a4/reference-regions/palette.png).

Continuous reference torso/skirt carries both stole bands, embroidery, bag,
medallion and layered hem. Separate reference cuffs and face/hair follow the
pose. A3 motion arms/torso twist and fixed mace/feet are retained. A small region
behind the reference's idle mace is reconstructed with adjacent plain reference
pixels; that patch is still visibly imperfect. No full figure was regenerated.
The body uses modest horizontal ease and shear; all source regions and control
points are committed. W1's rejected rigid proof is retained. W4 corrected raw
RGBA preservation after a real failing test, then regenerated all live evidence.

### Frame verdicts

Model observations only; no Owner/commercial art approval. A reference endpoint's
sequence PASS means it is byte-unchanged; adjacent transition failures are
assigned to the motion frames and all six pairs are explicitly FAIL in
[sequence-check.json](evidence/spike02-a4/sequence-check.json). Thus the reference
PASS rows do not claim an overall clean animation.

| Frame | Status | Stole | Embroidery | Cuffs | Hem | Face/hair | Palette | Sequence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `thoma/idle/01.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Byte-unchanged A3 reference; model PASS retained, not Owner art approval. |
| `thoma/swing/00.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | Reference pixel method fixes the old fan contour and duplicate motif rows, but shoulder band meets retained raised-arm paint abruptly; bag/plain-cloth clone has a visible horizontal seam. fan contour replaced with reference edge, but left boot/hem connection is too narrow and near-idle drape lacks coil. |
| `thoma/swing/01.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | Reference pixel method fixes the old fan contour and duplicate motif rows, but upper band/arm seam and horizontal bag clone edge remain visible. reference scalloped edge retained but transition from preceding wide stance is abrupt. |
| `thoma/swing/02.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | Reference pixel method fixes the old fan contour and duplicate motif rows, but squared shoulder cut and waist overlay boundary expose the cutout construction. old swept fan removed, but reference hem bridges the fixed stance awkwardly. |
| `thoma/swing/03.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | Reference pixel method fixes the old fan contour and duplicate motif rows, but waist/shoulder joins and cloned bag occlusion remain visible even though full source bands are used. reference-shaped edge replaces broad fan; wide planted stance still reads disconnected at the left ankle. |
| `thoma/swing/04.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | Reference pixel method fixes the old fan contour and duplicate motif rows, but torso twist retains an A3 shoulder seam; reference-band/body junction and bag clone remain apparent. trailing contour now derives from reference, but floor/boot overlap and recovery shape jump remain. |
| `thoma/swing/05.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | Byte-unchanged A3 reference; model PASS retained, not Owner art approval. |

[1:1 region comparison](evidence/spike02-a4/region-check.png),
[seven-frame sequence and onion strip](evidence/spike02-a4/sequence-strip.png),
[shared style check](../../shared-anim/thoma-weapon-style-check.png),
[rendered A3/A4 comparison](evidence/spike02-a4/contact-sheet-a3-vs-a4.png),
[exact same-scale asset comparison](evidence/spike02-a4/asset-sheet-a3-vs-a4.png),
[A3 byte baseline/hashes](evidence/spike02-a4/baseline-a3/hashes.json).

Six-region details and one-line failure reasons live in
[frame-audit.json](../../shared-anim/frame-audit.json). Stole, cuffs, hem and
sequence fail in every motion frame; the specific motif, face/hair and palette
checks pass. No PLACEHOLDER was removed. Palette deltas measure masked mean RGB,
not seam quality or human recognition. No commercial/repository art was copied.

### Measured timing and engineering evidence

| Setup | 720p normal | 720p Reduced Motion | 1080p normal | 1080p Reduced Motion |
| --- | --- | --- | --- | --- |
| Open | 0.917815 s | 0.650812 s | 0.919160 s | 0.684374 s |
| Unit-blocked | 0.917651 s | 0.684154 s | 0.917966 s | 0.667565 s |
| Terrain-blocked | 0.917613 s | 0.667759 s | 0.917747 s | 0.684457 s |

All twelve ordinary rendered runs include hitstop, exclude screenshot readback
and finish below **1.7 s** with input unlocked. [720p timing](evidence/spike02-a4/timing.json),
[1080p timing](evidence/spike02-a4/timing-1080p.json).

Manifest is identical to A3: **512x512**, pivot **[256,464]**, contact index **3**,
anchor **[455,196]**, durations **180/70/40/80/100/150 ms**, camera/offsets and
Reduced Motion keys unchanged. Fixed A3 reference hashes match; protected
weapon/head/grip, foot masks and ground pixels match raw RGBA. A3 and A2
baselines are evidence only, never manifest frames. Source/synced files: **64**
byte-identical. Read-only reconstruction reproduces all five live PNG hashes.

Full GUT: **42/42 tests, 1,583 assertions, exit 0**. Historical A3 alpha/audit
assertions now target the archived A3 bytes, while five added A4 tests verify the
current contracts. The first failed protected-RGBA run and the fix are retained;
assertions were not relaxed. [Test log](evidence/spike02-a4/test-run.log),
[correction](evidence/spike02-a4/W4-CORRECTION.md),
[verification commands and actual exits](VERIFICATION.md#spike-02-a4).

Both rendered runs report `CAPTURE_COMPLETE A4 movie=false runs=6 shots=13 pass=true`.
Required anticipation/smear/contact/follow-through/idle PNGs exist at 1280x720 and
1920x1080; extra raised/recovery and A3 comparison shots are also retained.
1080p initially failed because Windows clamped the viewport to 1875x1055; the
capture tool's minimum size was corrected, not the images upscaled. Failure
log/dimensions and one rejected image are preserved in the evidence directory.

[Full 60 FPS clip](evidence/spike02-a4/attack-60fps.avi): **59 frames**, **7,270,584
bytes**, no subsampling. Strike-to-ready **0.916667 s**; five identical decoded
contact frames give **83.333 ms** hold with visible resume. [Movie details](evidence/spike02-a4/MOVIE.md),
[source hashes](evidence/spike02-a4/source-hashes.json). Dummy audio does not
establish physical-device sound quality.

### Open items and limits

- Five costume frames still need art work on shoulder/waist joins, cuff edges,
  reference-mace occlusion repair and hem-to-stance/sequence continuity. A4 has
  changed the construction method but has not met full costume-art acceptance.
- **HUMAN_PENDING:** human playtest for hit weight, contact timing, responsiveness,
  animation continuity and sound. Automated capture/model review cannot replace it.
- Shared React/Godot asset-and-timing comparison rule remains open for Phase B.
  React was neither edited nor integrated. This handoff does not start B.
- No battlefield/props/knight edits, Ferry Dusk palette, rule/HUD/timing changes,
  engine adoption, new story/Ink, formal save system, AI or complete battle loop.
- This is task DONE, not SessionEnd. No canonical daily record was hand-edited.
  Shared PLAN/memory edits are outside the narrower A4 scope; this section records
  the milestone. Normal hooks ran with the nonblocking missing_canonical_memory
  advisory; their execution is not a claim of full lifecycle acceptance.

### Resource self-check

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md):

| Item | Status | Evidence / scoped exception |
| --- | --- | --- |
| A — prototype-fast | PASS (criterion) | Bounded five-frame proof/rig; explicit rejection conditions and honest PLACEHOLDER; no extra mechanic |
| A — level-design | N/A | No terrain, route, objective or placement changes |
| A — game-ai | N/A | No AI work authorized |
| A — game-ui-ux | PASS (scoped check) | Read pinned [skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md); actual 720p/1080p captures and existing keyboard/focus/overlay GUT checks; no HUD redesign |
| A — game-feel | PASS (engineering), HUMAN_PENDING | Read pinned [skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md); same-frame impact, hold, input-ready and Reduced Motion checked; no human feel claim |
| B — Grid-Tactics separation | PASS (criterion) | Rule/view separation unchanged; no code/art newly borrowed |
| B — HopeMetal attribution | N/A | No new reference-repo code or assets copied |
| B — new engine/dependency | PASS | Existing authorized Godot/GDScript/GUT/Pillow only; nothing installed |
| C — full 3-5 minute battle | N/A, explicit scope exception | One-attack costume spike, no complete-battle claim |
| C — understandable enemy actions | N/A, explicit scope exception | Fixed fixtures; no autonomous enemy turn |
| C — win/lose | N/A, explicit scope exception | Not in authorized spike |
| C — two tactical choices | N/A, explicit scope exception | Three fixtures are not a tactical decision loop |
| C — restart/change strategy | PASS (replay), N/A (strategy) | Real R replay captures and retained reset tests; strategy loop not claimed |
| C — no duplicate/stuck/invalid resolution | PASS (tested paths) | Full existing tests plus complete rendered runs with input-ready and unchanged geometry contract |
| C — 720p/1080p/keyboard | PASS (automated) | Both native rendered sizes; retained physical Space dispatch and focus/overlay tests |
| C — automation vs human | PASS | 42-test engineering result separate from HUMAN_PENDING and partial art |
| D — SRD/rule sources | N/A (new rules), PASS (scope) | No rule change, new SRD/WotC content or G005 change |
| D — authorization | PASS | Only shared-anim/ and godot-spike/ changed in these six steps; existing Owner brief is the only other path over bd80c5e; no other worktree, React, push, main merge, PR, Actions, deployment, S4 or B |

No sub-agent was spawned. No imagegen attempt was made; the Owner explicitly
requested scriptable compositing/warping, so offline Pillow implements it.
Model art observations are not independent review or Owner approval.

| Step | Commit |
| --- | --- |
| W1 — method/library/proof | `bd46c93` |
| W2 — five reference-derived frames / A3 baseline | `2809547` |
| W3 — region/sequence checks / honest flags | `bdd33a5` |
| W4 — sync / raw RGBA correction / 42 tests | `c28f046` |
| W5 — rendered verification / movie / hashes | `719473f` |
| W6 — A4 handoff | This commit |

**Stop after this W6 handoff commit and wait for review. No push. Phase B remains
unstarted. Task completion is not SessionEnd.**

W6 final table verification: `GODOT --headless --path godot-spike -s
res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a4_contract.gd -gexit`
passed **5/5 tests, 425 assertions, exit 0** after this section was written.
[Final handoff-table log](evidence/spike02-a4/handoff-table-check.log).

## spike-02 A5

2026-10-24, Codex, branch `codex/godot-spike`, isolated worktree
`D:\campaign-forge\scratch\godot-spike`, start cc164b2 above A4 8592fbb.
Owner confirmed this is the only agent session in this worktree.

**Engineering verification passes; art repair is PARTIAL.** All five rebuilt
motion frames remain PLACEHOLDER. Exactly one satchel and unit horizontal
motif scale now pass. Shoulder/waist/cuff fold joins, plain-cloth repair edges,
hem/boot attachment and six adjacent transitions still fail. Those are
unresolved art defects, not completed fixes. This handoff completes the six
requested work steps; it does not claim all A4 art defects have been solved.
Human hit-feel playtest remains **HUMAN_PENDING**. Weapon design/status stays
**APPROVED canon**: Thoma's short one-handed flanged mace.

**Phase B: CANCELLED by Owner (2026-10-24, Godot chosen).** Campaign Forge uses
Godot directly. No React work remains in this spike. The Owner should update
P010 to reflect this decision; Codex did not edit P010 or any decision record.
Earlier handoff language about engine selection/comparison is historical and
superseded by this explicit Owner instruction.

### Run

From this worktree root in PowerShell, using the existing approved Godot
binary (the `godot.cmd` PATH wrapper also works):

```powershell
$a5Godot = 'C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
& $a5Godot --headless --path godot-spike -s res://tools/sync_shared_anim.gd
& $a5Godot --headless --path godot-spike --import
& $a5Godot --path godot-spike --resolution 1280x720
```

Controls retained: 1/2/3 select open, unit-blocked, terrain-blocked fixtures;
R replays, Space operates the focused attack action, M toggles Reduced Motion,
G toggles grid, F1 diagnostics, Esc uses the existing overlay/back behaviour.
These are fixed one-attack fixtures, not a complete battle or rules engine.

Offline reproduction uses the installed Python:

```powershell
$a5Python = 'C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe'
& $a5Python godot-spike/tools/check_a5_reproduction.py
# Explicit rebuilding, if desired, writes only 00-04 and generated evidence:
& $a5Python godot-spike/tools/prepare_a5_frames.py --build
& $a5Python godot-spike/tools/a5_style_check.py
& $a5Python godot-spike/tools/a5_audit.py
& $a5Python godot-spike/tools/a5_contact_sheet.py
# Then sync/import as above; package_a5_evidence.py appends the real runtime row.
```

### Method and changes

Retained the unmodified A4 reference cutout helpers, source polygons, pose
controls, translated face, cuff quadrilaterals and exact protected weapon/feet.
One continuous recover-reference body replaces the bag-bearing clone patches;
two recorded plain-cloth transfers remove its occluded source mace. The upper
cape silhouette is retained, arm/cuff joins feather inward, and a small smoothing
pass is confined to committed narrow 6/8px seam bands. Global garment scale is
1.0. Lower-hem ease begins below the last motif row, widening stance coverage
without widening embroidery. No AI generation request or whole-frame repaint.
No new motif, costume design or palette. Original reference PNGs were not moved
or edited. A4 body/source library and prior baselines remain untouched.

[Method and per-frame rationale](evidence/spike02-a5/METHOD.md),
[rig controls](evidence/spike02-a5/rig-controls.json),
[committed seam mask coordinates/areas](evidence/spike02-a5/seam-masks/coordinates.json),
[scale measurement](evidence/spike02-a5/scale-measurement.json),
[provenance](../../shared-anim/a5-swing-prompts.json).
Mask areas: 7,608 / 5,450 / 5,939 / 6,004 / 5,687px, bounded at 10,000px
(<4% of canvas); widths <=8px. The embroidery ROI map is 25px ->25px (A4 was
28.75px), 0% local horizontal deviation versus a <=5% tolerance. This is an
analytical mapping measurement, not a perceptual raster-quality score.

W1 draft remains the original draft. W3 inspection found an inherited
reference-mace fragment in the first W2 transfer: the final version uses two
plain-cloth occlusion quads and restores exact face pixels after smoothing.
There is now one visible bag and no old mace head inside the live robe, but
its cloth repair boundary remains visible and is a seam FAIL. Source/mask and
runtime hashes/cleanup are recorded for all five frames. No AI attempts or
rejected AI artifacts (0/3 per frame); no image service was used.

### Audited frame table

Model observations only. `PASS` on immutable endpoint sequence checks means
the original endpoint remains accepted; failing incoming/outgoing transitions
are explicitly assigned to motion frames in sequence-check.json. This is not
an assertion that the complete animation sequence passes. Every live PASS
frame must pass all ten checks and have bag_count==1; otherwise PLACEHOLDER.

| Frame | Status | Stole | Embroidery | Cuffs | Hem | Face/hair | Palette | Seams | Bag count | Feet | Sequence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `thoma/idle/01.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | Byte-unchanged reference endpoint; adjacent transition failures are assigned to motion frames; not Owner art approval. |
| `thoma/swing/00.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | 1 PASS | FAIL | FAIL | Single bag and unit motif scale fixed; horizontal plain-cloth repair edge under satchel remains visible; right boot remains detached; left planted sole unchanged. |
| `thoma/swing/01.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | 1 PASS | FAIL | FAIL | Single bag and unit motif scale fixed; waist/body and bag-bottom cloth transition retain brightness steps; hem-to-boot transition remains narrow and not anatomically continuous. |
| `thoma/swing/02.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | 1 PASS | FAIL | FAIL | Single bag and unit motif scale fixed; shoulder/torso and plain-cloth bag repair edges remain visible; far boot has an exposed gap above its upper edge; fixed soles alone do not prove attachment. |
| `thoma/swing/03.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | 1 PASS | FAIL | FAIL | Single bag and unit motif scale fixed; plain-cloth patch ends in a horizontal bag-bottom seam; shoulder seam still reads; left contact improved; right leg-to-boot gap and boot overlap still fail. |
| `thoma/swing/04.png` | PLACEHOLDER | FAIL | PASS | FAIL | FAIL | PASS | PASS | FAIL | 1 PASS | FAIL | FAIL | Single bag and unit motif scale fixed; twisted sleeve/body and bag-bottom cloth repair remain apparent; trailing boot/hem overlap and far-leg gap remain; no continuous leg anatomy. |
| `thoma/swing/05.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | Byte-unchanged reference endpoint; adjacent transition failures are assigned to motion frames; not Owner art approval. |

Evidence: [region check](evidence/spike02-a5/region-check.png),
[sequence strip](evidence/spike02-a5/sequence-strip.png),
[style check](../../shared-anim/thoma-weapon-style-check.png),
[rendered A4/A5 comparison](evidence/spike02-a5/contact-sheet-a4-vs-a5.png),
[separate equal-scale asset comparison](evidence/spike02-a5/asset-sheet-a4-vs-a5.png).
The region sheet includes unscaled idle/recover/A4/A5 crops for stole,
embroidery, cuffs, hem, face/hair, palette, shoulder seam, waist seam, bag and
hem-to-feet, plus actual native 720p runtime crops. Six adjacent-pair mask
colour deltas and garment silhouette IoU are in
[sequence-check.json](evidence/spike02-a5/sequence-check.json). These proxies
measure sampled colour/overlap, not fold continuity or Owner acceptance.
A4 byte baselines and hashes live only under evidence/baseline-a4/; the live
manifest references no archived A4/A3/A2 frame. The historical A4 style sheet
is [preserved](evidence/spike02-a5/style-check-a4.png).

### Verification and unchanged timing

Full suite: **48/48 GUT tests, 2,126 assertions, exit 0**.
[Full test log](evidence/spike02-a5/test-run.log). All prior tests retained;
historical A4 checks target the A4 archive, while new live A5 contracts check
references, entire manifest, canvas/pivot/contact geometry and raw protection,
status/table agreement, all PASS gates, bag count, actual seam support/area,
provenance, local scale and six adjacent pairs. Sync parity: 65 files.
[Reproduction log](evidence/spike02-a5/reproduction.log) proves exact PNG bytes,
protection/seam masks and zero opaque pixels below y=464 in five motion frames.
Unchanged soles/ground bytes do not establish hem-to-boot attachment; feet
checks still FAIL for that visual reason.

Manifest is unchanged: 512x512, pivot [256,464], contact frame index 3, mace head
anchor [455,196], frame timing **180 / 70 / 40 / 80 / 100 / 150ms**, same offsets,
impact, camera and Reduced Motion indices [0,3,5]. Smear remains excluded from
Reduced Motion. No gameplay, HUD, terrain, props, knights or rule changes.

Actual rendered ordinary timing, including hitstop and return to input-ready:

| Resolution/mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.956431s | 0.951041s | 0.943756s |
| 720p Reduced Motion | 0.754909s | 0.720051s | 0.763822s |
| 1080p normal | 0.925129s | 0.956433s | 0.923250s |
| 1080p Reduced Motion | 0.743256s | 0.734362s | 0.766221s |

All 12 are below **1.7s**, contact triggers share a process frame, input becomes
ready, real hitstop >=80ms. Each resolution has 13 screenshots from a rendered
`CAPTURE_COMPLETE A5 movie=false runs=6 shots=13 pass=true` run. Readbacks are
on separate replays and excluded from timing. Native dimensions are verified;
1080p is not enlarged from 720p. Links/commands/real exit codes are in
[VERIFICATION — spike-02 A5](VERIFICATION.md#spike-02-a5).

[Complete 60fps AVI](evidence/spike02-a5/attack-60fps.avi): 59 native 1280x720
frames, **7,269,540 bytes**, no subsampling. Strike frame 2 to ready frame 57:
**0.916667s**. Contact frames 20-24 are identical decoded full RGB (**83.333ms**),
frame 25 resumes. [Movie details](evidence/spike02-a5/MOVIE.md),
[decoded frame hashes](evidence/spike02-a5/movie-index.json),
[source hashes](evidence/spike02-a5/source-hashes.json),
[720p timing](evidence/spike02-a5/timing.json),
[1080p timing](evidence/spike02-a5/timing-1080p.json).
Encoding wall time is not gameplay latency. Audio used Dummy driver, with no
speaker/headphone audition. Automation is not human playtest.

### Open questions / limits for review

- **Art NOT complete:** five PLACEHOLDER frames and all six neighbouring
  transitions retain explicit failures above. Bag count and unit local scale
  are improvements; no claim that all A4 P1/P2 defects were eliminated.
- Narrow smoothing softens joins but cannot reconstruct pose-specific fold
  anatomy. The retained cutout sleeve folds and fixed far-leg pixels still
  conflict with the reference body/hem. Wider hem coverage helps a planted
  ankle but does not solve the far-leg gap. No silhouette/colour proxy waives
  these failures. Further repairs require review/Owner direction after W6.
- **HUMAN_PENDING:** hit feel, readable motion at normal play distance and
  audible mix. Model judgement is neither human acceptance nor independent review.
- **Owner action:** update P010 for Godot chosen / Phase B cancelled; not edited
  here. No React follow-up exists in this spike.
- The brief limits writes to shared-anim/ and godot-spike/. Root PLAN/memory,
  ui-prototype/PLAN and story/shared decision files were not edited or locked;
  this handoff/verification are the authorized milestone record.

### Resource self-check

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md). Relevant
pinned game-ui-ux and game-feel skills were read for the scoped verification;
no new feature or code/art was borrowed from external repos.

| Item | Status | Evidence / scoped exception |
| --- | --- | --- |
| A — prototype-fast | PASS (criterion) | Bounded W1 proof, five frame repairs, predeclared rejection conditions; no extra mechanic |
| A — level-design | N/A | No level, route, objective or placement changes |
| A — game-ai | N/A | No AI logic work authorized |
| A — game-ui-ux | PASS (scoped verification) | Read [pinned skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md); actual native 720p/1080p captures, existing keyboard/focus/overlay tests pass; HUD unchanged |
| A — game-feel | PASS (engineering), HUMAN_PENDING | Read [pinned skill](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md); same-frame impact, real hold, return to ready and Reduced Motion tested; art/feel not approved |
| B — Grid-Tactics separation | PASS (criterion) | Game rules/view separation unchanged, no reference code copied |
| B — HopeMetal attribution | N/A | No code/assets borrowed |
| B — new engine/dependency | PASS | Existing approved Godot/GDScript/GUT/Pillow only; Godot chosen by Owner; nothing installed |
| C — full 3-5 minute battle | N/A, explicit scope exception | One-attack five-frame art segment, no full-battle claim |
| C — understandable enemy actions | N/A, explicit scope exception | Three fixed fixtures, no autonomous enemy turn |
| C — win/lose | N/A, explicit scope exception | Not part of this spike |
| C — two tactical choices | N/A, explicit scope exception | Fixtures are not a tactical decision loop |
| C — restart/change strategy | PASS (replay), N/A (strategy) | Repeated R input and retained reset tests; no strategy loop claim |
| C — no duplicate/stuck/invalid resolution | PASS (tested paths) | 48 tests plus 12 rendered timed runs and complete input-ready movie; gameplay unchanged |
| C — 720p/1080p/basic keyboard | PASS (automated) | Actual 26 screenshots, physical key-event dispatch in captures and retained keyboard/focus tests; no human input claim |
| C — automated vs human | PASS | Engineering pass, art partial/PLACEHOLDER and HUMAN_PENDING are separately recorded |
| D — SRD/rule sources | N/A (new rules), PASS (scope) | No new rule, SRD/WotC content or G005 change |
| D — project authorization | PASS | Own worktree only; no ui-prototype, other worktree, new story, S4, push, main merge, PR, Actions or deploy |

No unexplained C/D failure: full-battle items are explicit scope exceptions,
not a declaration of complete playable battle. Art failures remain open and
must be considered by the reviewers/Owner. No subagent spawned. The
external-executable-trust-audit skill was applied to local tool identification;
its full adversarial hardening ceiling is explicitly not claimed in VERIFICATION.
No custom launcher or global trust change. Normal hooks gave the existing
report-only missing_canonical_memory advisory; no hook bypass or SessionEnd.

| Step | Commit |
| --- | --- |
| W1 — method, seam masks, scale, proof | `a3657ab` |
| W2 — five frames and A4 baseline | `cf41d1e` |
| W3 — region/sequence audit and correction | `f1e0e01` |
| W4 — sync/import/48 tests | `a607a8b` |
| W5 — rendered verification/movie | `e5faf32` |
| W6 — this handoff and final table check | This commit |

**STOP after W6 commit; wait for review. Commit only, no push, merge or PR.
Task DONE is not SessionEnd.**

Final W6 actual-handoff check: `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a5_contract.gd -gexit` passed **6/6 tests, 540 assertions, exit 0** after this section and its exact table were written. [Final log](evidence/spike02-a5/handoff-table-check.log).

## spike-02 A6

**W1–W6 delivered for review; engineering passes, art remains PARTIAL.**
Complete frame generation repairs the recurring A5 floating sleeve/hem pieces
and detached boots. All five motion frames still have botanical motif/fringe,
face and sequence fidelity failures and remain **PLACEHOLDER**. Frame04 also
misses A5's follow-through mace-head height by about19px: the requested exact
painted mace pose geometry is **not fully met**. No false all-art PASS is claimed.
Human hit-feel/playtest remains **HUMAN_PENDING**, Owner art approval pending.
Owner accepted Godot/P010; React and Phase B are **CANCELLED**. Thoma's short
one-handed flanged mace remains **APPROVED canon**. No decision record edited.

### Run and method

Use this worktree on `codex/godot-spike`. `GODOT` is the Owner's existing
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`.

```text
GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd
GODOT --headless --path godot-spike --import
GODOT --path godot-spike --resolution 1280x720
```

Choose a target/preview and confirm, or use R to replay the scoped attack;
1/2/3 choose the existing fixtures, M toggles Reduced Motion, F1 diagnostics.
This remains a one-attack art spike, not a full tactical battle.

[METHOD](evidence/spike02-a6/METHOD.md) defines the bounded proof and cleanup.
Built-in image_gen generated each full figure independently with exactly
idle/01 + swing/05 for costume/face/palette/style/mace and A5 same-index ONLY
for pose/silhouette. No cutout rig, costume-piece transfer or region warp.
Only whole-frame uniform scale/translate, alpha cleanup and recorded idle
palette remap were used. [All raw candidates](evidence/spike02-a6/candidates/)
are unchanged; [exact prompts/settings/reference/raw/runtime hashes](../../shared-anim/a6-swing-prompts.json)
and [SOURCES](../../shared-anim/SOURCES.md#spike-02-a6--complete-per-frame-regeneration)
retain every attempt and cleanup mask. Seed/model/quality were not exposed.

W1's [swing02 proof](evidence/spike02-a6/proof-02.png) clearly beats A5: no loose
offhand cuff fragment, triangular hem scrap or disconnected right boot, while
retaining the two-band stole/teal robe/ivory cuffs/satchel/pendant design.
Gate PASS permitted W2; it did not approve exact motifs or a finished sequence.
All A5 live PNGs are preserved byte for byte in [baseline-a5](evidence/spike02-a6/baseline-a5/)
with hashes; no archive is referenced by the manifest. Idle01/recover05 remain
byte-identical. Original atlases were neither moved nor edited.

| Frame | Attempts / adopted | Reason |
| --- | --- | --- |
| swing/00 | 1/4, attempt1 | Whole wind-up removes detached shoe/broken hem |
| swing/02 | 2/4, attempt1 | Best W1 anatomy/costume proof; attempt2's shoulder/stole/wrist drift was worse |
| swing/03 | 1/4, attempt1 | Continuous contact arm/body; uniform transform anchors head center at [455,196] |
| swing/04 | 1/4, attempt1 | Continuous follow-through body/boots; mace-head height still fails A5 pose fidelity |
| swing/01 | 1/4, attempt1 | Authorized exception: old01 visibly pops in bag/hem/cuff proportions between new00/02 |
| idle/01, swing/05 | 0, unchanged | Fixed costume/style endpoints |

Generation order after W1 proof:00 → adopt completed02 →03 →04 →01. No frame
was started before the previous candidate/transform/pick was recorded.
The01 exception is demonstrated in [before](evidence/spike02-a6/01-neighbours-before.png)
and [after](evidence/spike02-a6/01-neighbours-after.png) equal-scale neighbour
comparisons; A5's single-frame PASS does not imply a match to new neighbours.

### Audited frame table

All results are model observations, not Owner approval. Reference endpoint
PASS preserves the byte-identical endpoint; failing adjacent transitions are
assigned to the generated motion frames. No complete sequence PASS is claimed.

| Frame | Status | Stole | Embroidery | Cuffs | Hem | Face/hair | Palette | Seams | Bag count | Feet | Mace | Sequence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `thoma/idle/01.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | Byte-identical reference endpoint; motion transition failures remain assigned to motion frames; not Owner approval. |
| `thoma/swing/00.png` | PLACEHOLDER | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | 1 PASS | PASS | PASS | FAIL | Structural fragments/feet repaired; generated motif/fringe and face fidelity still drift; sequence retains visible pops. |
| `thoma/swing/01.png` | PLACEHOLDER | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | 1 PASS | PASS | PASS | FAIL | Structural fragments/feet repaired; generated motif/fringe and face fidelity still drift; sequence retains visible pops. |
| `thoma/swing/02.png` | PLACEHOLDER | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | 1 PASS | PASS | PASS | FAIL | Structural fragments/feet repaired; generated motif/fringe and face fidelity still drift; sequence retains visible pops. |
| `thoma/swing/03.png` | PLACEHOLDER | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | 1 PASS | PASS | PASS | FAIL | Structural fragments/feet repaired; generated motif/fringe and face fidelity still drift; sequence retains visible pops. |
| `thoma/swing/04.png` | PLACEHOLDER | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | 1 PASS | PASS | FAIL | FAIL | Structural fragments/feet repaired; generated motif/fringe and face fidelity still drift; sequence retains visible pops. Follow-through mace-head height differs from A5. |
| `thoma/swing/05.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | Byte-identical reference endpoint; motion transition failures remain assigned to motion frames; not Owner approval. |

[Region check](evidence/spike02-a6/region-check.png):200 unscaled crops, including
stole, embroidery, cuffs, hem, seams, bag, feet, face/hair, palette and mace,
against idle/recover/A5, plus actual native720p replay crops.
[Sequence strip](evidence/spike02-a6/sequence-strip.png),
[seven-frame style check](../../shared-anim/thoma-weapon-style-check.png),
[rendered A5-vs-A6](evidence/spike02-a6/contact-sheet-a5-vs-a6.png) and
[separate equal-scale asset comparison](evidence/spike02-a6/asset-sheet-a5-vs-a6.png)
allow source and in-game checks independently.
[Full per-check reasons](../../shared-anim/frame-audit.json),
[geometry landmarks](evidence/spike02-a6/geometry-check.json) and
[model observations](evidence/spike02-a6/W3-OBSERVATIONS.md) preserve failures.

Real playback is backed by [all59 decoded rendered frames](evidence/spike02-a6/playback-every-frame.png),
[seven actual keyposes](evidence/spike02-a6/playback-keyframes.png),
[raw selected rendered PNGs](evidence/spike02-a6/sequence-runtime/) and
[post-draw trace/check](evidence/spike02-a6/playback-check.json).
No duplicate bag, floating cuff/boot or new01 cutout seam flashes observed.
Motif/fringe/shading changes and hem/stance width still pop; sequence FAIL.
Six adjacent pairs record region RGB delta, garment IoU and character-height
delta in [sequence-check.json](evidence/spike02-a6/sequence-check.json).
These proxies include pose/occlusion; they cannot approve cloth continuity.
The crop GIF is a preview with quantized GIF timing; AVI/trace is authoritative.

### Engineering and timing

**55/55 GUT tests,2,772 assertions, exit0**; [full log](evidence/spike02-a6/test-run.log).
48 prior tests retained; A5 art/protection assertions now read immutable A5
bytes. Seven A6 tests cover fixed endpoints/manifest/timing, all archive-path
exclusions, bounded retained attempts/three reference hashes/raw/runtime hashes,
canvas/ground/contact, audit/table/all-PASS gates/bag count and actual playback
evidence. They explicitly retain04's geometry failure. Source/copied parity:
66 files. [Reproduction](evidence/spike02-a6/reproduction.log) rebuilds all five
adopted PNGs and masks exactly from raw files/settings, with no costume transfer.

Manifest is unchanged:512x512 canvas, pivot[256,464], contact index3 and
anchor[455,196], durations **180/70/40/80/100/150ms**, same offsets/camera/
impact/scenarios, Reduced Motion[0,3,5] excludes smear02. Whole-figure measured
head-to-ground348.369–356.224px is within360+/-18px; opaque soles y463–464.
Manual raw landmarks have +/-3px selection uncertainty. Generated mace/hand
pixels differ; fixed manifest contracts do not certify exact painted geometry.

| Resolution/mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.947969s | 0.945312s | 0.951975s |
| 720p Reduced Motion | 0.752756s | 0.761012s | 0.752048s |
| 1080p normal | 0.942829s | 0.943195s | 0.949734s |
| 1080p Reduced Motion | 0.756074s | 0.760203s | 0.756672s |

All12 no-readback runs finish below **1.7s**, return input-ready and trigger
contact/SFX/VFX in one process frame. Screenshot replays are excluded.
Each resolution produced13 real screenshots with
`CAPTURE_COMPLETE A6 movie=false runs=6 shots=13 pass=true`.
[VERIFICATION](VERIFICATION.md#spike-02-a6) links poses at native720p/1080p,
actual commands and real exits; [720p](evidence/spike02-a6/timing.json),
[1080p](evidence/spike02-a6/timing-1080p.json),
[source hashes](evidence/spike02-a6/source-hashes.json),
[package audit](evidence/spike02-a6/evidence-audit.json).

[Complete60FPS movie](evidence/spike02-a6/attack-60fps.avi), captured inW3 and
retained unchanged forW5:59 native1280x720 frames, **7,272,456 bytes**, no frame
subsampling/transcoding. Strike2→ready57 is **0.916667s**, contact20–24 is
five identical decoded RGB frames/**83.333ms**, frame25 resumes.
[MOVIE](evidence/spike02-a6/MOVIE.md), [hashes](evidence/spike02-a6/movie-index.json).
One untraced terminal movie frame exactly equals the preceding traced ready
image;58 genuine trace records were kept. The initial59-vs58 assertion failure
is retained, not hidden or replaced by an invented trace. Encoding wall time
is not gameplay latency; Dummy audio is not a speaker/headphone audition.

### Open questions and resource self-check

- **Art NOT complete:** five PLACEHOLDER frames; exact motif/fringe and face
  matching and continuous sequence fidelity remain open.04's mace pose geometry
  remains an explicit unmet requirement. No patch re-compositing was attempted.
- **HUMAN_PENDING:** hit feel, real player motion readability and physical audio.
  Model inspection, GUT and recorded synthetic input are not human acceptance.
- Owner art approval remains pending. This task stops for review; no further
  generation, other characters, PhaseB/React work or follow-up scope is assumed.

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md). Relevant
[game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md)
and [game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md)
were read for scoped verification. No new effect/UI feature, reference-repo
code, commercial art, engine/addon/dependency or other character was introduced.

| Resource item | Result | Evidence / scoped exception |
| --- | --- | --- |
| A prototype-fast | PASS, scoped criterion | Bounded02 proof gate, max4 attempts, raw candidates retained; relative structure improves, final rejection conditions remain explicit |
| A level-design | N/A | No map/routes/objectives/placements changed |
| A game-ai | N/A | No autonomous AI authorized |
| A game-ui-ux | PASS for tested scope | Event-driven HUD unchanged; actual720p/1080p captures and existing keyboard/focus tests; no complete movement/threat UI claim |
| A game-feel | PASS engineering, HUMAN_PENDING | Same-event impact,83.333ms decoded hold, return-ready, Reduced Motion; all source/sequence art failures remain open |
| B Grid-Tactics separation | PASS criterion | Existing pure rules/view separation unchanged, no borrowed code/assets |
| B HopeMetal attribution | N/A | No borrowed pattern/code/art in this segment |
| B new engine/dependency | PASS | Existing Owner-approved Godot4.7.2/GDScript/GUT/Pillow only; nothing installed |
| C full3–5minute battle | N/A, explicit scope exception | Single-attack frame-regeneration segment, no full-battle claim |
| C understandable enemies | N/A, explicit scope exception | Three existing fixtures, no autonomous turn |
| C win/lose | N/A, explicit scope exception | No complete battle system authorized |
| C two tactical choices | N/A, explicit scope exception | Demonstration fixtures are not a tactical choice loop |
| C restart/change strategy | PASS replay, N/A strategy | Real repeated R/fixture-switch input; no strategy loop claim |
| C no duplicate/stuck/invalid resolution | PASS tested paths |55 tests,12 timed rendered runs and complete movie return to input-ready |
| C720p/1080p/basic keyboard | PASS automated |26 actual native screenshots, capture dispatches keyboard events, retained focus/input tests; no manual playtest claim |
| C automation versus human | PASS | Engineering/data checks, model art failures and HUMAN_PENDING stated independently |
| D SRD/rules | N/A new content, PASS scope | No new rules/WotC/SRD content or G005 change |
| D authorization/write boundary | PASS scope | Only shared-anim/ and godot-spike/ changed after438e801; no ui-prototype/story/decisions/other worktree; commit-only |
| D exact painted mace geometry | FAIL, explained |04 generated head about19px high; fixed contact03/manifest unchanged; geometry failure retained in audit, not waived by tests |

No unexplained C/D failure. Explained geometry failure means this is not ready
for art acceptance. Root PLAN/memory/shared files are outside this narrow
authorization; this handoff and VERIFICATION record the milestone. No new
agent was spawned. Normal hooks ran with report-only missing_canonical_memory;
no hook bypass, global trust edit or SessionEnd/canonical-closeout claim.

| Step | Commit |
| --- | --- |
| W1 proof/method | `4559e5d` |
| W2 complete frames/A5 baseline | `fa6fad8` |
| W3 region/real-playback audit | `785c2b8` |
| W4 sync/import/55 tests | `771c3d3` |
| W5 verification/screenshots/movie | `a581bc2` |
| W6 handoff | This commit |

**STOP after this W6 commit and wait for review. No push, main merge, PR,
stash, Actions, deployment or PhaseB. Task DONE is not SessionEnd.**

Final W6 check after writing this actual section and table:
`GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a6_contract.gd -gexit`
passed **7/7 tests, 636 assertions, exit 0**. The handoff is normalized to LF
so the heading/table check executes against the actual section, rather than
being skipped by a CRLF heading mismatch.
[Final log](evidence/spike02-a6/handoff-table-check.log).

## spike-02 A7

**W1–W6 evidence segment handed off; art FAIL, five motion PLACEHOLDER.** The
two-anchor appearance spec now exists, each frame was edited sequentially and
04's mace head is corrected downward19px. The attempted local transfers still
have visible face/stole seams, residual or misregistered motifs and unstable
fringe/drape. They do not meet the requested seam-free continuous-character
standard. 04's cuff bridge regresses A6's seamless painting. **63/63 GUT tests,
4,883 assertions pass**, proving covered engine/data/provenance contracts,
not successful art. Human hit-feel remains **HUMAN_PENDING**; Owner art approval
is pending. This is a review handoff, not an art acceptance recommendation.

Gavin's2026-10-24 instruction authorized this sole session/worktree and A7 only,
starting clean at `645ede1` over A6 `e233171`, branch `codex/godot-spike`, only
`D:\campaign-forge\scratch\godot-spike`. **Commit only, no push.** Owner chose
Godot/P010 accepted; React and Phase B are **CANCELLED**. Thoma's short
one-handed flanged mace remains **APPROVED canon**. Decision records, gameplay,
HUD/rules, knights, battlefield/props and ui-prototype were not changed.

### Run and inspect

From this worktree, using the existing installed standard Godot4.7.2 console:

```powershell
$godotExe = 'C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
& $godotExe --headless --path godot-spike -s res://tools/sync_shared_anim.gd
& $godotExe --headless --path godot-spike --import
& $godotExe --path godot-spike --resolution 1280x720
```

Or open `godot-spike/project.godot` and press F5. Existing controls: Space arms
and confirms, R replays;1/2/3 open/unit-blocked/terrain-blocked, M toggles Reduced
Motion while idle, H/? help, F1 debug, Esc closes overlay/forecast before exit.
No gameplay control or timing change. Run tests with
`& $godotExe --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`.

### Spec, sources and editing method

[Appearance spec](../../shared-anim/thoma-appearance-spec.md) and
[machine JSON](../../shared-anim/thoma-appearance-spec.json) use **only**
immutable idle/01 and swing/05 appearance pixels. Every element has an annotated
[crop](evidence/spike02-a7/spec-crops.png)/[box](evidence/spike02-a7/spec-crops.json).
Skin/hair/cloth/weapon hex values are real pixel samples; branch/fringe counts
retain ±1 uncertainty. Where anchors disagree, idle is the appearance master:
recover has a roughly10px higher head and7px higher right sprig. Hidden embroidery
under the idle mace was not invented. Body joints beneath cloth are estimates.

[Pose targets](evidence/spike02-a7/pose-targets.png) include the full landmark
set and one C1 cubic head trajectory. These are design targets, not observed
success. Pivot[256,464] is the actor registration origin; shoes have separate
positions. Contact03 is[455,196]. Full hands/feet/joints still miss targets.

W2 order was **01 →02 →00 →03 →04**, with completion/provenance recorded before
starting each next frame. Every first attempt used built-in image_gen **EDIT**
of the current A6 target and two immutable appearance anchors, not an independent
regeneration request. All five1254px returns reframed/repainted the target;
**none of those raw generated pixels was adopted**. Runtime retained A6's
single bag, connected shoes and body structure, using unit-scale masked anchor
face/hair and sprig/fringe interior transfers. Those limited transfers fail
the complete appearance and seam checks. Fixed neighbours were comparison only,
never appearance sources. No API/CLI image fallback or other character generated.

[Every attempt/input/mask/intermediate](evidence/spike02-a7/attempts/),
[prompts/hashes/settings](../../shared-anim/a7-swing-prompts.json),
[SOURCES](../../shared-anim/SOURCES.md#spike-02-a7--constrained-edits-and-anchor-touch-ups),
[method/limits](evidence/spike02-a7/METHOD.md),
[operations error record](evidence/spike02-a7/W2-OPERATIONS.md).
Raw PNGs and earlier evidence were not overwritten. A6 live frames were copied
byte-for-byte to [baseline-a6](evidence/spike02-a7/baseline-a6/), with hashes;
no baseline path is in the manifest. Scripts are offline Python/Pillow plus
GDScript capture/test tools; the game remains GDScript only, no new addon.

### Frame acceptance table

The following13 checks are model observations and exact data checks, never
Owner approval. PASS for an immutable anchor means it remains the source
endpoint; transition defects belong to motion frames. **No PLACEHOLDER removed.**

| Frame | Status | face_hair | stole | embroidery | tassels | cuffs | hem | palette | seams | bag_count | feet | mace | landmarks | sequence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `thoma/idle/01.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | PASS | Immutable reference endpoint, not Owner art approval. |
| `thoma/swing/00.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | 1 PASS | PASS | PASS | FAIL | FAIL | Anchor interior details corrected; outer face, drape, fringe and local seams remain unacceptable; full art acceptance FAIL. |
| `thoma/swing/01.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | 1 PASS | PASS | PASS | FAIL | FAIL | Anchor interior details corrected; outer face, drape, fringe and local seams remain unacceptable; full art acceptance FAIL. |
| `thoma/swing/02.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | 1 PASS | PASS | PASS | FAIL | FAIL | Anchor interior details corrected; outer face, drape, fringe and local seams remain unacceptable; full art acceptance FAIL. |
| `thoma/swing/03.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | 1 PASS | PASS | PASS | FAIL | FAIL | Anchor interior details corrected; outer face, drape, fringe and local seams remain unacceptable; full art acceptance FAIL. |
| `thoma/swing/04.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | 1 PASS | PASS | PASS | FAIL | FAIL | Anchor interior details corrected; outer face, drape, fringe and local seams remain unacceptable; full art acceptance FAIL. |
| `thoma/swing/05.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | PASS | Immutable reference endpoint, not Owner art approval. |

Per-check failures are explained in [frame-audit.json](../../shared-anim/frame-audit.json)
and [spec-check JSON](evidence/spike02-a7/spec-check.json). Read the matching
[anchor/current crops](evidence/spike02-a7/spec-check.png),
[landmark delta table](evidence/spike02-a7/landmark-deltas.md),
[sequence strip](evidence/spike02-a7/sequence-strip.png),
[transparent512px sheet](evidence/spike02-a7/equal-scale-transparent-sheet.png),
[style check](../../shared-anim/thoma-weapon-style-check.png),
[native A6-vs-A7](evidence/spike02-a7/contact-sheet-a6-vs-a7.png) and separately
labelled [source-pixel A6-vs-A7](evidence/spike02-a7/asset-sheet-a6-vs-a7.png).

| Processing order | Local attempts / image_gen calls | Base selection and changes | Remaining reason |
| --- | --- | --- | --- |
| 01 | 1 /1 | A5 passed single frame but different hem/body from A6 neighbours; A6 adopted structure selected, raw candidate is the same source at higher resolution; anchor face and two sprig/fringe interiors transferred | Outer face/hair and fringe/panel edges still A6; texture joins visible |
| 02 | 1 /1 | A6 adopted selected over A5 broken cuffs/feet and rejected A6 attempt2 bulbous stole; same anchor interior transfers | Right donor misregistered, residual A6 sprig produces extra strokes; face/hem/sequence also fail |
| 00 | 1 /1 | A6 connected anatomy selected over A5 detached shoe; source sprigs placed on existing panel interiors, face features transferred | Panel width/fringe/outer face not fully corrected, local texture joins |
| 03 | 1 /1 | A6 selected over A5 sleeve seam; anchor interiors transferred, exact A6 contact weapon/grip untouched | Draped panels and hem/face continuity still fail; hand targets not all met |
| 04 | 2 /1 | A6 selected over A5 floating hem; anchor interiors; first weapon extraction omitted original weapon pixels and left duplicate, rejected; local second attempt moves complete connected hand/weapon19px | Corrected head height and single mace, but visible cuff bridge and costume joins; seam regression |

Every base considered has its path/hash/reason in provenance, including A6 raw
candidates and A5 source frames. Seeds/model/quality not exposed are labelled
`not exposed`; local04 correction is deterministic. Attempt2's inherited
normalization preview is the origin raw edit's preview, not an operation on
the local output. Runtime/raw hashes and actual masks are explicit.

### 04 head correction, timing and real playback

04 A6 centre[420.72,357.384] → A7[420.72,376.384], W1 target[421,376],
error**0.475px**. Original head/haft/collar/grip pixels are translated[0,19],
not rescaled; GUT checks opaque head pixels exactly. Contact03 stays[455,196].
The head correction passes geometry; its cloth join and full pose do not pass.

Manifest unchanged:512x512, pivot[256,464], contact index3, swing durations
**180/70/40/80/100/150ms**, unchanged camera/offsets/impact/scenarios, reduced
indices[0,3,5] hide smear. Both anchors remain byte-identical. Lower legs/boots
below y420 match A6 exactly; one bag in every pose. Sync parity is69 files.

| Resolution / mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.925297s | 0.928701s | 0.905224s |
| 720p Reduced Motion | 0.727183s | 0.722318s | 0.747849s |
| 1080p normal | 0.923951s | 0.907859s | 0.931091s |
| 1080p Reduced Motion | 0.729055s | 0.748579s | 0.725249s |

All12 no-readback attacks include hitstop and return input-ready below1.7s;
contact events share a process frame. [720p timing](evidence/spike02-a7/timing.json),
[1080p timing](evidence/spike02-a7/timing-1080p.json). Both rendered captures have
`CAPTURE_COMPLETE A7 movie=false runs=6 shots=13 pass=true`. Each required pose
is captured at both native resolutions; [verification](VERIFICATION.md#spike-02-a7)
links the screenshots and exact commands/exits.

[Complete native60FPS clip](evidence/spike02-a7/attack-60fps.avi):59 frames,
7,272,394 bytes, no subsampling/transcoding. Strike2 → input-ready57:
**0.916667s**; contact20–24 identical full RGB, **83.333ms** hold. W3 real720p
[playback](evidence/spike02-a7/playback-check.json),
[all59 frame crops](evidence/spike02-a7/playback-every-frame.png),
[pair proxies](evidence/spike02-a7/sequence-check.json),
[MOVIE limits](evidence/spike02-a7/MOVIE.md). Region RGB uses actual readbacks
under source-alpha masks; silhouette IoU is explicitly a source occupancy
proxy. Neither approves continuity, particularly at tiny native character size.

### Resource self-check

Against [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md):

| Section / resource | Result | Scope/evidence |
| --- | --- | --- |
| A prototype-fast | PASS for this isolated segment | One spec, bounded sequential edits, explicit keep/discard gates; five raw reframed outputs discarded, every failure retained |
| A level-design / game-ai | N/A | No terrain/routes/objective or AI change authorized; no full battle claim |
| A game-ui-ux | PASS for unchanged input/feedback contracts | Existing GUT suite plus rendered1/2/3/R/M input-driven runs at both sizes; HUD code untouched, no new usability approval |
| A game-feel | Engineering PASS; art FAIL; human pending | Contact hold/timing/input-ready tested and recorded; seam/drape/identity sequence still fails; HUMAN_PENDING is separate |
| B Grid-Tactics / 2DTacticalRPGDemo | N/A new borrowing | No external code/art borrowed; existing rule/view split unchanged, no fresh repo audit claimed |
| B no new engine/dependency | PASS | Existing Owner-approved Godot4.7.2/GDScript and vendored GUT; installed Python/Pillow offline tools, no new addon/install |
| C full3–5min battle, autonomous enemy, win/lose, two tactical outcomes, restart strategy | N/A for this expressly bounded appearance segment | Existing isolated hit-feel fixtures, not a complete tactical battle; React/PhaseB cancelled, no rule expansion authorized |
| C no interrupted/duplicate resolution | PASS covered paths |63 GUT tests plus12 actual timed attacks, one contact resolution, input ready; no complete-game claim |
| C1280x720/1920x1080 and keyboard | PASS automated fixture paths |26 actual screenshots; injected keys1/2/3/R/M; human keyboard usability not claimed |
| C automation vs human evidence | PASS separation | Test logs/captures are machine/model evidence, human hit-feel remains HUMAN_PENDING, Owner art approval pending |
| D SRD/IP/rule-adaptation | N/A new rules; source boundary PASS | Only existing original Thoma pixels/authorized AI edits; no WotC/commercial asset, SRD rule or attribution changed |
| D AGENTS/Owner scope | PASS authorization; art requirements FAIL | Only own worktree and allowed paths, original anchors/evidence preserved, no story/decision edits or push/PR/merge/deploy; failed seam/full-spec requirements explicitly open |

No unexplained C/D failure. The isolated-scope N/A entries are not claims that
the product meets the full playable battle bar. External skill/repo research
was not expanded for this small art edit; imagegen skill's built-in edit and
non-destructive provenance workflow was used.

### Open items and stop

- Five motion PLACEHOLDER remain: complete face/hair silhouette, stole fall,
  exact motif/fringe edges, cuff/hem consistency, seam-free transfer and
  full pose-target/sequence acceptance. 02 and04 have the concrete regressions
  listed above; art is FAIL, not commercial-ready.
- Human hit-feel playtest **HUMAN_PENDING**; Owner art decision pending. No
  further asset round, new rule, migration/PhaseB or slice is implicitly authorized.
- Built-in edits could not preserve exact framing; local anchor transfers did
  not solve seamlessness. This segment does not establish a successful final
  animation production pipeline. Review the source crops as well as playback.
- Python/Godot were run from identified absolute installed paths; no hardened
  child environment or global trust completion is claimed. Commit hooks ran
  normally with report-only memory advisory; task handoff is not SessionEnd.

| Step | Commit |
| --- | --- |
| W1 anchor spec / crops / pose targets | `b711b3f` |
| W2 sequential edit attempts / baseline / provenance | `34e1260` |
| W3 honest spec/landmark/playback checks | `40ced11` |
| W4 sync/import/63 GUT tests | `926e006` |
| W5 verification/screenshots/movie | `03031f0` |
| W6 handoff and actual final table check | This commit |

**Stop after this W6 commit and wait for review. No push, PR, merge, stash,
Actions or deployment.** Final targeted GUT check runs after this actual section
and table have been written; its result is recorded below. Heading normalized
to LF so the handoff assertion executes rather than silently skipping it.

Final W6 command (after actual table insertion):
`GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a7_contract.gd -gexit`
returned **exit0,8/8 tests,2,102 assertions**.
[Final handoff/table log](evidence/spike02-a7/handoff-table-check.log).
The full W4 suite remains63/63 tests,4,883 assertions. Evidence/code hashes and
allowed-path diff are checked before this final commit; no push follows.

## spike-02 A8

**Ready for review as an AI experiment; art FAIL,0/5 motion frames accepted.**
The brief-driven shared sheet makes five poses share more consistent painting
and avoids A7's face/stole collage patches. It still does not preserve exact
anchor identity, costume geometry or continuous stance. All five stay
PLACEHOLDER. Engineering is verified by71/71 GUT tests,5729 assertions, native
720p/1080p runs and a complete60FPS movie; those results do not approve art.
Human hit-feel remains **HUMAN_PENDING** and Owner art approval is pending.

Owner authorization:2026-10-24 15:09 Asia/Taipei, try AI once more for Thoma
00–04 using the commission brief. Worktree `D:\campaign-forge\scratch\godot-spike`,
branch `codex/godot-spike`, clean base `a1cba50` above `fdc796b`. No push.
Godot is the Owner-selected engine; React/Phase B cancelled. No decision/story
file edited; mace canon remains APPROVED, even though these renderings fail
the complete mace art check. The commission brief is unchanged and remains
needed as the human-artist fallback. No additional attempt/slice is authorized
by this handoff.

### Run / inspect

`GODOT` is the installed console executable:
`C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe`.
From this worktree:

```powershell
& $GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd
& $GODOT --headless --path godot-spike --import
& $GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
& $GODOT --path godot-spike --resolution 1280x720
```

Or import `godot-spike/project.godot` and F5 in Godot4.7.2 standard. Existing
controls:1/2/3 choose open/unit-blocked/terrain-blocked; R or Strike replays;
M toggles Reduced Motion. Existing keyboard/focus/debug overlay contracts
remain tested. The scene constructs runtime children; the editor canvas alone
is not the game. [Full verification](VERIFICATION.md#spike-02-a8).

### Method, choice and local fixes

W1 creates one2048×1024 transparent4+3 grid, each panel512×512. First idle01
and seventh recover05 are exact original anchor pixels; middle cells have
the commission guide overlays. In attempts2/3,22% flat A7 silhouettes add pose
only, without copying A7 face or costume details. Each of three built-in
image_gen EDIT calls paints all five middle poses TOGETHER in one sheet.

The tool exposes no separate mask argument: the mask is a supporting image
and prompt constraint. All three outputs repaint/reframe the anchor cells.
They resemble the anchors but are not byte-identical; those generated endpoint
panels are never installed. Runtime idle01/recover05 remain originals.

- [Inputs, layout, mask, prompt and SHA-256](evidence/spike02-a8/inputs/)
- [All three immutable whole-sheet returns and per-attempt records](evidence/spike02-a8/sheet-attempts/)
- [Method and limitations](evidence/spike02-a8/METHOD.md)
- [Every prompt/input/raw/runtime/local-fix hash](../../shared-anim/a8-swing-prompts.json)

Attempt1 shares broad costume but puts02 too horizontally. Attempt2's pose
silhouette improves the weapon arc, but broadens/simplifies stole details and
has a less coherent02 grip. Attempt3 emphasizes anchor-scale narrow stole,
tiny sprigs, short fringe and short grey hair. It is selected for cross-panel
face/surface consistency first, pose readability second. All five adopted
bodies come from attempt3. **No per-frame generation or fallback edits used.**
This is a preference between failed candidates, not an accepted final style.

The whole return is uniformly mapped back to the recorded grid, sliced, then
each body is normalized by uniform scale/translation only. Head-to-ground361px,
ground464, pivot[256,464]; no rig/warp or independent face/costume transfer.
Generated alpha is preserved above24; detached islands<80px removed, hiddenRGB
zeroed, visibleRGB stays straight. Both boots remain attached.

All five mace positions missed after normalization. A local weapon-only fix
retains the painted hand/forearm/body, erases old exposed mace, redraws oak
haft/brass collar to target and rigidly rotates a masked original idle01 iron
head. Input/output/mask/donor hashes are preserved.01/04 first fixes left old
shaft slivers; pre-cleanup images remain archived and a second local mask
removes them. A missing-import cleanup error was corrected in a separate W2
commit before W3. Weapon contact locations pass; projection/painted joins still
fail art. There is no claim of seamless local repair or layered artist source.

### Frame-by-frame brief gate

Table values are exactly those in frame-audit.json.13 items must all PASS
plus the technical check before any motion frame can lose PLACEHOLDER. PASS
on the two original anchors identifies reference endpoints, not Owner approval.
`1 PASS` in bag_count means exactly one satchel plus its cloth roll.

| Frame | Status | face_hair | stole | embroidery | tassels | cuffs | hem | palette | seams | bag_count | feet | mace | landmarks | sequence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `thoma/idle/01.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | PASS | Immutable appearance endpoint; not Owner art approval. |
| `thoma/swing/00.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Shared sheet improves surface consistency; anchor identity, stole/motif/fringe, weapon integration and full pose/sequence still fail. |
| `thoma/swing/01.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Shared sheet improves surface consistency; anchor identity, stole/motif/fringe, weapon integration and full pose/sequence still fail. |
| `thoma/swing/02.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Shared sheet improves surface consistency; anchor identity, stole/motif/fringe, weapon integration and full pose/sequence still fail. |
| `thoma/swing/03.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Shared sheet improves surface consistency; anchor identity, stole/motif/fringe, weapon integration and full pose/sequence still fail. |
| `thoma/swing/04.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Shared sheet improves surface consistency; anchor identity, stole/motif/fringe, weapon integration and full pose/sequence still fail. |
| `thoma/swing/05.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | PASS | Immutable appearance endpoint; not Owner art approval. |

Failures common to00–04: face/hair is broader/softer than the anchor; stole
ends are wider/more symmetrical; two sprigs have changed scale/branch spacing;
fringe does not establish10/8 uneven tips±1; reconstructed weapon joins and
projection differ; observed hands/feet/elbows miss targets; anchor-to-action
stance and garment width still jump. Cuffs, continuous hem, muted material
families, one satchel/roll and connected grounded boots pass their individual
source checks. Full per-item one-line reasons are in the checklist JSON.

[Checklist/crops](evidence/spike02-a8/checklist.png) /
[13-item reasons and technical checks](evidence/spike02-a8/checklist.json) /
[all landmarks and adjacent deltas](evidence/spike02-a8/landmark-deltas.md) /
[transparent equal-scale sequence](evidence/spike02-a8/sequence-strip.png) /
[current style check](../../shared-anim/thoma-weapon-style-check.png) /
[A7 above A8 source comparison](evidence/spike02-a8/contact-sheet-a7-vs-a8.png) /
[real720p flicker check](evidence/spike02-a8/playback-check.json).

Landmark picks on visible features are±2px; cloth-hidden elbows/knees are
estimates±12px, not exact anatomical observations. No target value is substituted
to manufacture PASS. Full strict4px joint compliance fails. Region RGB deltas
are measured in actual decoded720p frames under transformed alpha masks;
silhouette IoU is source occupancy, not rendered segmentation. Proxies cannot
certify no flicker. All59 consecutive movie frames are inspectable in
[filmstrip](evidence/spike02-a8/playback-every-frame.png); the GIF is timing-
quantized and does not replace the60FPS AVI.

### Independent final mace-location check

Measured final-PNG alpha>0.9 centroids in37×37 head ROIs, including minor shaft
overlap; this is independent of the local fix's transformed-donor metadata.
All are within4px; contact03 pixel(455,196) is opaque. This passes placement,
while the complete mace art item remains FAIL.

| Frame | Measured | Brief target | Error px |
| --- | --- | --- | --- |
| 00 | (190.4115,85.2153) | (192,85) | 1.6030 |
| 01 | (258.7474,85.8856) | (259,87) | 1.1427 |
| 02 | (447.3775,111.5670) | (449,110) | 2.2557 |
| 03 | (454.5097,195.3932) | (455,196) | 0.7801 |
| 04 | (420.4930,374.4601) | (421,376) | 1.6212 |

[Final pixels/measurement method/hashes](evidence/spike02-a8/final-mace-centres.json).

### Timing and rendered evidence

Full manifest unchanged:512×512 canvas, pivot[256,464], contact index3,
anchor[455,196],180/70/40/80/100/150ms and80ms hitstop, Reduced Motion[0,3,5],
same offsets/events/knights/HUD/props/scenarios. A7's eight contracts run against
archived byte copies; eight new A8 tests cover the live swap. Full suite:
**71/71 tests,5729 assertions**, [log](evidence/spike02-a8/test-run.log).
All70 shared runtime files are byte-equal to source after sync.

| Resolution/mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.917871s | 0.916045s | 0.943971s |
| 720p Reduced Motion | 0.754644s | 0.745684s | 0.747847s |
| 1080p normal | 0.930527s | 0.944785s | 0.938591s |
| 1080p Reduced Motion | 0.780435s | 0.815044s | 0.768823s |

All12 return input-ready under1.7s, contact feedback shares a process frame,
hitstop wall91.069–107.246ms. Screenshot replays/readbacks excluded. The720p/
1080p capture processes overlapped; these are observed timings under that load,
not isolated performance benchmarks. Native AVI:59 frames at60FPS,7,273,022bytes,
no subsampling/transcoding; strike2→ready57 **0.916667s**; identical decodedRGB
on contact20–24 **83.333ms**,25 resumes. Encoding wall time is not gameplay
latency. Dummy audio is not a physical-device audition.

[AVI](evidence/spike02-a8/attack-60fps.avi) /
[movie notes/index](evidence/spike02-a8/MOVIE.md) /
[720p timing](evidence/spike02-a8/timing.json) /
[1080p timing](evidence/spike02-a8/timing-1080p.json).

| Pose |1280×720 |1920×1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a8/swing-anticipation.png) | [PNG](evidence/spike02-a8/swing-anticipation-1080p.png) |
| Smear | [PNG](evidence/spike02-a8/swing-smear.png) | [PNG](evidence/spike02-a8/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a8/contact.png) | [PNG](evidence/spike02-a8/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a8/follow-through.png) | [PNG](evidence/spike02-a8/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a8/idle.png) | [PNG](evidence/spike02-a8/idle-1080p.png) |

These are actual rendered native-resolution readbacks; both runs report
CAPTURE_COMPLETE A8 movie=false runs=6 shots=13 pass=true. Movie has its own
pass marker and is independently decoded/checked. The first movie writer run
had errors despite exit0/marker: it is excluded, retained and explained in
[verification](VERIFICATION.md#spike-02-a8), alongside all other real failures.

### A7 comparison / open items

Improved: one shared generation rather than independently invented frames;
the five middle surfaces share a more stable rendering treatment; removed
A7's face/stole texture-patch rectangles and04's cuff bridge. Kept original
anchor bytes, mechanical contracts and ground/contact locations.

Still fails: exact anchor face/hair, stole width/asymmetry, tiny sprigs/fringe,
all joint/foot targets, seam-free correctly projected weapon and stable full
sequence. Shared generation did not solve identity fidelity.00/01 weapon
projection is especially compressed;03 stance is substantially wider than
the brief;04 left foot lands on464 rather than the requested raised455.
This is not a successful final animation pipeline or commercial art approval.

Open: all five PLACEHOLDER frames, Owner art approval, human hit-feel playtest
HUMAN_PENDING and a human-artist production solution if the Owner proceeds.
The original commission brief remains valid and needed; no hand-painted or
layered source file was produced. No new AI attempt or commissioning action
is implied by these recommendations.

### Resource self-check

Checked every item in [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md).
Read pinned public
[game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md)
and [game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md)
methods this turn for verification; no code/art copied. Imagegen skill used
built-in EDIT, inspected inputs and archived actual raw returns. No other
project/worktree or company source was consulted.

| Checklist item | Result | Scope/evidence |
| --- | --- | --- |
| A prototype-fast | N/A new mechanics; scoped keep/discard check | Existing mechanic unchanged; keep attempt3 only as reviewable PLACEHOLDER, discard art-pass claim |
| A level-design | N/A | Battlefield, routes and placements unchanged; no new level or reachability claim |
| A game-ai | N/A | Fixed target/blocker spike, no new AI |
| A game-ui-ux | PASS for unchanged tested scope | Pinned method read; event-driven HUD unchanged, keyboard/focus/overlay GUT tests and native720p/1080p runs; no full move/threat UI claim |
| A game-feel | Engineering PASS; art FAIL; HUMAN_PENDING | Same-event contact, real hold/return-ready and Reduced Motion verified; no human weight/fun claim |
| B Grid-Tactics | N/A borrowing | No new architecture/code borrowed; simulation/view unchanged |
| B HopeMetal | N/A borrowing | No assets/code adopted; all generated art derives from original anchors |
| B new engine/dependency | PASS boundary | Existing Owner-approved Godot4.7.2/GUT/Pillow only; no new addon/install |
| C full3–5min battle alone | N/A scoped attack spike | A8 is five art frames; does not deliver a complete battle |
| C enemies react to player | N/A | Scripted defender in existing spike; no new enemy AI |
| C win/lose | N/A | Existing isolated attack, no new battle outcome system |
| C two tactical outcomes | N/A new tactical system | Existing open/unit/terrain-blocked setups exercised; no full tactical-choice claim |
| C restart/change strategy | PASS scoped replay | R and setup1/2/3 reinitialize existing sequence; GUT/capture runs |
| C no duplicate/stuck/invalid/interrupted resolution | PASS covered scope | Complete71-test suite; input lock/hold/contact/replay contracts and all12 input-ready captures |
| C two resolutions/basic keyboard | PASS | Native26 shots; parsed1/2/3/R/M capture input, keyboard/focus tests |
| C automated/human separated | PASS disclosure | Engineering PASS and model art FAIL; human HUMAN_PENDING, Owner approval pending |
| D SRD/CC-BY/WotC boundary | N/A rule change; PASS asset boundary | No rule changes or third-party character/art; original approved mace/anchors, sources retained; G005 untouched |
| D authorized scope/no main/story | PASS | Only shared-anim/,godot-spike/ plus pre-existing task brief; no ui-prototype/art-brief/story/decisions edits, no remote mutation |

No unexplained FAIL in C/D; their N/A items explicitly identify what this art
segment does not deliver. Independent Claude/GPT review is for the Owner to
route; no agent was spawned and model self-check is not review approval.

| Step | Local commit |
| --- | --- |
| W1 inputs and A7 archive | `6ab7061` |
| W2 shared sheet and local mace fixes | `2a355a0` |
| W2 cleanup correction | `c5f85fd` |
| W3 brief audit / actual flicker | `07e4bc5` |
| W4 swap-in /71 GUT tests | `aa29d60` |
| W5 verification / captures / movie | `dd14881` |
| W6 handoff / actual final table check | This commit |

**Stop after the W6 handoff commit. No push, merge, PR, stash, Actions,
deployment or further art generation.** Normal commit hooks run; report-only
missing_canonical_memory advisory is not bypassed. This is task DONE, not
SessionEnd. Explicit task scope excludes PLAN/memory/shared story-file writes.


Final W6 check after the actual section/table was inserted: GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_a8_contract.gd -gexit returned exit0,8/8 tests,843 assertions. See [handoff-table-check.log](evidence/spike02-a8/handoff-table-check.log). Full W4 remains71/71 tests,5729 assertions. No runtime asset or game code changed after capture/testing.


## spike-02 A9

**Delivery/evidence PASS; complete art gate FAIL,0/5.** The46 recorded local
operations improve four head identities and two uncompressed mace regions.
All five motion frames remain PLACEHOLDER because cloth details, integration,
full guide pose and temporal consistency still fail. The partial repairs do
not establish a successful final animation pipeline. HUMAN_PENDING for real
hit-feel; Owner art approval pending. The untouched commission brief remains
valid and needed for a human-artist fallback.

### Run / inspect

From this worktree root on codex/godot-spike, using the existing executable:

```powershell
$GODOT = 'C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
& $GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd
& $GODOT --headless --path godot-spike --import
& $GODOT --path godot-spike --resolution 1280x720
```

R replays;1/2/3 select open/unit-blocked/terrain-blocked;M toggles Reduced
Motion. Existing keyboard/HUD/controls unchanged. Run GUT with
`& $GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`.
Full final run:79/79,7948 assertions,
13 scripts, exit0, no warnings. A8's eight original tests now read its archived
PNG/audit; no old assertion removed. Eight A9 tests cover both fixed anchors,
mechanics, region/mask budget, regression flags, kept-pixel confinement and
actual evidence. [Commands/real failures](VERIFICATION.md#spike-02-a9).

### Method / provenance

A8 is the byte-archived base. [Measured defects/targets](evidence/spike02-a9/defects-and-targets.md),
[masks](evidence/spike02-a9/masks/), [all attempts](evidence/spike02-a9/attempts/),
[method](evidence/spike02-a9/METHOD.md), [fix log](evidence/spike02-a9/a9-fix-log.json),
[source records](../../shared-anim/SOURCES.md). No whole-frame/sheet generation
or independent face repaint. The expressly permitted Python/manual blend route
was used; **zero image_gen calls**. Kept donor pixels are transformed only by
recorded rigid translation/rotation at scale1. Every trial remains immutable;
each has actual changed-pixel and permission masks, input/output/donor SHA,
matrix, tool and kept/rejected reason. No region exceeds three attempts.

Order03,02,04,00,01. Head1 carved too much collar; head2 retains the collar
underpainting and copies the exact idle01 face/crown/beard onto03,02,04,00.
01 head2 leaves a fragment of the old head; head3's revised mask damages the
ivory collar, so all01 head trials are rejected. Its A8 head stays. Canon
recover05 mace2 uses a tighter source mask and an uncompressed rigid transform
on00/01, retaining the original painted gripping fingers. Projection/edge
integration remains an art FAIL even though compression and target position
improve. No weapon-design/canon status changed.

Stole/fringe patches from anchors produced gaps or abrupt cloth boundaries;
motif patches retained old larger leaves or weapon/teal crop contamination.
03 motif2 was initially kept, then explicitly withdrawn by operation3 during
adjacent-frame review.03 boot translations narrow the stance toward the brief;
04 translations move feet toward165,455 and334,464, but both open hem/leg
boundaries. All these regions return to exact A8 pixels. The regression gate
protects A8's PASS cuffs, hem, palette, one satchel/roll and attached grounded
boots. The remaining stance/foot defects are not waived.

W5's independent alpha scan found1 newly isolated opaque pixel on01 mace and2
on04's old-head edge. Tiny recorded region attempt3 erasures remove them;
original outputs/captures survive under [pre-alpha-cleanup](evidence/spike02-a9/pre-alpha-cleanup/).
Full GUT, native movie, flicker metrics and both resolution captures were rerun
after correction. [Alpha audit](evidence/spike02-a9/alpha-components.json) reports no NEW
tiny4-neighbour opaque clusters;02's A8 diagonal antialiasing pixels remain.
This is a measured regression proxy, not a universal halo detector.

[Integrity audit](evidence/spike02-a9/evidence-audit.json) independently replays the KEPT
regional operations to reconstruct every final RGBA byte, checks confinement
on all46 attempts, anchors/manifest,70 source-copy byte matches and actual
screenshots/movie. Final source snapshot: [hashes](evidence/spike02-a9/source-hashes.json).

### Exact frame gate / A8 to A9 comparison

All13 items must PASS plus technical checks before a motion frame can be
non-PLACEHOLDER. PASS endpoints below mean immutable reference frames, not
Owner art approval or a waiver of transition failures in the middle frames.

| Frame | Status | face_hair | stole | embroidery | tassels | cuffs | hem | palette | seams | bag_count | feet | mace | landmarks | sequence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `thoma/idle/01.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | PASS | Immutable appearance endpoint; not Owner art approval. |
| `thoma/swing/00.png` | PLACEHOLDER | PASS | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Partial anchor identity and/or uncompressed mace improvement; cloth details, integration and full pose/sequence still fail. |
| `thoma/swing/01.png` | PLACEHOLDER | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Partial anchor identity and/or uncompressed mace improvement; cloth details, integration and full pose/sequence still fail. |
| `thoma/swing/02.png` | PLACEHOLDER | PASS | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Partial anchor identity and/or uncompressed mace improvement; cloth details, integration and full pose/sequence still fail. |
| `thoma/swing/03.png` | PLACEHOLDER | PASS | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Partial anchor identity and/or uncompressed mace improvement; cloth details, integration and full pose/sequence still fail. |
| `thoma/swing/04.png` | PLACEHOLDER | PASS | FAIL | FAIL | FAIL | PASS | PASS | PASS | FAIL | 1 PASS | PASS | FAIL | FAIL | FAIL | Partial anchor identity and/or uncompressed mace improvement; cloth details, integration and full pose/sequence still fail. |
| `thoma/swing/05.png` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 1 PASS | PASS | PASS | PASS | PASS | Immutable appearance endpoint; not Owner art approval. |


Below are every item, its A8->A9 change and the reason. `improved` can still be
FAIL (mace integration); `same` can still be FAIL (retained A8 cloth/pose).
No formerly passing A8 item is downgraded.

| Frame | Item | A8 | A9 | Change | Reason |
| --- | --- | --- | --- | --- | --- |
| thoma/idle/01.png | face_hair | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | stole | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | embroidery | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | tassels | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | cuffs | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | hem | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | palette | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | seams | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | bag_count | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | feet | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | mace | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | landmarks | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/idle/01.png | sequence | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/00.png | face_hair | FAIL | PASS | improved | PASS: translated idle01 crown, brow, nose and squared beard retain the same donor identity; collar blending is judged separately under seams. |
| thoma/swing/00.png | stole | FAIL | FAIL | same | FAIL: A8 wide terminal panels retained because narrower anchor transplants opened garment gaps. |
| thoma/swing/00.png | embroidery | FAIL | FAIL | same | FAIL: A8 larger sprigs retained; anchor motif patches overlapped leaves or included weapon/teal edge contamination. |
| thoma/swing/00.png | tassels | FAIL | FAIL | same | FAIL: A8 regular fringe/cord retained; narrow donor fringe did not join the continuous hem; counts10/8 +/-1 not established. |
| thoma/swing/00.png | cuffs | PASS | PASS | same | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| thoma/swing/00.png | hem | PASS | PASS | same | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| thoma/swing/00.png | palette | PASS | PASS | same | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| thoma/swing/00.png | seams | FAIL | FAIL | same | FAIL: head/collar and/or mace-edge joins remain visible at native size; no complete seamless painted integration. |
| thoma/swing/00.png | bag_count | PASS | PASS | same | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| thoma/swing/00.png | feet | PASS | PASS | same | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| thoma/swing/00.png | mace | FAIL | FAIL | improved | FAIL: rigid recover05 head/haft transplant removes compression and meets target; grip/head edge highlights and projected-length integration still differ. |
| thoma/swing/00.png | landmarks | FAIL | FAIL | same | FAIL: A8 hands/elbows/knees and feet still exceed guide targets;03 narrowed-stance and04 foot trials rejected for hem/attachment regression. |
| thoma/swing/00.png | sequence | FAIL | FAIL | same | FAIL:01 retains A8 identity while other heads use anchors; broad cloth ends, stance and foot positions still jump across immutable endpoints. |
| thoma/swing/01.png | face_hair | FAIL | FAIL | same | FAIL: all three anchor-head trials produced old-face fragments or collar holes; A8 broad crown/softened beard retained. |
| thoma/swing/01.png | stole | FAIL | FAIL | same | FAIL: A8 wide terminal panels retained because narrower anchor transplants opened garment gaps. |
| thoma/swing/01.png | embroidery | FAIL | FAIL | same | FAIL: A8 larger sprigs retained; anchor motif patches overlapped leaves or included weapon/teal edge contamination. |
| thoma/swing/01.png | tassels | FAIL | FAIL | same | FAIL: A8 regular fringe/cord retained; narrow donor fringe did not join the continuous hem; counts10/8 +/-1 not established. |
| thoma/swing/01.png | cuffs | PASS | PASS | same | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| thoma/swing/01.png | hem | PASS | PASS | same | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| thoma/swing/01.png | palette | PASS | PASS | same | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| thoma/swing/01.png | seams | FAIL | FAIL | same | FAIL: head/collar and/or mace-edge joins remain visible at native size; no complete seamless painted integration. |
| thoma/swing/01.png | bag_count | PASS | PASS | same | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| thoma/swing/01.png | feet | PASS | PASS | same | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| thoma/swing/01.png | mace | FAIL | FAIL | improved | FAIL: rigid recover05 head/haft transplant removes compression and meets target; grip/head edge highlights and projected-length integration still differ. |
| thoma/swing/01.png | landmarks | FAIL | FAIL | same | FAIL: A8 hands/elbows/knees and feet still exceed guide targets;03 narrowed-stance and04 foot trials rejected for hem/attachment regression. |
| thoma/swing/01.png | sequence | FAIL | FAIL | same | FAIL:01 retains A8 identity while other heads use anchors; broad cloth ends, stance and foot positions still jump across immutable endpoints. |
| thoma/swing/03.png | face_hair | FAIL | PASS | improved | PASS: translated idle01 crown, brow, nose and squared beard retain the same donor identity; collar blending is judged separately under seams. |
| thoma/swing/03.png | stole | FAIL | FAIL | same | FAIL: A8 wide terminal panels retained because narrower anchor transplants opened garment gaps. |
| thoma/swing/03.png | embroidery | FAIL | FAIL | same | FAIL: A8 larger sprigs retained; anchor motif patches overlapped leaves or included weapon/teal edge contamination. |
| thoma/swing/03.png | tassels | FAIL | FAIL | same | FAIL: A8 regular fringe/cord retained; narrow donor fringe did not join the continuous hem; counts10/8 +/-1 not established. |
| thoma/swing/03.png | cuffs | PASS | PASS | same | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| thoma/swing/03.png | hem | PASS | PASS | same | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| thoma/swing/03.png | palette | PASS | PASS | same | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| thoma/swing/03.png | seams | FAIL | FAIL | same | FAIL: head/collar and/or mace-edge joins remain visible at native size; no complete seamless painted integration. |
| thoma/swing/03.png | bag_count | PASS | PASS | same | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| thoma/swing/03.png | feet | PASS | PASS | same | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| thoma/swing/03.png | mace | FAIL | FAIL | same | FAIL: A8 target/impact opacity pass, but reconstructed projected haft/head and brush joins still fail canon integration. |
| thoma/swing/03.png | landmarks | FAIL | FAIL | same | FAIL: A8 hands/elbows/knees and feet still exceed guide targets;03 narrowed-stance and04 foot trials rejected for hem/attachment regression. |
| thoma/swing/03.png | sequence | FAIL | FAIL | same | FAIL:01 retains A8 identity while other heads use anchors; broad cloth ends, stance and foot positions still jump across immutable endpoints. |
| thoma/swing/04.png | face_hair | FAIL | PASS | improved | PASS: translated idle01 crown, brow, nose and squared beard retain the same donor identity; collar blending is judged separately under seams. |
| thoma/swing/04.png | stole | FAIL | FAIL | same | FAIL: A8 wide terminal panels retained because narrower anchor transplants opened garment gaps. |
| thoma/swing/04.png | embroidery | FAIL | FAIL | same | FAIL: A8 larger sprigs retained; anchor motif patches overlapped leaves or included weapon/teal edge contamination. |
| thoma/swing/04.png | tassels | FAIL | FAIL | same | FAIL: A8 regular fringe/cord retained; narrow donor fringe did not join the continuous hem; counts10/8 +/-1 not established. |
| thoma/swing/04.png | cuffs | PASS | PASS | same | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| thoma/swing/04.png | hem | PASS | PASS | same | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| thoma/swing/04.png | palette | PASS | PASS | same | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| thoma/swing/04.png | seams | FAIL | FAIL | same | FAIL: head/collar and/or mace-edge joins remain visible at native size; no complete seamless painted integration. |
| thoma/swing/04.png | bag_count | PASS | PASS | same | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| thoma/swing/04.png | feet | PASS | PASS | same | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| thoma/swing/04.png | mace | FAIL | FAIL | same | FAIL: A8 target/impact opacity pass, but reconstructed projected haft/head and brush joins still fail canon integration. |
| thoma/swing/04.png | landmarks | FAIL | FAIL | same | FAIL: A8 hands/elbows/knees and feet still exceed guide targets;03 narrowed-stance and04 foot trials rejected for hem/attachment regression. |
| thoma/swing/04.png | sequence | FAIL | FAIL | same | FAIL:01 retains A8 identity while other heads use anchors; broad cloth ends, stance and foot positions still jump across immutable endpoints. |
| thoma/swing/05.png | face_hair | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | stole | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | embroidery | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | tassels | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | cuffs | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | hem | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | palette | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | seams | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | bag_count | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | feet | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | mace | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | landmarks | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/05.png | sequence | PASS | PASS | same | PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval. |
| thoma/swing/02.png | face_hair | FAIL | PASS | improved | PASS: translated idle01 crown, brow, nose and squared beard retain the same donor identity; collar blending is judged separately under seams. |
| thoma/swing/02.png | stole | FAIL | FAIL | same | FAIL: A8 wide terminal panels retained because narrower anchor transplants opened garment gaps. |
| thoma/swing/02.png | embroidery | FAIL | FAIL | same | FAIL: A8 larger sprigs retained; anchor motif patches overlapped leaves or included weapon/teal edge contamination. |
| thoma/swing/02.png | tassels | FAIL | FAIL | same | FAIL: A8 regular fringe/cord retained; narrow donor fringe did not join the continuous hem; counts10/8 +/-1 not established. |
| thoma/swing/02.png | cuffs | PASS | PASS | same | PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer. |
| thoma/swing/02.png | hem | PASS | PASS | same | PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments. |
| thoma/swing/02.png | palette | PASS | PASS | same | PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading. |
| thoma/swing/02.png | seams | FAIL | FAIL | same | FAIL: head/collar and/or mace-edge joins remain visible at native size; no complete seamless painted integration. |
| thoma/swing/02.png | bag_count | PASS | PASS | same | PASS: one brown flap satchel and one pale roll at screen-left hip in every panel. |
| thoma/swing/02.png | feet | PASS | PASS | same | PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465. |
| thoma/swing/02.png | mace | FAIL | FAIL | same | FAIL: A8 target/impact opacity pass, but reconstructed projected haft/head and brush joins still fail canon integration. |
| thoma/swing/02.png | landmarks | FAIL | FAIL | same | FAIL: A8 hands/elbows/knees and feet still exceed guide targets;03 narrowed-stance and04 foot trials rejected for hem/attachment regression. |
| thoma/swing/02.png | sequence | FAIL | FAIL | same | FAIL:01 retains A8 identity while other heads use anchors; broad cloth ends, stance and foot positions still jump across immutable endpoints. |


[13-item anchor crops](evidence/spike02-a9/checklist.png) /
[machine-readable checklist](evidence/spike02-a9/checklist.json) /
[measured landmark table](evidence/spike02-a9/landmark-deltas.md) /
[sequence strip](evidence/spike02-a9/sequence-strip.png) /
[style check](../../shared-anim/thoma-weapon-style-check.png) /
[A8 above A9, fixed anchors at both ends](evidence/spike02-a9/contact-sheet-a8-vs-a9.png).
These are source assets, not screenshots. Visible manual joint uncertainty
is+/-2px, hidden elbows/knees+/-12px. New head centres derive from anchor picks
and matrices; unchanged joints reuse exact A8 anatomy observations.01 headtop
retains original manual103px because its raised mace overlaps the head ROI.
No strict4px compliance is claimed for occluded anatomy.

### Mace / fixed mechanics

Final independent alpha>0.9 centroid in each37x37 head ROI (including a little
haft/antialiasing overlap); target placement is separate from design/brush PASS.

| Frame | Final opaque-ROI centroid | Brief target | Error px |
| --- | --- | --- | --- |
| 00 | [191.292, 85.33] | [192, 85] | 0.7808 |
| 01 | [259.084, 86.639] | [259, 87] | 0.3709 |
| 02 | [447.378, 111.567] | [449, 110] | 2.2557 |
| 03 | [454.51, 195.393] | [455, 196] | 0.7801 |
| 04 | [420.493, 374.46] | [421, 376] | 1.6212 |

03 pixel455,196 remains opaque. All five RGBA/transparent canvases512x512,
pivot256,464, at least one grounded foot464, opaque bottom463-465. Head-to-ground
height approximately360px; fixed original endpoints retain their known height
difference. Full manifest, events, offsets, contact frame3 and anchor455,196
unchanged;180/70/40/80/100/150ms,80ms hitstop, Reduced Motion00/03/05 unchanged.
idle01 and swing05 keep exact original SHA-256. No archived PNG in manifest.

### Actual playback / measured timing

[Actual seven-pose native720p crops](evidence/spike02-a9/playback-keyframes.png) /
[every decoded frame](evidence/spike02-a9/playback-every-frame.png) /
[region metrics](evidence/spike02-a9/playback-check.json). Region mean-colour deltas come
from rendered movie pixels through W1 masks/source alpha transformed into
viewport space. Source silhouette IoU and anatomical height deltas are
separately labelled proxies, not segmentation of rendered RGB or proof of
no flicker. The mixed01 identity and retained wide cloth/stance still jump.

| Resolution / mode | Open | Unit blocked | Terrain blocked |
| --- | --- | --- | --- |
| 720p normal | 0.909355s | 0.929085s | 0.946548s |
| 720p Reduced Motion | 0.749362s | 0.680090s | 0.717853s |
| 1080p normal | 0.919576s | 0.919482s | 0.918028s |
| 1080p Reduced Motion | 0.717850s | 0.735911s | 0.717906s |

All12 no-readback runs return input-ready under1.7s, with same-frame feedback
and at least80ms measured hitstop.720p/1080p real-time captures ran sequentially.
Movie:59 frames,60FPS,7,273,008 bytes, strike2
to ready57=0.916667s,
identical RGB held20-24
(83.333ms), then resumes. No subsampling/transcoding.
Encoding wall time is not attack latency; Dummy audio is not hardware audition.

[60FPS AVI](evidence/spike02-a9/attack-60fps.avi) / [movie notes](evidence/spike02-a9/MOVIE.md) /
[index](evidence/spike02-a9/movie-index.json) / [720p timing](evidence/spike02-a9/timing.json) /
[1080p timing](evidence/spike02-a9/timing-1080p.json).
Every rendered run printed CAPTURE_COMPLETE pass=true and passed native-size /
pose/hold gates.13 captures per resolution include extra raise/recover and A8
comparisons; the requested five are linked here:

| Pose | Native1280x720 | Native1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG](evidence/spike02-a9/swing-anticipation.png) | [PNG](evidence/spike02-a9/swing-anticipation-1080p.png) |
| Swing/smear | [PNG](evidence/spike02-a9/swing-smear.png) | [PNG](evidence/spike02-a9/swing-smear-1080p.png) |
| Contact during hitstop | [PNG](evidence/spike02-a9/contact.png) | [PNG](evidence/spike02-a9/contact-1080p.png) |
| Follow-through | [PNG](evidence/spike02-a9/follow-through.png) | [PNG](evidence/spike02-a9/follow-through-1080p.png) |
| Idle | [PNG](evidence/spike02-a9/idle.png) | [PNG](evidence/spike02-a9/idle-1080p.png) |

### What improved / remains open

The four copied faces look like the anchors rather than A8's softened generic
face;00/01 preserve more of the canon weapon's original head/haft proportions.
Only small recorded regions change; the rest of A8 is preserved exactly.
The method still cannot integrate narrow stole/fringe or repair foot positions
without damaging already passing shapes.01 identity, all costume details,
seams, complete pose and temporal consistency still fail. This is a partial
local improvement, not final animation acceptance or a proven production path.

Open: all five PLACEHOLDER motion frames, HUMAN_PENDING hit-feel playtest,
Owner art approval and an artist solution if Gavin proceeds. The [commission
brief](../../docs/art-briefs/thoma-swing-commission.md) remains valid/needed;
no layered artist source was produced. No new art round or commissioning
action is implied. No story, rules, timing/HUD, knight, environment, G005,
ui-prototype/, docs/art-briefs/, immutable anchor/raw-candidate PNG or previous A2-A8 evidence changed.

### Resource self-check

Every [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md) item is
accounted for below. The existing A8 handoff's pinned game-feel/game-ui-ux
references are local historical context; external SKILL files were not re-read
or installed this turn. This table asserts the listed acceptance evidence,
not new skill certification, third-party borrowing or human review.

| Checklist item | Result | Scope/evidence |
| --- | --- | --- |
| A prototype-fast | PASS scoped keep/discard discipline | No new mechanic; explicitly bounded region experiments and regression rejection,46 records |
| A level-design | N/A | No terrain/routes/objectives/placement changes or new reachability claim |
| A game-ai | N/A | Existing scripted defender; no new AI |
| A game-ui-ux | PASS tested unchanged scope | Existing keyboard/input/focus/HUD tests retained; native720p/1080p captures, no new move/threat UI claim |
| A game-feel | Engineering PASS; art FAIL; HUMAN_PENDING | Same-frame contact, >=80ms hold, <=1.7s return and Reduced Motion tested; actual movie, no human fun/weight claim |
| B Grid-Tactics | N/A borrowing | No new architecture/code adopted; simulation/view unchanged |
| B HopeMetal | N/A borrowing | No code/assets borrowed; existing original anchors only |
| B no new engine/dependency | PASS boundary | Existing approved Godot4.7.2/GUT/Pillow; no install/addon |
| C full3-5min battle alone | N/A scoped art/attack spike | This task repairs five animation frames, does not deliver a battle |
| C enemies react to player | N/A | Scripted defender; no new AI |
| C win/lose | N/A | No battle outcome system added |
| C two tactical outcomes | N/A new tactical system | Existing open/unit/terrain-blocked setups tested; no full tactical-choice claim |
| C restart/change strategy | PASS scoped replay | R /1/2/3 reinitialize; timing/capture runs and existing tests |
| C no duplicate/stuck/invalid/interrupted resolution | PASS covered scope | Full79-test suite, final12 ready captures; no complete-battle coverage claim |
| C both resolutions/basic keyboard | PASS |26 native captures and parsed R/1/2/3/M plus existing keyboard/focus tests |
| C automated/human separated | PASS disclosure | Engineering results, model art FAIL and HUMAN_PENDING recorded independently |
| D SRD/CC-BY/WotC boundary | N/A rules; PASS art boundary | No rule changes or new third-party IP; approved original mace/anchors only; G005 untouched |
| D scope/no main/story | PASS | Only allowed paths and existing brief diff; local commits only, no remote operation |

No unexplained FAIL in C/D: N/A entries state the deliberately scoped boundary.
Independent Claude/GPT review is Owner-routed; no sub-agent was spawned and
model self-check is not review approval. No cross-worktree/global trust edits.
Normal Git hooks ran; missing_canonical_memory is a report-only advisory,
not a bypass. This handoff is task DONE, not SessionEnd; explicit segment scope
excludes PLAN/memory/shared narrative updates.

| Step | Local commit |
| --- | --- |
| W1 masks / A8 archive |8b30434|
| W2 bounded transplants / regression records |11adc34|
| W3 full source / rendered audit |1555c74|
| W4 A8 history /79 GUT tests |b5e2f0d|
| W5 final alpha / native verification |6b2ee3d|
| W6 handoff / final table check |This commit|

**Stop after this W6 handoff commit. No push, merge, PR, stash, Actions,
deployment, new slice or further art attempt. Wait for Owner review.**

W6 final validation: A9 contract against the actual inserted handoff/table returned exit0,8/8 tests,2219 assertions, no warnings (handoff-table-check.log). Final independent package audit returned0:46 bounded operations,70 byte-equal shared files,26 native captures,59 movie frames; no PNG changed after W5 capture. Metadata-only correction binds frame-audit source/raw_sha256 to its archived A8 base and names the operation log separately; w6-sync.log and final contract/package checks verify that correction. Source snapshot refreshed after this final narrative addition.

## spike-03

**打擊回饋已實作並完成工程驗證；大地圖只有提案與獨立 mockup。**
人類打擊感試玩 **HUMAN_PENDING**，大地圖選案 **OWNER_PENDING**。這不代表
Gavin 已認可重量感、最終動畫、聲音、美術或正式關卡。

Owner Gavin Wu 於 2026-10-24 18:27 授權「A9 先暫用，接著做大地圖提案和
打擊感」；本輪依 [spike-03 brief](../../docs/tasks/godot-spike-03-hitfeel-bigmap.md)
在 `D:\campaign-forge\scratch\godot-spike`、`codex/godot-spike` 從乾淨 `20d9844`
（A9 `b2f460b` 上）依序完成 W1–W7。本段補充前面的歷史交接；Owner 已在
指定的 P010 決策分支選擇 Godot，React／Phase B 取消，不再提出 web 遷移工作。
未更改本分支的舊決策紀錄、正式劇情、G005、S3／S4 或任何共用 PLAN／memory。

### 如何執行與調參

從工作區根目錄執行；Godot 4.7.2 standard，遊戲程式全為 GDScript：

```powershell
$godotSpikeExe = 'C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
& $godotSpikeExe --headless --path godot-spike --import
& $godotSpikeExe --path godot-spike --resolution 1280x720
# A9 impact baseline（同一組原封不動的 A9 動作圖）：
& $godotSpikeExe --path godot-spike --resolution 1280x720 -- --impact-profile=a9_baseline
# 第一擊展示暴擊，傷害仍是 2：
& $godotSpikeExe --path godot-spike --resolution 1280x720 -- --crit
# 獨立大地圖 mockup；沒有從遊戲主場景導向它：
& $godotSpikeExe --path godot-spike res://scenes/mockups/BigMapMockup.tscn
```

也可開 `godot-spike/project.godot`，F5 玩原本 Skirmish；mockup 請另開場景 F6。
R 重播；1／2／3 選開放／友軍阻擋／地形阻擋；空白鍵準備／確認；M 切換
Reduced Motion；C 切換「下一擊展示暴擊」，出手後自動消耗，忙碌時不能切換。
F1 可看 C 狀態與原有除錯提示；H／? 說明、Tab 焦點、Esc 收起／取消／離開。
主 HUD 佈局未改。`--crit` 與 C 都只改 presentation，沒有正式暴擊規則。

調參入口是 [impact_profile.tres](../config/impact_profile.tres)，Inspector 可看到
[ImpactProfile](../scripts/impact/impact_profile.gd) 的分組、範圍與說明；未覆寫欄位
沿用 Resource 的 A9 預設值。[baseline](../config/impact_profile_a9_baseline.tres)
用於前後對照。`manifest.impact` 保留為 A9 歷史紀錄，不是新的 live tuning。
材質持續使用 `flash` uniform；所有 layer 時間、強度、數量、顏色、音量與 hook
名稱由 profile 供應。沒有新增 addon、安裝工具或外部素材。

### 打擊層：A9 → spike-03（設定值）

| 層 | A9 baseline | spike-03 normal／crit | Reduced Motion |
| --- | --- | --- | --- |
| Hitstop | 80 ms | 攻擊者／目標各110 ms，crit ×1.54545 ≈170 ms；整個 pausable world 取最大值，保留真實時間＋process 時間下限 | 80 ms |
| Shake | 3.4 px，首下 (3.4,−1.7)，非定向，200 ms、power decay2 | 沿 attacker→target 首下8／12 Camera2D offset units，200 ms、3 次震盪、exponential decay4，歸零 | 無 |
| Flash | 白 mix0.65，停頓後35 ms fade | 暖白 mix1.0，停頓期間保持，額外16.7 ms 後80／96 ms fade | 無，維持原抑制契約 |
| 接觸後仰 | 接觸幀無位移 | 目標 sprite 視覺 pivot 即時9 px，120 ms cubic-out 回位；不動邏輯格／actor | 無 |
| 火花／短 streak | 7 條1.2 px spokes +24 CPU sparks | 11 條2 px spokes +22 px 方向 streak +36 sparks；crit 約17 條／54 sparks | 無 |
| Ground dust | 只有受阻回彈 | 每次接觸18／27 dust particles＋即時低透明足底 puff；blocked recoil 仍有揚塵 | 無 |
| 數字 | 18 px，scale1，黑底，30 px rise／380 ms | 28／34 px，scale1.6／1.8 → overshoot →1，120 ms；brass／clay。移到目標上方112 px，tuned 無黑底 | 數字可 scale，無上浮 |
| Zoom punch | 無；原 attack zoom1.4 | 額外 +0.06，停頓後100 ms 回到 attack zoom | 無 attack zoom／punch |
| 擊退／受阻／settle | 220 ms；6 px／60+160 ms；180 ms | 全部維持 A9，仍只擊退規則決定的一格 | open knockback30 ms，原受阻時序維持 |
| SFX | 單一 impact，−7 dB | whoosh −14、impact −7／crit −6、thud −12 dB | whoosh 改 frame00，impact 仍 frame03 |

上述 px 為 1280×720 參考畫布／Camera2D 世界單位，實際 attack zoom 會放大可見
位移。新回饋保留同一個 frame03／anchor(455,196)，九個 layer 的觸發紀錄同幀；
原有 spark／sfx／flash 三事件契約也維持。recoil 是獨立 visual_offset，不會被
換圖覆蓋，也不和規則 knockback 搶同一個位置 tween。

保留 whole-world SceneTree pause：人物 frame clocks、camera、數字、粒子與
tweens 凍結，root／HUD 仍 always-process，F1 等可操作。這次沒有改成個別 actor
freeze，也沒有用全域 time_scale。profile 可分別填攻擊者／目標 minimum，但
在此模型中兩者與世界會一起等到較長值。UI 自動操作與原有 pause regression
繼續驗證這個契約。

### 實機證據、時序與測試

- [證據總覽](evidence/spike03/README.md)、[驗證命令與真實退出碼](VERIFICATION.md#spike-03)、
  [GAPS](evidence/spike03/GAPS.md)、[audit](evidence/spike03/audit.json)、
  [source hashes](evidence/spike03/source-hashes.json)。
- [相同版型 before／after strip](evidence/spike03/impact-strip-before-vs-after.png)、
  [crit strip](evidence/spike03/after-crit/impact-strip.png)、
  [before／after GIF](evidence/spike03/before-vs-after.gif)（約5.02 MiB，contact 對齊、30 FPS native crops）。
- [A9 baseline AVI](evidence/spike03/before/attack-60fps.avi)、
  [normal AVI](evidence/spike03/after/attack-60fps.avi)、
  [crit AVI](evidence/spike03/after-crit/attack-60fps.avi) 都是720p／60 FPS 原始輸出，
  [MOVIE](evidence/spike03/MOVIE.md) 交代 crop、編碼與時鐘定義。
- [接觸](evidence/spike03/contact.png)、[暴擊接觸](evidence/spike03/contact-crit.png)、
  [數字 pop](evidence/spike03/number-pop.png)、[原生1080p](evidence/spike03/contact-1080.png)。
  三組最終錄影共146張 native PNG，涵蓋接觸−8至恢復輸入，含要求的−6。

| 模式 | Open／unit-blocked／terrain-blocked，固定60FPS秒數 | 無 readback 的實測 wall 秒數 |
| --- | --- | --- |
| Normal | .950000／.950000／.950000 | .928577／.918207／.920291 |
| Crit presentation | 1.016667／1.016667／1.016667 | .987982／.983269／.975860 |
| Reduced Motion | .716667／.716667／.716667 | .683442／.676853／.681805 |

全部低於硬上限1.7秒，normal／crit 也低於1.2秒目標，Reduced Motion 更短。
A9 baseline 是.916667秒；原片／normal／crit 分別5／7／11個完全凍結的接觸畫面。
不要拿取圖／編碼 wall 時間當操作延遲；九次主要 timing run 都沒有 readback。
第一張1080圖的同步存檔拖慢了量測，已改到 ready 後寫檔並重跑，原紀錄保留。

完整 GUT **89／89，15 scripts，8958 assertions，exit0**；原79項全部保留，
加9項 impact 行為測試與1項 mockup smoke。包括 profile 每欄範圍與A9基準、
同幀 layer、normal／crit minimum、方向／衰減、Reduced Motion 全程零鏡頭與
recoil、flash歸零、數字歸一並刪除、粒子清除、SFX次數／frame、budget與三配置
相同規則結果。W6曾抓到新 debug hint 取代原文的回歸，已保留原文並重跑89項；
沒有修改舊測試來遷就它。日誌另保留 type／工具錯誤與修正，不把失敗當成功。

稽核確認70個 shared runtime 檔與 A9／shared source byte parity，規則不變。
傷害依然2，命中後4HP；三配置目標格為(1,6)、(1,5)、(3,4)。擊退格數、HP、
walkability、11×9與G005都未改。CPU emitter 不提供精確 live particle count，
timeline 如實標 capacity upper bound；凍結／清除另有測試。

### PLACEHOLDER 與真人待驗

全部新增音效是原創 deterministic **PLACEHOLDER**，沒有外部 sample：

| Hook | 長度／用途 |
| --- | --- |
| `swing_whoosh` | 180 ms，normal frame1；Reduced Motion frame0 |
| `impact` | 240 ms，A9 原本 hit PCM，frame3 |
| `impact_crit` | 280 ms，較低頻的展示暴擊，frame3 |
| `knockback_thud` | 280 ms，open knockback 落點 |
| `blocked_thud` | 280 ms，受阻後回彈開始 |

詳 [audio/SOURCES](../audio/SOURCES.md)。Dummy driver 的事件與PCM測試不代表
喇叭試聽或混音通過。VFX 是可調的開發表現，也不是最後美術。

A9 原有動作圖00–04的 **PLACEHOLDER**、所有 `frame-audit.json` 旗標、idle／05
固定 anchor、knight 圖及全部 shared-anim 原樣保留；未重畫、生成或修改 frame PNG。
180／70／40／80／100／150ms、contact3、anchor455,196 也未變。短單手 flanged
mace 的 **APPROVED canon** 不變。[人類委託 brief](../../docs/art-briefs/thoma-swing-commission.md)
仍是動作美術 fallback，這輪沒有發包或聲稱動畫終稿通過。

**HUMAN_PENDING**：Gavin 實際試一般／暴擊／Reduced Motion，判斷停頓、閃白、
震動與音量是否舒服，數字是否擋資訊；模型看圖與自動測試無法代替這個判斷。
本輪工程結果不能推出完整戰鬥好玩或商業美術品質。沒有正式crit、完整戰鬥、
敵方AI、正式存檔或網路功能。

### 大地圖提案與 mockup 交接

[繁中提案](../../docs/proposals/big-map-proposal.md) 比較 A菱形128／24×18、
B方格80／32×24、**C菱形160×94.5／32×24（推薦、未定案）**。C人物參考高96px，
延用投影與原創暗黑奇幻手繪方向；實際代價是每屏格數變少，必須補捲動、
離屏提示與地景分塊。L03建議保留11×9教學，絞盤(2,1)、渡口與後果不重建。
成本與回合節奏只是估算；不授權照這份建議自動遷移關卡或正式規則。

獨立 mockup 是32×24／768格、12個重複idle站位，terrain是既有繪畫小塊與
程式 placeholder。不在 main scene 引用鏈，不讀 rules／真實HUD，不是L03。
WASD／方向鍵、中鍵、edge、wheel、O、F／Home可操作；1／2／3比較格寬。
小地圖只顯示，不能點擊。實際 camera input checks全真，bounds smoke通過。

- [全圖](../../docs/proposals/big-map/overview.png)、
  [西](../../docs/proposals/big-map/scroll-west.png)／
  [渡口](../../docs/proposals/big-map/scroll-crossing.png)／
  [東](../../docs/proposals/big-map/scroll-east.png)。
- [格寬128](../../docs/proposals/big-map/tile-128.png)／
  [160](../../docs/proposals/big-map/tile-160.png)／
  [192](../../docs/proposals/big-map/tile-192.png)：原生720p，不是編輯器合成圖。
- [操作／限制](../../docs/proposals/big-map/README.md)、
  [camera data](../../docs/proposals/big-map/capture.json)。

高物件遮擋、正式威脅／AI／fog、鏡頭跟隨／事件／攻擊後回原捲動位置、
TileMapLayer／painted-chunk管線與正式大戰效能都未實作／驗收。overview人物很小
是全圖閱讀模式；建議操作尺度在局部圖。現有灰盒重複地景不是新的商業美術。

交給 Gavin 的問題（完整代價在提案，每題可一行答）：

1. A菱形128／B方格80／C菱形160，選哪個？
2. 標準圖先24×18還是32×24？
3. 人物高先約76／96／114px哪一級？
4. L03保留11×9教學，另做大圖灰盒是否可行？
5. 第一版全圖可見、無fog是否可行？
6. WASD＋中鍵，還是edge為主？
7. 一張標準戰鬥15–20／20–35／35分鐘以上？
8. 是否先用hybrid地景、少量tiles／painted chunks驗證？

這是待 Owner 決策清單；不在本輪追問、不代填決策、不啟動下一個任務。

### RESOURCE-CHECKLIST self-check

逐項對照 [RESOURCE-CHECKLIST](../../docs/review/RESOURCE-CHECKLIST.md)。
game-feel／game-ui-ux於W1基準擷取期間唯讀讀取；prototype-fast於W3證據期間、
level-design於W4提案期間讀取。均為原清單 repo 的 pinned
`0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd` 方法，提案/GAPS有連結；相關feedback／
layout references也已讀，沒有安裝或複製其程式。官方Godot API只供核對，無商業
素材或reference-repo code採用。未派生新模型代理；此自查不是Claude／GPT審查。

| Item | Result | 證據／本輪適用範圍 |
| --- | --- | --- |
| A prototype-fast | PASS scoped | 問題、keep/discard與throwaway界線在GAPS／提案；mockup不接主遊戲，沒有順帶做完整大圖系統 |
| A level-design | PASS proposal／N/A實作關卡 | 提案列路線距離、增援預告、成本與目標節奏；mockup沒有可達／勝路宣稱，既有規則不變 |
| A game-ai | N/A | 無AI實作，提案只列成本與未來行為假設 |
| A game-ui-ux | PASS tested scope | 原HUD／焦點／Space契約保留，C提示同步；原生720p/1080p、parsed keyboard與mockup鍵鼠／edge實測 |
| A game-feel | Engineering PASS／HUMAN_PENDING | 同幀回饋、5/7/11幀真實freeze、九配置budget、歸零／cleanup與Reduced Motion測試；不宣稱真人重量感通過 |
| B Grid-Tactics | PASS architecture criterion／N/A borrowing | 規則純函式輸出events，presentation播放；rule hash不變，未借程式或素材 |
| B HopeMetal | N/A borrowing | 無新採用pattern／code／asset |
| B no new engine/dependency | PASS | 既有且Owner已選Godot4.7.2／GUT，Pillow既有，無新增addon或安裝 |
| C full3–5min battle alone | N/A explicit spike scope | 單擊工程與鏡頭mockup，沒有完整戰鬥交付宣稱 |
| C enemies react to player | N/A | 固定防守者；無AI新功能 |
| C win/lose | N/A | 無戰役勝負系統 |
| C two tactical outcomes | N/A new tactical choice | 三配置保留不同擊退結果，但未宣稱完整戰術選擇系統 |
| C restart/change strategy | PASS scoped replay | R／1/2/3重設；三配置多次回放，不擴張成完整strategy驗收 |
| C no duplicate/stuck/invalid/interrupted | PASS covered scope | 原有spam／lock／pause測試保留，完整89/89與九次ready，規則結果一致 |
| C both resolutions/basic keyboard | PASS | 720p逐幀、原生1080p parsed-R截圖；mockup按brief只驗720p，7個input checks全真 |
| C automated/human separated | PASS | 工程測試、模型看圖、HUMAN_PENDING／OWNER_PENDING分開記錄 |
| D SRD/CC-BY/WotC boundary | N/A rules／PASS assets | 規則／G005原樣，無新SRD改寫、商業素材或WotC IP；原創音效明標PLACEHOLDER |
| D scope/no main/story | PASS | scope audit限定Godot／proposals／既有brief；frame PNG、shared-anim、React、art briefs、故事與shared files零變更；正常本地commit，無push/merge/PR/stash |

C／D沒有未解釋FAIL；N/A是本輪明確授權界線，不是完整可玩驗收。
正式大圖、正式AI／規則、完整動畫與真人美術判斷都不能由這個自查推導通過。

### Choices、驗證狀態與停止點

遇到可選作法採最保守界線並記錄：保留whole-world pause以延續回歸；影響參數
放獨立Resource，完全不動shared manifest；不做新美術，只重用idle與裝飾地面；
保留菱形作mockup推薦，L03不擴圖；工具缺ffmpeg就用既有Pillow，不安裝；
精確粒子數不可觀測就標上限；未取得真人回饋就保留HUMAN_PENDING。

最後一次正式capture後，只修復被原測試抓到的除錯提示文字，並已在W6最終89項
重跑通過；打擊層與主畫面效果未再變動。W7追加交接後再跑既有offline audit並更新source hashes，沒有擴大
測試或實作範圍。最終hash含此交接；active audit stdout與hash檔本身不自我納入。
實際退出碼與scope記錄見VERIFICATION／audit。pre-commit原樣執行，既有
missing_canonical_memory僅report-only advisory，沒有繞過hook。

| Step | Local commit |
| --- | --- |
| W1 baseline／gaps | `4ca7bfb` |
| W2 profiles／layers | `8c5dd5c` |
| W3 tests／before-after evidence | `da29b7f` |
| W4 proposal | `d789734` |
| W5 isolated mockup | `f383128` |
| W6 final verification／scope | `d6ed2ad` |
| W7 handoff | This commit |

**W7交接commit完成後停止，等待Owner review。不push、merge、PR、stash、部署、
Actions或自動接續下一任務。此為task DONE，不是SessionEnd；沒有宣稱canonical
closeout或完整原生治理接線驗收。**

## spike-04

本段依 Gavin 2026-10-24 21:26 Asia/Taipei 的 Option C 授權，完成獨立的
**可操作24×18戰場**與打擊感降濃。160×94.5px菱形格、約96px人物；沒有製作
32×24、迷霧或正式戰鬥規則。主場景仍為11×9 Skirmish。工程與自動操作證據
通過；**Gavin完整遊玩、鏡頭舒適度、辨識度、美術與打擊感判定仍為HUMAN_PENDING**。
本工作區 `D:\campaign-forge\scratch\godot-spike`，分支 `codex/godot-spike`，
起點 `cbf3608`，本段只做本地commit，不push。

### 啟動與操作

在本工作區執行以下PowerShell；直接啟動新場景，不會更改預設main scene。

```powershell
$godotExe = 'C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
& $godotExe --path godot-spike res://scenes/levels/Field24x18.tscn
# 歷史打擊設定，可替換成 a9_baseline；省略參數就是spike04 toned。
& $godotExe --path godot-spike res://scenes/levels/Field24x18.tscn -- --impact-profile=spike03
# 小教學地圖維持原預設：
& $godotExe --path godot-spike
```

| 操作 | 效果 |
| --- | --- |
| 點隊員→點可達格→再點／Enter | 成本範圍、路徑預覽，再確認移動；每人一回合移動一次 |
| 點射程內敵人→再點／Enter | 預覽傷害2，再確認攻擊；攻擊或等待後結束該人行動 |
| Esc／右鍵 | 取消預覽；中鍵獨立用於拖曳 |
| Tab、IJKL、Enter、T | 循環隊員、移格游標、選擇／確認、循環合法目標 |
| Space／N | 等待／結束我方回合；按鈕同樣可用 |
| WASD／方向鍵、中鍵拖曳 | 鏡頭捲動；速度隨zoom修正 |
| 滾輪、O、F／Home | .8／1／1.2游標錨定縮放、全圖閱讀、定位選取隊員 |
| P／點小地圖、點邊緣箭頭 | 收合小地圖／移鏡頭、定位威脅或目標 |
| E | 邊緣捲動開關，預設OFF，提示同步顯示 |
| G／V | 格線／敵方可達攻擊威脅範圍 |
| B／按住Shift、X | 敵方2×／暫時加速、略過敵方移動動畫；不跳過規則結算 |
| M、C | Reduced Motion、下一次攻擊暴擊展示；展示仍只傷害2 |
| F1、R | telemetry／重新部署；勝敗後也能R改策略 |

滑鼠使用事件本身的viewport座標換算格位；確認鍵的按下與放開由戰術輸入接管，
避免聚焦按鈕重複結算。攻擊／敵方階段鎖戰術輸入，保留加速與診斷操作。
F1列首接戰回合、每兵種平均步數、攻擊／傷害／擊殺／無目標回合、敵方階段秒數；
每次結算將完整逐單位逐回合資料寫到專案內 `.godot/spike04/live-telemetry.json`。
這是本地診斷輸出，沒有帳號、連線或永久遊戲存檔。

### 打擊感03→04

| 參數 | spike03 | spike04預設 |
| --- | ---: | ---: |
| flash_mix | 1.0 | .8；hold16.67ms／80ms不變，暴擊有效mix仍≤1 |
| sparks／spokes | 36／11 | 22／7 |
| 暴擊粒子倍率 | 1.5 | 1.3 |
| 方向偏重／streak | 0／22px | .8／22px；收窄散射，保留命中方向 |
| 一般／暴擊數字字級 | 28／34 | 24／30，縮小14.29%／11.76% |
| hitstop／shake／recoil／dust／zoom／SFX | 原設定 | 配置不變；crit dust數量仍共用已降低的粒子倍率 |

歷史profile原樣保存在 `config/impact_profile_spike03.tres`，Git blob與
`a0ae42c`相同；a9_baseline未改。舊spike03測試只重新指向保存的profile，
新測試另驗證04預設。Skirmish只加profile選擇及方向粒子；HUD、格位、傷害、
阻擋、G005、swing接觸幀／時序未改。
[四組接觸±8幀比較](evidence/spike04/hitfeel/impact-strip-spike03-vs-spike04.png)、
[四組AVI及原始PNG](evidence/spike04/hitfeel/)、
[九次Skirmish時序](evidence/spike04/hitfeel/timing.json)。
一般 .950s、暴擊1.017s、Reduced .717s（固定60FPS）；未讀圖wall最高 .985s。
三setup仍為HP4、格位(1,6)／(1,5)／(3,4)。

### 新戰場與測試規則

獨立 `scenes/levels/Field24x18.tscn`、`scripts/rules/field_rules.gd`、
`data/levels/field_24x18.gd`，不引用裝飾mockup。純函式複製輸入並回傳事件；
場景只播放移動、接觸、傷害、擊退與回合事件。另用小型impact adapter，
避免抽共用邏輯時擾動原Skirmish。

四鄰格，荒地／道路成本1、森林2、高機動森林3、淺灘2，深水／峭壁不通行；
守備高地只有地標、沒有隱藏防禦加成。主道路橫跨y9／10，北森林通往x15的
y5／6淺灘，南森林為較昂貴的通路。地形取自規則資料，不從繪圖推斷。

| 兵種（全部是spike test values） | 移動 | HP | 曼哈頓射程 | 傷害／擊退 |
| --- | ---: | ---: | --- | --- |
| 近戰：托瑪＋guard | 4 | 8 | 1 | 2／1格或阻擋 |
| 遠程：bow-1／2 | 3 | 6 | 2–3；不能貼身射擊 | 2／無擊退；**無LOS** |
| 高機動：scout-1／2 | 6 | 6 | 1 | 2／1格或阻擋，森林額外成本1 |
| 敵騎士 | 4 | 6 | 1 | 2／1格或阻擋 |
| 敵領袖 | 4 | 10 | 1 | 2／1格或阻擋 |

六我方部署西側x2–3；初始11騎士＋1領袖，另有3騎士增援。前線距部署
約11–12曼哈頓格。每人可移動一次後攻擊／等待一次，也可原地攻擊結束行動。
我方→敵方→增援／目標檢查→下回合。**擊敗領袖勝利，托瑪倒下或超過15回合敗北**；
不要求全殲。開場頂部明示目標、失敗條件與上限。

增援在我方第4回合完整預告，第5回合開始到場，出生當回合不動，最早敵方第6回合
行動。入口(23,4)／(23,5)／(23,6)，小地圖與戰場T5標記同步。占位時依
上／左／右／下BFS找最近空且可通行格；完全無空位則延後，沒有憑空覆蓋角色。

AI按群組guard→alert→approach→attack：4格警戒或同群受擊即追擊；領袖持位，
受擊或目標點2格內受威脅才離位。合法射程內先挑低HP、再按id；否則用反向
Dijkstra共用距離圖找最近可攻擊位置。cache鍵為兵種／陣營／occupancy_revision，
移動、死亡、擊退與增援使其失效。種子24018控制座標平手，不用全域RNG。

### 鏡頭與可讀性

base位置／zoom保留玩家導航，attack focus保存並復位到攻擊前狀態，impact只走
offset／短zoom punch。每次縮放／shake都夾在包含HUD安全邊界的世界矩形；
預留左右120px、上下180px空白，所以畫面可能看見菱形地圖之外的深色背景。
O容納整圖並保存返回位置；全圖模式點選可回到局部。選隊員與移動平滑跟隨，
敵方攻擊／增援短提示定位。Reduced Motion定位與移動改snap，關shake／punch／
閃光／粒子／recoil，保留必要回饋。不再跳回(640,360)。

右上可收合、可點的小地圖有地形、我方方塊／敵方三角／領袖菱形、目標、增援與
viewport框。HUD安全區箭頭顯示領袖、已公告入口，以及距我方8格內敵群的一名代表；
可點定位。沒有fog。框、標籤與非純顏色識別仍是原型，密集近戰下重疊需真人看。
[720p部署](evidence/spike04/deployment.png)、[1080p部署](evidence/spike04/deployment-1080.png)、
[相機復位逐幀條](evidence/spike04/camera-follow-return-strip.png)。

### 節奏、平衡與效能

| 自動策略 | 初始布局 | 只調敵方位置後 | 首接戰 | 平均近戰／遠程／高機動步數 | 估計分鐘 |
| --- | --- | --- | ---: | --- | --- |
| road主道 | 7回合敗 | **12回合勝** | 2 | 2.65／2.25／4.86 | 12.9–21.2 |
| flank北側 | 6回合敗 | 7回合敗 | 2 | 2.42／2.29／4.25 | 8.7–14.4 |
| turtle固守＋射擊 | 3回合敗 | 3回合敗 | 2 | 2.33／2.67／2.67 | 4.6–7.6 |

步數是實際走格／存活單位回合，含零移動，成本另記。idle定義為階段開始時，
任何合法可達格都無法攻擊敵人；即使有往前走也可能算idle。首次布局三策皆很早
倒下，故只把側翼／後衛部署拉開，保留兩名前線；未改數值、地形、wave或policy。
前後JSON、事件與命令全部保留。[PACING完整表](evidence/spike04/PACING.md)。

估算=`回合×（實測敵方平均秒＋每回合平均存活我方數×假設每人思考15–25秒）`。
實際場景主道11個敵方階段平均1.999s、最高4.719s；50個我方單位回合／12回合
約4.17人。若固定六人不減員則18.4–30.4分鐘。估算與15–25分鐘部分重疊，
**不代表達成真人目標**；側翼／固守過早失敗仍有問題。簡單policy不是最佳解。

road近戰17次攻擊、53.1%傷害；遠程31.25%傷害卻拿60%擊殺，有出手順序／尾刀
偏差；高機動15.6%傷害、早死。沒有觀察到遠程或高機動>50%傷害統治，但樣本小，
無LOS仍可能利於射手。敵騎士有72個無目標單位回合，後衛／增援可被目標擊殺路線
繞過；增援可見不等於增援有戰術價值。這些是下一輪設計風險，不靠這次自動測試定案。

連續實際場景使用選取／預覽／確認／等待／結束回合跑到12回合勝利；另外60FPS
操作AVI解析實際鍵鼠事件，先捲動／選取／移動，再從該road軌跡首攻擊狀態展示
攻擊／鏡頭返回，**不是完整連續戰役錄影**。另有正常敵方階段AVI。
ffmpeg不存在，交付AVI＋PNG strips；Dummy音效有觸發證據、未實際聆聽。
[MOVIE說明與錄影](evidence/spike04/MOVIE.md)。

| AMD780M、GL Compatibility、720p未錄影 | 平均ms | 最差ms |
| --- | ---: | ---: |
| 捲動 | 19.666 | 42.897 |
| 敵方正常 | 22.776 | 30.366 |
| 敵方2× | 22.521 | 32.135 |

同一敵方第2回合正常2.188s／2×1.433s。短時間inter-frame wall取樣含60FPS
cap與排程，**沒有穩定60FPS保證**。錄影／讀圖會拖長wall，不能當操作延遲；
未錄影完整場景48次一般攻擊最高wall .893s，符合1.7s硬限與1.2s目標；GUT另測
crit／Reduced。[PERFORMANCE原始數字](evidence/spike04/PERFORMANCE.md)。

### 驗證、限制與待人工判定

最終匯入0；GUT **123／123、10,310 assertions、21 scripts、exit0**。
[test log](evidence/spike04/test-run.log)、[驗證指令與真實退出碼](VERIFICATION.md#spike-04)、
[完整證據索引](evidence/spike04/README.md)、[稽核及雜湊](evidence/spike04/audit.json)。
70個共用動畫檔與原始A9 hash相符，grid_rules未變；保護路徑Git diff為空。
首次capture／測試的失敗、包括exit0但含錯誤的紀錄都保留；以最終逐項檢查與乾淨log
為準。未弱化舊測試。既有hook只有非阻擋missing_canonical_memory提示，沒有繞過。

PLACEHOLDER：程式繪製地形／岸線／渡口chunks／樹岩旗／標記；所有我方借托瑪，
敵方借knight-a／b；BOW／BOOT／leader標籤代替正式弓手、坐騎與領袖美術；A9
swing原幀未修，敵騎士以位移代攻擊幀；合成SFX。這些不構成商業美術／動畫驗收。
新地景來源及生成方式在 `art/bigmap/SOURCES.md`；沒有下載第三方素材或修改原幀。

HUMAN_PENDING：Gavin用鍵鼠完整打一場並重來一次，判定鏡頭舒適、96px辨識、
低濃度命中感、15–25分鐘節奏與兵種公平性。工程證據不能替代此判定，也不能
把測試數值升格正式規則。尚無真人回饋；沒有製作存檔、多人、LOS、迷霧或32×24。

後續Owner決策／open questions（每項一行即可；本輪不追問、不執行）：

1. 目標：保留擊敗領袖，或下一輪改占點。
2. 移動：保留4／3／6，或指定要調整的兵種。
3. 24×18真人驗收：通過／需重做；32×24維持未授權，須另開任務。
4. 邊緣捲動：維持預設OFF，或改ON。
5. 敵方速度：預設正常，或預設2×。
6. 增援：維持可繞過守點，或下一輪要求其確實接戰。

### Resource self-check

依 `docs/review/RESOURCE-CHECKLIST.md` 逐項記錄。此為Codex自查，Claude／GPT
獨立review及Owner核准仍屬後續流程；本段沒有新增代理或代填他人review。

| 區段／項目 | 結果與證據 |
| --- | --- |
| A prototype-fast | PASS：WORK先列keep/discard條件，獨立一次性spike；W1–W8是Owner範圍，不擴張正式引擎或故事 |
| A level-design | PASS（有限）：可達主道／昂貴北側淺灘、非全殲目標、road勝利軌跡；側翼策略未證明可勝，已明列風險；本場不是原故事雙分支 |
| A game-ai | PASS：群組警戒、領袖持位、低HP目標、seed與Dijkstra；rules determinism測試及事件JSON |
| A game-ui-ux | PASS：成本／目標／預覽／威脅／敵意／回合／增援／控制提示；720p／1080p實際截圖 |
| A game-feel | PASS工程、HUMAN_PENDING感受：03→04 strips、歷史profile、實測≤1.7s、Reduced；真人尚未判定 |
| B Grid-Tactics架構 | PASS架構／N/A新借用：新pure rules→events→view，沒有本輪複製該repo程式或素材 |
| B HopeMetal MIT | N/A：本輪無借用程式／資產，無新增授權依賴 |
| B engine/dependency | PASS：Owner明確授權的獨立Godot4.7.2 PoC，GDScript＋既有GUT，Python僅離線證據；沒有新增引擎／addon |
| C 單人完整戰鬥3–5分鐘 | HUMAN_PENDING；Owner本輪15–25分鐘覆蓋通用3–5。自動完整win12不等於人類遊玩；估算未證實目標 |
| C 敵人理解／勝敗 | PASS工程：AI事件、road勝／另兩策敗、規則目標／失敗測試 |
| C 兩種戰術不同後果 | PASS：road／flank／turtle結果與傷害分布不同，非正式劇情分支 |
| C 重來改策略 | PASS工程：R／result按鈕與restart測試；真人完整重玩仍pending |
| C 重複結算／卡回合／非法移動／動畫中斷 | PASS測試範圍：pure rules、busy鎖與連續12回合、preview/cancel/confirm、rest/reset測試；不宣稱窮盡所有操作 |
| C 720p／1080p／鍵盤 | PASS工程：原生執行截圖、解析鍵盤／拖曳／滑鼠操作AVI、UI／camera測試；真人舒適度pending |
| C 自動與人工分開 | PASS：所有自動紀錄具名，HUMAN_PENDING與美術判定另列，沒有假稱人工回饋 |
| D SRD／授權／adaptation | PASS邊界／N/A新增SRD：沒有引入WotC IP、書籍或第三方規則；Field數值標記測試值，未改G005／L03或宣稱正式adaptation |
| D AGENTS授權／故事／Git | PASS：只寫godot-spike/，只本地codex分支commit；原故事／保護路徑未改，無push／merge／PR／stash／Actions／部署／S4 |

五個指定skill的唯讀固定版本來源及套用方法見證據README。安全的模糊處選擇：
defensive地形僅作地標；射程採無LOS；增援占位採BFS／延後；歷史Skirmish不抽大共用
重構；profile未知參數回預設；差別兵種只加標籤，不自創正式角色或動畫幀。

### 本段commit

| W | 本地commit |
| --- | --- |
| W1 toned profile／歷史保存／前後證據 | `2360cad` |
| W2 pure rules／24×18資料 | `3e7352b` |
| W3 獨立可玩場景 | `32e6480` |
| W4 三層捲動相機 | `4d74672` |
| W5 小地圖／目標／增援UI | `7bab449` |
| W6 telemetry／自動節奏／執行證據 | `e56b36f` |
| W7 全測試／範圍稽核 | `fafa6f0` |
| W8 本交接／metadata hash刷新 | 本commit |

**W8交接commit後停止，等待review；不push、merge、PR、stash或自動開下一段。
沒有其他worktree寫入、正式世界觀／故事／S4變更。這是task DONE，不是SessionEnd，
不觸發canonical daily closeout，也不宣稱治理完整自動導入。**

## spike-05

本段依Gavin2026-10-26 10:19授權，在`codex/godot-spike`完成W1–W8；
24×18，沒有新美術投資。敵軍啟動、推進、護衛與增援追擊已實作；遠程LOS與掩護
接入純規則、預覽及威脅；閃白／數字再降，鏡頭保護完整行動角色，標籤去重疊。
**工程檢查147/147通過；完整初始部署的獲勝策略尚未驗證，三個固定策略都敗。
本段不能判定平衡、美術或人類可玩性已通過。**

證據入口：[README](evidence/spike05/README.md)、[WORK](evidence/spike05/WORK.md)、
[PACING](evidence/spike05/PACING.md)、[PERFORMANCE](evidence/spike05/PERFORMANCE.md)、
[MOVIE](evidence/spike05/MOVIE.md)、[稽核](evidence/spike05/audit.json)、
[測試](evidence/spike05/test-run.log)。以下數字都是spike測試值，沒有正式設定或S4決策。

### 執行與操作

從本worktree以PowerShell執行；預設主場景仍是小型Skirmish，Field須指定場景。

```powershell
$godot='C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
& $godot --path godot-spike res://scenes/levels/Field24x18.tscn
& $godot --path godot-spike res://scenes/levels/Field24x18.tscn -- --impact-profile=spike04
& $godot --path godot-spike -- --impact-profile=spike03
& $godot --path godot-spike -- --impact-profile=a9_baseline
```

不帶profile參數＝spike05 default；後兩例載入Skirmish，可在場景參數後加同樣旗標
比較Field。未知參數安全回預設。四種profile均有載入／選擇測試。

| 輸入 | 功能 |
| --- | --- |
| 滑鼠左鍵、Tab | 選擇／輪替存活未完成單位 |
| I/J/K/L、Enter | 網格游標、確認移動或攻擊；移動／技能預覽後才確認 |
| T、Esc、Space、N | 輪替合法攻擊目標、取消預覽、待機、結束回合 |
| WASD／方向鍵、中鍵拖曳、滾輪 | 捲動、拖曳、游標附近縮放；名義倍率.8/1/1.2 |
| O、F／Home、E | 全圖閱讀模式、定位選取者、切換邊緣捲動（預設OFF） |
| 小地圖點擊、P | 定位／顯示切換 |
| G、V | 網格、含LOS的敵人可移動後攻擊威脅 |
| M、C | Reduced Motion、下次攻擊crit展示；crit沒有新增傷害規則 |
| B、Shift、X | 切換2×、按住2×、跳過敵方移動展示；預設正常速度 |
| F1、R | 技術資訊／即時telemetry、重新開始 |

忙碌時鎖定戰術輸入；F1是技術檢查，不是玩家必開介面。Reduced關閉閃白、震動及
zoom punch，保留較短hitstop；必要的HUD安全取景仍可直接定位。Esc撤銷尚未確認的
移動／攻擊；已確認動作不回滾。實際parsed滑鼠／Esc／Enter流程見
[操作AVI](evidence/spike05/select-move-ranged-60fps.avi)。

### AI狀態、啟動及護衛

距離均為網格Manhattan；不是畫面像素或遮蔽視野。seed24018；無全域RNG。
非正式戰鬥規則，不推導其他關卡。

| 狀態／觸發 | 行為與記錄 |
| --- | --- |
| guard | 未啟動守衛；仍計真idle，不藏成有效行動 |
| activation | 我軍進入任一組員半徑6；組員被打；受擊組與任一同側組員相距≤5而連帶警戒；或turn4全面出發；任一成立便鎖定，不回guard |
| advance | 共享反向Dijkstra向合法攻擊位置推進；同伴距離微小懲罰最多.72成本，優先實際前進，形成鬆散隊形而非編隊引擎 |
| regroup | 半徑3內我軍數>敵支援數+1，且完全無近支援、有遠方騎士，向最近支援靠攏一次；之後恢復推進，避免無限反覆。擁塞無攻擊路徑時嘗試側向合法格 |
| attack | 當前有合法目標先打，避免穿過近戰；移動後再檢查並攻擊 |
| bodyguard-intercept | reserve兩騎士追截距領袖≤6的我軍，通常限定領袖半徑3內；一次regroup可例外離開範圍，下一次恢復護衛 |
| bodyguard-hold | 無接近威脅且已在半徑3，或邊界內無更好進展，明列保護理由；不偽裝成前進 |
| counter | 領袖有相鄰合法目標便反擊；HP≤4且半徑3內至少兩我軍時優先尋找安全退格 |
| step-back／leader-hold | 無可反擊目標或低血被圍時，最近我軍距離≤2才嘗試一個相鄰合法空格，提高最近距離，且距原指揮點≤2；沒有更安全格就明列持位。不是任意逃跑 |
| intercept | 增援休息後主動追截最接近領袖的我軍；若半徑6尚無目標，沿共享圖追最近可攻位置 |

可攻擊者的focus依序：**絕對HP較低 → 距領袖≤4 → 距攻擊者近 →
遠程／高機動同級優先 → id**。這是合法候選內排序；不隔著近戰無條件跳射後排。
反向距離圖按兵種／陣營／occupancy revision／追截目標共用，移動或死亡後失效；
不為每個候選目的格重建全圖。規則複製輸入，產生intent/move/attack事件，動畫只播放結果。

增援仍turn4預告、turn5從(23,4)/(23,5)/(23,6)進三騎士，出生回合不行動；
入場占用處理沿用spike04。全編制scripted bypass從turn5附近滲透位置開始，
turn7首次交戰（任一方攻擊都算），不是完整起手戰役；
[隔離追擊截圖](evidence/spike05/reinforcement-interception.png)另證明增援在兩個可行動
回合內主動出手。首輪全probe沒有錄到敵增援出手、exit1，失敗證據保留；最終改用
原地圖、原數值的thoma／leader／wave隔離fixture，不把我軍先射增援當作敵軍出手。
三條西側短戰鬥在波次接近前已結束，所以wave仍never。**未證明無法繞過**；
目標仍斬首，沒有強制清波或改入場時間。

### LOS／掩護及地形

新增`field_sight.gd`純函式：網格中心到中心的整數supercover，射程仍Manhattan2–3，
相鄰不能射。中間峭壁`^`、深水岸`~`、存活單位皆阻擋；忽略射手／目標本身。
中間或目標格森林`f`提供**傷害−1、最低1**，多片森林不疊加；沒有機率。
終點格不作阻擋格，但目標森林仍有掩護。

```text
射手 A —— ^／~／其他存活單位 —— B：不可射
射手 A —— f —— B：可射，2→1
射手 A —— . —— B(f)：可射，2→1
精確斜角 A(0,0) → B(2,2)：經過角點時，先檢查x側格，再y側格；兩側都算
```

`attack_info`同時供攻擊判定、候選、高亮、preview、hover、V overlay、AI與autoplay。
V包含成本合法移動後的合法攻擊，沒有出生回合增援威脅；不是只畫距離菱形。
目前敵編制無遠程，若用同API遠程也受相同限制。實例：
[(14,8)→(16,8)深岸阻擋](evidence/spike05/los-blocked.png)、
[(11,6)→(14,6)森林掩護](evidence/spike05/cover-preview.png)、
[威脅](evidence/spike05/threat-los.png)。零實際blocked shots是合法射擊結果，
不是零阻擋機會；W1 counterfactual road3/flank1/turtle1。

**本段地形／部署變更清單：空。**沒有加淺灘、開森林、移敵人或調HP／傷害。
高機動仍move6、森林額外成本沿用；退路不足先保留風險，採scout-retreat探測，
避免在沒有人工判定前改圖製造勝利。

### 閃白、數字與攻擊時序

| 項目 | spike04 | spike05 default |
| --- | --- | --- |
| flash_mix | .8 | .6 |
| hold / fade |16.67 /80ms |0 /60ms |
| crit multiplier /最高mix |1.2 |1.2；field最高.72，Skirmish只延長fade |
| sparks / spokes |22 /7 |18 /6 |
| normal /crit字級 |24 /30 |21 /26（−12.5%／−13.3%） |
| number位置／短pop |頭頂外、原scale |相同 |
| hitstop normal/crit/Reduced |110/170/80ms |相同 |
| directional shake normal/crit |8/12px |相同 |
| recoil /streak /方向bias |9px /22px /.8 |相同 |
| dust /zoom punch /knockback /SFX |原值 |相同 |

spike04先逐byte保存為`impact_profile_spike04.tres`，Git blob與舊default一致；
a9_baseline／spike03未變。Field與Skirmish同profile。看
[四列比較strip](evidence/spike05/hitfeel/impact-strip-spike04-vs-spike05.png)：
contact frame0018及±8張顯示.6較保留目標深色細節、沒有新增hold；仍有明顯接觸亮色，
是否足夠淡由Gavin判斷。比較用原生720p60FPS正常／crit各兩套AVI，不是生成圖。

[timing.json](evidence/spike05/hitfeel/timing.json)：3個Skirmish setup×normal/crit/Reduced，
HP4與(1,6)/(1,5)/(3,4)一致；固定60Hz分別.950／1.016667／.716667s，
wall均≤1.7s、Reduced≤normal；Field40次實際攻擊maxwall.902s，皆達≤1.2s目標。
動畫180/70/40/80/100/150ms、contact3、anchor(455,196)未改。
音效只有Dummy driver觸發，沒有試聽。

### 鏡頭與HUD

720p邏輯安全區(52,230,1176,304)，留開頂部HUD／小地圖與底面板；每角色估計框
(-58,-124,116,140)，另留16px震動預算，涵蓋96px人物、頭／HP／badge。
選取follow、移動、攻擊preview、敵人預pan、接觸均保護行動者／目標完整框；
雙方距離大會暫時縮小實際zoom以容納，保存玩家名義zoom供結束後還原。
回原視角仍受安全區限制。四角／各zoom／crit／遠程雙人／preview立即取景皆有測試。
呈現邊界四周增加留白（左右／上500px、下400px），仍clamp，沒有加網格格數。
手動探索會清除follow保護；無關的畫外單位可能被裁切，不代表選取者仍被裁切。

O仍為閱讀模式：固定14px我軍方形／敵三角、18px領袖菱形，4格HP pips與群組標籤；
重疊marker移位並畫連線。一般模式用螢幕空間兵種＋目前HP短牌，完整選取名稱在HUD。
候選槽及有限fallback依序避開人物、重要prop代理框、畫外指示與先前標籤；
低優先超額標籤可被抑制，JSON明列suppressed，不假稱所有名稱永遠可見。
小地圖維持原座標轉換測試，方5px／三角6px／菱10px可區別，點擊定位有效。
三個明亮入口改一個半徑12、alpha.55群組圈；預告回合／種類／出生休息文字保留。
見[O](evidence/spike05/overview.png)、[密集牌](evidence/spike05/dense-labels.png)、
[邊緣](evidence/spike05/edge-safe.png)、[1080p](evidence/spike05/deployment-1080.png)。
截圖狀態牌框交集0，真人可讀性與鏡頭舒適度另驗。

### 節奏、兵種與效能

| 策略 | before→after結果／回合 | 首接觸 | true idle before→after | after估分鐘 |
| --- | --- | --- | --- | --- |
| road |勝12→敗8 |2→2 |66/97→20/77（68.0%→26.0%） |10.0–16.3 |
| flank |敗7→敗7 |2→2 |45/68→24/69（66.2%→34.8%） |9.9–16.2 |
| turtle |敗3→敗6 |2→2 |22/26→26/55（84.6%→47.3%） |9.3–15.3 |
| bypass（scripted中段） |N/A→敗7 |5 |0/29 |4.4–7.1，非整場 |
| scout-retreat |N/A→敗9 |2 |26/88 |13.3–21.8 |

按組idle、所有策略兵種傷害／擊殺／死亡回合、wave與LOS完整表見PACING。
true idle＝有實際觀測到可行動phase、不能攻擊、未移動／攻擊、無明確持位角色；
guard仍算，出生與terminal後未輪到者排除。W1保存JSON不改，以相同觀測定義重算
before／after。舊72 no-target包含已移動者，不能當真idle。Turtle時間變長，
總idle22→26、比率下降；不宣稱每條絕對值下降。五條after軌跡沒有無理由的active停留。

road近戰／遠程／高機動傷害占比53.1/31.2/15.6%→42.9/23.8/33.3%，
擊殺40/60/0%→66.7/16.7/16.7%；scout死亡3/4→4/5，仍早死。
scout-retreat保命到終局、傷害僅4.5%且0擊殺，角色用途待設計。遠程變化受AI與LOS
同時影響，不能歸因單一機制。Flank7與turtle6仍崩，策略弱點與難度混合；
沒有調低敵數值解決。**沒有找到新AI下原始部署完整勝局**；
[staged win](evidence/spike05/win-staged-terminal.png)只驗證斬首與結果畫面，
[lose](evidence/spike05/lose.png)才是連續road實跑。

估算用turns×(實測敵phase均值＋該回合平均存活我軍×假設15–25秒)，
before1.999s、after3.456164s（8個正常phase，含最後部分phase）。
未含閱讀／選單與真人失誤；bypass只觀測中段，不能比整場。15–25min未成立，
road反而失去勝局。這是下一輪平衡與人類試玩的已知限制。

同機AMD780M、Godot4.7.2 GL Compatibility、720p限60，無錄影／讀回的短樣本：

| 操作 | before mean/worst ms | after mean/worst ms（n） | mean差 |
| --- | --- | --- | --- |
| scroll |19.666/42.897 |20.703/30.588（90） |+1.037ms |
| normal enemy |22.776/30.366 |23.509/33.983（46） |+.733ms |
| 2× enemy |22.521/32.135 |23.124/29.606（30） |+.603ms |

正常／2× turn2呈現1.336／.951s。均值退步如實保留；含排程、camera安全與label工作，
未隔離AI因果，不保證穩定60FPS。Movie固定時鐘不當效能；ffmpeg缺席，用Godot
60FPS AVI與Pillow PNG strips，沒有新增依賴。攻擊時間樣本含一張melee contact讀回，
效能樣本無讀回，兩者不可混用。

### PLACEHOLDER、風險與HUMAN_PENDING

地形／props是既有展示地標，守備高地尚無額外戰鬥bonus；Thoma素材重用作我軍
兵種stand-in、騎士作敵軍stand-in，非新角色美術。A9 swing仍開發PLACEHOLDER，
所有swing／idle／knight PNG、共享素材及manifest未動；SFX為既有原創合成placeholder。
無商業素材、新圖、新正式故事、11×9／G005／L03規則變更。

風險：原始整場可勝性未驗證；壓力變高，三個簡單policy不足以區分策略問題／難度；
增援不能保證必打；cover與嚴格corner規則可能令人困惑；高機動保命與貢獻有取捨；
安全鏡頭會因遠距配對自動退zoom，標籤代理框未涵蓋每種未來prop；
低優先標籤可抑制、重要角色閱讀仍需人工；短效能樣本均值略退步；
自動strip判斷不能代替Owner的美術／感受判定。

**HUMAN_PENDING**：Gavin以原始部署盲玩road／flank／turtle各一次，記錄實際分鐘、
每位傷亡、困惑位置、勝敗原因及想重玩的策略；分別判定移動與攻擊時的鏡頭舒適度、
O標記／HP可讀性、密集牌／增援提示及更淡的normal／crit接觸感。另試聽SFX。
模型操作、測試147通過、stagedwin與已保存舊roadwin都不算這些人工驗收。

### 給Gavin的一行可答問題

1. 勝利維持「擊敗領袖」，或改「佔點」？未答維持斬首；Thoma倒下／超15回合敗。
2. 移動近戰4／遠程3／高機動6是否保留？未答照舊。
3. 邊緣捲動預設OFF是否保留？未答OFF。
4. 敵phase預設正常或2×？未答正常。
5. 增援是否必須交戰？未答只主動追截，不強制目標。
6. 24×18是否通過，之後可否考慮32×24？本段仍未授權32×24。
7. LOS採「峭壁／深岸／單位阻擋，森林−1掩護，斜角兩側檢查」可否保留？未答維持測試值。
8. 高機動優先設計側翼輸出、誘敵偵察、或撤退保命？本段無傷害／HP buff或改路。
9. 下輪先驗證可勝路線與難度，還是維持目前壓力做盲測？本段不自動接續。

### Resource自查（docs/review/RESOURCE-CHECKLIST.md）

| 條目 | 結論／證據 |
| --- | --- |
| A prototype-fast | PASS：W1 WORK先訂keep/discard，Owner W1–W8單一spike；不擴張引擎／素材 |
| A level-design | FAIL／已知限制：地圖／可達性測試仍過，三個初始策略全敗，無新完整win；staged不算。無正式故事雙分支。PACING明列，待Owner決定下一輪 |
| A game-ai | PASS工程：顯式啟動、focus／護衛／增援、確定性與輸入不變測試；理解程度HUMAN_PENDING |
| A game-ui-ux | PASS工程：共用合法性與LOS、V／preview／hover，720p1080p、overview／edge／dense實圖及安全／去重疊測試；真人待驗 |
| A game-feel | PASS工程／HUMAN_PENDING感受：04→05strip、9組timing、40次field attack；保留hitstop/shake/recoil/dust |
| B Grid-Tactics | PASS架構／N/A新借用：pure state→events→animation；未新增複製程式、美術或外部依賴 |
| B HopeMetal MIT | N/A：本輪無借用程式／資產，無新增授權依賴 |
| B engine/dependency | PASS：Owner核准Godot4.7.2獨立PoC、既有GUT，Python僅離線Pillow，無新addon |
| C 單人完整3–5分鐘 | FAIL／已知限制：Owner15–25min覆蓋通用3–5；估算不足驗收，真人全場待測。PACING與HUMAN_PENDING明列 |
| C 敵行為可理解 | PASS工程：intent／activation理由、AI測試／實際enemy AVI；真人判讀待驗 |
| C 可勝可敗 | FAIL／已知限制：terminalwin／lose規則有測，連續road敗8；尚無新AI原始部署整場win，不足整體可玩驗收 |
| C 兩戰術不同結果 | PASS工程：road／flank／turtle終局回合與傷亡不同，scout-retreat保命但低傷害；無正式故事分支宣稱 |
| C restart改策略 | PASS工程：既有R／UI restart與測試；真人重玩HUMAN_PENDING |
| C 無重複／卡回合／非法／中斷 | PASS已測範圍：147tests、scene連續lose8、preview／cancel／confirm、busy鎖、wave休息；不聲稱窮盡 |
| C 720p／1080p／鍵盤 | PASS工程：native畫面、parsed Esc／Enter AVI與minimap／camera測試；舒適度待驗 |
| C 自動／人工分開 | PASS：自動操作具名、fixture標示、失敗保留；無人工回饋或Owner美術通過宣稱 |
| D SRD／來源／adaptation | PASS界線／N/A新增SRD：無新WotC IP／第三方規則，美術未動；所有Field／LOS值標測試，L03／G005未改 |
| D 授權／Git／故事 | PASS：僅godot-spike變更、brief先存；正常local commit，無push／PR／merge／stash／Actions／部署／32×24／故事定案／S4 |

指定五個公開skill唯讀固定版本與方法見README，未安裝。架構reference本輪沒有新借用；
本機external-executable-trust-audit用在Owner提供的明確執行檔路徑與離線證據工具，
不宣稱完成整個工具鏈信任根稽核。C與A的FAIL均有上述明確證據／限制，
**不建議當作整體玩法PASS合入依據**；模型review不是Owner批准或人類測試。

模糊處採最保守做法：不改地形／部署；森林用固定−1而非隨機；corner兩側阻擋；
wave交戰分開記「任一方首次交戰」與「敵增援出手」；勝圖明示terminalfixture；
不為新AI修改數值獲勝。milestone留本project WORK與本交接，沒有寫共用PLAN／memory；
正常hooks只有既有missing_canonical_memory非阻擋advisory，沒有bypass。

### 本段commit

| W | 本地commit |
| --- | --- |
| W1 baseline／idle telemetry | `1e86503` |
| W2 AI pressure／leader／wave | `bfc94f4` |
| W3 LOS／cover共用規則 | `81312d0` |
| W4 flash／numbers／比較證據 | `afb4e9b` |
| W5 camera／overview／labels | `d2907dd` |
| W6 pacing／performance／runtime | `bbe7bfe` |
| W7 全測試／scope／hash | `0505825` |
| W8 本交接／文件hash刷新 | 本commit |

**W8 handoff commit後停止，等待review。只有local commits，沒有push、merge、PR、
git stash或後續slice。Task DONE不是SessionEnd，不執行canonical daily closeout；
沒有完整治理自動導入或人類／Owner驗收宣稱。**

## spike-06

本段已建立可重現的完整勝路：20固定種子的支援側翼策略勝14局（70%），
勝局全部與援軍交戰；實際scene從初始部署連續操作於T13勝利。
GUT **165/165、11,749 assertions**，scope／evidence audit exit0。
15–25分鐘全面估算門檻仍FAIL，影格時間明顯退步，真人盲玩與0.5閃白判斷待驗。
這是本地工程與玩法探針結果，沒有Owner遊玩、美術通過或正式規則定案。

Owner Gavin Wu／Gavin0099於2026-10-26 19:17 Asia/Taipei授權本段；
brief8010bde、前版6ee5cb7，worktree `D:\campaign-forge\scratch\godot-spike`，
branch `codex/godot-spike`。僅godot-spike/，W1–W8逐步commit，**不push**。
沒有改main／其他worktree／共用PLAN或memory，沒有新增代理或正式故事／S4。

### 先給盲玩者

**Gavin若要盲測，先只讀此小節與下一節操作，不讀後面的「勝路」與數據。**
請road／flank／turtle各玩一次，記實際分鐘、每位傷亡、困惑位置、勝敗原因及
下一次想改的策略；記錄斥候定位、援軍預告與到場是否看得懂。
之後再對照自動策略。另判定0.5閃白、V圖例、O標籤、鏡頭舒適度與SFX。
全部標 **HUMAN_PENDING**，自動操作與模型看圖不能代填真人回饋。

### 啟動、操作與重跑

```powershell
$godot='C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe'
$python='C:\Users\daish\AppData\Local\Programs\Python\Python312\python.exe'
& $godot --path godot-spike res://scenes/levels/Field24x18.tscn
# 舊資料（也可配舊profile）；R重啟沿用variant
& $godot --path godot-spike res://scenes/levels/Field24x18.tscn -- --variant=spike05 --impact-profile=spike05
# 單獨比較profile：a9_baseline / spike03 / spike04 / spike05；省略參數為新default
& $godot --path godot-spike -- --impact-profile=spike05
# 上一行進原本Skirmish；明指Field scene才能進大場

# Before重跑，另寫ignored .godot目錄，避免覆蓋已提交證據
& $godot --headless --path godot-spike -s res://tools/autoplay_field.gd -- --variant=spike05 --seeds=fixed --output=res://.godot/spike06-before/
& $godot --headless --path godot-spike -s res://tools/autoplay_field.gd -- --seeds=fixed --enemy-mean=1.47633625 --output=res://.godot/spike06-after/
& $python godot-spike/tools/summarize_spike06.py .godot/spike06-after
# 也支援 --seeds=24018,1001 或 --seeds=1001:1019，--policies=road,flank
& $godot --headless --path godot-spike --import
& $godot --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
```

滑鼠選隊員／落點／目標，Enter或再點確認；Esc／右鍵取消預覽。
Tab換隊員、IJKL移游標、Enter選擇／確認、T換攻擊目標、Space等待、N結束回合、
R重新部署。WASD／方向鍵捲動，中鍵拖曳，滾輪縮放，O全圖／點地圖返回，
F定位、P收合小地圖；E邊緣捲動預設OFF。G格線、V威脅／圖例、M Reduced Motion、
B切2×、Shift按住加速、X略敵移動、F1 debug、C下一擊crit展示。
敵phase預設正常；勝利仍擊敗領袖，Thoma倒下或超15回合敗。

V六色：青綠移動、暗紅敵威脅、橘可攻擊、灰LOS阻擋、金森林−1、紫斥候鄰格攔截。
斥候攻後若剩撤離預算，HUD顯示可移格；等候會結束撤離。這不是再次攻擊。
O群組標籤13→15px、112→144px，沿用有限去重疊；終局隱藏world nameplates，
避免蓋住勝敗文字。沒有新美術。

### 根因與每項調整（全為spike測試值）

舊operator只向最近attack slot衝刺，scout移6把自己送到移4近戰之前；
不判斷危險、保護Thoma或先殺可殺目標，甚至總優先領袖。另一方面，
11騎士＋領袖及3援軍合計94HP對我方40HP，T4全體march疊加連鎖警戒，
不留局部人數優勢。全敗同時包含operator錯誤與壓力堆疊，不能僅據此說AI作弊。

先補kill priority／傷兵撤退／screen cohesion，再依序試部署、march時點、
敵數。較強operator配原部署也未證明勝路；前推部署候選仍敗，六騎士候選
20seed僅45% road勝。保留所有試驗於WORK與w2-*，不假稱最優解／單一因果。
選五騎士時W2 road85%；W3入口、W4 kit及operator改動後，最終支援側翼70%。

| 項目 | spike05 → spike06 | 原因 |
| --- | --- | --- |
| Thoma部署 | (3,9) → (3,10) | 後移半步，讓guard先形成道路屏障 |
| guard部署 | (3,10) → (4,9) | 道路前排 |
| bow-1／bow-2 | (2,8)/(2,11) → (3,8)/(3,11) | 緊跟屏障提供支援 |
| scout-1／scout-2 | (3,7)/(3,12) → (2,8)/(2,11) | 後排側翼起步，避免孤立前衝 |
| 全體march | T4 → T6 | 開局先處理局部；半徑6感知／群組受擊／連鎖警戒仍即時啟動 |
| knight-4 south | (12,15) present → omitted | 少一名同時南面壓力 |
| knight-6／7 flank | (19,4)/(20,4) present → omitted | 留一名北側interceptor，減少三人疊壓 |
| knight-10／11 rear | (22,14)/(23,15) present → omitted | 不與已預告三援軍再疊完整後備波 |
| knight-9 reserve | (19,10) present → omitted | 六騎士45%未過門檻，保留knight-8單bodyguard |
| 初始騎士／領袖／援軍 | 11/1/3 → 5/1/3 | 降同時兵力，不改留下單位的HP／base damage |
| 援軍entry | (23,4)/(23,5)/(23,6) → (23,8)/(23,9)/(23,10) | 東側渡口接近領袖交戰線，縮短追擊距離 |
| 援軍標示 | 東北入口 → 東側渡口入口 | HUD／warning與真實entry一致 |
| scout kit | 無 → 半血收割＋1／鄰格停步／攻後最多2成本撤離 | 側翼、攔截、收割後能回到屏障 |
| road／flank operator | 無危險直衝 → kill優先、傷兵／Thoma保護、scout貼screen、預留撤離並評估leader hold／擊退 | 先補明顯操作錯誤，不加玩家隱藏規則 |

沒有地形格、留下敵人的座標／group、HP、base damage、move4/3/6、射程、
alert6／chain5／support3／bodyguard3／intercept6、leader contest2／counter／
step-back／hold參數、wave T4預告／T5到場／出生休息、15回合與斬首目標的變更。
純supercover LOS、峭壁／深岸／活單位阻擋、森林−1 min1、斜角兩側檢查保持。
新增scout finisher是明示條件加成，不是base stat傷害上調。grid_rules.gd未動。

### 勝路與風險

指定勝路為**近戰護著雙弓沿主道路推進，斥候靠北側y7附近支援側翼**。
先集中消滅當前局部敵人，別為領袖放棄可殺目標；Thoma受傷先退，guard接前線。
scout可走完整6成本趕路，但要打完撤離就盡量只花≤4；貼著screen找殘血收割，
把紫色控制區放在敵軍接近弓手／援軍追路上。到渡口再一起壓領袖，容許擊退
改變counter距離。這是operator的策略說明，不是每格固定答案或人類最佳路線證明。

最終road50%勝，flank70%；road仍有過度集中／時間不夠的風險。
turtle讓敵軍與援軍逐步包上、失去局部優勢；scout-retreat兩scout全活但少了
收割／攔截支援，Thoma常先崩，兩者20種子均0勝。這些是naive probe，不代表
所有真人龜陣都不可能贏。scout仍可T3陣亡，不能當肉盾或無代價誘敵。

### 援軍

T4持續預告，T5由(23,8)/(23,9)/(23,10)進場，出生回合休息，之後沿原AI
追截我方／領袖附近攻擊者。沒有強制擊殺wave的目標，沒有teleport或強制交戰。
flank19/20局曾碰wave、14/14勝局都碰；首次任一方交戰T7[6–8]，
wave自己出手T7[6–9]、被打T8[7–9]。具名事件分開記錄，不把僅到場算交戰。

scripted bypass從T5預放到東側，不是從我方原部署打過去：20/20勝，
T7[6–9]，平均死0.70（近戰.05／弓.50／斥候.15），17/20與wave交戰。
種子1014／1015／1017仍T6零死、沒碰wave。**繞過仍可能，免費繞後反例未消除**；
不能拿這個部分起點的100%勝率宣稱完整最佳路線，也不能宣稱入口調整封死繞路。
本輪用最小entry槓桿，保留反例供難度review，未再加未必要的強制交戰規則。

### 斥候kit與實測角色

半血定義currentHP≤50% maxHP，近戰收割加1（base2仍不變），3HP騎士可收掉；
preview／hover與實際傷害共源。四個正交鄰格為控制區，敵人**進入時結束移動**，
仍能攻擊；從已受控起點離開可以。無reaction傷害，多人控制只記一個來源。
AI合法reach／threat也經同一函數，並非只畫圖阻嚇。

攻擊後可選一次 `min(2,6−已花移動成本)` 撤離；總成本≤6、地形加權計算。
完整移6後無撤離；原地攻擊也只有2，不能補走6、重複撤、再攻擊。
等待消耗機會，下回合重置；保留spike05 variant無kit。
測過full remaining撤離候選，最後保留較小的cap2，沒有暗中給更多移動。

| flank職業／版本 | 傷害／占比 | kills／占比 | 收割 | 攔截 | 平均死 | 死亡回合中位[範圍] | living unit-turns |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| 近戰before | 175/39.6% | 9/20.9% | 9 | 0 | 1.95 | 5[4–7] | 186 |
| 近戰after | 390/39.4% | 42/28.2% | 42 | 0 | .45 | 9[6–10] | 468 |
| 遠程before | 155/35.1% | 34/79.1% | 34 | 0 | 0 | — | 204 |
| 遠程after | 352/35.6% | 46/30.9% | 46 | 0 | .50 | 9[7–13] | 452 |
| 斥候before | 112/25.3% | 0/0% | 0 | 0 | 1.05 | 2[2–5] | 146 |
| 斥候after | 248/25.1% | 61/40.9% | 61 | 87 | 1.15 | 8[3–14] | 364 |

近戰是最高傷害與屏障，遠程是受LOS限制的持續支援，斥候lead收割／攔截，
不是最高傷害。收割定義是對已受傷敵人的致命一下，各職業同定義，baseline由
原damage events重算；intercept是移動在scout控制區結束，不等於一定少吃一次攻擊。
死亡中位僅算死者，存活者censored，不能解讀成全員必活8回合。
與舊default24018的T4–5相比確實更久；20seed baseline中位其實T2，非4–5。
平均死者反而1.05→1.15，戰鬥更長、兵力／部署／policy也改，不能把差別全歸kit。

### 多種子before／after與時間

固定24018、1001–1019。AI原有seed小tie-break＋policy同職業出手順序／同分目標
hash；24018保留舊順序，傷害固定、無部署jitter。W1與W6的spike05各100組
trace、commands、終局、傷亡、archetypes、unit-turns、wave逐一相同。
24018重現road敗8／flank敗7／turtle敗6／retreat敗9／bypass敗7。
distinct traces每20組before10/9/14/9/8，after20/20/12/14/10（以下表順序），
不是把同一場重印20次，也不代表抽到20種真人水平。

| 策略／版本 | 勝率 | 勝回合中位[範圍] | 敗回合中位[範圍] | 平均死亡近／弓／斥 | wave總／勝局 | true idle | 分鐘估算中位區間；全範圍 |
| --- | ---: | --- | --- | --- | --- | ---: | --- |
| road before | 0% | — | 6[5–8] | 1.60/.45/1.85 | 0%/— | 37.1% | 7.3–12.0；6.8–16.3 |
| road after | 50% | 14[10–15] | 14.5[7–16] | .70/.65/1.50 | 100%/100% | 26.9% | 17.5–28.9；10.7–35.0 |
| flank before | 0% | — | 5[5–7] | 1.95/0/1.05 | 0%/— | 43.2% | 6.8–11.1；6.8–16.2 |
| flank after | 70% | 13[7–15] | 16[7–16] | .45/.50/1.15 | 95%/100% | 30.0% | 17.2–28.4；9.9–33.7 |
| turtle before | 0% | — | 8[6–10] | 1.15/.20/1.80 | 30%/— | 32.6% | 10.7–17.5；9.3–22.2 |
| turtle after | 0% | — | 12[9–16] | 1.10/1.05/1.45 | 100%/— | 31.7% | 14.8–24.5；12.2–29.6 |
| scout-retreat before | 0% | — | 5[5–9] | 2/.30/.90 | 0%/— | 40.0% | 6.8–11.1；6.8–21.8 |
| scout-retreat after | 0% | — | 8[6–10] | 1.85/.10/0 | 80%/— | 28.6% | 12.2–20.2；8.6–24.4 |
| scripted bypass before | 0% | — | 6[5–7] | 1/.50/.90 | 20%/— | 0% | 3.3–5.3；1.8–7.1（部分起點） |
| scripted bypass after | 100% | 7[6–9] | — | .05/.50/.15 | 85%/85% | 6.9% | 4.7–7.7；3.1–11.5（部分起點） |

T16是超15回合終局紀錄，沒有額外可玩的第16回合。true idle沿spike05定義，
只算eligible且已observed的敵人，無移動／攻擊、無可達攻擊、非明示role hold；
inactive guard算，出生休息／terminal未處理尾段不算。群組明細見
[PACING](evidence/spike06/PACING.md)。新flank idle288/961≈29.97%，不放寬35%門檻。
LOS所有100after實際阻擋射擊0，flank phase-start blocked機會43；是當下射程內
blocked pair，不是全部可能路徑。policy／部署／兵力一起變，無孤立LOS因果宣稱。

估算＝(終局回合×enemy mean＋living ally unit-turns×假設15–25秒思考)/60。
before mean3.456164s，after獨立無錄影連續勝局12個normal phase mean1.47633625s。
玩家回合勝仍保守算一個enemy phase；bypass部分起點不可當全場分鐘比較。
flank中位17.2–28.4，整個envelope9.9–33.7，**0/20完整區間落於15–25**，
時間目標FAIL，沒有靠HP填充。真人分鐘未知；只有14勝的回合中位13，不保證
人人玩得快／有趣。勝率≥60、weak多敗、非全T8前勝、idle≤35、wave勝局≥70、
scout定位與較晚死亡門檻均PASS；整體好玩與商業品質仍未驗收。

### hit feel與實際時鐘

| 層 | spike05 → spike06 |
| --- | --- |
| flash_mix | .6 → **.5** |
| hold／fade | 0／60ms → 相同；沒有換45ms |
| crit multiplier | 1.2 → 相同；profile理論乘積.72→.6，非field實際亮度 |
| field實際normal／crit峰值 | 兩者均.6 → 兩者均.5（adapter從未乘crit亮度） |
| hitstop normal／crit／Reduced | 110／170／80ms → 相同 |
| directional shake normal／crit | 8／12px，decay4 → 相同 |
| recoil／streak／bias | 9／22px／.8 → 相同 |
| sparks／spokes | 18／6 → 相同 |
| normal／crit number | 21／26px → 相同 |
| dust／zoom .06／knockback／layered SFX | 相同 |

先byte-for-byte保存spike05 resource，blob與6ee5cb7 default同為
65883cfef205855bfef691380b5dc7d09beb5a07。五profile載入／選擇與所有其他exported
值相等都有測試。舊handoff的field「crit .72」不符合adapter實作，這裡明確更正；
Skirmish的crit multiplier作用於fade duration，沒有為湊亮度描述改其他層。

[前後contact±8總strip](evidence/spike06/hitfeel/impact-strip-spike05-vs-spike06.png)、
[field hit](evidence/spike06/hitfeel/field-melee-hit.png)、
[timing](evidence/spike06/hitfeel/timing.json)。normal／crit各兩套contact still與AVI。
模型看圖仍見凍結幀明顯接觸閃光，不能因此宣稱Owner接受0.5。

三Skirmish setup的HP4、cells(1,6)/(1,5)/(3,4)不變；fixed60 simulation秒為
normal.950／crit1.016667／Reduced.716667。**fixed60 wall單獨跑也超hard1.7**，
normal最多1.886456／crit1.971366；保留alone JSON及先前並行觀察，不把並行
當已證實原因。另獨立real-time無錄影／readback九組wall max.8570／.9276／
.6681s，Reduced每setup≤normal；field41次max.943979，皆過實際hard1.7／target1.2。
錄影或固定模擬時鐘wall超標仍是已知限制，兩種時鐘分列，不能刪掉不利測量。

### 效能與畫面證據

| Native720p操作 | spike05 mean/worst ms | spike06 n／mean/worst ms |
| --- | --- | --- |
| scroll | 20.703/30.588 | 54／34.007/46.443 |
| enemy normal | 23.509/33.983 | 70／34.053/47.043 |
| enemy2× | 23.124/29.606 | 43／34.585/45.572 |

AMD780M GL Compatibility，無錄影／readback／其他Godot程序，max60FPS，
normal與2×用同個真實可達wave state。平均+13.304／10.544／11.461ms是
**明顯退步**，不是pass60FPS；舊測T2、新測援軍階段，工作量不同，無單一歸因。
[PERFORMANCE](evidence/spike06/PERFORMANCE.md)保留frame samples與各職業attack latency。

[連續winT13](evidence/spike06/win-continuous.png)、
[連續road1001 loseT8](evidence/spike06/lose.png)、
[1080p](evidence/spike06/deployment-1080.png)、
[midbattle](evidence/spike06/route-midbattle.png)、
[wave](evidence/spike06/reinforcement-engaging.png)、
[ZoC](evidence/spike06/scout-zoc-preview.png)、
[legend](evidence/spike06/threat-legend.png)、[overview](evidence/spike06/overview.png)。
win／lose確實由初始部署一路操作，非終局fixture；其他shots詳
[README index](evidence/spike06/README.md)。兩段60FPS native AVI＋PNG strip是
可達snapshot續播（snapshot保存state／commands），無stagedHP：
[wave strip](evidence/spike06/enemy-wave-60fps-strip.png)及
[scout flank→finish→retreat](evidence/spike06/scout-flank-finish-retreat-60fps-strip.png)。
ffmpeg未安裝，使用Godot MJPEG AVI＋Pillow提PNG；60FPS為simulation clock，
不是此PC實際render FPS。Dummy音效未試聽。

### 驗證、保護範圍與PLACEHOLDER

W7 import0／GUT0，30 scripts、165 passing、11,749 assertions、104.245s；
新增18 tests，舊147保留。歷史部署／18 actors／T4march／NE warning／autoplay
測試固定在保留spike05 variant／operator，profile歷史值固定spike05 resource，
新default獨立測合法性／wave／scout／HUD，沒有刪除或弱化斷言。
最終audit0驗70份共用動畫bytes、A9 grid_rules、W6 runtime freeze、100舊trace、
native dimensions／plate overlaps、AVI hashes、時鐘／scope。完整命令與失敗保留見
[VERIFICATION](VERIFICATION.md)的spike-06與[WORK](evidence/spike06/WORK.md)。

git diff6ee5cb7保護路徑exit0，只有godot-spike/與W1前既有brief；
ui-prototype／docs/art-briefs／docs/proposals／shared-anim／framePNG／11×9
Skirmish三setup／grid_rules未動，唯一共用presentation改動為flash_mix。
source-hashes是包含檔案commit前working bytes＋normalizedLF，排除self／audit stdout；
W8只改本交接／文件與metadata，沒有偷偷重調規則或換美術。

仍為PLACEHOLDER：terrain／props既有展示素材、全我方共用Thoma stand-in、
敵騎士兩stand-in、A9 swing development frames（本輪無任何frame改動）、
SFX與所有Field測試數值。沒有新canon；Thoma已核准短單手flanged mace不變。
24×18 only、無fog，32×24未授權，正式戰鬥／故事／S4沒有新增授權。

### 風險與給Gavin的一行可答問題

70%是20固定seed的competent heuristic結果，包含policy改進，非真人難度分布；
有T7快勝／T15壓線／超15敗，六敵初始數量也可能讓真人覺得稀疏。
scout仍早死且長戰平均死者未降低；ZoC只停步仍可被打。Bypass仍有免費避wave反例。
時間估算FAIL與影格退步保留；固定時鐘wall超標和真人感受需要獨立判斷。
正常hooks僅既有missing_canonical_memory非阻擋advisory，沒有bypass，
不宣稱治理全自動完成或session end。

以下只是交接問題，不在本輪自動執行，也不重問已答defaults：

1. 難度review是否先以目前flank14/20可勝、naive多敗作為盲測起點？答「是／需更易／需更難」。
2. 斥候「半血＋1、鄰格停步、攻後剩餘最多2成本撤離」是否保留到下一次測試？答「留／改哪項」。
3. 三個scripted零死避wave反例可否先保留，下一輪只驗真人能否從初始部署重現？答「可／優先補此項」。
4. 15–25min區間未全面達標，是否先收真人分鐘再考慮節奏改動？答「先盲玩／另指示」。
5. 影格約34ms退步是否排為後續profile優先項？答「優先／排後」。
6. 0.5閃白及V／O可讀性人工判斷為何？答「接受／需改哪個」。

### Resource自查（docs/review/RESOURCE-CHECKLIST.md）

| 條目 | 結論與證據 |
| --- | --- |
| A prototype-fast | PASS：WORK在W2前固定keep/discard／勝率／idle／wave／kit門檻；僅Owner W1–W8，無新素材／引擎擴張 |
| A level-design | PASS已測範圍：部署／leader／entry可達測試、14/20 flank勝與scene連續win13；無本輪故事雙分支，N/A；bypass反例／真人理解待驗 |
| A game-ai | PASS工程：原顯式activation／hold／counter／pursuit，reach納ZoC；determinism／immutability測試與wave AVI；理解HUMAN_PENDING |
| A game-ui-ux | PASS工程：preview／hover／damage／ZoC／threat共源，六色legend、O15px、720/1080native、parsedEsc/Enter；HUMAN_PENDING舒適度 |
| A game-feel | PASS真實時鐘工程／FAIL已解釋限制：Skirmish9＋field41實際≤1.7；fixed60 wall可超1.7，保留。0.5前後strip／其他層不變；感受未驗 |
| B Grid-Tactics | PASS架構／N/A借用：pure rules state→events→view，無新增複製code／art，不下載無license素材 |
| B HopeMetal MIT | N/A：本輪無新增借用程式／資產，無新增授權依賴 |
| B 無新引擎／依賴 | PASS：Owner已核准Godot4.7.2獨立spike，既有GUT／離線Python Pillow，無addon |
| C 單人完整3–5分鐘 | FAIL／已解釋：Owner本輪15–25min覆蓋通用3–5；估算0/20全面達標，真人分鐘待測，不能以自動勝替代 |
| C 敵行為可理解 | PASS工程：intent與warning理由可見、AI／ZoC純規則測試及wave AVI；真人判讀未驗 |
| C 可勝可敗 | PASS工程：同原始部署實際flank win13／road lose8，100after終局／零illegal，非staged terminalwin |
| C 兩戰術不同結果 | PASS工程：flank70／road50／turtle0，貢獻／傷亡不同；非正式故事分支或真人勝率 |
| C 可重開換策略 | PASS工程：原R／button restart測試保留，variant restart維持；人類重玩未驗 |
| C 無重複／卡回合／非法／中斷 | PASS已測：165tests、scene連續勝敗、parsed preview/cancel、cap2 budget／不可重複、100runs零illegal；非窮盡證明 |
| C 720／1080／鍵盤 | PASS工程：native圖片、parsed mouse/Esc/Enter scout AVI、既有keyboard/camera測試全過；效能退步另列，無60FPS保證 |
| C 自動／人工分開 | PASS：capture mode與snapshot標明、HUMAN_PENDING盲玩未代填、失敗保留；模型review不是Owner批准 |
| D SRD／來源／adaptation | PASS授權界線／N/A新增SRD：無WotC IP／外來規則或美術；自創spike kit、未改L03/G005。checklist所引RULE-ADAPTATION-CONTRACT.md在checkout不存在，未虛稱審過 |
| D AGENTS／Git／故事 | PASS：Owner明確指定本worktree／brief範圍，僅godot-spike正常commits，無push／PR／merge／stash／Actions／部署／32×24／canon/S4 |

五個公開skill唯讀固定版方法與來源見[README](evidence/spike06/README.md)，未安裝或抄用素材。
本機[external-executable-trust-audit](C:/Users/daish/.codex/skills/external-executable-trust-audit/SKILL.md)
用於明確Owner執行檔與離線工具；未宣稱PATH／DLL／Git全信任根審核。
沒有叫Claude或GPT代理review，此自查不冒充獨立review。所有C／D未過項均已解釋；
**建議review本輪工程結果與人工待驗項，不把audit pass當整體遊戲通過。**

### 保守選擇與commit表

不動terrain／leader參數，先較強operator再部署／時點／敵數，wave僅移entry；
kit用小cap2不擴move6；不為達分鐘填HP；不因三個bypass反例擅加forced objective；
field crit實作與舊文件矛盾時保留adapter、據實更正描述；影格與固定時鐘wall
不利結果全列。共享PLAN／memory不在本段scope，milestone留WORK／本交接。

| W | 本地commit |
| --- | --- |
| W1 多種子baseline／preserved05 | `5cff31f` |
| W2 根因／部署／可靠路線 | `535d951` |
| W3 東側援軍entry | `29ec69f` |
| W4 scout收割／控制／撤離 | `c0bfab0` |
| W5 flash0.5／HUD／hit evidence | `75a37fc` |
| W6 final100＋recheck100／real runtime | `c323990` |
| W7 165tests／scope／hash audit | `a89e2b0` |
| W8 本交接／文件hash刷新 | 本commit |

**W8 handoff commit後停止。沒有push、merge、PR、git stash或未授權後續工作。
Task DONE不是SessionEnd；沒有canonical closeout、完整治理自動導入、人類／Owner批准宣稱。**
