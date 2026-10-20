# AI Governance 導入程度 — 2026-10-20

## 最新使用者回覆：修正版已信任

使用者已確認0fc109f修正版完成信任與重新載入，因此下方「修正版需要重新檢閱信任」已是歷史步驟，不能再當作待辦要求。此次VD2沒有修改bridge或hook定義。代理仍未取得平台原生回呼收據；信任完成與完整導入驗收分開，沒有以手動測試或正常push冒充自然SessionEnd。

## 使用者完成平台信任後的核對

使用者已確認「已完成信任與重新載入」，並確認 Hooks 檢閱頁的四個事件皆為已信任／啟用、沒有錯誤。這是使用者提供的平台狀態，取代下方歷史段落中「尚待使用者信任」的描述。

代理初次核對本 repo：四事件設定存在、Python／Git／Node 及 bridge／framework 來源均符合本機綁定的長度與 SHA-256。然而 `artifacts/runtime/codex/` 尚無原生事件收據，`native_status` 仍為 `complete=false`、`observed_native_events=[]`。因此前一版本的信任步驟已由使用者確認完成，原生執行仍待平台證據；目前不能宣稱完整導入，也不能將缺少收據直接判為使用者未信任或 bridge 執行失敗。

這次重驗另外發現 SessionEnd 耗時3.390秒，超出平台三秒上限；原始失敗收據保留於 `artifacts/governance-native-timeout-regression.json`。量測顯示收尾共啟動53次子程序，其中19次為同一 consumer root 的重複 Git 查詢。本輪將三個 Git 身分查詢合併，讓短生命週期程序內的 canonical root helper 重用最初已驗證的 Git 身分，每次仍檢查絕對路徑、root／.git 是否被重導，以及 envelope 的 root 是否完全相符；其餘 canonical、ownership、memory guard、writer 均維持原流程。另將 pre/post-task import 移至各自事件分支，未更動上游框架。

修正後13/13隔離測試通過；三個全新 session 的 SessionEnd 原樣命令分別為2.360、2.281、2.281秒，均低於三秒。新增偽造 envelope 借用另一個 repo root 的拒絕案例；成功耗時仍只代表本機 replay，尚無平台 timeout 或原生 writer 的成功證據。此次 bridge 修正已重新產生本機 hook 定義；Codex 依定義雜湊信任，**修正版需要重新檢閱信任**，不能沿用使用者對前一版的確認。這是修正帶來的新要求，沒有改動全域信任資料。

下一個診斷點是同一 repo 的普通文字訊息是否觸發 UserPromptSubmit，以及 Hooks 介面的實際執行紀錄。若仍無紀錄，須核對平台是否載入此專案設定；不反覆安裝、修改信任資料或以手動 replay 偽裝回呼。自然 SessionEnd 與 canonical writer 仍須在真正結束聊天後核對，本次沒有自行封存聊天。原始程式／隔離驗收的界線保持不變。

## 最新補線里程碑

使用者本輪要求補齊剩餘接線與驗收並 push。四個 Codex 原生事件已實作，使用 repo 本機產生、固定 Python／Git 與來源雜湊的命令；沒有改動全域信任或開啟 Actions。SessionStart 建立及保留原生身分、UserPromptSubmit 作前置檢查、Stop 驗證兩個領域 validator，SessionEnd 才執行 canonical closeout。詳見 [CODEX-LIFECYCLE.md](CODEX-LIFECYCLE.md)。

驗收證據為 `artifacts/governance-native-acceptance.json`（隔離命令測試、scope、TypeScript、Vite 的真實 exit code 與輸出），以及 `artifacts/governance-native-external-smoke.json`（pre_task、session_start、post_task 均 true，兩個領域 validator 實際執行）。後置 fixture 為明確標記的 synthetic、無額外檢查宣稱的最小合約案例；不以手填的測試成功欄位充作執行證據。

最新隔離測試 **13/13 通過**，SessionEnd 三次原樣命令耗時見上方修正紀錄；scope、TypeScript 與 Vite exit code 均0。先前 readiness 17/17、drift ok、本機 Git hook 安裝 valid；其 JSON 分別保留在 `artifacts/governance-native-readiness.json`、`governance-native-drift.json`、`governance-native-git-hooks.json`，不冒充本次重新執行。Copilot 可選項仍提示未安裝，與本次 Codex 接線分開。

合約已加入 `hard_stop_rules`，故事文件違規不再只是 warning。隔離命令驗證失敗拒絕、故事保護、執行環境注入、重複 Stop、缺少前置檢查、resume/compact、缺乏／過期證據及完整導入宣稱。收尾命令另驗證 canonical 內容有效及 receipt，並要求實際耗時小於平台三秒上限；replay 禁止寫正式日記，不能替代原生 writer 證據。

初次安裝時 installer 回報 `REQUIRES_USER_REVIEW`；使用者現已確認四個事件皆已信任／啟用並重新載入。自然事件驗收仍未觀察到：完整導入判定還需要同一自然 session 的四個成功事件與 `written`／`already_present` canonical writer receipt；目前不能稱已完整導入。這項待驗狀態沒有以 smoke、Git hook 成功或靜態 full_candidate 取代。

啟用前已把本輪手動 smoke runtime 完整移至工作區 `scratch/governance-before-native-20261020T1109/` 保留，避免 R2 將舊 envelope 誤判為未完成 owner。沒有刪除歷史或改寫自然 session 證據。正式故事仍停 S3，未修改 UI 行為，沒有自行結束此聊天。

以下為前一階段歷史；其中「尚未接線／post_task 為 null」描述已由上述新里程碑取代，平台信任與自然回呼仍待驗。

## Windows 工作副本重新驗收

本次使用者指示「先幫我導入AI governance」。觀察到新工作副本的 submodule 未初始化、Git hooks 未安裝，舊驗收屬於先前環境。本次已還原固定的 e8e67796894cd562ef0bce217bfad0fac211a44d，使用官方 Python installer 安裝 hooks-only；未更新框架版本。

Windows 以普通檔案簽出 ui-prototype/memory 與 .governance 的符號連結，且建立真正連結被 WinError 1314 拒絕；原 UI smoke 因此 session_start_ok=false。已移除兩個連結，改從 repo runtime root 讀取唯一的記憶、規則與 baseline，仍明確使用 UI 計畫；相同 smoke 重跑的 pre_task、session_start 與 validator preflight 均通過。

本機 readiness 17/17、drift 與 hook 安裝檢查通過，證據為 artifacts/governance-windows-readiness.json、governance-windows-drift.json、governance-windows-hooks.json，以及更新的 governance-ui-quickstart.json。手動 runtime、安裝檢查與真實 Git hook 觸發是不同證據；本次 Git 交付結果另以實際終端輸出及遠端 HEAD 核對，尚未自動接上 Codex lifecycle。下方原有環境的紀錄保留為歷史，不能當成本機最新執行結果。

另外執行 `python scripts/validate_ui_scope.py` 通過13份企劃保護檢查；`npm run build --prefix ui-prototype` 首次因未安裝依賴找不到 tsc，執行 `npm ci --prefix ui-prototype --ignore-scripts --no-audit --no-fund` 後建置成功。記憶 authority guard 全部計數0、warnings/blockers 為空且 completion_claim_allowed=true，原件見 artifacts/governance-windows-memory.json；這是里程碑記憶檢查，不是 session-end closeout。本輪 UI 行為未變更，未重跑或宣稱新的瀏覽器驗收。

## 結論

本 repo 已達框架靜態評估的 **full_candidate**：必要靜態治理檔案齊備，版本帳本與 submodule 一致，repo-specific 規則、contract 與 validator 已存在。根目錄 readiness 全部17項檢查通過，沒有 error。這個名稱表示可進一步驗收的完整候選，不等於所有 agent 對話都有自動強制治理。

除靜態評估外，本輪確實執行了專案 runtime smoke、正式 commit 與 push，以及 canonical memory writer 和 authority guard；不能只用 summary 裡的 not_checked 否定這些獨立證據，也不能反過來把手動測試當成已接上平台自動 lifecycle。

## 本輪實際證據

| 面向 | 已觀察狀態 | 證據／範圍 |
| --- | --- | --- |
| Framework 本體 | submodule 已提交 | e8e67796894cd562ef0bce217bfad0fac211a44d；Apache-2.0 notices 保留 |
| 版本帳本 | consistent | governance/framework.lock.json 與 checkout 相同；對本地 tracking ref current，未另做 F7 遠端最新更新 |
| 本 repo 規則 | 已導入 | AGENTS.base + 專案 AGENTS；原故事正文保護、UI scope、風險升級界線 |
| 領域合約 | 已載入 | game-ui-prototype / low；風險分類由使用者授權代填 |
| 靜態檢查 | PASS | readiness 17/17、drift 無 error |
| DomainValidator | 可載入、可執行 | 保護13份故事企劃；PLAN 只允許核准的治理表頭；禁止 Actions／root LICENSE；檢查美術資產 |
| 根 repo runtime | PASS（手動） | session_start=True、pre_task=True；rules common + game-ui-prototype |
| UI workspace runtime | PASS（手動） | scripts/verify_governance_ui.py；validator preflight=True |
| 本機 Git hooks | 真實觸發成功 | a97c8a8 正常 commit；正常 push 已被遠端 main 接受；無 --no-verify、強推或繞過 |
| 記憶工作流 | writer + guard 通過 | canonical daily 綁定 a97c8a8；guard 全部計數0、warnings空、completion_claim_allowed=True |

第一次 push 的 pre-push JSON closure guard 實際掃描19個 JSON blobs 並通過；隨後的 runtime enforcement 跑的是 framework 自身 smoke。消費端 campaign-forge 的 runtime smoke 另外獨立執行，兩者證據沒有混稱。

## 還不能宣稱的部分

- 沒有把 Codex 桌面 task 的每次 session_start / post_task / session_end 自動接線；目前是本機 Git hooks 加手動 runtime 驗證。
- 外部 repo smoke 的 post_task_ok 為 null（沒有本專案的 post-task replay fixtures），沒有宣稱完整後置語意檢查已驗收。
- 內建 domain 自動 risk lookup 尚不認識 game-ui-prototype，可能顯示 unknown；contract 明確宣告 low，root smoke 的執行參數也明確傳入 low。沒有改成不相干領域來消除提示。
- framework smoke 留有 assumption/decision policy 的 advisory；沒有關閉它們或偽造結構化決策證據。
- 未啟用 CI／GitHub Actions，也未宣稱所有開發者機器都強制安裝 hooks。
- 沒有做正式故事、玩法正確性、完整框架測試套件、正式發行或外部玩家驗收。

這次是首次手動 submodule onboarding，沒有聲稱 F7 更新流程已執行。首次 pre-commit 對尚未提交的版本帳本及缺少 update receipt 有 advisory；提交後帳本已 consistent。canonical memory 的初次 evidence commit mismatch 已透過在 a97c8a8 上重跑實際檢查並重產 receipt 解決，沒有手改測試 exit code。

## 工具原始人類可讀摘要

以下完整保留工具的靜態摘要；runtime 與記憶的實際執行補充以本文件上表及相關 evidence 為準。

用途：這段用人類可讀的方式說明 AI Governance 更新後，目前哪些功能已導入、哪些尚未導入或尚未驗證。
先看結論：
這份檢查做了什麼：檢查 framework、版本帳本、repo 規則、hooks、領域合約、自動檢查與記憶工作流的可見狀態。
現在能不能用：可使用目前可見的治理表面；但 runtime 強制與內容正確性仍未被證明。
還差什麼：這份靜態檢查沒有看到導入缺口；runtime 與實際強制效果仍未驗證。
整體導入狀態：full_candidate - 可見的靜態表面已齊備，但 runtime enforcement 仍未被證明.
需要查技術細項再往下看：
AI Governance 功能導入狀態：
| 功能 | 狀態 | 這個功能是做什麼 |
| --- | --- | --- |
| 版本帳實一致性（Lock vs checkout consistency） | 已可用 | 比對 governance/framework.lock.json 的 adopted_commit 與本地 framework checkout HEAD；不做 fetch，也不宣稱真實遠端最新版。 |
| 框架本體（Framework checkout） | 已可用 | 提供 AI Governance 工具與規則來源；目前偵測到的導入型態是 submodule_consumer。 |
| 版本新鮮度（Framework version freshness） | 已可用 | 檢查本地 framework 是否追上本地已知 tracking ref；真正遠端最新證據由 updater 另外回報。 |
| 本 repo 規則（Repo governance instructions） | 已可用 | 讓 agent 進入這個 repo 時知道本 repo 的風險、測試與操作規則。 |
| 靜態治理檔案（Static framework files） | 已可用 | 提供不跑 runtime 也能讀到的治理文件、規則與導入狀態。 |
| runtime 治理能力（Runtime-capable governance） | 未驗證 | 代表 repo 是否具備可執行的 runtime governance；只有明確回報已可用時才算導入。 |
| 本機 commit/push 檢查（Git hooks） | 已可用 | 在本機 commit 或 push 前提示/檢查治理狀態；這不等於所有機器都已強制執行。 |
| 領域合約（Domain contract） | 已可用 | 用 contract.yaml 宣告這個 repo 自己的治理需求與驗證入口。 |
| 自動驗證層（Validator surface） | 已可用 | 列出 repo 專屬 validator，讓更新後能知道是否接上自動檢查。 |
| 記憶工作流（Memory workflow） | 未驗證 | 顯示 memory 寫入/檢查流程是否有被觀測；不代表記憶內容已完整同步。 |
技術細項：
- AI Governance framework checkout: present - 偵測到的導入型態是 submodule_consumer
- Framework version freshness: current_vs_local_tracking - 比較本地 framework 與本地已知 tracking ref；這不是遠端最新 head 的證明
- Repo governance instructions: 已可用 - AGENTS.md 包含 agent 應遵守的 repo 專屬治理規則
- Static framework files: yes - 檢查可見 framework 檔案是否足以提供靜態治理指引
- Runtime-capable governance: not_checked - 這份 summary 不證明 runtime execution 已可用
- Git hook framework root: inside_repo - 顯示本機 pre-commit/pre-push hooks 指向哪裡；hook 是本機狀態，不代表所有環境都強制執行
- Domain contract: 已可用 - contract.yaml 宣告 repo 專屬治理合約
- Validator surface: 已可用 - validator 是 contract 宣告的 repo 專屬自動檢查
- Memory workflow surface: not_checked - 這份 summary 不推論 memory 是否完整同步
尚未導入或尚未被證明：這份 report-only summary 沒有偵測到缺口。
白話結論：
- AI Governance 在可見的靜態表面上看起來已齊備，但 runtime enforcement 仍未被證明。
不能從這份 summary 宣稱：
- domain correctness
- framework pin matches the true remote head
- full governance adoption
- hook or CI enforcement
- memory consolidation completeness
- release readiness
- runtime self-contained governance
- runtime smoke passed

## 重現與證據

- `python3 scripts/validate_ui_scope.py`
- `python3 scripts/verify_governance_ui.py`
- `PYTHONPATH=ai-governance-framework python3 -m governance_tools.external_repo_readiness --repo . --framework-root ai-governance-framework --format human`
- `PYTHONPATH=ai-governance-framework python3 -m governance_tools.memory_workflow --repo . --check --run-guard --format json`
- artifacts/governance-readiness.json
- artifacts/governance-drift.json
- artifacts/governance-hooks.json
- artifacts/governance-maturity.json / .txt
- artifacts/governance-memory-check.json
- artifacts/evidence/test-results/external-repo-smoke.json
- artifacts/evidence/test-results/ui-build.json、scope.json、ui-governance.json

早期失敗診斷（例如 governance-quickstart.json）保留為歷史，不能替代本次最後檢查的結果。無部署、無 PR、無付費，正式故事仍停在 S3。
