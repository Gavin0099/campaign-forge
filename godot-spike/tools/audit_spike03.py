"""Read-only local evidence checks plus explicit reports/hashes. No subprocesses."""
import hashlib
import json
import math
import re
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
from package_spike03 import chunks

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
OUT = PROJECT/'docs/evidence/spike03'
TEXT = {'.gd','.py','.gdshader','.tres','.tscn','.json','.md','.txt','.log','.godot','.uid'}

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def log(name):
    raw = (OUT/name).read_bytes()
    return re.sub(r'\x1b\[[0-9;]*m','',raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'))

def main():
    # Keep the native command output, but make logs readable text in Git. The
    # active audit stdout files are excluded to avoid changing an open writer.
    for path in OUT.rglob('*.log'):
        if path.name in {'audit-run.log','handoff-audit-run.log'}: continue
        raw = path.read_bytes()
        value = raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
        value = re.sub(r'\x1b\[[0-9;]*m','',value).replace('\r\n','\n').replace('\r','')
        value = '\n'.join(line.rstrip() for line in value.splitlines()).rstrip()+'\n'
        path.write_text(value,encoding='utf-8',newline='\n')
    final_log = log('test-run.log')
    assert 'All tests passed!' in final_log
    count = int(re.search(r'Passing Tests\s+(\d+)',final_log).group(1))
    assert count >= 89
    for name in ['test-run.log','w6-import.log','timing-run.log','still1080-run.log','w5-capture.log']:
        assert not any(token in log(name) for token in ['SCRIPT ERROR:','ERROR:','WARNING:','GUT WARNING']),name
    evidence = {}
    for name,minimum,seconds,capacity in [('before',80,55/60,24),('after',110,57/60,54),('after-crit',170,61/60,81)]:
        folder = OUT/name
        data = load(folder/'timeline.json')
        assert data['pass'] and data['fixed_fps']==60 and data['resolution']==[1280,720]
        assert data['contact_row']>=8
        run = data['runs'][0]
        assert run['same_frame_contact'] and run['input_ready'] and run['hp']==4 and run['cell']==[1,6]
        assert abs(run['fixed_fps_seconds']-seconds)<1e-6
        assert run['hitstop_wall_ms']>=minimum and run['hitstop_process_ms']>=minimum
        frames = data['frames']
        assert [r['process_frame'] for r in frames]==list(range(frames[0]['process_frame'],frames[-1]['process_frame']+1))
        contact = frames[data['contact_row']]
        assert contact['hitstop'] and contact['swing_frame_index']==3 and contact['target_flash']==1
        assert contact['live_particle_count_upper_bound']==capacity
        assert {r['frame'] for r in run['triggers']}=={contact['process_frame']}
        held = [r for r in frames if r['hitstop']]
        native = []
        held_rgb = []
        for row in frames[data['contact_row']-8:]:
            image = Image.open(folder/row['png']).convert('RGB')
            assert image.size==(1280,720)
            assert len(set(image.resize((16,9)).get_flattened_data()))>50
            native.append(row['png'])
            if row['hitstop']: held_rgb.append(digest(image.tobytes()))
        assert len(set(held_rgb))==1,(name,'world must render the held frame identically')
        ready = frames[-1]
        assert ready['phase']=='ready' and not ready['paused'] and ready['target_flash']==0
        assert ready['camera_offset']==[0,0] and ready['camera_zoom']==[1,1]
        assert ready['recoil_delta']==[0,0] and not ready['damage_numbers']
        raw = (folder/'attack-60fps.avi').read_bytes()
        movie = [Image.open(BytesIO(v)).convert('RGB') for k,v in chunks(raw,12,len(raw)) if k in (b'00dc',b'00db')]
        assert all(im.size==(1280,720) for im in movie)
        movie_hashes = [digest(movie[r['process_frame']].tobytes()) for r in held]
        assert len(set(movie_hashes))==1,(name,'decoded AVI hold')
        # MJPEG is lossy; confirm the indexed AVI frame matches the native PNG.
        difference = ImageStat.Stat(ImageChops.difference(movie[contact['process_frame']],Image.open(folder/contact['png']).convert('RGB'))).mean
        assert max(difference)<5,(name,'movie/native frame alignment',difference)
        assert digest(raw)==load(folder/'movie-index.json')['sha256']
        if name!='before':
            assert len(data['impact_layers'])==9
            assert {r['frame'] for r in data['impact_layers']}=={contact['process_frame']}
            assert math.isclose(math.hypot(*contact['camera_offset']),12 if name=='after-crit' else 8,abs_tol=1e-4)
            assert math.isclose(math.hypot(*contact['recoil_delta']),9,abs_tol=1e-4)
            assert abs(contact['camera_zoom'][0]-1.46)<1e-4
            assert len(data['sfx_trace'])==3
            assert [s['hook'] for s in data['sfx_trace']]==['swing_whoosh','impact_crit' if name=='after-crit' else 'impact','knockback_thud']
        evidence[name] = {'native_pngs':len(native),'held_pngs':len(held_rgb),'held_pixels_identical':True,
            'movie_frames':len(movie),'movie_sha256':digest(raw),'movie_hold_pixels_identical':True,
            'movie_vs_png_mean_abs_rgb':difference,'strike_to_ready_seconds':run['fixed_fps_seconds']}

    timing = load(OUT/'timing.json')
    assert timing['pass'] and timing['readbacks']==0 and len(timing['runs'])==9
    runs = {(r['mode'],r['setup']):r for r in timing['runs']}
    for r in timing['runs']:
        assert r['same_frame_contact'] and r['input_ready'] and r['hp']==4
        assert r['cell']=={1:[1,6],2:[1,5],3:[3,4]}[r['setup']]
        assert 0<r['fixed_fps_seconds']<=1.7 and 0<r['wall_seconds']<=1.7
    for setup in (1,2,3):
        for clock in ('fixed_fps_seconds','wall_seconds'):
            assert runs['reduced',setup][clock]<=runs['normal',setup][clock]
    assert Image.open(OUT/'contact-1080.png').size==(1920,1080)
    assert (OUT/'before-vs-after.gif').stat().st_size<8*1024*1024
    mockup = load(REPO/'docs/proposals/big-map/capture.json')
    assert mockup['pass'] and all(mockup['checks'].values()) and len(mockup['screenshots'])==7
    for shot in mockup['screenshots']:
        assert shot['clamped'] and shot['native_resolution']==[1280,720]
        assert Image.open(REPO/'docs/proposals/big-map'/shot['file']).size==(1280,720)
    main_scene = (PROJECT/'project.godot').read_text(encoding='utf-8')
    assert 'run/main_scene="res://scenes/Skirmish.tscn"' in main_scene
    for path in [PROJECT/'scripts/skirmish.gd',PROJECT/'scripts/battle_hud.gd',PROJECT/'scenes/Skirmish.tscn']:
        assert 'mockup' not in path.read_text(encoding='utf-8').lower()

    old = {r['path']:r for r in load(PROJECT/'docs/evidence/spike02-a9/source-hashes.json')}
    protected = []
    copied = PROJECT/'art/anim-shared'
    for path in sorted(copied.rglob('*')):
        if not path.is_file() or path.suffix in {'.import','.uid'}: continue
        source = REPO/'shared-anim'/path.relative_to(copied)
        assert source.read_bytes()==path.read_bytes(),str(path)
        key = source.relative_to(REPO).as_posix()
        previous = old[key]
        raw = source.read_bytes()
        assert digest(raw if path.suffix=='.png' else raw.replace(b'\r\n',b'\n')) == previous['sha256_working_tree' if path.suffix=='.png' else 'sha256_git_lf'],key
        protected.append({'path':key,'sha256':digest(raw),'a9_unchanged':True})
    rules_key = 'godot-spike/scripts/rules/grid_rules.gd'
    assert digest((REPO/rules_key).read_bytes().replace(b'\r\n',b'\n'))==old[rules_key]['sha256_git_lf']
    changed = (OUT/'changed-paths.txt').read_text(encoding='utf-8-sig').splitlines()
    for path in changed:
        assert path.startswith(('godot-spike/','docs/proposals/')) or path=='docs/tasks/godot-spike-03-hitfeel-bigmap.md',path
        assert not path.startswith(('godot-spike/art/anim-shared/','godot-spike/scripts/rules/')),path
        assert not (path.endswith('.png') and any(part in path.split('/') for part in ('swing','idle','knight-a','knight-b'))),path
    write(OUT/'audit.json',{'pass':True,'gut_tests':count,'captures':evidence,'no_readback_runs':9,
        'mockup_checks':mockup['checks'],'protected_shared_files':protected,'rules_a9_unchanged':True,
        'scope_base':'b2f460b','changed_paths_checked':len(changed),
        'limits':['CPU particle counts are emitter-capacity upper bounds.','Dummy audio is not device audition.',
            'Human hit-feel HUMAN_PENDING; big-map option OWNER_PENDING.','Mockup is decorative, not a playable level.']})

    files = {PROJECT/'project.godot',REPO/'docs/tasks/godot-spike-03-hitfeel-bigmap.md'}
    for directory in ['scripts','config','scenes','shaders','tests','audio','tools']:
        files.update(p for p in (PROJECT/directory).rglob('*') if p.is_file() and p.suffix in TEXT)
    files.update([PROJECT/'docs/HANDOFF.md',PROJECT/'docs/VERIFICATION.md'])
    for directory in [OUT,REPO/'docs/proposals',REPO/'shared-anim',copied]:
        files.update(p for p in directory.rglob('*') if p.is_file() and p.suffix not in {'.import','.pyc'})
    files = {p for p in files if p.name not in {'source-hashes.json','audit-run.log','handoff-audit-run.log'}}
    hashes = []
    for path in sorted(files):
        raw = path.read_bytes()
        hashes.append({'path':path.relative_to(REPO).as_posix(),'sha256_working_tree':digest(raw),
            'sha256_git_lf':digest(raw.replace(b'\r\n',b'\n')) if path.suffix in TEXT else digest(raw)})
    write(OUT/'source-hashes.json',hashes)
    print(f'SPIKE03_AUDIT pass=true tests={count} protected={len(protected)} native_pngs={sum(x["native_pngs"] for x in evidence.values())} sources={len(hashes)}')

if __name__=='__main__': main()
