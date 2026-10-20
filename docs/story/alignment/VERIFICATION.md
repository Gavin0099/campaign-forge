# 敘事與產品對齊驗收

本輪由 story@4f5e447 開始，main 基準505fca7。具體提交與遠端交付結果由 Git 核對；此文件不預告尚未發生的 push。

主實作 `e8311673399119131a61cd9b9c81aa8bec7720e6` 已於2026-10-21 01:14:04 +08:00核對正常FF推送、遠端相符，main仍505fca7且兩工作區乾淨。[交付觀察](evidence/delivery.json) 綁定實作commit、8份證據hash與明確未宣稱事項；[實際push輸出](evidence/implementation-push.txt) 是共用Git hooks的framework smoke，不是平台自然回呼。[原稿信任分布](evidence/baseline-trust.json) 另保留實際結果。此後交付補件亦只走正常故事分支推送，最終head由最後refs核對。

## 結果分界

| 面向 | 判定 | 意義 |
| --- | --- | --- |
| 工程／劇情狀態 | PASS（詳下方實際證據） | 編譯、可達、列明的狀態不變條件、拒絕錯誤及瀏覽器流程；不是完整戰棋規則 |
| 缺稿三項 | SOURCE_NOT_FOUND | 貝恩、燈號簿、洩潮地未找到原稿，沒有編造修復，不算內容驗收通過 |
| 敘事品質 | 待人工審查 | 模型反例判讀已完成，真人試讀0；K1平衡、L07公平與情感投入尚未通過 |
| 產品／美術規格 | 候選可審閱；商業美術待人工 | Creative Bible 與 L03 規格完成；未替換 main UI、未製作新正式美術 |
| 治理 | 維持既有界線，平台自然回呼待驗 | 不把 Git hooks、模型測試、正常 push 當成自然 Codex 事件／SessionEnd |

## 實際命令與證據

本機使用 Node24.13.0 的已核對絕對執行檔；可攜命令省略該路徑，環境設定見 [README](../../../story-playtest/README.md)。

| 命令／活動 | exit | 證據與限制 |
| --- | --- | --- |
| inkjs2.3.2 compiler -o scratch/baseline.json docs/story/script/main.ink（4f5e447 原稿）＋原 walk.js | 0 | 55,296終端組合，原有檢查0錯；原驗證器錯誤時未設定exit，不能用於負例驗收 |
| 原稿信任分布重走 | 0 | trust2=23,040、3=25,344、4=6,912，符合門檻32,256（58.33%），非玩家機率 |
| inkjs compiler -o scratch/current.json docs/story/script/main.ink | 0 | 本輪編譯零警告／錯誤 |
| node docs/story/script/check/walk.js scratch/current.json --out=docs/story/alignment/evidence/walk.json | 0 | [walk.json](evidence/walk.json)：55,296終端、37,791選項邊界、10種主分支組合；核心拒絕全路徑、公開作證32,256 |
| node story-playtest/tools/build.cjs | 0 | [build.json](evidence/build.json)：同源編譯、完整TS檢查、來源與輸出hash；依賴在ignored scratch |
| node story-playtest/tests/negative.cjs | 0（各負例CLI必須為1） | [negative.json](evidence/negative.json)：14種刻意破壞；驗證真實入口回傳1且對應正確不變條件，含死亡與撤離人數越界 |
| node story-playtest/tests/consistency.cjs | 0 | [consistency.json](evidence/consistency.json)：25項，旗標／關卡／出場／函式階段與名鑰／本地連結；瀏覽器與走訪執行的編譯內容一致（CLI可多UTF-8 BOM） |
| node story-playtest/tests/browser.cjs | 0 | [browser.json](evidence/browser.json)：32項，實際按鈕路線、匯出、回退、兩尺寸、20組重播、高低信任、放大文字與鍵盤、舊版本拒絕、運行畫面文字對比 |
| 官方 memory_workflow --repo 隔離工作區 --check --run-guard --format json | 0 | [memory-workflow.json](evidence/memory-workflow.json)：blockers空、B0=0、completion_claim_allowed=true；missing_canonical_memory為advisory，任務交付不是SessionEnd，不因警告編造daily |

截圖均來自運行頁面：[720p初始](evidence/reading-1280.png)、[1080p初始](evidence/reading-1920.png)、[720p章末](evidence/ending-1280.png)、[1080p章末](evidence/ending-1920.png)、[放大文字720p](evidence/reading-large-1280.png)、[窄螢幕200%](evidence/reading-large-390.png)。檢視過實際排版；不能當 Steam 戰鬥美術通過。

## 範圍、原件與治理

原 A／B／C、README、SLICES、STORY-GATE、整個 ui-prototype／framework／治理程式保持既有版本。根 PLAN／AGENTS 與決策、記憶只增加本輪授權與里程碑；原故事企劃本文保留。G004／G005仍待決，沒有新增L08起劇本、技能數值、部署、Actions、PR或故事LICENSE。

共用既有 Git hooks；linked worktree 沒有複製 main 的原生 Codex root 綁定，也沒有把隔離工作區偽裝為平台已信任根。Git pre-push 的 framework smoke 與本輪故事驗證分開記錄；真正自然平台回呼仍待證據。任務完成／push不是SessionEnd，不為此觸發收尾或自動寫新daily。

原 `scripts/validate_ui_scope.py` 固定以最初13份故事檔案與僅允許PLAN表頭為契約，不能代表本輪新增劇情修改授權；本輪未弱化或改寫該驗證器，以故事基準4f5e447的保護路徑diff核對範圍。UI及框架程式完全未變更，沒有重跑無關的VD3全套來充作故事驗收。官方記憶工具透過本機唯讀adapter核對既有Python／Git位元組、framework來源hash，以及本輪worktree／共用git目錄後執行，不使用main原生hook的root綁定來宣稱本worktree已受平台回呼驗證。

驗證期間有一次瀏覽器焦點斷言在 requestAnimationFrame 之前讀到 BUTTON；補上等候實際H2取得焦點後重跑31項全過。另出場檢查起初把L05初見尚未收留薩溫當成缺席復現，修正為允許既有初見／拒絕告別，後續才檢查缺席發言。這兩項是測試時序／前置條件修正，沒有修改劇情來迎合測試。

本輪投入依 [TIME-LEDGER](TIME-LEDGER.md) 的實際時窗，重疊只算一次，12小時並未用滿。剩餘劇情風險與Owner問題見 [NARRATIVE-REVIEW](NARRATIVE-REVIEW.md)。
