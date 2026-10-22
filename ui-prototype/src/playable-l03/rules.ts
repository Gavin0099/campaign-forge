// P0 only: provisional, original occupancy rules; not SRD/G005 or story state.
import { sceneRows } from "../l03Scene.ts";

export type Cell = Readonly<{ x: number; y: number }>;
export type Route = "open" | "sealed";
export type Unit = Readonly<{
  id: string; side: "ally" | "enemy"; cell: Cell; alive: boolean;
}>;
// P0c experiments only. Omitted by default so P0/P0b serialized states stay identical.
export type RulesConfig = Readonly<{ blockAlliedPassage: boolean;
  p0c?: Readonly<{ survivalTurns?: 5 | 6; requiredHoldTurns?: number; thomaStartsWest?: boolean }>;
  p0d?: Readonly<{ blockedTurnsBeforeBreakout: number }>;
}>;
export type MapDef = Readonly<{
  rows: readonly string[]; winch: Cell; wagon: Cell; exit: Cell;
}>;
export const MAP: MapDef = Object.freeze({
  rows: Object.freeze([...sceneRows]),
  winch: Object.freeze({ x: 2, y: 1 }),
  wagon: Object.freeze({ x: 8, y: 4 }),
  exit: Object.freeze({ x: 0, y: 4 }),
});
export const DEFAULT_CONFIG: RulesConfig = Object.freeze({ blockAlliedPassage: true });
// One fixed PoC deployment shared by both map modes. Only open has a turn loop.
// The two initial knights and three allies use the reviewed spec's positions.
const DEPLOYMENT: readonly Unit[] = [
  { id: "karen", side: "ally", cell: { x: 2, y: 5 }, alive: true },
  { id: "lace", side: "ally", cell: { x: 1, y: 3 }, alive: true },
  { id: "thoma", side: "ally", cell: { x: 1, y: 4 }, alive: true },
  { id: "knight-1", side: "enemy", cell: { x: 1, y: 8 }, alive: true },
  { id: "knight-2", side: "enemy", cell: { x: 3, y: 8 }, alive: true },
];
export type State = Readonly<{
  route: Route; config: RulesConfig; turn: number;
  status: "playing" | "success" | "failure";
  progress: number; units: readonly Unit[]; moved: readonly string[];
  holdStreak?: number;
  blockedTurns?: Readonly<Record<string, number>>;
}>;
export type Event =
  | { type: "move"; unit: string; path: readonly Cell[] }
  | { type: "intent"; unit: string; target: "winch"; reason: "turn-winch" | "approach" | "blocked" }
  | { type: "breakout"; unit: string; blockedTurns: number; path: readonly Cell[];
      swapped?: { unit: string; from: Cell; to: Cell } }
  | { type: "progress"; delta: number; total: number }
  | { type: "turn"; completed: number }
  | { type: "result"; status: "success" | "failure" }
  | { type: "retry" };
export type Result = Readonly<{
  ok: boolean; state: State; events: readonly Event[]; reason?: string;
}>;
export type Command =
  | { type: "move"; turn: number; unit: string; to: Cell }
  | { type: "resolve"; turn: number }
  | { type: "retry" };
export const key = (p: Cell) => `${p.x},${p.y}`;
const same = (a: Cell, b: Cell) => key(a) === key(b);
const distance = (a: Cell, b: Cell) => Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
// Fixed tie order makes all equal-cost choices reproducible.
export const neighbors = (p: Cell): Cell[] => [
  { x: p.x, y: p.y - 1 }, { x: p.x - 1, y: p.y },
  { x: p.x + 1, y: p.y }, { x: p.x, y: p.y + 1 },
];
export function walkable(p: Cell, route: Route): boolean {
  if (!Number.isInteger(p.x) || !Number.isInteger(p.y)) return false;
  if (p.y < 0 || p.y >= MAP.rows.length || p.x < 0 || p.x >= MAP.rows[0].length) return false;
  const tile = MAP.rows[p.y]?.[p.x];
  return !!tile && tile !== "~" &&
    !(route === "open" && p.y === 4 && (p.x === 4 || p.x === 5));
}
export function initialState(route: Route = "open", config = DEFAULT_CONFIG): State {
  const experiment = config.p0c;
  const limit = experiment?.survivalTurns ?? 5;
  const hold = experiment?.requiredHoldTurns ?? 0;
  if (![5, 6].includes(limit) || !Number.isInteger(hold) || hold < 0 || hold > limit)
    throw new Error("invalid-P0c-config");
  const pressure = config.p0d?.blockedTurnsBeforeBreakout;
  if (config.p0d && (!Number.isSafeInteger(pressure) || pressure! < 1))
    throw new Error("invalid-P0d-config");
  return { route, config: { ...config }, turn: 1, status: "playing", progress: 0,
    units: DEPLOYMENT.map(u => ({ ...u, cell: experiment?.thomaStartsWest && u.id === "thoma"
      ? { x: 0, y: 4 } : { ...u.cell } })), moved: [], ...(hold ? { holdStreak: 0 } : {}),
    ...(config.p0d ? { blockedTurns: {} } : {}) };
}
// Bounded BFS; destinations always empty, even when allied transit is enabled.
export function findPath(state: State, actor: Unit, to: Cell): Cell[] | undefined {
  if (!walkable(to, state.route) || state.units.some(u =>
    u.alive && u.id !== actor.id && same(u.cell, to))) return undefined;
  const queue: Cell[][] = [[actor.cell]], seen = new Set([key(actor.cell)]);
  for (let i = 0; i < queue.length; i++) {
    const path = queue[i], here = path[path.length - 1];
    if (same(here, to)) return path;
    for (const next of neighbors(here)) {
      if (!walkable(next, state.route) || seen.has(key(next))) continue;
      const occupant = state.units.find(u => u.alive && u.id !== actor.id && same(u.cell, next));
      if (occupant && (state.config.blockAlliedPassage || occupant.side !== actor.side)) continue;
      seen.add(key(next));
      queue.push([...path, next]);
    }
  }
  return undefined;
}
const rejected = (state: State, reason: string): Result => ({ ok: false, state, events: [], reason });

// D experiment: after N consecutive blocked phases, take ONE bounded breakout.
// Ignore living allies only when planning; other enemies remain obstacles.
// Travel <=3 cells, stop at the FIRST ally, swapping it into the preceding cell.
// Shortest approach and path ties use the existing N/W/E/S order. No damage.
function breakout(state: State, enemy: Unit, streak: number): { state: State; event?: Event } {
  const planning = { ...state, config: { ...state.config, blockAlliedPassage: true },
    units: state.units.filter(u => u.side === "enemy") };
  const path = neighbors(MAP.winch).map(to => findPath(planning, enemy, to))
    .filter((p): p is Cell[] => !!p).sort((a, b) => a.length - b.length)[0];
  if (!path || path.length < 2) return { state };
  let steps = Math.min(3, path.length - 1);
  let swapped: { unit: string; from: Cell; to: Cell } | undefined;
  for (let i = 1; i <= steps; i++) {
    const ally = state.units.find(u => u.alive && u.side === "ally" && same(u.cell, path[i]));
    if (ally) { steps = i; swapped = { unit: ally.id, from: ally.cell, to: path[i - 1] }; break; }
  }
  return { state: { ...state, units: state.units.map(u => u.id === enemy.id
    ? { ...u, cell: path[steps] } : u.id === swapped?.unit ? { ...u, cell: swapped.to } : u) },
    event: { type: "breakout", unit: enemy.id, blockedTurns: streak, path: path.slice(0, steps + 1),
      ...(swapped ? { swapped } : {}) } };
}

export function command(state: State, input: Command): Result {
  if (input.type === "retry") {
    if (state.status === "playing") return rejected(state, "battle-not-finished");
    return { ok: true, state: initialState(state.route, state.config), events: [{ type: "retry" }] };
  }
  if (state.status !== "playing") return rejected(state, "battle-finished");
  if (input.turn !== state.turn) return rejected(state, "stale-turn");
  if (input.type === "resolve") return resolve(state, input.turn);
  const actor = state.units.find(u => u.id === input.unit && u.alive && u.side === "ally");
  if (!actor) return rejected(state, "not-living-ally");
  if (state.moved.includes(actor.id)) return rejected(state, "already-moved");
  const path = findPath(state, actor, input.to);
  if (!path || path.length < 2 || path.length > 4) return rejected(state, "illegal-move");
  return { ok: true, state: { ...state,
    units: state.units.map(u => u.id === actor.id ? { ...u, cell: { ...input.to } } : u),
    moved: [...state.moved, actor.id] }, events: [{ type: "move", unit: actor.id, path }] };
}

// Atomic enemy -> objective -> terminal/next-turn transition. No presentation work.
export function resolve(state: State, expectedTurn: number): Result {
  if (state.status !== "playing") return rejected(state, "battle-finished");
  if (expectedTurn !== state.turn) return rejected(state, "stale-turn");
  if (state.route !== "open") return rejected(state, "sealed-map-only-in-P0");
  let current = state;
  const events: Event[] = [];
  const threshold = state.config.p0d?.blockedTurnsBeforeBreakout;
  const blockedTurns = { ...state.blockedTurns };
  const blocked = (enemy: Unit) => {
    if (threshold === undefined) return;
    const streak = Math.min(threshold, (blockedTurns[enemy.id] ?? 0) + 1);
    blockedTurns[enemy.id] = streak;
    if (streak < threshold) return;
    const result = breakout(current, enemy, streak);
    if (result.event) { current = result.state; events.push(result.event); blockedTurns[enemy.id] = 0; }
  };
  // Only knights adjacent at phase START contribute; arriving grants a reaction turn.
  const contributors = state.units.filter(u => u.alive && u.side === "enemy" && distance(u.cell, MAP.winch) === 1);
  for (const enemy of state.units.filter(u => u.alive && u.side === "enemy")) {
    if (contributors.some(u => u.id === enemy.id)) {
      events.push({ type: "intent", unit: enemy.id, target: "winch", reason: "turn-winch" });
      if (threshold !== undefined) blockedTurns[enemy.id] = 0;
      continue;
    }
    const paths = neighbors(MAP.winch).map(to => findPath(current, enemy, to))
      .filter((p): p is Cell[] => !!p).sort((a, b) => a.length - b.length);
    const path = paths[0];
    events.push({ type: "intent", unit: enemy.id, target: "winch", reason: path ? "approach" : "blocked" });
    if (!path) { blocked(enemy); continue; }
    // With allied transit allowed, never end a partial move inside another unit.
    let steps = Math.min(3, path.length - 1);
    while (steps > 0 && current.units.some(u => u.alive && u.id !== enemy.id && same(u.cell, path[steps]))) steps--;
    if (!steps) { blocked(enemy); continue; }
    if (threshold !== undefined) blockedTurns[enemy.id] = 0;
    const traveled = path.slice(0, steps + 1);
    current = { ...current, units: current.units.map(u => u.id === enemy.id ? { ...u, cell: traveled[steps] } : u) };
    events.push({ type: "move", unit: enemy.id, path: traveled });
  }
  const progress = current.progress + contributors.length;
  const limit = state.config.p0c?.survivalTurns ?? 5;
  const hold = state.config.p0c?.requiredHoldTurns ?? 0;
  const held = current.units.some(u => u.alive && u.side === "ally" && distance(u.cell, MAP.winch) === 1);
  const holdStreak = held && progress < 3 ? (state.holdStreak ?? 0) + 1 : 0;
  // Loss takes precedence if the failure threshold is reached on the last turn.
  const status = progress >= 3 ? "failure" : state.turn >= limit
    ? (holdStreak >= hold ? "success" : "failure") : "playing";
  events.push({ type: "progress", delta: contributors.length, total: progress }, { type: "turn", completed: state.turn });
  if (status !== "playing") events.push({ type: "result", status });
  return { ok: true, state: { ...current, progress, status,
    turn: status === "playing" ? state.turn + 1 : state.turn, moved: [],
    ...(hold ? { holdStreak } : {}), ...(threshold === undefined ? {} : { blockedTurns }) }, events };
}
