"""Verify rendered A5 evidence and retain the actual native 60 FPS movie."""
from pathlib import Path
from PIL import Image, ImageDraw
from io import BytesIO
import hashlib, json, re, shutil, struct
from package_a3_evidence import chunks
from prepare_a5_frames import REPO, SHARED, OUT, sha, write

ROOT=REPO/'godot-spike'
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    for path in OUT.glob('*.log'):
        if path.name=='package-run.log':continue  # active shell redirect is locked on Windows
        raw=path.read_bytes();text=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
        text=re.sub(r'\x1b\[[0-9;]*m','',text)
        path.write_text('\n'.join(line.rstrip() for line in text.replace('\r\n','\n').replace('\r','').splitlines())+'\n',encoding='utf-8',newline='\n')
    logs={p.name:p.read_text(encoding='utf-8') for p in OUT.glob('*.log') if not p.name.startswith(('package-run','attempt-'))}
    assert 'Passing Tests        48' in logs['test-run.log'] and 'Asserts            2126' in logs['test-run.log']
    for name in ['test-run.log','rendered-run.log','rendered-1080p-run.log','movie-run.log','sync-run.log','import-run.log']:
        assert not any(t in logs[name] for t in ['SCRIPT ERROR:','ERROR:','GUT WARNING']),name
    for name in ['rendered-run.log','rendered-1080p-run.log']:
        assert 'CAPTURE_COMPLETE A5 movie=false runs=6 shots=13 pass=true' in logs[name]
    assert 'CAPTURE_COMPLETE A5 movie=true runs=1 shots=0 pass=true' in logs['movie-run.log']
    names=['swing-anticipation','swing-raised','swing-smear','contact','follow-through','recover']
    timings=[]
    for suffix,size in [('',(1280,720)),('-1080p',(1920,1080))]:
        timing=load(OUT/f'timing{suffix}.json');timings.append(timing)
        assert timing['complete'] and len(timing['runs'])==6 and tuple(timing['resolution'])==size
        for run in timing['runs']:
            assert 0<run['wall_seconds']<=1.7 and run['hitstop_wall_ms']>=80 and run['hitstop_process_ms']>=80
            assert run['same_frame_contact'] and run['input_ready']
        shots={s['file']:s for s in timing['screenshots']}
        for prefix in ['', 'rendered-baseline-a4/']:
            for i,name in enumerate(names):
                file=prefix+name+suffix+'.png';assert shots[file]['frame']==i
                assert Image.open(OUT/file).size==size
            contact=shots[prefix+'contact'+suffix+'.png'];assert contact['hold'] and contact['phase']=='contact'
        assert Image.open(OUT/('idle'+suffix+'.png')).size==size
    # Native pixel crops, not sprite composites. Observer camera sampling varies
    # slightly between real replay attacks; no zoom/rescale is applied here.
    box=(260,160,580,480)
    sheet=Image.new('RGB',(1920,710),(34,40,38));draw=ImageDraw.Draw(sheet)
    for row,prefix in enumerate(['rendered-baseline-a4/','']):
        top=row*355;draw.text((8,top+5),'A4 rendered baseline' if row==0 else 'A5 rendered reference transfer - PLACEHOLDER',fill='white')
        for i,name in enumerate(names):
            im=Image.open(OUT/(prefix+name+'.png')).convert('RGB').crop(box)
            sheet.paste(im,(i*320,top+20));draw.text((i*320+5,top+340),name,fill='white')
    sheet.save(OUT/'contact-sheet-a4-vs-a5.png',optimize=True)
    # Supplement the W3 source-pixel sheet with actual unscaled 720p render
    # crops. The source rows remain at their original 1:1 pixel scale.
    regions=Image.open(OUT/'region-check.png').convert('RGB')
    extended=Image.new('RGB',(regions.width,2065),(34,40,38))
    extended.paste(regions.crop((0,0,regions.width,1690)),(0,0))
    rd=ImageDraw.Draw(extended)
    rd.text((10,1700),'ACTUAL native 720p viewport crops (no resizing) | A5 posed replays; camera sampling differs slightly | W5',fill='white')
    for i,name in enumerate(['idle']+names):
        im=Image.open(OUT/(name+'.png')).convert('RGB').crop(box)
        extended.paste(im,(i*340,1725));rd.text((i*340+4,2048),name,fill='white')
    extended.save(OUT/'region-check.png',optimize=True)
    asset_sheet=Image.new('RGB',(1536,590),(34,40,38));asset_draw=ImageDraw.Draw(asset_sheet)
    for row in range(2):
        asset_draw.text((8,row*295+5),'A4 baseline ASSETS' if row==0 else 'A5 ASSETS - exactly equal sprite scale; not a game screenshot',fill='white')
        for i in range(6):
            path=OUT/f'baseline-a4/{i:02}.png' if row==0 else SHARED/f'thoma/swing/{i:02}.png'
            im=Image.open(path).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
            asset_sheet.paste(im,(i*256,row*295+25),im)
    asset_sheet.save(OUT/'asset-sheet-a4-vs-a5.png',optimize=True)
    write(OUT/'comparison-sheet.json',{'kind':'native unresized crops of actual rendered 1280x720 replays','crop':box,'source_rows':[[prefix+n+'.png' for n in names] for prefix in ['rendered-baseline-a4/','']],'limits':'Same resolution/crop and pose index; camera/tween sampling varies slightly across replays. Asset sequence strip is separate.'})
    parity=0
    for p in SHARED.rglob('*'):
        if not p.is_file() or any(part in ['rejected','tools','__pycache__'] for part in p.parts) or p.suffix in ['.uid','.import']:continue
        assert sha(p)==sha(ROOT/'art/anim-shared'/p.relative_to(SHARED)),p
        parity+=1
    assert load(SHARED/'manifest.json')==load(OUT/'baseline-a4/manifest.json')
    originals=load(ROOT/'docs/evidence/spike02-a4/original-assets.json')
    for original in originals:
        # Compare immutable hashes from A4; no React checkout/file access.
        assert sha(REPO/original['local'])==original['sha256']
    write(OUT/'original-assets.json',originals)
    avi=ROOT/'.godot/spike02-a5-movie/attack.avi';data=avi.read_bytes()
    assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
    header=struct.unpack_from('<14I',data,data.index(b'avih')+8)
    payloads=[payload for kind,payload in chunks(data,12,len(data)) if kind in [b'00dc',b'00db']]
    assert (header[8],header[9])==(1280,720) and 16665<=header[0]<=16667
    assert len(payloads)==header[4] and len(data)<8*1024*1024
    movie=load(OUT/'movie-timing.json');assert movie['complete'];run=movie['runs'][0]
    phases={p['phase']:p['frame'] for p in run['phases']}
    begin,contact,resume,ready=[phases[k] for k in ['windup','contact','knockback','ready']]
    assert 0<(ready-begin)/60<=1.7
    frames=[Image.open(BytesIO(p)).convert('RGB') for p in payloads]
    hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
    assert len(set(hashes[contact:resume]))==1 and hashes[resume]!=hashes[contact]
    assert (resume-contact)/60>=.08 and len(frames)>ready
    dest=OUT/'movie-samples';dest.mkdir(exist_ok=True)
    selected=[begin,phases['lunge'],contact,resume-1,resume+6,ready]
    for i in selected:frames[i].save(dest/f'frame{i:04}.png',optimize=True)
    shutil.copyfile(avi,OUT/'attack-60fps.avi')
    info={'fps':60,'frames':len(frames),'bytes':len(data),'sha256':sha(avi),'strike_frame':begin,'input_ready_frame':ready,
          'strike_to_ready_seconds':(ready-begin)/60,'contact_frame':contact,'resume_frame':resume,'held_frames':list(range(contact,resume)),
          'hold_ms':(resume-contact)/60*1000,'decoded_rgb_hashes':hashes,'retained_png_frames':selected,'subsampled':False}
    write(OUT/'movie-index.json',info)
    (OUT/'MOVIE.md').write_text(f'''# A5 native 60 FPS movie

`attack-60fps.avi` is complete Godot `--write-movie` output at `--fixed-fps 60`:
{len(frames)} frames at 1280x720, {len(data):,} bytes. Under 8 MiB; no frames
subsampled, transcoded or omitted. Six supplementary decoded PNG samples are
in movie-samples; every decoded frame hash is in movie-index.json.

Strike frame {begin} to input-ready frame {ready}: {(ready-begin)/60:.6f} seconds.
Contact frames {contact} through {resume-1} have identical full decoded RGB:
{(resume-contact)/60*1000:.3f} ms; frame {resume} visibly resumes.

Encoding wall time is not gameplay latency. Ordinary timing.json and
timing-1080p.json measure six no-readback runs each. Dummy audio is not a
physical-device audition. Human hit-feel playtest remains HUMAN_PENDING.
''',encoding='utf-8',newline='\n')
    sources=[ROOT/'project.godot']+[p for folder in ['scripts','tests','tools','shaders'] for p in (ROOT/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader']]
    sources += [p for p in SHARED.rglob('*') if p.is_file() and p.suffix in ['.png','.json','.md'] and not any(part in ['rejected','tools'] for part in p.parts)]
    sources += [OUT/'rig-controls.json',OUT/'scale-measurement.json',OUT/'frame-status-table.md',OUT/'sequence-check.json']
    sources += [p for folder in ['seam-masks','protected-masks','baseline-a4'] for p in (OUT/folder).iterdir() if p.is_file()]
    write(OUT/'source-hashes.json',[{'path':p.relative_to(REPO).as_posix(),'sha256_working_tree':sha(p),'sha256_git_lf':hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() if p.suffix!='.png' else sha(p)} for p in sorted(sources)])
    report={'engineering_pass':True,'art_completion':'PARTIAL','tests':48,'assertions':2126,'shared_files_byte_equal':parity,
        'screenshots_720p':13,'screenshots_1080p':13,'timing_runs_per_resolution':6,'movie':info,'model_pass_reference_frames':2,
        'model_placeholder_motion_frames':5,'owner_art_approval':False,'human_playtest':'HUMAN_PENDING','P010':'Owner update pending; not edited', 'owner_engine_decision':'Godot chosen 2026-10-24; Phase B CANCELLED'}
    write(OUT/'evidence-audit.json',report)
    print(f'A5_EVIDENCE_PACKAGE pass=true tests=48 parity={parity} screenshots=26 movie_frames={len(frames)} bytes={len(data)}')

if __name__=='__main__':main()
