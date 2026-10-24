"""Offline evidence/source audit; Git supplies separate scope snapshots.
No subprocesses, network, source-art writes or external workspace access.
"""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

PROJECT=Path(__file__).resolve().parents[1]
REPO=PROJECT.parent
OUT=PROJECT/'docs/evidence/spike04'
TEXT={'.gd','.gdshader','.py','.tres','.tscn','.json','.md','.txt','.log','.godot','.uid'}
def digest(raw): return hashlib.sha256(raw).hexdigest()
def text(path):
    raw=path.read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
def read(path): return json.loads(text(path))
def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    for path in OUT.rglob('*.log'):
        if path.name.endswith('audit-run.log'): continue
        value=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',text(path))
        path.write_text('\n'.join(line.rstrip() for line in value.splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
    for name in ['w7-exit-codes.json','git-scope.json']: write(OUT/name,read(OUT/name))
    for name in ['changed-paths.txt','untracked-paths.txt','diff-stat.txt']:
        path=OUT/name
        path.write_text(text(path).rstrip()+'\n',encoding='utf-8',newline='\n')
    exits=read(OUT/'w7-exit-codes.json')
    assert exits['import_exit']==exits['gut_exit']==0
    log=text(OUT/'test-run.log')
    count=int(re.search(r'Passing Tests\s+(\d+)',log).group(1))
    assertions=int(re.search(r'Asserts\s+(\d+)',log).group(1))
    assert count>=89 and 'All tests passed!' in log
    for name in ['test-run.log','w7-import.log','w6-sequence-verified.log','w6-enemy-final.log',
                 'w6-full-battle-final.log','w6-1080-final.log','w6-performance-clean.log','w6-debug.log']:
        assert not any(t in text(OUT/name) for t in ['SCRIPT ERROR:','ERROR:','WARNING:','GUT WARNING']),name
    scope=read(OUT/'git-scope.json')
    assert scope['branch']=='codex/godot-spike' and scope['protected_diff_exit']==0
    assert scope['profile_byte_match'] and scope['historical_profile_blob']==scope['preserved_profile_blob']
    paths=set(text(OUT/'changed-paths.txt').splitlines()+text(OUT/'untracked-paths.txt').splitlines())
    for name in paths:
        assert name.startswith('godot-spike/') or name=='docs/tasks/godot-spike-04-bigmap-24x18.md',name
        assert not name.startswith(('godot-spike/art/anim-shared/','godot-spike/scripts/rules/grid_rules.gd')),name
        assert not (name.endswith('.png') and any(p in name.split('/') for p in ['swing','idle','knight-a','knight-b'])),name
    old={r['path']:r for r in read(PROJECT/'docs/evidence/spike02-a9/source-hashes.json')}
    protected=[]
    copied=PROJECT/'art/anim-shared'
    for path in sorted(copied.rglob('*')):
        if not path.is_file() or path.suffix in {'.import','.uid'}: continue
        source=REPO/'shared-anim'/path.relative_to(copied)
        raw=source.read_bytes()
        assert path.read_bytes()==raw
        key=source.relative_to(REPO).as_posix()
        normalized=raw if path.suffix=='.png' else raw.replace(b'\r\n',b'\n')
        assert digest(normalized)==old[key]['sha256_working_tree' if path.suffix=='.png' else 'sha256_git_lf'],key
        protected.append({'path':key,'sha256':digest(raw),'matches_a9':True})
    rules='godot-spike/scripts/rules/grid_rules.gd'
    assert digest((REPO/rules).read_bytes().replace(b'\r\n',b'\n'))==old[rules]['sha256_git_lf']
    captures={}
    for mode in ['sequence','stills','enemy','1080','perf','debug']:
        data=read(OUT/f'capture-{mode}.json')
        assert data['pass'] and all(data['checks'].values()),mode
        for shot in data['shots']: assert Image.open(OUT/shot['file']).size==tuple(shot['resolution'])
        captures[mode]=data['checks']
    timing=read(OUT/'hitfeel/timing.json')
    assert timing['pass'] and timing['readbacks']==0 and len(timing['runs'])==9
    for row in timing['runs']:
        assert row['hp']==4 and row['cell']=={1:[1,6],2:[1,5],3:[3,4]}[row['setup']]
        assert row['same_frame_contact'] and row['input_ready']
        assert 0<row['fixed_fps_seconds']<=1.7 and 0<row['wall_seconds']<=1.7
    for setup in [1,2,3]:
        rows={r['mode']:r for r in timing['runs'] if r['setup']==setup}
        for clock in ['fixed_fps_seconds','wall_seconds']: assert rows['reduced'][clock]<=rows['normal'][clock]
    runtime=read(OUT/'runtime-battle.json')
    assert runtime['status']=='win' and runtime['turns_to_result']==12
    for policy,result,turn in [('road','win',12),('flank','lose',7),('turtle','lose',3)]:
        data=read(OUT/f'autoplay/{policy}.json')
        assert data['status']==result and data['turns_to_result']==turn and data['first_contact_turn']==2
        assert (OUT/f'autoplay/initial/{policy}.json').exists()
    attacks=read(OUT/'runtime-attack-timings.json')
    assert attacks and all(r['wall_seconds']<=1.7 for r in attacks)
    assert 'run/main_scene="res://scenes/Skirmish.tscn"' in text(PROJECT/'project.godot')
    write(OUT/'audit.json',{'pass':True,'tests':count,'assertions':assertions,'scope_base':'a0ae42c',
        'git_scope':scope,'protected_shared_files':protected,'grid_rules_a9_unchanged':True,
        'captures':captures,'skirmish_timing_runs':9,'runtime_attacks':len(attacks),
        'limits':['Automated operator only; HUMAN_PENDING.','Movie clock is not performance; no steady60FPS claim.']})
    files={PROJECT/'project.godot',PROJECT/'docs/HANDOFF.md',PROJECT/'docs/VERIFICATION.md',
           REPO/'docs/tasks/godot-spike-04-bigmap-24x18.md'}
    for folder in ['scripts','config','scenes','shaders','tests','tools','data']:
        files.update(p for p in (PROJECT/folder).rglob('*') if p.is_file() and p.suffix in TEXT)
    for folder in [OUT,PROJECT/'art/bigmap',copied,REPO/'shared-anim']:
        files.update(p for p in folder.rglob('*') if p.is_file() and p.suffix not in {'.import','.pyc'})
    files={p for p in files if p.name!='source-hashes.json' and not p.name.endswith('audit-run.log')}
    hashes=[]
    for path in sorted(files):
        raw=path.read_bytes()
        hashes.append({'path':path.relative_to(REPO).as_posix(),'sha256_working_tree':digest(raw),
            'sha256_git_lf':digest(raw.replace(b'\r\n',b'\n')) if path.suffix in TEXT else digest(raw)})
    write(OUT/'source-hashes.json',hashes)
    print(f'SPIKE04_AUDIT pass=true tests={count} assertions={assertions} protected={len(protected)} sources={len(hashes)}')

if __name__=='__main__': main()
