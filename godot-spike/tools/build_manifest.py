"""Author the engine-neutral contract, not a runtime dependency."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2] / 'shared-anim'
def sequence(character, name, durations, **extra):
    return dict(character=character, frames=[dict(path=f'{character}/{name}/{i:02}.png', duration_ms=t) for i,t in enumerate(durations)], loop=False, **extra)
m = dict(version=1, characters={c: dict(canvas_size=[512,512], pivot=[256,464], reference_height_px=360, facing='right') for c in ['thoma','knight-a','knight-b']}, sequences={})
m['characters']['knight-a']['facing']='left'
m['characters']['knight-b']['facing']='left'
for c in m['characters']:
    m['sequences'][f'{c}.idle'] = sequence(c, 'idle', [100])
m['sequences']['thoma.swing'] = sequence('thoma','swing',[160,80,50,70,110,150], contact_frame_index=3, reduced_frame_indices=[0,3,5], reduced_duration_ms=100, events=[dict(frame=3,type=t,anchor=[480,180]) for t in ['spark','sfx']])
for f,offset in zip(m['sequences']['thoma.swing']['frames'],[[0,0],[40,70],[70,160],[100,220],[80,160],[0,0]]): f['offset']=offset
for c in ['knight-a','knight-b']:
    m['sequences'][f'{c}.hit'] = sequence(c,'hit',[90,130,140])
    m['sequences'][f'{c}.stagger'] = sequence(c,'stagger',[70,140,150],events=[dict(frame=1,type='dust',anchor=[256,460])])
m['impact'] = dict(hitstop_ms=80,shake=dict(strength_px=3.4,duration_ms=200,decay=2),flash_ms=35,knockback_ms=220,blocked_shove_ms=60,blocked_recoil_ms=160,blocked_shove_px=6,settle_ms=180,reduced_knockback_ms=30)
m['camera'] = dict(zoom=1.5,in_ms=240,out_ms=180,focus='attacker_target_midpoint',focus_weight=0.4)
m['scenarios'] = {k:dict(setup_index=i,reaction='hit' if i==0 else 'stagger',movement='knockback' if i==0 else 'knockback_blocked') for i,k in enumerate(['open','unit-blocked','terrain-blocked'])}
root.mkdir(exist_ok=True)
(root/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
positive = dict(type='integer',minimum=1)
point = dict(type='array',items=dict(type='number'),minItems=2,maxItems=2)
schema = {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Shared impact animation v1','type':'object','additionalProperties':False,'required':list(m),'properties':{
 'version':{'const':1},
 'characters':dict(type='object',minProperties=1,additionalProperties=dict(type='object',required=['canvas_size','pivot','reference_height_px','facing'],properties=dict(canvas_size=dict(type='array',items=positive,minItems=2,maxItems=2),pivot=point,reference_height_px=positive,facing={'enum':['left','right']}),additionalProperties=False)),
 'sequences':dict(type='object',minProperties=1,additionalProperties=dict(type='object',required=['character','frames','loop'],properties=dict(character=dict(type='string'),loop={'const':False},contact_frame_index=dict(type='integer',minimum=0),reduced_frame_indices=dict(type='array',items=dict(type='integer',minimum=0),minItems=1,uniqueItems=True),reduced_duration_ms=positive,frames=dict(type='array',minItems=1,items=dict(type='object',required=['path','duration_ms'],properties=dict(path=dict(type='string',pattern=r'^[a-z-]+/[a-z-]+/[0-9]{2}\.png$'),duration_ms=positive,offset=point),additionalProperties=False)),events=dict(type='array',items=dict(type='object',required=['frame','type','anchor'],properties=dict(frame=dict(type='integer',minimum=0),type={'enum':['sfx','spark','dust']},anchor=point),additionalProperties=False))),additionalProperties=False)),
 'impact':dict(type='object',required=list(m['impact']),properties={k:(dict(type='object',required=['strength_px','duration_ms','decay'],properties=dict(strength_px=dict(type='number',minimum=0),duration_ms=positive,decay=dict(type='number',minimum=0)),additionalProperties=False) if k=='shake' else positive) for k in m['impact']},additionalProperties=False),
 'camera':dict(type='object',required=list(m['camera']),properties=dict(zoom=dict(type='number',minimum=1,maximum=2),in_ms=positive,out_ms=positive,focus={'const':'attacker_target_midpoint'},focus_weight=dict(type='number',minimum=0,maximum=1)),additionalProperties=False),
 'scenarios':dict(type='object',required=list(m['scenarios']),additionalProperties=dict(type='object',required=['setup_index','reaction','movement'],properties=dict(setup_index=dict(type='integer',minimum=0,maximum=2),reaction={'enum':['hit','stagger']},movement={'enum':['knockback','knockback_blocked']}),additionalProperties=False))}}
(root/'manifest.schema.json').write_text(json.dumps(schema,indent=2)+'\n',encoding='utf-8')
