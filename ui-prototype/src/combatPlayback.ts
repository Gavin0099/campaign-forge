import { useCallback, useEffect, useRef, useState } from "react";

export type Point = { x: number; y: number };
export type ClipKind = "physical" | "arcane" | "ward" | "hit";
export type Stage = "move" | "windup" | "release" | "impact" | "recovery";
export type Clip = {
  kind: ClipKind;
  actor: string;
  target: string;
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
  physical: [800, 460, 240, 180, 520],
  arcane: [0, 900, 460, 360, 520],
  ward: [0, 720, 420, 560, 560],
  hit: [0, 0, 0, 400, 620],
} satisfies Record<ClipKind, number[]>;
const stages: Stage[] = ["move", "windup", "release", "impact", "recovery"];

// Visual clock only. Game state is owned by App and changes once at Impact.
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
  const raf = useRef(0);
  const sequence = useRef(0);
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
      if (active.current) return false; // Synchronous gate also catches two clicks in one React batch.
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
      let lastPaint = -100;
      const tick = (now: number) => {
        if (active.current !== current) return;
        const duration = reducedRef.current
          ? [0, 0, 0, 80, 80]
          : [...clipTiming[clip.kind]];
        if (!travels) duration[0] = 0;
        const elapsed = now - current.started;
        const impactAt = duration[0] + duration[1] + duration[2];
        if (!current.impacted && elapsed >= impactAt) {
          current.impacted = true;
          current.impact();
        }
        const total = duration.reduce((a, b) => a + b, 0);
        if (elapsed >= total) {
          active.current = null;
          setPlayback(null);
          current.done();
          return;
        }
        if (now - lastPaint >= 32) {
          let index = 0,
            before = 0;
          while (index < 4 && elapsed >= before + duration[index])
            before += duration[index++];
          setPlayback({
            ...clip,
            stage: stages[index],
            progress: Math.min(
              1,
              (elapsed - before) / Math.max(1, duration[index]),
            ),
            elapsed,
            sequence: current.sequence,
          });
          lastPaint = now;
        }
        raf.current = requestAnimationFrame(tick);
      };
      raf.current = requestAnimationFrame(tick);
      return true;
    },
    [],
  );
  return { playback, busy: playback !== null, reduced, start, cancel };
}
