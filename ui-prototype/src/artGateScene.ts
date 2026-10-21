import { sceneUnits } from "./l03Scene";

// Screen-space composition anchors, NOT a navigation mesh or replacement for sceneRows.
// Both render directions consume exactly this frozen pre-K1 inspection state.
export const artGateState = {
  id: "L03-pre-K1-art-study-v1",
  gate: "undecided",
  bridge: "intact",
  actions: 0,
  boats: 3,
  chests: 3,
  units: sceneUnits.map(({ id, name, hp, max, side, role }) => ({
    id,
    name,
    hp,
    max,
    side,
    role,
  })),
  anchors: [
    { id: "karen", x: 435, y: 454, size: 149 },
    { id: "lace", x: 312, y: 314, size: 127 },
    { id: "thoma", x: 253, y: 625, size: 153 },
    { id: "knight", x: 1034, y: 427, size: 134 },
    { id: "crawler", x: 846, y: 402, size: 140 },
  ],
  landmarks: [
    {
      id: "teo",
      name: "提歐的燈",
      x: 612,
      y: 76,
      detail: "最後一船仍在上游。蕾絲正等著這盞燈靠岸。",
    },
    {
      id: "boats",
      name: "三艘船",
      x: 710,
      y: 229,
      detail: "三船尚未靠岸；橋前的急流正把它們推向閘門。",
    },
    {
      id: "gate",
      name: "閘門與絞盤",
      x: 1340,
      y: 109,
      detail: "開閘接船或封閘護橋，仍未作出選擇。",
    },
    {
      id: "bridge",
      name: "渡口木橋",
      x: 815,
      y: 375,
      detail: "橋尚完整，兩岸仍相通。開閘之後，水會沖毀這條路。",
    },
    {
      id: "maggie",
      name: "瑪歌",
      x: 1315,
      y: 489,
      detail: "她攥著從店裡帶出的燈芯，站在車隊與逃難者之間。",
    },
    {
      id: "caravan",
      name: "車隊的三箱",
      x: 1404,
      y: 436,
      detail: "三只箱子還在車上。封閘能保住筆記，卻會失去最後一船。",
    },
    {
      id: "refugees",
      name: "逃難者",
      x: 1500,
      y: 547,
      detail: "大人帶著孩子離開低岸。水已漫過圍欄，退路正在縮小。",
    },
  ],
} as const;

export type ArtDirection = "a" | "b";
export const artDirections = {
  a: {
    name: "手繪奇幻",
    subtitle: "濕石、舊木與逆流中的燈",
    plate: "/art/art-gate/river-a-v1.png",
    party: "/art/l03-party-v1.png",
    enemy: "/art/l03-enemies-v1.png",
  },
  b: {
    name: "立體造型",
    subtitle: "切面地形、層次與定向光影",
    plate: "/art/art-gate/river-b-v1.png",
    party: "/art/art-gate/party-b-v1.png",
    enemy: "/art/art-gate/enemies-b-v1.png",
  },
} as const;
