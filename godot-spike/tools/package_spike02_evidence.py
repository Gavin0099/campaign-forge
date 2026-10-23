"""Validate and package actual write-movie files; no generated screenshot pixels."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil,struct

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/spike02'
RAW=ROOT/'.godot/spike02-movie'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')

timing=load(OUT/'timing.json')
assert timing['complete'] and len(timing['runs'])==6
for run in timing['runs']:
    assert run['wall_seconds']<=1.7 and run['game_seconds_including_nominal_hitstop']<=1.7
    assert 80<=run['hitstop_observed_wall_ms']<=107
    assert run['hitstop_observed_process_ms']>=80
    assert run['same_frame_contact']
shots={s['file']:s for s in timing['screenshots']}
required=['anticipation.png','contact.png','recoil.png','blocked-unit-stagger.png',
          'blocked-terrain-stagger.png','reduced-motion-contact.png','readability-option-a.png',
          'readability-option-b.png','knights-grayscale.png','hud-minimal.png','hud-debug.png']
for name in required:
    assert name in shots and Image.open(OUT/name).size==(1280,720)
for name in ['contact.png','reduced-motion-contact.png']:
    assert shots[name]['hold_active'] and shots[name]['attacker_frame']==3
for name in ['blocked-unit-stagger.png','blocked-terrain-stagger.png']:
    assert shots[name]['target_frame']==1, 'Must capture actual buckled pose'
comparison=load(OUT/'readability-overlap.json')
assert len(comparison)==12
for row in comparison:
    assert Image.open(OUT/row['file']).size==(1280,720)
    if row['option']=='a':
        assert row['opaque_overlap_px']['thoma/knight-2']==0
        assert row['opaque_overlap_px']['knight-1/knight-2']==0
assert any(row['option']=='b' and row['opaque_overlap_px']['knight-1/knight-2']>0 for row in comparison)
assert 'CAPTURE_COMPLETE readability shots=12 pass=true' in (OUT/'readability-run.log').read_text(encoding='utf-8-sig')

movie=load(OUT/'movie-timing.json');assert movie['complete']
run=movie['runs'][0];phases={p['phase']:p for p in run['phases']}
contact=phases['contact']['process_frame'];resume=phases['knockback']['process_frame']
begin=phases['windup']['process_frame'];ready=phases['ready']['process_frame']
frames=sorted(RAW.glob('frame????????.png'))
assert len(frames)>=ready+1
assert (ready-begin)/60<=1.7
assert (resume-contact)/60>=0.08
hashes=[dict(frame=i,sha256=sha(p),bytes=p.stat().st_size) for i,p in enumerate(frames)]
assert len({hashes[i]['sha256'] for i in range(contact,resume)})==1,'Whole rendered hold must be identical'
assert hashes[resume]['sha256']!=hashes[contact]['sha256'],'World must visibly resume'
selected=[begin,phases['lunge']['process_frame'],contact,resume-1,resume+6,ready]
destination=OUT/'movie-samples';destination.mkdir(exist_ok=True)
for i in selected:shutil.copyfile(frames[i],destination/frames[i].name)
assert sum(frames[i].stat().st_size for i in selected)<8*1024*1024

avi=RAW/'attack.avi';data=avi.read_bytes()
assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
header=data.index(b'avih')+8
values=struct.unpack_from('<14I',data,header)
avi_info=dict(bytes=len(data),sha256=sha(avi),microseconds_per_frame=values[0],
              frames=values[4],width=values[8],height=values[9])
assert avi_info['frames']>=50 and (avi_info['width'],avi_info['height'])==(1280,720)
assert 16665<=avi_info['microseconds_per_frame']<=16667
assert len(data)<8*1024*1024
assert load(OUT/'movie-avi-timing.json')['complete']
shutil.copyfile(avi,OUT/'attack-60fps.avi')
dump('movie-index.json',dict(fps=60,all_png_count=len(frames),raw_png_bytes=sum(p.stat().st_size for p in frames),
    retained_frames=selected,retained_png_bytes=sum(frames[i].stat().st_size for i in selected),
    strike_frame=begin,input_ready_frame=ready,strike_to_ready_seconds=(ready-begin)/60,
    contact_frame=contact,resume_frame=resume,identical_hold_frames=list(range(contact,resume)),
    quantized_hold_ms=(resume-contact)/60*1000,avi=avi_info,all_raw_png_hashes=hashes))

originals=[]
mapping={'battlefield.png':'ui-prototype/public/art/l03-p1v4/battlefield.png',
         'props.png':'ui-prototype/public/art/l03-p1v4/props.png',
         'l03-party-v1.png':'ui-prototype/public/art/l03-party-v1.png',
         'l03-enemies-v1.png':'ui-prototype/public/art/l03-enemies-v1.png'}
for name,source in mapping.items():
    a=sha(ROOT/'art'/name);b=sha(ROOT.parent/source);assert a==b
    originals.append(dict(godot='godot-spike/art/'+name,original=source,sha256=a,identical=True))
dump('original-assets.json',originals)

# Normalize PowerShell redirection encoding without changing log content.
for p in OUT.glob('*.log'):
    b=p.read_bytes();encoding='utf-16' if b.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'
    text=b.decode(encoding).replace('\r\n','\n').replace('\r','')
    text='\n'.join(line.rstrip() for line in text.splitlines())+'\n'
    p.write_text(text,encoding='utf-8',newline='\n')
assert not any(word in (OUT/'movie-run.log').read_text() for word in ['SCRIPT ERROR:','ERROR:'])
assert not any(word in (OUT/'movie-avi-run.log').read_text() for word in ['SCRIPT ERROR:','ERROR:'])
dump('evidence-audit.json',dict(pass_result=True,screenshots=len(required),
    original_assets_identical=len(originals),frozen_rendered_frames=resume-contact,
    native_avi=avi_info,scope='actual files and timing, not Owner playtest or art approval'))
source_paths=[ROOT/'project.godot',ROOT.parent/'shared-anim/manifest.json',ROOT.parent/'shared-anim/manifest.schema.json']
for folder in ['scripts','tests','tools','shaders']:
    source_paths += [p for p in (ROOT/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader']]
dump('source-hashes.json',[dict(path=p.relative_to(ROOT.parent).as_posix(),sha256_working_tree=sha(p),
    sha256_git_lf=hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()) for p in sorted(source_paths)])
print('EVIDENCE_PACKAGE_COMPLETE screenshots=11 movie_hold_frames=%d avi_bytes=%d pass=true' % (resume-contact,len(data)))
