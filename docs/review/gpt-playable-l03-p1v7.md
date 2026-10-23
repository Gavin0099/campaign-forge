<!-- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6adb24b8-2098-83ee-8727-1bdfeb6b674a title "P1v7 修正審查" (initially "Review P1v7 fixes"). Text captured from ChatGPT's Copy button via paste. -->

## 1. 結論：needs Owner

P1v7 的三項追蹤事項，兩項已有程式碼及測試證據支持修正，另一項已依 Gavin 決策保留為已知限制；建議技術上有條件接受，但不等同完整遊戲體驗驗收。

零移動回合回饋

修正有據

受阻標記與事件同步

修正有據

最後一名敵人落地與 finish() 同時

已接受限制

真人可玩性與美術驗收

待 Owner

審查基準為 [`67c4dd8...ff87682`](https://github.com/Gavin0099/campaign-forge/compare/67c4dd8...ff87682?utm_source=chatgpt.com)，已讀取核心程式、測試、交接、驗證及資源檢核表，並檢視提供的五張 1280×720 畫面。

值得肯定的是，這次沒有為了解決動畫問題而延長所有回合，也沒有修改遊戲規則。但技術測試通過與玩家實際感受到回饋，是兩種不同的驗收。

## 2. 問題

以下只列實際程式或測試可確認的限制，不把已經修正的 P1v6 問題重複當成新缺陷。

| Priority | File:line                          | Issue                                            | Evidence                                                                                                                 | Suggested fix                                        |
| -------- | ---------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| P2       | `PlayableL03.tsx:186–197`          | 零移動回合的結束回饋只採用第一個 `winch` cue                     | `timeline.find()` 只取第一筆；阻擋事件則使用 `flatMap()` 收集全部。若日後單回合出現多筆進度事件，畫面無法完整表達它們。                                              | 本版不必修改；未來支援多個 progress event 時，改為按事件佇列播放或聚合並明確顯示總變化。 |
| P2       | `PlayableL03.tsx:167–181, 233–235` | 標記同步以 feedback cue 的 `eventIndex` 推進，不是獨立逐事件播放游標 | 目前 `playCue()` 在 block、landing、winch cue 到達時更新 `playedIndex`；沒有 cue 的 intent 不會單獨推進游標。對現有 blocked event，因為它有對應 cue，結果成立。 | 保留本版；若修改事件種類或同時間事件順序，應加上事件順序測試，避免游標語意失效。             |

P0：未確認新的阻斷問題。P1：原先兩項待修問題已找到對應修正。

### 三項舊問題的核對

A. 最後落地與 `finish()` 同時：接受，文件誠實。

[`PlayableL03.tsx:206–215`](https://github.com/Gavin0099/campaign-forge/blob/ff87682/ui-prototype/src/playable-l03/PlayableL03.tsx?utm_source=chatgpt.com#L206-L215) 顯示最後一步到達後直接呼叫 `finish()`，沒有額外 `setTimeout`、額外 RAF 或等待灰塵消失。

程式註解、handoff 及 `VERIFICATION.md` 都明確說明最後落地與狀態提交共用邊界，並未宣稱所有落地都嚴格發生在回合結束之前。這符合 Owner 已接受的限制。

B. 零移動回合的回饋瞬間消失：已修正。

[`PlayableL03.tsx:186–198`](https://github.com/Gavin0099/campaign-forge/blob/ff87682/ui-prototype/src/playable-l03/PlayableL03.tsx?utm_source=chatgpt.com#L186-L198) 先執行 `finish()`，再建立獨立 `settledCue`，並用 `performance.now() + 750` 設定到期時間。

[`PlayableL03.tsx:110–119`](https://github.com/Gavin0099/campaign-forge/blob/ff87682/ui-prototype/src/playable-l03/PlayableL03.tsx?utm_source=chatgpt.com#L110-L119) 包含序號比對、計時器清理，以及 Reduced Motion／跳過動畫取消。

此 cue 不擁有 `pending` 或 `busy`。測試也針對立即接受輸入、選取清除、重新結算替換、Retry 和到期後不重複提交設計檢查。

[Dark Fantasy Isometric Adventures Midjourney Prompt | PromptBase](https://images.openai.com/static-rsc-4/r_aEVla27ODZXeEOw6WhEgNYHjtOJ32DWkpJA4oiQfaVPSSY3notwQFeRE84VqIhm2sPpMF2T8r4wKKRMGwWL2U6GMNV3-ezlkJsTHqVLgyTvKEaEq0G1o1zBbMiucGipL2Ds4uti1t2ptJUzlVg5on6-mE5a4HsFjZwJsanupE?purpose=inline)

驗證重點：絞盤回饋在結算後仍可辨識。

[Prelude Dark Pain on Steam](https://images.openai.com/static-rsc-4/HRRz7k3WoOhqFadLqZG8Ifjs_8eA5uvEJLArlOSHCErgN8vEAeEFCZYR351ouvXroCi-L0cD8PPu6muwUZzCzOsSv4qVjpLTKg3WTldrT8zkRkYVncdJct4kKSGRmdQS_YRoJZ8zI_b8U8n4bFHO_rq6F7Bx83DwJysZ9q-eFSY?purpose=inline)

驗證重點：阻擋文字與標記在結算後仍可辨識。

C. 播放期間提前透露受阻結果：已修正。

[`feedback.ts:30–38`](https://github.com/Gavin0099/campaign-forge/blob/ff87682/ui-prototype/src/playable-l03/feedback.ts?utm_source=chatgpt.com#L30-L38) 的 `blockedAtEventIndex()` 僅回傳目前播放索引之前已發生的 blocked intents。

[`PlayableL03.tsx:233–235`](https://github.com/Gavin0099/campaign-forge/blob/ff87682/ui-prototype/src/playable-l03/PlayableL03.tsx?utm_source=chatgpt.com#L233-L235) 區分播放期間的實際事件與一般預覽時的未來預測；[`363–364`](https://github.com/Gavin0099/campaign-forge/blob/ff87682/ui-prototype/src/playable-l03/PlayableL03.tsx?utm_source=chatgpt.com#L363-L364) 則使用 `visualUnits` 決定受阻標記位置。

新測試涵蓋先移動後受阻，以及先受阻、另一名敵人稍後移動的兩種順序。這是比只檢查回合結束畫面更有意義的回歸驗證。

## 3. 與交接報告不符之處

沒有確認重大不實宣稱；但有兩個表述需要縮小適用範圍。

| 交接宣稱                         | 審查結果                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| 所有既有行為斷言保留                   | 基本成立。P1v6 的 marker count assertion 從 End Turn 後移到之前，保留預覽檢查；P1v7 新測試補足播放期間的缺席及出現時機。這是合理修改，不是單純刪除失敗斷言。 |
| 125 個 game checks 通過         | 有對應測試程式、指令結果及 `evidence-audit.json`，但屬交付者紀錄，非本次獨立重新執行。                                               |
| 正常回合沒有增加等待                   | 程式未新增等待，且交付記錄的六步回合平均為 P1v6 的 1401.3 ms、P1v7 的 1407.0 ms。支持沒有明顯增加，但不能據此保證所有裝置均無延遲。                    |
| 所有已到達的 blocked intents 都正確同步 | 現有事件模式與兩個測試情境成立；其實作依賴 `buildFeedbackTimeline()` 產生 cue 的順序，並不是通用事件播放器。                               |
| 所有可玩性驗收完成                    | 交接並未如此宣稱，明確保留 `HUMAN_PENDING`。這點記錄正確。                                                                |

另外，handoff 記載本次為 commit-only、沒有 push，但所指定的 `ff87682` 現在已可從 GitHub 讀取。這只表示後續已有人完成遠端交付，不能據此判斷 Codex 違反當時的 commit-only 指令。

本次沒有 Claude 的 P1v7 審查，因此沒有 Claude 意見可交叉驗證。

## 4. 遊戲性與故事觀點

是，比 P1v6 更像可玩的戰術遊戲，但進步主要是操作回饋的一致性，不是策略深度。

五張提供的實際畫面顯示，手繪渡口、人物、絞盤、河道及馬車已能形成一致的暗黑奇幻戰場。新回饋可以讓玩家更清楚知道敵人何時被擋住、絞盤何時受到干擾。

不過，畫面仍存在以下體驗差距：戰場實際佔用的螢幕空間偏小、人物辨識依賴底座與標籤、敵方意圖面板較像測試工具，以及玩家的主要戰術選擇仍集中在移動和卡位。

依本次截圖的視覺檢查

已具備

戰場美術一致性

自然地景、人物與物件有統一方向。

仍需強化

行動與後果的連結

玩家不一定直覺理解誰阻止了誰、產生什麼代價。

下一個最值得做的單一改動：建立「行動 → 原因 → 後果」的戰場內回饋。

這是建議，不是已授權的新規則。例如騎士被托瑪阻擋後，讓短暫的視覺連結指向托瑪，再顯示「未能接近絞盤」。事件與結果都沿用現有規則，不需要新故事或新職業。

這比繼續增加火花、灰塵或動畫影格更有機會提升玩家的理解與參與感。真正的下一道門檻不是特效數量，而是玩家是否能解釋自己為何成功。

## 5. 沒檢查到的部分

本次已閱讀 GitHub 的實際檔案與測試原始碼，也檢視五張提交畫面，但沒有在本機啟動 React／Vite、執行 Node 測試、Playwright 或重新編譯。

因此，以下只能引用交付者的驗證紀錄，不能宣稱獨立重現：125 個檢查全部通過、55 張截圖雜湊、73 項來源綁定、Chrome 實際動畫計時，以及 1920×1080、200% 字級與鍵盤操作的完整瀏覽器行為。

此外，未進行真人連續遊玩、Reduced Motion 的人工觀察、不同硬體幀率測試，亦未獨立稽核 SRD 授權文件的所有歷史來源。程式差異清單沒有 `rules.ts`，但這不等於已重新驗證整個遊戲引擎。

## 6. 給 Gavin 的決策

建議接受 P1v7 的本次修補，停止針對這三項問題反覆迭代；不要因為仍有小型 P2 可改善點，就無限延長這個 slice。

需要 Owner 決定的只有兩件事：

1. 是否將 P1v7 標記為技術上接受、真人遊玩驗收待完成？ 我的建議：是。
2. 下一階段是否優先改善行動與後果的直覺性，而不是繼續增加特效？ 我的建議：是；先採用不更動規則的視覺回饋方案。

已接受的最後落地邊界不需要再次確認。

## 7. 資源檢核

依 [`RESOURCE-CHECKLIST.md`](https://github.com/Gavin0099/campaign-forge/blob/main/docs/review/RESOURCE-CHECKLIST.md?utm_source=chatgpt.com) 的 A–D 原始項目逐項填列。以下 PASS 僅代表指定範圍的證據足夠，不表示整個遊戲完成驗收。

### A. Skills

| 項目             | 結果   | 證據                                                              |
| -------------- | ---- | --------------------------------------------------------------- |
| prototype-fast | PASS | P1v7 task brief 先定義零移動、標記同步與不延長等待的保留條件；實作沒有擴大到規則。               |
| level-design   | N/A  | 本次沒有修改地形、路線、目標或部署；不能用這次測試證明所有路線皆具策略意義。                          |
| game-ai        | N/A  | 未修改敵方決策規則；原有 intent 邏輯沿用。                                       |
| game-ui-ux     | PASS | `PlayableL03.tsx:233–235` 與 `363–364` 區分事件標記和預測標記，截圖有目標進度及意圖面板。 |
| game-feel      | PASS | 750 ms cue、非阻擋輸入、事件同步標記、跳過與減少動態效果處理皆有程式及測試。                     |

### B. Reference repos

| 項目                          | 結果   | 證據                                                                          |
| --------------------------- | ---- | --------------------------------------------------------------------------- |
| franciscobom/Grid-Tactics   | PASS | `rules.ts` 維持獨立，`feedback.ts` 使用純查詢，React 負責事件視覺呈現；未發現本次導入外部程式碼。            |
| HopeMetal/2DTacticalRPGDemo | N/A  | 本次未借用新的程式、素材或設計模式，無新的授權標記需求。                                                |
| 新引擎或依賴的 PoC／Owner 核准        | PASS | Commit compare 未包含 `package.json` 或 lockfile 變更，亦未新增 Phaser、Godot、Pixi 等引擎。 |

### C. Playable acceptance bar

| 項目                         | 結果   | 證據                                                                           |
| -------------------------- | ---- | ---------------------------------------------------------------------------- |
| 玩家能獨自完成 3–5 分鐘戰鬥           | FAIL | 沒有無提示真人試玩或實測完整遊戲時間。                                                          |
| 敵人行動能依玩家狀態理解               | PASS | 既有意圖預測與本次受阻事件同步測試成立；真人理解仍待驗。                                                 |
| 玩家能勝利或失敗                   | PASS | 原有 P0/P1v 成敗路徑與回歸測試紀錄保留。                                                     |
| 兩種戰術選擇產生不同結果               | PASS | 原有防守與放任路線具不同結果；只達最低要求，策略深度仍薄弱。                                               |
| 能重試並改變策略                   | PASS | `PlayableL03.tsx:142–146` 及 P1v7 browser 測試涵蓋 Retry、回到初始狀態與取消殘留 cue。         |
| 沒有重複結算、卡回合、非法移動或動畫中斷       | PASS | `pending`、`busy`、序號到期與取消機制有對應測試；僅代表已測案例。                                     |
| 1280×720、1920×1080 與基本鍵盤操作 | PASS | 本次五張 720p 截圖，加上交付紀錄的既有 1080p、鍵盤及文字縮放回歸測試；未自行重跑。                              |
| 自動化測試與真人回饋分開記錄             | PASS | `feedback-results.json`、`evidence-audit.json` 及 handoff 均明列 `HUMAN_PENDING`。 |

### D. Project rules

| 項目                               | 結果   | 證據                                                                         |
| -------------------------------- | ---- | -------------------------------------------------------------------------- |
| SRD 5.2.1／CC-BY、無 WotC IP、規則調整契約 | PASS | 本次 `rules.ts` 未更動、沒有新劇情與外部素材；PASS 限定本 chunk，非全專案授權稽核。                      |
| AGENTS.md 授權範圍、未合併 main、未擅自新增劇情  | PASS | Task brief 明定 presentation-only；差異為 React、feedback、測試及交接文件，未見新增劇情或合併 main。 |

最終審查建議：P1v7 技術有條件接受，Owner 可結束此輪修補。 下一個工作應從「回饋是否按時出現」轉向「玩家是否真正理解戰術後果」，並以一次無提示真人遊玩作為重要驗收依據。
