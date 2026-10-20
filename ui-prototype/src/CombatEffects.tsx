import type { Playback, Point } from "./combatPlayback";
const mix = (a: number, b: number, p: number) => a + (b - a) * p;
const cubic = (a: Point, b: Point, c: Point, d: Point, t: number): Point => ({
  x:
    (1 - t) ** 3 * a.x +
    3 * (1 - t) ** 2 * t * b.x +
    3 * (1 - t) * t * t * c.x +
    t ** 3 * d.x,
  y:
    (1 - t) ** 3 * a.y +
    3 * (1 - t) ** 2 * t * b.y +
    3 * (1 - t) * t * t * c.y +
    t ** 3 * d.y,
});
export function CombatEffects({
  clip,
  source,
  targets,
}: {
  clip: Playback;
  source: Point;
  targets: Point[];
  direction?: "cartography" | "ember";
}) {
  const p = clip.progress,
    target = targets[0] || source;
  if (clip.kind === "physical") {
    // Small dust/sparks at the shared blade/chest contact. No flash or giant slash.
    if (!["contact", "impact", "reaction"].includes(clip.stage)) return null;
    const fade = clip.stage === "reaction" ? 1 - p : 1;
    return (
      <g
        data-effect="physical"
        className="combat-effect"
        pointerEvents="none"
        opacity={fade}
      >
        {[0, 1, 2, 3, 4].map((i) => (
          <path
            key={i}
            d={`M${target.x + (i - 2) * 2} ${target.y - 85}l${(i - 2) * 3} ${-6 - i * 2}`}
            stroke={i % 2 ? "#b99b61" : "#e8dab2"}
            strokeWidth="1.4"
          />
        ))}
      </g>
    );
  }
  const windup = clip.stage === "windup",
    flight = clip.stage === "release",
    hit = ["impact", "reaction", "recovery"].includes(clip.stage);
  const hand = { x: source.x + 39, y: source.y - 111 };
  return (
    <g
      data-effect="magicMissile"
      className="combat-effect magic-missiles"
      pointerEvents="none"
    >
      {targets.map((to, i) => {
        const end = { x: to.x - 10 + (i - 1) * 5, y: to.y - 85 + (i - 1) * 9 };
        const start = { x: hand.x + 8 + i * 10, y: hand.y - 26 + i * 24 };
        const c1 = { x: start.x + 90, y: start.y - 65 + (i - 1) * 30 },
          c2 = { x: end.x - 80, y: end.y - 70 + (i - 1) * 38 };
        const t = flight ? p : 0,
          pos = windup
            ? {
                x: mix(hand.x, start.x, Math.min(1, p * 1.5)),
                y: mix(hand.y, start.y, Math.min(1, p * 1.5)),
              }
            : cubic(start, c1, c2, end, t);
        const tail = cubic(start, c1, c2, end, Math.max(0, t - 0.13));
        const before = cubic(start, c1, c2, end, Math.max(0, t - 0.015));
        const angle = flight
          ? (Math.atan2(pos.y - before.y, pos.x - before.x) * 180) / Math.PI
          : -15 + (i - 1) * 14;
        const opacity = windup
          ? Math.min(1, Math.max(0, (p - i * 0.1) * 2.2))
          : flight
            ? 1
            : 0;
        return (
          <g
            key={i}
            data-missile={i + 1}
            data-target={clip.targets?.[i]}
            data-impact-x={end.x}
            data-impact-y={end.y}
          >
            {(windup || flight) && (
              <g opacity={opacity}>
                {flight && (
                  <path
                    d={`M${tail.x} ${tail.y}Q${mix(tail.x, pos.x, 0.5)} ${mix(tail.y, pos.y, 0.5) - 3} ${pos.x} ${pos.y}`}
                    stroke="#78cbd0"
                    strokeWidth="4"
                    opacity=".4"
                    fill="none"
                    strokeLinecap="round"
                  />
                )}
                <g transform={`translate(${pos.x} ${pos.y}) rotate(${angle})`}>
                  <ellipse rx="12" ry="6" fill="#84c9df" opacity=".14" />
                  <path
                    d="M-11 0Q-5 -5 2 -3L8 0L2 3Q-5 5 -11 0Z"
                    fill="#8ddde3"
                  />
                  <path
                    d="M-5 0L6 0"
                    stroke="#f1faf1"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                  />
                </g>
              </g>
            )}
            {hit && (
              <g
                transform={`translate(${end.x} ${end.y})`}
                opacity={
                  clip.stage === "recovery"
                    ? Math.max(0, 1 - p * 2)
                    : clip.stage === "reaction"
                      ? 1 - p * 0.8
                      : 1
                }
              >
                <ellipse
                  rx={clip.stage === "impact" ? 6 : 6 + p * 10}
                  ry={clip.stage === "impact" ? 9 : 9 + p * 12}
                  fill="none"
                  stroke="#a2e4e5"
                  strokeWidth="1.6"
                />
                {[0, 1, 2].map((n) => (
                  <path
                    key={n}
                    d={`M${(n - 1) * 3} -3l${(n - 1) * (7 + p * 10)} ${-8 - p * 14}`}
                    stroke="#d3efdf"
                    strokeWidth="1.6"
                  />
                ))}
              </g>
            )}
          </g>
        );
      })}
      {windup && (
        <g
          transform={`translate(${hand.x} ${hand.y})`}
          opacity={Math.sin(p * Math.PI) * 0.7}
        >
          <path
            d="M-8 6Q-17 -9 -5 -15M10 -3Q22 10 10 17"
            fill="none"
            stroke="#8dbec1"
            strokeWidth="1.5"
          />
        </g>
      )}
    </g>
  );
}
