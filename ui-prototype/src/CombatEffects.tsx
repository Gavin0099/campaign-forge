import { Playback } from "./combatPlayback";

type XY = { x: number; y: number };
const mix = (a: number, b: number, t: number) => a + (b - a) * t;
export function CombatEffects({
  clip,
  source,
  target,
  direction,
}: {
  clip: Playback;
  source: XY;
  target: XY;
  direction: "cartography" | "ember";
}) {
  const { stage, progress: p, kind } = clip;
  const windup = stage === "windup",
    release = stage === "release",
    impact = stage === "impact";
  const recovery = stage === "recovery";
  const ink = direction === "cartography";
  const attackColor = ink ? "#86f8ed" : "#ffb759";
  const wardColor = ink ? "#efb18d" : "#f3e3b9";
  if (stage === "move")
    return (
      <g className="footfalls" aria-hidden="true">
        {[0, 1, 2].map((i) => (
          <ellipse
            key={i}
            cx={mix(source.x, target.x, p) - i * 9}
            cy={mix(source.y, target.y, p) + 4}
            rx={4 + i * 2}
            ry={2}
            fill="#dbc792"
            opacity={(1 - p) * 0.3}
          />
        ))}
      </g>
    );
  const center = windup
    ? { x: source.x + 24, y: source.y - 75 }
    : { x: target.x, y: target.y - 65 };
  return (
    <g
      className={`combat-effects effect-${kind}`}
      data-effect={kind}
      data-stage={stage}
      pointerEvents="none"
      aria-hidden="true"
    >
      {kind === "physical" && (
        <>
          {(release || impact) && (
            <g
              transform={`translate(${target.x} ${target.y - 65}) rotate(-24)`}
            >
              <path
                d="M-74 30 Q-12 -63 72 -22 Q0 -16 -74 30"
                fill="#fff1c5"
                opacity={impact ? 1 - p : 0.95}
              />
              <path
                d="M-83 40 Q-15 -61 83 -28"
                fill="none"
                stroke={ink ? "#e5c48d" : "#ef945d"}
                strokeWidth="5"
              />
              {impact &&
                [0, 1, 2, 3, 4, 5].map((i) => (
                  <path
                    key={i}
                    d={`M${Math.cos(i) * 22} ${Math.sin(i) * 22}l${Math.cos(i) * (28 + p * 30)} ${Math.sin(i) * (28 + p * 30)}`}
                    stroke="#fff4d7"
                    strokeWidth="3"
                    opacity={1 - p}
                  />
                ))}
            </g>
          )}
          {windup && (
            <path
              d={`M${source.x + 26} ${source.y - 82}q-30 -22 -45 8`}
              className="ink-gesture"
              strokeDasharray={`${p * 60} 90`}
            />
          )}
        </>
      )}
      {kind === "arcane" && (
        <>
          {windup && (
            <g transform={`translate(${center.x} ${center.y})`}>
              <circle
                r={12 + p * 22}
                fill={attackColor}
                opacity={0.15 + p * 0.2}
              />
              <circle
                r={24 + p * 22}
                fill="none"
                stroke={attackColor}
                strokeWidth="2"
                strokeDasharray="9 6"
                transform={`rotate(${p * 120})`}
              />
              <path
                d={
                  ink
                    ? "M0 -38L33 20H-33ZM0 -25V36M-40 0H40"
                    : "M0 -38L9 -9 38 0 9 9 0 38 -9 9 -38 0 -9 -9Z"
                }
                fill="none"
                stroke={attackColor}
                strokeWidth="2"
                opacity={p}
              />
              {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
                <circle
                  key={i}
                  cx={Math.cos((i * Math.PI) / 4 + p * 2) * (70 - p * 45)}
                  cy={Math.sin((i * Math.PI) / 4 + p * 2) * (70 - p * 45)}
                  r="2.5"
                  fill={attackColor}
                />
              ))}
            </g>
          )}
          {release && (
            <g>
              <path
                d={`M${source.x + 24} ${source.y - 75}Q${mix(source.x, target.x, 0.5)} ${Math.min(source.y, target.y) - 160} ${target.x} ${target.y - 65}`}
                fill="none"
                stroke={attackColor}
                strokeWidth="14"
                opacity=".12"
              />
              <g
                transform={`translate(${mix(source.x + 24, target.x, p)} ${mix(source.y - 75, target.y - 65, p) - Math.sin(p * Math.PI) * 60}) rotate(-25)`}
              >
                <path d="M-88 0L-16 -9 20 0 -16 9Z" fill={attackColor} />
                <path d="M-45 0H18" stroke="#fff9df" strokeWidth="3" />
                {ink && (
                  <path
                    d="M-18 -17L20 0 -18 17M-33 -12L-10 0 -33 12"
                    fill="none"
                    stroke={attackColor}
                    strokeWidth="2"
                  />
                )}
              </g>
            </g>
          )}
          {(impact || recovery) && (
            <g
              transform={`translate(${target.x} ${target.y - 65})`}
              opacity={recovery ? 1 - p : 1}
            >
              <circle
                r={impact ? 15 + p * 65 : 80}
                fill="none"
                stroke={attackColor}
                strokeWidth={impact ? 10 - p * 8 : 1}
              />
              <path
                d={
                  ink
                    ? "M0 -70L18 -20 62 -34 26 5 45 48 0 27 -35 61 -23 13 -67 -8 -18 -15Z"
                    : "M0 -65L12 -14 60 0 12 14 0 65 -12 14 -60 0 -12 -14Z"
                }
                fill={attackColor}
                opacity={impact ? (1 - p) * 0.8 : 0.12}
              />
              {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => (
                <path
                  key={i}
                  d={`M${Math.cos(i) * 30} ${Math.sin(i) * 30}l${Math.cos(i) * (20 + p * 30)} ${Math.sin(i) * (20 + p * 30)}`}
                  stroke={attackColor}
                  strokeWidth="2"
                />
              ))}
            </g>
          )}
        </>
      )}
      {kind === "ward" && (
        <g transform={`translate(${target.x} ${target.y})`}>
          <ellipse
            cy="-1"
            rx={windup ? 25 + p * 25 : 52}
            ry="22"
            fill={wardColor}
            opacity={recovery ? (1 - p) * 0.16 : 0.16}
          />
          <g
            transform="scale(1 .45)"
            stroke={wardColor}
            fill="none"
            opacity={recovery ? 1 - p : 1}
          >
            <circle
              r="56"
              strokeWidth="2"
              strokeDasharray={ink ? "60 5 8 5" : "3 8"}
            />
            <path
              d={
                ink
                  ? "M0 -45L39 23H-39ZM0 -56V56M-56 0H56"
                  : "M0 -48Q56 -20 33 30Q0 60 -33 30Q-56 -20 0 -48Z"
              }
              strokeWidth="2"
            />
          </g>
          {!windup && (
            <g opacity={recovery ? 1 - p : 1}>
              <path
                d="M-40 -108Q0 -128 40 -108L34 -45Q18 -15 0 -5Q-18 -15 -34 -45Z"
                fill={wardColor}
                fillOpacity=".12"
                stroke={wardColor}
                strokeWidth="2.5"
                strokeDasharray={release ? `${p * 300} 300` : undefined}
              />
              <path
                d="M0 -100V-36M-22 -69H22"
                stroke={wardColor}
                strokeWidth="4"
              />
              {[0, 1, 2, 3, 4, 5].map((i) => (
                <path
                  key={i}
                  d={`M${(i - 2.5) * 18} ${-30 - ((p * 70 + i * 13) % 100)}v-12`}
                  stroke={wardColor}
                  opacity=".8"
                />
              ))}
            </g>
          )}
        </g>
      )}
    </g>
  );
}
