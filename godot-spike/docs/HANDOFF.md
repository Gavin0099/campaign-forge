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
