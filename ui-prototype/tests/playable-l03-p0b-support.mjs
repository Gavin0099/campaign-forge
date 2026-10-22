import assert from 'node:assert/strict';
import { MAP, initialState, command, resolve, key } from '../src/playable-l03/rules.ts';

// Enumerate commands through the real public API; no duplicate rules simulator.
export function legalMoves(state) {
  const result = [];
  for (const actor of state.units.filter(u => u.alive && u.side === 'ally' && !state.moved.includes(u.id))) {
    for (let y = 0; y < MAP.rows.length; y++) for (let x = 0; x < MAP.rows[y].length; x++) {
      const d = Math.abs(x - actor.cell.x) + Math.abs(y - actor.cell.y);
      if (d < 1 || d > 3) continue;
      const input = { type: 'move', turn: state.turn, unit: actor.id, to: { x, y } };
      const next = command(state, input);
      if (next.ok) result.push({ input, next, tiles: next.events[0].path.length - 1 });
    }
  }
  return result;
}
export const positionKey = state => state.units.map(u => `${u.id}:${key(u.cell)}`).join('|');
export const cost = moves => ({ moves: moves.length, units: new Set(moves.map(m => m.input.unit)).size,
  tiles: moves.reduce((n, m) => n + m.tiles, 0) });
export function compareCost(a, b) {
  const x = cost(a), y = cost(b);
  return x.moves - y.moves || x.units - y.units || x.tiles - y.tiles;
}
export function waitOut(start) {
  let state = start;
  while (state.status === 'playing') {
    const result = resolve(state, state.turn);
    assert.ok(result.ok, result.reason);
    state = result.state;
  }
  return state;
}
export function runPlan(plan, start = initialState()) {
  let state = start;
  const records = [{ initial: state }];
  while (state.status === 'playing') {
    for (const [unit, x, y] of plan[state.turn] ?? []) {
      const input = { type: 'move', turn: state.turn, unit, to: { x, y } };
      const result = command(state, input);
      assert.ok(result.ok, result.reason);
      state = result.state;
      records.push({ command: input, events: result.events, state });
    }
    const input = { type: 'resolve', turn: state.turn };
    const result = resolve(state, state.turn);
    assert.ok(result.ok, result.reason);
    state = result.state;
    records.push({ command: input, events: result.events, state });
  }
  return { state, records };
}
