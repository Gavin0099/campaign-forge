import { useCallback, useEffect, useRef, useState } from "react";
import type { Playback } from "./combatPlayback";

// Original, quiet synthesis; no downloaded samples or ambient audio permission.
export function useCombatSound(clip: Playback | null, reduced: boolean) {
  const [enabled, setEnabled] = useState(false),
    [error, setError] = useState("");
  const context = useRef<AudioContext | null>(null);
  const sources = useRef(new Set<OscillatorNode>());
  const stop = useCallback(() => {
    for (const source of sources.current) {
      try {
        source.stop();
      } catch {}
      source.disconnect();
    }
    sources.current.clear();
  }, []);
  const toggle = useCallback(async () => {
    if (enabled) {
      stop();
      setEnabled(false);
      await context.current?.suspend();
      return;
    }
    try {
      context.current ||= new AudioContext();
      await context.current.resume();
      setEnabled(true);
      setError("");
    } catch {
      setError("音效暫時無法開啟；演出仍可播放。");
    }
  }, [enabled, stop]);
  useEffect(() => {
    if (!enabled || reduced || !clip) {
      stop();
      return;
    }
    const ctx = context.current;
    if (!ctx || ctx.state !== "running") return;
    const tone = (
      frequency: number,
      to: number,
      seconds: number,
      volume: number,
      type: OscillatorType,
      delay = 0,
    ) => {
      const now = ctx.currentTime + delay,
        oscillator = ctx.createOscillator(),
        envelope = ctx.createGain();
      oscillator.type = type;
      oscillator.frequency.setValueAtTime(frequency, now);
      oscillator.frequency.exponentialRampToValueAtTime(to, now + seconds);
      envelope.gain.setValueAtTime(0, now);
      envelope.gain.linearRampToValueAtTime(volume, now + 0.012);
      envelope.gain.exponentialRampToValueAtTime(0.0001, now + seconds);
      oscillator.connect(envelope);
      envelope.connect(ctx.destination);
      oscillator.onended = () => {
        sources.current.delete(oscillator);
        oscillator.disconnect();
        envelope.disconnect();
      };
      sources.current.add(oscillator);
      oscillator.start(now);
      oscillator.stop(now + seconds + 0.02);
    };
    if (clip.kind === "physical") {
      if (clip.stage === "release") tone(260, 75, 0.18, 0.018, "triangle");
      if (clip.stage === "impact") {
        tone(110, 36, 0.2, 0.055, "sine");
        tone(740, 240, 0.12, 0.013, "triangle");
      }
    } else {
      if (clip.stage === "windup")
        [330, 440, 550].forEach((f, i) =>
          tone(f, f * 1.12, 0.36, 0.013, "sine", i * 0.1),
        );
      if (clip.stage === "release") tone(550, 880, 0.5, 0.018, "sine");
      if (clip.stage === "impact")
        [220, 330, 440].forEach((f) =>
          tone(f, f * 0.65, 0.22, 0.016, "triangle"),
        );
    }
  }, [clip?.sequence, clip?.stage, enabled, reduced, stop]);
  useEffect(
    () => () => {
      stop();
      void context.current?.close();
    },
    [stop],
  );
  return { enabled, error, toggle };
}
