// Original, provisional scene layout. These are UI rehearsal values, not G005 rules.
export type Cell = { x: number; y: number };
export type SceneUnit = Cell & {
  id: string;
  name: string;
  role: string;
  hp: number;
  max: number;
  side: "ally" | "enemy";
  acted: boolean;
  color: string;
};
export type Gate = "open" | "sealed";
export const sceneRows = [
  "FFF.~~.....",
  "FF..~~.....",
  "F...~~..F..",
  "....~~.....",
  "...RRRRRR..",
  "....~~.....",
  "....~~...FF",
  "....~~..FFF",
  "....~~.FFFF",
];
export const sceneUnits: SceneUnit[] = [
  {
    id: "karen",
    name: "凱倫",
    role: "盾劍護衛",
    x: 2,
    y: 5,
    hp: 9,
    max: 9,
    side: "ally",
    acted: false,
    color: "#9e4f41",
  },
  {
    id: "lace",
    name: "蕾絲",
    role: "繩具與機關",
    x: 0,
    y: 2,
    hp: 7,
    max: 7,
    side: "ally",
    acted: false,
    color: "#c1a065",
  },
  {
    id: "thoma",
    name: "托瑪",
    role: "醫療與支援",
    x: 1,
    y: 7,
    hp: 8,
    max: 8,
    side: "ally",
    acted: false,
    color: "#7eaaa1",
  },
  {
    id: "knight",
    name: "議會騎士",
    role: "閘門方向",
    x: 3,
    y: 3,
    hp: 6,
    max: 6,
    side: "enemy",
    acted: false,
    color: "#a18998",
  },
  {
    id: "crawler",
    name: "登岸爬行者",
    role: "橋頭方向",
    x: 7,
    y: 4,
    hp: 8,
    max: 8,
    side: "enemy",
    acted: false,
    color: "#b19a80",
  },
];
export const gatePlans = {
  open: {
    title: "開閘接船",
    objective: "守住絞盤，接應三艘船",
    secondary: "留意岸邊落水者，保留接應路線。",
    cost: "提歐生還；橋梁被沖毀，筆記隨車隊沉沒。",
    short: "三船靠岸 · 橋梁失守",
    marker: "絞盤",
    markerCell: { x: 8, y: 1 },
    quote: "同一股水，能托起船，也能沖垮橋。",
  },
  sealed: {
    title: "封閘護橋",
    objective: "護送學院車隊通過橋頭",
    secondary: "沿岸可救援，最後一船仍無法返回。",
    cost: "筆記保住；提歐隨最後一船失蹤。",
    short: "車隊過橋 · 最後一船失聯",
    marker: "車隊",
    markerCell: { x: 8, y: 4 },
    quote: "橋還在。有些人的路，卻在這裡斷了。",
  },
} as const;
export const cellKey = (p: Cell) => `${p.x},${p.y}`;
export const cellDistance = (a: Cell, b: Cell) =>
  Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
export const sceneProject = (x: number, y: number) => ({
  x: 550 + (x - y) * 44,
  y: 90 + (x + y) * 15,
});
export const sceneDiamond = (x: number, y: number) =>
  [
    sceneProject(x, y),
    sceneProject(x + 1, y),
    sceneProject(x + 1, y + 1),
    sceneProject(x, y + 1),
  ]
    .map((p) => `${p.x},${p.y}`)
    .join(" ");
export function walkable(p: Cell, gate: Gate) {
  const tile = sceneRows[p.y]?.[p.x];
  return (
    !!tile &&
    tile !== "~" &&
    !(gate === "open" && p.y === 4 && (p.x === 4 || p.x === 5))
  );
}
export function movementCells(
  actor: SceneUnit,
  units: SceneUnit[],
  gate: Gate,
) {
  const reachable = new Set([cellKey(actor)]),
    queue = [{ ...actor, steps: 0 }];
  for (let i = 0; i < queue.length; i++) {
    const p = queue[i];
    if (p.steps >= 3) continue;
    for (const next of [
      { x: p.x + 1, y: p.y },
      { x: p.x - 1, y: p.y },
      { x: p.x, y: p.y + 1 },
      { x: p.x, y: p.y - 1 },
    ]) {
      if (
        !walkable(next, gate) ||
        reachable.has(cellKey(next)) ||
        units.some(
          (u) => u.id !== actor.id && u.hp > 0 && cellKey(u) === cellKey(next),
        )
      )
        continue;
      reachable.add(cellKey(next));
      queue.push({ ...actor, ...next, steps: p.steps + 1 });
    }
  }
  return reachable;
}
export function movementPath(
  actor: SceneUnit,
  destination: Cell,
  units: SceneUnit[],
  gate: Gate,
): Cell[] {
  const queue: Cell[][] = [[actor]],
    seen = new Set([cellKey(actor)]);
  for (let i = 0; i < queue.length; i++) {
    const path = queue[i],
      p = path[path.length - 1];
    if (cellKey(p) === cellKey(destination)) return path;
    if (path.length > 3) continue;
    for (const next of [
      { x: p.x + 1, y: p.y },
      { x: p.x - 1, y: p.y },
      { x: p.x, y: p.y + 1 },
      { x: p.x, y: p.y - 1 },
    ]) {
      if (
        !walkable(next, gate) ||
        seen.has(cellKey(next)) ||
        units.some(
          (u) => u.id !== actor.id && u.hp > 0 && cellKey(u) === cellKey(next),
        )
      )
        continue;
      seen.add(cellKey(next));
      queue.push([...path, next]);
    }
  }
  return [actor];
}
