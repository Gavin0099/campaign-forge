# GPT review: L03 P0b stance validation (097f5a7...373dca2)

- Date: 2026-10-22 15:20 (Asia/Taipei)
- Reviewer: ChatGPT web, campaign-forge project
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad9a198-9114-83ee-b461-0937f1b8eb71
- Scope: `docs/tasks/playable-l03-P0b-stance.md`, the P0b section of `docs/handoff/codex-playable-l03-research.md`, the search script, tests and results (implementation 0cf8017, head 373dca2).
- Transcription: Grok Bot copied this from the page, and tables are flattened. It is one reply, with no continuation.
- This is a model review. It is not Owner approval and not a human playtest.

---

Campaign Forge — P0b 獨立審查

比較 097f5a7...373dca2｜實作 0cf8017｜2026/10/22

## 1. 結論：CHEESE 成立，P0b 可接受
P0b PASS／遊戲性 FAIL

已讀取實際搜尋腳本、共用搜尋函式、9 項測試、結果 JSON、規則程式、任務書與 handoff。

Codex 的 CHEESE 結論可信。 搜尋確實呼叫正式的 command() 和 resolve()，不是另外模擬一套遊戲規則。

搜尋範圍 ｜ 勝 ｜ 敗 ｜ 判定
- 第一回合所有合法終點配置，其後等待 ｜ 493 ｜ 6,303 ｜ 可信
- 五回合最多移動一次 ｜ 6 ｜ 211 ｜ 可信
- 真正單人及雙人陣容 ｜ 6 種陣容皆找到勝法 ｜ 未完整統計 ｜ 存在性可信

但這些是特定搜尋空間的結果，不是所有五回合策略的總數，更不是玩家勝率。

最有力的證據是：

蕾絲第一回合不動，第二回合從 (1,3) 移動一格到 (0,3)，接下來全部等待，就能以進度 2 獲勝。

這代表玩家甚至不需要靠近絞盤守點，也能利用敵人尋路與五回合截止時間取勝。

測試腳本本身有固定數字斷言、結果檔逐位元組比較及重播測試；handoff 記錄兩次搜尋及兩次測試均 exit 0。不過我沒有在獨立 Node 環境重新執行，因此將其判定為原始碼與已提交測試證據一致，而非我另行執行的驗收。

## 2. 問題（P0–P2）
等級 ｜ 位置 ｜ 發現及影響
- P0 ｜ rules.ts:112–134 ｜ 核心 CHEESE：敵人被短暫拖延，五回合就自動勝利。沒有守點完成條件。阻擋一次即可利用時間獲勝。
- P1 ｜ playable-l03-p0b-search.mjs:9–17 ｜ 第一回合搜尋按最終站位去重，保留成本最低的代表。這適合統計不同配置，但不是所有指令順序的統計。
- P1 ｜ playable-l03-p0b-search.mjs:34–44 ｜ 最多移動一次的搜尋不包含兩次以上的跨回合策略。217 不能當作全部可能策略。
- P1 ｜ playable-l03-p0b-search.mjs:56–79 ｜ 單人／雙人只找第一個勝利 witness，且每回合最多一個移動指令；不能宣稱找到最佳解或完整勝率。
- P2 ｜ playable-l03-p0b.mjs:62–88 ｜ 敵人順序及平手測試充分證明目前結果可重現，但沒有驗證不同順序下的戰術公平性。
- P2 ｜ rules.ts:57–58 ｜ 新增地圖邊界檢查正確；playable-l03-p0b.mjs:15–35 有回歸驗證，未發現新問題。

沒有發現必須撤銷 P0b 成果的搜尋實作缺陷。

## 3. 三個提案評估
提案 ｜ 能否消除 CHEESE ｜ 副作用 ｜ 必要驗證
- A：延長至 6 回合 ｜ 不保證 ｜ 延長等待，可能只讓玩家多站一回合；也可能讓原本合理的守點策略失敗 ｜ 重跑兩種搜尋、原守點 trace、單人／雙人勝法
- B：勝利時須有隊友相鄰絞盤 ｜ 可排除已發現的遠端拖延勝法，但不能消除所有 CHEESE ｜ 玩家可能最後一回合才站到絞盤旁，仍然輕鬆獲勝 ｜ 搜尋最後一回合突入、單人守點、最少移動成本
- C：托瑪起點改為 (0,4) ｜ 不保證 ｜ 改變初始阻擋拓撲，可能製造新的卡位解法 ｜ 新部署下完整重跑搜尋與可達性測試

我的推薦
優先選 B 作為下一個實驗，不直接採用 A+B+C。

原因是目前的漏洞本質並非五回合太短，而是「玩家不需要實際保護絞盤也能勝利」。

不過 B 仍不夠完善。我更推薦比較以下替代條件：

B+：玩家必須在最後兩回合都維持至少一名隊友相鄰絞盤，且敵方進度低於門檻。

這會排除單純最後一回合衝進守點格的策略，也較符合「守住絞盤」的任務語意。

但兩回合本身也是暫定值，不應直接寫死。應測試原本四次移動的成功策略能否通過，以及是否又產生只移動一名隊員就能等待獲勝的新解法。

另外，不能把「找不到任何勝法」誤認為成功修好 CHEESE。

## 4. 給 Gavin 的決策
1. 接受 P0b 驗證結果。 CHEESE 有實際證據，原本的 P0 可解性仍成立，但戰術設計未通過。
2. 授權一個純驗證 P0c。 僅比較 A、B、C 及 B+，用相同搜尋範圍量化勝敗數、最低移動成本、原守點是否仍可勝。不修改正式玩法、UI 或故事。
3. 先不授權完整 P1。 等 P0c 證明至少有數種有意義且可重現的勝法，再進入 UI 與互動實作，避免把已知無聊的規則做成精美介面。

## 5. 資源檢核（僅列變化項目）
依 docs/review/RESOURCE-CHECKLIST.md：

項目 ｜ 判定 ｜ 證據
- A — prototype-fast ｜ PASS ｜ P0b 任務先定義 CHEESE 標準；搜尋與測試專注驗證，不擴充玩法。
- A — level-design ｜ FAIL（遊戲性） ｜ 493 個第一回合配置勝法，以及一格移動勝法，證明現行守點機制容易被利用。
- A — game-ai ｜ PASS（決定性）／FAIL（戰術品質） ｜ playable-l03-p0b.mjs:62–88 確認尋路平手與敵人順序；敵人仍容易被短暫阻擋拖延。
- C — 敵人行為可理解 ｜ PASS（程式層） ｜ 五種站位 trace 與兩種競爭目標測試均可重播。未經真人理解度測試。
- C — 兩種戰術選擇產生不同結果 ｜ PASS（勝敗）／FAIL（深度） ｜ 一格後退能勝利，站著不動會失敗，但未形成足夠戰術取捨。
- C — 無非法移動、卡住回合 ｜ PASS（已測範圍） ｜ 邊界修正、碰撞、平手與敵人順序測試；P0b 9 tests exit 0（依 handoff）。
- B — 無新增引擎與依賴 ｜ PASS ｜ 比較變更沒有增加套件；使用既有 Node 測試。
- D — 遵守授權範圍 ｜ PASS ｜ 唯一規則變更為 walkable() 邊界修正；A/B/C 均未實作。

其餘項目沿用 P0 審查結果，P1 UI、美術、鍵盤及真人遊玩仍屬 N/A。

最終結論：P0b 應該結案。下一步不是直接加敵人攻擊或更多功能，而是先驗證「玩家究竟做了什麼，才應該算成功守住絞盤」。
