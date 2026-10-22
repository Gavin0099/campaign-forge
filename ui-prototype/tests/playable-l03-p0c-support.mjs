import assert from 'node:assert/strict';
import { DEFAULT_CONFIG, initialState, command, resolve } from '../src/playable-l03/rules.ts';
import { legalMoves, positionKey, cost, compareCost, waitOut } from './playable-l03-p0b-support.mjs';

export const variants = [
  { name: 'Baseline', options: {} },
  { name: 'A', options: { survivalTurns: 6 } },
  { name: 'B', options: { requiredHoldTurns: 1 } },
  { name: 'C', options: { thomaStartsWest: true } },
  { name: 'B+ N=2', options: { requiredHoldTurns: 2 } },
  { name: 'B+ N=3', options: { requiredHoldTurns: 3 } },
];
export function startFor(options = {}, party) {
  const base = initialState('open', Object.keys(options).length
    ? { ...DEFAULT_CONFIG, p0c: options } : DEFAULT_CONFIG);
  return party ? { ...base, units: base.units.filter(u => u.side === 'enemy' || party.includes(u.id)) } : base;
}
export const stateKey = state => `${positionKey(state)}|${state.progress}|${state.holdStreak ?? 0}`;
export function turnOnePlacements(start) {
  const placements = new Map();
  function visit(state, moves) {
    const id = positionKey(state), previous = placements.get(id);
    if (!previous || compareCost(moves, previous.moves) < 0) placements.set(id, { state, moves });
    for (const move of legalMoves(state)) visit(move.next.state, [...moves, move]);
  }
  visit(start, []);
  return [...placements.values()];
}
export function oneMoveCandidates(start) {
  const candidates = [{ state: start, moves: [] }];
  for (let state = start; state.status === 'playing'; state = resolve(state, state.turn).state)
    for (const move of legalMoves(state)) candidates.push({ state: move.next.state, moves: [move] });
  return candidates;
}
export function witness(moves, end) {
  return { ...cost(moves), commands: moves.map(m => m.input), progress: end.progress, turn: end.turn,
    ...(end.holdStreak === undefined ? {} : { holdStreak: end.holdStreak }) };
}
export function summarize(candidates) {
  let wins = 0, losses = 0, best;
  for (const { state, moves } of candidates) {
    const end = waitOut(state);
    if (end.status === 'success') {
      wins++;
      if (!best || compareCost(moves, best.moves) < 0) best = { moves, end };
    } else losses++;
  }
  return { strategies: wins + losses, wins, losses,
    minimumCostWin: best ? witness(best.moves, best.end) : null };
}
// Same existence-search bounds as P0b. Include hold history in deduplication.
export function lineupWitness(start) {
  let frontier = [{ state: start, moves: [] }], truncated = false;
  const widths = [];
  for (let turn = 1; turn <= (start.config.p0c?.survivalTurns ?? 5); turn++) {
    const next = new Map();
    for (const node of frontier) {
      const choices = [{ state: node.state, moves: node.moves }, ...legalMoves(node.state)
        .map(m => ({ state: m.next.state, moves: [...node.moves, m] }))];
      for (const choice of choices) {
        const state = resolve(choice.state, choice.state.turn).state;
        if (state.status === 'success') return { found: true, truncated, widths,
          witness: witness(choice.moves, state) };
        if (state.status !== 'playing') continue;
        const id = stateKey(state), previous = next.get(id);
        if (!previous && next.size >= 10000) { truncated = true; continue; }
        if (!previous || compareCost(choice.moves, previous.moves) < 0) next.set(id, { state, moves: choice.moves });
      }
    }
    frontier = [...next.values()]; widths.push(frontier.length);
  }
  return { found: false, truncated, widths };
}
export function replay(commands, start) {
  let state = start;
  const records = [{ initial: state }];
  while (state.status === 'playing') {
    for (const input of commands.filter(c => c.turn === state.turn)) {
      const result = command(state, input);
      if (!result.ok) return { legal: false, reason: result.reason, rejected: input, state, records };
      state = result.state; records.push({ command: input, events: result.events, state });
    }
    const input = { type: 'resolve', turn: state.turn }, result = resolve(state, state.turn);
    assert.ok(result.ok, result.reason);
    state = result.state; records.push({ command: input, events: result.events, state });
  }
  return { legal: true, state, records };
}

// Exact, bounded multi-move search: <=2 commands TOTAL, hence <=2 per turn.
// For every first command (all units/tiles/turns), enumerate all second commands
// in that turn or any subsequent still-playing turn, then wait. No beam/cap.
// Enumerates command sequences, not unique end states. Cost is P0b's order.
export function twoMoveSearch(start) {
  let wins = 0, losses = 0, best, lateArrival;
  function assess(state, moves) {
    const end = waitOut(state);
    if (end.status !== 'success') { losses++; return; }
    wins++;
    if (!best || compareCost(moves, best.moves) < 0) best = { moves, end };
    const trace = replay(moves.map(m => m.input), start);
    const holdTurns = trace.records.filter(r => r.command?.type === 'resolve' && r.state.holdStreak > 0)
      .map(r => r.command.turn);
    const requiredStart = (start.config.p0c?.survivalTurns ?? 5) - (start.config.p0c?.requiredHoldTurns ?? 1) + 1;
    if (holdTurns[0] === requiredStart && (!lateArrival || compareCost(moves, lateArrival.moves) < 0))
      lateArrival = { moves, end, holdTurns };
  }
  assess(start, []);
  for (let firstState = start; firstState.status === 'playing'; firstState = resolve(firstState, firstState.turn).state) {
    for (const first of legalMoves(firstState)) {
      assess(first.next.state, [first]);
      for (let secondState = first.next.state; secondState.status === 'playing'; secondState = resolve(secondState, secondState.turn).state)
        for (const second of legalMoves(secondState)) assess(second.next.state, [first, second]);
    }
  }
  return { bounds: { survivalTurns: start.config.p0c?.survivalTurns ?? 5, maxMovesPerTurn: 2,
    maxMovesTotal: 2, stateCap: null, exhaustiveWithinBounds: true },
    strategies: wins + losses, wins, losses,
    minimumCostWin: best ? witness(best.moves, best.end) : null,
    latestRequiredArrivalWin: lateArrival ? { ...witness(lateArrival.moves, lateArrival.end), holdTurns: lateArrival.holdTurns } : null };
}
