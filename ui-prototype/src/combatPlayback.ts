import { useCallback, useEffect, useRef, useState } from "react";
import { permitsClip } from "./combatIdentity";

export type Point = { x: number; y: number };
export type ClipKind = "physical" | "magicMissile";
export type Stage =
  | "move"
  | "windup"
  | "release"
  | "contact"
  | "impact"
  | "reaction"
  | "recovery";
export type Clip = {
  kind: ClipKind;
  actor: string;
  target: string;
  targets?: string[];
  from: Point;
  to: Point;
  committed: boolean;
};
export type Playback = Clip & {
  stage: Stage;
  progress: number;
  elapsed: number;
  sequence: number;
};
export const clipTiming = {
  physical: [880, 580, 180, 34, 88, 260, 680],
  magicMissile: [0, 1100, 760, 0, 88, 330, 680],
} satisfies Record<ClipKind, number[]>;
const stages: Stage[] = [
  "move",
  "windup",
  "release",
  "contact",
  "impact",
  "reaction",
  "recovery",
];

// One clock drives both actors, contact, VFX and the sole game-state boundary.
export function useCombatPlayback() {
  const [playback, setPlayback] = useState<Playback | null>(null);
  const [reduced, setReduced] = useState(
    () => matchMedia("(prefers-reduced-motion: reduce)").matches,
  );
  const reducedRef = useRef(reduced);
  const active = useRef<{
    clip: Clip;
    impact: () => void;
    done: () => void;
    impacted: boolean;
    started: number;
    sequence: number;
  } | null>(null);
  const raf = useRef(0),
    sequence = useRef(0);
  const cancel = useCallback(() => {
    cancelAnimationFrame(raf.current);
    active.current = null;
    setPlayback(null);
  }, []);
  useEffect(() => {
    const query = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => {
      reducedRef.current = query.matches;
      setReduced(query.matches);
    };
    query.addEventListener("change", change);
    return () => {
      query.removeEventListener("change", change);
      cancelAnimationFrame(raf.current);
      active.current = null;
    };
  }, []);
  const start = useCallback(
    (
      clip: Clip,
      impact: () => void = () => {},
      done: () => void = () => {},
    ) => {
      if (active.current || !permitsClip(clip)) return false;
      const current = {
        clip,
        impact,
        done,
        impacted: false,
        started: performance.now(),
        sequence: ++sequence.current,
      };
      active.current = current;
      const travels = clip.from.x !== clip.to.x || clip.from.y !== clip.to.y;
      setPlayback({
        ...clip,
        stage: travels ? "move" : "windup",
        progress: 0,
        elapsed: 0,
        sequence: current.sequence,
      });
      const tick = (now: number) => {
        if (active.current !== current) return;
        const durations = reducedRef.current
          ? [0, 0, 0, 0, 80, 0, 80]
          : [...clipTiming[clip.kind]];
        if (!travels) durations[0] = 0;
        const elapsed = now - current.started;
        const impactAt = durations.slice(0, 4).reduce((a, b) => a + b, 0);
        const total = durations.reduce((a, b) => a + b, 0);
        let index = 0,
          before = 0;
        while (
          index < stages.length - 1 &&
          elapsed >= before + durations[index]
        )
          before += durations[index++];
        if (!current.impacted && elapsed >= impactAt) {
          current.impacted = true;
          current.impact();
        }
        if (elapsed >= total) {
          active.current = null;
          setPlayback(null);
          current.done();
          return;
        }
        setPlayback({
          ...clip,
          stage: stages[index],
          progress: Math.min(
            1,
            (elapsed - before) / Math.max(1, durations[index]),
          ),
          elapsed,
          sequence: current.sequence,
        });
        raf.current = requestAnimationFrame(tick);
      };
      raf.current = requestAnimationFrame(tick);
      return true;
    },
    [],
  );
  return { playback, busy: playback !== null, reduced, start, cancel };
}
