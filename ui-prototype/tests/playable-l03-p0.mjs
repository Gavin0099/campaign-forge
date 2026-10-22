import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { MAP, DEFAULT_CONFIG, initialState, command, resolve, findPath, walkable, key, neighbors } from '../src/playable-l03/rules.ts';

const traceDir = new URL('../docs/playable-l03-p0/', import.meta.url);
const writeTraces = process.argv.includes('--write-traces');
let passed = 0;
function test(name, run) { run(); passed++; console.log(`PASS ${passed}: ${name}`); }
function freeze(value) {
  if (value && typeof value === 'object') { Object.freeze(value); Object.values(value).forEach(freeze); }
  return value;
}
function checked(state, input) {
  const before = structuredClone(state);
  freeze(state);
  const result = command(state, input);
  assert.deepEqual(state, before, 'input mutated');
  if (!result.ok) { assert.deepEqual(result.state, before); assert.deepEqual(result.events, []); }
  const living = result.state.units.filter(u => u.alive);
  assert.equal(new Set(living.map(u => key(u.cell))).size, living.length, 'overlap');
  living.forEach(u => assert.ok(walkable(u.cell, state.route), 'unit on invalid tile'));
  for (const event of result.events.filter(e => e.type === 'move')) {
    assert.ok(event.path.length <= 4);
    event.path.forEach(p => assert.ok(walkable(p, state.route)));
    event.path.slice(1).forEach((p, i) => assert.equal(
      Math.abs(p.x - event.path[i].x) + Math.abs(p.y - event.path[i].y), 1));
  }
  return result;
}
function flood(start, route) {
  const seen = new Set([key(start)]), queue = [start];
  for (let i = 0; i < queue.length; i++) for (const p of neighbors(queue[i])) {
    if (!walkable(p, route) || seen.has(key(p))) continue;
    seen.add(key(p)); queue.push(p);
  }
  return seen;
}
function runTrace(strategy, config = DEFAULT_CONFIG, startingState = initialState('open', config)) {
  let state = startingState;
  const records = [{ initial: state }];
  const apply = input => {
    const result = checked(state, input);
    assert.ok(result.ok, result.reason);
    state = result.state;
    records.push({ command: input, events: result.events, state });
  };
  for (let round = 1; state.status === 'playing' && round <= 5; round++) {
    const moves = strategy === 'hold' ? (round === 1 ? [
      ['lace', { x: 1, y: 1 }], ['thoma', { x: 2, y: 2 }], ['karen', { x: 3, y: 3 }],
    ] : round === 2 ? [['karen', { x: 3, y: 1 }]] : []) : [];
    moves.forEach(([unit, to]) => apply({ type: 'move', turn: state.turn, unit, to }));
    apply({ type: 'resolve', turn: state.turn });
  }
  assert.notEqual(state.status, 'playing', 'turn loop failed to settle');
  return { state, records };
}
const encode = records => records.map(r => JSON.stringify(r)).join('\n') + '\n';

test('AC1: fixed 11x9 map, west-bank winch, both route deployments and objectives reachable', () => {
  assert.equal(MAP.rows.length, 9); assert.ok(MAP.rows.every(r => r.length === 11));
  assert.deepEqual(MAP.winch, { x: 2, y: 1 });
  assert.deepEqual(initialState('open').units, initialState('sealed').units);
  for (const route of ['open', 'sealed']) {
    const state = initialState(route), occupied = state.units.map(u => key(u.cell));
    assert.equal(new Set(occupied).size, state.units.length);
    assert.ok(!occupied.includes(key(MAP.winch)) && !occupied.includes(key(MAP.wagon)));
    state.units.forEach(u => assert.ok(walkable(u.cell, route)));
    const reachable = flood(state.units[0].cell, route);
    state.units.forEach(u => assert.ok(reachable.has(key(u.cell))));
    assert.ok(reachable.has(key(MAP.winch)));
    for (const ally of state.units.filter(u => u.side === 'ally')) {
      assert.ok(ally.cell.x < 4);
      assert.ok(findPath(state, ally, MAP.winch), `${route} ${ally.id} winch`);
      if (route === 'sealed') assert.ok(findPath(state, ally, MAP.wagon), `${ally.id} wagon`);
    }
    if (route === 'sealed') {
      const wagonReach = flood(MAP.wagon, route);
      assert.ok(wagonReach.has(key(MAP.exit)));
      for (let x = 0; x <= 8; x++) assert.ok(walkable({ x, y: 4 }, route));
    } else {
      assert.ok(!reachable.has(key(MAP.wagon)), 'open river must stay separated');
      assert.ok(!walkable({ x: 4, y: 4 }, route) && !walkable({ x: 5, y: 4 }, route));
    }
  }
});
test('AC2: legal moves deterministic, one move per turn, rejected moves deep-equal', () => {
  const s = initialState(), move = { type: 'move', turn: 1, unit: 'karen', to: { x: 3, y: 3 } };
  const good = checked(s, move); assert.ok(good.ok);
  assert.deepEqual(good, checked(s, move));
  assert.equal(checked(good.state, { ...move, to: { x: 3, y: 2 } }).reason, 'already-moved');
  const invalid = [
    { x: -1, y: 5 }, { x: 11, y: 5 }, { x: 2, y: 9 }, { x: 2.5, y: 5 },
    { x: NaN, y: 5 }, { x: Infinity, y: 5 }, { x: 4, y: 5 },
    { x: 4, y: 4 }, { x: 2, y: 5 }, { x: 1, y: 4 }, { x: 0, y: 0 },
  ];
  invalid.forEach(to => assert.equal(checked(s, { ...move, to }).ok, false));
  for (const unit of ['missing', 'knight-1']) assert.equal(checked(s, { ...move, unit }).ok, false);
  assert.equal(checked(s, { ...move, turn: 0 }).reason, 'stale-turn');
});
test('AC2: single passage flag blocks living allies by default; never allows occupied endpoints or enemies', () => {
  const base = initialState('sealed');
  const corridor = { ...base, units: [
    { id: 'a', side: 'ally', alive: true, cell: { x: 3, y: 4 } },
    { id: 'b', side: 'ally', alive: true, cell: { x: 4, y: 4 } },
  ] };
  const move = { type: 'move', turn: 1, unit: 'a', to: { x: 6, y: 4 } };
  assert.equal(checked(corridor, move).ok, false);
  const pass = { ...corridor, config: { blockAlliedPassage: false } };
  assert.equal(checked(pass, move).ok, true);
  assert.equal(checked(pass, { ...move, to: { x: 4, y: 4 } }).ok, false);
  const enemy = { ...pass, units: pass.units.map(u => u.id === 'b' ? { ...u, side: 'enemy' } : u) };
  assert.equal(checked(enemy, move).ok, false);
  const dead = { ...corridor, units: corridor.units.map(u => u.id === 'b' ? { ...u, alive: false } : u) };
  assert.equal(checked(dead, move).ok, true);
});
test('AC3: resolve synchronously settles one turn; stale and finished resolutions rejected', () => {
  const s = freeze(initialState()), result = resolve(s, 1);
  assert.equal(result.ok, true); assert.equal(result.state.turn, 2);
  assert.equal(typeof result.then, 'undefined');
  assert.deepEqual(result, resolve(s, 1));
  assert.equal(checked(result.state, { type: 'resolve', turn: 1 }).reason, 'stale-turn');
  const finished = runTrace('idle').state;
  assert.equal(checked(finished, { type: 'resolve', turn: finished.turn }).reason, 'battle-finished');
  assert.equal(checked(initialState('sealed'), { type: 'resolve', turn: 1 }).reason, 'sealed-map-only-in-P0');
  const source = readFileSync(new URL('../src/playable-l03/rules.ts', import.meta.url), 'utf8');
  assert.doesNotMatch(source, /\b(React|setTimeout|setInterval|requestAnimationFrame|Date|Math\.random)\b/);
});
test('AC4: interference progresses only after arrival; failure takes precedence on turn five', () => {
  const s = initialState();
  const adjacent = { ...s, units: s.units.map(u => u.id === 'knight-1' ? { ...u, cell: { x: 2, y: 2 } } : u) };
  assert.equal(resolve(adjacent, 1).state.progress, 1);
  assert.equal(resolve(s, 1).state.progress, 0);
  assert.equal(resolve({ ...adjacent, turn: 5, progress: 2 }, 5).state.status, 'failure');
  const crowded = { ...s, units: [s.units[3], ...neighbors(MAP.winch).map((cell, i) =>
    ({ id: `guard-${i}`, side: 'ally', alive: true, cell }))] };
  assert.ok(resolve(crowded, 1).events.some(e => e.type === 'intent' && e.reason === 'blocked'));
});
const success = runTrace('hold'), failure = runTrace('idle');
test('AC4/5: hold succeeds, standing still fails, default blocking ON remains solvable', () => {
  assert.equal(DEFAULT_CONFIG.blockAlliedPassage, true);
  assert.equal(success.state.status, 'success'); assert.equal(failure.state.status, 'failure');
  assert.ok(failure.state.progress >= 3); assert.ok(success.state.progress < failure.state.progress);
  assert.deepEqual(success, runTrace('hold', { blockAlliedPassage: true }));
  assert.equal(runTrace('hold', { blockAlliedPassage: false }).state.status, 'success');
  assert.deepEqual(failure, runTrace('idle'));
});
const retryResult = checked(failure.state, { type: 'retry' });
const retry = runTrace('hold', DEFAULT_CONFIG, retryResult.state);
test('AC5: retry clears terminal state, progress and moves; changing strategy wins', () => {
  assert.ok(retryResult.ok); assert.deepEqual(retryResult.state, initialState());
  assert.equal(retry.state.status, 'success');
  assert.equal(checked(initialState(), { type: 'retry' }).reason, 'battle-not-finished');
  const afterSuccess = checked(success.state, { type: 'retry' });
  assert.deepEqual(afterSuccess.state, initialState());
  const alternative = runTrace('hold', DEFAULT_CONFIG, checked(runTrace('idle').state, { type: 'retry' }).state);
  assert.deepEqual(retry, alternative);
});
test('AC5: committed success, failure and retry traces match byte for byte', () => {
  const traces = {
    success: success.records, failure: failure.records,
    retry: [{ previous: failure.state, command: { type: 'retry' }, ...retryResult }, ...retry.records],
  };
  if (writeTraces) mkdirSync(traceDir, { recursive: true });
  for (const [name, records] of Object.entries(traces)) {
    const path = new URL(`${name}.jsonl`, traceDir), bytes = encode(records);
    if (writeTraces) writeFileSync(path, bytes);
    assert.equal(readFileSync(path, 'utf8'), bytes, fileURLToPath(path));
  }
});
console.log(`${passed} tests passed; hold=${success.state.status} progress=${success.state.progress}, idle=${failure.state.status} progress=${failure.state.progress}`);
