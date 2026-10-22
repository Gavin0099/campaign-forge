# GPT web review: playable-l03 P1v4 (art pass: continuous painted battlefield, painted props, second knight portrait, scale exception)

- Reviewer: ChatGPT web, campaign-forge project (static source review via GitHub; no tests run, PNG screenshots not rendered directly)
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ada19f4-6454-83ee-a4b3-89643d097237
- Reviewed: codex/playable-l03-research, 1803cfe..024292b (P1v4 brief f1e0ab6, implementation 8bd06db, handoff 024292b)
- Date: 2026-10-22 22:16 Asia/Taipei
- Prompt: docs/review/GPT-REVIEW-PROMPT.md, with section 7 資源檢核 against docs/review/RESOURCE-CHECKLIST.md
- Claude review: none for this chunk at review time.
- Transcription: Grok Bot copied this from the rendered page text. Tables are rebuilt as pipe rows; the wording is unchanged. Use the chat link above as the source of record.
- Transcriber note: the reply's own total line says 15 PASS / 1 FAIL / 3 N/A, but its section 7 tables contain 10 PASS / 1 FAIL / 4 N/A (15 rows). Left as written.

---

## 1. 結論

needs Owner — P1v4 已從重複菱形地圖推進到單一手繪戰場，但仍不能認定已達到完整商業戰術 RPG 的視覺品質。

審查範圍：1803cfe...024292b，共 3 個 commits。

依照實際讀取的程式與文件，P1v3 三項美術缺失的修復情況如下：

| P1v3 問題 | P1v4 判定 | 理由 |
|---|---|---|
| 重複菱形地板 | 程式層面已修復 | 改用單張 battlefield.png，閒置格線透明 |
| SVG 幾何道具 | 主要結構已修復 | 絞盤、斷橋、馬車改用繪製圖集，但仍有向量標籤與標記 |
| 美術語言不一致 | 部分改善 | 背景與道具採一致的手繪方向；角色本體、肖像、UI 的整體一致性仍需視覺驗收 |

不建議因為 79 項自動檢查的紀錄通過，就直接將美術品質標記為 PASS。 這些檢查主要證明功能、定位及既有行為沒有明顯退化，不是美術品質的客觀分數。

## 2. 問題

以下只列出已從原始碼或提交的證據確認的問題，不將未親自觀察的畫面缺陷寫成既成事實。

| Priority | File:line | Issue | Evidence | Suggested fix |
|---|---|---|---|---|
| P1 | presentation.tsx:12–20 | 角色未達要求的 1.2–1.5 格高度 | FIGURE_HEIGHT = 52，菱形格高度 52；實際不透明圖像僅 0.960–0.979 格。1.3 格試驗確實留下 lace/thoma 重疊失敗紀錄。 | 接受本次例外，但下一輪應處理角色占位與視覺比例，不能只繼續放大 SVG。 |
| P2 | presentation.tsx:17–32 | 第二騎士肖像與戰場角色不一致 | knight-2 有獨立新肖像，但兩個騎士的 Figure 都使用相同 l03-enemies-v1.png 裁切。 | 製作第二騎士對應的全身角色，保留同一光源、材質與輪廓語言。 |
| P2 | presentation.tsx:42–51、p1v4-browser.mjs:55–64 | 地圖美術與判定格的視覺對齊尚未被自動化充分驗證 | 程式檢查 99 個格子中心是否可點擊、河道是否不可通行；沒有直接判斷繪製河岸與邏輯河岸的像素誤差。 | 以診斷格線圖做人工重疊審查，特別核對河岸、斷橋、絞盤及馬車。 |
| P2 | p1v4-browser.mjs:43–53 | 自動化美術驗收僅檢查素材存在與結構，不檢查真正的風格一致性 | 五張肖像的驗證條件是五個不同的來源／裁切 signature；單一背景與四個道具實例的驗證是 DOM 數量檢查。 | 增設 Owner 視覺驗收表，比較材質、光線、人物大小、輪廓辨識及 UI 一致性。 |

P1 的角色尺寸是已確認未滿足原始目標，但符合任務 brief 中容許「以通過原本重疊測試的最大尺寸替代，並留下證據」的例外條款。因此不應直接視為阻擋整個 P1v4 交付的 P0。

## 3. 與交接報告不符之處

這次交接報告整體比單純宣稱 PASS 更審慎；我沒有發現足以判定它虛報測試結果的明確矛盾。

不過有三個需要限制解讀的地方。

第一，「五個不同肖像」與「五個不同戰場角色」不是同一件事。 交接所稱五種肖像 signature 與原始碼一致，但不能解讀成五個完整且各自不同的角色美術。

第二，「79 項 automated checks」並不等於 79 項獨立視覺品質驗收。 交接將它分為 26 項純測試與 53 項瀏覽器測試，和提交的命令紀錄一致；但其中大部分屬於既有功能回歸檢查。這不能證明整體畫風已統一。

第三，「52 為幾何最大高度」具有條件。 它是在現行站位、共同角色 viewport，以及零重疊測試不放寬的前提下成立，不代表未來採用其他角色構圖、視覺遮擋或透視呈現方式時，角色永遠無法放大。

交接已明確承認上述角色尺寸例外、騎士本體重複、動畫未新增，以及真人測試待完成，所以我不將它們重複列為交接不實。

## 4. 遊戲性與故事觀點

比 P1v3 更接近真正的遊戲，但改進集中在視覺場景，不是玩法。

最實質的進步，是戰場不再由 99 個可見的地板菱形拼貼構成，而是由一張連續環境插畫承載；輸入格線則轉為互動時才出現。這比較符合一般戰術 RPG 的呈現方式，也有助於減少工具介面的印象。

但遊戲性沒有因 P1v4 而實質增加。這次沒有改動敵人決策、勝敗條件、任務分歧或故事內容；這點也與交接承認的 THIN 狀態一致。

最值得做的一項改變：讓玩家行動的結果在戰場上產生可見反應。

例如，當絞盤受到干擾時，透過已有事件播放絞盤轉動、拉索緊繃或狀態變化的視覺回饋。這只是下一輪的功能建議，不是已實作項目，也不是新增劇情設定。

理由是目前最大的問題已逐漸不是背景有沒有畫好，而是玩家的決策是否讓世界產生反應。若只有角色位移、進度數字和回合提示，仍容易讓玩家感覺自己是在操作一個規則展示器。

## 5. 沒檢查到的部分

本次已透過 GitHub 連線實際讀取提交差異、React 元件、CSS、測試程式、資源紀錄、交接文件與 checklist。

以下不能宣稱完成：

- 沒有在本機重新執行 npm run build、Playwright 或 P0～P1v4 測試。提交紀錄顯示 exit code 0，但那是 Codex 的執行紀錄。
- 沒有直接渲染並逐張目視比對 720p／1080p PNG，因此不能判定畫面實際美感、素材邊緣或角色辨識度已合格。
- 沒有真人從頭完成 3–5 分鐘戰鬥。
- 沒有實測音效、Gamepad、Screen Reader、GPU 效能及不同瀏覽器。
- 沒有逐一審核外部 skills 原文或參考 repo 的全部程式碼與授權內容。

證據文件 VERIFICATION.md 及 evidence-audit.json 已記錄 53 項瀏覽器檢查、33 個截圖雜湊及 47 個來源綁定檢查，但這些是提交的紀錄，不是本次獨立重跑結果。

## 6. 給 Gavin 的決策

建議 保留 P1v4 的實作方向，暫不授予最終美術 PASS，也不因為視覺尚未完美而要求整個重做。

需要 Gavin 決定的事項最多兩項：

1. 是否接受角色暫時只有 1.0 格高？ 我建議接受為 P1v4 的工程例外，但下一輪必須重新評估角色比例，而非永久凍結。
2. 下一輪優先處理角色與環境融合，還是戰場互動回饋？ 我傾向先處理互動回饋，讓遊戲不只好看，也讓每次行動更有存在感；但最終排序應以實際截圖的視覺品質決定。

## 7. 資源檢核

依據 RESOURCE-CHECKLIST.md 的 A～D 原始項目逐條填寫。這是本次獨立審查判定，並未修改 main 上的 checklist 檔案。

### A. Skills

| 檢核項目 | 結果 | Evidence |
|---|---|---|
| prototype-fast | PASS | P1v4 brief 明定只處理視覺，且有保留或拒絕素材的條件；第一次戰場生成被拒絕並保留紀錄 |
| level-design | N/A | 沒有新增地形規則；P0 測試紀錄顯示既有可達性檢查 exit 0，非本次重新設計 |
| game-ai | N/A | 沒有修改敵方 AI；既有 deterministic traces 在 P0b 紀錄中仍通過 |
| game-ui-ux | PASS | PlayableL03.tsx:85–95, 190–221 保留可移動範圍、敵方意圖、預覽路徑與鍵盤操作 |
| game-feel | PASS | 限本次範圍：playable.css:68–70, 99–114, 148 保留著陸、回合提示與 Reduced Motion；不代表打擊感完成 |

### B. Reference repos

| 檢核項目 | 結果 | Evidence |
|---|---|---|
| Grid-Tactics 架構分離 | PASS | PlayableL03.tsx:85–95 查詢純規則，presentation.tsx 專責視覺呈現；原有 rules.ts 未修改 |
| 2DTacticalRPGDemo 授權及素材 | N/A | 本次沒有引入其程式碼或素材；STYLE.md 明確記錄使用原有與生成素材 |
| 不引入未核准引擎或相依套件 | PASS | Commit compare 未出現 package.json、lockfile 或新引擎修改 |

### C. Playable acceptance bar

| 檢核項目 | 結果 | Evidence |
|---|---|---|
| 單人完成完整 3–5 分鐘戰鬥 | FAIL | 無真人完整遊玩與計時證據；交接仍標記 HUMAN_PENDING |
| 敵方行動能根據玩家狀態理解 | PASS | 工程範圍：敵方預測與意圖顯示保留，P0b 軌跡紀錄通過；真人是否能理解仍待測 |
| 玩家能獲勝或失敗 | PASS | P1v browser 紀錄涵蓋勝利、失敗及結果畫面，exit 0 |
| 兩種戰術選擇產生不同結果 | PASS | P0 紀錄中 hold 成功、idle 失敗；但這只證明最小差異，不代表選擇深度足夠 |
| 可以重試並改變策略 | PASS | P0 與 P1v 回歸紀錄涵蓋 Retry、reset 與策略變更 |
| 無重複結算、卡住、非法移動或動畫中斷 | PASS | 既有 P0／P1v 檢查紀錄 exit 0；僅涵蓋已測試案例 |
| 720p、1080p、基本鍵盤操作 | PASS | P1v、P1v2、P1v3、P1v4 的瀏覽器證據與兩種解析度截圖已提交 |
| 自動測試與真人測試分開紀錄 | PASS | VERIFICATION.md 清楚標記 HUMAN_PENDING，沒有將模型審查當真人測試 |

### D. Project rules

| 檢核項目 | 結果 | Evidence |
|---|---|---|
| SRD 5.2.1、CC-BY、不得使用 WotC IP | PASS | 本次無規則改動；art-prompts.json 使用原創素材提示，差異中未發現新增 WotC 內容。此判定不等於全專案授權稽核 |
| AGENTS.md 授權、不得合併 main 或自行擴增故事 | PASS | 差異限 P1v4 相關素材、UI、測試與文件；交接記錄推送到工作分支，未合併 main、未新增劇情 |

資源檢核總計：15 PASS、1 FAIL、3 N/A

最終意見：P1v4 可作為下一輪工作的基礎，但仍需 Owner 目視驗收與真人遊玩驗證。 下一階段不應再以增加素材數量當成進度，而應衡量畫面整體一致性，以及玩家行動是否產生足夠清楚的遊戲回饋。
