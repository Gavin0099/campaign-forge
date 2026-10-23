import assert from 'node:assert/strict';
import fs from 'node:fs';
import { initialState, command, resolve } from '../src/playable-l03/rules.ts';
import { buildFeedbackTimeline, confirmedContactBlocker, stateBeforeEvent } from '../src/playable-l03/feedback.ts';

const events = [
  {type:'intent',unit:'knight-1',target:'winch',reason:'approach'},
  {type:'move',unit:'knight-1',path:[{x:1,y:8},{x:1,y:7},{x:1,y:6}]},
  {type:'intent',unit:'knight-2',target:'winch',reason:'blocked'},
  {type:'move',unit:'lace',path:[{x:1,y:3},{x:1,y:2}]},
  {type:'progress',delta:1,total:2},
  {type:'turn',completed:3},
];
const before = JSON.stringify(events), cues = buildFeedbackTimeline(events,230);
assert.deepEqual(cues.map(c=>[c.atMs,c.kind,c.eventIndex]),[
  [460,'landing',1],[460,'block',2],[690,'landing',3],[690,'winch',4],
]);
assert.deepEqual(cues.filter(c=>c.kind==='landing').map(c=>[c.unit,c.cell]),[
  ['knight-1',{x:1,y:6}],['lace',{x:1,y:2}],
]);
assert.equal(JSON.stringify(events),before);
assert.deepEqual(buildFeedbackTimeline([{type:'progress',delta:0,total:0}],230),[]);
assert.deepEqual(buildFeedbackTimeline([{type:'move',unit:'lace',path:[{x:1,y:3}]}],230),[]);
assert.throws(()=>buildFeedbackTimeline(events,0),/invalid-step-duration/);
console.log('PASS: timeline event order, every landing, progress after movement, zero-step and input purity');

const rows=fs.readFileSync(new URL('../docs/playable-l03-p0/success.jsonl',import.meta.url),'utf8').trim().split('\n').map(JSON.parse);
let state=initialState();
for(const row of rows.filter(r=>r.command).slice(0,6))state=command(state,row.command).state;
const resolution=resolve(state,state.turn),index=resolution.events.findIndex(e=>e.type==='intent' && e.reason==='blocked');
const atEvent=stateBeforeEvent(state,resolution.events,index),snapshot=JSON.stringify(atEvent);
assert.equal(confirmedContactBlocker(atEvent,'knight-2')?.id,'thoma');
assert.equal(JSON.stringify(atEvent),snapshot);
assert.deepEqual(atEvent.units.find(u=>u.id==='knight-1').cell,{x:0,y:0});
assert.deepEqual(state.units.find(u=>u.id==='knight-1').cell,{x:1,y:2});
const incidental={...initialState(),units:[
  {id:'knight-2',side:'enemy',alive:true,cell:{x:6,y:3}},
  {id:'lace',side:'ally',alive:true,cell:{x:6,y:2}},
]};
assert.equal(resolve(incidental,1).events[0].reason,'blocked');
assert.equal(confirmedContactBlocker(incidental,'knight-2'),undefined);
assert.equal(confirmedContactBlocker(initialState(),'knight-1'),undefined);
assert.equal(confirmedContactBlocker(atEvent,'missing'),undefined);
console.log('PASS: real counterfactual contact selects Thoma; incidental adjacency, open route and missing actor earn no spark; event snapshot is pure');
