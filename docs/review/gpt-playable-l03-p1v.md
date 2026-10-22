# GPT web review — playable-l03 P1v (first playable screen)

- Reviewer: ChatGPT web, campaign-forge project
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad9a198-9114-83ee-b461-0937f1b8eb71
- Reviewed: codex/playable-l03-research, 13a6e17..684d189 (implementation ece8e50, handoff 684d189)
- Date: 2026-10-22 (Asia/Taipei)
- Transcription: Grok Bot copied this from the page, with the tables rebuilt as pipe rows and no wording changed. GPT's first reply was cut off in section 7, so a continuation was requested. That continuation redid section 7 in full, and section 7 below uses it. The first reply had game-feel as "PASS（有限）"; the continuation changed it to "FAIL（完整體驗）".

---

## 1. 結論：PASS（工程驗收），needs Owner（可玩性與視覺驗收）

P1v 已達到第一個可親手操作的 L03 戰鬥畫面之主要工程驗收要求，建議交給 Gavin 實際試玩；但角色重疊及 A 仍為 THIN，尚不能視為完整遊戲體驗通過。

| 驗收項目 | 判定 | 證據 |
|---|---|---|
| 獨立入口與既有畫面隔離 | PASS | main.tsx:61,427；新增 PlayableL03.tsx |
| 11×9 地圖、5 名角色、絞盤與資訊列 | PASS | PlayableL03.tsx:120–175；瀏覽器測試檢查 99 格、5 人 |
| 合法移動、等待、結束回合、鍵盤操作 | PASS | PlayableL03.tsx:70–118,224–235；測試涵蓋移動與輸入 |
| 敵方意圖與移動動畫 | PASS | PlayableL03.tsx:73–75,88–106,173–221 |
| 動畫與跳過動畫結果一致 | PASS | 測試 playable-l03-p1v-browser.mjs:154–164,180–203 |
| 勝敗、Retry 與狀態清除 | PASS | PlayableL03.tsx:50–59,82–86；測試 66–75 |
| 1280×720、1920×1080 截圖 | PASS（有紀錄） | VERIFICATION.md 及兩組實機截圖檔 |
| 3–5 分鐘真人試玩 | HUMAN_PENDING | 尚無真人試玩與趣味性評估 |

Reviewer 沒有重新執行 Playwright 或 build；測試通過是根據已提交的測試程式與執行紀錄。

## 2. 問題（P0–P2）

| 優先級 | file:line | 問題與證據 | 建議 |
|---|---|---|---|
| P0 | — | 未發現足以阻擋整個 P1v 工程交付的已確認 P0 缺陷。 | 保留現有純規則測試與回歸保護。 |
| P1 | PlayableL03.tsx:192–208 | 單幀角色素材高度較大，鄰近格角色可能互相遮擋；這也會遮住部分名稱及點擊區域。Handoff 已明確記錄此限制。 | 優先改善角色深度排序、縮放與名稱標籤位置，並新增重疊情境的瀏覽器驗收。 |
| P1 | PlayableL03.tsx:73–75,173–221 | 敵人意圖取自 resolve() 的結果，資料來源正確；但畫面只顯示本回合的路徑／終點與簡短原因，尚未證明玩家能清楚理解下一回合威脅。 | P2 應延續同一套 intent 契約，讓每種行為都有明確原因與可核對的實際行動。 |
| P2 | PlayableL03.tsx:34–35,108–118,233 | 等待狀態保存在 UI 的 waited，不是規則狀態。 | 若未來需要存檔、回放或重連，再決定是否把等待納入命令模型；本輪不必擴大範圍。 |
| P2 | PlayableL03.tsx:20–27,453–461（AnimatedActor.tsx） | 現有 L03 角色使用單幀圖，只加上移動與輕微上下浮動，並非真正的關節動畫。 | 保持如實描述，不要將目前移動演出視為完整角色動畫。 |

四個關鍵技術問題：
- 規則與畫面是否分離？是。元件呼叫 command()、resolve() 取得規則結果，畫面負責選取、呈現與動畫；沒有把 React 或動畫時鐘引入規則模組。
- 動畫是否影響結算？沒有看到。先產生 Result，動畫播放完或跳過後才採用同一個結果；busyRef 與 pending 避免重複結算。
- Retry 是否清乾淨？測試檢查了初始規則狀態、選取、等待、合法移動提示、結果對話框、動畫與跳過設定，覆蓋充分。
- 敵人意圖是否與實際行動一致？兩者都來自同一份 resolve() 結果，動畫也播放該結果中的 move events。尚待驗證的是玩家能否理解意圖。

## 3. 可玩性與 UI/UX

P1v 的重要進展，是玩家終於可以親自選角、移動、等待、結束回合，看到敵人接近絞盤，再透過勝敗與 Retry 重試。資訊層級有合理基礎：頂部顯示回合及絞盤干擾；戰場顯示角色、地形、絞盤與移動範圍；側欄顯示敵人意圖及原因；底部提供等待、結束回合與操作提示。

不過，角色重疊不能只當成美術小瑕疵。如果玩家看不清角色、標籤或可點擊區域，就會直接影響戰術判斷與操作信心。建議在下一輪先改善角色層次與標籤可讀性，再考慮更複雜的動畫。不要在玩家還不能可靠辨識單位時，就增加更多敵方行為。P1v 啟用的 A 仍是六回合 THIN 實驗，畫面目前主要驗證操作與回饋，尚未驗證關卡是否有趣。

## 4. 下一段 P2：兩種敵方回應

建議先等 P0d 的規則驗證結果，再正式實作 P2 的敵人反應。P1v 本身已可玩，不需要為了等待 P0d 而回頭重做畫面。P2 應維持窄範圍，只實作兩種行為：目標干擾（依既有目標與可達性，對絞盤造成壓力）與追弱點（根據明確、可測試的條件，選擇一名可追擊的目標）。每種行為都應回傳 intent + reason + action，並驗證預告與實際行動一致。P0d 結果出來前，可以先準備介面契約與測試案例，但不要先決定最終 AI 優先序、勝敗條件或加入傷害／HP。

## 5. 沒檢查到的部分

- 沒有獨立執行 Playwright、build 或 governance 命令。
- 沒有直接逐張檢視 PNG 像素；核對了截圖清單、尺寸／雜湊驗證紀錄及程式中的版面設定。
- 沒有真人試玩。
- 沒有驗證螢幕閱讀器、手把、長時間效能或完整無障礙標準。

## 6. 給 Gavin 的決策

- P1v 工程交付是否接受？建議接受，開始親自試玩；保留角色重疊為待修問題。
- 是否先修視覺重疊？建議先改善角色層次、標籤與點擊區域，不擴大到全員骨架動畫。
- P2 是否等 P0d？建議等 P0d 的規則結論後，再正式實作兩種敵方回應；目前可先做介面契約與測試規格。

## 7. 資源檢核（RESOURCE-CHECKLIST A–D）

**A. Skills**

| 項目 | 判定 | 證據與說明 |
|---|---|---|
| prototype-fast | PASS | PlayableL03.tsx 建立獨立可玩畫面，沿用原有規則與素材，沒有重建戰鬥系統。 |
| level-design | PASS（限定範圍） | 11×9 地圖、絞盤 (2,1)、合法移動及開閘勝敗可驗證；封閘路線仍未實作。 |
| game-ai | PASS（工程） | PlayableL03.tsx:73–75 的敵方預告來自 resolve()，與實際事件使用相同規則。 |
| game-ui-ux | FAIL（完整體驗） | PlayableL03.tsx:192–208 存在角色及標籤互相遮擋；基本選取、移動範圍、提示、鍵盤功能則有自動化測試證據。 |
| game-feel | FAIL（完整體驗） | AnimatedActor.tsx:453–461 只讓單幀素材上下浮動；有逐格移動、跳過與 Reduced Motion，但尚無充分的角色動態與真人節奏驗收。 |

game-ui-ux 與 game-feel 的最低 P1v 工程要求已有實作，不等於完整使用體驗與動畫品質通過。

**B. Reference repos**

| 項目 | 判定 | 證據與說明 |
|---|---|---|
| Grid-Tactics：規則與顯示分離 | PASS | PlayableL03.tsx:77–106 先取得規則 Result，動畫僅播放事件，完成或跳過後採用同一結果。未複製外部程式碼。 |
| HopeMetal：授權與素材檢查 | PASS | 沿用專案既有 L03 素材，沒有從參考 Repo 引進素材；既有授權盤點仍有效。 |
| 不新增引擎與依賴 | PASS | 13a6e17..684d189 沒有 package／lockfile 變更。 |

**C. Playable acceptance bar**

| 項目 | 判定 | 證據與說明 |
|---|---|---|
| 玩家可獨自完成 3–5 分鐘戰鬥 | FAIL（HUMAN_PENDING） | 有完整六回合自動化勝敗流程，但尚無真人試玩與實際耗時紀錄。 |
| 敵人行為可理解 | PASS（工程） | PlayableL03.tsx:213–222 顯示敵方意圖、目標及原因；真人理解度尚未驗證。 |
| 玩家可以獲勝或失敗 | PASS | playable-l03-p1v-browser.mjs:154–164 覆蓋正常與跳過動畫的完整勝敗流程。 |
| 兩種戰術選擇有不同結果 | PASS（最低要求） | 原 P0 守點策略勝利，不移動策略失敗；A 的戰術深度仍為 THIN。 |
| 可重試並改變策略 | PASS | playable-l03-p1v-browser.mjs:66–75 驗證 Retry 清除規則及 UI 狀態。 |
| 沒有重複結算、卡住回合、非法移動或動畫中斷問題 | PASS（已測範圍） | playable-l03-p1v-browser.mjs:180–209 涵蓋跳過、重複輸入、Reduced Motion 與離開畫面。 |
| 1280×720、1920×1080 及鍵盤操作 | PASS（自動化） | 測試涵蓋兩種尺寸、Space／方向鍵／Esc／Enter、200% 文字與 390px 備援版面。 |
| 自動化與真人測試分開記錄 | PASS | VERIFICATION.md 明確將瀏覽器測試與 HUMAN_PENDING 分開。 |

**D. Project rules**

| 項目 | 判定 | 證據與說明 |
|---|---|---|
| SRD 5.2.1／CC-BY／WotC IP 與規則改編契約 | PASS（未新增改編） | 只使用已存在的暫定規則與原有素材。 |
| AGENTS／Owner 授權範圍 | PASS | 變更集中在新可玩畫面、共用動畫元件的相容擴充、測試與證據；沒有修改正式故事、啟動 P0d／P2 或改變原規則預設。 |

**最終 Reviewer 判定**

| 驗收層級 | 結果 |
|---|---|
| P1v 功能與架構 | PASS |
| 自動化勝敗、動畫與 Retry | PASS |
| UI 可讀性與角色遮擋 | Needs fixes |
| 戰術深度 | THIN |
| 真人可玩性驗收 | HUMAN_PENDING |
| 完整遊戲品質 | 尚未達標 |

建議接受 P1v 作為第一個可操作的工程里程碑，而不是完整關卡完成。下一步最重要的是先讓 Gavin 實際操作這場戰鬥，確認能否在沒有開發者提示的情況下，理解移動、敵方威脅及勝敗原因。P0d 與 P2 應維持獨立：P0d 確認敵方反制機制是否改善戰術深度，P2 再將通過驗證的規則整合進可玩畫面。
