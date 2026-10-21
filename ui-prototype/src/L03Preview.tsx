import { useEffect, useId, useRef, useState } from "react";
import {
  Cell,
  Gate,
  SceneUnit,
  cellDistance,
  cellKey,
  gatePlans,
  movementCells,
  movementPath,
  sceneDiamond,
  sceneProject,
  sceneRows,
  sceneUnits,
} from "./l03Scene";
import "./l03.css";

// New hand-painted costume studies; original vector drafts remain as a load-failure fallback.
function Figure({ id }: { id: string }) {
  const [failed, setFailed] = useState(false);
  const column = ["karen", "lace", "thoma"].indexOf(id);
  if ((id === "knight" || id === "crawler") && !failed) {
    const creature = id === "crawler";
    return (
      <g className="l03-figure" data-l03-art="painted">
        <svg
          x={creature ? -45 : -51}
          y={creature ? -60 : -103}
          width={creature ? 90 : 102}
          height={creature ? 65 : 108}
          viewBox={`${creature ? 887 : 0} 0 887 887`}
          preserveAspectRatio="xMidYMax meet"
        >
          <image
            href="/art/l03-enemies-v1.png"
            width="1774"
            height="887"
            onError={() => setFailed(true)}
          />
        </svg>
      </g>
    );
  }
  if (column < 0 || failed) return <VectorFigure id={id} />;
  return (
    <g className="l03-figure" data-l03-art="painted">
      <svg
        x="-37"
        y="-100"
        width="74"
        height="105"
        viewBox={`${column * 724 + 110} 0 520 724`}
        preserveAspectRatio="xMidYMax meet"
      >
        <image
          href="/art/l03-party-v1.png"
          width="2172"
          height="724"
          onError={() => setFailed(true)}
        />
      </svg>
    </g>
  );
}
function VectorFigure({ id, large = false }: { id: string; large?: boolean }) {
  const cleric = id === "thoma",
    rogue = id === "lace",
    enemy = id === "knight",
    creature = id === "crawler";
  if (creature)
    return (
      <g className="l03-figure" data-l03-art="vector">
        <path
          d="M-25-8Q-30-25-13-34L-3-41 12-31 25-16 10-5Z"
          fill="#707b70"
          stroke="#303e39"
          strokeWidth="2"
        />
        <path
          d="m-12-19-19 15m23-23-3 27m21-24 19 11M7-37l5-14"
          stroke="#c1bca0"
          strokeWidth="4"
        />
        <path d="m-14-30 10 3" stroke="#e0bd78" strokeWidth="3" />
      </g>
    );
  const coat = cleric
    ? "#759d91"
    : rogue
      ? "#b29461"
      : enemy
        ? "#8c7885"
        : "#914e43";
  return (
    <g
      className={`l03-figure ${large ? "large" : ""}`}
      data-l03-art="vector"
      stroke="#263a36"
      strokeWidth="1.8"
      strokeLinejoin="round"
    >
      <path d="M-15-65Q-27-49-20-10L0-3 21-13Q24-48 12-65Z" fill={coat} />
      <path d="m-14-23-2 23 9 1 9-26m6 1 2 24 10-1-5-30" fill="#38443f" />
      <path d="m-18 0 12-1 2 5-17 1m31-5 8-1 5 6-14-1" fill="#252e2d" />
      <path
        d="M-13-57-26-43-22-24-16-28-15-43M12-58 23-43 19-28 13-30 12-44"
        fill={cleric ? "#d6d0af" : "#66736a"}
      />
      <path
        d="m-12-60 14 10 12-11-12-8Z"
        fill={cleric ? "#e0d4af" : "#99a59a"}
      />
      <path d="M-9-67Q-13-81-5-86 7-91 12-79L9-66 1-61Z" fill="#d2b59a" />
      <path
        d={
          rogue
            ? "M-11-66Q-20-88-2-93 18-88 14-67L5-82-10-76Z"
            : cleric
              ? "M-11-76Q-12-91 4-89L14-82 9-78-1-84Z"
              : "M-10-78Q-11-91 5-88L13-80 7-77-1-82Z"
        }
        fill={cleric ? "#b4ada1" : "#343c36"}
      />
      <path d="m-8-40 20-3 1 7-22 4Z" fill="#493f31" />
      {cleric ? (
        <>
          <path d="M-2-55 0-12M-9-48 9-49" stroke="#e4d3aa" strokeWidth="3" />
          <rect x="10" y="-29" width="16" height="19" rx="3" fill="#8c664d" />
          <path d="m17-23 0 9m-4-5h8" stroke="#e0d4af" strokeWidth="2" />
        </>
      ) : rogue ? (
        <>
          <ellipse
            cx="-18"
            cy="-26"
            rx="8"
            ry="13"
            fill="none"
            stroke="#e0cc98"
            strokeWidth="3"
          />
          <path d="m18-32 6-19 3 1-4 21" fill="#c3c9bb" />
          <path d="m-11-61 24 25" stroke="#504332" strokeWidth="4" />
        </>
      ) : (
        <>
          <path
            d="m-19-49-18 4 1 26 15 10 11-14-1-23Z"
            fill={enemy ? "#777e84" : "#9fa9a1"}
          />
          <path d="m-22-42 1 23m-8-16 14-2" stroke="#c6b38d" strokeWidth="3" />
          <g className="l03-sword" transform="translate(21 -31)">
            <path d="M-3 0 0-41 4-45 6-39 3 0Z" fill="#e0e2cc" />
            <path d="M-8 0 9-1M1 0 2 10" stroke="#c4a271" strokeWidth="4" />
          </g>
        </>
      )}
      {enemy && (
        <path d="M-12-80 0-90 14-81 12-67-10-67ZM-8-75H10" fill="#9fa6a3" />
      )}
    </g>
  );
}

function Tree({ x, y, scale = 1 }: Cell & { scale?: number }) {
  const p = sceneProject(x, y);
  return (
    <g transform={`translate(${p.x} ${p.y}) scale(${scale})`}>
      <ellipse cy="6" rx="29" ry="12" fill="#233e37" opacity=".25" />
      <svg
        x="-45"
        y="-91"
        width="90"
        height="99"
        viewBox="0 0 724 724"
        preserveAspectRatio="xMidYMax meet"
      >
        <image href="/art/props-v2.png" width="2172" height="724" />
      </svg>
    </g>
  );
}
function SceneMap({
  gate,
  units,
  selected,
  destination,
  target,
  phase,
  moves,
  onPick,
  running,
  progress,
  zoom,
  grid,
}: {
  gate: Gate;
  units: SceneUnit[];
  selected: string | null;
  destination: Cell | null;
  target: string | null;
  phase: string;
  moves: Set<string>;
  onPick: (p: Cell) => void;
  running: string | null;
  progress: number;
  zoom: number;
  grid: boolean;
}) {
  const uid = useId().replace(/:/g, ""),
    actor = units.find((u) => u.id === selected),
    planned = destination || actor;
  const coords = sceneRows.flatMap((row, y) =>
    [...row].map((tile, x) => ({ x, y, tile })),
  );
  const objective = sceneProject(
    gatePlans[gate].markerCell.x + 0.5,
    gatePlans[gate].markerCell.y + 0.5,
  );
  const cellActive = (p: Cell) => {
    if (running) return false;
    const unit = units.find((u) => u.hp > 0 && cellKey(u) === cellKey(p));
    return phase === "select"
      ? unit?.side === "ally" && !unit.acted
      : phase === "move"
        ? moves.has(cellKey(p))
        : phase === "target" &&
          planned &&
          unit &&
          cellDistance(planned, unit) <= 2 &&
          (actor?.id === "thoma"
            ? unit.side === "ally"
            : unit.side === "enemy");
  };
  return (
    <svg
      className="l03-map"
      viewBox={`${550 - 550 / zoom} ${210 - 210 / zoom} ${1100 / zoom} ${420 / zoom}`}
      role="group"
      aria-label="渡口閘門 11 乘 9 互動戰場"
      data-phase={running || phase}
    >
      <defs>
        {["grass", "stone", "water", "forest"].map((name, index) => (
          <pattern
            key={name}
            id={`${uid}terrain-${name}`}
            width="200"
            height="200"
            patternUnits="userSpaceOnUse"
            patternTransform="matrix(1 .34 -1 .34 550 90)"
          >
            <image
              href="/art/terrain-v2.png"
              width="400"
              height="400"
              x={index % 2 ? -200 : 0}
              y={index > 1 ? -200 : 0}
            />
          </pattern>
        ))}
        <pattern
          id={`${uid}water`}
          width="54"
          height="34"
          patternUnits="userSpaceOnUse"
        >
          <path
            d="M0 13q14-5 29 0t27 0M19 29l19-3"
            fill="none"
            stroke="#bdd0c1"
            strokeWidth="1"
            opacity=".32"
          />
        </pattern>
        <pattern
          id={`${uid}hatch`}
          width="12"
          height="12"
          patternUnits="userSpaceOnUse"
          patternTransform="rotate(30)"
        >
          <path d="M0 0V12" stroke="#d4ead2" strokeWidth="2" opacity=".5" />
        </pattern>
        <radialGradient id={`${uid}light`}>
          <stop stopColor="#e8d8ac" stopOpacity=".8" />
          <stop offset="1" stopColor="#e8d8ac" stopOpacity="0" />
        </radialGradient>
        <filter id={`${uid}shade`} x="-40%" y="-40%" width="180%" height="200%">
          <feDropShadow
            dx="0"
            dy="15"
            stdDeviation="14"
            floodColor="#182b29"
            floodOpacity=".4"
          />
        </filter>
      </defs>
      <g aria-hidden="true" pointerEvents="none">
        <ellipse
          cx="550"
          cy="375"
          rx="500"
          ry="230"
          fill={`url(#${uid}light)`}
          opacity=".25"
        />
        {[0, 1, 2, 3].map((i) => (
          <path
            key={i}
            d={`M${50 + i * 12} ${325 + i * 19}Q420 ${30 + i * 12} 1030 ${315 + i * 22}T590 ${630 + i * 19}`}
            fill="none"
            stroke="#afbc9d"
            opacity=".13"
          />
        ))}
        <path
          d="M154 225 638 390 1034 255 1034 280 638 419 154 251Z"
          fill="#424f43"
          filter={`url(#${uid}shade)`}
        />
        {coords.map(({ x, y, tile }) => (
          <g key={`${x},${y}`}>
            <polygon
              data-ground={`${x},${y}`}
              points={sceneDiamond(x, y)}
              fill={
                tile === "~"
                  ? "#648f88"
                  : tile === "R"
                    ? "#a58a60"
                    : (x * 7 + y * 3) % 4 === 0
                      ? "#a3a383"
                      : "#959c7a"
              }
            />
            <polygon
              points={sceneDiamond(x, y)}
              fill={`url(#${uid}terrain-${tile === "~" ? "water" : tile === "F" ? "forest" : tile === "R" ? "stone" : "grass"})`}
              opacity={tile === "~" ? 0.26 : 0.36}
            />
            {tile === "~" && (
              <polygon points={sceneDiamond(x, y)} fill={`url(#${uid}water)`} />
            )}
          </g>
        ))}
        {coords
          .filter((c) => c.tile !== "~")
          .flatMap(({ x, y }) =>
            [
              {
                a: sceneProject(x, y),
                b: sceneProject(x + 1, y),
                water: sceneRows[y - 1]?.[x] === "~",
              },
              {
                a: sceneProject(x + 1, y),
                b: sceneProject(x + 1, y + 1),
                water: sceneRows[y]?.[x + 1] === "~",
              },
              {
                a: sceneProject(x, y + 1),
                b: sceneProject(x + 1, y + 1),
                water: sceneRows[y + 1]?.[x] === "~",
              },
              {
                a: sceneProject(x, y),
                b: sceneProject(x, y + 1),
                water: sceneRows[y]?.[x - 1] === "~",
              },
            ]
              .filter((e) => e.water)
              .map((e, i) => (
                <path
                  key={`${x},${y}-${i}`}
                  d={`M${e.a.x} ${e.a.y}L${e.b.x} ${e.b.y}`}
                  stroke="#d0c5a1"
                  strokeWidth="7"
                />
              )),
          )}
        {[3, 4, 5, 6, 7, 8].map((x) => {
          const p = sceneProject(x, 4);
          return (
            <g
              key={x}
              opacity={gate === "open" && (x === 4 || x === 5) ? 0.32 : 1}
            >
              <polygon
                points={sceneDiamond(x, 4)}
                fill="#947454"
                stroke="#d0b188"
                strokeWidth="2"
              />
              {[0.2, 0.4, 0.6, 0.8].map((v) => {
                const a = sceneProject(x + v, 4),
                  b = sceneProject(x + v, 5);
                return (
                  <path
                    key={v}
                    d={`M${a.x} ${a.y}L${b.x} ${b.y}`}
                    stroke="#5f4f3c"
                    strokeWidth="2"
                  />
                );
              })}
              <path
                d={`M${p.x} ${p.y - 16}l44 23m0-16v17`}
                stroke="#776248"
                strokeWidth="4"
              />
            </g>
          );
        })}
        {gate === "open" && (
          <g>
            <polygon points={sceneDiamond(4, 4)} fill="#648f88" />
            <polygon points={sceneDiamond(5, 4)} fill="#648f88" />
            <path
              d="m525 216 25 12m-5-22 30 12m-18 8 14 7"
              stroke="#e0cc9e"
              strokeWidth="4"
            />
            <text x="555" y="259" className="l03-world-warning">
              斷橋 · 無法通行
            </text>
          </g>
        )}
        {[
          [0.5, 1.2, 1],
          [1.2, 0.5, 0.8],
          [1, 2, 0.8],
          [0.5, 0.2, 0.9],
          [9.4, 7.8, 1],
          [8.7, 8.3, 0.85],
          [10.3, 6.8, 0.9],
          [10, 8.5, 1.1],
        ].map(([x, y, s], i) => (
          <Tree key={i} x={x} y={y} scale={s} />
        ))}
        <g
          transform={`translate(${sceneProject(8.7, 1.5).x} ${sceneProject(8.7, 1.5).y})`}
        >
          <path d="m-36 7 37 19 34-18-35-18Z" fill="#d6c4a0" />
          <path
            d="m-27 5 0-34 12-7 5 41m26 7 0-34 13-7 4 36"
            fill="#777f70"
            stroke="#d9cfac"
            strokeWidth="2"
          />
          <ellipse
            cy="-23"
            rx="31"
            ry="10"
            fill="#6f5940"
            stroke="#c1ac77"
            strokeWidth="3"
          />
          <path
            d="m-26-23 54 0M0-33v20m-6-8-63 27"
            stroke="#dfcda3"
            strokeWidth="3"
          />
          <text x="0" y="-63" className="l03-landmark">
            01 絞盤高台
          </text>
        </g>
        <g
          transform={`translate(${sceneProject(8.5, 4.3).x} ${sceneProject(8.5, 4.3).y})`}
        >
          <path
            d="m-33-4 27-13 47 23-27 13Z"
            fill="#8b6b46"
            stroke="#d4bc89"
            strokeWidth="2"
          />
          {[-14, 5, 24].map((x) => (
            <g key={x} transform={`translate(${x} ${x * 0.5 - 7})`}>
              <path
                d="m-9-15 10-5 12 6v17L3 8-9 1Z"
                fill="#b2a37e"
                stroke="#504e3c"
              />
              <path d="M2-18V7" stroke="#526157" strokeWidth="3" />
            </g>
          ))}
          <circle cx="-17" cy="11" r="8" fill="#3f4940" />
          <circle cx="21" cy="28" r="8" fill="#3f4940" />
          <text x="15" y="-50" className="l03-landmark">
            02 學院車隊
          </text>
        </g>
        <g
          transform={`translate(${sceneProject(3.4, 7.6).x} ${sceneProject(3.4, 7.6).y})`}
        >
          <path
            d="m-52 0 78 39 31-16-78-39Z"
            fill="#a28b61"
            stroke="#d3c29a"
            strokeWidth="2"
          />
          {[-32, -12, 8, 28].map((x) => (
            <path
              key={x}
              d={`m${x} ${x * 0.5 + 9} 0 18`}
              stroke="#5d6552"
              strokeWidth="5"
            />
          ))}
          <text x="-7" y="58" className="l03-landmark">
            03 接應碼頭
          </text>
        </g>
        {[0, 1, 2].map((i) => {
          const p = sceneProject(4.8, 1 + i * 2.3);
          return (
            <g
              key={i}
              transform={`translate(${p.x} ${p.y})`}
              opacity={gate === "sealed" && i === 2 ? 0.28 : 1}
            >
              <path
                d="M-35-5Q-12 23 34 14L46 5 0-18Z"
                fill="#6d6249"
                stroke="#d1bd88"
                strokeWidth="2"
              />
              <path
                d="m-20-4 47 23m-31-29L-9 12m21-15L5 17"
                stroke="#b99d69"
                strokeWidth="2"
              />
              {i === 0 && (
                <>
                  <path d="M3-6v-18" stroke="#332f28" />
                  <rect
                    x="-1"
                    y="-34"
                    width="9"
                    height="13"
                    rx="2"
                    fill="#f2cc79"
                    stroke="#755b37"
                  />
                  <circle cx="4" cy="-28" r="19" fill={`url(#${uid}light)`} />
                </>
              )}
            </g>
          );
        })}
        <g
          transform={`translate(${objective.x} ${objective.y})`}
          className="l03-objective-pin"
        >
          <path
            d="m0-59 13 13-13 13-13-13Z"
            fill="#f0d299"
            stroke="#3e5045"
            strokeWidth="2"
          />
          <path d="M0-31V-5" stroke="#e9d6a7" strokeWidth="2" />
          <ellipse
            rx="30"
            ry="14"
            fill="none"
            stroke="#f0d299"
            strokeDasharray="5 5"
            strokeWidth="2"
          />
        </g>
        <path
          d="m510 155 12 9-2-7m-6 0 4 15m-42 52 12 9-2-7m-6 0 4 15"
          stroke="#d0e0ce"
          strokeWidth="2"
          fill="none"
          opacity=".6"
        />
      </g>
      <g className={`l03-cells ${grid ? "show-grid" : ""}`}>
        {coords.map((p) => {
          const k = cellKey(p),
            unit = units.find((u) => u.hp > 0 && cellKey(u) === k),
            can = !!cellActive(p),
            move = phase === "move" && moves.has(k),
            range =
              phase === "target" && planned && cellDistance(planned, p) <= 2,
            active = unit?.id === selected || unit?.id === target;
          return (
            <polygon
              key={k}
              data-l03-cell={k}
              points={sceneDiamond(p.x, p.y)}
              role="button"
              tabIndex={can ? 0 : -1}
              aria-disabled={!can}
              aria-label={`${p.x + 1}列${p.y + 1}行${unit ? ` ${unit.name} 生命${unit.hp}` : ""}${move ? " 可移動" : ""}`}
              className={`${move ? "move" : ""} ${range ? "range" : ""} ${active ? "active" : ""} ${destination && cellKey(destination) === k ? "destination" : ""}`}
              onClick={() => can && onPick(p)}
              onKeyDown={(e) => {
                if (can && (e.key === "Enter" || e.key === " ")) {
                  e.preventDefault();
                  onPick(p);
                }
              }}
            />
          );
        })}
      </g>
      <g pointerEvents="none" aria-hidden="true">
        {units
          .filter((u) => u.hp > 0)
          .sort((a, b) => a.x + a.y - b.x - b.y)
          .map((unit) => {
            const moving =
              running === "move" && selected === unit.id && destination;
            const route = moving
                ? movementPath(unit, destination, units, gate)
                : [unit],
              segment = Math.min(
                Math.max(0, route.length - 2),
                Math.floor(progress * (route.length - 1)),
              ),
              blend = progress * (route.length - 1) - segment,
              a = route[segment],
              b = route[segment + 1] || a;
            const p = sceneProject(
              a.x + (b.x - a.x) * blend + 0.5,
              a.y + (b.y - a.y) * blend + 0.5,
            );
            const staged =
              running &&
              running !== "move" &&
              selected === unit.id &&
              destination
                ? sceneProject(destination.x + 0.5, destination.y + 0.5)
                : p;
            return (
              <g
                key={unit.id}
                data-l03-unit={unit.id}
                data-hp={unit.hp}
                data-acted={unit.acted}
                className={`l03-piece ${unit.id === selected ? "selected" : ""} ${unit.acted ? "spent" : ""} ${target === unit.id && running === "impact" ? "hit" : ""} ${selected === unit.id ? running || "" : ""}`}
                transform={`translate(${staged.x} ${staged.y})`}
              >
                <ellipse rx="24" ry="10" fill="#233c34" opacity=".4" />
                <ellipse
                  rx="24"
                  ry="11"
                  fill="none"
                  stroke={unit.side === "ally" ? "#d7e0bb" : "#b97365"}
                  strokeWidth="2"
                />
                <Figure id={unit.id} />
                <g className="l03-unit-label">
                  <rect
                    x="-50"
                    y="13"
                    width="100"
                    height="20"
                    rx="2"
                    fill="#243b35"
                  />
                  <text y="27" textAnchor="middle" fill="#f0ead4">
                    {unit.side === "ally" ? "◆" : "▲"} {unit.name}
                  </text>
                  <rect x="-24" y="36" width="48" height="4" fill="#37463e" />
                  <rect
                    x="-24"
                    y="36"
                    width={(48 * unit.hp) / unit.max}
                    height="4"
                    fill={unit.side === "ally" ? "#bdd1a3" : "#ce8a75"}
                  />
                </g>
                {unit.id === target && running === "impact" && (
                  <text className="l03-damage" y="-105" textAnchor="middle">
                    {actor?.id === "thoma" ? "支援標記" : "−3"}
                  </text>
                )}
              </g>
            );
          })}
        {actor && destination && !running && (
          <g
            opacity=".35"
            transform={`translate(${sceneProject(destination.x + 0.5, destination.y + 0.5).x} ${sceneProject(destination.x + 0.5, destination.y + 0.5).y})`}
          >
            <Figure id={actor.id} />
          </g>
        )}
        {running === "impact" &&
          actor &&
          target &&
          (() => {
            const a = sceneProject(
                (destination || actor).x + 0.5,
                (destination || actor).y + 0.5,
              ),
              b = units.find((u) => u.id === target)!;
            const p = sceneProject(b.x + 0.5, b.y + 0.5);
            return actor.id === "thoma" ? (
              <g stroke="#dddfae" fill="none" strokeWidth="3">
                <ellipse cx={p.x} cy={p.y - 30} rx="30" ry="40" />
                <path d={`M${p.x - 13} ${p.y - 30}h26m-13-13v26`} />
              </g>
            ) : actor.id === "lace" ? (
              <path
                d={`M${a.x} ${a.y - 40}Q${(a.x + p.x) / 2} ${a.y - 110} ${p.x} ${p.y - 30}`}
                stroke="#ecd8a4"
                strokeWidth="3"
                fill="none"
              />
            ) : (
              <path
                d={`M${p.x - 30} ${p.y - 100}Q${p.x + 35} ${p.y - 75} ${p.x + 20} ${p.y - 30}`}
                stroke="#f4e3be"
                strokeWidth="7"
                fill="none"
              />
            );
          })()}
      </g>
    </svg>
  );
}

export function L03Preview({ onExit }: { onExit: () => void }) {
  const [gate, setGate] = useState<Gate>("open"),
    [units, setUnits] = useState(() => sceneUnits.map((u) => ({ ...u }))),
    [selected, setSelected] = useState<string | null>(null),
    [destination, setDestination] = useState<Cell | null>(null),
    [target, setTarget] = useState<string | null>(null),
    [phase, setPhase] = useState("select"),
    [running, setRunning] = useState<string | null>(null),
    [progress, setProgress] = useState(0),
    [actions, setActions] = useState(0),
    [large, setLarge] = useState(false),
    [grid, setGrid] = useState(true),
    [zoom, setZoom] = useState(1),
    [log, setLog] = useState("水位正在升高。先選一名隊員，規劃接應路線。"),
    [brief, setBrief] = useState(false),
    [history, setHistory] = useState<string[]>([]);
  const active = useRef<{ frame: number; impacted: boolean } | null>(null),
    reduced = useRef(matchMedia("(prefers-reduced-motion: reduce)").matches),
    heading = useRef<HTMLHeadingElement>(null),
    dialog = useRef<HTMLDialogElement>(null),
    briefButton = useRef<HTMLButtonElement>(null);
  const actor = units.find((u) => u.id === selected),
    recipient = units.find((u) => u.id === target),
    plan = gatePlans[gate];
  const moves = actor ? movementCells(actor, units, gate) : new Set<string>();
  function clear() {
    setSelected(null);
    setDestination(null);
    setTarget(null);
    setPhase("select");
  }
  function cancel() {
    if (active.current) cancelAnimationFrame(active.current.frame);
    active.current = null;
    setRunning(null);
    clear();
  }
  useEffect(() => {
    heading.current?.focus({ preventScroll: true });
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => {
      reduced.current = media.matches;
    };
    media.addEventListener("change", change);
    return () => {
      media.removeEventListener("change", change);
      if (active.current) cancelAnimationFrame(active.current.frame);
      active.current = null;
    };
  }, []);
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !dialog.current?.open) {
        cancel();
        setLog("未完成的預演已取消；已命中的效果保留。");
      }
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  });
  useEffect(() => {
    if (brief) {
      dialog.current?.showModal();
    } else if (dialog.current?.open) {
      dialog.current.close();
      briefButton.current?.focus();
    }
  }, [brief]);
  function reset(next = gate) {
    cancel();
    setGate(next);
    setUnits(sceneUnits.map((u) => ({ ...u })));
    setActions(0);
    setHistory([]);
    setLog(`${gatePlans[next].title}構圖已載入。選一名隊員開始預演。`);
  }
  function select(id: string) {
    if (running) return;
    const unit = units.find((u) => u.id === id);
    if (!unit || unit.acted) return;
    setSelected(id);
    setDestination(null);
    setTarget(null);
    setPhase("move");
    setLog(`${unit.name}：選取斜紋格，或選腳下格原地演出。`);
  }
  function pick(p: Cell) {
    if (running) return;
    const unit = units.find((u) => u.hp > 0 && cellKey(u) === cellKey(p));
    if (phase === "select" && unit?.side === "ally") select(unit.id);
    else if (phase === "move" && moves.has(cellKey(p))) {
      setDestination(p);
      setPhase("target");
      setLog(
        actor?.id === "thoma"
          ? "選擇兩格內的我方，預覽支援標記；不改生命。"
          : "選擇兩格內的敵方，預覽固定 −3 演出。",
      );
    } else if (
      phase === "target" &&
      actor &&
      destination &&
      unit &&
      cellDistance(destination, unit) <= 2 &&
      (actor.id === "thoma" ? unit.side === "ally" : unit.side === "enemy")
    ) {
      setTarget(unit.id);
      setPhase("confirm");
    }
  }
  function confirm() {
    if (
      active.current ||
      phase !== "confirm" ||
      !actor ||
      actor.acted ||
      !destination ||
      !recipient
    )
      return;
    const from = { x: actor.x, y: actor.y },
      to = { ...destination },
      id = actor.id,
      hit = recipient.id,
      start = performance.now(),
      token = { frame: 0, impacted: false };
    active.current = token;
    const message =
      id === "thoma"
        ? `${actor.name}在${recipient.name}身旁留下支援標記；生命不變。`
        : `${actor.name}完成${id === "lace" ? "繩索" : "盾劍"}演出，${recipient.name}固定 −3。`;
    const tick = (now: number) => {
      if (active.current !== token) return;
      const elapsed = now - start,
        travel = reduced.current ? 0 : 480,
        impactAt = reduced.current ? 0 : 1050,
        total = reduced.current ? 160 : 1600;
      if (!token.impacted && elapsed >= impactAt) {
        token.impacted = true;
        setUnits((current) =>
          current.map((u) =>
            u.id === id
              ? { ...u, ...to, acted: true }
              : u.id === hit && id !== "thoma"
                ? { ...u, hp: Math.max(0, u.hp - 3) }
                : u,
          ),
        );
        setActions((n) => n + 1);
        setLog(message);
        setHistory((lines) => [message, ...lines]);
      }
      if (elapsed >= total) {
        active.current = null;
        setRunning(null);
        clear();
        return;
      }
      setRunning(
        elapsed < travel
          ? "move"
          : elapsed < impactAt - 170
            ? "windup"
            : elapsed < impactAt
              ? "release"
              : elapsed < impactAt + 180
                ? "impact"
                : "recovery",
      );
      setProgress(travel ? Math.min(1, elapsed / travel) : 1);
      token.frame = requestAnimationFrame(tick);
    };
    setRunning(from.x === to.x && from.y === to.y ? "windup" : "move");
    token.frame = requestAnimationFrame(tick);
  }
  return (
    <div className={`l03-app ${large ? "l03-large" : ""}`}>
      <a className="l03-skip" href="#l03-controls">
        跳至行動指令
      </a>
      <header className="l03-header">
        <button
          className="l03-wordmark"
          onClick={() => {
            cancel();
            onExit();
          }}
          aria-label="返回原型主選單"
        >
          <span className="l03-sigil">╱╲</span>
          <span>
            CAMPAIGN FORGE<small>碑 誓　／　候選戰鬥展示</small>
          </span>
        </button>
        <nav aria-label="展示操作">
          <button aria-pressed={large} onClick={() => setLarge((v) => !v)}>
            Aa <span>放大文字</span>
          </button>
          <button ref={briefButton} onClick={() => setBrief(true)}>
            戰前情報 <span>↗</span>
          </button>
          <button onClick={() => reset()}>重設預演</button>
        </nav>
      </header>
      <main className="l03-main">
        <div className="l03-title">
          <div>
            <p className="l03-overline">第一章　／　L03　／　戰地測繪</p>
            <h1 ref={heading} tabIndex={-1}>
              渡口閘門<span>THE FLOODGATE</span>
            </h1>
          </div>
          <div className="l03-route" role="group" aria-label="比較渡口選擇">
            <button
              aria-pressed={gate === "open"}
              onClick={() => reset("open")}
            >
              01 <strong>開閘接船</strong>
            </button>
            <button
              aria-pressed={gate === "sealed"}
              onClick={() => reset("sealed")}
            >
              02 <strong>封閘護橋</strong>
            </button>
          </div>
        </div>
        <div className="l03-layout">
          <section className="l03-world" aria-label="渡口戰場">
            <div className="l03-world-top">
              <span>
                <i /> 我方行動 <small>已確認 {actions} 次</small>
              </span>
              <div>
                <button aria-pressed={grid} onClick={() => setGrid((v) => !v)}>
                  格線
                </button>
                <button
                  aria-label="縮小地圖"
                  onClick={() => setZoom((z) => Math.max(0.85, z - 0.15))}
                >
                  −
                </button>
                <output aria-label="地圖倍率">{Math.round(zoom * 100)}%</output>
                <button
                  aria-label="放大地圖"
                  onClick={() => setZoom((z) => Math.min(1.45, z + 0.15))}
                >
                  ＋
                </button>
                <button onClick={() => setZoom(1)}>全景</button>
              </div>
            </div>
            <div className="l03-world-note">
              <span>北岸水位標記</span>
              <strong>裂潮將至</strong>
              <small>↑ 上游來水</small>
            </div>
            <div className="l03-north" aria-hidden="true">
              N<span>↗</span>
            </div>
            <SceneMap
              {...{
                gate,
                units,
                selected,
                destination,
                target,
                phase,
                moves,
                running,
                progress,
                zoom,
                grid,
              }}
              onPick={pick}
            />
            <div className="l03-map-foot">
              <span>11 × 9　／　{plan.short}</span>
              <span>◆ 我方　▲ 敵方　▧ 可移動</span>
            </div>
          </section>
          <aside className="l03-ledger" aria-label="任務與行動指令">
            <section className="l03-mission">
              <div className="l03-overline">MISSION / 當前目標</div>
              <h2>{plan.objective}</h2>
              <div className="l03-subobjective">
                <span>◇</span>
                <p>{plan.secondary}</p>
              </div>
              <div className="l03-cost">
                <span>這個選擇將留下</span>
                <p>{plan.cost}</p>
              </div>
            </section>
            <section id="l03-controls" tabIndex={-1} className="l03-command">
              <div className="l03-order-body">
                <div className="l03-overline">ORDERS / 行動預覽</div>
                <ol className="l03-steps" aria-label="操作步驟">
                  {["選人", "移動", "目標", "確認"].map((s, i) => (
                    <li
                      key={s}
                      aria-current={
                        ["select", "move", "target", "confirm"].indexOf(
                          phase,
                        ) === i
                          ? "step"
                          : undefined
                      }
                    >
                      <span>{i + 1}</span>
                      {s}
                    </li>
                  ))}
                </ol>
                {actor ? (
                  <>
                    <div className="l03-selected">
                      <svg viewBox="-38 -100 76 110" aria-hidden="true">
                        <Figure id={actor.id} />
                      </svg>
                      <div>
                        <h3>{actor.name}</h3>
                        <p>
                          {actor.role}
                          <span>
                            生命 {actor.hp} / {actor.max}
                          </span>
                        </p>
                      </div>
                    </div>
                    <div className="l03-skill">
                      <strong>
                        {actor.id === "thoma"
                          ? "支援標記"
                          : actor.id === "lace"
                            ? "繩索牽制"
                            : "盾劍掩護"}
                      </strong>
                      <p>
                        {actor.id === "thoma"
                          ? "為兩格內同伴標記接應位置。無治療或資源判定。"
                          : "兩格內敵方的固定 −3 演出；不表示正式傷害或命中判定。"}
                      </p>
                    </div>
                  </>
                ) : (
                  <div className="l03-empty">
                    <span>◆</span>
                    <p>
                      選取一名隊員
                      <br />
                      <small>從地圖或下方隊伍開始</small>
                    </p>
                  </div>
                )}
              </div>
              <div className="l03-order-actions">
                {recipient && (
                  <div className="l03-target" role="status">
                    <span>{running ? "演出目標" : "確認前預覽"}</span>
                    <strong>
                      {recipient.name}　
                      {actor?.id === "thoma"
                        ? "標記，生命不變"
                        : running
                          ? `生命 ${recipient.hp}`
                          : `${recipient.hp} → ${Math.max(0, recipient.hp - 3)}`}
                    </strong>
                  </div>
                )}
                <button
                  className="l03-commit"
                  disabled={phase !== "confirm" || !!running}
                  onClick={confirm}
                >
                  {running
                    ? "正在演出…"
                    : phase === "confirm"
                      ? "確認這次演出　→"
                      : "選擇隊員、位置與目標"}
                </button>
                <button
                  className="l03-undo"
                  disabled={phase === "select" && !running}
                  onClick={() => {
                    cancel();
                    setLog("預演已取消；未命中的效果不套用。");
                  }}
                >
                  取消預覽 <kbd>Esc</kbd>
                </button>
              </div>
            </section>
          </aside>
        </div>
        <section className="l03-bottom" aria-label="可出戰隊伍">
          <div className="l03-party-label">
            <span>FIELD PARTY</span>
            <strong>渡口小隊</strong>
            <small>造型與職能候選</small>
          </div>
          <div className="l03-roster">
            {units
              .filter((u) => u.side === "ally")
              .map((u, i) => (
                <button
                  key={u.id}
                  className={`l03-roster-unit ${selected === u.id ? "chosen" : ""}`}
                  aria-pressed={selected === u.id}
                  disabled={u.acted || !!running}
                  onClick={() => select(u.id)}
                >
                  <span className="l03-number">0{i + 1}</span>
                  <svg viewBox="-38 -100 76 110" aria-hidden="true">
                    <Figure id={u.id} />
                  </svg>
                  <span>
                    <strong>{u.name}</strong>
                    <small>{u.role}</small>
                    <span className="l03-health">
                      <i style={{ width: `${(100 * u.hp) / u.max}%` }} />
                    </span>
                  </span>
                  <span className="l03-hp">
                    {u.acted ? "已行動" : `${u.hp}/${u.max}`}
                  </span>
                </button>
              ))}
          </div>
          <button
            className="l03-round"
            disabled={!!running}
            onClick={() => {
              clear();
              setUnits((current) =>
                current.map((u) => ({ ...u, acted: false })),
              );
              setLog("隊員恢復可演出；本展示不執行敵方回合。");
            }}
          >
            下一輪預演 <span>→</span>
          </button>
        </section>
        <div className="l03-status" role="status" aria-live="polite">
          <span>行動紀錄</span>
          {log}
        </div>
        <footer className="l03-footer">
          <span>候選構圖與操作排練 · 無正式勝敗、AI 或存檔</span>
          <details>
            <summary>預演紀錄與範圍</summary>
            <p>
              本頁不寫入 Ink；切換開閘／封閘會重設預演。三格移動、兩格範圍與 −3
              沿用固定介面示例。造型為新繪向量草案，G004／G005
              與人工美術審查仍待核准。
            </p>
            <ol>
              {history.map((line, i) => (
                <li key={i}>{line}</li>
              ))}
            </ol>
          </details>
        </footer>
      </main>
      <dialog
        className="l03-brief"
        ref={dialog}
        onCancel={(event) => {
          event.preventDefault();
          setBrief(false);
        }}
        onClose={() => {
          setBrief(false);
          briefButton.current?.focus();
        }}
        aria-labelledby="l03-brief-heading"
      >
        <div className="l03-overline">渡口現場 / 已知情報</div>
        <h2 id="l03-brief-heading">水只有一條去路</h2>
        <p>
          開閘讓三艘船靠岸，水流也會沖毀載著三箱筆記的橋；封閘能讓學院車隊過橋，提歐所在的最後一船將無法返回。
        </p>
        <blockquote>{plan.quote}</blockquote>
        <p>
          沿岸救援可以多救一些人，不能讓已失去的船或完整名鑰無代價回來。這裡比較兩種場景構圖，並非重新選定正式劇情。
        </p>
        <button className="l03-commit" onClick={() => setBrief(false)}>
          返回渡口
        </button>
      </dialog>
    </div>
  );
}
