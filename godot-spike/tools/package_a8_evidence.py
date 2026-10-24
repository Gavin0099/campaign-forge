"""Verify A8 evidence integrity independently of its failed art acceptance."""
from prepare_a8_sheet import ROOT, SHARED, OUT, sha, write
from a8_style_check import load, PATHS, CHECKS
from package_a3_evidence import chunks
from PIL import Image
from io import BytesIO
import hashlib
import struct
import re
import shutil

def main():
    logs={}
    for name in ['test-run.log','sync-run.log','import-run.log','rendered-run.log','rendered-1080p-run.log','w3-playback.log']:
        raw=(OUT/name).read_bytes();text=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
        logs[name]=re.sub(r'\x1b\[[0-9;]*m','',text)
        assert not any(token in logs[name] for token in ['SCRIPT ERROR:','ERROR:','GUT WARNING']),name
    match=re.search(r'Passing Tests\s+(\d+)\s+Asserts\s+(\d+)',logs['test-run.log']);assert match
    tests,assertions=map(int,match.groups());assert tests>=63 and 'All tests passed!' in logs['test-run.log']
    assert 'CAPTURE_COMPLETE A8 movie=true runs=1 shots=0 pass=true' in logs['w3-playback.log']
    timings=[]
    names=['swing-anticipation','swing-raised','swing-smear','contact','follow-through','recover']
    for suffix,size,log in [('',(1280,720),'rendered-run.log'),('-1080p',(1920,1080),'rendered-1080p-run.log')]:
        assert 'CAPTURE_COMPLETE A8 movie=false runs=6 shots=13 pass=true' in logs[log]
        timing=load(OUT/f'timing{suffix}.json');assert timing['complete'] and timing['resolution']==list(size)
        assert len(timing['runs'])==6 and len(timing['screenshots'])==13
        for run in timing['runs']:
            assert 0<run['wall_seconds']<=1.7 and run['hitstop_wall_ms']>=80 and run['hitstop_process_ms']>=80
            assert run['same_frame_contact'] and run['input_ready']
        shots={r['file']:r for r in timing['screenshots']}
        for prefix in ['', 'rendered-baseline-a7/']:
            for i,name in enumerate(names):
                file=prefix+name+suffix+'.png';assert shots[file]['frame']==i and Image.open(OUT/file).size==size
            assert shots[prefix+'contact'+suffix+'.png']['hold'] and shots[prefix+'contact'+suffix+'.png']['phase']=='contact'
        assert Image.open(OUT/('idle'+suffix+'.png')).size==size
        timings.append(timing)
    parity=0
    for p in SHARED.rglob('*'):
        if not p.is_file() or p.suffix in ['.uid','.import'] or any(q in ['rejected','tools','__pycache__'] for q in p.parts):continue
        assert sha(p)==sha(ROOT/'godot-spike/art/anim-shared'/p.relative_to(SHARED)),p
        parity+=1
    assert load(SHARED/'manifest.json')==load(OUT/'baseline-a7/manifest.json')
    fixed={'thoma/idle/01.png':'c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808',
           'thoma/swing/05.png':'f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf'}
    for path,digest in fixed.items():assert sha(SHARED/path)==digest
    provenance=load(SHARED/'a8-swing-prompts.json');assert 1<=len(provenance['sheet_attempts'])<=4
    for attempt in provenance['sheet_attempts']:
        assert sha(ROOT/attempt['raw'])==attempt['raw_sha256']
        for ref in attempt['inputs']:assert sha(ROOT/ref['path'])==ref['sha256']
    for r in provenance['frames']:
        assert sha(SHARED/r['frame'])==r['runtime_sha256']==sha(ROOT/r['runtime'])
        for fix in r['local_fixes']:
            for key in ['input','output','mask']:assert sha(ROOT/fix[key])==fix[key+'_sha256']
    # Independently measure final PNG occupancy, including shaft/antialiasing,
    # rather than report only the transformed donor's intended placement.
    centres=[]
    for i,target in enumerate([(192,85),(259,87),(449,110),(455,196),(421,376)]):
        path=SHARED/f'thoma/swing/{i:02}.png';im=Image.open(path).convert('RGBA')
        points=[(x,y) for y in range(target[1]-18,target[1]+19) for x in range(target[0]-18,target[0]+19) if im.getpixel((x,y))[3]>229]
        centre=[sum(p[k] for p in points)/len(points) for k in range(2)]
        error=sum((a-b)**2 for a,b in zip(centre,target))**.5
        assert error<=4 and len(points)>150
        if i==3:assert im.getpixel((455,196))[3]>229
        centres.append({'frame':f'thoma/swing/{i:02}.png','sha256':sha(path),'measured':[round(v,4) for v in centre],
           'target':list(target),'error_px':round(error,4),'within4':True,'opaque_pixels':len(points),
           'method':'Independent final-PNG alpha>0.9 centroid in37x37 head ROI; includes small haft overlap, not a pose/design acceptance'})
    write(OUT/'final-mace-centres.json',centres)
    assert not provenance['fallback_edits']
    for item in load(OUT/'baseline-a7/hashes.json'):
        if item['path'].endswith('.png'):assert sha(ROOT/item['path'])==item['sha256']
    avi=ROOT/'godot-spike/.godot/spike02-a8-movie/attack.avi';data=avi.read_bytes()
    assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
    header=struct.unpack_from('<14I',data,data.index(b'avih')+8)
    assert (header[8],header[9])==(1280,720) and 16665<=header[0]<=16667
    frames=[Image.open(BytesIO(p)).convert('RGB') for kind,p in chunks(data,12,len(data)) if kind in [b'00dc',b'00db']]
    assert len(frames)==header[4] and len(data)<8*1024*1024
    assert load(OUT/'playback-check.json')['source_movie_sha256']==sha(avi)
    timing=load(OUT/'movie-timing.json');assert timing['complete']
    phases={p['phase']:p['frame'] for p in timing['runs'][0]['phases']}
    start,contact,resume,ready=[phases[k] for k in ['windup','contact','knockback','ready']]
    hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
    assert len(set(hashes[contact:resume]))==1 and hashes[resume]!=hashes[contact]
    assert 0<(ready-start)/60<=1.7 and (resume-contact)/60>=.08
    shutil.copyfile(avi,OUT/'attack-60fps.avi')
    samples=[start,phases['lunge'],contact,resume-1,resume+6,ready]
    (OUT/'movie-samples').mkdir(exist_ok=True)
    for i in samples:frames[i].save(OUT/f'movie-samples/frame{i:04}.png',optimize=True)
    movie={'fps':60,'frames':len(frames),'bytes':len(data),'sha256':sha(avi),'strike_frame':start,'input_ready_frame':ready,
           'strike_to_ready_seconds':(ready-start)/60,'contact_frame':contact,'resume_frame':resume,
           'held_frames':list(range(contact,resume)),'hold_ms':(resume-contact)/60*1000,'decoded_rgb_hashes':hashes,'subsampled':False}
    write(OUT/'movie-index.json',movie)
    (OUT/'MOVIE.md').write_text(f'''# A8 native60FPS capture

`attack-60fps.avi` is complete Godot `--write-movie` output at `--fixed-fps60`,
{len(frames)} frames,1280×720,{len(data):,} bytes. No subsampling/transcoding.
It is the same successful native movie decoded for W3 flicker measurements.
The initial failed writer run is excluded and retained in w3-playback-failed-1.log.

Strike frame{start} → input-ready{ready}: {(ready-start)/60:.6f}s.
Full decodedRGB is identical on contact frames{contact}–{resume-1}:
{movie['hold_ms']:.3f}ms hold; frame{resume} resumes. Every decoded frame hash
is in movie-index.json; six supplementary PNGs are in movie-samples/.

Movie-run wall time includes encoding/rendering and is not attack latency.
Normal and Reduced Motion real-time timing uses six no-readback runs per
resolution; screenshot replays are excluded. Dummy audio is not a physical
audition. GIF quantizes60FPS timing. Art FAIL,0/5; human feel HUMAN_PENDING,
Owner art approval pending. No complete-battle or commercial-quality claim.
''',encoding='utf-8',newline='\n')
    audit=load(SHARED/'frame-audit.json');motion=[r for r in audit if r['path'] in PATHS[1:6]]
    assert len(motion)==5 and all(r['status']=='PLACEHOLDER' for r in motion)
    assert all(r['technical_check']['pass'] for r in motion)
    write(OUT/'evidence-audit.json',{'engineering_pass':True,'tests':tests,'assertions':assertions,'shared_files_byte_equal':parity,
       'screenshots_720p':13,'screenshots_1080p':13,'timing_runs_per_resolution':6,'movie':movie,
       'sheet_attempts':len(provenance['sheet_attempts']),'selected_attempt':provenance['selected_attempt'],'fallback_used':False,
       'art_verdict':'FAIL','model_pass_reference_frames':2,'model_placeholder_motion_frames':5,'owner_art_approval':False,'human_playtest':'HUMAN_PENDING',
       'limits':['prompt-only mask; generated anchors repainted, runtime originals unchanged','manual hidden-joint estimates cannot certify4px compliance',
                 'head centres validated, weapon brush/length still FAIL','source alpha IoU is not rendered segmentation','full3-5min battle outside isolated attack-spike scope']})
    sources=[ROOT/'godot-spike/project.godot']
    for folder in ['scripts','tests','tools','shaders','scenes']:
        sources += [p for p in (ROOT/'godot-spike'/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader','.tscn']]
    sources += [p for p in SHARED.rglob('*') if p.is_file() and p.suffix in ['.png','.json','.md'] and not any(q in ['tools','rejected'] for q in p.parts)]
    sources += [p for p in OUT.rglob('*') if p.is_file() and p.name!='source-hashes.json']
    text_suffixes=['.gd','.py','.gdshader','.tscn','.json','.md','.txt','.godot','.log']
    write(OUT/'source-hashes.json',[{'path':p.relative_to(ROOT).as_posix(),'sha256_working_tree':sha(p),
       'sha256_git_lf':hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() if p.suffix in text_suffixes else sha(p)} for p in sorted(set(sources))])
    print(f'A8_EVIDENCE integrity_pass=true tests={tests} asserts={assertions} parity={parity} shots=26 movie_frames={len(frames)} bytes={len(data)} art=FAIL')

if __name__=='__main__':main()
