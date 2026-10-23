# Decisions and observations

- 2026-10-23 P1v5觀察：同一單位的落腳塵土與arrival動畫若共用相鄰React key，timeout移除後可能殘留舊SVG；以dust-序號與角色動畫序號分開，瀏覽器斷言短效DOM歸零。表現讀取既有progress／blocked事件，效果timer不持有busy；沒有hit／shove事件就不顯示假傷害或改格位。
- 2026-10-23 P1v6：逐事件回饋必須與相同 path-step clock 共用邊界，不能在 finish 才一次補播。最後一步落地可與原子提交同一邊界，不為落塵增加 busy。反事實查詢要先重建該 intent 前的位置，將被查詢敵人排首避免較早敵人再移一次；只有移除相鄰同伴確實打開路徑、且接觸者唯一才出火花。
- 2026-10-23 P1v6：Chrome 對 nested SVG viewport 本身做 drop-shadow，會露出原 PNG 圖集中裁切外的幀；顯式 overflow:hidden 並改為在 viewport 內 image 做濾鏡。DOM 幀數與建置不會發現漏圖，必須看實機截圖；180ms 效果時序用 MutationObserver 留存，截圖另行重播，避免截圖編碼錯過下一事件。
- 2026-10-20：UI 計畫放 ui-prototype/PLAN.md，保護原始故事 PLAN。基線 plan_path 指向 UI 計畫。
- 人物概念圖和戰場小人分開生成；CSS atlas 呈現，沒有聲稱已有動作動畫。
- 早期v1立繪需保留3:8欄位比例；v2已改為透明四等欄2:1圖集，按新原檔比例呈現，不能拉伸填滿人物面板。
- 治理預設 adoption 會新增 GitHub Actions，與使用者限制衝突，採手動 submodule 導入及官方 baseline helper。
- 部分上游 readiness/smoke 仍硬編碼根 PLAN；使用 explicit-plan quickstart 驗證 UI 路徑，另保留原始診斷，禁止隱藏失敗。
- 2026-10-20 Windows 觀察：core.symlinks=false 將 UI 的 memory/.governance 連結簽出為文字檔；無建立符號連結權限時 session-start 失敗。UI 治理驗證使用 repo runtime root 與 explicit UI plan，直接共享 canonical memory、規則與 baseline；不需要提權、重複記憶或變更安全設定。
- 2026-10-20 原生接線觀察：固定 framework 的 Codex installer 使用 Stop 收尾，且 context builder 的 legacy writer 不相容於原生 root-bound envelope；消費端須分離 Stop/SessionEnd 並保留既有身分。validator 的 rule_ids 必須與 game-ui-prototype 相交，只有可載入不代表有執行。官方 SessionEnd 上限三秒，候選準備須提前；正式 writer 仍僅能在真正 session end 執行。
- 2026-10-20 驗收觀察：領域 violations 預設僅為 warning，須在 contract 宣告 hard_stop_rules。canonical entry exit0 也不等於內容有效或寫入成功，應核對 closeout_status、memory_write_claim_verified 與實際 writer status。Windows 使用 isolated Python 直接 bootstrap，避免 PowerShell 啟動耗盡收尾時間；Node 僅在建置前驗證。
- 2026-10-20 Visual Sprint架構：mapRows同時生成地表與互動polygon，共用斜俯視project；角色sprite保持直立。生成近景只負責對話／外圍氣氛，不能當作可走格資料。原地形、站位、距離與固定效果不變。
- v2裁切根因：SVG的meet留白區仍可露出原圖其他欄，必須明確clipPath到自己的圖集欄。先重排武器跨欄，再驗證分界alpha，不能只改CSS背景位置掩蓋原圖問題。
- 720p固定按鈕曾覆蓋預覽；回合／護送操作移至戰場下方，窄畫面預覽壓成清楚層級，確認／撤銷與預覽邊界納入實際瀏覽器幾何檢查。Esc關閉確認視窗後恢復觸發鍵焦點。
- 瀏覽器驗收以真實Tab／Enter／Space導航和React流程為證據；輸入及截圖SHA-256防止舊圖冒充目前畫面。它不驗證商業美術品質；生成與程式交錯時應從開始使用分片計時器，本輪只能提供牆鐘及回溯活動窗。
