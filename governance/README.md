# AI Governance 導入

本次為首次 submodule 導入，不是 F7 更新。來源 `Gavin0099/ai-governance-framework`，固定 `e8e67796894cd562ef0bce217bfad0fac211a44d`。使用者後續已授權完成段落後 commit / push；未授權 PR / 部署 / Actions。

## 已可用

- root contract：game-ui-prototype / low（使用者授權代理填寫）。
- 官方受保護 baseline、專案 AGENTS 規則、memory 01–04、版本宣告與本地 Git hooks。
- 原始企劃保護 DomainValidator，可由 CLI 或 framework 載入。
- `python scripts/verify_governance_ui.py`：以 repo 為 runtime root，明確指定 ui-prototype/PLAN.md；直接讀取根目錄的 memory、規則與 .governance，無需符號連結權限。檢查 domain contract、pre-task、session-start、validator preflight。這是手動測試，未接上 Codex lifecycle。
- `PYTHONPATH=ai-governance-framework python3 -m governance_tools.governance_drift_checker --repo . --format human`。
- `PYTHONPATH=ai-governance-framework python3 -m governance_tools.hook_install_validator --repo . --framework-root ai-governance-framework --format human`。

## 原生 lifecycle 接線

四個原生事件的安裝、信任與驗收見 [CODEX-LIFECYCLE.md](CODEX-LIFECYCLE.md)。執行 `python scripts/install_codex_governance.py` 產生本機設定，再以 `python scripts/record_governance_checks.py` 執行隔離測試、scope、TypeScript 與 Vite 建置。Stop 檢查兩個領域 validator；`hard_stop_rules` 明確要求違規停止，避免框架預設只發警告。

接線程式與 replay 不等於平台信任或原生回呼。只有同一自然 session 的四事件及有效 writer receipt 齊備後才能報完整導入；本輪狀態見 [ADOPTION-STATUS.md](ADOPTION-STATUS.md)。

## 完整驗收剩餘界線

上游 root readiness 與 pre-commit 固定讀 root PLAN。使用者已於本輪明確允許只加治理表頭，`proposed-root-plan-header.patch` 已依授權套用；故事正文與 S3／S4 狀態不變，scope validator 只允許這段確切 metadata。

版本帳本與 submodule checkout SHA 相符；實際提交狀態與導入程度以 ADOPTION-STATUS.md 與 Git 歷史為準。真實 commit / push hook 已在 a97c8a8 正常交付中執行且通過。Copilot hooks 不適用本次 Codex 工作，沒有宣稱其安裝或驗證。

診斷原件在 artifacts。UI runtime PASS 不代表 root readiness PASS，也不表示平台自動執行、正式規則完整或全框架測試通過。

## Windows 工作副本設定

框架與 hooks 不會隨一般 clone 自動就緒。從 repo 根目錄以 PowerShell 執行：

```powershell
git submodule update --init -- ai-governance-framework
$env:PYTHONPATH = (Resolve-Path ai-governance-framework).Path
$env:PYTHONUTF8 = '1'
python -m governance_tools.hook_installer --repo . --framework-root ai-governance-framework --hooks-only
python -m governance_tools.external_repo_readiness --repo . --framework-root ai-governance-framework --format human
python scripts/verify_governance_ui.py
python scripts/validate_ui_scope.py
```

使用已安裝的 Python 3，不依賴 WindowsApps 的 python3 別名。Git hooks 由 Git for Windows 的 Bash 執行，無需 WSL。此設定只安裝本 repo 的 Git hooks，不新增 Copilot、Actions 或 Codex 平台 lifecycle。新工作副本需重跑設定；原有歷史證據不能代替本機驗證。
