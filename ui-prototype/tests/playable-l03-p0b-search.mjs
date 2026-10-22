import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { initialState, resolve } from '../src/playable-l03/rules.ts';
import { legalMoves, positionKey, cost, compareCost, waitOut } from './playable-l03-p0b-support.mjs';

// Question: can occupancy + the five-turn deadline be won trivially?
// Retain evidence, not gameplay changes. CHEESE if a single-move win exists.
// Exhaustive T1 endpoints (all legal orders), then WAIT ONLY. Not all 5-turn play.
function turnOnePlacements() {
  const placements = new Map();
  function visit(state, moves) {
    const id = positionKey(state), previous = placements.get(id);
    if (!previous || compareCost(moves, previous.moves) < 0) placements.set(id, { state, moves });
    for (const move of legalMoves(state)) visit(move.next.state, [...moves, move]);
  }
  visit(initialState(), []);
  return [...placements.values()];
}
function summarize(candidates) {
  let wins = 0, losses = 0, best;
  const byUnitsMoved = {};
  for (const { state, moves } of candidates) {
    const end = waitOut(state), c = cost(moves);
    const bucket = byUnitsMoved[c.units] ??= { wins: 0, losses: 0 };
    if (end.status === 'success') {
      wins++; bucket.wins++;
      if (!best || compareCost(moves, best.moves) < 0) best = { moves, end };
    } else { losses++; bucket.losses++; }
  }
  return { strategies: wins + losses, wins, losses, byUnitsMoved,
    minimumCostWin: best ? { ...cost(best.moves), commands: best.moves.map(m => m.input),
      progress: best.end.progress, turn: best.end.turn } : null };
}
// Exhaustive over <=1 move, any ally/destination/turn, waits on every other turn.
// No-move strategy counted once; commands after terminal failure never generated.
function oneMoveCandidates(start) {
  const candidates = [{ state: start, moves: [] }];
  let state = start;
  while (state.status === 'playing') {
    for (const move of legalMoves(state)) candidates.push({ state: move.next.state, moves: [move] });
    state = resolve(state, state.turn).state;
  }
  return candidates;
}
const t1 = summarize(turnOnePlacements());
const oneMove = summarize(oneMoveCandidates(initialState()));
assert.deepEqual([t1.wins, t1.losses], [493, 6303]);
assert.deepEqual([oneMove.wins, oneMove.losses], [6, 211]);
assert.deepEqual([t1.minimumCostWin.moves, t1.minimumCostWin.units, t1.minimumCostWin.tiles], [1, 1, 3]);
assert.deepEqual([oneMove.minimumCostWin.moves, oneMove.minimumCostWin.units, oneMove.minimumCostWin.tiles], [1, 1, 1]);
const lineups = [];
const ids = ['karen', 'lace', 'thoma'];
// Additional lineup witness search: <=1 ally command per turn, deduplicate at
// turn boundaries; deterministic 10,000-state cap. A witness is proof of
// existence, not an exhaustive win/loss rate for the reduced lineup.
function lineupWitness(start) {
  let frontier = [{ state: start, moves: [] }];
  const widths = [];
  let truncated = false;
  for (let turn = 1; turn <= 5; turn++) {
    const next = new Map();
    for (const node of frontier) {
      const choices = [{ state: node.state, moves: node.moves }, ...legalMoves(node.state)
        .map(m => ({ state: m.next.state, moves: [...node.moves, m] }))];
      for (const choice of choices) {
        const state = resolve(choice.state, choice.state.turn).state;
        if (state.status === 'success') return { found: true, truncated, widths,
          cost: cost(choice.moves), commands: choice.moves.map(m => m.input), progress: state.progress };
        if (state.status !== 'playing') continue;
        const id = `${positionKey(state)}|${state.progress}`;
        const previous = next.get(id);
        if (!previous && next.size >= 10000) { truncated = true; continue; }
        if (!previous || compareCost(choice.moves, previous.moves) < 0) next.set(id, { state, moves: choice.moves });
      }
    }
    frontier = [...next.values()];
    widths.push(frontier.length);
  }
  return { found: false, truncated, widths };
}
for (let mask = 1; mask < 7; mask++) {
  const party = ids.filter((_, i) => mask & (1 << i));
  const base = initialState();
  const start = { ...base, units: base.units.filter(u => u.side === 'enemy' || party.includes(u.id)) };
  lineups.push({ party, atMostOneMove: summarize(oneMoveCandidates(start)), witness: lineupWitness(start) });
}
assert.ok(lineups.some(l => l.party.length === 1 && l.witness.found));
assert.ok(lineups.some(l => l.party.length === 2 && l.witness.found));
const report = { verdict: 'CHEESE', route: 'open', blockAlliedPassage: true,
  counting: 'T1: unique labeled end placements over all legal move orders, minimum-cost representative; later turns wait. One-move: distinct legal command/turn plus idle once. No randomness.',
  bounds: 'Five turns; all T1 placements, <=1 move over later turns. Not exhaustive multi-move strategies over all five turns. Solo/duo remove absent allies, retaining both enemies.',
  turnOneThenWait: t1, atMostOneMove: oneMove, lineups };
const file = new URL('../docs/playable-l03-p0b/search-results.json', import.meta.url);
const encoded = JSON.stringify(report, null, 2) + '\n';
if (process.argv.includes('--write-results')) { mkdirSync(new URL('.', file), { recursive: true }); writeFileSync(file, encoded); }
else assert.equal(readFileSync(file, 'utf8'), encoded, 'search report drift');
console.log(encoded);
