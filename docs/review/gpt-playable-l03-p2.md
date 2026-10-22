# GPT web review — playable-l03 P2 (opt-in enemy telegraphs and responses)

- Reviewer: ChatGPT web, campaign-forge project
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad9ef8a-1c80-83ee-bd29-97de78ccf0ad (sidebar title "P2 審查結論")
- Reviewed: codex/playable-l03-p2, ce45ad2..557b723 (brief ce45ad2, implementation 48652a6, handoff 557b723)
- Date: 2026-10-22 (Asia/Taipei)
- Transcription: Grok Bot copied this from the page text. Tables are rebuilt as pipe rows; the wording is unchanged. Sent once, no retry, no truncation. A diagram in section 4 rendered without text and is not reproduced.

---

## 1. 結論：needs Owner

P2 的敵人預告、延遲突破與取消機制已有可檢查的規則實作及測試證據，但尚不足以提升為正式玩法：已知的低成本勝利策略仍然成立。

審查範圍：ce45ad2..557b723，實作 48652a6，僅評估 P2 新增內容。

從實際程式碼與測試邏輯來看，P2 做對了三件事：

- 使用 enemyBehaviour: "p2" 獨立開啟實驗，不直接改變預設敵人行為。
- 將敵人突破拆成 blocked → prepare-breakout → breakout，並保存明確的目標、路徑與回合。
- 建立反事實測試：同一條防守路線，玩家是否回應敵人預告，可以改變勝負。

但目前的問題不在「敵人有沒有反應」，而在於敵人反應是否真的迫使玩家思考。

交接報告提供的搜尋結果顯示，玩家只需操作 Karen 兩次，就能在六回合內獲勝，完全不用應對敵人的突破預告。這代表 P2 可以創造局部戰術決策，卻沒有消除整體關卡的支配策略。

因此我同意交接報告的 CHEESE 判定，不建議直接將 P2 作為正式預設 AI。

## 2. 問題

以下依 P0 → P2 排序，列出能直接由程式碼或已保存證據確認的問題。

| Priority | File:line | Issue | Evidence | Suggested fix |
|---|---|---|---|---|
| P1 | rules.ts:169–186 | AI 受阻後需要額外準備回合，可能反而降低威脅 | 首次受阻先移動、再次受阻準備且等待、下一次才交換；每個階段都消耗敵方行動機會 | 保留預告，但重新校準受阻時的行動代價，避免反覆等待成為玩家最佳策略 |
| P1 | rules.ts:164–169 | 壓力判定依賴一條最短直達路線，沒有全面比較可選阻擋目標 | approachPath() 先依路徑長度選出單一解，再用該解的第一名盟友作為阻擋者；可能受到等長路線的固定排序影響 | 比較所有同長最短候選路線，明確定義 AI 的目標選擇策略 |
| P1 | rules.ts:173–181 | 敵人突破僅在阻擋者處於指定距離內時才能進入準備階段 | index <= 3 才會產生 prepare-breakout；否則只能持續處於 blocked 並靠近 | 為「逼近中」與「確實卡住」定義可驗證的行為進度，避免只重複阻擋意圖 |
| P1 | search-results.json、README.md:65–98 | 兩指令必勝策略仍然存在 | 已保存搜尋結果顯示 ≤2 moves 有 80 勝；最佳成本為 1 名角色、2 指令、2 格 | 在接受 P2 前，針對低成本等待與折返策略做新的對抗性驗證 |
| P2 | rules.ts:156–158, 189–198 | 取消預告時，同一名敵人可輸出取消事件及新的行動意圖 | 程式先發出 cancel-breakout，再繼續一般決策；消費事件的 UI 必須知道第一個事件只是通知 | 新增明確的事件語意或回合行動摘要，避免 UI 將取消誤認為第二次行動 |
| P2 | tests/playable-l03-p2.mjs:115–120 | 佈陣抽樣測試並非完整狀態空間驗證 | 測試以 i += 31 取樣初始佈陣；不能據此認定所有中途改位、替換和路徑競爭情況都覆蓋 | 增加針對多名敵人競爭與預告取消後重規劃的測試 |

其中第一、第四項直接影響遊戲性；第二、第三項屬 AI 決策品質與狀態機限制；第五、六項主要影響未來整合與驗證信心。

上述屬於程式碼結構及測試覆蓋已確認的限制，不代表每一項都已重現為執行期錯誤。

## 3. 與交接報告不符之處

整體而言，交接報告相當清楚地揭露了限制，沒有發現重大成果造假或將 P2 宣稱為正式完成的情形。但有兩個地方需要更精確。

| 交接說法 | 核對結果 |
|---|---|
| P2 產生可驗證的因果性重新決策 | 有程式與保存的測試結果支持。 reactionEvidence() 在 p2-support.mjs:10–32 比較回應、忽略，以及未啟用 P2 三種結果 |
| 預告後的突破會完全吻合原計畫 | 主要路徑符合設計，rules.ts:140–154 保存及執行相同計畫；但我尚未獨立執行所有狀態組合 |
| 取消預告會重新規劃 | 基本成立，但語意需要區分。 取消預告後同一階段可能繼續移動，並不代表取消本身消耗一個敵方行動 |
| 搜尋是完整、無截斷的搜尋 | 只對明訂的指令與回合界線成立。p2-support.mjs:94–113 枚舉有限指令數；六指令反應案例是另外的定向探測 |
| P1v 瀏覽器回歸通過 | 有保存的 26 項檢查報告與退出碼，但該測試是 P2 關閉 的舊畫面，不能證明 P2 UI 正常 |
| 所有舊版輸出保持不變 | compare 沒有列出舊版 UI／測試檔案變更，並有雜湊紀錄支持；我沒有在本機獨立重算所有雜湊 |

還有一個重要的契約問題：

AGENTS.md 與 RESOURCE-CHECKLIST.md 要求遵循的 docs/design/RULE-ADAPTATION-CONTRACT.md，在指定 P2 commit 下讀取結果為 404。這與交接報告說明一致，不能將不存在的規則契約視為已通過。

## 4. 遊戲性與故事觀點

P2 在規則層比以前更接近戰術遊戲，但還沒有讓玩家實際感受到更完整的遊戲。

P2 的主要價值，是讓敵人從固定尋路變成可以觀察玩家阻擋，預告突破，並讓玩家選擇是否回應。

（原回覆此處有一張「P2 新增的敵我互動循環」圖，頁面文字未包含其內容。）

從故事觀點來說，「敵人看穿防線並開始突破」比敵人一直往絞盤走更能製造緊張感。重要的是讓玩家看見即將發生的事，而不是讓規則在背景偷偷運算。

最值得做的一項改變：重新平衡敵人的受阻代價，讓預告機制創造真正的選擇，而不是額外贈送玩家等待回合。

建議先保留這套 state machine，再用相同六回合搜尋框架驗證修正後是否仍存在兩指令必勝。這比繼續新增敵人種類、攻擊或故事劇情更有價值。

## 5. 沒檢查到的部分

這次完成了 GitHub 原始碼、測試程式、搜尋實作、交接、驗證紀錄與資源清單的靜態審查。

以下不納入已驗證通過：

- 沒有在本機執行 Node、TypeScript build、Vite 或 Chrome 測試。
- 沒有親自操作 P2 戰鬥畫面；目前也沒有 P2 UI 整合。
- 沒有重新執行超過 190 萬筆候選的完整有界搜尋。
- 沒有實際逐張檢視二進位 PNG 截圖。
- 沒有執行真人玩家測試、完整六指令搜尋或全部角色組合的平衡測試。
- 沒有取得獨立 Claude P2 審查。
- 沒有逐一重新讀取外部 prototype-fast、level-design、game-ai SKILL.md 的完整內容，因此不將 Codex 的 skill 使用紀錄當成我自己的獨立驗證。

## 6. 給 Gavin 的決策

我建議以下三項決定，不需要新增故事或擴大功能。

1. 保留 P2 作為 opt-in 實驗，不合併成正式預設 AI。 規則機制有研究價值，但目前的 CHEESE 結果尚未解決。
2. 授權一個小型平衡修正 slice。 目標只處理敵人受阻／準備回合造成的低成本勝法，維持完整預告與公平反應窗口。通過條件是重新執行有界搜尋，確認支配策略是否實質改善，而不是單純增加敵人強度。
3. P2 平衡改善後再與 P1v2 整合。 先確認規則值得保留，再實作預告視覺化；否則很可能替一套尚不成熟的 AI 機制製作過多 UI。

## 7. 資源檢核

依據 RESOURCE-CHECKLIST.md 的 A～D 原始檢核項目逐項填寫。以下 PASS 代表在 P2 授權範圍及可取得證據內 通過，不等於整個遊戲已驗收。

### A. Skills

| 項目 | 結果 | 證據 |
|---|---|---|
| prototype-fast | PASS | docs/tasks/playable-l03-P2-enemy.md:12–24, 26–40：聚焦兩種敵方反應，預先定義驗收與時間範圍 |
| level-design | FAIL | search-results.json：仍有 80 條兩指令內勝利候選，關卡策略尚不具足夠區別 |
| game-ai | PASS | rules.ts:125–201：敵方受阻、預告、突破、取消與重規劃狀態明確，具有玩家狀態反應 |
| game-ui-ux | N/A | P2 規格 :5–7, 24 明確禁止 UI 修改；預告尚未視覺化 |
| game-feel | N/A | 未修改動畫、打擊反應或演出節奏 |

### B. Reference repos

| 項目 | 結果 | 證據 |
|---|---|---|
| Grid-Tactics 架構隔離 | PASS | rules.ts:203–255：狀態與事件由純規則處理，沒有 React 視圖依賴；未見引用該專案的程式或素材 |
| HopeMetal/2DTacticalRPGDemo 授權 | N/A | 本次差異沒有複製該專案程式或素材；無新增可歸屬該專案的資源 |
| 禁止未核准新引擎／依賴 | PASS | commit compare 未列出 package／lockfile 變動，也沒有新增遊戲引擎 |

### C. Playable acceptance bar

| 項目 | 結果 | 證據 |
|---|---|---|
| 玩家能自行完成 3–5 分鐘戰鬥 | N/A | P2 沒有 UI；無針對 P2 的真人操作證據 |
| 敵人行為可理解並回應玩家 | PASS（規則層） | rules.ts:140–198：reason、targetAlly、plan、action 提供明確行為依據；玩家理解程度尚未實測 |
| 玩家可以勝利或失敗 | PASS | search-results.json 包含勝敗搜尋結果及反事實案例 |
| 兩種戰術選擇導致不同後果 | PASS（局部） | p2-support.mjs:10–32 與 search-results.json.keyGate：回應預告勝利、忽略預告失敗；但不代表整體策略深度已達標 |
| 玩家能重試並改變策略 | PASS（規則層） | rules.ts:204–206、p2.mjs:106–114：重試重建初始狀態 |
| 無重複結算、卡住、非法移動或動畫中斷 | PASS（已測規則） | p2.mjs:15–47, 115–120 測試事件一致性、佔位與移動；動畫不屬於本次 P2 變更 |
| 1280×720、1920×1080 與鍵盤操作 | N/A（P2） | VERIFICATION.md 記錄舊 P1v 的 26 項瀏覽器檢查，且明確指出 P2 關閉 |
| 自動測試與真人試玩分開紀錄 | PASS | VERIFICATION.md 與 handoff 分開記錄自動測試及未執行真人驗收，沒有混為一談 |

### D. Project rules

| 項目 | 結果 | 證據 |
|---|---|---|
| SRD 5.2.1、CC-BY 與規則調整契約 | N/A（正式改編） | rules.ts:1 註明是原創暫行佔位規則；本次沒有新增 WotC IP，但指定的 RULE-ADAPTATION-CONTRACT.md 無法取得，正式規則合規不能判定 PASS |
| AGENTS.md 授權／分支／故事限制 | PASS（變更範圍） | ce45ad2..557b723 僅增加 P2 rules、tests、evidence、handoff；沒有修改 P1v UI、故事、main 或建立 PR。工作樹操作紀錄則依交接收據，未獨立現場驗證 |

最終資源檢核： A 有一項遊戲性 FAIL；C 有範圍限定的 PASS，但仍缺 P2 真人遊玩與畫面驗證；D 未見超出已授權的程式變更。

依照專案的驗收原則，P2 可保留為實驗成果，不應被解讀為可正式採用、完成玩家驗收或已準備合併的最終戰鬥 AI。

本次審查僅在此回覆提供，沒有修改 GitHub 檔案、建立 review branch 或推送 commit。
