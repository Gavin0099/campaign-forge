# Active task

2026-10-20。

## 使用者陳述與既有授權

本次指示：「先幫我導入AI governance」。既有授權包含 UI-01..05、代填 domain/risk、完成段落後正常 commit/push，以及根 PLAN 的確切治理表頭；PR、部署、付費、Actions 與 S4 未授權。本輪優先完成治理導入，不擴寫 UI 或故事。

## 本輪代理觀察

Windows 新工作副本缺少框架 checkout 與本機 hooks，已初始化固定 submodule 並用官方 installer 安裝 hooks-only。原 UI smoke 因 symlink 以文字檔簽出而失敗；Windows 建立連結權限不足，改用 repo runtime root 與 UI 計畫，移除兩個不再需要的連結。pre-task、session-start、validator preflight、readiness 17/17、drift 與 hook 安裝檢查通過。記憶與規則維持根目錄單一來源。

## 驗收界線

先前環境的 UI 與真實 Git 交付證據已存在，不能代替 Windows 本機驗證。本機 Git 交付依實際終端結果及遠端 HEAD 核對；未宣稱 Codex lifecycle 自動接線、最新框架更新或 full adoption。詳細證據見 governance/ADOPTION-STATUS.md。任務完成不代表 session end，不觸發 canonical daily closeout。
