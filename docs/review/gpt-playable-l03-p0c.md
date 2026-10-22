# GPT web review — playable-l03 P0c (win-condition variants)

- Reviewer: ChatGPT web, campaign-forge project
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad9a198-9114-83ee-b461-0937f1b8eb71
- Reviewed: codex/playable-l03-research, d42024b..99fe6da (baseline d42024b, implementation ab749d6, handoff 99fe6da)
- Date: 2026-10-22 (Asia/Taipei)
- Transcribed from the web page by Grok Bot. The page showed table cells one per line, so the tables were rebuilt as pipe rows; the wording is unchanged.

---

# Campaign Forge — P0c 獨立 Reviewer 審查

## 1. 結論：pass（驗證），needs Owner（玩法決策）

P0c 驗證通過。同意 Codex 的主要結論：A 是目前最值得保留的候選，但還不足以正式採用，更不能宣稱已達到有趣的戰術玩法。

| 驗證項目 | Reviewer 判定 | 證據 |
|---|---|---|
| 搜尋使用真正的遊戲規則 | PASS | playable-l03-p0c-support.mjs:74–121 呼叫既有 command()／resolve() |
| T1 配置搜尋 | PASS | support.mjs:19–28，終點去重，保留最低成本代表 |
| 跨回合最多一次移動 | PASS | support.mjs:29–34 |
| 多步策略搜尋 | PASS（有限範圍） | support.mjs:90–121，最多兩個移動指令，非完整五、六回合搜尋 |
| 可重現性 | PASS（提交證據） | VERIFICATION.md：搜尋兩次、P0c 9 tests、P0 8 tests、P0b 9 tests，均記錄 exit 0 |
| 原有預設規則不變 | PASS | rules.ts:9–11,22,67–75，變體 opt-in；原測試與 trace 回歸一致 |
| 未開始 P1 | PASS | Diff 僅新增驗證程式、文件及可選規則配置，沒有 UI、動畫或故事修改 |

限制：Reviewer 核對了原始碼與提交證據，但沒有在獨立執行環境重新跑 Node 測試，因此 exit code 屬 Codex 的執行紀錄，非本次獨立執行結果。

## 2. 問題（P0–P2）

| 優先級 | file:line | 問題 | 證據 | 建議修正 |
|---|---|---|---|---|
| P1 | playable-l03-p0c-search.mjs:37–44 | A 的 THIN 判定建立在尚未充分搜尋的策略空間 | A 沒有接受與 B/B+ 同等的跨回合兩指令搜尋 | 先補 A 的跨回合搜尋，再保留或修正 THIN |
| P1 | playable-l03-p0c-support.mjs:51–73 | A 的 solo/duo「none found」不能當成不可獲勝 | 每回合最多一指令、最多 10,000 個狀態、只搜尋部分策略 | 加入每回合 2–3 指令的有界搜尋，檢查單人、雙人是否仍可解 |
| P1 | rules.ts:142–149 | 勝利仍然主要取決於回合期限與被動的絞盤進度 | A 可第一回合部署後等待到第六回合獲勝 | P0d 應測試是否需要持續防守、敵方壓力或玩家主動操作 |
| P2 | playable-l03-p0c-support.mjs:90–120 | 24,668 個策略只涵蓋最多兩個移動指令 | 不是每回合各兩個移動、累計十個指令的完整搜尋 | 文件持續明確標示為 bounded search |
| P2 | playable-l03-p0c.mjs:35–59 | B/B+ 的條件測試正確，但沒有證明其戰術品質 | 兩次移動的成功 witness 仍存在 | 維持 CHEESE，不直接採用 |

沒有發現 P0 級驗證錯誤。

## 3. 與 handoff 不符之處及各變體判斷

沒有發現明確的數據造假或實作與 handoff 直接矛盾之處。不過，A 的 THIN 是有限搜尋下的暫定評級，不等於已證明不存在兩指令勝法。

| 變體 | Codex | Reviewer | 理由 |
|---|---|---|---|
| Baseline | CHEESE | 同意 | 一格移動就能勝 |
| A：6 回合 | THIN | 暫時同意 | 最便宜已找到的勝法需要 3 人、3 指令、8 格，但仍可第一回合部署後等待 |
| B：終局有人守點 | CHEESE | 同意 | 蕾絲兩次移動就能勝 |
| C：托瑪起點變更 | CHEESE | 同意 | 仍存在一次移動勝法，而且原 P0 trace 不再合法 |
| B+ N=2 | CHEESE | 同意 | 兩次移動後等待仍可勝 |
| B+ N=3 | CHEESE | 同意 | 同樣存在兩次移動勝法 |

A 的單人／雙人結論：不足以作為不可解的證據，但足以作為風險訊號。六種縮減陣容在目前限定搜尋中沒有找到勝法，不能直接認定必須三人才能獲勝，也不能證明單人／雙人模式不可能成功。更重要的是，A 的最佳已知方案仍然是「第一回合三人部署，然後等待」。它比原本困難，但不代表策略深度有實質提升。

A+B：尚不建議。六回合 B/B+ 的兩指令搜尋都是 0/24,922，這只能證明在這個搜尋範圍內找不到勝法，不是證明組合更好。增加條件可能只是讓關卡更難，甚至接近不可解。

## 4. 遊戲性與故事觀點

P0c 比 P0b 前進了一步：它找出了「增加防守期限」比單純要求相鄰守點更有機會去除低成本勝法。但核心玩法仍是靜態堵路與等待。目前玩家不必攻擊、不必援救、不必使用職業能力，也不需要在敵人抵達後持續調整策略。

下一個最值得測試的變更，不是再提高回合數，而是有限度的敵人反制：敵人連續被阻擋兩回合後，改變其進攻目標或採取簡單破局動作。這只是 P0d 的候選假設，不是正式規則或故事改動。

## 5. 沒檢查到的部分

- 沒有獨立執行 Node／build／scope 命令。
- 沒有完整窮舉五、六回合所有可能的玩家行動。
- A 沒有同等深度的跨回合兩指令搜尋，因此尚未排除更便宜的解法。
- 沒有驗證真人是否能理解或享受這些玩法。
- 封閘護送、完整敵方戰鬥與 QR-11 路線收益問題仍未驗證。

## 6. 給 Gavin 的決策

1. 接受 P0c 結案？建議 Yes。方法與主要數字具有可信證據，範圍符合授權。
2. 現在正式採用 A？建議 No。將 A 保留為優先候選，不改預設規則。
3. 是否授權 P0d？建議 Yes，但限制為最後一次小型純規則驗證：
   - 補齊 A 的跨回合低成本搜尋，以及 solo／duo 可解性。
   - 比較 A 與「敵人被堵住後改變行為」的簡單機制；不新增 UI、HP、動畫或故事。
   - 驗收重點不只是能贏，而是至少存在不同策略及可理解的代價，而且避免所有最佳策略都變成第一回合部署後等待。

不要無限延伸 P0。若 P0d 仍無法產生值得選擇的戰術行為，應重新檢討核心戰鬥設計，而非繼續微調期限與站位條件。

## 7. 資源檢核（RESOURCE-CHECKLIST A–D）

判定依 P0c 授權範圍；N/A 不等於未來驗收通過。

**A. Skills**

| 項目 | 判定 | 證據 |
|---|---|---|
| prototype-fast | PASS | playable-l03-p0c-search.mjs:6–10 定義問題、CHEESE／THIN／OK 標準，並維持小型驗證 |
| level-design | FAIL（深度） | A 尚未達 OK；B/C/B+ 存在低成本勝法；封閘勝利不在本輪範圍 |
| game-ai | PASS（規則驗證） | support.mjs:74–121 重用敵人決策程式；敵人缺乏破局能力仍是已知問題 |
| game-ui-ux | N/A | P0c 禁止 UI 變更 |
| game-feel | N/A | 沒有動畫或節奏調整 |

**B. Reference repos**

| 項目 | 判定 | 證據 |
|---|---|---|
| Grid-Tactics | PASS | rules.ts:115–155 狀態結算與事件輸出仍分離，沒有引入外部實作 |
| HopeMetal/2DTacticalRPGDemo | N/A | 本輪沒有借用程式碼或素材；原授權盤點不變 |
| 不新增引擎或依賴 | PASS | Diff 未修改 package／lockfile；VERIFICATION.md 記錄既有工具完成測試與 build |

**C. Playable acceptance bar**

| 項目 | 判定 | 證據 |
|---|---|---|
| 完整 3–5 分鐘單人可玩戰鬥 | N/A | Headless 驗證，沒有遊戲 UI |
| 敵人行為可理解 | PASS（程式層） | rules.ts:122–140 決定敵人移動與目標，既有 P0b AI 測試通過紀錄 |
| 玩家可以勝利或失敗 | PASS | search-results.json 含各變體勝敗統計 |
| 不同戰術產生不同結果 | PASS（結果）／FAIL（深度） | A 有 5 種 T1 勝利配置，但不能證明持續戰術選擇 |
| 重試並改變策略 | PASS（回歸） | playable-l03-p0c.mjs:71–78 驗證 retry 保留實驗配置、重設歷史 |
| 無重複結算、卡住回合、非法移動或動畫中斷 | PASS（已測規則）／N/A（動畫） | P0/P0b 回歸通過紀錄，P0c 的 9 項測試也涵蓋參數及結算條件 |
| 720p／1080p／鍵盤 | N/A | 本輪沒有 UI |
| 自動化與真人試玩分開 | PASS | VERIFICATION.md 明確區分 headless 結果及未進行的人類試玩 |

**D. Project rules**

| 項目 | 判定 | 證據 |
|---|---|---|
| SRD 5.2.1／CC-BY 與規則改編契約 | N/A（正式改編） | rules.ts:1,9–11 為原創暫定實驗規則，未引用新 SRD 內容或外部素材 |
| AGENTS／Owner 授權與範圍 | PASS | d42024b..99fe6da 僅增加 P0c 驗證、opt-in 規則與交接文件；未啟動 P1，也未改故事 |

Reviewer 最終建議：P0c PASS；A 保留候選；授權一次範圍受控的 P0d，再決定是否進入真正可玩的戰鬥實作。
