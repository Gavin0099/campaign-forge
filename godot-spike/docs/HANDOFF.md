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
