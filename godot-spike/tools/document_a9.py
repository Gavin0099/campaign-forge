"""Append this segment's reviewable verification/handoff; never rewrite history."""
from prepare_a9_regions import *
import argparse

LINK='evidence/spike02-a9/'

def timing_table():
    lines=['| Resolution / mode | Open | Unit blocked | Terrain blocked |','| --- | --- | --- | --- |']
    for suffix,label in [('', '720p'),('-1080p','1080p')]:
        runs=load(OUT/f'timing{suffix}.json')['runs']
        for reduced in [False,True]:
            selected=[r for r in runs if r['reduced_motion']==reduced]
            lines.append('| '+label+(' Reduced Motion' if reduced else ' normal')+' | '+' | '.join(f'{r["wall_seconds"]:.6f}s' for r in selected)+' |')
    return '\n'.join(lines)

def verification():
    p=ROOT/'godot-spike/docs/VERIFICATION.md';old=p.read_text(encoding='utf-8-sig');assert '## spike-02 A9\n' not in old
    audit=load(OUT/'evidence-audit.json');movie=audit['movie']
    text=f'''

## spike-02 A9

**Engineering/evidence PASS; full art acceptance FAIL,0/5.** A8 is the base,
with enforced local masks and original anchor-pixel transplants. The authorized
Python/manual-blend option was used: zero image_gen calls, zero whole-frame or
whole-sheet regeneration. Four head identities and two uncompressed mace
regions improve; costume/pose repairs did not integrate and were rolled back.
All five motion frames remain PLACEHOLDER. HUMAN_PENDING; Owner art approval
pending. The commission brief is untouched and still needed as the fallback.

### Actual environment and commands

Worktree D:\\campaign-forge\\scratch\\godot-spike; branch codex/godot-spike;
clean start8b6d957 on A8 dcc949c. No fetch/push/remote mutation or branch change.
`PYTHON` = C:\\Users\\daish\\AppData\\Local\\Programs\\Python\\Python312\\python.exe
(Pillow12.2.0); `GODOT` =
C:\\Users\\daish\\AppData\\Local\\Microsoft\\WinGet\\Packages\\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\\Godot_v4.7.2-stable_win64_console.exe.
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
| `GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | First1 (78/79); second0 with type warning; third0,79/79; after alpha correction0,79/79 | Final test-run.log: {audit['assertions']} assertions,13 scripts, no warnings/errors; prior runs retained |
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

{timing_table()}

All12 no-readback runs return input-ready with same-frame contact feedback,
under1.7s. Native60FPS AVI: {movie['frames']} frames,{movie['bytes']:,} bytes,
strike{movie['strike_frame']} ->ready{movie['input_ready_frame']} =
{movie['strike_to_ready_seconds']:.6f}s. Identical decoded contact RGB
frames{movie['contact_frame']}-{movie['resume_frame']-1} = {movie['hold_ms']:.3f}ms;
next frame resumes. No transcoding/subsampling; movie wall time includes
encoding, not game latency.720p/1080p real-time processes ran sequentially.

### Evidence / claim ceiling

[Integrity audit]({LINK}evidence-audit.json), [source hashes]({LINK}source-hashes.json),
[movie]({LINK}attack-60fps.avi), [movie index]({LINK}movie-index.json),
[timing720p]({LINK}timing.json), [1080p]({LINK}timing-1080p.json).

| Pose | Native1280x720 | Native1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG]({LINK}swing-anticipation.png) | [PNG]({LINK}swing-anticipation-1080p.png) |
| Swing/smear | [PNG]({LINK}swing-smear.png) | [PNG]({LINK}swing-smear-1080p.png) |
| Contact during hitstop | [PNG]({LINK}contact.png) | [PNG]({LINK}contact-1080p.png) |
| Follow-through | [PNG]({LINK}follow-through.png) | [PNG]({LINK}follow-through-1080p.png) |
| Idle | [PNG]({LINK}idle.png) | [PNG]({LINK}idle-1080p.png) |

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
'''
    p.write_text(old+text,encoding='utf-8',newline='\n');print('A9_VERIFICATION appended')

def handoff():
    p=ROOT/'godot-spike/docs/HANDOFF.md';old=p.read_text(encoding='utf-8-sig');assert '## spike-02 A9\n' not in old
    audit=load(OUT/'evidence-audit.json');movie=audit['movie'];table=(OUT/'frame-status-table.md').read_text(encoding='utf-8-sig')
    changes=(OUT/'checklist-changes.md').read_text(encoding='utf-8-sig').split('\n\n',1)[1]
    centres=load(OUT/'final-mace-centres.json')
    mace_table='| Frame | Final opaque-ROI centroid | Brief target | Error px |\n| --- | --- | --- | --- |\n'+'\n'.join(f'| {Path(r["frame"]).stem} | {[round(v,3) for v in r["measured"]]} | {r["target"]} | {r["error_px"]} |' for r in centres)
    text=f'''

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
$GODOT = 'C:\\Users\\daish\\AppData\\Local\\Microsoft\\WinGet\\Packages\\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\\Godot_v4.7.2-stable_win64_console.exe'
& $GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd
& $GODOT --headless --path godot-spike --import
& $GODOT --path godot-spike --resolution 1280x720
```

R replays;1/2/3 select open/unit-blocked/terrain-blocked;M toggles Reduced
Motion. Existing keyboard/HUD/controls unchanged. Run GUT with
`& $GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`.
Full final run:{audit['tests']}/{audit['tests']},{audit['assertions']} assertions,
13 scripts, exit0, no warnings. A8's eight original tests now read its archived
PNG/audit; no old assertion removed. Eight A9 tests cover both fixed anchors,
mechanics, region/mask budget, regression flags, kept-pixel confinement and
actual evidence. [Commands/real failures](VERIFICATION.md#spike-02-a9).

### Method / provenance

A8 is the byte-archived base. [Measured defects/targets]({LINK}defects-and-targets.md),
[masks]({LINK}masks/), [all attempts]({LINK}attempts/),
[method]({LINK}METHOD.md), [fix log]({LINK}a9-fix-log.json),
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
original outputs/captures survive under [pre-alpha-cleanup]({LINK}pre-alpha-cleanup/).
Full GUT, native movie, flicker metrics and both resolution captures were rerun
after correction. [Alpha audit]({LINK}alpha-components.json) reports no NEW
tiny4-neighbour opaque clusters;02's A8 diagonal antialiasing pixels remain.
This is a measured regression proxy, not a universal halo detector.

[Integrity audit]({LINK}evidence-audit.json) independently replays the KEPT
regional operations to reconstruct every final RGBA byte, checks confinement
on all46 attempts, anchors/manifest,70 source-copy byte matches and actual
screenshots/movie. Final source snapshot: [hashes]({LINK}source-hashes.json).

### Exact frame gate / A8 to A9 comparison

All13 items must PASS plus technical checks before a motion frame can be
non-PLACEHOLDER. PASS endpoints below mean immutable reference frames, not
Owner art approval or a waiver of transition failures in the middle frames.

{table}

Below are every item, its A8->A9 change and the reason. `improved` can still be
FAIL (mace integration); `same` can still be FAIL (retained A8 cloth/pose).
No formerly passing A8 item is downgraded.

{changes}

[13-item anchor crops]({LINK}checklist.png) /
[machine-readable checklist]({LINK}checklist.json) /
[measured landmark table]({LINK}landmark-deltas.md) /
[sequence strip]({LINK}sequence-strip.png) /
[style check](../../shared-anim/thoma-weapon-style-check.png) /
[A8 above A9, fixed anchors at both ends]({LINK}contact-sheet-a8-vs-a9.png).
These are source assets, not screenshots. Visible manual joint uncertainty
is+/-2px, hidden elbows/knees+/-12px. New head centres derive from anchor picks
and matrices; unchanged joints reuse exact A8 anatomy observations.01 headtop
retains original manual103px because its raised mace overlaps the head ROI.
No strict4px compliance is claimed for occluded anatomy.

### Mace / fixed mechanics

Final independent alpha>0.9 centroid in each37x37 head ROI (including a little
haft/antialiasing overlap); target placement is separate from design/brush PASS.

{mace_table}

03 pixel455,196 remains opaque. All five RGBA/transparent canvases512x512,
pivot256,464, at least one grounded foot464, opaque bottom463-465. Head-to-ground
height approximately360px; fixed original endpoints retain their known height
difference. Full manifest, events, offsets, contact frame3 and anchor455,196
unchanged;180/70/40/80/100/150ms,80ms hitstop, Reduced Motion00/03/05 unchanged.
idle01 and swing05 keep exact original SHA-256. No archived PNG in manifest.

### Actual playback / measured timing

[Actual seven-pose native720p crops]({LINK}playback-keyframes.png) /
[every decoded frame]({LINK}playback-every-frame.png) /
[region metrics]({LINK}playback-check.json). Region mean-colour deltas come
from rendered movie pixels through W1 masks/source alpha transformed into
viewport space. Source silhouette IoU and anatomical height deltas are
separately labelled proxies, not segmentation of rendered RGB or proof of
no flicker. The mixed01 identity and retained wide cloth/stance still jump.

{timing_table()}

All12 no-readback runs return input-ready under1.7s, with same-frame feedback
and at least80ms measured hitstop.720p/1080p real-time captures ran sequentially.
Movie:59 frames,60FPS,{movie['bytes']:,} bytes, strike{movie['strike_frame']}
to ready{movie['input_ready_frame']}={movie['strike_to_ready_seconds']:.6f}s,
identical RGB held{movie['contact_frame']}-{movie['resume_frame']-1}
({movie['hold_ms']:.3f}ms), then resumes. No subsampling/transcoding.
Encoding wall time is not attack latency; Dummy audio is not hardware audition.

[60FPS AVI]({LINK}attack-60fps.avi) / [movie notes]({LINK}MOVIE.md) /
[index]({LINK}movie-index.json) / [720p timing]({LINK}timing.json) /
[1080p timing]({LINK}timing-1080p.json).
Every rendered run printed CAPTURE_COMPLETE pass=true and passed native-size /
pose/hold gates.13 captures per resolution include extra raise/recover and A8
comparisons; the requested five are linked here:

| Pose | Native1280x720 | Native1920x1080 |
| --- | --- | --- |
| Anticipation | [PNG]({LINK}swing-anticipation.png) | [PNG]({LINK}swing-anticipation-1080p.png) |
| Swing/smear | [PNG]({LINK}swing-smear.png) | [PNG]({LINK}swing-smear-1080p.png) |
| Contact during hitstop | [PNG]({LINK}contact.png) | [PNG]({LINK}contact-1080p.png) |
| Follow-through | [PNG]({LINK}follow-through.png) | [PNG]({LINK}follow-through-1080p.png) |
| Idle | [PNG]({LINK}idle.png) | [PNG]({LINK}idle-1080p.png) |

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
ui-prototype/, docs/art-briefs/, original PNG or previous A2-A8 evidence changed.

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
'''
    p.write_text(old+text,encoding='utf-8',newline='\n');print('A9_HANDOFF appended; final table test still required before commit')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verification',action='store_true');ap.add_argument('--handoff',action='store_true');args=ap.parse_args()
    if args.verification:verification()
    if args.handoff:handoff()
