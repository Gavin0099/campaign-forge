import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { variants, startFor, summarize, boundedMoves } from './playable-l03-p2-support.mjs';
import { turnOnePlacements, oneMoveCandidates, replay } from './playable-l03-p0c-support.mjs';
import { DEFAULT_CONFIG, initialState } from '../src/playable-l03/rules.ts';
import { legalMoves, cost } from './playable-l03-p0b-support.mjs';
import { reactionEvidence } from './playable-l03-p2-support.mjs';

// Keep as opt-in evidence only. A causal witness is necessary for THIN; cheap
// <=2-command wins still earn CHEESE even when that local key gate is achieved.
const start = startFor(variants[0].config);
const rearDelay = [
  { type: 'move', turn: 1, unit: 'karen', to: { x: 1, y: 5 } },
  { type: 'move', turn: 1, unit: 'lace', to: { x: 3, y: 4 } },
  { type: 'move', turn: 2, unit: 'karen', to: { x: 2, y: 5 } },
];
const cases = {};
cases.turnOneThenWait = summarize(turnOnePlacements(start), start);
console.log('T1 complete');
cases.atMostOneMove = summarize(oneMoveCandidates(start), start);
console.log('<=1 complete');
cases.atMostTwoMoves = boundedMoves(start, 2);
console.log('<=2 complete');
cases.atMostThreeMoves = boundedMoves(start, 3);
console.log('<=3 complete');
const rear = replay(rearDelay, start);
assert(rear.legal);
// Separate directed probe: retain the original P0 defense prefix, then try <=2
// reactions on a telegraphed turn. Stops at the first causal witness; NOT an
// exhaustive four/six-command search and never included in the W/L table.
const original = [
  { type: 'move', turn: 1, unit: 'lace', to: { x: 1, y: 1 } },
  { type: 'move', turn: 1, unit: 'thoma', to: { x: 2, y: 2 } },
  { type: 'move', turn: 1, unit: 'karen', to: { x: 3, y: 3 } },
  { type: 'move', turn: 2, unit: 'karen', to: { x: 3, y: 1 } },
];
let directedGate = null, singlesExamined = 0, pairsExamined = 0;
outer: for (const r of replay(original, start).records) {
  if (r.command?.type !== 'resolve' || r.state.status !== 'playing' || !r.events.some(e => e.intent === 'prepare-breakout')) continue;
  const candidate = moves => [...original.filter(c => c.turn <= r.command.turn), ...moves,
    ...original.filter(c => c.turn > r.command.turn)];
  const firsts = legalMoves(r.state);
  for (const first of firsts) {
    singlesExamined++;
    directedGate = reactionEvidence(candidate([first.input]), start);
    if (directedGate) break outer;
  }
  for (const first of firsts) for (const second of legalMoves(first.next.state)) {
    pairsExamined++;
    directedGate = reactionEvidence(candidate([first.input, second.input]), start);
    if (directedGate) break outer;
  }
}
const gate = Object.values(cases).find(c => c.keyGateWitness)?.keyGateWitness ?? directedGate;
const gateTrace = gate && replay(gate.commands, start);
const gateCost = gateTrace && cost(gateTrace.records.filter(r => r.command?.type === 'move')
  .map(r => ({ input: r.command, tiles: r.events[0].path.length - 1 })));
const report = { schema: 1, config: start.config, variant: 'A+P2',
  costOrder: 'commands, distinct voluntarily moved allies, path tiles',
  method: 'P0d exhaustive bounded harness copied at 2dc92b6; state key includes P2 memory; full party; spaces overlap',
  cases, rearDelay: { commands: rearDelay, status: rear.state.status, progress: rear.state.progress },
  directedProbe: { original, singlesExamined, pairsExamined, stopAtFirstWitness: true, exhaustive: false, witnessCost: gateCost },
  keyGate: gate, verdict: !gate ? 'NO_REDECISION' : cases.atMostTwoMoves.wins ? 'CHEESE' : 'THIN' };
const output = new URL('../docs/playable-l03-p2/', import.meta.url);
mkdirSync(output, { recursive: true });
writeFileSync(new URL('search-results.json', output), JSON.stringify(report, null, 2) + '\n');
const traces = [{ name: 'rear-delay', ...rear }];
if (gate) {
  traces.push({ name: 'key-gate-react', ...replay(gate.commands, start) },
    { name: 'key-gate-ignore', ...replay(gate.ignoredCommands, start) },
    { name: 'key-gate-no-P2', ...replay(gate.ignoredCommands, initialState('open', { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 } })) });
}
writeFileSync(new URL('witnesses.jsonl', output), traces.map(t => JSON.stringify(t)).join('\n') + '\n');
console.log(JSON.stringify(Object.fromEntries(Object.entries(cases).map(([k, v]) => [k, {
  wins: v.wins, losses: v.losses, min: v.minimumCostWin, ties: v.bestWinTies,
  reactions: v.cheapestWinsRequiringTelegraphReaction }]))));
console.log(`verdict=${report.verdict}; rearDelay=${rear.state.status}`);
