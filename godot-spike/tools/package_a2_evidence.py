"""Validate actual A2 artifacts, source parity and native Godot movie output."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil,struct
import jsonschema
root=Path(__file__).resolve().parents[1];repo=root.parent
out=root/'docs/evidence/spike02-a2';raw=root/'.godot/spike02-a2-movie'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(name,obj):(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in out.glob('*.log'):
 b=p.read_bytes();t=b.decode('utf-16' if b.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
 p.write_text('\n'.join(line.rstrip() for line in t.replace('\r\n','\n').replace('\r','').splitlines())+'\n',encoding='utf-8',newline='\n')
timing=load(out/'timing.json');assert timing['complete'] and len(timing['runs'])==6
test_log=(out/'test-run.log').read_text()
assert 'Passing Tests        33' in test_log and 'All tests passed!' in test_log
assert not any(x in test_log for x in ['SCRIPT ERROR:','ERROR:','GUT WARNING']), 'test summaries alone do not prove clean execution'
for run in timing['runs']:
 assert 0<run['wall_seconds']<=1.7 and run['hitstop_wall_ms']>=80 and run['hitstop_process_ms']>=80
 assert run['same_frame_contact']
shots={s['file']:s for s in timing['screenshots']}
names=['default-view.png','selected-unit.png','attack-forecast.png','forecast-blocked-unit.png',
 'forecast-blocked-terrain.png','contact.png','blocked-stagger.png','help-overlay.png','debug-f1.png']
for name in names:
 assert name in shots and Image.open(out/name).size==(1280,720)
assert shots['contact.png']['hold'] and shots['contact.png']['attacker_frame']==3
assert shots['blocked-stagger.png']['target_frame']==1
for name in names[2:5]:assert shots[name]['phase']=='ready' and shots[name]['forecast_visible']
assert not shots['default-view.png']['debug_visible'] and not shots['default-view.png']['help_visible']
assert shots['help-overlay.png']['help_visible'] and shots['debug-f1.png']['debug_visible']
assert 'CAPTURE_COMPLETE A2 movie=false runs=6 shots=9 pass=true' in (out/'rendered-run.log').read_text()
overlap=load(out/'readability-overlap.json');assert len(overlap)==9
for row in overlap:
 assert Image.open(out/row['file']).size==(1280,720)
 assert row['opaque_overlap_px']['thoma/knight-2']==0
 assert row['opaque_overlap_px']['knight-1/knight-2']==0
 if row['phase']=='ready':assert row['opaque_overlap_px']['thoma/knight-1']==0
assert 'CAPTURE_COMPLETE A2 readability shots=9 pass=true' in (out/'readability-run.log').read_text()
contrast=load(out/'contrast.json');assert contrast['all_normal_AA'] and all(p['ratio']>=4.5 for p in contrast['pairs'])
schema=load(repo/'shared-anim/manifest.schema.json');manifest=load(repo/'shared-anim/manifest.json')
jsonschema.Draft202012Validator.check_schema(schema);jsonschema.validate(manifest,schema)
print('JSON_SCHEMA_VALIDATION pass=true')
for p in (repo/'shared-anim').rglob('*'):
 if not p.is_file() or 'rejected' in p.parts or p.suffix in ['.import','.uid']:continue
 assert sha(p)==sha(root/'art/anim-shared'/p.relative_to(repo/'shared-anim')),str(p)
shutil.copyfile(repo/'shared-anim/thoma-weapon-style-check.png',out/'thoma-weapon-style-check.png')
movie=load(out/'movie-png-timing.json');assert movie['complete']
run=movie['runs'][0];phases={p['phase']:p['frame'] for p in run['phases']}
contact,resume=phases['contact'],phases['knockback'];begin,ready=phases['windup'],phases['ready']
frames=sorted(raw.glob('frame????????.png'));assert len(frames)>ready
assert (ready-begin)/60<=1.7 and (resume-contact)/60>=.08
hashes=[dict(frame=i,sha256=sha(p),bytes=p.stat().st_size) for i,p in enumerate(frames)]
assert len({hashes[i]['sha256'] for i in range(contact,resume)})==1,'complete rendered hold must be identical'
assert hashes[resume]['sha256']!=hashes[contact]['sha256'],'must visibly resume'
selected=[begin,phases['lunge'],contact,resume-1,resume+6,ready]
dest=out/'movie-samples';dest.mkdir(exist_ok=True)
for i in selected:shutil.copyfile(frames[i],dest/frames[i].name)
avi=raw/'attack.avi';data=avi.read_bytes();assert data[:4]==b'RIFF' and data[8:12]==b'AVI '
header=struct.unpack_from('<14I',data,data.index(b'avih')+8)
avi_info=dict(bytes=len(data),sha256=sha(avi),microseconds_per_frame=header[0],frames=header[4],width=header[8],height=header[9])
assert avi_info['frames']>=ready and (avi_info['width'],avi_info['height'])==(1280,720)
assert 16665<=avi_info['microseconds_per_frame']<=16667 and len(data)<8*1024*1024
assert load(out/'movie-avi-timing.json')['complete']
shutil.copyfile(avi,out/'attack-60fps.avi')
dump('movie-index.json',dict(fps=60,strike_frame=begin,input_ready_frame=ready,strike_to_ready_seconds=(ready-begin)/60,
 contact_frame=contact,resume_frame=resume,identical_hold_frames=list(range(contact,resume)),hold_ms=(resume-contact)/60*1000,
 all_png_count=len(frames),raw_png_bytes=sum(p.stat().st_size for p in frames),all_png_hashes=hashes,
 retained_png_frames=selected,retained_png_bytes=sum(frames[i].stat().st_size for i in selected),avi=avi_info))
for name in ['movie-png-run.log','movie-avi-run.log']:
 t=(out/name).read_text();assert 'CAPTURE_COMPLETE A2 movie=true runs=1 shots=0 pass=true' in t
 assert not any(x in t for x in ['SCRIPT ERROR:','ERROR:'])
assert Image.open(out/'overview-1080.png').size==(1920,1080)
assert 'CAPTURE_COMPLETE A2 overview=1920x1080 pass=true' in (out/'overview-run.log').read_text()
originals=[]
mapping={'battlefield.png':'ui-prototype/public/art/l03-p1v4/battlefield.png','props.png':'ui-prototype/public/art/l03-p1v4/props.png',
 'l03-party-v1.png':'ui-prototype/public/art/l03-party-v1.png','l03-enemies-v1.png':'ui-prototype/public/art/l03-enemies-v1.png'}
for name,source in mapping.items():
 assert sha(root/'art'/name)==sha(repo/source)
 originals.append(dict(local='godot-spike/art/'+name,original=source,sha256=sha(root/'art'/name),unchanged=True))
dump('original-assets.json',originals)
sources=[root/'project.godot',repo/'shared-anim/manifest.json',repo/'shared-anim/manifest.schema.json']
for folder in ['scripts','tests','tools','shaders']:
 sources += [p for p in (root/folder).rglob('*') if p.suffix in ['.gd','.py','.gdshader']]
dump('source-hashes.json',[dict(path=p.relative_to(repo).as_posix(),sha256_working_tree=sha(p),sha256_git_lf=hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()) for p in sorted(sources)])
dump('evidence-audit.json',dict(pass_result=True,hud_screenshots=len(names),readability_screenshots=len(overlap),
 original_assets_unchanged=len(originals),minimum_text_contrast=min(p['ratio'] for p in contrast['pairs']),
 normal_seconds=[r['wall_seconds'] for r in timing['runs'] if not r['reduced_motion']],
 reduced_seconds=[r['wall_seconds'] for r in timing['runs'] if r['reduced_motion']],
 frozen_movie_frames=resume-contact,movie_strike_seconds=(ready-begin)/60,avi=avi_info,
 scope='Actual pixels/files/schema/parity/timing; not human playtest, equipment confirmation or Owner art approval'))
print('EVIDENCE_PACKAGE_COMPLETE A2 screenshots=18 movie_hold_frames=%d avi_bytes=%d pass=true' % (resume-contact,len(data)))
