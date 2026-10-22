# GPT web review — playable-l03 P1v2 (unit readability and tile selection)

- Reviewer: ChatGPT web, campaign-forge project
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad9a198-9114-83ee-b461-0937f1b8eb71
- Reviewed: codex/playable-l03-research, 684d189..8f8a42b (brief 63a1f11, implementation d98a472, handoff 8f8a42b)
- Date: 2026-10-22 (Asia/Taipei)
- Transcription: Grok Bot copied this from the page text. Tables are rebuilt as pipe rows; the wording is unchanged. The first send failed in the browser and created no chat; the prompt was then delivered once. The reply landed in the existing project chat "L03 P0 審查".

---

## 範圍

684d189...8f8a42b｜Brief 63a1f11｜Implementation d98a472｜Handoff 8f8a42b

## 1. 結論：pass

P1v2 工程 PASS

P1v2 已解決原先「角色圖像遮擋鄰格操作」的主要工程問題，並改善姓名顯示與單位辨識；但 720p 的角色辨識度仍需要 Owner 親自驗收。

我已讀取實際程式、CSS、Playwright 測試、任務書、handoff、驗證紀錄及指定 commit diff。這次只評估 P1v2，不重新審查 P1v 與早期規則。

### P1v2 驗收

| 項目 | 判定 | 實際證據 |
|---|---|---|
| 等角視角深度排序 | PASS | PlayableL03.tsx:127–133，依動畫中的實際腳點 Y、X、ID 排序 |
| 角色縮放、腳點錨定 | PASS（自動化） | PlayableL03.tsx:20–29；測試 88–105 |
| 鄰近單位不互相遮擋 | PASS（指定場景） | 測試 69–108，含絞盤附近與同列相鄰配置 |
| 格子獨立接收點擊 | PASS | playable.css:34–35、PlayableL03.tsx:200–214 |
| 我方／敵方辨識 | PASS | 圓形／菱形底座、不同顏色、姓名資訊 |
| 鍵盤與 200% 文字 | PASS（自動化） | 測試 129–152 |
| 原有規則與 A 不變 | PASS | Diff 未修改 rules.ts，A 仍只在新畫面啟用 |
| 真人辨識測試 | HUMAN_PENDING | 未提供真人試玩紀錄 |

handoff 記錄 P0／P0b／P0c 的 8／9／9 項、P1v 的 26 項、P1v2 的 9 項及 build 全部 exit 0。這些是提交的執行證據；我沒有獨立重跑測試。

## 2. 問題（P0–P2）

沒有發現已確認的 P0 阻擋問題。

| 優先級 | file:line | Issue | Evidence | Suggested fix |
|---|---|---|---|---|
| P1 | PlayableL03.tsx:20–29 | 角色縮到 24–28 × 26 SVG 單位，解決重疊，但降低人物細節辨識能力。 | 原圖被縮到小型 viewport；handoff 也承認 720p 細節損失。 | Owner 實測能否只看戰場分辨五名角色；不通過才調整大小或造型辨識。 |
| P1 | PlayableL03.tsx:157–165 | 姓名與狀態只有在 hover、focus 或 inspection 時出現，無法同時觀看所有角色名稱。 | inspectedUnit 條件渲染單一資訊列。 | 先維持現狀，但驗證玩家是否需要常態識別標記。 |
| P2 | PlayableL03.tsx:112–123 | inspection 與 selection 分開正確，但點擊敵人或已行動隊友後，操作狀態可能與玩家原本的行動意圖不同。 | 已行動隊友會清除 selected；敵人亦清除選取。 | 將「查看」與「取消行動選取」的回饋區分清楚。 |
| P2 | playable-l03-p1v2-browser.mjs:69–108 | 點擊測試集中在兩組指定配置，尚未覆蓋所有可能的密集單位排列。 | 測試涵蓋 100 次指標點擊，但場景數有限。 | 後續新增多單位擁擠場景時，再擴充幾何回歸。 |

其中前兩項屬於可讀性取捨與待驗收風險，不是已證實的操作功能失敗。

## 3. 與交接報告不符之處

核心技術敘述大致與實作一致。

「只有 tile 接收輸入」成立。 角色及地標使用 pointer-events: none，實際輸入交由格子 polygon 處理。

「角色有深度排序」成立。 排序依動畫中即時腳點，而非僅依起始座標。

「名稱不被人物遮擋」有測試支持。 新測試檢查資訊列 bounding box 與裁切後角色 viewport 不相交。

「原規則未修改」成立。 比較範圍沒有 rules.ts 變更。

但交接中的「可靠辨識角色」應限定為自動化辨識及點擊正確，不能延伸為真人玩家已能直覺分辨五名角色。

另一個交付資訊差異是：handoff 記錄 push 失敗、成果仍在本機，但指定的 8f8a42b 內容已可從 GitHub 讀取。因此該紀錄不能直接代表目前遠端交付狀態，應以最新遠端分支查核為準。

## 4. 遊戲性與故事觀點

P1v2 比 P1v 更接近可操作遊戲，因為改善的是戰術遊戲的基本需求：玩家必須知道自己點的是誰、移動的是誰，以及下一步會發生什麼。

這次選擇用較小角色加上獨立資訊列，而不是繼續放大人物或增加美術特效，工程方向合理。

不過它仍有一個重要取捨：

改善前
角色較大，形象比較清楚，但遮住周圍單位與格子。

改善後
角色、格子和點擊區分開，但人物變小，可能需要依賴資訊列辨識。

這是依程式與測試紀錄作出的比較；本次未能直接開啟 PNG 進行視覺品質評分。

最值得做的一項改善： 若真人試玩確認角色難辨，優先加入常態顯示的簡短識別標記，而不是重新放大整張人物圖。可用角色首字、圖示或職業符號，並確保不遮住格子。

本輪沒有改動劇情、角色背景或敘事內容。故事觀點維持 N/A，不需要額外新增設定。

## 5. 沒檢查到的部分

- 沒有獨立執行 Playwright、build 或 Python scope validator。
- 已確認 Before／After PNG 檔案存在於 diff，但未能直接解碼並目視比較，因此不宣稱美術品質通過。
- 沒有真人執行 3–5 分鐘遊玩。
- 沒有實測觸控裝置、完整螢幕閱讀器操作或手把。
- 沒有覆蓋所有可能的單位擁擠配置、全部縮放倍率與不同作業系統字型。

## 6. 給 Gavin 的決策

1. P1v2 是否結案？ 建議 Yes，工程範圍通過，沒有理由為了已驗證的點擊問題再重寫介面。
2. 角色目前大小是否接受？ 建議 Gavin 直接試玩 720p，且不要刻意把滑鼠移到角色上，確認能否辨識五名單位。若辨識失敗，再追加識別標記，不先投入全員動畫或新美術。
3. 是否繼續 P2？ 建議 Yes。P1v2 的主要任務是讓單位可靠可選，不應以完整美術品質作為 P2 的前置條件；但要保留真人辨識度問題。

## 7. 資源檢核（RESOURCE-CHECKLIST A–D）

### A. Skills

| 項目 | 判定 | 證據 |
|---|---|---|
| prototype-fast | PASS | 任務只修角色可讀性與點擊，沒有新增戰鬥機制；60 分鐘上限，handoff 記錄約 18 分鐘。 |
| level-design | N/A | 地圖、部署及規則不變；P0 成功 trace 回歸有紀錄。 |
| game-ai | N/A | 敵人 AI 未變；P1v 26 項回歸保留。 |
| game-ui-ux | PASS（自動化） | PlayableL03.tsx:112–165,200–214、P1v2 browser tests：選取、姓名、焦點、格子命中及 200% 文字。 |
| game-feel | PASS（移動呈現回歸） | PlayableL03.tsx:127–133：移動時持續排序；測試 155–168。命中反應與整體節奏仍未驗收。 |

### B. Reference repos

| 項目 | 判定 | 證據 |
|---|---|---|
| Grid-Tactics 架構分離 | PASS | rules.ts 未修改，所有 P1v2 互動變更都在 React 顯示層。 |
| HopeMetal 素材授權 | N/A | 沒有借用新程式或素材，仍使用原有圖片。 |
| 不新增引擎或依賴 | PASS | Diff 沒有 package.json 或 lockfile 變更。 |

### C. Playable acceptance bar

| 項目 | 判定 | 證據 |
|---|---|---|
| 玩家可獨立完成 3–5 分鐘戰鬥 | FAIL（HUMAN_PENDING） | 沒有真人試玩時間紀錄。 |
| 敵方行動可理解 | PASS（既有工程功能） | P1v 的 intent、路徑與原因未變；26 項瀏覽器回歸。真人理解度未驗證。 |
| 玩家可勝或敗 | PASS | P1v 回歸涵蓋勝利及失敗。 |
| 兩種戰術選擇產生不同結果 | PASS（最低要求） | 原 P0 重新站位勝、不移動敗；A 仍屬 THIN。 |
| 重試並改變策略 | PASS | 原 P1v Retry 測試持續通過的執行紀錄。 |
| 無重複結算、卡住回合、非法移動或動畫中斷 | PASS（已測範圍） | P1v 26 項回歸，加上 P1v2 動態腳點排序測試。 |
| 1280×720、1920×1080 與鍵盤 | PASS（自動化） | 兩種尺寸、100 次格子指標測試、Space／Esc、200% 文字版面。 |
| 自動化與真人證據分開 | PASS | VERIFICATION.md 明確標示 HUMAN_PENDING，沒有以代理測試代替真人驗收。 |

### D. Project rules

| 項目 | 判定 | 證據 |
|---|---|---|
| SRD 5.2.1／CC-BY／WotC IP／規則改編 | N/A | 沒有新規則、官方文字或第三方素材。 |
| AGENTS／Owner 授權範圍 | PASS | 684d189..8f8a42b 僅更動 P1v2 顯示、CSS、測試與證據；沒有實作 P2、修改劇情或新增套件。 |

## Reviewer 最終判定

- P1v2 工程驗收：PASS
- 角色點擊與標籤隔離：PASS
- 720p 人物視覺辨識：HUMAN_PENDING
- 完整遊戲體驗：尚未達標

建議 P1v2 工程結案，繼續 P2。 這一輪最有價值的成果是將「人物顯示」與「格子操作」可靠分離；後續應把主要精力轉向敵方反應、戰術選擇與玩家能否理解戰場，而不是反覆微調已通過自動化測試的點擊區域。
