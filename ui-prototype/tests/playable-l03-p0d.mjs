import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { initialState, DEFAULT_CONFIG, resolve, command, key, walkable } from '../src/playable-l03/rules.ts';
import { replay, twoMoveSearch } from './playable-l03-p0c-support.mjs';
import { variants, startFor, stateKey, familyKey, boundedMoves, costOrder } from './playable-l03-p0d-support.mjs';

let passed = 0;
const test = (name, run) => { run(); console.log(`PASS ${++passed}: ${name}`); };
const unit = (id, side, x, y, alive = true) => ({ id, side, alive, cell: { x, y } });
const guards = () => [unit('n', 'ally', 2, 0), unit('w', 'ally', 1, 1),
  unit('e', 'ally', 3, 1), unit('s', 'ally', 2, 2)];
const fixture = (threshold = 2) => ({ ...initialState('open', { ...DEFAULT_CONFIG,
  p0d: { blockedTurnsBeforeBreakout: threshold } }), units: [...guards(), unit('a', 'enemy', 1, 3)] });
function freeze(o) { Object.freeze(o); for (const v of Object.values(o)) if (v && typeof v === 'object') freeze(v); return o; }
function valid(state) {
  const living = state.units.filter(u => u.alive);
  assert.equal(new Set(living.map(u => key(u.cell))).size, living.length, 'no overlap');
  living.forEach(u => assert.ok(walkable(u.cell, state.route), `${u.id} on legal terrain`));
}

test('D is absent by default; positive safe integer threshold only', () => {
  assert.deepEqual(DEFAULT_CONFIG, { blockAlliedPassage: true });
  assert.equal('p0d' in initialState().config, false);
  assert.equal('blockedTurns' in initialState(), false);
  assert.equal('blockedTurns' in resolve(initialState(), 1).state, false);
  for (const n of [0, -1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1, undefined])
    assert.throws(() => initialState('open', { ...DEFAULT_CONFIG, p0d: { blockedTurnsBeforeBreakout: n } }), /invalid-P0d-config/);
  for (const n of [1, 2, 3, 20]) assert.deepEqual(fixture(n).blockedTurns, {});
});
test('second consecutive blocked phase swaps first ally on deterministic W-before-S path', () => {
  const s = freeze(fixture()), first = resolve(s, 1);
  assert.equal(first.state.blockedTurns.a, 1);
  assert.equal(first.events.some(e => e.type === 'breakout'), false);
  assert.deepEqual(first.state.units, s.units);
  const second = resolve(freeze(first.state), 2);
  const event = second.events.find(e => e.type === 'breakout');
  assert.deepEqual(event, { type: 'breakout', unit: 'a', blockedTurns: 2,
    path: [{ x: 1, y: 3 }, { x: 1, y: 2 }, { x: 1, y: 1 }],
    swapped: { unit: 'w', from: { x: 1, y: 1 }, to: { x: 1, y: 2 } } });
  assert.equal(second.state.blockedTurns.a, 0);
  assert.equal(second.state.progress, 0, 'arrival does not contribute this phase');
  assert.equal(resolve(second.state, 3).state.progress, 1);
  valid(second.state);
  assert.deepEqual(second, resolve(first.state, 2));
});
test('threshold parameter and consecutive reset; contributor resets blocked counter', () => {
  let s = fixture(3);
  for (let t = 1; t <= 2; t++) { const r = resolve(s, t); assert.ok(!r.events.some(e => e.type === 'breakout')); s = r.state; }
  assert.ok(resolve(s, 3).events.some(e => e.type === 'breakout'));
  s = resolve(fixture(), 1).state;
  s = { ...s, units: s.units.filter(u => u.id !== 'w') };
  s = resolve(s, 2).state;
  assert.equal(s.blockedTurns.a, 0, 'normal approach resets streak');
  s = { ...s, units: fixture().units };
  const again = resolve(s, 3);
  assert.equal(again.state.blockedTurns.a, 1);
  assert.ok(!again.events.some(e => e.type === 'breakout'));
  const atWinch = { ...fixture(), blockedTurns: { a: 1 }, units: [unit('a', 'enemy', 1, 1)] };
  assert.equal(resolve(atWinch, 1).state.blockedTurns.a, 0);
});
test('breakout stops at first blocker, travels <=3, cannot swap other enemies or dead allies', () => {
  const s = { ...fixture(1), units: [...guards(), unit('near', 'ally', 1, 2), unit('a', 'enemy', 1, 3)] };
  const r = resolve(s, 1), e = r.events.find(e => e.type === 'breakout');
  assert.equal(e.swapped.unit, 'near'); assert.equal(e.path.length, 2); valid(r.state);
  const far = { ...fixture(1), units: [...guards(), unit('a', 'enemy', 1, 8)] };
  const farEvent = resolve(far, 1).events.find(e => e.type === 'breakout');
  assert.equal(farEvent.path.length, 4); assert.equal(farEvent.swapped, undefined);
  const enemies = { ...fixture(1), units: [...guards().map(u => ({ ...u, side: 'enemy' })), unit('a', 'enemy', 1, 3)] };
  assert.ok(!resolve(enemies, 1).events.some(e => e.type === 'breakout'));
  const dead = { ...fixture(1), units: fixture(1).units.map(u => u.id === 'w' ? { ...u, alive: false } : u) };
  assert.ok(!resolve(dead, 1).events.some(e => e.type === 'breakout'));
});
test('two enemies resolve sequentially without overlap; retry clears pressure; guards remain atomic', () => {
  const s = { ...fixture(1), units: [...fixture(1).units, unit('b', 'enemy', 3, 3)] };
  const r = resolve(freeze(s), 1); valid(r.state);
  assert.equal(r.events.filter(e => e.type === 'breakout').length, 2);
  assert.equal(r.state.progress, 0);
  assert.equal(resolve(r.state, 1).ok, false);
  const end = { ...r.state, status: 'failure' };
  assert.deepEqual(command(end, { type: 'retry' }).state, initialState('open', s.config));
  assert.deepEqual(resolve({ ...s, route: 'sealed' }, 1), { ok: false, state: { ...s, route: 'sealed' }, events: [], reason: 'sealed-map-only-in-P0' });
  assert.notEqual(stateKey(s), stateKey({ ...s, blockedTurns: { a: 1 } }));
});
test('A two-command enumeration independently matches unchanged P0c algorithm', () => {
  const s = startFor(variants[0].config), old = twoMoveSearch(s), fresh = boundedMoves(s, 2);
  for (const k of ['strategies', 'wins', 'losses', 'minimumCostWin']) assert.deepEqual(fresh[k], old[k]);
  assert.equal(fresh.strategies, 24922); assert.equal(fresh.wins, 0);
});

if (!process.argv.includes('--unit-only')) {
  const dir = new URL('../docs/playable-l03-p0d/', import.meta.url);
  const report = JSON.parse(readFileSync(new URL('search-results.json', dir), 'utf8'));
  const traces = [];
  test('original P0 trace and retreat outcomes match report; full-party minima and gates agree', () => {
    const original = [
      { type: 'move', turn: 1, unit: 'lace', to: { x: 1, y: 1 } },
      { type: 'move', turn: 1, unit: 'thoma', to: { x: 2, y: 2 } },
      { type: 'move', turn: 1, unit: 'karen', to: { x: 3, y: 3 } },
      { type: 'move', turn: 2, unit: 'karen', to: { x: 3, y: 1 } },
    ];
    for (const row of report.results) {
      for (const [label, commands] of [['originalP0', original], ['laceRetreat', [{ type: 'move', turn: 2, unit: 'lace', to: { x: 0, y: 3 } }]]]) {
        const r = replay(commands, startFor(row.config));
        assert.deepEqual({ legal: r.legal, status: r.state.status, progress: r.state.progress, turn: r.state.turn,
          ...(r.reason ? { reason: r.reason } : {}) }, row[label]);
        r.records.forEach(v => valid(v.state ?? v.initial));
        traces.push({ label: `${row.name}/${label}`, commands, records: r.records });
      }
      const spaces = [row.turnOneThenWait, row.atMostOneMove, row.multiMove, row.threeMove];
      const best = spaces.map(s => s.minimumCostWin).filter(Boolean).sort(costOrder)[0] ?? null;
      assert.deepEqual(row.minimumCostWin, best);
      const ties = spaces.filter(s => s.minimumCostWin && costOrder(s.minimumCostWin, best) === 0);
      assert.equal(row.allBestWinsAreT1ThenWait, ties.length ? ties.every(s => s.allBestWinsAreT1ThenWait) : null);
      assert.equal(row.distinctWinningStrategyFamilies, new Set(spaces.flatMap(s => s.families.map(f => f.family))).size);
      assert.equal(row.verdict, !best ? 'UNSOLVABLE' : best.moves <= 2 ? 'CHEESE' : Object.values(row.gates).every(Boolean) ? 'OK' : 'THIN');
      assert.ok(row.threeMove.strategies >= row.multiMove.strategies);
      assert.ok(row.threeMove.wins >= row.multiMove.wins);
    }
  });
  test('all cheapest and family witnesses legally replay with stated costs, grouping and bounds', () => {
    function check(w, start, label, bounds, family) {
      if (!w) return;
      const r = replay(w.commands, freeze(start));
      assert.ok(r.legal, `${label}: ${r.reason}`); assert.equal(r.state.status, 'success', label);
      const moves = r.records.filter(v => v.command?.type === 'move');
      assert.equal(w.moves, moves.length); assert.equal(w.units, new Set(moves.map(v => v.command.unit)).size);
      assert.equal(w.tiles, moves.reduce((n, v) => n + v.events[0].path.length - 1, 0));
      assert.equal(w.progress, r.state.progress); assert.equal(w.turn, r.state.turn);
      r.records.forEach(v => { valid(v.state ?? v.initial); for (const e of v.events ?? []) if (e.type === 'breakout') {
        assert.ok(e.path.length >= 2 && e.path.length <= 4);
        for (let i = 1; i < e.path.length; i++) assert.equal(Math.abs(e.path[i].x - e.path[i-1].x) + Math.abs(e.path[i].y - e.path[i-1].y), 1);
      } });
      if (bounds?.maxMovesTotal) assert.ok(w.moves <= bounds.maxMovesTotal);
      if (bounds?.maxMovesPerTurn) for (let t = 1; t <= w.turn; t++) assert.ok(w.commands.filter(c => c.turn === t).length <= bounds.maxMovesPerTurn);
      if (family) assert.equal(familyKey(r.state, moves.map(v => ({ input: v.command }))), family);
      traces.push({ label, commands: w.commands, records: r.records });
    }
    function space(s, start, label) {
      if ('strategies' in s) {
        assert.equal(s.strategies, s.wins + s.losses);
        assert.equal(s.distinctWinningStrategyFamilies, s.families.length);
        assert.equal(s.families.reduce((n, f) => n + f.wins, 0), s.wins);
        assert.equal(s.allBestWinsAreT1ThenWait, s.wins ? s.bestWinTies.afterT1 === 0 : null);
      }
      check(s.minimumCostWin, start, label, s.bounds);
      for (const f of s.families ?? []) check(f.minimumCostWin, start, `${label}/${f.family}`, s.bounds, f.family);
    }
    for (const row of report.results) {
      const start = startFor(row.config);
      for (const k of ['turnOneThenWait', 'atMostOneMove', 'multiMove', 'threeMove']) space(row[k], start, `${row.name}/${k}`);
      for (const l of row.lineups) {
        const reduced = startFor(row.config, l.party);
        assert.equal(reduced.units.filter(u => u.side === 'ally').length, l.party.length);
        for (const k of ['turnOneThenWait', 'atMostOneMove', 'multiMove', 'threeMove', 'widerSearch']) space(l[k], reduced, `${row.name}/${l.party}/${k}`);
        assert.equal(l.widerSearch.found, !!l.widerSearch.minimumCostWin);
        const best = [l.turnOneThenWait, l.atMostOneMove, l.multiMove, l.threeMove, l.widerSearch].map(s => s.minimumCostWin).filter(Boolean).sort(costOrder)[0] ?? null;
        assert.deepEqual(l.cheapestFound, best);
      }
    }
  });
  test('serialized replay evidence is byte-identical', () => {
    const text = traces.map(t => JSON.stringify(t)).join('\n') + '\n';
    const file = new URL('witnesses.jsonl', dir);
    if (process.argv.includes('--write-traces')) writeFileSync(file, text);
    else assert.equal(readFileSync(file, 'utf8'), text);
  });
}
console.log(`${passed} P0d tests passed`);
