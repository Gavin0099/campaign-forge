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

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verification',action='store_true');args=ap.parse_args()
    if args.verification:verification()
