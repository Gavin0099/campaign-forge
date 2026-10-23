import { MAP, resolve, type Cell, type Event, type State, type Unit } from "./rules.ts";

export type FeedbackCue = { atMs: number; eventIndex: number } & (
  | { kind: "landing"; unit: string; cell: Cell }
  | { kind: "block"; unit: string }
  | { kind: "winch"; cell: Cell; total: number; delta: number }
);

// The same sequential path-step clock as the view. Intent takes no extra time;
// a landing and the next intent can share a boundary, in original event order.
export function buildFeedbackTimeline(events: readonly Event[], stepMs: number): FeedbackCue[] {
  if (!Number.isFinite(stepMs) || stepMs <= 0) throw new Error("invalid-step-duration");
  let atMs = 0;
  return events.flatMap((event, eventIndex): FeedbackCue[] => {
    if (event.type === "move") {
      atMs += Math.max(0, event.path.length - 1) * stepMs;
      return event.path.length > 1
        ? [{ atMs, eventIndex, kind: "landing", unit: event.unit, cell: event.path[event.path.length - 1] }] : [];
    }
    if (event.type === "intent" && event.reason === "blocked")
      return [{ atMs, eventIndex, kind: "block", unit: event.unit }];
    if (event.type === "progress" && event.delta > 0)
      return [{ atMs, eventIndex, kind: "winch", cell: MAP.winch, total: event.total, delta: event.delta }];
    return [];
  });
}

// A resolution marker describes only intents already reached by playback.
// The preview for a future turn must never leak into an earlier visual moment.
export function blockedAtEventIndex(events: readonly Event[], playedIndex: number): Set<string> {
  const blocked = new Set<string>();
  for (const event of events.slice(0, Math.max(0, playedIndex + 1))) {
    if (event.type !== "intent") continue;
    if (event.reason === "blocked") blocked.add(event.unit);
    else blocked.delete(event.unit);
  }
  return blocked;
}

// Reconstruct only presentation positions preceding this event. No turn,
// progress or rule state is committed by a feedback query.
export function stateBeforeEvent(state: State, events: readonly Event[], eventIndex: number): State {
  return events.slice(0, eventIndex).reduce((current, event) => event.type === "move" && event.path.length
    ? { ...current, units: current.units.map(u => u.id === event.unit ? { ...u, cell: event.path[event.path.length - 1] } : u) }
    : current, state);
}

export function confirmedContactBlocker(state: State, enemyId: string): Unit | undefined {
  const enemy = state.units.find(u => u.id === enemyId && u.alive && u.side === "enemy");
  if (!enemy) return undefined;
  // Query this enemy FIRST at its actual event position; earlier enemies have
  // already moved and must remain obstacles, rather than moving a second time.
  const query: State = { ...state, units: [enemy, ...state.units.filter(u => u.id !== enemyId)] };
  const reason = (s: State) => resolve(s, s.turn).events.find(e => e.type === "intent" && e.unit === enemyId);
  const baseline = reason(query);
  if (baseline?.type !== "intent" || baseline.reason !== "blocked") return undefined;
  const confirmed = state.units.filter(ally => {
    // A distant route obstruction is not physical contact at this enemy's feet.
    if (!ally.alive || ally.side !== "ally" ||
      Math.abs(ally.cell.x-enemy.cell.x)+Math.abs(ally.cell.y-enemy.cell.y) !== 1) return false;
    const opened = reason({ ...query, units: query.units.filter(u => u.id !== ally.id) });
    return opened?.type === "intent" && opened.reason === "approach";
  });
  // Ambiguous alternate openings do not identify one actual contact.
  return confirmed.length === 1 ? confirmed[0] : undefined;
}
