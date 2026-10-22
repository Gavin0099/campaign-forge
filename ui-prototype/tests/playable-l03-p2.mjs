import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { initialState, command, resolve, key, walkable, MAP } from '../src/playable-l03/rules.ts';
import { variants, startFor, boundedMoves, reactionEvidence } from './playable-l03-p2-support.mjs';
import { replay, twoMoveSearch, turnOnePlacements } from './playable-l03-p0c-support.mjs';
const config = variants[0].config;
const start = () => startFor(config);
const intents = r => r.events.filter(e => e.type === 'enemy-intent');
let passed = 0;
function test(name, run) { run(); console.log(`PASS ${++passed}: ${name}`); }
function freeze(value) { if (value && typeof value === 'object') { Object.values(value).forEach(freeze); Object.freeze(value); } return value; }
function step(state) {
  const before = JSON.stringify(state);
  const r = resolve(freeze(state), state.turn);
  assert(r.ok); assert.equal(JSON.stringify(state), before);
  const events = r.events;
  for (const [i, e] of events.entries()) {
    if (e.type === 'enemy-intent') {
      assert(e.reason.length); assert(walkable(e.targetTile, state.route));
      assert(e.plannedPath.length >= 1 && e.plannedPath.length <= 4);
      if (e.action === 'move') assert.deepEqual(events[i + 1], { type: 'move', unit: e.unit, path: e.plannedPath });
      if (e.action === 'swap') assert.deepEqual(events[i + 1], { type: 'breakout', unit: e.unit, plan: e.plan });
      if (e.action === 'wait') assert(!['move', 'breakout'].includes(events[i + 1]?.type));
      if (e.intent === 'prepare-breakout') {
        assert.equal(e.action, 'wait'); assert.equal(e.plan.preparedTurn, state.turn);
        assert.deepEqual(e.targetTile, e.plan.from); assert.equal(e.targetAlly, e.plan.ally);
      }
    }
    if (e.type === 'move') {
      assert.equal(events[i - 1]?.action, 'move'); assert.equal(events[i - 1]?.unit, e.unit);
      for (let j = 1; j < e.path.length; j++) {
        assert(walkable(e.path[j], state.route));
        assert.equal(Math.abs(e.path[j].x-e.path[j-1].x)+Math.abs(e.path[j].y-e.path[j-1].y), 1);
      }
    }
    if (e.type === 'breakout') {
      assert.equal(events[i - 1]?.action, 'swap');
      assert.equal(state.enemyPressure[e.unit].stage, 'prepare-breakout');
      assert.deepEqual(e.plan, state.enemyPressure[e.unit].plan);
      assert.equal(e.plan.preparedTurn, state.turn - 1);
      assert.deepEqual(r.state.units.find(u => u.id === e.plan.ally).cell, e.plan.to);
    }
  }
  assert.equal(events.find(e => e.type === 'progress').delta, intents(r).filter(e => e.action === 'progress').length);
  assert.equal(new Set(r.state.units.filter(u => u.alive).map(u => key(u.cell))).size, r.state.units.filter(u => u.alive).length);
  assert(r.state.units.every(u => walkable(u.cell, state.route)));
  return r;
}
const prepared = () => step(step(start()).state).state;
test('opt-in only, validates threshold, default has no pressure data', () => {
  assert(!('enemyPressure' in initialState()));
  for (const value of [-1, 0.5, NaN, Infinity]) assert.throws(() => initialState('open', { ...config, detourThreshold: value }), /invalid-P2/);
  for (const value of [0, 1, 2, 10]) assert.doesNotThrow(() => initialState('open', { ...config, detourThreshold: value }));
});
test('detour pressure, blocked then prepare then exact no-damage swap on distinct phases', () => {
  const first = step(start()), second = step(first.state), third = step(second.state);
  const a = intents(first).find(e => e.unit === 'knight-1');
  assert.equal(a.intent, 'blocked'); assert.equal(a.reason, 'detour:2>1');
  assert.equal(intents(second).find(e => e.unit === 'knight-1').intent, 'prepare-breakout');
  assert(!second.events.some(e => e.type === 'breakout'));
  assert.deepEqual(third.events.find(e => e.type === 'breakout').plan, second.state.enemyPressure['knight-1'].plan);
  assert.deepEqual(third.state.units.map(u => [u.id, u.alive]), start().units.map(u => [u.id, u.alive]));
});
test('threshold is strict: equal detour uses ordinary target interference', () => {
  const r = step(startFor({ ...config, detourThreshold: 2 }));
  assert.equal(intents(r)[0].behaviour, 'target-interference');
  assert.equal(intents(r)[0].intent, 'approach');
  assert.deepEqual(intents(r)[0].targetTile, MAP.winch);
});
test('fully blocked is pressure even with high detour threshold', () => {
  const state = { ...startFor({ ...config, detourThreshold: 100 }), units: [
    { id: 'knight-1', side: 'enemy', alive: true, cell: { x: 0, y: 0 } },
    { id: 'karen', side: 'ally', alive: true, cell: { x: 1, y: 0 } },
    { id: 'lace', side: 'ally', alive: true, cell: { x: 0, y: 1 } },
  ] };
  const r = step(state);
  assert.equal(intents(r)[0].intent, 'blocked'); assert.equal(intents(r)[0].reason, 'direct-lane-blocked');
  step(step(r.state).state);
});
test('player vacates telegraphed cell: cancellation with reason and no swap', () => {
  const s = prepared();
  const moved = command(s, { type: 'move', turn: 3, unit: 'thoma', to: { x: 0, y: 4 } });
  assert(moved.ok);
  const r = step(moved.state);
  assert(intents(r).some(e => e.intent === 'cancel-breakout' && e.reason === 'target-moved-or-absent'));
  assert(!r.events.some(e => e.type === 'breakout'));
});
test('replacement blocker is re-planned, never surprise-swapped under old telegraph', () => {
  let s = prepared();
  s = command(s, { type: 'move', turn: 3, unit: 'thoma', to: { x: 0, y: 4 } }).state;
  const replacement = command(s, { type: 'move', turn: 3, unit: 'lace', to: { x: 1, y: 4 } });
  assert(replacement.ok);
  const r = step(replacement.state);
  assert(intents(r).some(e => e.intent === 'cancel-breakout'));
  assert(!r.events.some(e => e.type === 'breakout'));
  assert(!intents(r).some(e => e.intent === 'prepare-breakout'));
});
test('absent/dead target cancels and other knights remain obstacles', () => {
  const s = prepared();
  for (const units of [s.units.filter(u => u.id !== 'thoma'), s.units.map(u => u.id === 'thoma' ? { ...u, alive: false } : u)]) {
    const r = step({ ...s, units });
    assert(intents(r).some(e => e.reason === 'target-moved-or-absent'));
    assert(!r.events.some(e => e.type === 'breakout'));
  }
});
test('phase-start progress, immutable deterministic preview, terminal/stale guards, retry reset', () => {
  let s = start();
  while (s.status === 'playing') {
    const r = step(s); assert.deepEqual(resolve(s, s.turn), r);
    assert.equal(resolve(s, s.turn + 1).reason, 'stale-turn'); s = r.state;
  }
  assert.equal(s.status, 'failure'); assert.equal(resolve(s, s.turn).reason, 'battle-finished');
  const retry = command(s, { type: 'retry' }); assert(retry.ok); assert.deepEqual(retry.state, start());
});
test('deterministic placement sample: every intent/action matches, no overlap or surprise swap', () => {
  const placements = turnOnePlacements(start());
  for (let i = 0; i < placements.length; i += 31) {
    let state = placements[i].state;
    while (state.status === 'playing') state = step(state).state;
  }
});
test('copied P0d bounded harness matches independent P0c <=2 enumerator', () => {
  const actual = boundedMoves(start(), 2), other = twoMoveSearch(start());
  for (const field of ['wins', 'losses', 'strategies', 'minimumCostWin']) assert.deepEqual(actual[field], other[field]);
});
test('saved search witnesses and cheapest ties replay with matching intents/actions', () => {
  const report = JSON.parse(readFileSync(new URL('../docs/playable-l03-p2/search-results.json', import.meta.url)));
  for (const c of Object.values(report.cases)) for (const commands of c.cheapestCommands) {
    const trace = replay(commands, start()); assert(trace.legal); assert.equal(trace.state.status, 'success');
    let state = start();
    for (const record of trace.records.slice(1)) {
      const r = record.command.type === 'resolve' ? step(state) : command(state, record.command);
      assert.deepEqual(r.state, record.state); assert.deepEqual(r.events, record.events); state = r.state;
    }
  }
  if (report.keyGate) {
    assert.deepEqual(reactionEvidence(report.keyGate.commands, start()), report.keyGate);
    for (const commands of [report.keyGate.commands, report.keyGate.ignoredCommands]) {
      let state = start();
      while (state.status === 'playing') {
        for (const input of commands.filter(c => c.turn === state.turn)) {
          const r = command(state, input); assert(r.ok); state = r.state;
        }
        state = step(state).state;
      }
      assert.equal(state.status, commands === report.keyGate.commands ? 'success' : 'failure');
    }
  }
  else assert.equal(report.verdict, 'NO_REDECISION');
});
console.log(`${passed} tests passed`);
