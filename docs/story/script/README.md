# 《碑誓》對白腳本（Ink）

**格式選擇**　採 [ink](https://github.com/inkle/ink)（MIT）。理由：純文字、可 diff、適合 Git 與代理協作；引擎未定時可用 [inkjs](https://github.com/y-lohse/inkjs)（MIT）在瀏覽器／React 原型執行，日後若選 Unity 有 [ink-unity-integration](https://github.com/inkle/ink-unity-integration)，選 Godot 有 [godot-ink](https://github.com/paulloz/godot-ink)。繁體中文內容可直接寫。

## 檔案

| 檔案 | 內容 |
| --- | --- |
| `main.ink` | 入口，INCLUDE 其他檔 |
| `globals.ink` | 全域旗標、隱藏信任與 `stage()` 對照函式 |
| `ch01.ink` | 第一章 L01–L04 |
| `ch02.ink` | 第二章 L05–L07；L08 起待文字試玩後續寫 |

## 慣例

- knot 名稱：`L##_pre`、`L##_battle`、`L##_post`；個人任務用 `P##_*`。
- 標籤：`#speaker:名字`、`#scene:ID`、`#bg:場景`、`#battle:關卡ID`、`#objective:文字`、`#trigger:事件`、`#flag:旗標`。標籤是給未來執行端的提示，不是引擎規格。
- 戰鬥規則、數值、技能與法術不寫在腳本；只在 `levels/L##.md` 寫敘事目標，能力名稱一律等 G005。
- 信任數值為隱藏故事狀態，對應 [COMPANION-ARCS](../COMPANION-ARCS.md) 四段。

## 驗證（不寫入 repo 的本機暫存）

```
mkdir -p /tmp/inkcheck && cd /tmp/inkcheck && npm init -y && npm i inkjs@2
npx inkjs-compiler -o /tmp/out.json <repo>/docs/story/script/main.ink
INKJS=/tmp/inkcheck/node_modules/inkjs node <repo>/docs/story/script/check/walk.js /tmp/out.json
```

`check/walk.js` 以狀態快照窮舉所有選項路徑，並檢查後果一致性（K1 與提歐、名鑰的對應；小昆與星盤不可兩全；章末刻度；小昆連結下限）。新增規則時同步更新 [FLAGS](../FLAGS.md) 的檢查欄。

最近一次結果（L01–L07）：編譯零錯誤；55,296 條終端路徑全部到達結尾；一致性錯誤 0。`#sim` 選項是文字試玩用的戰果模擬，不是玩家抉擇。這是語法、路徑與狀態檢查，不是文字品質或玩家測試。
