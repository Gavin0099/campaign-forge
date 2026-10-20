# Architecture

- 原始企劃在 repo root / docs；本次保持內容不變。
- UI 在 ui-prototype，資料集中 src/data.ts，視覺 public/art，React 本次頁面記憶狀態。
- AI Governance 以 repo 內 submodule 固定 e8e67796894cd562ef0bce217bfad0fac211a44d。
- AGENTS.base.md 與 common/core.md 原樣複製自該版本，Apache 2.0 授權只適用相應框架檔案，見 licenses。專案故事與新美術沒有因此被授予開源授權。
- 本地 Git hooks 使用 framework 既有 installer；不建立 GitHub Actions 或外部服務。
- 未設定 Codex 平台 lifecycle 自動呼叫，手動 runtime smoke 僅驗證函式可執行。
