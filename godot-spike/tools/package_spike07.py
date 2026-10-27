"""Offline stratification, provenance checks, native MJPEG extraction. No subprocess."""
import hashlib
import json
import statistics
import struct
import sys
import shutil
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw
from package_spike03 import chunks
from summarize_spike07 import summarize
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/spike07'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fmt(v):return '—' if v is None else f"{v['median']:g} [{v['min']:g}–{v['max']:g}]"
def reports():
    before=summarize(OUT/'baseline');after=summarize(OUT/'after');again=summarize(OUT/'baseline-recheck')
    assert before['seeds']==after['seeds']==again['seeds'] and len(before['seeds'])==40
    checked=[]
    for policy in before['policies']:
        for seed in before['seeds']:
            a=read(OUT/'baseline/runs'/f'{policy}-{seed}.json');b=read(OUT/'baseline-recheck/runs'/f'{policy}-{seed}.json')
            for key in ['trace_hash','commands','status','turns_to_result','ally_deaths','archetypes','unit_turns','bypass_win']:
                assert a[key]==b[key],(policy,seed,key)
            checked.append({'policy':policy,'seed':seed,'trace':a['trace_hash'],'identical':True})
    save(OUT/'baseline-reproduction.json',{'runs':checked,'count':len(checked)})
    scout_checked=[]
    for policy in ['road','flank']:
        for seed in before['seeds']:
            a=read(OUT/'scout/runs'/f'{policy}-{seed}.json');b=read(OUT/'after/runs'/f'{policy}-{seed}.json')
            assert a['trace_hash']==b['trace_hash'],(policy,seed,'W5 changed rules trace')
            scout_checked.append({'policy':policy,'seed':seed,'identical':True})
    save(OUT/'optimized-trace-reproduction.json',scout_checked)
    lines=['# Pacing and stratified40-seed results','',before['sample_caveat'],
        'Seeds24018,1001–1039. Seed varies coordinate AI tie-break and policy ordering only; fixed stats/damage. All default reports have no illegal commands. Bypass is a stagedT5 partial-start probe, never a full-route win or minutes estimate.','',
        '| Policy/version | Wins [95% Wilson] | Bypass wins | Win turns | Loss turns | Wave all / wins | First wave turn | M/B/S mean deaths | True idle | Distinct |',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for p in before['policies']:
        for label,data in [('before06',before),('after07',after)]:
            r=data['policies'][p];lo,hi=r['win_interval95'];w=r['reinforcement_engagement_in_wins']
            deaths='/'.join(f"{r['classes'][k]['mean_casualties']:.2f}" for k in ['melee','ranged','mobile'])
            lines.append(f"| {p}/{label} | {r['win_rate']:.1%} [{lo:.1%}–{hi:.1%}] | {r['bypass_wins']}/40 | {fmt(r['win_turns'])} | {fmt(r['loss_turns'])} | {r['reinforcement_engagement_rate']:.1%} / {w if w is not None else '—'} | {fmt(r['wave_first_engage'])} | {deaths} | {r['true_idle_share']:.1%} | {r['distinct_traces']}/40 |")
    lines+=['','## Policy × outcome strata','', '| Policy/version/outcome | n | Rate [95%] | Turns | M/B/S deaths median[range] | Wave n; first turn | Scout death turn | Distinct |','| --- | --- | --- | --- | --- | --- | --- | --- |']
    for p in before['policies']:
        for label,data in [('before06',before),('after07',after)]:
            for outcome,s in data['policies'][p]['strata'].items():
                lo,hi=s['interval95'];deaths=' / '.join(fmt(s['deaths'][k]) for k in ['melee','ranged','mobile'])
                lines.append(f"| {p}/{label}/{outcome} | {s['count']} | {s['rate']:.1%} [{lo:.1%}–{hi:.1%}] | {fmt(s['turns'])} | {deaths} | {s['wave_engaged']}; {fmt(s['wave_first_engage'])} | {fmt(s['scout_death_turns'])} | {s['distinct_traces']} |")
    lines+=['','## Class contribution and survival','', '| Policy/version/class | Damage share | Kills/share | Finishes | Intercepts | Death turn | Scout early-death run share |','| --- | --- | --- | --- | --- | --- | --- |']
    for p in before['policies']:
        for label,data in [('before06',before),('after07',after)]:
            r=data['policies'][p]
            for k,c in r['classes'].items():
                lines.append(f"| {p}/{label}/{k} | {c['damage']} / {c['damage_share']:.1%} | {c['kills']} / {c['kill_share']:.1%} | {c['finishing_kills']} | {c['intercepts']} | {fmt(c['death_turns'])} | {r['scout_early_death_runs']}/40 |")
    lines+=['','## Enemy idle by group / estimated minutes','', '| Policy/version | front/flank/south/reserve/rear/leader/wave idle | Eligible observed | LOS blocked actual / opportunities | Estimated median minutes / full span | Inside15–25min |','| --- | --- | --- | --- | --- | --- |']
    for p in before['policies']:
        for label,data in [('before06',before),('after07',after)]:
            r=data['policies'][p];idle='/'.join(str(r['idle_by_group'][g]) for g in ['front','flank','south','reserve','rear','leader','reinforcements'])
            lines.append(f"| {p}/{label} | {idle} | {r['observed_enemy_turns']} | {r['los_blocked_shots']} / {r['los_blocked_opportunities']} | {r['median_length_minutes']} / {r['length_minutes']} | {r['length_intervals_inside_target']}/40 |")
    lines+=['','Minutes are arithmetic only: living ally unit-turns ×15–25s + result turn × supplied enemy mean, /60. Read each run estimate_enemy_mean/source; after uses frozen spike06 reference1.47633625s for comparability, NOT a fresh human-time claim. No tuning toward minutes; HUMAN_PENDING. True idle retains spike06 definition; birth rest/unprocessed terminal tails excluded. LOS opportunities are phase-start in-range blocked pairs, not attempted illegal shots.', '',
        '## Targets (definitions locked before tuning)','',
        '- PASS: full-route bypass0/200; partial probe has no wave-free zero-deathT6 win. Empirical probe closure, not proof against all human strategies.',
        '- PASS: road60% within40–60%, flank67.5% within52.5–72.5%; W1 road50%,flank62.5%. Original20W1 road50%,flank70% reproduced. Naive turtle/retreat still mostly lose.',
        '- PASS: intended-route scouts no death<T4 in80/80 (>=90%); no top damage class. FAIL: conditional scout death median7<8, flank finishing kills89<ranged126. Road scoutfinishes122 lead; scoutintercepts188/190 lead.',
        '- PASS minimum native mean20.7/23.5ms; FAIL strict16.67ms all / worst33ms. See PERFORMANCE.md; no stable60FPS claim.',
        '- PASS: 240 frozen06 recheck traces/commands/outcomes/deaths/class/turn metrics exactly match W1;80 W3 traces match after optimized rules. Distinct does not imply independent samples.',
        '- Human timing, clarity, fairness, art/feel approval remain HUMAN_PENDING.']
    (OUT/'PACING.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('REPORT07 240 baseline +80 optimized trace comparisons passed')
def movies():
    index={}
    for mode in ['enemy','scout']:
        source=ROOT/'.godot/spike07-movies'/f'{mode}.avi'
        raw=source.read_bytes();parts=list(chunks(raw,12,len(raw)))
        header=next(v for k,v in parts if k==b'avih');fps=1_000_000/struct.unpack_from('<I',header)[0]
        assert abs(fps-60)<.01
        frames=[v for k,v in parts if k in (b'00dc',b'00db')]
        for frame in frames:
            with Image.open(BytesIO(frame)) as im: assert im.size==(1280,720)
        shutil.copyfile(source,OUT/(mode+'-60fps.avi'))
        strip=Image.new('RGB',(1440,900),'#101a19');draw=ImageDraw.Draw(strip)
        directory=OUT/(mode+'-frames');directory.mkdir(exist_ok=True)
        for i in range(9):
            n=i*(len(frames)-1)//8;im=Image.open(BytesIO(frames[n])).convert('RGB');im.save(directory/f'{n:04d}.png')
            x,y=i%3*480,i//3*300;strip.paste(im.resize((480,270)),(x,y+30));draw.text((x+6,y+6),f'{mode} F{n} @60 simulation FPS',fill='#eee7d6')
        strip.save(OUT/(mode+'-strip.png'))
        index[mode]={'fps':fps,'frames':len(frames),'bytes':len(raw),'resolution':[1280,720],'sha256':hashlib.sha256(raw).hexdigest()}
    save(OUT/'movie-index.json',index)
    (OUT/'MOVIE.md').write_text('''# Actual runtime captures

ffmpeg is absent. Godot --write-movie makes native1280×720 MJPEG AVIs at60 simulationFPS; Pillow validates every frame/header and extracts PNG strips. Encoder wall time is not runtime FPS. Native timing/performance runs have no readbacks/movie and run alone.

- enemy-60fps.avi / enemy-strip.png: actual real-deployment leader-dash1014 reached phase, resumed snapshot; snapshot-enemy.json binds state. Leader/wave attacks respond to the dash. Not a continuous whole-battle movie.
- scout-60fps.avi / scout-strip.png: actual reached flank1006 finisher and safe<=2-cost retreat; mouse/keyboard preview,Esc,confirm, safe-cell threat check. Snapshot provenance in snapshot-scout.json. No staged HP/terrain.
- win-continuous.png: full real-deployment flank1006 through real scene input/confirmation until win; runtime-runtime.json binds the continuous event log. lose.png: continuous road1011 Thoma falls. Neither terminal screen is a staged fixture.
- bypass-before/after-T5,T6,outcome.png: seed1014 scripted partialT5 fixture, explicitly not full route; before/after same turn. Corresponding runtime telemetry/outcome JSON retains wave contact.
- deployment,warning,arrival,route-midbattle,threat-legend,overview,deployment-1080.png are actual runtime shots. pixels-before/after-* and pixel-diff.json prove W5 equivalence.

All art and A9 swings remain existing PLACEHOLDER. Dummy audio was not auditioned. HUMAN_PENDING: blind play, real minutes, fairness, visual/feel approval and perceived smoothness.
''',encoding='utf-8')
    print('MOVIE07 headers/every frame verified, PNG strips and AVI copied')
def freeze():
    files={ROOT/'project.godot'}
    for folder in ['scripts','data','config','scenes','shaders']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix!='.uid')
    files.update((ROOT/'tools').glob('*.gd'))
    save(OUT/'capture-source-hashes.json',{'method':'W6 final runtime/data/config/scenes/shaders and GDScript operators working bytes. Offline Python/docs/tests excluded.','files':[{'path':p.relative_to(ROOT.parent).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]})
if __name__=='__main__':
    if sys.argv[1]=='reports':reports()
    elif sys.argv[1]=='movies':movies()
    elif sys.argv[1]=='freeze':freeze()
