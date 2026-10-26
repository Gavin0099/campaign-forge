"""Offline evidence audit. No subprocess/network; Git snapshots supplied by operator.
Hashes describe pre-containing-commit working bytes and normalized LF, not HEAD.
"""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
from package_spike06_field import normalize_logs, read, write

PROJECT=Path(__file__).resolve().parents[1]
REPO=PROJECT.parent
OUT=PROJECT/'docs/evidence/spike06'
TEXT={'.gd','.gdshader','.py','.tres','.tscn','.json','.md','.txt','.log','.godot','.uid'}

def sha(raw): return hashlib.sha256(raw).hexdigest()
def save(name,value): write(OUT/name,json.dumps(value,ensure_ascii=False,indent=2))
def content(path):
    raw=path.read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')

def main():
    normalize_logs()
    exits=read(OUT/'w7-exit-codes.json')
    assert exits['import_exit']==exits['gut_exit']==0
    log=content(OUT/'test-run.log')
    tests=int(re.search(r'Passing Tests\s+(\d+)',log).group(1))
    assertions=int(re.search(r'Asserts\s+(\d+)',log).group(1))
    assert tests>=147 and 'All tests passed!' in log
    for name in ['test-run.log','w7-import.log',*[p.name for p in OUT.glob('w6-*.log')]]:
        assert not any(s in content(OUT/name) for s in ('SCRIPT ERROR:','ERROR:','WARNING:','GUT WARNING')),name
    for name in ['git-scope.json','w6-exit-codes.json','w7-exit-codes.json']:
        save(name,read(OUT/name))
    for name in ['changed-paths.txt','untracked-paths.txt','diff-stat.txt']:
        write(OUT/name,content(OUT/name).rstrip())
    scope=read(OUT/'git-scope.json')
    assert scope['branch']=='codex/godot-spike'
    assert scope['protected_diff_exit']==scope['diff_check_exit']==0
    assert scope['historical_profile_blob']==scope['preserved_profile_blob']=='65883cfef205855bfef691380b5dc7d09beb5a07'
    paths=set(content(OUT/'changed-paths.txt').splitlines()+content(OUT/'untracked-paths.txt').splitlines())-{''}
    for name in paths:
        assert name.startswith('godot-spike/') or name=='docs/tasks/godot-spike-06-balance-winroute.md',name
        assert not name.startswith(('godot-spike/art/','godot-spike/scripts/rules/grid_rules.gd')),name
        assert not (name.endswith('.png') and any(s in name.lower().split('/') for s in ['swing','idle','knight-a','knight-b'])),name
    old={r['path']:r for r in read(PROJECT/'docs/evidence/spike02-a9/source-hashes.json')}
    protected=[]
    for p in sorted((PROJECT/'art/anim-shared').rglob('*')):
        if not p.is_file() or p.suffix in {'.import','.uid'}: continue
        source=REPO/'shared-anim'/p.relative_to(PROJECT/'art/anim-shared')
        raw=source.read_bytes();key=source.relative_to(REPO).as_posix()
        assert p.read_bytes()==raw
        assert sha(raw if p.suffix=='.png' else raw.replace(b'\r\n',b'\n'))==old[key]['sha256_working_tree' if p.suffix=='.png' else 'sha256_git_lf']
        protected.append({'path':key,'sha256':sha(raw),'matches_a9':True})
    key='godot-spike/scripts/rules/grid_rules.gd'
    assert sha((REPO/key).read_bytes().replace(b'\r\n',b'\n'))==old[key]['sha256_git_lf']
    frozen=read(OUT/'capture-source-hashes.json')['files']
    for row in frozen: assert sha((REPO/row['path']).read_bytes())==row['sha256'],row['path']
    captures={}
    for mode in ['qa','1080','enemy','scout','runtime','lose','measure','perf']:
        data=read(OUT/f'capture-{mode}.json')
        assert data['pass'] and all(data['checks'].values()),mode
        for shot in data['shots']:
            assert shot['overlaps']==0
            assert Image.open(OUT/(shot['name']+'.png')).size==tuple(shot['resolution'])
            if shot['name'] in ['win-continuous','lose']: assert not shot['labels']
        captures[mode]=data['checks']
    for name,row in read(OUT/'movie-index.json').items():
        raw=(OUT/(name+'.avi')).read_bytes()
        assert sha(raw)==row['sha256'] and len(raw)==row['bytes']
        assert row['resolution']==[1280,720] and abs(row['fps']-60)<.01
    timing=read(OUT/'hitfeel/timing.json')
    assert timing['pass'] and timing['readbacks']==0
    for clock,rows in [('fixed_fps_seconds',timing['runs']),('wall_seconds',timing['runtime_runs'])]:
        assert len(rows)==9
        for row in rows:
            assert row['hp']==4 and row['cell']=={1:[1,6],2:[1,5],3:[3,4]}[row['setup']]
            assert row['same_frame_contact'] and row['input_ready'] and 0<row[clock]<=1.7
        for setup in [1,2,3]:
            modes={r['mode']:r for r in rows if r['setup']==setup}
            assert modes['reduced'][clock]<=modes['normal'][clock]
    for name in ['spike05-normal','spike06-normal','spike05-crit','spike06-crit']:
        row=read(OUT/'hitfeel'/name/'timeline.json')
        assert row['pass'] and row['resolution']==[1280,720]
        assert (OUT/'hitfeel'/name/'attack-60fps.avi').stat().st_size>0
    before=read(OUT/'baseline/aggregate.json');after=read(OUT/'after/aggregate.json')
    assert before['seeds']==after['seeds']==[24018,*range(1001,1020)]
    rechecked=0
    for policy in ['road','flank','turtle','scout-retreat','bypass']:
        assert after['policies'][policy]['runs']==20 and after['policies'][policy]['illegal_commands']==0
        for seed in before['seeds']:
            a=read(OUT/'baseline/runs'/f'{policy}-{seed}.json')
            b=read(OUT/'baseline-recheck/runs'/f'{policy}-{seed}.json')
            for key in ['trace_hash','commands','status','turns_to_result','ally_deaths','archetypes','unit_turns','reinforcement_first_engage_turn']: assert a[key]==b[key]
            rechecked+=1
    for policy,turn in [('road',8),('flank',7),('turtle',6),('scout-retreat',9),('bypass',7)]:
        row=read(OUT/'baseline/runs'/f'{policy}-24018.json')
        assert row['status']=='lose' and row['turns_to_result']==turn
    assert read(OUT/'runtime-runtime.json')['status']=='win'
    assert read(OUT/'runtime-runtime.json')['turns_to_result']==13
    assert read(OUT/'runtime-lose.json')['status']=='lose'
    attacks=read(OUT/'attacks-measure.json')
    assert len(attacks)==41 and all(0<r['wall_seconds']<=1.7 for r in attacks)
    targets=read(OUT/'targets.json')
    assert all(v for k,v in targets.items() if k!='all_intended_estimate_intervals_inside_15_25')
    assert targets['all_intended_estimate_intervals_inside_15_25'] is False # retained honest miss
    assert 'run/main_scene="res://scenes/Skirmish.tscn"' in content(PROJECT/'project.godot')
    save('audit.json',{'pass':True,'meaning':'Evidence consistency / scope / regression pass; not all design targets or human approval.',
        'tests':tests,'assertions':assertions,'scope_base':'6ee5cb7','git_scope':scope,
        'protected_shared_files':protected,'grid_rules_a9_unchanged':True,'capture_source_freeze_matches':len(frozen),
        'captures':captures,'baseline_rechecked_runs':rechecked,'targets':targets,'runtime_attacks':len(attacks),
        'limits':['15–25min full estimate intervals fail; actual human minutes pending.',
            'Material frame-time regression; no steady60FPS claim.',
            'Three scripted bypass seeds avoid the wave without casualties.',
            'Fixed60 simulation-clock wall normal/crit can exceed1.7s; real-time clock passes independently.',
            'Automated operators and resumed snapshot movies are not human blind play.']})
    files={PROJECT/'project.godot',PROJECT/'docs/HANDOFF.md',PROJECT/'docs/VERIFICATION.md',REPO/'docs/tasks/godot-spike-06-balance-winroute.md'}
    for folder in ['scripts','config','scenes','shaders','tests','tools','data']:
        files.update(p for p in (PROJECT/folder).rglob('*') if p.is_file() and p.suffix in TEXT)
    for folder in [OUT,PROJECT/'art/bigmap',PROJECT/'art/anim-shared',REPO/'shared-anim']:
        files.update(p for p in folder.rglob('*') if p.is_file() and p.suffix not in {'.import','.pyc'})
    files={p for p in files if p.name!='source-hashes.json' and not p.name.endswith('audit-run.log')}
    save('source-hashes.json',[{'path':p.relative_to(REPO).as_posix(),'sha256_working_tree':sha(p.read_bytes()),
        'sha256_git_lf':sha(p.read_bytes().replace(b'\r\n',b'\n')) if p.suffix in TEXT else sha(p.read_bytes())} for p in sorted(files)])
    print(f'SPIKE06_AUDIT pass=true tests={tests} assertions={assertions} recheck={rechecked} protected={len(protected)} hashes={len(files)}')

if __name__=='__main__': main()
