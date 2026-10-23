import type { Cell } from "./rules";
import { MAP } from "./rules";

// Presentation-only camera; the painting was generated from this exact layout.
export const project = (x: number, y: number) => ({ x: 550 + (x - y) * 44, y: 70 + (x + y) * 26 });
export const center = (p: Cell) => project(p.x + .5, p.y + .5);
export const diamond = (x: number, y: number) =>
  [project(x,y),project(x+1,y),project(x+1,y+1),project(x,y+1)].map(p => `${p.x},${p.y}`).join(" ");

// 67.6 (1.3 tiles) fails P1v2's same-column/cluster overlap checks. The nearest
// co-column foot spacing is 52; use that geometric maximum without moving feet.
export const FIGURE_HEIGHT = 52;
export function Figure({ id }: { id: string }) {
  const column = ["karen", "lace", "thoma"].indexOf(id);
  const width = column >= 0 ? FIGURE_HEIGHT * .76 : 44;
  return <svg data-p1v-figure={id} x={-width/2} y={-FIGURE_HEIGHT} width={width} height={FIGURE_HEIGHT}
    viewBox={column >= 0 ? `${column * 724 + 110} 0 520 ${id === "thoma" ? 711 : 710}` : "15 8 745 863"}
    preserveAspectRatio="xMidYMax meet">
    <image href={column >= 0 ? "/art/l03-party-v1.png" : "/art/l03-enemies-v1.png"}
      width={column >= 0 ? 2172 : 1774} height={column >= 0 ? 724 : 887} />
  </svg>;
}

export function Portrait({ id }: { id: string }) {
  const column = ["karen", "lace", "thoma"].indexOf(id);
  if (id === "knight-2") return <svg className="p1v-portrait" viewBox="0 0 1254 1254" aria-hidden="true" data-p1v-portrait={id}>
    <image href="/art/l03-p1v4/knight-2-portrait.png" width="1254" height="1254" />
  </svg>;
  return <svg className="p1v-portrait" data-p1v-portrait={id}
    viewBox={column < 0 ? "185 30 390 390" : `${column * 724 + 240} 0 300 300`} aria-hidden="true">
    <image href={`/art/${column < 0 ? "l03-enemies-v1" : "l03-party-v1"}.png`}
      width={column < 0 ? 1774 : 2172} height={column < 0 ? 887 : 724} />
  </svg>;
}

export function BlockedMarker({ unit, cell, label }: { unit: string; cell: Cell; label: string }) {
  const p = center(cell);
  // Uneven, layered strokes read like a weathered painted broken chain.
  // Static state: deliberately independent of every motion preference.
  return <g className="p1v-blocked-marker" data-p1v-blocked-marker={unit} data-cell={cell.x+","+cell.y}
    transform={`translate(${p.x} ${p.y+12})`} role="img" aria-label={`${label}：通道受阻`}>
    <path className="p1v-chain-shadow" d="M-2-3-7-5Q-16-9-20-3T-14 6L-6 8M3 4 8 7Q17 10 20 3T14-5L7-7" />
    <path className="p1v-chain-paint" d="M-3-4-9-6Q-18-8-20-1T-13 6L-7 7M4 4 10 7Q18 8 20 1T13-6L8-7" />
    <path className="p1v-chain-highlight" d="M-18-2Q-15-7-10-5M10 5Q16 7 18 2M-3-9-1-13M3 10 6 13" />
    <text y="28" textAnchor="middle">受阻</text>
  </g>;
}

function Prop({ crop, x, y, width, height, kind }: { crop: string; x: number; y: number; width: number; height: number; kind: string }) {
  return <svg x={x} y={y} width={width} height={height} viewBox={crop} preserveAspectRatio="xMidYMax meet" data-p1v-prop={kind}>
    <image href="/art/l03-p1v4/props.png" width="1536" height="1024" />
  </svg>;
}

export function Terrain({ uid }: { uid: string }) {
  return <g className="p1v-terrain" aria-hidden="true">
    <defs>
      <linearGradient id={`${uid}-edge-x`}><stop offset="0" stopColor="black" /><stop offset=".025" stopColor="white" /><stop offset=".975" stopColor="white" /><stop offset="1" stopColor="black" /></linearGradient>
      <linearGradient id={`${uid}-edge-y`} x2="0" y2="1"><stop offset="0" stopColor="black" /><stop offset=".035" stopColor="white" /><stop offset=".965" stopColor="white" /><stop offset="1" stopColor="black" /></linearGradient>
      <mask id={`${uid}-edge-mask-x`} maskUnits="userSpaceOnUse" x="130" y="32" width="940" height="590"><rect x="130" y="32" width="940" height="590" fill={`url(#${uid}-edge-x)`} /></mask>
      <mask id={`${uid}-edge-mask`} maskUnits="userSpaceOnUse" x="130" y="32" width="940" height="590"><rect x="130" y="32" width="940" height="590" fill={`url(#${uid}-edge-y)`} mask={`url(#${uid}-edge-mask-x)`} /></mask>
    </defs>
    {/* Invert the layout guide's xMidYMid framing. Hit polygons keep the same camera. */}
    <image data-p1v-battlefield href="/art/l03-p1v4/battlefield.png" x="130" y="13.666667" width="940" height="626.666667" mask={`url(#${uid}-edge-mask)`} />
    <g fill="none" stroke="#9abfb9" strokeWidth="1.2">
      <path className="p1v-water-glint" d="M743 217q-17 12-29 17m-25 15-26 15m-22 14-24 14" />
      <path className="p1v-water-glint" d="M583 335q-20 9-29 17m-25 15-26 15m-22 14-24 14" />
    </g>
  </g>;
}

export function Landmarks({ dev, winchSerial, warning = false }: { dev: boolean; winchSerial?: number; warning?: boolean }) {
  const winch=center(MAP.winch), wagon=center(MAP.wagon);
  return <g className="p1v-landmarks" aria-hidden="true">
    {[{x:3,y:4},{x:6,y:4}].map((p,i) => <g key={i} transform={`translate(${center(p).x} ${center(p).y})`}>
      <g transform={i ? "scale(-1 1)" : undefined}><Prop kind="bridge" crop="530 310 490 510" x={-30} y={-31} width={60} height={48} /></g>
    </g>)}
    <text x={center({x:5,y:4}).x} y={center({x:5,y:4}).y+18} textAnchor="middle">斷橋</text>
    <g transform={`translate(${winch.x} ${winch.y})`}>
      <ellipse rx="24" ry="8" cy="4" fill="#0b1411" opacity=".45" />
      <g key={winchSerial || "rest"} className={winchSerial ? "p1v-winch-jerk" : undefined}
        data-p1v-prop="winch" data-p1v-winch-painted data-warning={warning}>
        {/* Non-destructive crops normalize the generated frame padding/footing. */}
        {["48 104 526 540", "605 104 512 540", "1155 104 505 540", "1698 104 474 540"].map((crop,i) =>
          <svg key={i} x="-32" y="-49" width="64" height="58" viewBox={crop} preserveAspectRatio="none"
            className={`p1v-winch-frame frame-${i} ${warning && i === 3 ? "p1v-winch-alert" : ""}`}
            data-p1v-winch-frame={i}>
            <image href="/art/l03-p1v6/winch-frames.png" width="2172" height="724" />
          </svg>)}
      </g>
      <g key={`rope-${winchSerial || 0}`} className={`p1v-winch-rope ${winchSerial ? "taut" : ""}`}>
        <svg x="8" y="-18" width="58" height="34" viewBox={winchSerial ? "40 780 1080 560" : "40 90 1080 530"}
          preserveAspectRatio="none" data-p1v-rope-state={winchSerial ? "taut" : "slack"}>
          <image href="/art/l03-p1v6/rope-states.png" width="1159" height="1358" />
        </svg>
      </g>
      <text y="-56" textAnchor="middle" data-p1v-landmark="winch">絞盤{dev ? " (2,1)" : ""}</text>
      <path className="p1v-objective-pin" d="M-4-70L0-74 4-70 0-66Z" fill="#e5cd91" />
    </g>
    <g transform={`translate(${wagon.x} ${wagon.y})`}>
      <ellipse rx="33" ry="10" cy="6" fill="#0b1411" opacity=".4" />
      <Prop kind="wagon" crop="1020 290 516 510" x={-40} y={-57} width={80} height={68} />
      <text y="-63" textAnchor="middle">車隊</text>
    </g>
  </g>;
}
