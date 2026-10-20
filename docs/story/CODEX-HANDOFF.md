# Codex 交接：《碑誓》故事與腳本

更新日期 2026-10-20。本文件給在 `D:\campaign-forge` 工作的 Codex 使用。開始前照 [AGENTS.md](../../AGENTS.md) 讀 memory 與 PLAN；本交接不取代治理規則。

## 正典檔案（衝突時依此順序）

1. [docs/DECISIONS.md](../DECISIONS.md)：U001–U006 使用者陳述、P006–P008、G004／G005
2. [STORY.md](STORY.md)：世界規則、隊伍、勢力、六章、K1–K5
3. [COMPANION-ARCS.md](COMPANION-ARCS.md)、[ANTAGONIST.md](ANTAGONIST.md)、[ENDINGS-MATRIX.md](ENDINGS-MATRIX.md)
4. [levels/LEVEL-LIST.md](levels/LEVEL-LIST.md)、`levels/L##.md` 與 [FLAGS.md](FLAGS.md)
5. [script/](script/)：Ink 腳本；旗標名稱以 `globals.ink` 為準

`docs/candidates/` 的 A／B／C 與 `ui-prototype/` 的人名是歷史或展示，不是正典。

## 相關 skill

[.codex/skills/dnd-framework/SKILL.md](../../.codex/skills/dnd-framework/SKILL.md)：規則基礎決策（DECISIONS G005）與任何職業、法術、怪物、狀態設計都必須依此 skill 進行，只用其列出的開放授權來源、記錄來源 ID、避開禁止 IP 與商標。G005 未決前，仍不得在故事或關卡文件新增正式數值與能力。

## 下一步（依序）

1. **L01–L07 文字試玩（必須先做）**：用 Inky 或 inkjs 跑兩條以上路徑（至少 K1 開閘＋救小昆、K1 封閘＋救星盤），請人類讀者試讀並記錄：能否說出 K1 兩邊的所得所失、是否在乎燈芯屋與小昆、L07 是否覺得被強迫。紀錄放 `docs/story/playtest/L01-L07.md`，區分人類回饋與模型自評。
2. 依試玩回饋修 L01–L07；重新編譯並跑 `script/check/walk.js`，更新 [FLAGS](FLAGS.md)。
3. **試玩通過並經 Gavin 確認後**才寫 L08 回聲之路與第三章（L09–L12、P01），沿用 FLAGS 與 LEVEL-LIST 的風險緩解原則。
4. G004 通過後再改寫 README.md 與 docs/review/STORY-GATE.md（DECISIONS G006）。

## 限制

- **不新增職業、技能、法術、數值或骰子規則。** 只可使用 STORY 隊伍表中的職業名稱；能力一律寫敘事描述，等 G005。
- 不新增核心同伴或勢力；新的具名配角可加，但需列入該章心之錨或關卡表。
- 不得使用他作的人物、地名、台詞或情節（D&D 名作只作原則參考，見 NARRATIVE-GAPS）。
- 不修改 `ui-prototype/`、`governance/`、`scripts/`、`tests/`、`artifacts/`；不選引擎、不安裝套件進 repo。
- 保持黑暗基調但每個死亡或背叛須有事前可見徵兆。
- 蕾絲在任何條件下都不原諒凱倫；托瑪的底線與信任無關；伊瑟拉感情線以價值衝突推進。
- 抉擇後果優先以目標、缺席、增援與對白表達，不新增完整地圖分支（見 LEVEL-LIST〈製作風險緩解〉）。
- 主要腳本總數超過 LEVEL-LIST 的估算時停下，提出裁剪選項給 Gavin。
- 使用者陳述與代理觀察分開記錄；未得授權不 push、不開 PR。

## 驗收標準（每章）

- 每關有 `levels/L##.md` 表（目標、地圖、敵人、勝敗、出戰、戰前戰後、觸發、旗標信任、設計註記）與對應 `L##_pre/_battle/_post` knot。
- ink 編譯零錯誤；窮舉走訪無死路，所有路徑到達該章結尾或明確佔位。
- 每關至少一句台詞讓玩家感到某位同伴的個性；每章至少一個抉擇或旗標被後續讀取。
- 本章新增或讀取的旗標全部出現在 FLAGS.md。
- 不出現正典以外的職業、法術或數值。
