// Adapted by copying this repo's P0d harness at 2dc92b6d5ec22e9e4e48bb82db995adeb111e58a.
// No merge; no external source or assets. Only the required full-party searches remain.
import { DEFAULT_CONFIG, initialState, resolve } from '../src/playable-l03/rules.ts';
import { legalMoves, positionKey, cost, compareCost, waitOut } from './playable-l03-p0b-support.mjs';
import { witness, replay } from './playable-l03-p0c-support.mjs';

// Strict causal witness: react on the full turn after an actual prepare event;
// omitting that turn's commands loses under P2, but wins under A alone. The
// actual reaction must cancel that knight's exact telegraph. No timing-only win.
export function reactionEvidence(commands, start) {
  const full = replay(commands, start);
  if (!full.legal || full.state.status !== 'success') return null;
  for (const record of full.records) for (const event of record.events ?? []) {
    if (event.type !== 'enemy-intent' || event.intent !== 'prepare-breakout') continue;
    const reactionTurn = record.command.turn + 1;
    const response = commands.filter(c => c.turn === reactionTurn);
    if (!response.length) continue;
    const after = full.records.find(r => r.command?.type === 'resolve' && r.command.turn === reactionTurn);
    if (!after?.events.some(e => e.type === 'enemy-intent' && e.unit === event.unit && e.intent === 'cancel-breakout')) continue;
    const ignoredCommands = commands.filter(c => c.turn !== reactionTurn);
    const ignored = replay(ignoredCommands, start);
    const baseline = replay(ignoredCommands, initialState('open', { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 } }));
    if (!ignored.legal || ignored.state.status !== 'failure' || !baseline.legal || baseline.state.status !== 'success') continue;
    if (!ignored.records.some(r => r.command?.turn === reactionTurn && r.events?.some(e =>
      e.type === 'breakout' && e.unit === event.unit && JSON.stringify(e.plan) === JSON.stringify(event.plan)))) continue;
    return { commands, ignoredCommands, reactionTurn, telegraph: event,
      reacting: { status: full.state.status, progress: full.state.progress },
      ignoring: { status: ignored.state.status, progress: ignored.state.progress },
      ignoringWithoutP2: { status: baseline.state.status, progress: baseline.state.progress } };
  }
  return null;
}

export const variants = [
  { name: 'A+P2', config: { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 }, enemyBehaviour: 'p2', detourThreshold: 1 } },
];
export function startFor(config, party) {
  const state = initialState('open', config);
  return party ? { ...state, units: state.units.filter(u => u.side === 'enemy' || party.includes(u.id)) } : state;
}
export const stateKey = s => `${s.turn}|${s.status}|${positionKey(s)}|${s.progress}|${s.holdStreak ?? 0}|${JSON.stringify(s.enemyPressure ?? {})}`;
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
export function collector(start) {
  let wins = 0, losses = 0, best, bestT1 = 0, bestLater = 0;
  let bestReactions = 0, keyGateWitness = null;
  const cheapest = [];
  const families = new Map();
  return {
    assess(state, moves) {
      if (state.status !== 'success') { losses++; return; }
      wins++;
      const k = familyKey(state, moves), old = families.get(k);
      if (!old) families.set(k, { family: k, wins: 1, minimumCostWin: witness(moves, state) });
      else { old.wins++; if (costOrder(cost(moves), old.minimumCostWin) < 0) old.minimumCostWin = witness(moves, state); }
      const comparison = best ? compareCost(moves, best.moves) : -1;
      const reaction = start && (!keyGateWitness || comparison <= 0) ? reactionEvidence(moves.map(m => m.input), start) : null;
      if (reaction && !keyGateWitness) keyGateWitness = reaction;
      if (comparison < 0) { best = { state, moves }; bestT1 = 0; bestLater = 0; bestReactions = 0; cheapest.length = 0; }
      if (comparison <= 0) {
        if (t1Only(moves)) bestT1++; else bestLater++;
        if (reaction) bestReactions++;
        cheapest.push(moves.map(m => m.input));
      }
    },
    result() {
      return { strategies: wins + losses, wins, losses,
        minimumCostWin: best ? witness(best.moves, best.state) : null,
        bestWinTies: { t1ThenWait: bestT1, afterT1: bestLater },
        cheapestWinsRequiringTelegraphReaction: bestReactions, cheapestCommands: cheapest, keyGateWitness,
        allBestWinsAreT1ThenWait: best ? bestLater === 0 : null,
        distinctWinningStrategyFamilies: families.size,
        families: [...families.values()].sort((a, b) => a.family.localeCompare(b.family, 'en')) };
    },
  };
}
export function summarize(candidates, start) {
  const c = collector(start);
  for (const { state, moves } of candidates) c.assess(waitOut(state), moves);
  return c.result();
}

// Enumerate every legal command sequence within the declared bounds, then wait.
// No beam or pruning. Caches only deterministic wait tails, not command histories.
export function boundedMoves(start, maxMovesTotal = 2, maxMovesPerTurn = 2) {
  const c = collector(start), tails = new Map();
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
