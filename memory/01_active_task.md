# Active task

2026-10-20。

## 使用者陳述與既有授權

本次最新指示：「把剩下的接線與驗收補齊，做到完整導入，完成後幫我 push」。既有授權包含 UI-01..05、代填 domain/risk、完成段落後正常 commit/push，以及根 PLAN 的確切治理表頭；PR、部署、付費、Actions 與 S4 未授權。本輪優先完成治理接線，不擴寫 UI 或故事。

## 本輪代理觀察

Windows 新工作副本缺少框架 checkout 與本機 hooks，已初始化固定 submodule 並用官方 installer 安裝 hooks-only。原 UI smoke 因 symlink 以文字檔簽出而失敗；Windows 建立連結權限不足，改用 repo runtime root 與 UI 計畫，移除兩個不再需要的連結。pre-task、session-start、validator preflight、readiness 17/17、drift 與 hook 安裝檢查通過。記憶與規則維持根目錄單一來源。

## 驗收界線

先前環境的 UI 與真實 Git 交付證據已存在，不能代替 Windows 本機驗證。本輪新增四事件轉接與隔離驗收；設定生成、replay、Codex 信任、真實回呼及 canonical writer receipt 分開驗收，結果見 governance/ADOPTION-STATUS.md。使用者尚未要求結束聊天，不自行觸發本 session 的 canonical closeout。未取得自然 SessionEnd 證據前，不宣稱 full adoption。

## 最新補線觀察

已建立 Windows isolated Python 四事件接線；hard_stop_rules 已補齊，兩個 validator 實際執行。消費端 smoke 的 pre-task/session-start/post-task 均 true。PowerShell 雙層啟動超過官方 SessionEnd 三秒限制，已改直接固定 Python，收尾 replay 約2.86秒。隔離測試使用工作區內 Git 副本，replay 不寫真實日記。手動 smoke runtime 保留於 scratch/governance-before-native-20261020T1109；使用者信任與自然回呼仍待確認。最新完整測試結果以 artifacts/governance-native-acceptance.json 為準。
