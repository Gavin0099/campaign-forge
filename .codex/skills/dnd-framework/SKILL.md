---
name: dnd-framework
description: Design D&D-style classes, spells, monsters, conditions and campaign stories for an ORIGINAL commercial game using only open-licensed sources (SRD 5.1/5.2.1 CC-BY-4.0, ORC), with attribution, forbidden-IP checks, grid-tactics rebalancing and narrative principles. Use when a project wants "D&D feel" without using Wizards of the Coast IP or trademarks.
---

# D&D 式框架設計（原創商業遊戲用）

## 何時使用

- 為原創遊戲設計 D&D 式職業、法術、怪物、狀態、隊伍與戰役故事。
- 判斷某項 D&D 相關素材能否用於付費商品（Steam、主機、手機）。
- 把桌上規則改造成電腦戰棋（格子、回合、AI）規則。

不適用：免費同人作品（另見 Fan Content Policy）、官方授權合作、法律意見。本 skill 是工作規範，不是律師意見；發行前由人工確認。

## 一、授權規則

### 可安全使用的來源（商業可用，需署名）

| 來源 | 授權 | 備註 |
| --- | --- | --- |
| SRD 5.1（2014 規則） | CC-BY-4.0（亦可選 OGL 1.0a） | https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf |
| SRD 5.2.1（2024 規則） | CC-BY-4.0 | https://www.dndbeyond.com/srd |
| Black Flag Reference Document（Kobold Press） | ORC | https://koboldpress.com/black-flag-reference-document/ ；依 ORC 條款署名並遵守其保留材料 |
| Pathfinder 2e Remaster 等 ORC 釋出內容 | ORC | https://paizo.com/orclicense ；不可使用其保留材料（Reserved Material） |

優先使用 CC-BY-4.0：條款簡單、不可撤回。只用 OGL 1.0a 的第三方內容時，需附 OGL 全文與 Section 15，並避開 Product Identity。

### 署名範本（逐字使用，不加其他 Wizards 字樣）

SRD 5.2.1：
> This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

SRD 5.1：
> This work includes material taken from the System Reference Document 5.1 ("SRD 5.1") by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.

放在遊戲 credits 與商店頁／說明文件的授權段。官方只允許額外寫「compatible with fifth edition」或「5E compatible」。

### 禁止使用（不在 SRD，或屬商標）

- 商標與名稱：Dungeons & Dragons、D&D、Wizards of the Coast 標誌、龍形安培標、Forgotten Realms、Faerûn、Waterdeep、Baldur's Gate、Ravenloft、Barovia、Strahd、Dragonlance、Greyhawk、Eberron、Spelljammer、Avernus 等世界與地名。
- 非 SRD 怪物：beholder（眼魔）、mind flayer／illithid（奪心魔）、displacer beast、githyanki／githzerai、slaad、carrion crawler、umber hulk、yuan-ti 等（SRD 文字可能順帶提到名稱，但沒有數據塊，不等於授權）。
- 具名人物、神祇、組織、冒險模組情節（Curse of Strahd、Tomb of Annihilation 等的人物、地點、事件）。
- 官方書籍中非 SRD 的子職業、法術、專長、插圖、地圖與文字。
- 行銷：不可寫「D&D 遊戲」「Dungeons & Dragons 授權」，不可暗示官方認可。描述可用「經典奇幻 TRPG 啟發」「5E compatible」（僅限確實使用 SRD 規則時）。

### Fan Content Policy

https://company.wizards.com/en/legal/fancontentpolicy ：只允許**免費**同人作品，不得販售或收費存取。**付費遊戲不能依此政策使用任何 Wizards IP。**

## 二、改編工作流程

1. **列需求**：先寫遊戲需要的職能（前排、控場、治療、爆發、偵察），不要先抄職業表。
2. **查來源**：只從上方安全來源取用；每一條記下來源 ID，例如 `SRD5.2.1:Spells/Fireball` 或 `BFRD:Monsters/xxx`。
3. **原創化**：
   - 重新命名（即使 SRD 名稱可用，也優先取符合世界觀的原創名，減少與官方混淆）。
   - 重寫描述文字；SRD 規則文字可用，但故事、地名、敘述一律原創。
   - 外觀、陣營、文化重新設計；不要做「換皮眼魔」等近似非 SRD 怪物。
4. **為格子戰棋重平衡**（5E 原生不是格子戰術平衡的）：
   - 範圍法術以格數定義形狀（圓、錐、線），重新測試 AoE 對密集陣型的效果。
   - 反應（藉機攻擊）、掩體、高低差、夾擊需明確規則與 UI 預覽。
   - 骰子變異在少量單位的戰棋中過大，考慮預覽命中率、平均化或保底。
   - 休息與每日資源（法術欄）在連續關卡中需改為每關或每章重置。
   - 狀態（倒地、束縛、恐懼、魅惑等）改寫成持續回合數與可見圖示。
   - 以模擬或試玩驗證，不假設桌上數值直接成立。
5. **記錄**：在設計文件保留「原創名 ↔ 來源 ID ↔ 改動摘要」對照表，作為署名與審查依據。
6. **審查**：發行前跑下方檢查表，並由人工做相似性與商標檢查。

## 三、D&D 式敘事原則（只取原則，不取內容）

| ID | 原則 | 落點 |
| --- | --- | --- |
| P1 | 反派是被扭曲的美德，反覆現身，至少讓主角輸一次 | 每章出場表 |
| P2 | 每名同伴有 2–3 拍個人任務，與主線交織、可略過 | 同伴弧線文件 |
| P3 | 信任以隱藏階段門檻運作，不顯示分數 | 3–4 段信任 |
| P4 | 沒有完美結局，人人要與選擇和解 | 結局矩陣 |
| P5 | 先讓玩家愛上具名的人與地，再讓威脅觸及 | 每章「心之錨」 |
| P6 | 冒險鉤子從角色背景長出 | 同伴背景 ↔ 主線事件 |
| P7 | 隊伍內部分裂與背叛最痛，需有事前徵兆 | 背叛節點 |
| P8 | 小而親密的開場、可見的倒數 | 第一章與威脅刻度 |

輔助結構：關鍵真相至少三條線索（Three Clue Rule）；地城關可用五房結構（入口守衛 → 謎題 → 陷阱或挫折 → 高潮 → 報酬或轉折）；反派勢力可用「威脅推進表」（每章不處理就前進一步）。

## 四、檢查表

- [ ] 每項規則內容都有來源 ID，且來源屬於安全清單。
- [ ] credits 含正確逐字署名；無其他 Wizards 字樣。
- [ ] 無禁止清單中的名稱、怪物、世界、人物或情節；已搜尋全文與素材檔名。
- [ ] 行銷文案未使用 D&D 商標或暗示官方認可。
- [ ] 所有職業、法術、怪物有原創名稱與原創描述。
- [ ] 已針對格子戰棋重平衡，並有試玩或模擬紀錄。
- [ ] 美術未參考官方插圖構圖或非 SRD 怪物外形。
- [ ] OGL 內容（若有）已附 OGL 1.0a 全文與 Section 15，並避開 Product Identity。
- [ ] 不確定的授權已標註，發行前交人工審查。
