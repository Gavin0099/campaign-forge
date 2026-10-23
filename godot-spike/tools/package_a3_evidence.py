"""Validate real A3 outputs, extract native AVI frames, and package review evidence."""
from pathlib import Path
from PIL import Image, ImageDraw
from io import BytesIO
import hashlib, json, re, shutil, struct
REPO=Path(__file__).resolve().parents[2]
ROOT=REPO/'godot-spike'
SHARED=REPO/'shared-anim'
OUT=ROOT/'docs/evidence/spike02-a3'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def chunks(data,start,end):
    while start+8<=end:
        kind=data[start:start+4];size=struct.unpack_from('<I',data,start+4)[0]
        payload=start+8
        if kind in [b'LIST',b'RIFF']:
            yield from chunks(data,payload+4,min(payload+size,end))
        else:
            yield kind,data[payload:payload+size]
        start=payload+size+(size%2)

def main():
    for path in OUT.glob('*.log'):
        raw=path.read_bytes()
        text=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
        text=re.sub(r'\x1b\[[0-9;]*m','',text)
        path.write_text(text.replace('\r\n','\n').replace('\r','').rstrip()+'\n',encoding='utf-8',newline='\n')
    logs={p.name:p.read_text(encoding='utf-8') for p in OUT.glob('*.log')}
    assert 'Passing Tests        37' in logs['test-run.log'] and 'All tests passed!' in logs['test-run.log']
    for name in ['test-run.log','rendered-run.log','movie-run.log','readability-run.log','sync-run.log','import-run.log']:
        assert not any(token in logs[name] for token in ['SCRIPT ERROR:','ERROR:','GUT WARNING']),name
    assert 'CAPTURE_COMPLETE A3 movie=false runs=6 shots=13 pass=true' in logs['rendered-run.log']
    assert 'CAPTURE_COMPLETE A3 movie=true runs=1 shots=0 pass=true' in logs['movie-run.log']
    assert 'CAPTURE_COMPLETE A3 readability shots=12 pass=true' in logs['readability-run.log']
    timing=load(OUT/'timing.json');assert timing['complete'] and len(timing['runs'])==6
    for run in timing['runs']:
        assert 0<run['wall_seconds']<=1.7 and run['hitstop_wall_ms']>=80 and run['hitstop_process_ms']>=80
        assert run['same_frame_contact'] and run['input_ready']
    shots={row['file']:row for row in timing['screenshots']}
    names=['swing-anticipation.png','swing-raised.png','swing-smear.png','contact.png','follow-through.png','recover.png']
    for prefix in ['', 'rendered-baseline-a2/']:
        for i,name in enumerate(names):
            row=shots[prefix+name]
            assert row['frame']==i
            assert Image.open(OUT/(prefix+name)).size==(1280,720)
        assert shots[prefix+'contact.png']['hold'] and shots[prefix+'contact.png']['phase']=='contact'
    assert Image.open(OUT/'idle.png').size==(1280,720)
    # Exactly native-size crops of actual viewport readbacks, no asset compositing.
    box=(260,160,580,480)
    sheet=Image.new('RGB',(1920,710),(34,40,38));draw=ImageDraw.Draw(sheet)
    for row,prefix in enumerate(['rendered-baseline-a2/','']):
        top=row*355
        draw.text((8,top+5),'A2 rendered baseline' if row==0 else 'A3 rendered repaint',fill='#eee7d6')
        for i,name in enumerate(names):
            shot=Image.open(OUT/(prefix+name)).convert('RGB').crop(box)
            sheet.paste(shot,(i*320,top+20))
            draw.text((i*320+5,top+340),f'{i:02}: '+name.removesuffix('.png'),fill='#eee7d6')
    sheet.save(OUT/'contact-sheet-old-vs-new.png',optimize=True)
    write(OUT/'comparison-sheet.json',{'kind':'native-size crops from rendered 1280x720 viewport screenshots',
        'crop_xyxy':list(box),'resized':False,'source_rows':[[prefix+n for n in names] for prefix in ['rendered-baseline-a2/','']],
        'limits':'Separate real attacks at matching pose indices, so camera/tween sampling can vary slightly. Asset comparison at exactly fixed sprite scale is asset-sheet-old-vs-new.png.'})
    assert load(SHARED/'manifest.json')==load(OUT/'baseline-a2/manifest.json')
    parity=0
    for p in SHARED.rglob('*'):
        if not p.is_file() or 'rejected' in p.parts or 'tools' in p.parts or p.suffix in ['.uid','.import']:continue
        assert sha(p)==sha(ROOT/'art/anim-shared'/p.relative_to(SHARED)),p
        parity+=1
    source_originals=[]
    for local,source in {'battlefield.png':'ui-prototype/public/art/l03-p1v4/battlefield.png',
        'props.png':'ui-prototype/public/art/l03-p1v4/props.png','l03-party-v1.png':'ui-prototype/public/art/l03-party-v1.png',
        'l03-enemies-v1.png':'ui-prototype/public/art/l03-enemies-v1.png'}.items():
        assert sha(ROOT/'art'/local)==sha(REPO/source)
        source_originals.append({'local':'godot-spike/art/'+local,'original':source,'sha256':sha(REPO/source),'unchanged':True})
    write(OUT/'original-assets.json',source_originals)
    avi=ROOT/'.godot/spike02-a3-movie/attack.avi'
    data=avi.read_bytes();assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
    header=struct.unpack_from('<14I',data,data.index(b'avih')+8)
    payloads=[payload for kind,payload in chunks(data,12,len(data)) if kind in [b'00dc',b'00db']]
    assert (header[8],header[9])==(1280,720) and 16665<=header[0]<=16667
    assert len(payloads)==header[4] and len(data)<8*1024*1024
    movie=load(OUT/'movie-timing.json');assert movie['complete']
    run=movie['runs'][0];phases={p['phase']:p['frame'] for p in run['phases']}
    begin,contact,resume,ready=[phases[k] for k in ['windup','contact','knockback','ready']]
    assert 0<run['fixed_fps_seconds']<=1.7
    assert abs((ready-begin)/60-run['fixed_fps_seconds'])<1e-9
    frames=[Image.open(BytesIO(p)).convert('RGB') for p in payloads]
    hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
    assert len(set(hashes[contact:resume]))==1,'actual decoded movie hold is not frozen'
    assert hashes[resume]!=hashes[contact],'movie must visibly resume'
    assert (resume-contact)/60>=.08 and len(frames)>ready
    dest=OUT/'movie-samples';dest.mkdir(exist_ok=True)
    selected=[begin,phases['lunge'],contact,resume-1,resume+6,ready]
    for i in selected:frames[i].save(dest/f'frame{i:04}.png',optimize=True)
    shutil.copyfile(avi,OUT/'attack-60fps.avi')
    movie_info={'fps':60,'frames':len(frames),'bytes':len(data),'sha256':sha(avi),
        'strike_frame':begin,'input_ready_frame':ready,'strike_to_ready_seconds':(ready-begin)/60,
        'contact_frame':contact,'resume_frame':resume,'held_frames':list(range(contact,resume)),
        'hold_ms':(resume-contact)/60*1000,'decoded_rgb_hashes':hashes,'retained_png_frames':selected,
        'subsampled':False,'retention':'Full native Godot AVI below 8 MiB; six decoded PNG samples supplement it. No frames removed.'}
    write(OUT/'movie-index.json',movie_info)
    (OUT/'MOVIE.md').write_text(f'''# A3 native 60 FPS movie

`attack-60fps.avi` is Godot --write-movie output: {len(frames)} complete 1280x720 frames, {len(data):,} bytes. No subsampling or transcoding. Six PNGs in movie-samples are decoded supplementary frames.

Strike frame {begin} to input-ready frame {ready}: **{(ready-begin)/60:.6f} s**. Contact frames {contact}–{resume-1}: **{(resume-contact)/60*1000:.3f} ms**, with identical decoded full-frame RGB hashes. Frame {resume} visibly resumes. `movie-index.json` records every decoded frame hash and retained samples.

The engine's printed elapsed_wall_s includes offline movie encoding and is not gameplay latency. The fixed-60-fps timeline is the movie measurement; ordinary real-time runs are separately in timing.json. Audio-driver Dummy was used: no physical audio-device audition or human hit-feel verdict is claimed. Human playtest remains HUMAN_PENDING.
''',encoding='utf-8',newline='\n')
    sources=[ROOT/'project.godot']+[p for folder in ['scripts','tests','tools','shaders'] for p in (ROOT/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader']]
    sources += [SHARED/name for name in ['manifest.json','manifest.schema.json','frame-audit.json','a3-swing-prompts.json']]
    write(OUT/'source-hashes.json',[{'path':p.relative_to(REPO).as_posix(),'sha256_working_tree':sha(p),
        'sha256_git_lf':hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()} for p in sorted(sources)])
    report={'pass_result':True,'tests':37,'assertions':1162,'shared_files_byte_equal':parity,
        'new_runtime_screenshots':7,'rendered_baseline_screenshots':6,'knight_readability_screenshots':12,
        'original_png_parity':len(source_originals),'normal_seconds':[r['wall_seconds'] for r in timing['runs'] if not r['reduced_motion']],
        'reduced_seconds':[r['wall_seconds'] for r in timing['runs'] if r['reduced_motion']],
        'movie_seconds':movie_info['strike_to_ready_seconds'],'movie_hold_ms':movie_info['hold_ms'],
        'model_style_pass':2,'model_style_placeholder':5,'owner_art_approval':False,'human_playtest':'HUMAN_PENDING','P010':'PROPOSED'}
    write(OUT/'evidence-audit.json',report)
    print('A3_EVIDENCE_PACKAGE pass=true '+json.dumps(report))

if __name__=='__main__':main()
