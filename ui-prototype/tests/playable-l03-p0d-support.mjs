import { DEFAULT_CONFIG, initialState, resolve } from '../src/playable-l03/rules.ts';
import { legalMoves, positionKey, cost, compareCost, waitOut } from './playable-l03-p0b-support.mjs';
import { witness } from './playable-l03-p0c-support.mjs';

export const variants = [
  { name: 'A', config: { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 } } },
  { name: 'D', config: { ...DEFAULT_CONFIG, p0d: { blockedTurnsBeforeBreakout: 2 } } },
  { name: 'A+D', config: { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 }, p0d: { blockedTurnsBeforeBreakout: 2 } } },
];
export function startFor(config, party) {
  const state = initialState('open', config);
  return party ? { ...state, units: state.units.filter(u => u.side === 'enemy' || party.includes(u.id)) } : state;
}
export const stateKey = s => `${s.turn}|${s.status}|${positionKey(s)}|${s.progress}|${s.holdStreak ?? 0}|${JSON.stringify(s.blockedTurns ?? {})}`;
export const costOrder = (a, b) => a.moves - b.moves || a.units - b.units || a.tiles - b.tiles;
export const t1Only = moves => moves.every(m => m.input.turn === 1);

// Deliberately coarse operational grouping, not a claim of distinct human tactics.
// Final living ally lane assignments + voluntary repositioning after T1.
// Within-lane tile/timing differences are merged; forced swaps do not count as commands.
export function familyKey(state, moves) {
  const lane = ({ x, y }) => y > 3 ? 'rear' : y === 0 ? 'north' : x <= 1 ? 'west' : x === 2 ? 'south' : 'east';
  return state.units.filter(u => u.side === 'ally' && u.alive)
    .map(u => `${u.id}:${lane(u.cell)}`).join('|') + `|afterT1:${!t1Only(moves)}`;
}
export function collector() {
  let wins = 0, losses = 0, best, bestT1 = 0, bestLater = 0;
  const families = new Map();
  return {
    assess(state, moves) {
      if (state.status !== 'success') { losses++; return; }
      wins++;
      const k = familyKey(state, moves), old = families.get(k);
      if (!old) families.set(k, { family: k, wins: 1, minimumCostWin: witness(moves, state) });
      else { old.wins++; if (costOrder(cost(moves), old.minimumCostWin) < 0) old.minimumCostWin = witness(moves, state); }
      const comparison = best ? compareCost(moves, best.moves) : -1;
      if (comparison < 0) { best = { state, moves }; bestT1 = 0; bestLater = 0; }
      if (comparison <= 0) { if (t1Only(moves)) bestT1++; else bestLater++; }
    },
    result() {
      return { strategies: wins + losses, wins, losses,
        minimumCostWin: best ? witness(best.moves, best.state) : null,
        bestWinTies: { t1ThenWait: bestT1, afterT1: bestLater },
        allBestWinsAreT1ThenWait: best ? bestLater === 0 : null,
        distinctWinningStrategyFamilies: families.size,
        families: [...families.values()].sort((a, b) => a.family.localeCompare(b.family, 'en')) };
    },
  };
}
export function summarize(candidates) {
  const c = collector();
  for (const { state, moves } of candidates) c.assess(waitOut(state), moves);
  return c.result();
}

// Enumerate every legal command sequence within the declared bounds, then wait.
// No beam or pruning. Caches only deterministic wait tails, not command histories.
export function boundedMoves(start, maxMovesTotal = 2, maxMovesPerTurn = 2) {
  const c = collector(), tails = new Map();
  function assess(state, moves) {
    const k = stateKey(state);
    let end = tails.get(k);
    if (!end) { end = waitOut(state); if (tails.size < 100000) tails.set(k, end); }
    c.assess(end, moves);
  }
  function visit(state, moves) {
    assess(state, moves);
    if (moves.length === maxMovesTotal) return;
    for (let s = state; s.status === 'playing'; s = resolve(s, s.turn).state) {
      if (moves.filter(m => m.input.turn === s.turn).length >= maxMovesPerTurn) continue;
      for (const move of legalMoves(s)) visit(move.next.state, [...moves, move]);
    }
  }
  visit(start, []);
  return { bounds: { survivalTurns: start.config.p0c?.survivalTurns ?? 5,
    maxMovesPerTurn, maxMovesTotal, stateCap: null, exhaustiveWithinBounds: true }, ...c.result() };
}

// Wider solo/duo probe: <=2 commands each turn, no TOTAL command cap.
// Deduplicate only future-equivalent state + moved-unit set (needed by cost).
// Deterministic transition/state caps are disclosed; never call a capped result optimal.
export function lineupSearch(start, stateCap = 10000, transitionCapPerTurn = 250000) {
  let frontier = [{ state: start, moves: [] }], truncated = false, best;
  const layers = [];
  for (let turn = 1; turn <= (start.config.p0c?.survivalTurns ?? 5) && frontier.length; turn++) {
    const next = new Map();
    let transitions = 0, stateCapHit = false, transitionCapHit = false;
    function accept(state, moves) {
      if (transitions >= transitionCapPerTurn) { transitionCapHit = true; return false; }
      transitions++;
      const end = resolve(state, state.turn).state;
      if (end.status === 'success') {
        if (!best || compareCost(moves, best.moves) < 0) best = { state: end, moves };
      } else if (end.status === 'playing') {
        const movedSet = [...new Set(moves.map(m => m.input.unit))].sort().join(',');
        const k = `${stateKey(end)}|used:${movedSet}`, old = next.get(k);
        if (!old && next.size >= stateCap) stateCapHit = true;
        else if (!old || compareCost(moves, old.moves) < 0) next.set(k, { state: end, moves });
      }
      return true;
    }
    outer: for (const node of frontier) {
      if (!accept(node.state, node.moves)) break;
      for (const first of legalMoves(node.state)) {
        const moves = [...node.moves, first];
        if (!accept(first.next.state, moves)) break outer;
        for (const second of legalMoves(first.next.state))
          if (!accept(second.next.state, [...moves, second])) break outer;
      }
    }
    truncated ||= stateCapHit || transitionCapHit;
    frontier = [...next.values()].sort((a, b) => compareCost(a.moves, b.moves));
    layers.push({ turn, transitions, retainedStates: frontier.length, stateCapHit, transitionCapHit });
  }
  return { bounds: { maxMovesPerTurn: 2, maxMovesTotal: null, stateCap, transitionCapPerTurn },
    truncated, exhaustiveWithinBounds: !truncated, layers, found: !!best,
    minimumCostWin: best ? witness(best.moves, best.state) : null };
}
