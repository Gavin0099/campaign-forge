import { useId } from "react";
import frames from "./shienFrames.json";
import { Playback } from "./combatPlayback";

export function actorFrame(id: string, clip: Playback | null, idle: number) {
  if (!clip) return [0, idle % 6];
  const { stage, progress: p } = clip;
  if (
    (clip.target === id &&
      clip.actor !== id &&
      (stage === "impact" || stage === "recovery")) ||
    (clip.actor === id && clip.kind === "hit")
  )
    return [
      3,
      stage === "recovery"
        ? 2 + Math.min(3, Math.floor(p * 4))
        : Math.min(1, Math.floor(p * 2)),
    ];
  if (clip.actor !== id) return [0, idle % 6];
  if (stage === "move") return [1, Math.floor(clip.elapsed / 110) % 6];
  const row = clip.kind === "physical" ? 2 : 4;
  return [
    row,
    stage === "windup"
      ? Math.min(1, Math.floor(p * 2))
      : stage === "release"
        ? 2
        : stage === "impact"
          ? 3
          : 4 + Math.min(1, Math.floor(p * 2)),
  ];
}
export function AnimatedActor({
  clip,
  idle,
  reduced,
}: {
  clip: Playback | null;
  idle: number;
  reduced: boolean;
}) {
  const id = useId().replace(/:/g, "");
  const [row, col] = actorFrame("shien", reduced ? null : clip, idle);
  const frame = frames.frames[row * 6 + col];
  return (
    <svg
      x="-85"
      y="-140"
      width="170"
      height="140"
      viewBox="-140 -235 280 235"
      data-pose={`${row}:${col}`}
      className="animated-actor"
    >
      <defs>
        <clipPath id={id}>
          <rect
            x={frame.x - 2}
            y={frame.y - 2}
            width={frame.width + 4}
            height={frame.height + 4}
          />
        </clipPath>
      </defs>
      <g transform={`translate(${-frame.anchorX} ${-frame.anchorY})`}>
        <image
          href="/art/shien-actions-v3.png"
          width={frames.width}
          height={frames.height}
          clipPath={`url(#${id})`}
        />
      </g>
    </svg>
  );
}
