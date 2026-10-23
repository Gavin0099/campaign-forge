import { MAP, type Cell, type Event } from "./rules.ts";

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
