"""Offline reports/native AVI extraction; no subprocess, network or game edits."""
import hashlib
import json
import re
import shutil
import struct
from io import BytesIO
from pathlib import Path
from statistics import mean
from PIL import Image, ImageDraw
from package_spike03 import chunks
from summarize_spike06 import aggregate

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT/'docs/evidence/spike06'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(value+'\n',encoding='utf-8',newline='\n')

def formatted(span):
    return '—' if span is None else f"{span['median']:g} [{span['min']:g}–{span['max']:g}]"

def reports():
    before=aggregate(OUT/'baseline',write=False,verbose=False)
    after=aggregate(OUT/'after',verbose=False)
    recheck=aggregate(OUT/'baseline-recheck',verbose=False)
    comparisons=[]
    for policy in before['policies']:
        for seed in before['seeds']:
            a=read(OUT/'baseline/runs'/f'{policy}-{seed}.json')
            b=read(OUT/'baseline-recheck/runs'/f'{policy}-{seed}.json')
            for key in ('trace_hash','commands','status','turns_to_result','ally_deaths','archetypes','unit_turns','reinforcement_first_engage_turn'):
                assert a[key]==b[key],(policy,seed,key)
            comparisons.append({'policy':policy,'seed':seed,'trace_matches':True})
    write(OUT/'baseline-recheck/comparison.json',json.dumps(comparisons,indent=2))
    runtime=read(OUT/'runtime-measure.json')
    assert runtime['status']=='win' and runtime['turns_to_result']==13
    phase_mean=mean(p['seconds'] for p in runtime['enemy_phase_seconds'])
    for path in (OUT/'after/runs').glob('*.json'):
        assert abs(read(path)['estimate_enemy_mean_seconds']-phase_mean)<1e-9
    lines=['# spike-06 multi-seed before/after', '',
        '20 fixed seeds per policy. Before: unchanged spike05 data/operator. After: tuned default plus supported road/flank and scout kit. Bypass is a scripted turn5 start, not full-battle pacing.', '',
        '| Policy/version | Win | Win turn median[range] | Loss turn | Mean casualties M/R/S | Wave all / wins | First engage | True idle | Estimate median; full range min |',
        '| --- | ---: | --- | --- | --- | --- | --- | ---: | --- |']
    for name in before['policies']:
        for label,data in [('before',before),('after',after)]:
            r=data['policies'][name]
            classes=r['classes']
            casualties='/'.join(f"{classes[k]['mean_casualties']:.2f}" for k in ('melee','ranged','mobile'))
            wavewin='—' if r['reinforcement_engagement_in_wins'] is None else f"{r['reinforcement_engagement_in_wins']:.0%}"
            lo,hi=r['length_minutes'];ml,mh=r['median_length_minutes']
            lines.append(f"| {name}/{label} | {r['win_rate']:.0%} | {formatted(r['win_turns'])} | {formatted(r['loss_turns'])} | {casualties} | {r['reinforcement_engagement_rate']:.0%}/{wavewin} | {formatted(r['wave_first_engage'])} | {r['true_idle_share']:.1%} | {ml:.1f}–{mh:.1f}; {lo:.1f}–{hi:.1f} |")
    lines += ['',f'Estimate = (result turn × enemy mean + living ally unit-turns × assumed15–25 seconds)/60. Before mean3.456164s; after{phase_mean:.6f}s from12 actual normal phases of the uncaptured flank seed24018 win13. A conservative result-turn phase is included even for a player-turn win. Bypass uses observed ally turns from its scripted start, so never compare its minutes as a full route.',
        'No15–25min acceptance from model arithmetic: intervals span outside target; no HP padding. Actual human minutes pending.', '',
        '## Pressure and wave details', '',
        '| Policy/version | front | flank | south | reserve | rear | leader | wave | Observed enemy turns | Wave attacks / attacked median[range] | LOS blocked actual shots / phase-start opportunities |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |']
    for name in before['policies']:
        for label,data in [('before',before),('after',after)]:
            r=data['policies'][name]
            idle=' | '.join(str(r['idle_by_group'][g]) for g in ('front','flank','south','reserve','rear','leader','reinforcements'))
            lines.append(f"| {name}/{label} | {idle} | {r['observed_enemy_turns']} | {formatted(r['wave_first_attack'])} / {formatted(r['wave_first_attacked'])} | {r['los_blocked_shots']} / {r['los_blocked_opportunities']} |")
    lines += ['', 'True idle: eligible observed enemy actor, no reachable attack at registration, no move/attack, no explicit role hold. Inactive guards count; birth rest and unprocessed terminal tails do not. Legal actual shots must remain unblocked; opportunity counts are in-range blocked pairs at phase registration, not all hypothetical moves.', '',
        '## Class contribution / survival', '',
        '| Policy/version/class | Damage/share | Kills/share | Finishing kills | Intercepts | Mean deaths | Death turn median[range] | Living unit-turns |',
        '| --- | --- | --- | ---: | ---: | ---: | --- | ---: |']
    for name in before['policies']:
        for label,data in [('before',before),('after',after)]:
            for kind,r in data['policies'][name]['classes'].items():
                lines.append(f"| {name}/{label}/{kind} | {r['damage']}/{r['damage_share']:.1%} | {r['kills']}/{r['kill_share']:.1%} | {r['finishing_kills']} | {r['intercepts']} | {r['mean_casualties']:.2f} | {formatted(r['death_turns'])} | {r['living_unit_turns']} |")
    r=after['policies']['flank'];c=r['classes']
    checks={'intended_flank_win_ge_60':r['win_rate']>=.6,
        'wave_ge_70_of_wins':r['reinforcement_engagement_in_wins']>=.7,
        'idle_le_35':r['true_idle_share']<=.35,
        'not_all_wins_before8':r['win_turns']['max']>=8,
        'scout_not_top_damage':c['mobile']['damage_share']<max(c['melee']['damage_share'],c['ranged']['damage_share']),
        'scout_leads_finishers':c['mobile']['finishing_kills']>=max(c['melee']['finishing_kills'],c['ranged']['finishing_kills']),
        'scout_death_median_later':c['mobile']['death_turns']['median']>before['policies']['flank']['classes']['mobile']['death_turns']['median'],
        'naive_policy_loses_majority':any(after['policies'][p]['win_rate']<.5 for p in ('turtle','scout-retreat')),
        'all_intended_estimate_intervals_inside_15_25':r['length_intervals_inside_target']==20}
    lines += ['', '## Locked targets', '', *[f'- {key}: {"PASS" if value else "FAIL"}' for key,value in checks.items()], '',
        f"Only{r['length_intervals_inside_target']}/20 intended-policy full estimate intervals fit15–25min; median interval is{r['median_length_minutes'][0]:.1f}–{r['median_length_minutes'][1]:.1f}min.",
        'Melee supplies the durable screen and the highest aggregate damage; ranged supplies LOS-constrained support; scouts lead finishing/interception rather than damage. Death medians are conditional on dying, with survivors censored; longer battles and deployment/count changes confound isolation of kit effects. Some scouts still die early. Finishing kill = last hit against an already wounded target; baseline counts recomputed from unchanged damage events using the same definition. Intercept = a movement ended on scout control (one source credited if several), not a guaranteed prevented attack.',
        'All100 spike05 recheck traces, commands, outcomes, casualties, classes and unit-turns match W1. No jitter or random damage. Distinct traces per20 after: '+', '.join(f"{p} {v['distinct_traces']}" for p,v in after['policies'].items())+'.',
        'BOTH policies and level changed between versions; this is not isolated LOS/AI causality, optimal strategy proof, human blind play or commercial quality acceptance.']
    bypass=[read(p) for p in sorted((OUT/'after/runs').glob('bypass-*.json'))]
    missed=[row for row in bypass if row['reinforcement_first_engage_turn']<0]
    lines += ['', '## Scripted bypass counterexamples', '',
        'The probe starts atT5 with pre-positioned allies. Its100% win rate and low average casualties are not evidence of an obtainable optimal full route. The wave is still avoidable; no forced objective was introduced. These no-wave wins remain explicit design risks:', '',
        '| Seed | Win turn | Casualties |', '| --- | ---: | ---: |',
        *[f"| {row['seed']} | {row['turns_to_result']} | {len(row['ally_deaths'])} |" for row in missed]]
    write(OUT/'PACING.md','\n'.join(lines))
    write(OUT/'targets.json',json.dumps(checks,indent=2))
    performance(phase_mean)

def performance(phase_mean):
    perf=read(OUT/'performance.json');old=read(PROJECT/'docs/evidence/spike05/performance.json')
    lines=['# Native720p performance on this PC','',perf['method'],'',
        '| Operation | spike05 mean/worst ms | spike06 n | mean/worst ms | Mean delta |',
        '| --- | --- | ---: | --- | --- |']
    metrics={}
    for kind in ('scroll','enemy-normal','enemy-fast'):
        a=[s['ms'] for s in old['samples'] if s['phase']==kind]
        b=[s['ms'] for s in perf['samples'] if s['phase']==kind]
        assert a and b
        metrics[kind]={'n':len(b),'mean_ms':mean(b),'worst_ms':max(b),'mean_delta_ms':mean(b)-mean(a)}
        lines.append(f'| {kind} | {mean(a):.3f}/{max(a):.3f} | {len(b)} | {mean(b):.3f}/{max(b):.3f} | {mean(b)-mean(a):+.3f} |')
    attacks=read(OUT/'attacks-measure.json')
    assert attacks and all(a['wall_seconds']<=1.7 for a in attacks)
    lines += ['',f'Uncaptured continuous flank normal enemy mean{phase_mean:.6f}s across12 phases. Normal and2× phase samples use the same reached wave state. Positive frame deltas are observed regressions, not isolated causation; scene workload differs from spike05 T2. No steady60FPS claim.', '',
        '| Real-time uncaptured attack | n | mean / max wall s | max process s |','| --- | ---: | --- | ---: |']
    for kind in sorted({a['kind'] for a in attacks}):
        rows=[a for a in attacks if a['kind']==kind]
        lines.append(f"| {kind} | {len(rows)} | {mean(a['wall_seconds'] for a in rows):.3f}/{max(a['wall_seconds'] for a in rows):.3f} | {max(a['process_seconds'] for a in rows):.3f} |")
    lines += ['', 'Separate screenshot/AVI proof runs are not performance measurements. Fixed60 movie-clock wall duration can exceed gameplay timings; hitfeel/timing.json retains both clocks. Dummy audio driven, not auditioned. Human comfort/pacing pending.']
    write(OUT/'PERFORMANCE.md','\n'.join(lines))
    write(OUT/'metrics-summary.json',json.dumps({'enemy_mean_seconds':phase_mean,'performance':metrics,'attack_samples':len(attacks)},indent=2))

def movies():
    index={}
    for mode,name in [('enemy','enemy-wave-60fps'),('scout','scout-flank-finish-retreat-60fps')]:
        capture=read(OUT/f'capture-{mode}.json')
        assert capture['pass'] and all(capture['checks'].values())
        source=PROJECT/'.godot/spike06-field'/f'{mode}.avi'
        raw=source.read_bytes();parts=list(chunks(raw,12,len(raw)))
        header=next(v for k,v in parts if k==b'avih')
        fps=1_000_000/struct.unpack_from('<I',header)[0]
        assert abs(fps-60)<.01
        frames=[v for k,v in parts if k in (b'00dc',b'00db')]
        for frame in frames:
            with Image.open(BytesIO(frame)) as im: assert im.size==(1280,720)
        shutil.copyfile(source,OUT/(name+'.avi'))
        native=OUT/(mode+'-frames');native.mkdir(exist_ok=True)
        sheet=Image.new('RGB',(1440,900),'#101a19');draw=ImageDraw.Draw(sheet)
        for i in range(9):
            n=i*(len(frames)-1)//8
            im=Image.open(BytesIO(frames[n])).convert('RGB')
            im.save(native/f'{n:04d}.png')
            x,y=i%3*480,i//3*300
            sheet.paste(im.resize((480,270)),(x,y+30))
            draw.text((x+6,y+6),f'{mode} F{n} /60FPS',fill='#eee7d6')
        sheet.save(OUT/(name+'-strip.png'))
        index[name]={'fps':fps,'frames':len(frames),'resolution':[1280,720],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    write(OUT/'movie-index.json',json.dumps(index,indent=2))
    write(OUT/'MOVIE.md', '''# Native runtime AVI and PNG strips

ffmpeg is not installed. Godot --write-movie records native1280×720 MJPEG AVI at60 simulation FPS. Pillow verifies headers/every frame and extracts PNGs. Encoder wall time is not runtime FPS.

- enemy-wave-60fps.avi / strip: reached flank seed24018 enemy phase with actual reinforcement attacks. snapshot-enemy.json records the reached state. It is a resumed snapshot movie, not a continuous movie.
- scout-flank-finish-retreat-60fps.avi / strip: reached same-route scout turn, parsed mouse/keyboard select, flank preview, Esc, confirm, finisher and budgeted retreat. snapshot-scout.json binds state/commands; no staged HP or terrain.
- win-continuous.png: actual continuous initial-deployment flank seed24018 win13 through real scene controls. runtime-runtime.json is its telemetry. lose.png is continuous road seed1001 loss, not a terminal fixture.
- deployment/route-midbattle/reinforcement-engaging/route-scout-finisher/threat-legend/overview and deployment-1080 are runtime screenshots.
- hitfeel/: four normal/crit spike05/spike06 AVIs, contact stills and±8 strips.

Performance and latency come from separate uncaptured, uncontended real-time runs. Proof capture timing can be slowed by readback/encoding/concurrent headless sweeps. Dummy SFX was not auditioned. HUMAN_PENDING: feel, readability, actual minutes and blind road/flank/turtle.
''')

def normalize_logs():
    for p in OUT.rglob('*.log'):
        if p.name in {'w6-package.log','w7-audit-run.log'}: continue # stdout may be open on Windows
        raw=p.read_bytes()
        value=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
        value=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',value)
        write(p,'\n'.join(line.rstrip() for line in value.splitlines()).rstrip())

def freeze():
    files={PROJECT/'project.godot'}
    for folder in ('scripts','data','config','scenes','shaders'):
        files.update(p for p in (PROJECT/folder).rglob('*') if p.is_file() and p.suffix!='.uid')
    files.update((PROJECT/'tools').glob('*.gd'))
    rows=[{'path':p.relative_to(PROJECT.parent).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
    write(OUT/'capture-source-hashes.json',json.dumps({'method':'W6 final runtime/data/config/scene/shader/GDScript-operator working bytes. Offline Python/docs/tests excluded; terminal-label-only repair followed by fresh measurements and terminal captures.','files':rows},indent=2))

if __name__=='__main__':
    reports();movies();normalize_logs();freeze()
    print('SPIKE06_FIELD packaged100 before/after/recheck comparisons, movies, real measurements')
