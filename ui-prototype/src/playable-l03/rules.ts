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
  enemyBehaviour?: "p2";
  detourThreshold?: number;
}>;
export type BreakoutPlan = Readonly<{
  ally: string; from: Cell; to: Cell; path: readonly Cell[]; preparedTurn: number;
}>;
export type EnemyPressure = Readonly<
  { stage: "blocked"; ally: string; cell: Cell } |
  { stage: "prepare-breakout"; plan: BreakoutPlan }
>;
export type EnemyIntent = Readonly<{
  type: "enemy-intent"; unit: string;
  behaviour: "target-interference" | "hunt-weak-point";
  intent: "approach" | "turn-winch" | "blocked" | "prepare-breakout" | "breakout" | "cancel-breakout";
  reason: string; targetTile: Cell; targetAlly?: string;
  plannedPath: readonly Cell[]; action: "move" | "wait" | "progress" | "swap";
  plan?: BreakoutPlan;
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
  enemyPressure?: Readonly<Record<string, EnemyPressure>>;
}>;
export type Event =
  | EnemyIntent
  | { type: "breakout"; unit: string; plan: BreakoutPlan }
  | { type: "move"; unit: string; path: readonly Cell[] }
  | { type: "intent"; unit: string; target: "winch"; reason: "turn-winch" | "approach" | "blocked" }
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
  if ((config.enemyBehaviour !== undefined && config.enemyBehaviour !== "p2") ||
    (config.detourThreshold !== undefined && (!Number.isSafeInteger(config.detourThreshold) || config.detourThreshold < 0)))
    throw new Error("invalid-P2-config");
  return { route, config: { ...config }, turn: 1, status: "playing", progress: 0,
    units: DEPLOYMENT.map(u => ({ ...u, cell: experiment?.thomaStartsWest && u.id === "thoma"
      ? { x: 0, y: 4 } : { ...u.cell } })), moved: [], ...(hold ? { holdStreak: 0 } : {}),
    ...(config.enemyBehaviour === "p2" ? { enemyPressure: {} } : {}) };
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

const approachPath = (state: State, enemy: Unit) => neighbors(MAP.winch)
  .map(to => findPath(state, enemy, to)).filter((p): p is Cell[] => !!p)
  .sort((a, b) => a.length - b.length)[0];

// P2 is opt-in. Planning ignores allies only to identify pressure and its FIRST
// blocker (P0d's swap geometry); execution always validates the advertised cells.
function p2Enemy(state: State, enemy: Unit, contributes: boolean): { state: State; events: Event[] } {
  const events: Event[] = [], memory = { ...state.enemyPressure };
  const previous = memory[enemy.id];
  delete memory[enemy.id];
  let current: State = { ...state, enemyPressure: memory };
  const emit = (intent: Omit<EnemyIntent, "type" | "unit">) =>
    events.push({ type: "enemy-intent", unit: enemy.id, ...intent });
  const move = (path: readonly Cell[]) => {
    if (path.length < 2) return;
    current = { ...current, units: current.units.map(u => u.id === enemy.id
      ? { ...u, cell: path[path.length - 1] } : u) };
    events.push({ type: "move", unit: enemy.id, path });
  };
  if (previous?.stage === "prepare-breakout") {
    const plan = previous.plan;
    const ally = state.units.find(u => u.id === plan.ally && u.alive && u.side === "ally");
    const invalid = !ally || !same(ally.cell, plan.from) ? "target-moved-or-absent"
      : !same(enemy.cell, plan.path[0]) ? "knight-displaced"
      : plan.preparedTurn !== state.turn - 1 ? "expired-telegraph"
      : plan.path.slice(1, -1).some(p => state.units.some(u => u.alive && u.id !== enemy.id && same(u.cell, p)))
        ? "advertised-path-occupied" : undefined;
    if (!invalid && !contributes) {
      emit({ behaviour: "hunt-weak-point", intent: "breakout", reason: "telegraph-still-valid",
        targetTile: plan.from, targetAlly: plan.ally, plannedPath: plan.path, action: "swap", plan });
      current = { ...current, units: current.units.map(u => u.id === enemy.id
        ? { ...u, cell: plan.from } : u.id === plan.ally ? { ...u, cell: plan.to } : u) };
      events.push({ type: "breakout", unit: enemy.id, plan });
      return { state: current, events };
    }
    emit({ behaviour: "hunt-weak-point", intent: "cancel-breakout", reason: invalid ?? "already-at-objective",
      targetTile: plan.from, targetAlly: plan.ally, plannedPath: [enemy.cell], action: "wait", plan });
  }
  if (contributes) {
    emit({ behaviour: "target-interference", intent: "turn-winch", reason: "adjacent-at-phase-start",
      targetTile: MAP.winch, plannedPath: [enemy.cell], action: "progress" });
    return { state: current, events };
  }
  const normal = approachPath(state, enemy);
  const direct = approachPath({ ...state, config: { ...state.config, blockAlliedPassage: true },
    units: state.units.filter(u => u.side === "enemy") }, enemy);
  const index = direct?.findIndex((p, i) => i > 0 && state.units.some(u =>
    u.alive && u.side === "ally" && same(u.cell, p))) ?? -1;
  const pressured = direct && index > 0 && (!normal || normal.length - direct.length > (state.config.detourThreshold ?? 1));
  if (pressured) {
    const ally = state.units.find(u => u.alive && u.side === "ally" && same(u.cell, direct[index]))!;
    const reason = normal ? `detour:${normal.length - direct.length}>${state.config.detourThreshold ?? 1}` : "direct-lane-blocked";
    if (previous?.stage === "blocked" && previous.ally === ally.id && same(previous.cell, ally.cell) && index <= 3) {
      const plan: BreakoutPlan = { ally: ally.id, from: ally.cell, to: direct[index - 1],
        path: direct.slice(0, index + 1), preparedTurn: state.turn };
      memory[enemy.id] = { stage: "prepare-breakout", plan };
      emit({ behaviour: "hunt-weak-point", intent: "prepare-breakout", reason,
        targetTile: ally.cell, targetAlly: ally.id, plannedPath: [enemy.cell], action: "wait", plan });
    } else {
      // Approach the blocker, but never enter its cell before a full telegraph turn.
      const path = direct.slice(0, Math.min(3, index - 1) + 1);
      memory[enemy.id] = { stage: "blocked", ally: ally.id, cell: ally.cell };
      emit({ behaviour: "hunt-weak-point", intent: "blocked",
        reason: previous ? `replan:${reason}` : reason, targetTile: ally.cell, targetAlly: ally.id,
        plannedPath: path, action: path.length > 1 ? "move" : "wait" });
      move(path);
    }
  } else {
    if (previous?.stage === "blocked") emit({ behaviour: "hunt-weak-point", intent: "cancel-breakout",
      reason: "pressure-cleared", targetTile: previous.cell, targetAlly: previous.ally,
      plannedPath: [enemy.cell], action: "wait" });
    let steps = Math.min(3, (normal?.length ?? 1) - 1);
    while (steps > 0 && state.units.some(u => u.alive && u.id !== enemy.id && same(u.cell, normal![steps]))) steps--;
    const path = normal?.slice(0, steps + 1) ?? [enemy.cell];
    emit({ behaviour: "target-interference", intent: steps ? "approach" : "blocked",
      reason: steps ? "shortest-open-approach" : "no-open-step", targetTile: MAP.winch,
      plannedPath: path, action: steps ? "move" : "wait" });
    move(path);
  }
  return { state: current, events };
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
  // Only knights adjacent at phase START contribute; arriving grants a reaction turn.
  const contributors = state.units.filter(u => u.alive && u.side === "enemy" && distance(u.cell, MAP.winch) === 1);
  for (const enemy of state.units.filter(u => u.alive && u.side === "enemy")) {
    if (state.config.enemyBehaviour === "p2") {
      const result = p2Enemy(current, enemy, contributors.some(u => u.id === enemy.id));
      current = result.state; events.push(...result.events);
      continue;
    }
    if (contributors.some(u => u.id === enemy.id)) {
      events.push({ type: "intent", unit: enemy.id, target: "winch", reason: "turn-winch" });
      continue;
    }
    const paths = neighbors(MAP.winch).map(to => findPath(current, enemy, to))
      .filter((p): p is Cell[] => !!p).sort((a, b) => a.length - b.length);
    const path = paths[0];
    events.push({ type: "intent", unit: enemy.id, target: "winch", reason: path ? "approach" : "blocked" });
    if (!path) continue;
    // With allied transit allowed, never end a partial move inside another unit.
    let steps = Math.min(3, path.length - 1);
    while (steps > 0 && current.units.some(u => u.alive && u.id !== enemy.id && same(u.cell, path[steps]))) steps--;
    if (!steps) continue;
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
    ...(hold ? { holdStreak } : {}) }, events };
}
