import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { MAP, initialState, resolve, findPath, walkable, key } from '../src/playable-l03/rules.ts';
import { runPlan } from './playable-l03-p0b-support.mjs';

const write = process.argv.includes('--write-traces');
const dir = new URL('../docs/playable-l03-p0b/', import.meta.url);
let passed = 0;
function test(name, run) { run(); console.log(`PASS ${++passed}: ${name}`); }
function trace(name, value) {
  const text = value.map(v => JSON.stringify(v)).join('\n') + '\n';
  if (write) { mkdirSync(dir, { recursive: true }); writeFileSync(new URL(`${name}.jsonl`, dir), text); }
  else assert.equal(readFileSync(new URL(`${name}.jsonl`, dir), 'utf8'), text, `${name} drift`);
}
test('bounds: both routes reject every rectangle edge and inherited negative rows', () => {
  for (const route of ['open', 'sealed']) {
    for (let y = -1; y <= MAP.rows.length; y++) for (let x = -1; x <= MAP.rows[0].length; x++) {
      if (x < 0 || y < 0 || x >= 11 || y >= 9) assert.equal(walkable({ x, y }, route), false);
    }
    for (const x of [NaN, Infinity, -Infinity, 0.5]) assert.equal(walkable({ x, y: 1 }, route), false);
    for (const y of [NaN, Infinity, -Infinity, 0.5]) assert.equal(walkable({ x: 1, y }, route), false);
    assert.equal(walkable({ x: 0, y: 0 }, route), true);
    assert.equal(walkable({ x: 10, y: 8 }, route), true);
    assert.equal(walkable({ x: 4, y: 3 }, route), false);
    assert.equal(walkable({ x: 4, y: 4 }, route), route === 'sealed');
  }
  const previous = Object.getOwnPropertyDescriptor(Array.prototype, '-1');
  try {
    Object.defineProperty(Array.prototype, '-1', { value: '...........', configurable: true });
    assert.equal(walkable({ x: 0, y: -1 }, 'open'), false, 'negative y must not resolve inherited row');
  } finally {
    if (previous) Object.defineProperty(Array.prototype, '-1', previous);
    else delete Array.prototype[-1];
  }
});
const stances = [
  ['current-hold', { 1: [['lace', 1, 1], ['thoma', 2, 2], ['karen', 3, 3]], 2: [['karen', 3, 1]] }],
  ['north-partial', { 1: [['lace', 1, 1]] }],
  ['south-choke', { 1: [['karen', 3, 3]] }],
  ['lace-retreat-t2', { 2: [['lace', 0, 3]] }],
  ['lace-choke-t1', { 1: [['lace', 3, 4]] }],
];
for (const [name, plan] of stances) test(`stance ${name}: deterministic five-turn trace`, () => {
  const value = runPlan(plan);
  assert.deepEqual(value, runPlan(plan));
  const expected = { 'current-hold': ['success', 1], 'north-partial': ['failure', 3],
    'south-choke': ['failure', 3], 'lace-retreat-t2': ['success', 2], 'lace-choke-t1': ['success', 2] }[name];
  assert.deepEqual([value.state.status, value.state.progress], expected);
  for (const r of value.records) {
    const units = (r.state ?? r.initial).units.filter(u => u.alive);
    assert.equal(new Set(units.map(u => key(u.cell))).size, units.length);
    units.forEach(u => assert.ok(walkable(u.cell, 'open')));
  }
  trace(name, value.records);
  console.log(JSON.stringify({ stance: name, outcome: value.state.status, progress: value.state.progress,
    intents: value.records.filter(r => r.command?.type === 'resolve').map(r => ({ turn: r.command.turn,
      enemies: r.events.filter(e => e.type === 'intent').map(e => [e.unit, e.reason]),
      positions: r.state.units.filter(u => u.side === 'enemy').map(u => [u.id, u.cell]) })) }));
});
const unit = (id, side, x, y) => ({ id, side, alive: true, cell: { x, y } });
function fixture(units) { return { ...initialState(), units }; }
test('equal BFS paths use N/W/E/S; equal target lengths keep N/W/E/S target order', () => {
  const enemy = unit('e', 'enemy', 1, 3), state = fixture([enemy]);
  assert.deepEqual(findPath(state, enemy, { x: 2, y: 2 }), [{ x: 1, y: 3 }, { x: 1, y: 2 }, { x: 2, y: 2 }]);
  const result = resolve(state, 1);
  assert.deepEqual(result.state.units[0].cell, { x: 1, y: 1 }, 'W target wins equal cost over S target');
  const north = fixture([unit('e', 'enemy', 0, 0)]);
  assert.deepEqual(resolve(north, 1).state.units[0].cell, { x: 2, y: 0 }, 'N target wins equal cost over W target');
  trace('equal-ties', [{ initial: state, result }, { initial: north, result: resolve(north, 1) }]);
});
test('same target contention, blocked fallback and move-order identity effects', () => {
  // Only S is empty; first enemy reaches it, second has no remaining target.
  const guards = [unit('n', 'ally', 2, 0), unit('w', 'ally', 1, 1), unit('e', 'ally', 3, 1)];
  const a = unit('a', 'enemy', 1, 3), b = unit('b', 'enemy', 3, 3);
  const rows = [];
  for (const enemies of [[a, b], [b, a]]) {
    const state = fixture([...guards, ...enemies]), result = resolve(state, 1);
    assert.deepEqual(result, resolve(state, 1));
    assert.deepEqual(result.events.filter(e => e.type === 'intent').map(e => [e.unit, e.reason]),
      [[enemies[0].id, 'approach'], [enemies[1].id, 'blocked']]);
    assert.deepEqual(result.state.units.find(u => u.id === enemies[0].id).cell, { x: 2, y: 2 });
    assert.deepEqual(result.state.units.find(u => u.id === enemies[1].id).cell, enemies[1].cell);
    assert.equal(result.state.progress, 0, 'arrival is not a phase-start contribution');
    assert.equal(resolve(result.state, 2).state.progress, 1);
    rows.push({ initial: state, result });
  }
  trace('contention-order', rows);
});
test('all solo/duo search witnesses replay with absent allies removed', () => {
  const report = JSON.parse(readFileSync(new URL('search-results.json', dir), 'utf8'));
  for (const lineup of report.lineups) {
    assert.equal(lineup.witness.found, true);
    assert.equal(lineup.witness.truncated, false);
    const base = initialState();
    const start = { ...base, units: base.units.filter(u => u.side === 'enemy' || lineup.party.includes(u.id)) };
    const plan = {};
    for (const c of lineup.witness.commands) (plan[c.turn] ??= []).push([c.unit, c.to.x, c.to.y]);
    const result = runPlan(plan, start);
    assert.equal(result.state.status, 'success');
    assert.equal(result.state.progress, lineup.witness.progress);
    trace(`lineup-${lineup.party.join('-')}`, result.records);
  }
});
console.log(`${passed} P0b tests passed`);
