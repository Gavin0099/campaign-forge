# AI Governance 導入

本次為首次 submodule 導入，不是 F7 更新。來源 `Gavin0099/ai-governance-framework`，固定 `e8e67796894cd562ef0bce217bfad0fac211a44d`。使用者後續已授權完成段落後 commit / push；未授權 PR / 部署 / Actions。

## 已可用

- root contract：game-ui-prototype / low（使用者授權代理填寫）。
- 官方受保護 baseline、專案 AGENTS 規則、memory 01–04、版本宣告與本地 Git hooks。
- 原始企劃保護 DomainValidator，可由 CLI 或 framework 載入。
- `python3 scripts/verify_governance_ui.py`：以 ui-prototype 為 runtime root；其 memory 與 .governance symlink 指回 repo，避免重複真相來源。檢查 domain contract、pre-task、session-start、validator preflight。這是手動測試，未接上 Codex lifecycle。
- `PYTHONPATH=ai-governance-framework python3 -m governance_tools.governance_drift_checker --repo . --format human`。
- `PYTHONPATH=ai-governance-framework python3 -m governance_tools.hook_install_validator --repo . --framework-root ai-governance-framework --format human`。

## 完整驗收剩餘界線

上游 root readiness 與 pre-commit 固定讀 root PLAN。使用者已於本輪明確允許只加治理表頭，`proposed-root-plan-header.patch` 已依授權套用；故事正文與 S3／S4 狀態不變，scope validator 只允許這段確切 metadata。

版本帳本與 submodule checkout SHA 相符；實際提交狀態與導入程度以 ADOPTION-STATUS.md 與 Git 歷史為準。真實 commit / push hook 已在 a97c8a8 正常交付中執行且通過。Copilot hooks 不適用本次 Codex 工作，沒有宣稱其安裝或驗證。

診斷原件在 artifacts。UI runtime PASS 不代表 root readiness PASS，也不表示平台自動執行、正式規則完整或全框架測試通過。
