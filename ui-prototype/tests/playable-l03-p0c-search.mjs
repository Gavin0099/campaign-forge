import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { variants, startFor, turnOnePlacements, oneMoveCandidates, summarize, lineupWitness,
  replay, twoMoveSearch } from './playable-l03-p0c-support.mjs';

// QUESTION: do these opt-in objectives remove cheap waiting wins?
// Keep evidence only; never promote an option to default. 45-minute P0c task.
// CHEESE: <=1 move wins or a <=2-total-move hold/rush wins with full party.
// THIN: solvable and cheap witnesses excluded in these bounds, depth unproved.
// OK requires additional tactical evidence; no win found is UNSOLVABLE, not fixed.
const original = [
  { type: 'move', turn: 1, unit: 'lace', to: { x: 1, y: 1 } },
  { type: 'move', turn: 1, unit: 'thoma', to: { x: 2, y: 2 } },
  { type: 'move', turn: 1, unit: 'karen', to: { x: 3, y: 3 } },
  { type: 'move', turn: 2, unit: 'karen', to: { x: 3, y: 1 } },
];
const retreat = [{ type: 'move', turn: 2, unit: 'lace', to: { x: 0, y: 3 } }];
const results = [];
for (const variant of variants) {
  const start = startFor(variant.options);
  const turnOneThenWait = summarize(turnOnePlacements(start));
  const atMostOneMove = summarize(oneMoveCandidates(start));
  const ids = ['karen', 'lace', 'thoma'], lineups = [];
  for (let mask = 1; mask < 7; mask++) {
    const party = ids.filter((_, i) => mask & (1 << i)), reduced = startFor(variant.options, party);
    lineups.push({ party, turnOneThenWait: summarize(turnOnePlacements(reduced)),
      atMostOneMove: summarize(oneMoveCandidates(reduced)), witness: lineupWitness(reduced) });
  }
  const check = commands => {
    const r = replay(commands, start);
    return { legal: r.legal, status: r.state.status, progress: r.state.progress,
      ...(r.reason ? { reason: r.reason, rejected: r.rejected } : {}) };
  };
  const multiMove = [];
  if (variant.name === 'B' || variant.name.startsWith('B+'))
    for (const survivalTurns of [5, 6]) multiMove.push(twoMoveSearch(startFor({ ...variant.options, survivalTurns })));
  const minima = [turnOneThenWait.minimumCostWin, atMostOneMove.minimumCostWin,
    ...multiMove.filter(m => m.bounds.survivalTurns === 5).map(m => m.minimumCostWin)].filter(Boolean);
  minima.sort((a, b) => a.moves - b.moves || a.units - b.units || a.tiles - b.tiles);
  const found = minima.length || lineups.some(l => l.witness.found);
  const cheap = atMostOneMove.wins || multiMove.some(m => m.bounds.survivalTurns === 5 && m.wins);
  results.push({ ...variant, verdict: !found ? 'UNSOLVABLE' : cheap ? 'CHEESE' : 'THIN',
    turnOneThenWait, atMostOneMove, minimumCostWin: minima[0] ?? null,
    originalP0: check(original), laceRetreat: check(retreat), lineups, multiMove });
  console.error(`finished ${variant.name}`);
}
assert.deepEqual([results[0].turnOneThenWait.wins, results[0].turnOneThenWait.losses], [493, 6303]);
assert.deepEqual([results[0].atMostOneMove.wins, results[0].atMostOneMove.losses], [6, 211]);
const report = {
  scope: 'P0c opt-in verification only; defaults, UI, story and P1 unchanged',
  counting: 'P0b T1 unique labeled endpoints, cheapest representative over all legal orders; one-move distinct command+turn and idle once. Cost: moves, distinct moved allies, path tiles. Not human win rates.',
  lineupBounds: 'Same P0b <=1 command/turn witness search, 10000 distinct turn-boundary states, stop at first win; absent allies removed; holdStreak included in key. Counts for T1 and <=1 total also supplied per lineup.',
  multiMoveBounds: '<=2 moves per turn AND <=2 moves in total, all command orders/units/legal destinations, then wait, no cap; 5 and 6 turns. Exact within bounds, not all strategies with up to 10/12 moves.',
  verdictCriterion: 'CHEESE if <=1 move wins or <=2-total-move full-party hold/rush wins at the variant horizon; THIN if other win exists without those witnesses; OK requires additional tactical evidence; UNSOLVABLE means no win found in tested bounds, not a proof of global impossibility.',
  results,
};
const file = new URL('../docs/playable-l03-p0c/search-results.json', import.meta.url);
const encoded = JSON.stringify(report, null, 2) + '\n';
if (process.argv.includes('--write-results')) { mkdirSync(new URL('.', file), { recursive: true }); writeFileSync(file, encoded); }
else assert.equal(readFileSync(file, 'utf8'), encoded, 'P0c search report drift');
console.log(encoded);
