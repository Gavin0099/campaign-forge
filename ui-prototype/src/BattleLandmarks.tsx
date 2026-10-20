import { useId } from "react";
import { project } from "./Battlefield";

function LandmarkArt({
  column,
  row,
  x,
  y,
  size,
}: {
  column: number;
  row: number;
  x: number;
  y: number;
  size: number;
}) {
  const id = useId().replace(/:/g, "");
  const point = project(x, y);
  return (
    <g transform={`translate(${point.x} ${point.y})`}>
      <ellipse
        cy="2"
        rx={size * 0.23}
        ry={size * 0.08}
        fill="#101719"
        opacity=".5"
      />
      <svg
        x={-size / 2}
        y={-size}
        width={size}
        height={size}
        viewBox={`${column * 640} ${row * 640} 640 640`}
      >
        <defs>
          <clipPath id={id}>
            <rect x={column * 640} y={row * 640} width="640" height="640" />
          </clipPath>
        </defs>
        <image
          href="/art/landmarks-v3.png"
          width="1280"
          height="1280"
          clipPath={`url(#${id})`}
        />
      </svg>
    </g>
  );
}

export function BattleLandmarks({
  direction,
}: {
  direction: "cartography" | "ember";
}) {
  const ink = direction === "cartography";
  return (
    <g
      pointerEvents="none"
      aria-hidden="true"
      className={`landmarks landmarks-${direction}`}
    >
      {ink ? (
        <>
          <g
            className="survey-traces"
            fill="none"
            stroke="#d3bb7d"
            strokeWidth="1.3"
            opacity=".55"
          >
            <path d="M120 340Q230 190 410 230T820 210M140 348Q240 210 405 250T810 227M160 356Q255 234 400 270T800 246M720 555Q700 440 870 410T1090 380M740 565Q720 462 885 429T1100 397" />
            <path
              d="M235 460L510 142M236 460L1020 350M400 510L720 180"
              strokeDasharray="5 7"
            />
            <path d="M215 460h40m-20 -20v40M490 142h40m-20 -20v40M1000 350h40m-20 -20v40" />
            <circle cx="235" cy="460" r="33" />
            <circle cx="510" cy="142" r="20" />
          </g>
          <g fill="none" stroke="#7ce8e3" strokeWidth="2" opacity=".65">
            <path d="M735 228l-30 15 -20 10 -28 13 -22 12 9 22 -9 28 -28 14 -22 10M485 403l9 21 -9 29 -15 15 -10 22" />
          </g>
          <LandmarkArt column={0} row={0} x={10.2} y={2.2} size={170} />
          <LandmarkArt column={1} row={0} x={9.5} y={8.6} size={115} />
        </>
      ) : (
        <>
          <g
            className="ember-tectonics"
            fill="none"
            stroke="#cf9455"
            opacity=".6"
          >
            <path
              d="M270 400l52 9 37 -23 36 13 51 -45M710 530l28 -61 47 -17 12 -32 65 -20M670 176l-6 48 34 16 6 38 44 18"
              strokeWidth="2"
            />
            <path
              d="M283 405l40 8 38 -22 35 15 60 -41M714 539l33 -63 44 -17 15 -29 64 -17"
              strokeWidth=".8"
            />
          </g>
          <LandmarkArt column={0} row={1} x={10.2} y={2.2} size={170} />
          <LandmarkArt column={1} row={1} x={9.5} y={8.6} size={115} />
        </>
      )}
    </g>
  );
}
