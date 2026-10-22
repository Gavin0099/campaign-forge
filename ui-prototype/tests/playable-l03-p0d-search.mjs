import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { turnOnePlacements, oneMoveCandidates, replay } from './playable-l03-p0c-support.mjs';
import { variants, startFor, summarize, boundedMoves, lineupSearch, costOrder } from './playable-l03-p0d-support.mjs';

// QUESTION: can the final P0 experiment avoid all cheapest wins being T1+wait?
// Retain verification evidence only. Experiments OFF by default, 60 min total.
// CHEESE: <=2-command win. THIN: solvable but OK gates fail. UNSOLVABLE:
// none found in stated spaces, never a global impossibility proof.
// OK: >=2 lane/reposition families; wins <50% in EVERY exact space containing
// a win; T1 absent or minimum >=3 commands/3 allies/8 tiles; not all cheapest
// tested wins T1+wait; original trace legally wins or has an explained loss.
const original = [
  { type: 'move', turn: 1, unit: 'lace', to: { x: 1, y: 1 } },
  { type: 'move', turn: 1, unit: 'thoma', to: { x: 2, y: 2 } },
  { type: 'move', turn: 1, unit: 'karen', to: { x: 3, y: 3 } },
  { type: 'move', turn: 2, unit: 'karen', to: { x: 3, y: 1 } },
];
const retreat = [{ type: 'move', turn: 2, unit: 'lace', to: { x: 0, y: 3 } }];
const results = [];
for (const variant of variants) {
  const start = startFor(variant.config);
  const turnOneThenWait = summarize(turnOnePlacements(start));
  const atMostOneMove = summarize(oneMoveCandidates(start));
  const multiMove = boundedMoves(start, 2);
  console.error(`${variant.name}: T1 and two-move complete`);
  const threeMove = boundedMoves(start, 3, 2);
  console.error(`${variant.name}: three-move complete`);
  const lineups = [];
  const ids = ['karen', 'lace', 'thoma'];
  for (let mask = 1; mask < 7; mask++) {
    const party = ids.filter((_, i) => mask & (1 << i)), reduced = startFor(variant.config, party);
    const row = { party, turnOneThenWait: summarize(turnOnePlacements(reduced)),
      atMostOneMove: summarize(oneMoveCandidates(reduced)), multiMove: boundedMoves(reduced, 2),
      threeMove: boundedMoves(reduced, 3, 2), widerSearch: lineupSearch(reduced) };
    const wins = [row.turnOneThenWait, row.atMostOneMove, row.multiMove, row.threeMove, row.widerSearch]
      .map(s => s.minimumCostWin).filter(Boolean).sort(costOrder);
    row.cheapestFound = wins[0] ?? null;
    lineups.push(row);
    console.error(`${variant.name}: ${party.join('+')} complete`);
  }
  const spaces = [turnOneThenWait, atMostOneMove, multiMove, threeMove];
  const bestSpace = spaces.filter(s => s.minimumCostWin).sort((a, b) => costOrder(a.minimumCostWin, b.minimumCostWin))[0];
  const minimumCostWin = bestSpace?.minimumCostWin ?? null;
  const bestSpaces = spaces.filter(s => s.minimumCostWin && costOrder(s.minimumCostWin, minimumCostWin) === 0);
  const allBestWinsAreT1ThenWait = bestSpaces.length ? bestSpaces.every(s => s.allBestWinsAreT1ThenWait) : null;
  const families = [...new Set(spaces.flatMap(s => s.families.map(f => f.family)))].sort();
  const check = commands => {
    const r = replay(commands, start);
    return { legal: r.legal, status: r.state.status, progress: r.state.progress, turn: r.state.turn,
      ...(r.reason ? { reason: r.reason } : {}) };
  };
  const originalP0 = check(original), t1 = turnOneThenWait.minimumCostWin;
  const gates = { noOrCostlyT1: !t1 || (t1.moves >= 3 && t1.units >= 3 && t1.tiles >= 8),
    multipleFamilies: families.length >= 2,
    winsMinority: spaces.filter(s => s.wins).every(s => s.wins < s.strategies / 2),
    someBestWinNeedsLaterCommand: allBestWinsAreT1ThenWait === false,
    originalTraceLegal: originalP0.legal };
  const verdict = !minimumCostWin ? 'UNSOLVABLE' : minimumCostWin.moves <= 2 ? 'CHEESE'
    : Object.values(gates).every(Boolean) ? 'OK' : 'THIN';
  results.push({ ...variant, verdict, gates, turnOneThenWait, atMostOneMove, multiMove, threeMove,
    minimumCostWin, distinctWinningStrategyFamilies: families.length, families,
    allBestWinsAreT1ThenWait, originalP0, laceRetreat: check(retreat), lineups });
}
const report = { scope: 'P0d only; opt-in D; A remains a candidate. No UI, HP, attack, story or dependencies.',
  counting: 'T1 unique labeled endpoints over all legal orders; <=1 and bounded multi count distinct command sequences. Overlapping spaces NOT summed. Cost order commands, distinct voluntarily moved allies, path tiles; forced swaps cost no player commands. Not human win rates.',
  families: 'Final living allies: y>3 rear; otherwise y=0 north, x<=1 west, x=2 south, x>=3 east. Group by labeled lane assignment and whether ANY voluntary command is after T1. Within-lane/timing variants merged. Operational groups, not proof of tactical depth.',
  bounds: 'Full-party and reduced-lineup exact <=2-total and <=3-total searches, <=2 commands/turn, no cap. T1 additionally includes 3-command placements. Wider solo/duo <=2 commands/turn with no total cap: 10000 retained states and 250000 examined transitions per turn; flags disclose truncation. Cheapest found is not global optimum.',
  verdictCriterion: 'CHEESE <=2-command full-party win; OK requires all five gates plus explained original trace in handoff. Costly T1 means >=3 commands, >=3 moved allies, >=8 tiles. THIN otherwise solvable. UNSOLVABLE means no win found, not global impossibility.', results };
const file = new URL('../docs/playable-l03-p0d/search-results.json', import.meta.url);
const encoded = JSON.stringify(report, null, 2) + '\n';
if (process.argv.includes('--write-results')) { mkdirSync(new URL('.', file), { recursive: true }); writeFileSync(file, encoded); }
else assert.equal(readFileSync(file, 'utf8'), encoded, 'P0d complete search output drift');
console.log(encoded);
