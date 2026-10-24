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

{{FRAME_TABLE}}

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
