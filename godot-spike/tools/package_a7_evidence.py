"""A7 evidence integrity/package, explicitly separate from failed art gates."""
from build_a7_spec import *
from PIL import ImageChops
from package_a3_evidence import chunks
from io import BytesIO
import re, struct, shutil

def main():
    logs={}
    for name in ['test-run.log','rendered-run.log','rendered-1080p-run.log','w3-playback.log','sync-run.log','import-run.log']:
      raw=(OUT/name).read_bytes();s=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
      s=re.sub(r'\x1b\[[0-9;]*m','',s);logs[name]=s
      assert not any(word in s for word in ['SCRIPT ERROR:','ERROR:','GUT WARNING']),name
    match=re.search(r'Passing Tests\s+(\d+)\s+Asserts\s+(\d+)',logs['test-run.log']);assert match
    tests,assertions=map(int,match.groups());assert tests>=55
    for name in ['rendered-run.log','rendered-1080p-run.log']:
      assert 'CAPTURE_COMPLETE A7 movie=false runs=6 shots=13 pass=true' in logs[name]
    assert 'CAPTURE_COMPLETE A7 movie=true runs=1 shots=0 pass=true' in logs['w3-playback.log']
    names=['swing-anticipation','swing-raised','swing-smear','contact','follow-through','recover']
    timing=[]
    for suffix,size in [('',(1280,720)),('-1080p',(1920,1080))]:
      t=load(OUT/f'timing{suffix}.json');timing.append(t)
      assert t['complete'] and len(t['runs'])==6 and t['resolution']==list(size)
      for run in t['runs']:
        assert 0<run['wall_seconds']<=1.7 and run['hitstop_wall_ms']>=80 and run['hitstop_process_ms']>=80
        assert run['same_frame_contact'] and run['input_ready']
      shots={r['file']:r for r in t['screenshots']}
      for prefix in ['', 'rendered-baseline-a6/']:
        for i,name in enumerate(names):
          file=prefix+name+suffix+'.png';assert shots[file]['frame']==i and Image.open(OUT/file).size==size
        assert shots[prefix+'contact'+suffix+'.png']['hold']
        assert shots[prefix+'contact'+suffix+'.png']['phase']=='contact'
      assert Image.open(OUT/('idle'+suffix+'.png')).size==size
    sheet=Image.new('RGB',(1920,710),(34,40,38));d=ImageDraw.Draw(sheet);box=(260,160,580,480)
    for row,prefix in enumerate(['rendered-baseline-a6/','']):
      y=row*355;d.text((8,y+4),'A6 actual rendered baseline' if row==0 else 'A7 actual rendered — five PLACEHOLDER, art FAIL',fill='white')
      for i,name in enumerate(names):
        sheet.paste(Image.open(OUT/(prefix+name+'.png')).convert('RGB').crop(box),(i*320,y+20));d.text((i*320+4,y+340),name,fill='white')
    sheet.save(OUT/'contact-sheet-a6-vs-a7.png',optimize=True)
    write(OUT/'comparison-sheet.json',{'kind':'same native320px crops of actual720p rendered replays, no resizing','crop':box,
      'rows':[['rendered-baseline-a6/'+n+'.png' for n in names],[n+'.png' for n in names]],'limits':'Resolution/crop identical; camera interpolation sampling varies between replay attacks. Asset comparison separately labelled.'})
    assets=Image.new('RGB',(7*512,1120),(34,40,38));d=ImageDraw.Draw(assets)
    paths=['idle-01.png']+[f'{i:02}.png' for i in range(6)]
    for row in [0,1]:
      d.text((8,row*560+5),'A6 BASELINE source512px' if row==0 else 'A7 source512px — model art FAIL',fill='white')
      for i,name in enumerate(paths):
        file=OUT/'baseline-a6'/name if row==0 else SHARED/('thoma/idle/01.png' if i==0 else 'thoma/swing/'+name)
        im=Image.open(file).convert('RGBA');assets.paste(im,(i*512,row*560+30),im)
    assets.save(OUT/'asset-sheet-a6-vs-a7.png',optimize=True)
    parity=0
    for p in SHARED.rglob('*'):
      if not p.is_file() or p.suffix in ['.uid','.import'] or any(q in ['rejected','tools','__pycache__'] for q in p.parts):continue
      assert sha(p)==sha(ROOT/'godot-spike/art/anim-shared'/p.relative_to(SHARED)),p
      parity+=1
    assert load(SHARED/'manifest.json')==load(OUT/'baseline-a6/manifest.json')
    originals=load(ROOT/'godot-spike/docs/evidence/spike02-a4/original-assets.json')
    for original in originals:assert sha(ROOT/original['local'])==original['sha256']
    write(OUT/'original-assets.json',originals)
    avi=ROOT/'godot-spike/.godot/spike02-a7-movie/attack.avi';data=avi.read_bytes()
    assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
    header=struct.unpack_from('<14I',data,data.index(b'avih')+8)
    assert (header[8],header[9])==(1280,720) and 16665<=header[0]<=16667
    frames=[Image.open(BytesIO(p)).convert('RGB') for kind,p in chunks(data,12,len(data)) if kind in [b'00dc',b'00db']]
    assert len(frames)==header[4]
    assert load(OUT/'playback-check.json')['source_movie_sha256']==sha(avi)
    t=load(OUT/'movie-timing.json');assert t['complete']
    phases={r['phase']:r['frame'] for r in t['runs'][0]['phases']}
    start,contact,resume,ready=[phases[k] for k in ['windup','contact','knockback','ready']]
    hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
    assert len(set(hashes[contact:resume]))==1 and hashes[resume]!=hashes[contact]
    assert 0<(ready-start)/60<=1.7 and (resume-contact)/60>=.08
    # The complete native movie is retained under ~8MB; no transcode/subsample.
    assert len(data)<8*1024*1024
    shutil.copyfile(avi,OUT/'attack-60fps.avi')
    samples=[start,phases['lunge'],contact,resume-1,resume+6,ready]
    (OUT/'movie-samples').mkdir(exist_ok=True)
    for i in samples:frames[i].save(OUT/f'movie-samples/frame{i:04}.png',optimize=True)
    info={'fps':60,'frames':len(frames),'bytes':len(data),'sha256':sha(avi),'strike_frame':start,'input_ready_frame':ready,
      'strike_to_ready_seconds':(ready-start)/60,'contact_frame':contact,'resume_frame':resume,'held_frames':list(range(contact,resume)),
      'hold_ms':(resume-contact)/60*1000,'decoded_rgb_hashes':hashes,'retained_png_frames':samples,'subsampled':False}
    write(OUT/'movie-index.json',info)
    (OUT/'MOVIE.md').write_text(f'''# A7 native60FPS capture

`attack-60fps.avi` is complete Godot `--write-movie` output at `--fixed-fps60`,
{len(frames)} frames,1280x720,{len(data):,} bytes. No subsampling/transcoding.
This is the same native movie used for W3 playback/trace/region measurements.

Strike frame{start} → input-ready{ready}: {(ready-start)/60:.6f}s.
Full decodedRGB is identical on contact frames{contact}–{resume-1}:
{(resume-contact)/60*1000:.3f}ms hold; frame{resume} resumes. Every decoded frame
hash is in movie-index.json; six supplementary PNGs in movie-samples/.

The movie-run wall time includes rendering/encoding and is NOT attack latency.
Normal and Reduced Motion real-time runs are in timing.json/timing-1080p.json,
with synchronous screenshot replays excluded. Dummy audio is not an audition
through physical speakers/headphones. GIF timing is quantized. Art FAIL;
human hit-feel remains HUMAN_PENDING, Owner art approval pending.
''',encoding='utf-8',newline='\n')
    records=load(SHARED/'a7-swing-prompts.json')
    for r in records:
      assert r['raw_sha256']==sha(ROOT/r['raw'])
      if r['adopted']:assert r['runtime_sha256']==sha(SHARED/r['frame'])
    sources=[ROOT/'godot-spike/project.godot']
    for folder in ['scripts','tests','tools','shaders','scenes']:
      sources += [p for p in (ROOT/'godot-spike'/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader','.tscn']]
    sources += [p for p in SHARED.rglob('*') if p.is_file() and p.suffix in ['.png','.json','.md'] and not any(q in ['tools','rejected'] for q in p.parts)]
    sources += [p for folder in ['attempts','baseline-a6','sequence-runtime'] for p in (OUT/folder).rglob('*') if p.is_file()]
    sources += [OUT/n for n in ['spec-crops.json','spec-check.json','geometry-check.json','landmark-deltas.json','playback-check.json','sequence-check.json','render-trace.json','frame-status-table.md','METHOD.md','W3-OBSERVATIONS.md']]
    text_suffixes=['.gd','.py','.gdshader','.tscn','.json','.md','.txt','.godot']
    write(OUT/'source-hashes.json',[{'path':p.relative_to(ROOT).as_posix(),'sha256_working_tree':sha(p),
       'sha256_git_lf':hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() if p.suffix in text_suffixes else sha(p)} for p in sorted(set(sources))])
    report={'engineering_pass':True,'tests':tests,'assertions':assertions,'shared_files_byte_equal':parity,'screenshots_720p':13,'screenshots_1080p':13,
      'timing_runs_per_resolution':6,'movie':info,'art_verdict':'FAIL','model_pass_reference_frames':2,'model_placeholder_motion_frames':5,
      'seam_regression':True,'failed_requirements':['seam-free anchor transfer','exact full face/hair silhouette','exact embroidery/fringe and stole drape','full joint/hand/feet pose-target compliance','continuous stable sequence'],
      'mace04_head_corrected':True,'owner_art_approval':False,'human_playtest':'HUMAN_PENDING','engine':'Owner accepted Godot, P010 unchanged','Phase B':'CANCELLED','React':'CANCELLED'}
    write(OUT/'evidence-audit.json',report)
    print(f'A7_EVIDENCE_PACKAGE integrity_pass=true tests={tests} asserts={assertions} parity={parity} screenshots=26 movie_frames={len(frames)} bytes={len(data)} art=FAIL')

if __name__=='__main__':main()
