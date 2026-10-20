# Decisions and observations

- 2026-10-20：UI 計畫放 ui-prototype/PLAN.md，保護原始故事 PLAN。基線 plan_path 指向 UI 計畫。
- 人物概念圖和戰場小人分開生成；CSS atlas 呈現，沒有聲稱已有動作動畫。
- 立繪需保留 3:8 每人欄位比例；不能拉伸填滿人物面板。
- 治理預設 adoption 會新增 GitHub Actions，與使用者限制衝突，採手動 submodule 導入及官方 baseline helper。
- 部分上游 readiness/smoke 仍硬編碼根 PLAN；使用 explicit-plan quickstart 驗證 UI 路徑，另保留原始診斷，禁止隱藏失敗。
- 2026-10-20 Windows 觀察：core.symlinks=false 將 UI 的 memory/.governance 連結簽出為文字檔；無建立符號連結權限時 session-start 失敗。UI 治理驗證使用 repo runtime root 與 explicit UI plan，直接共享 canonical memory、規則與 baseline；不需要提權、重複記憶或變更安全設定。
