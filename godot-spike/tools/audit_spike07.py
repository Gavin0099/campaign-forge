"""Offline W7/W8 evidence and source audit. No subprocess or external workspace reads."""
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/spike07'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def sources():
    files={ROOT/'project.godot',ROOT/'docs/HANDOFF.md',ROOT/'docs/VERIFICATION.md'}
    for folder in ['scripts','data','config','scenes','shaders','tests','tools']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix not in {'.pyc','.import'} and '__pycache__' not in p.parts)
    files.update(p for p in (OUT).glob('*.md'))
    rows=[]
    for p in sorted(files):
        b=p.read_bytes();rows.append({'path':p.relative_to(ROOT.parent).as_posix(),'bytes':len(b),'sha256_working':sha(b),'sha256_LF':sha(b.replace(b'\r\n',b'\n'))})
    save(OUT/'source-hashes.json',{'method':'Pre-containing-commit source bytes, text LF normalization also recorded. Excludes self and generated evidence. W8 refreshes docs only. Git protected audit separately checks unchanged historical blobs.','files':rows})
def audit():
    exits=read(OUT/'w7-exit-codes.json');assert exits['import_exit']==exits['gut_exit']==0
    text=(OUT/'test-run.log').read_text(encoding='utf-8-sig')
    count=int(re.search(r'Passing Tests\s+(\d+)',text)[1]);assert count>=165 and 'All tests passed!' in text
    assertions=int(re.search(r'Asserts\s+(\d+)',text)[1])
    assert not any(s in text for s in ['SCRIPT ERROR:','ERROR:','GUT WARNING'])
    scope=read(OUT/'git-scope.json')
    assert scope['branch']=='codex/godot-spike' and scope['protected_diff_exit']==scope['diff_check_exit']==0
    paths=set((OUT/'changed-paths.txt').read_text(encoding='utf-8-sig').splitlines()+(OUT/'untracked-paths.txt').read_text(encoding='utf-8-sig').splitlines())
    for p in paths:
        assert p.startswith('godot-spike/') or p=='docs/tasks/godot-spike-07-bypass-perf.md',p
        assert not p.startswith(('godot-spike/art/','godot-spike/config/impact_profile','godot-spike/scripts/rules/grid_rules.gd')),p
    assert read(OUT/'w6-exit-codes.json')=={'after':0,'recheck':0,'spike05':0}
    assert read(OUT/'baseline-reproduction.json')['count']==240
    assert len(read(OUT/'optimized-trace-reproduction.json'))==80
    for row in read(OUT/'capture-source-hashes.json')['files']:
        assert sha((ROOT.parent/row['path']).read_bytes())==row['sha256'],row['path']
    for p in ['qa','1080','runtime','lose','enemy','scout','bypass-before','bypass-after','measure']:
        capture=read(OUT/f'capture-{p}.json');assert capture['pass'] and all(capture['checks'].values()),p
        for shot in capture['shots']:
            assert shot['overlaps']==0
            assert Image.open(OUT/(shot['name']+'.png')).size==tuple(shot['resolution'])
    for r in read(OUT/'pixel-diff.json').values():assert r['pixels_changed']==0 and r['bbox'] is None
    for p,v in read(OUT/'movie-index.json').items():
        b=(OUT/(p+'-60fps.avi')).read_bytes();assert sha(b)==v['sha256'] and len(b)==v['bytes'] and abs(v['fps']-60)<.01
    timing=read(OUT/'hitfeel/timing-runtime.json');assert timing['pass'] and len(timing['runs'])==9 and timing['readbacks']==0
    for r in timing['runs']:
        assert 0<r['wall_seconds']<=1.7 and r['hp']==4 and r['cell']=={1:[1,6],2:[1,5],3:[3,4]}[r['setup']]
        assert r['same_frame_contact'] and r['input_ready']
    for setup in [1,2,3]:
        modes={r['mode']:r for r in timing['runs'] if r['setup']==setup};assert modes['reduced']['wall_seconds']<=modes['normal']['wall_seconds']
    timing=read(OUT/'field-timing.json');assert timing['pass'] and timing['readbacks']==0
    for r in timing['runs']:assert 0<r['wall_seconds']<=1.7
    for r in read(OUT/'attacks-measure.json'):assert 0<r['wall_seconds']<=1.7
    runtime=read(OUT/'runtime-runtime.json');assert runtime['status']=='win' and runtime['turns_to_result']==14
    runtime=read(OUT/'runtime-lose.json');assert runtime['status']=='lose'
    after=read(OUT/'after/aggregate.json')
    for p,r in after['policies'].items():assert r['runs']==40 and r['bypass_wins']==0 and r['illegal_commands']==0
    assert .4<=after['policies']['road']['win_rate']<=.6 and .525<=after['policies']['flank']['win_rate']<=.725
    for p in ['turtle','scout-retreat']:assert after['policies'][p]['win_rate']<.5
    # Record known failed targets; do not turn them into silent audit passes.
    save(OUT/'audit.json',{'engineering_evidence_consistent':True,'tests':count,'assertions':assertions,'baseline_rechecks':240,'optimized_trace_checks':80,'known_target_failures':['Scout conditional death median7<8','Flank scouts not leading finishing kills','Not all means<=16.67ms, enemy worst>33ms'],'human':'HUMAN_PENDING; no Owner acceptance inferred'})
    sources()
    print(f'AUDIT07 evidence consistent; {count} passing tests/{assertions} assertions; known target failures explicitly retained')
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='sources':sources()
    else:audit()
