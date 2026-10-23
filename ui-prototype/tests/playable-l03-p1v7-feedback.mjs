import assert from 'node:assert/strict';
import { blockedAtEventIndex } from '../src/playable-l03/feedback.ts';

const events = [
  {type:'intent',unit:'knight-1',target:'winch',reason:'approach'},
  {type:'move',unit:'knight-1',path:[{x:1,y:8},{x:1,y:7}]},
  {type:'intent',unit:'knight-2',target:'winch',reason:'blocked'},
  {type:'intent',unit:'knight-3',target:'winch',reason:'blocked'},
  {type:'progress',delta:0,total:0},
];
const snapshot = JSON.stringify(events);
assert.deepEqual([...blockedAtEventIndex(events,-1)],[]);
assert.deepEqual([...blockedAtEventIndex(events,0)],[]);
assert.deepEqual([...blockedAtEventIndex(events,1)],[]);
console.log('PASS: no blocked marker before its intent, including during an earlier enemy move');
assert.deepEqual([...blockedAtEventIndex(events,2)],['knight-2']);
assert.deepEqual([...blockedAtEventIndex(events,3)],['knight-2','knight-3']);
assert.deepEqual([...blockedAtEventIndex(events,4)],['knight-2','knight-3']);
console.log('PASS: blocked intents appear inclusively and accumulate independently for several enemies');
assert.deepEqual([...blockedAtEventIndex([],10)],[]);
blockedAtEventIndex(events,3).clear();
assert.deepEqual([...blockedAtEventIndex(events,3)],['knight-2','knight-3']);
assert.equal(JSON.stringify(events),snapshot);
console.log('PASS: helper leaves events intact and returns an independent set');
