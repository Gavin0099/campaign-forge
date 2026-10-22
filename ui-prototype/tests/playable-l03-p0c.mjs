import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { MAP, DEFAULT_CONFIG, initialState, command, resolve, findPath } from '../src/playable-l03/rules.ts';
import { variants, startFor, replay, stateKey } from './playable-l03-p0c-support.mjs';

let passed = 0;
function test(name, fn) { fn(); console.log(`PASS ${++passed}: ${name}`); }
const fixture = (options, held = true) => {
  const base = startFor(options);
  return { ...base, units: [{ id: 'lace', side: 'ally', alive: true,
    cell: held ? { x: 1, y: 1 } : { x: 1, y: 3 } }] };
};
const finish = start => { let s = start; while (s.status === 'playing') s = resolve(s, s.turn).state; return s; };

test('experiments omitted by default; empty options serialize exactly as defaults', () => {
  assert.deepEqual(DEFAULT_CONFIG, { blockAlliedPassage: true });
  assert.equal(JSON.stringify(initialState()), JSON.stringify(initialState('open', { blockAlliedPassage: true })));
  assert.equal('p0c' in initialState().config, false);
  assert.equal('holdStreak' in finish(initialState()), false);
  assert.equal(finish(initialState()).status, 'failure');
  const neutral = initialState('open', { ...DEFAULT_CONFIG, p0c: {} });
  const ordinary = initialState();
  const { p0c, ...config } = neutral.config;
  assert.deepEqual({ ...neutral, config }, ordinary);
});
test('A survives through turn six, threshold loss still takes precedence', () => {
  let s = fixture({ survivalTurns: 6 });
  for (let t = 1; t <= 5; t++) { s = resolve(s, s.turn).state; assert.equal(s.status, 'playing'); }
  assert.equal(s.turn, 6);
  assert.equal(resolve(s, 6).state.status, 'success');
  const e = { id: 'knight', side: 'enemy', alive: true, cell: { x: 2, y: 0 } };
  s = { ...s, progress: 2, units: [...s.units, e] };
  assert.equal(resolve(s, 6).state.status, 'failure');
});
test('B checks final adjacency; early holding alone fails, final arrival passes', () => {
  const early = fixture({ requiredHoldTurns: 1 });
  let s = resolve(early, 1).state;
  s = { ...s, units: s.units.map(u => ({ ...u, cell: { x: 1, y: 3 } })) };
  assert.equal(finish(s).status, 'failure');
  s = fixture({ requiredHoldTurns: 1 }, false);
  for (let t = 1; t < 5; t++) s = resolve(s, s.turn).state;
  s = command(s, { type: 'move', turn: 5, unit: 'lace', to: { x: 1, y: 1 } }).state;
  const end = resolve(s, 5).state;
  assert.equal(end.status, 'success'); assert.equal(end.holdStreak, 1);
});
test('B+ N=2/3 require each last turn, reset on gaps, not total hold count', () => {
  for (const n of [2, 3]) {
    let s = fixture({ requiredHoldTurns: n });
    s = resolve(s, 1).state; assert.equal(s.holdStreak, 1);
    s = { ...s, units: s.units.map(u => ({ ...u, cell: { x: 1, y: 3 } })) };
    s = resolve(s, 2).state; assert.equal(s.holdStreak, 0);
    // Arrive on turn 4; only the last two ends are held.
    s = resolve(s, 3).state;
    s = command(s, { type: 'move', turn: 4, unit: 'lace', to: { x: 1, y: 1 } }).state;
    const end = finish(s);
    assert.equal(end.holdStreak, 2); assert.equal(end.status, n === 2 ? 'success' : 'failure');
    assert.equal(finish(fixture({ requiredHoldTurns: n })).status, 'success');
  }
});
test('only living companions count; progress must stay below three even during hold', () => {
  let s = fixture({ requiredHoldTurns: 2 });
  s = { ...s, turn: 5, holdStreak: 4, progress: 2,
    units: [...s.units, { id: 'knight', side: 'enemy', alive: true, cell: { x: 2, y: 0 } }] };
  const result = resolve(s, 5);
  assert.equal(result.state.progress, 3); assert.equal(result.state.status, 'failure');
  assert.equal(result.state.holdStreak, 0);
  s = fixture({ requiredHoldTurns: 1 });
  assert.equal(finish({ ...s, units: s.units.map(u => ({ ...u, alive: false })) }).status, 'failure');
  assert.notEqual(stateKey({ ...s, holdStreak: 1 }), stateKey({ ...s, holdStreak: 2 }));
});
test('C only changes Thoma spawn, is reachable, retry preserves experiments and resets history', () => {
  const s = startFor({ thomaStartsWest: true, requiredHoldTurns: 2 });
  const actor = s.units.find(u => u.id === 'thoma');
  assert.deepEqual(actor.cell, { x: 0, y: 4 }); assert.ok(findPath(s, actor, MAP.winch));
  assert.deepEqual(initialState().units.find(u => u.id === 'thoma').cell, { x: 1, y: 4 });
  const end = finish(s), result = command(end, { type: 'retry' });
  assert.ok(result.ok); assert.deepEqual(result.state, s); assert.equal(result.state.holdStreak, 0);
});
test('invalid horizon/hold parameters fail immediately', () => {
  for (const p0c of [{ survivalTurns: 4 }, { survivalTurns: 7 }, { requiredHoldTurns: -1 },
    { requiredHoldTurns: 1.5 }, { requiredHoldTurns: NaN }, { requiredHoldTurns: 6 }])
    assert.throws(() => initialState('open', { ...DEFAULT_CONFIG, p0c }), /invalid-P0c-config/);
});

const dir = new URL('../docs/playable-l03-p0c/', import.meta.url);
const report = JSON.parse(readFileSync(new URL('search-results.json', dir), 'utf8'));
const traces = [];
test('every reported solo/duo and multi-move witness legally replays at stated cost and bounds', () => {
  function check(w, start, label, bounds) {
    if (!w) return;
    const result = replay(w.commands, start); assert.ok(result.legal, label);
    assert.equal(result.state.status, 'success', label);
    const moves = result.records.filter(r => r.command?.type === 'move');
    const actual = { moves: moves.length, units: new Set(moves.map(r => r.command.unit)).size,
      tiles: moves.reduce((n, r) => n + r.events[0].path.length - 1, 0) };
    for (const k of ['moves', 'units', 'tiles']) assert.equal(actual[k], w[k], `${label} ${k}`);
    assert.equal(result.state.progress, w.progress, label);
    if (bounds) {
      assert.ok(w.commands.length <= bounds.maxMovesTotal);
      for (let t = 1; t <= bounds.survivalTurns; t++)
        assert.ok(w.commands.filter(c => c.turn === t).length <= bounds.maxMovesPerTurn);
      assert.equal(result.state.turn, bounds.survivalTurns);
      traces.push({ label, records: result.records });
    }
  }
  for (const row of report.results) {
    check(row.turnOneThenWait.minimumCostWin, startFor(row.options), `${row.name} T1`);
    check(row.atMostOneMove.minimumCostWin, startFor(row.options), `${row.name} one`);
    for (const l of row.lineups) {
      assert.equal(l.witness.found, !!l.witness.witness);
      check(l.witness.witness, startFor(row.options, l.party), `${row.name} ${l.party}`);
    }
    for (const m of row.multiMove) {
      const start = startFor({ ...row.options, survivalTurns: m.bounds.survivalTurns });
      check(m.minimumCostWin, start, `${row.name}/${m.bounds.survivalTurns} cheapest`, m.bounds);
      check(m.latestRequiredArrivalWin, start, `${row.name}/${m.bounds.survivalTurns} late`, m.bounds);
    }
  }
});
test('all variants stay opt-in and originals remain repeatable; P0c traces are byte-identical', () => {
  assert.deepEqual(report.results.map(r => r.name), variants.map(v => v.name));
  const text = traces.map(t => JSON.stringify(t)).join('\n') + '\n';
  const file = new URL('multi-move-witnesses.jsonl', dir);
  if (process.argv.includes('--write-traces')) writeFileSync(file, text);
  else assert.equal(readFileSync(file, 'utf8'), text);
});
console.log(`${passed} P0c tests passed`);
