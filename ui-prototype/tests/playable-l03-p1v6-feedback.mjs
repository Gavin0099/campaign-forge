import assert from 'node:assert/strict';
import { buildFeedbackTimeline } from '../src/playable-l03/feedback.ts';

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
