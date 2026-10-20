import { useId } from "react";
import { mapRows, unitSeeds } from "./data";

type Point = { x: number; y: number };
type Unit = (typeof unitSeeds)[number] & { acted?: boolean };
type Props = {
  units: Unit[];
  selected: string | null;
  target: string | null;
  destination: Point | null;
  phase: "select" | "move" | "skill" | "confirm";
  moveCells: Set<string>;
  skillCells: Set<string>;
  feedback: { id: string; sequence: number } | null;
  onPick: (point: Point) => void;
};
const terrain = (t: string) =>
  ({ ".": "平地", F: "林地", R: "道路", "~": "河道" })[t];
const material = (t: string) =>
  ({ ".": "grass", F: "forest", R: "road", "~": "water" })[t];
export const project = (x: number, y: number) => ({
  x: 560 + (x - y) * 50,
  y: 115 + (x + y) * 25,
});
const diamond = (x: number, y: number) =>
  [project(x, y), project(x + 1, y), project(x + 1, y + 1), project(x, y + 1)]
    .map((p) => `${p.x},${p.y}`)
    .join(" ");
const coordinates = mapRows.flatMap((row, y) =>
  [...row].map((tile, x) => ({ x, y, tile })),
);
const spriteIndex = { shien: 0, lida: 1, olun: 2, scout: 3, guard: 4 };

function Scenery({
  column,
  x,
  y,
  width = 140,
}: {
  column: number;
  x: number;
  y: number;
  width?: number;
}) {
  const clip = useId().replace(/:/g, "");
  const point = project(x, y);
  return (
    <svg
      x={point.x - width / 2}
      y={point.y - width * 0.84}
      width={width}
      height={width}
      viewBox={`${column * 724} 0 724 724`}
      preserveAspectRatio="xMidYMax meet"
    >
      <defs>
        <clipPath id={clip}>
          <rect x={column * 724} width="724" height="724" />
        </clipPath>
      </defs>
      <image
        clipPath={`url(#${clip})`}
        href="/art/props-v2.png"
        width="2172"
        height="724"
      />
    </svg>
  );
}

function Sprite({
  unit,
  x,
  y,
  ghost = false,
  selected = false,
}: {
  unit: Unit;
  x: number;
  y: number;
  ghost?: boolean;
  selected?: boolean;
}) {
  const point = project(x + 0.5, y + 0.5);
  const max = unitSeeds.find((seed) => seed.id === unit.id)!.hp;
  const clip = useId().replace(/:/g, "");
  const column = spriteIndex[unit.id as keyof typeof spriteIndex];
  return (
    <g
      className={`board-unit ${unit.side} ${unit.acted ? "has-acted" : ""} ${ghost ? "ghost-unit" : ""} ${selected ? "is-selected" : ""}`}
      transform={`translate(${point.x} ${point.y})`}
      data-unit={ghost ? undefined : unit.id}
      data-x={x}
      data-y={y}
    >
      <ellipse className="unit-shadow" cy="2" rx="27" ry="11" />
      <ellipse className="faction-base" rx="28" ry="12" />
      <svg
        x="-49"
        y="-124"
        width="98"
        height="130"
        viewBox={`${column * 400} 180 400 560`}
        preserveAspectRatio="xMidYMax meet"
      >
        <defs>
          <clipPath id={clip}>
            <rect x={column * 400} width="400" height="800" />
          </clipPath>
        </defs>
        <image
          clipPath={`url(#${clip})`}
          href="/art/units-v2.png"
          width="2000"
          height="800"
        />
      </svg>
      {!ghost && (
        <g className="unit-vitals" transform="translate(-25 14)">
          <rect className="hp-track" width="50" height="5" rx="2" />
          <rect
            className="hp-fill"
            width={(50 * unit.hp) / max}
            height="5"
            rx="2"
          />
          <text x="-7" y="6" textAnchor="end">
            {unit.side === "ally" ? "◆" : "▲"}
          </text>
          <text x="57" y="6">
            {unit.hp}
          </text>
          {unit.acted && (
            <text className="spent-mark" x="25" y="22" textAnchor="middle">
              已行動
            </text>
          )}
        </g>
      )}
    </g>
  );
}

export function Battlefield({
  units,
  selected,
  target,
  destination,
  phase,
  moveCells,
  skillCells,
  feedback,
  onPick,
}: Props) {
  const id = useId().replace(/:/g, "");
  const actor = units.find((u) => u.id === selected);
  const drawingUnits = units
    .filter((u) => u.hp > 0)
    .sort((a, b) => a.x + a.y - b.x - b.y);
  return (
    <section className="battle-arena" aria-label="11 乘 9 戰場格線">
      <div className="arena-label" aria-hidden="true">
        <span>北岸渡口</span>
        <small>低地 / 裂潮前夕</small>
      </div>
      <div className="arena-compass" aria-hidden="true">
        N <span>↗</span>
      </div>
      <svg
        className="tactical-board"
        viewBox="60 70 1100 610"
        aria-label="渡口斜俯視戰場"
      >
        <defs>
          {["grass", "road", "water", "forest"].map((name, index) => (
            <pattern
              key={name}
              id={`${id}-${name}`}
              width="200"
              height="200"
              patternUnits="userSpaceOnUse"
              patternTransform="matrix(1 .5 -1 .5 560 115)"
            >
              <image
                href="/art/terrain-v2.png"
                width="400"
                height="400"
                x={index % 2 ? -200 : 0}
                y={index > 1 ? -200 : 0}
                preserveAspectRatio="none"
              />
            </pattern>
          ))}
          <pattern
            id={`${id}-move`}
            width="12"
            height="12"
            patternUnits="userSpaceOnUse"
            patternTransform="rotate(25)"
          >
            <path d="M0 0V12" stroke="#b5e9d8" strokeWidth="2" opacity=".3" />
          </pattern>
          <filter
            id={`${id}-shadow`}
            x="-30%"
            y="-30%"
            width="160%"
            height="180%"
          >
            <feDropShadow
              dx="0"
              dy="20"
              stdDeviation="16"
              floodColor="#040c0e"
              floodOpacity=".75"
            />
          </filter>
        </defs>
        <g
          aria-hidden="true"
          className="terrain-ground"
          filter={`url(#${id}-shadow)`}
        >
          <polygon
            points="110,340 660,615 1110,390 1110,412 660,642 110,365"
            fill="#252d27"
            stroke="#686951"
          />
          {coordinates.map(({ x, y, tile }) => (
            <polygon
              key={`${x},${y}`}
              points={diamond(x, y)}
              fill={`url(#${id}-${material(tile)})`}
              data-terrain={tile}
              data-x={x}
              data-y={y}
            />
          ))}
        </g>
        <g aria-hidden="true" className="river-banks">
          {coordinates
            .filter((c) => c.tile !== "~")
            .flatMap(({ x, y }) => {
              const edges = [
                {
                  water: mapRows[y - 1]?.[x] === "~",
                  a: project(x, y),
                  b: project(x + 1, y),
                },
                {
                  water: mapRows[y]?.[x + 1] === "~",
                  a: project(x + 1, y),
                  b: project(x + 1, y + 1),
                },
                {
                  water: mapRows[y + 1]?.[x] === "~",
                  a: project(x, y + 1),
                  b: project(x + 1, y + 1),
                },
                {
                  water: mapRows[y]?.[x - 1] === "~",
                  a: project(x, y),
                  b: project(x, y + 1),
                },
              ];
              return edges
                .filter((e) => e.water)
                .map((e, i) => (
                  <path
                    key={`${x},${y}-${i}`}
                    d={`M${e.a.x} ${e.a.y}L${e.b.x} ${e.b.y}`}
                  />
                ));
            })}
        </g>
        <g className="battle-scenery" aria-hidden="true" pointerEvents="none">
          <Scenery column={0} x={2.5} y={1.8} width={138} />
          <Scenery column={0} x={8.8} y={2.8} width={165} />
          <Scenery column={0} x={1.4} y={4.8} width={108} />
          <Scenery column={0} x={7.6} y={6.6} width={115} />
          <Scenery column={1} x={4.6} y={5.8} width={150} />
          <Scenery column={2} x={6.4} y={1.1} width={95} />
          <Scenery column={2} x={9.4} y={6.7} width={95} />
        </g>
        <g className="board-grid">
          {coordinates.map(({ x, y, tile }) => {
            const cellKey = `${x},${y}`;
            const occupant = units.find(
              (u) => u.hp > 0 && u.x === x && u.y === y,
            );
            const move = moveCells.has(cellKey),
              skill = skillCells.has(cellKey);
            const actionable =
              phase === "select"
                ? occupant?.side === "ally" && !occupant.acted
                : phase === "move"
                  ? move
                  : phase === "skill"
                    ? occupant?.side === "enemy" && skill
                    : false;
            const planned = destination?.x === x && destination?.y === y;
            const active = occupant?.id === selected || occupant?.id === target;
            return (
              <g key={cellKey}>
                <polygon
                  role="button"
                  aria-disabled={!actionable}
                  tabIndex={actionable ? 0 : -1}
                  data-cell={cellKey}
                  data-terrain={tile}
                  points={diamond(x, y)}
                  aria-label={`${x + 1} 列 ${y + 1} 行，${terrain(tile)}${occupant ? `，${occupant.name}，生命 ${occupant.hp}` : ""}${move ? "，可移動" : ""}${skill ? "，技能範圍" : ""}`}
                  className={`board-cell ${move ? "move-cell" : ""} ${skill ? "skill-cell" : ""} ${planned ? "planned-cell" : ""} ${active ? "selected-cell" : ""} ${occupant?.side === "enemy" && skill ? "target-cell" : ""}`}
                  onClick={() => {
                    if (actionable) onPick({ x, y });
                  }}
                  onKeyDown={(event) => {
                    if (
                      actionable &&
                      (event.key === "Enter" || event.key === " ")
                    ) {
                      event.preventDefault();
                      onPick({ x, y });
                    }
                  }}
                >
                  <title>
                    {terrain(tile)} · {x + 1}, {y + 1}
                    {occupant ? ` · ${occupant.name}` : ""}
                  </title>
                </polygon>
                {move && (
                  <polygon
                    className="move-hatch"
                    points={diamond(x, y)}
                    fill={`url(#${id}-move)`}
                  />
                )}
              </g>
            );
          })}
        </g>
        <g aria-hidden="true" className="board-figures">
          {drawingUnits.map((unit) => (
            <Sprite
              key={unit.id}
              unit={unit}
              x={unit.x}
              y={unit.y}
              selected={unit.id === selected}
            />
          ))}
          {actor && destination && (
            <Sprite unit={actor} {...destination} ghost />
          )}
          {feedback &&
            (() => {
              const hit = units.find((u) => u.id === feedback.id);
              if (!hit) return null;
              const point = project(hit.x + 0.5, hit.y + 0.5);
              return (
                <g
                  key={feedback.sequence}
                  className="hit-feedback"
                  transform={`translate(${point.x} ${point.y - 75})`}
                >
                  <circle r="42" />
                  <text textAnchor="middle" y="-18">
                    −3
                  </text>
                </g>
              );
            })()}
        </g>
      </svg>
      <div className="arena-caption">
        <span>11 × 9 · 河道不可通行</span>
        <span>
          {destination ? "虛影為預覽 · 確認後執行" : "◆ 我方　▲ 敵方"}
        </span>
      </div>
    </section>
  );
}
