"""Offline packaging of real Field24x18 captures; no game art edits."""
import hashlib
import json
import shutil
import struct
from io import BytesIO
from pathlib import Path
from statistics import mean
from PIL import Image, ImageDraw
from package_spike03 import chunks

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / 'docs/evidence/spike04'

def read(name):
    return json.loads((OUT/name).read_text(encoding='utf-8'))

def write(name, text):
    (OUT/name).write_text(text+'\n', encoding='utf-8')

def movies():
    index = {}
    for source, name in [('sequence','scroll-select-move-attack-60fps'),('enemy','enemy-phase-60fps')]:
        data = read('capture-'+source+'.json')
        assert data['pass'] and all(data['checks'].values()), data
        raw = (PROJECT/'.godot/spike04-field'/f'{source}.avi').read_bytes()
        parts = list(chunks(raw,12,len(raw)))
        header = next(v for k,v in parts if k==b'avih')
        us_per_frame = struct.unpack_from('<I',header)[0]
        assert abs(1_000_000/us_per_frame-60)<.01
        frames = [v for k,v in parts if k in (b'00dc',b'00db')]
        assert frames
        for frame in frames:
            with Image.open(BytesIO(frame)) as im: assert im.size==(1280,720)
        shutil.copyfile(PROJECT/'.godot/spike04-field'/f'{source}.avi',OUT/f'{name}.avi')
        index[name]={'frames':len(frames),'fps':60,'resolution':[1280,720],
                     'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
        if source=='sequence':
            samples = read('camera-sequence.json')['samples']
            selected = [samples[0],samples[len(samples)//5],
                        next(s for s in samples if s['offset']!='(0.0, 0.0)'),
                        samples[len(samples)*3//4],samples[-1]]
            # Engine process-frame index is the native movie index. Preserve
            # complete frames; downsample only this labelled review strip.
            sheet=Image.new('RGB',(3*480,2*300),'#101a19')
            draw=ImageDraw.Draw(sheet)
            folder=OUT/'camera-frames';folder.mkdir(exist_ok=True)
            for i,s in enumerate(selected):
                number=s['frame'];assert number<len(frames)
                im=Image.open(BytesIO(frames[number])).convert('RGB')
                im.save(folder/f'frame-{number:04d}.png')
                x,y=i%3*480,i//3*300
                sheet.paste(im.resize((480,270)),(x,y+30))
                draw.text((x+4,y+4),f'F{number} zoom{s["zoom"]} offset{s["offset"]}',fill='#eee7d6')
            Image.open(OUT/'camera-return.png').convert('RGB').resize((480,270)).save(folder/'return-review.png')
            sheet.paste(Image.open(OUT/'camera-return.png').resize((480,270)),(960,330))
            draw.text((964,304),'Input-ready: saved base restored',fill='#eee7d6')
            sheet.save(OUT/'camera-follow-return-strip.png')
    write('movie-index.json',json.dumps(index,indent=2))
    write('MOVIE.md',"""# Runtime movies and strips

ffmpeg is unavailable. Godot Movie Maker recorded native 1280×720 MJPEG AVI at
60 simulation frames/s; Pillow only decodes frames and lays out PNG strips.
`movie-index.json` verifies AVI headers, every frame dimension and SHA-256.

- [Scroll/select/move/attack AVI](scroll-select-move-attack-60fps.avi): parsed D,
  middle-drag, O, F, actual mouse select → preview → confirm move. The subsequent
  attack resumes the exact first-attack state of the road policy at turn2;
  it is a staged operating sequence, not a continuous battle movie.
- [Enemy-phase AVI](enemy-phase-60fps.avi): real normal-speed playback of the
  road policy's turn2 enemy phase, no rule changes.
- [Camera follow/return strip](camera-follow-return-strip.png),
  [native extracted frames](camera-frames/), [per-frame camera data](camera-sequence.json).
- [Hit-feel comparison](hitfeel/impact-strip-spike03-vs-spike04.png): normal/crit
  spike03 vs toned spike04, contact ±8 frames; four AVIs in `hitfeel/`.

`capture-sequence.json` requires every parsed input check. Failed attempts and
logs remain under `attempts/` and `w6-sequence*.log`; final verified run is
`w6-sequence-verified.log`. An early script aborted on an empty timing array
yet reported pass; those rejected results are not acceptance evidence.

`capture-stills.json` instead drives a continuous deployment-to-turn12-win
battle through scene UI commands. Its images include first contact, ranged,
melee, turn4 warning, turn5 arrival, overview, enemy phase and win. This is an
automated operator, not a human playtest. Native 1080p deployment is separate.

AVI encoding and PNG readback stretch wall time. Fixed-fps process time is
the movie clock; it is not real input latency or a 60 FPS performance claim.
Unrecorded runtime timings and frame samples are in PERFORMANCE.md. Placeholder
audio was driven through Dummy, not listened to. HUMAN_PENDING remains.
""")

def reports():
    perf=read('performance.json')
    lines=['# Measured 720p performance','','AMD Radeon 780M; Godot4.7.2 GL Compatibility.',
           perf['method'],'','| Operation | Samples | Mean ms | Worst ms |',
           '| --- | ---: | ---: | ---: |']
    for phase in ['scroll','enemy-normal','enemy-fast']:
        values=[s['ms'] for s in perf['samples'] if s['phase']==phase]
        assert values
        lines.append(f'| {phase} | {len(values)} | {mean(values):.3f} | {max(values):.3f} |')
    lines += ['', 'Enemy turn2 wall duration: '+', '.join(
        ('2×' if r['fast'] else 'normal')+f' {r["seconds"]:.3f}s' for r in perf['enemy_phases'])+'.',
        '', 'Inter-frame samples include pacing/UI/rules and OS scheduling; this is a short local',
        'run, not a GPU benchmark or steady-60 guarantee. Worst frames exceed16.67ms.',
        'Raw samples: [performance.json](performance.json); clean exit0: `w6-performance-clean.log`.',
        'Earlier probes/logs remain; the verbose probe identified an unfinished placeholder',
        'audio playback at shutdown. Final capture waits for it and frees streams.',
        '', '| Unrecorded normal attack | n | Mean wall s | Max wall s | Max process s |',
        '| --- | ---: | ---: | ---: | ---: |']
    timing=read('runtime-attack-timings.json')
    assert timing and all(x['wall_seconds']<=1.7 for x in timing)
    for kind in ['melee','ranged','mobile','knight','leader']:
        rows=[r for r in timing if r['kind']==kind]
        lines.append(f'| {kind} | {len(rows)} | {mean(r["wall_seconds"] for r in rows):.3f} | {max(r["wall_seconds"] for r in rows):.3f} | {max(r["process_seconds"] for r in rows):.3f} |')
    lines += ['', 'Strike-to-input-ready includes presentation and return; hard ceiling1.7s, target1.2s.',
              'GUT separately checks crit/Reduced Motion and all Skirmish setups. Movie wall time',
              'includes encoding, so use process seconds there and these unrecorded wall samples.']
    write('PERFORMANCE.md','\n'.join(lines))
    runtime=read('runtime-battle.json')
    phases=runtime['enemy_phase_seconds']; enemy_mean=mean(r['seconds'] for r in phases)
    lines=['# Pacing and balance — automated evidence, HUMAN_PENDING','',
           'Seed24018; rules-only policies have no presentation time. The road policy was also',
           'played continuously through the real scene to win on turn12. The other two policies',
           'are deliberately simple probes; their losses are not proof those routes are unwinnable.',
           'Road: melee-first nearest legal attack / approach leader. Flank: mobile goes via north',
           'ford(16,5). Turtle: stage at(10,9/10), then hold melee unless an attack is reachable.',
           'Targets prefer leader, then lowestHP/id; neither policy is an expert tactics solver.',
           '', '| Policy | Initial result/turn | Retuned result/turn | First contact | Living ally unit-turns | Estimated min |',
           '| --- | --- | --- | ---: | ---: | --- |']
    for policy in ['road','flank','turtle']:
        d=read(f'autoplay/{policy}.json');a=read(f'autoplay/initial/{policy}.json')
        count=sum(v['unit_turns'] for v in d['archetypes'].values() if v['side']=='ally')
        low=(count*15+d['turns_to_result']*enemy_mean)/60
        high=(count*25+d['turns_to_result']*enemy_mean)/60
        lines.append(f'| {policy} | {a["status"]}/{a["turns_to_result"]} | {d["status"]}/{d["turns_to_result"]} | {d["first_contact_turn"]} | {count} | {low:.1f}–{high:.1f} |')
    lines += ['', 'Initial front/side groups overwhelmed every policy. Only authored enemy positions',
              'were retuned: two front, south/flank farther back, rear beyond leader. No stats,',
              'terrain, wave, turn limit or policy were relaxed. Both runs are retained in autoplay/.',
              'First front is 11–12 Manhattan cells from deployment; all policies contact on turn2',
              '(target2–3), so no four-turn empty opening. Northern forest/ford has higher move cost.',
              '', f'Measured normal enemy mean = {enemy_mean:.3f}s over {len(phases)} real phases,',
              f'max = {max(r["seconds"] for r in phases):.3f}s. Estimate formula:',
              '`turns × (measured enemy mean + mean living allies/turn × assumed 15–25s think/unit)`.',
              'Equivalently sum living ally unit-turns ×15–25s plus turns × enemy mean. It includes',
              'a conservative extra enemy phase on the winning turn and omits menu/reading breaks.',
              f'Road has50 unit-turns /12 =4.17 living allies/turn: about{(750+12*enemy_mean)/60:.1f}–{(1250+12*enemy_mean)/60:.1f}min. A fixed',
              f'six-unit assumption gives{(1080+12*enemy_mean)/60:.1f}–{(1800+12*enemy_mean)/60:.1f}min. The15–25min goal is plausible but not verified;',
              'flank/turtle terminate too soon. Human pacing/balance remains pending.',
              '', '| Policy / ally kind | Mean actual steps/unit-turn | Attacks | Damage dealt/taken | Damage share | Kills/share | No reachable target phases |',
              '| --- | ---: | ---: | --- | ---: | --- | ---: |']
    for policy in ['road','flank','turtle']:
        d=read(f'autoplay/{policy}.json');kinds=d['archetypes']
        damage=sum(kinds[k]['damage_dealt'] for k in ['melee','ranged','mobile'])
        kills=sum(kinds[k]['kills'] for k in ['melee','ranged','mobile'])
        for kind in ['melee','ranged','mobile']:
            v=kinds[kind]
            lines.append(f'| {policy}/{kind} | {v["average_move_per_unit_turn"]:.2f} | {v["attacks"]} | {v["damage_dealt"]}/{v["damage_taken"]} | {v["damage_dealt"]/max(1,damage):.1%} | {v["kills"]}/{v["kills"]/max(1,kills):.1%} | {v["idle_turns"]} |')
    lines += ['', 'Movement averages include zero-move living phases, not just moves; per-unit per-turn',
              'steps and weighted cost are in JSON. Idle means no target can be attacked from any',
              'cost-legal destination at phase start, even if the unit moves toward contact.',
              '', 'Road melee supplies53.1% damage and17 attacks: it does engage. Ranged supplies31.3%',
              'damage but60% of kills (last-hit/order bias): flag for human review. Mobile supplies',
              '15.6% damage and dies early, so speed is not dominating this policy. Flank ranged',
              'is50% damage, not >50%; turtle is50% of only4 total damage. These tiny samples do',
              'not establish balance. No LOS benefits ranged; simple leader pursuit exposes scouts.',
              'Road enemy knights have72 no-target unit-phases; rear/wave guards can be bypassed',
              'because the objective is leader defeat, not rout. Reinforcements visibly arrive but',
              'may never engage: a design risk to assess before any larger map. No32×24 built.']
    write('PACING.md','\n'.join(lines))

if __name__=='__main__':
    movies()
    reports()
    print('FIELD_EVIDENCE packaged verified native AVI, camera strip, pacing/performance reports')
