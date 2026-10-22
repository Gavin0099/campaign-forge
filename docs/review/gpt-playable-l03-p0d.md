# GPT web review — playable-l03 P0d (A search completion + enemy counter-pressure D)

- Reviewer: ChatGPT web, campaign-forge project
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad9a198-9114-83ee-b461-0937f1b8eb71
- Reviewed: codex/playable-l03-p0d, 13a6e17..2dc92b6 (implementation cafe688, handoff 2dc92b6)
- Date: 2026-10-22 (Asia/Taipei)
- Transcribed by Grok Bot from the page's accessibility tree. Tables are rebuilt as pipe rows; the wording is unchanged. The request was accidentally sent twice and got one reply.

---

## 1. 結論：PASS（驗證），needs Owner（玩法決策）

P0d 工程驗證 PASS。同意搜尋與規則驗證基本成立，但不完全同意 Codex 對 A、A+D 給予「OK (bounded)」的遊戲性評價。重新區分：工程／數學驗證 PASS；A：THIN；D：CHEESE；A+D：THIN，但優於 A 的靜態防守限制；是否足以作為正式戰鬥規則：尚未通過。

| 項目 | 判定 | 證據 |
|---|---|---|
| OK 條件事先宣告 | PASS | `P0d-pressure.md` 與 `playable-l03-p0d-search.mjs:6–12` |
| 使用真正規則，而非第二套模擬器 | PASS | `p0d-support.mjs:58–77` 使用原本 `resolve()`、`legalMoves()` |
| 最多 2 個指令搜尋 | PASS | `p0d-support.mjs:58–77` |
| 最多 3 個指令搜尋 | PASS | 同上；每回合最多 2 指令，無狀態截斷 |
| Solo／Duo 搜尋 | 部分 PASS | `p0d-support.mjs:82–118`；雙人較寬搜尋有 transition cap |
| Witness 可重播 | PASS（提交證據） | `playable-l03-p0d.mjs:120–165` |
| 可重現性 | PASS（提交證據） | `VERIFICATION.md:19–29`：兩次正式搜尋 exit 0、輸出雜湊一致 |
| 原規則預設未改 | PASS | `rules.ts:10–12,23,71–83`；`p0d` 可選且預設不存在 |
| P0／P0b／P0c 回歸 | PASS（提交紀錄） | 8／9／9 tests 與原始 JSON 比對均回報 exit 0 |
| 只做 P0d | PASS | Diff 僅涉及規則實驗、搜尋、測試、證據與專屬 handoff |

沒有發現必須使整個 P0d 驗證作廢的錯誤。以下評分是依搜尋結果做出的遊戲設計判斷，不是程式測試結果。

## 2. 問題（P0–P2）

| 優先級 | file:line | 問題 | 證據 | 建議 |
|---|---|---|---|---|
| P0 | — | 未發現已確認的 P0 程式阻擋問題。 | 原始測試與 witness 有回歸驗證。 | P0d 可結案。 |
| P1 | `p0d-search.mjs:53–60` | OK 門檻不足以證明戰術深度。 | 只要求多個粗略策略 family、勝率低於 50%、最低成本不超低。 | 保留「bounded gates PASS」，但遊戲性降為 THIN。 |
| P1 | `p0d-support.mjs:18–25` | Family 數可能誤導。 | 僅依最後站位所屬區域與是否 T1 後移動分類。 | 補充敵方反應差異與關鍵決策節點。 |
| P1 | `rules.ts:105–124` | D 的反制沒有解決最佳策略。 | A/A+D 最低成本勝法都未觸發 breakout。 | D 不宜直接當成 P2 的正式 AI。 |
| P1 | `rules.ts:170–174` | 反制預告語意不完整。 | 敵人先輸出 `intent: blocked`，可能隨即執行 `breakout`。 | P2 必須能提前區分 blocked、準備突破、實際突破。 |
| P2 | `p0d-support.mjs:82–118` | 雙人無勝法的結論受到截斷影響。 | Duo 寬搜尋達 transition cap。 | 不能認定 A/A+D 雙人不可解。 |
| P2 | `rules.ts:117–124` | 強制交換位置沒有玩家操作或反制成本。 | 遭阻擋者可把我方直接換到前一格。 | P2 應檢查玩家是否能預測及回應此效果。 |

最重要的發現：A+D 並非靠持續戰鬥獲勝，而是利用移動時序操控敵方最短路徑。A 與 A+D 的共同最低成本勝法是：回合 1，凱倫 (2,5)→(1,5)、蕾絲 (1,3)→(3,4)；回合 2，凱倫回到 (2,5)，迫使騎士重新繞路；回合 3–6 全部等待。這條勝法的成本是 2 人、3 指令、5 格，D 突破事件 0 次，最終干擾進度 2／3。這證明 A+D 已排除部分過於簡單的靜態勝法，但沒有證明玩家需要持續觀察、判斷或操作才能獲勝。

## 3. 與交接報告不符之處

| Codex 宣稱 | Reviewer 判斷 |
|---|---|
| A、A+D 為 OK (bounded) | 同意符合事先定義的搜尋門檻；不同意視為遊戲性 OK。 |
| A+D 有 8 個策略 family | 數值是粗略站位分類，不是 8 種已證明有意義的戰術。 |
| A／A+D 單人、雙人沒找到勝法 | 可以這樣報告，但不代表不可解，尤其雙人搜尋已被截斷。 |

Codex 已在 handoff 承認上述限制；主要分歧是 OK 這個標籤容易被誤當成正式遊戲性驗收。

| 變體 | Codex | Reviewer | 關鍵原因 |
|---|---|---|---|
| A（6T） | OK (bounded) | THIN | 223／1,855,543 個三指令勝法；最低成本仍可 T3–T6 等待 |
| D（5T） | CHEESE | CHEESE | 一格移動勝法仍存在 |
| A+D（6T） | OK (bounded) | THIN，較有研究價值 | 沒有 T1 部署後直接等待的勝法，但最低成本路線仍完全避開 D |

D 作為 P0d 實驗是合理的：規則清楚、可重現。但 GPT 不建議照搬為正式敵人 AI，理由有三：
- 只有完全找不到合法路線才會累計 blocked，繞很遠的路不算。
- 敵人沒有針對玩家的真正弱點作戰，只是強制穿越。
- 強制交換若缺少明確預告，玩家會覺得規則突然改變。

D 更適合當 P2 的反制設計參考。

## 4. 遊戲性與 P2 建議

建議 P2 先沿用 A 的六回合試玩設定，不直接採用 A+D；把 D 的概念納入第二種敵方行為的設計。

| P2 行為 | 設計方向 | 需要輸出的證據 |
|---|---|---|
| 目標干擾 | 騎士接近絞盤並累積進度，沿用現有 A 行為 | `intent`、目標座標、路徑、原因 |
| 追弱點 | 當直接接近困難時，選擇阻擋關鍵通道的隊友，迫使其重新部署 | `intent`、被針對隊友、原因、實際行動 |

第二種行為不必立刻實作 HP 或攻擊，可先用一個最小且明確預告的位移效果驗證。必須加入三項驗收：
1. 意圖與行動一致：顯示「準備突破某位置」後，實際事件必須符合預告。
2. 玩家有反應機會：敵方反制在發動前必須有可理解的提示。
3. 真正改變策略：至少一條測試勝法必須因敵方反制而需要重新決策。

P2 不需要再等待另一輪 P0 搜尋。

## 5. 沒檢查到的部分

- 未獨立重跑搜尋；exit 0 與雜湊一致性來自 `VERIFICATION.md`。
- 沒有窮舉所有六回合、所有移動指令的可能策略。
- 沒有證明 A/A+D 的單人、雙人陣容一定不可解。
- 沒有真人試玩或敵方反制的可理解性驗收。
- 沒有驗證 P0d 與 P1v 分支整合後的實際 UI 行為。

## 6. 給 Gavin 的決策

1. 是否接受 P0d？建議 Yes。
2. 正式玩法暫時使用哪個變體？建議保留 A（6 回合）作為 P1v 試玩基準，A+D 僅保留實驗候選。
3. 是否授權 P2？建議 Yes，限定「目標干擾＋追弱點」兩種敵方行為，要求預告、原因、實際結果一致，且至少證明一種反制確實迫使玩家重新決策。

## 7. 資源檢核（RESOURCE-CHECKLIST A–D）

**A. Skills**

| 項目 | 判定 | 證據 |
|---|---|---|
| prototype-fast | PASS | `playable-l03-p0d-search.mjs:6–12`、`README.md:9–25` |
| level-design | FAIL（戰術深度） | A/A+D 仍有三指令後等待勝法；封閘勝利不在本輪 |
| game-ai | PASS（機制） | `rules.ts:105–124,152–183`；戰術品質仍未通過 |
| game-ui-ux | N/A | P0d 明確排除 UI |
| game-feel | N/A | 沒有動畫、命中反應或節奏實作 |

**B. Reference repos**

| 項目 | 判定 | 證據 |
|---|---|---|
| Grid-Tactics | PASS | 純規則／事件架構；未借用外部程式碼 |
| HopeMetal／素材授權 | N/A | 沒有新增第三方程式或素材 |
| 不新增引擎或依賴 | PASS | 沒有 package／lockfile 變更 |

**C. Playable acceptance bar**

| 項目 | 判定 | 證據 |
|---|---|---|
| 完整 3–5 分鐘單人戰鬥 | N/A | headless 規則驗證 |
| 敵人行為可理解 | PASS（程式層） | `rules.ts:162–183` 與 P0d 測試；真人理解度未驗 |
| 玩家可勝可敗 | PASS | 三種變體都有可重播的勝敗策略 |
| 不同戰術選擇產生不同結果 | PASS（結果）／FAIL（深度） | A+D 有 8 個操作分類，但最低成本勝法只使用路徑延遲 |
| 重試並改變策略 | PASS | `playable-l03-p0d.mjs` 驗證 Retry 保留 config、清除 blocked 計數 |
| 無重複結算、卡住或非法移動 | PASS（已測規則） | 檢查合法地形、碰撞、交換、stale turn；動畫 N/A |
| 720p／1080p／鍵盤操作 | N/A | 沒有 UI |
| 自動化與真人證據分開 | PASS | `VERIFICATION.md:84–97` |

**D. Project rules**

| 項目 | 判定 | 證據 |
|---|---|---|
| SRD 5.2.1／CC-BY、WotC IP 與改編契約 | N/A（正式改編） | 只有原創暫定機制 |
| AGENTS／Owner 授權範圍 | PASS | 僅修改獨立 P0d 規則實驗、搜尋、驗證與交接 |

**最終 Reviewer 判定**

| 驗收層級 | 結果 |
|---|---|
| P0d 工程驗收 | PASS |
| A／A+D 戰術深度 | THIN |
| D 單獨作為正式機制 | FAIL |
| 進入 P2 | 建議授權 |

結論：不要再花時間用 P0 搜尋微調回合數、站位與勝利門檻。下一步應讓 P2 的敵人行為真正要求玩家觀察威脅、理解意圖、重新部署，再由真人試玩判斷。
