import type { Cell } from "./rules";
import { MAP, key, walkable } from "./rules";

// This camera belongs only to the playable view. Map cells and rules are unchanged.
// A steeper diamond gives the 50-unit figures room without overlapping the
// nearest same-column pair (52 units between their feet).
export const project = (x: number, y: number) => ({ x: 550 + (x - y) * 44, y: 70 + (x + y) * 26 });
export const center = (p: Cell) => project(p.x + .5, p.y + .5);
export const diamond = (x: number, y: number) =>
  [project(x,y),project(x+1,y),project(x+1,y+1),project(x,y+1)].map(p => `${p.x},${p.y}`).join(" ");

export function Figure({ id }: { id: string }) {
  const column = ["karen", "lace", "thoma"].indexOf(id);
  return column >= 0 ? <svg data-p1v-figure={id} x="-19" y="-50" width="38" height="50"
    viewBox={`${column * 724 + 110} 0 520 ${id === "thoma" ? 711 : 710}`} preserveAspectRatio="xMidYMax meet">
    <image href="/art/l03-party-v1.png" width="2172" height="724" />
  </svg> : <svg data-p1v-figure={id} x="-21" y="-50" width="42" height="50" viewBox="0 0 887 871" preserveAspectRatio="xMidYMax meet">
    <image href="/art/l03-enemies-v1.png" width="1774" height="887" />
  </svg>;
}

export function Portrait({ id }: { id: string }) {
  const column = ["karen", "lace", "thoma"].indexOf(id);
  return <svg className="p1v-portrait" viewBox={column < 0 ? "185 30 390 390" : `${column * 724 + 240} 0 300 300`} aria-hidden="true">
    <image href={`/art/${column < 0 ? "l03-enemies-v1" : "l03-party-v1"}.png`}
      width={column < 0 ? 1774 : 2172} height={column < 0 ? 887 : 724} />
  </svg>;
}

function Prop({ crop, x, y, width, height }: { crop: string; x: number; y: number; width: number; height: number }) {
  return <svg x={x} y={y} width={width} height={height} viewBox={crop} preserveAspectRatio="xMidYMax meet">
    <image href="/art/props-v2.png" width="2048" height="683" />
  </svg>;
}

export function Terrain({ uid }: { uid: string }) {
  const cells = MAP.rows.flatMap((row,y) => [...row].map((tile,x) => ({x,y,tile})))
    .sort((a,b) => a.x+a.y-b.x-b.y || a.x-b.x);
  return <g className="p1v-terrain" aria-hidden="true">
    {cells.map(p => {
      const water = !walkable(p,"open"), a=project(p.x,p.y+1), b=project(p.x+1,p.y+1), c=project(p.x+1,p.y);
      const surface = water ? "water" : p.tile === "F" ? "forest" : p.tile === "R" ? "stone" : "grass";
      return <g key={key(p)}>
        {!water && <g className="p1v-tile-sides">
          <polygon points={`${a.x},${a.y} ${b.x},${b.y} ${b.x},${b.y+18} ${a.x},${a.y+18}`} fill="#383a2b" />
          <polygon points={`${b.x},${b.y} ${c.x},${c.y} ${c.x},${c.y+18} ${b.x},${b.y+18}`} fill="#242b25" />
          <path d={`M${a.x} ${a.y+5}L${b.x} ${b.y+5}L${c.x} ${c.y+5}`} fill="none" stroke="#96886a" strokeOpacity=".25" />
        </g>}
        <g transform={water ? "translate(0 12)" : undefined}>
          <polygon points={diamond(p.x,p.y)} fill={`url(#${uid}-${surface})`} />
          <polygon className={water ? "p1v-water-glint" : "p1v-ground-tone"} points={diamond(p.x,p.y)}
            fill={water ? "#8eb9ad" : "#202b1e"} opacity={water ? .08 : .12} />
        </g>
      </g>;
    })}
  </g>;
}

export function Landmarks({ dev }: { dev: boolean }) {
  const winch=center(MAP.winch), wagon=center(MAP.wagon);
  return <g className="p1v-landmarks" aria-hidden="true">
    {/* Decorative trees stay at the outer forest edge, away from the west-bank unit cluster. */}
    {[{x:0,y:0},{x:1,y:0},{x:10,y:7},{x:10,y:8}].map(p => {
      const at=center(p); return <g key={key(p)} transform={`translate(${at.x} ${at.y})`}>
        <Prop crop="0 0 680 683" x={-37} y={-80} width={74} height={88} />
      </g>;
    })}
    {/* Only the surviving banks get planks. The broken river cells remain open water. */}
    {[{x:3,y:4},{x:6,y:4}].map(p => <g key={key(p)} transform={`translate(${center(p).x} ${center(p).y})`}>
      <path d="M-31-3L-2-20 31 0 2 17Z" fill="#776047" stroke="#c0a77b" />
      <path d="M-24 1L5-16M-14 7L15-10M-4 13L25-4" stroke="#332d25" strokeWidth="3" />
      <path d="M-27 4v15M25 2v17" stroke="#484236" strokeWidth="6" />
    </g>)}
    <text x={center({x:5,y:4}).x} y={center({x:5,y:4}).y+18} textAnchor="middle">斷橋</text>
    <g transform={`translate(${winch.x} ${winch.y})`}>
      <ellipse rx="23" ry="8" cy="4" fill="#0b1411" opacity=".6" />
      <path d="M-20-2L0-14 22-1 0 12Z" fill="#67543c" stroke="#c6ae7d" />
      <path d="M-11 0V-24M11 2V-22" stroke="#3b3026" strokeWidth="7" />
      <path d="M-12-14H13" stroke="#9c875c" strokeWidth="8" />
      <circle cy="-21" r="14" fill="#2c3028" stroke="#c7a767" strokeWidth="3" />
      <path d="M-11-21H11M0-32V-10M-8-29L8-13" stroke="#d4bc83" strokeWidth="2" />
      <text y="-43" textAnchor="middle" data-p1v-landmark="winch">絞盤{dev ? " (2,1)" : ""}</text>
      <path className="p1v-objective-pin" d="M-4-58L0-62 4-58 0-54Z" fill="#e5cd91" />
    </g>
    <g transform={`translate(${wagon.x} ${wagon.y})`}>
      <ellipse rx="35" ry="10" cy="6" fill="#0b1411" opacity=".5" />
      <path d="M-35-7L-9-20 36 7 10 22Z" fill="#735e44" stroke="#bda37b" strokeWidth="2" />
      <circle cx="-18" cy="9" r="9" fill="#292a23" stroke="#887552" strokeWidth="3" />
      <circle cx="20" cy="23" r="9" fill="#292a23" stroke="#887552" strokeWidth="3" />
      <Prop crop="1370 150 678 490" x={-39} y={-51} width={78} height={62} />
      <text y="-57" textAnchor="middle">車隊</text>
    </g>
  </g>;
}
