# Codex 交接：《碑誓》故事與腳本

更新日期 2026-10-20。本文件給在 `D:\campaign-forge` 工作的 Codex 使用。開始前照 [AGENTS.md](../../AGENTS.md) 讀 memory 與 PLAN；本交接不取代治理規則。

## 正典檔案（衝突時依此順序）

1. [docs/DECISIONS.md](../DECISIONS.md)：U001–U006 使用者陳述、P006–P008、G004／G005
2. [STORY.md](STORY.md)：世界規則、隊伍、勢力、六章、K1–K5
3. [COMPANION-ARCS.md](COMPANION-ARCS.md)、[ANTAGONIST.md](ANTAGONIST.md)、[ENDINGS-MATRIX.md](ENDINGS-MATRIX.md)
4. [levels/LEVEL-LIST.md](levels/LEVEL-LIST.md) 與 `levels/L##.md`
5. [script/](script/)：Ink 腳本；旗標名稱以 `globals.ink` 為準

`docs/candidates/` 的 A／B／C 與 `ui-prototype/` 的人名是歷史或展示，不是正典。

## 下一步（依序）

1. **L07–L08 腳本與關卡表**：照 LEVEL-LIST 與 ANTAGONIST 第二章出場；L07 莫瑞安必須贏，帶走小昆（`quin_taken=true`），玩家只能撤退。
2. **第三章 L09–L12 與 P01**：K2 寫入 `k2_revenge`，讀 `trust_lis`、`k1_gate`。
3. **旗標表**：新增 `docs/story/FLAGS.md`，列每個旗標的寫入點、讀取點與預設值，與 `globals.ink` 一致。
4. 每完成一章，跑 ink 編譯與路徑窮舉檢查（見 script/README），並更新 memory 與 PLAN。

## 限制

- **不新增職業、技能、法術、數值或骰子規則。** 只可使用 STORY 隊伍表中的職業名稱；能力一律寫敘事描述，等 G005。
- 不新增核心同伴或勢力；新的具名配角可加，但需列入該章心之錨或關卡表。
- 不得使用他作的人物、地名、台詞或情節（D&D 名作只作原則參考，見 NARRATIVE-GAPS）。
- 不修改 `ui-prototype/`、`governance/`、`scripts/`、`tests/`、`artifacts/`；不選引擎、不安裝套件進 repo。
- 保持黑暗基調但每個死亡或背叛須有事前可見徵兆。
- 主要腳本總數超過 LEVEL-LIST 的估算時停下，提出裁剪選項給 Gavin。
- 使用者陳述與代理觀察分開記錄；未得授權不 push、不開 PR。

## 驗收標準（每章）

- 每關有 `levels/L##.md` 表（目標、地圖、敵人、勝敗、出戰、戰前戰後、觸發、旗標信任、設計註記）與對應 `L##_pre/_battle/_post` knot。
- ink 編譯零錯誤；窮舉走訪無死路，所有路徑到達該章結尾或明確佔位。
- 每關至少一句台詞讓玩家感到某位同伴的個性；每章至少一個抉擇或旗標被後續讀取。
- 本章新增或讀取的旗標全部出現在 FLAGS.md。
- 不出現正典以外的職業、法術或數值。
