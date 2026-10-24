"""Independent offline verification of region confinement and native evidence."""
from prepare_a9_regions import *
from package_a3_evidence import chunks
from fix_a9_regions import delta_mask, technical
from PIL import ImageChops
from io import BytesIO
from collections import Counter
import re, struct, argparse

def read_log(name):
    raw=(OUT/name).read_bytes()
    return re.sub(r'\x1b\[[0-9;]*m','',raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'))

def alpha_components(im):
    pts={(x,y) for y in range(512) for x in range(512) if im.getpixel((x,y))[3]>127};components=[]
    while pts:
        seed=pts.pop();queue=[seed]
        for x,y in queue:
            for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if n in pts:pts.remove(n);queue.append(n)
        components.append(queue)
    return sorted(components,key=len,reverse=True)

def hashes():
    sources=[ROOT/'godot-spike/project.godot',ROOT/'godot-spike/docs/HANDOFF.md',ROOT/'godot-spike/docs/VERIFICATION.md',ROOT/'docs/tasks/godot-spike-02-a9-targeted-fix.md',ROOT/'docs/art-briefs/thoma-swing-commission.md']
    for folder in ['scripts','tests','tools','shaders','scenes']:
        sources += [p for p in (ROOT/'godot-spike'/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader','.tscn']]
    sources += [p for p in SHARED.rglob('*') if p.is_file() and p.suffix in ['.png','.json','.md'] and not any(q in ['tools','rejected'] for q in p.parts)]
    sources += [p for p in OUT.rglob('*') if p.is_file() and p.name!='source-hashes.json']
    text_suffixes=['.gd','.py','.gdshader','.tscn','.json','.md','.txt','.godot','.log']
    write(OUT/'source-hashes.json',[{'path':rel(p),'sha256_working_tree':sha(p),
      'sha256_git_lf':hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() if p.suffix in text_suffixes else sha(p)} for p in sorted(set(sources))])

def main():
    logs={n:read_log(n) for n in ['test-run.log','sync-run.log','import-run.log','w3-playback.log','rendered-run.log','rendered-1080p-run.log']}
    for name,text in logs.items():
        assert not any(t in text for t in ['SCRIPT ERROR:','ERROR:','GUT WARNING','ERR_CANT_OPEN','ERR_UNCONFIGURED']),name
    tests=int(re.search(r'Passing Tests\s+(\d+)',logs['test-run.log']).group(1))
    assertions=int(re.search(r'Asserts\s+(\d+)',logs['test-run.log']).group(1))
    assert tests>=71 and 'All tests passed!' in logs['test-run.log']
    assert 'CAPTURE_COMPLETE A9 movie=true runs=1 shots=0 pass=true' in logs['w3-playback.log']
    for path,digest in [('thoma/idle/01.png','c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808'),('thoma/swing/05.png','f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf')]:assert sha(SHARED/path)==digest
    assert load(SHARED/'manifest.json')==load(OUT/'baseline-a8/manifest.json')
    for r in load(OUT/'baseline-a8/hashes.json'):
        if r['path'].endswith('.png'):assert sha(ROOT/r['path'])==r['sha256']
    fixlog=load(OUT/'a9-fix-log.json');counts=Counter();outside_changes=0;operation_audit=[]
    assert list(fixlog['frames'])==ORDER
    for op in fixlog['operations']:
        counts[(op['frame'],op['region'])]+=1;assert not op['whole_frame_regeneration']
        for key in ['input','output','mask','permission_mask']:assert sha(ROOT/op[key])==op[key+'_sha256']
        source=OUT/op['source_anchor'] if op['source_anchor'].startswith('baseline-a8/') else OUT/f'baseline-a8/{Path(op["frame"]).name}' if '(baseline A8)' in op['source_anchor'] else SHARED/op['source_anchor']
        assert sha(source)==op['source_sha256']
        for t in op['transform']:
            if t.get('source_mask_sha256'):assert sha(ROOT/t['source_mask'])==t['source_mask_sha256']
        before=Image.open(ROOT/op['input']).convert('RGBA');after=Image.open(ROOT/op['output']).convert('RGBA')
        actual=delta_mask(before,after);mask=Image.open(ROOT/op['mask']).convert('L');permission=Image.open(ROOT/op['permission_mask']).convert('L')
        assert actual.size==(512,512) and mask.size==actual.size and permission.size==actual.size
        assert ImageChops.subtract(actual,mask).getbbox() is None,(op['frame'],op['region'],'unlogged changed pixel')
        assert ImageChops.subtract(actual,permission).getbbox() is None,(op['frame'],op['region'],'permission escape')
        assert sum(v>0 for v in permission.getdata())<512*512/2
        operation_audit.append({'frame':op['frame'],'region':op['region'],'attempt':op['attempt'],'outside_permission_pixels':0,'outside_recorded_mask_pixels':0,'kept':op['kept']})
    assert len(counts)==30 and max(counts.values())<=3
    live_checks={};component_report={}
    for f,row in fixlog['frames'].items():
        p=SHARED/f'thoma/swing/{f}.png';im=Image.open(p).convert('RGBA');baseline=Image.open(OUT/f'baseline-a8/{f}.png').convert('RGBA')
        assert sha(p)==row['sha256']==sha(ROOT/row['installed'])
        kept=Image.open(ROOT/row['kept_mask']).convert('L');assert sha(ROOT/row['kept_mask'])==row['kept_mask_sha256']
        assert ImageChops.subtract(delta_mask(baseline,im),kept).getbbox() is None
        reconstructed=baseline.copy()
        for op in fixlog['operations']:
            if op['frame']==f'thoma/swing/{f}.png' and op['kept']:reconstructed=Image.composite(Image.open(ROOT/op['output']),reconstructed,Image.open(ROOT/op['mask']))
        assert reconstructed.tobytes()==im.tobytes(),'Final cannot be reconstructed from kept regions'
        t=technical(im,f);assert 463<=t['bottom']<=465 and t['ground']>4 and t['mace_error']<=4 and t['contact_opaque']
        assert im.size==(512,512) and im.mode=='RGBA' and im.getpixel((0,0))[3]==0
        live_checks[f]=t
        comps=alpha_components(im);old=alpha_components(baseline)
        old_small={p for c in old if len(c)<8 for p in c}
        new_small={p for c in comps if len(c)<8 for p in c}
        assert not (new_small-old_small),(f,'newly isolated opaque alpha fragment')
        component_report[f]={'sha256':sha(p),'method':'4-neighbour connected components at alpha>127; tiny diagonal antialiasing clusters compared to exact A8, not an absolute halo detector',
          'final_components':[{'pixels':len(c),'bbox':[min(x for x,y in c),min(y for x,y in c),max(x for x,y in c),max(y for x,y in c)]} for c in comps],
          'unchanged_a8_tiny_pixels':[list(v) for v in sorted(new_small)],'new_tiny_pixels':[]}
    write(OUT/'alpha-components.json',component_report)
    parity=0
    for p in SHARED.rglob('*'):
        if not p.is_file() or p.suffix in ['.uid','.import'] or any(q in ['rejected','tools','__pycache__'] for q in p.parts):continue
        assert sha(p)==sha(ROOT/'godot-spike/art/anim-shared'/p.relative_to(SHARED)),p
        parity+=1
    timing_summaries=[]
    names=['swing-anticipation','swing-raised','swing-smear','contact','follow-through','recover']
    for suffix,size,log in [('',(1280,720),'rendered-run.log'),('-1080p',(1920,1080),'rendered-1080p-run.log')]:
        assert 'CAPTURE_COMPLETE A9 movie=false runs=6 shots=13 pass=true' in logs[log]
        timing=load(OUT/f'timing{suffix}.json');assert timing['complete'] and timing['resolution']==list(size)
        assert len(timing['runs'])==6 and len(timing['screenshots'])==13
        for run in timing['runs']:
            assert 0<run['wall_seconds']<=1.7 and run['hitstop_wall_ms']>=80 and run['hitstop_process_ms']>=80
            assert run['same_frame_contact'] and run['input_ready']
        shots={s['file']:s for s in timing['screenshots']}
        for prefix in ['', 'rendered-baseline-a8/']:
            for i,name in enumerate(names):
                file=prefix+name+suffix+'.png';assert shots[file]['frame']==i and Image.open(OUT/file).size==size
            assert shots[prefix+'contact'+suffix+'.png']['hold'] and shots[prefix+'contact'+suffix+'.png']['phase']=='contact'
        assert Image.open(OUT/('idle'+suffix+'.png')).size==size
        timing_summaries.append({'resolution':size,'runs':timing['runs']})
    avi=ROOT/'godot-spike/.godot/spike02-a9-movie/attack.avi';data=avi.read_bytes()
    assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
    header=struct.unpack_from('<14I',data,data.index(b'avih')+8)
    assert (header[8],header[9])==(1280,720) and 16665<=header[0]<=16667
    frames=[Image.open(BytesIO(p)).convert('RGB') for kind,p in chunks(data,12,len(data)) if kind in [b'00dc',b'00db']]
    assert len(frames)==header[4] and len(data)<8*1024*1024
    assert load(OUT/'playback-check.json')['source_movie_sha256']==sha(avi)
    movie_timing=load(OUT/'movie-timing.json');assert movie_timing['complete']
    phases={p['phase']:p['frame'] for p in movie_timing['runs'][0]['phases']}
    start,contact,resume,ready=[phases[k] for k in ['windup','contact','knockback','ready']]
    decoded=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
    assert len(set(decoded[contact:resume]))==1 and decoded[resume]!=decoded[contact]
    assert 0<(ready-start)/60<=1.7 and (resume-contact)/60>=.08
    shutil.copyfile(avi,OUT/'attack-60fps.avi')
    movie={'fps':60,'frames':len(frames),'bytes':len(data),'sha256':sha(avi),'strike_frame':start,'input_ready_frame':ready,'strike_to_ready_seconds':(ready-start)/60,
      'contact_frame':contact,'resume_frame':resume,'held_frames':list(range(contact,resume)),'hold_ms':(resume-contact)/60*1000,'decoded_rgb_hashes':decoded,'subsampled':False}
    write(OUT/'movie-index.json',movie)
    dest=OUT/'movie-samples';dest.mkdir(exist_ok=True)
    for i in [start,phases['lunge'],contact,resume-1,resume+6,ready]:frames[i].save(dest/f'frame{i:04}.png',optimize=True)
    (OUT/'MOVIE.md').write_text(f'''# A9 native60FPS capture

attack-60fps.avi is complete Godot --write-movie output at --fixed-fps60,
{len(frames)} frames,1280x720,{len(data):,} bytes. No transcoding/subsampling.
Same exact captured state as W3 flicker evidence; no duplicate capture needed.
Strike frame{start} -> input-ready{ready}: {(ready-start)/60:.6f}s.
Full decoded RGB is identical on contact frames{contact}-{resume-1}:
{movie['hold_ms']:.3f}ms hold; frame{resume} resumes. Every decoded RGB hash
is in movie-index.json. Six supplementary native samples in movie-samples/.

Encoding wall time is not attack latency. Normal/Reduced Motion real-time
runs at720p/1080p exclude screenshot readbacks and were run sequentially.
Dummy audio is not a hardware audition. Model art verdict remains FAIL,0/5;
human hit-feel HUMAN_PENDING, Owner approval pending. Not a full-battle claim.
''',encoding='utf-8')
    audit=load(SHARED/'frame-audit.json');middle=[r for r in audit if r['path'] in [f'thoma/swing/{i:02}.png' for i in range(5)]]
    assert len(middle)==5 and all(r['status']=='PLACEHOLDER' for r in middle)
    assert all(r['technical_check']['pass'] for r in middle)
    write(OUT/'evidence-audit.json',{'engineering_pass':True,'tests':tests,'assertions':assertions,'shared_files_byte_equal':parity,'operations':operation_audit,
      'attempt_counts':{f'{a}/{b}':n for (a,b),n in counts.items()},'max_attempts_per_region':max(counts.values()),'whole_frame_regenerations':0,'image_gen_calls':0,
      'final_live_technical':live_checks,'screenshots_720p':13,'screenshots_1080p':13,'timing_runs':timing_summaries,'movie':movie,
      'model_art_pass_frames':0,'model_placeholder_frames':5,'owner_art_approval':False,'human_playtest':'HUMAN_PENDING',
      'limits':['four donor faces improved;01 head trial rejected','costume/03 stance/04 feet repairs rejected for integration regression','hidden joints +/-12px; no strict4px certification','source IoU is not rendered RGB segmentation','no layered artist source or complete battle; commission fallback still needed']})
    hashes()
    print(f'A9_EVIDENCE integrity_pass=true tests={tests} asserts={assertions} operations={len(operation_audit)} max_attempts={max(counts.values())} parity={parity} shots=26 movie_frames={len(frames)} bytes={len(data)} art_pass=0/5')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--hashes-only',action='store_true');args=ap.parse_args()
    hashes() if args.hashes_only else main()
