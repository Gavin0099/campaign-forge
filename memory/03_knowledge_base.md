# Decisions and observations

- 2026-10-20：UI 計畫放 ui-prototype/PLAN.md，保護原始故事 PLAN。基線 plan_path 指向 UI 計畫。
- 人物概念圖和戰場小人分開生成；CSS atlas 呈現，沒有聲稱已有動作動畫。
- 立繪需保留 3:8 每人欄位比例；不能拉伸填滿人物面板。
- 治理預設 adoption 會新增 GitHub Actions，與使用者限制衝突，採手動 submodule 導入及官方 baseline helper。
- 部分上游 readiness/smoke 仍硬編碼根 PLAN；使用 explicit-plan quickstart 驗證 UI 路徑，另保留原始診斷，禁止隱藏失敗。
- 2026-10-20 Windows 觀察：core.symlinks=false 將 UI 的 memory/.governance 連結簽出為文字檔；無建立符號連結權限時 session-start 失敗。UI 治理驗證使用 repo runtime root 與 explicit UI plan，直接共享 canonical memory、規則與 baseline；不需要提權、重複記憶或變更安全設定。
- 2026-10-20 原生接線觀察：固定 framework 的 Codex installer 使用 Stop 收尾，且 context builder 的 legacy writer 不相容於原生 root-bound envelope；消費端須分離 Stop/SessionEnd 並保留既有身分。validator 的 rule_ids 必須與 game-ui-prototype 相交，只有可載入不代表有執行。官方 SessionEnd 上限三秒，候選準備須提前；正式 writer 仍僅能在真正 session end 執行。
- 2026-10-20 驗收觀察：領域 violations 預設僅為 warning，須在 contract 宣告 hard_stop_rules。canonical entry exit0 也不等於內容有效或寫入成功，應核對 closeout_status、memory_write_claim_verified 與實際 writer status。Windows 使用 isolated Python 直接 bootstrap，避免 PowerShell 啟動耗盡收尾時間；Node 僅在建置前驗證。
