# Campaign Forge 工作界線

本 repo 專做原創 Steam／PC 奇幻戰棋 RPG 的故事企劃。當前停在 S3 故事選擇關卡，A、B、C 都是提案。

- 先讀 README、PLAN、SLICES、docs/DECISIONS.md 與 docs/EXECUTION.md，再接續工作。
- Gavin 選案前，保留三案獨立性。推薦結果不構成定案，不建立正式世界觀或 24 關腳本。
- 已核准的本批只有 S0 至 S3。S4 起須在使用者選案並明確授權後才執行。
- 所有讀寫限於本企劃工作區。可唯讀查閱 docs/SOURCES.md 列出的公開來源。不要讀取其他專案、公司檔案或公司系統。
- GitHub 僅使用已授權工具與既有 gh 登入。目標 `Gavin0099/campaign-forge` 已由擁有者建立並選擇 Public；不重試建庫，不新增憑證、登入或權限，不變更 visibility。
- 僅正常推送到已授權的目標 repo。若遠端出現尚未核對的提交或衝突，停止並報告；不覆寫使用者內容、不接管其他 repo、不強制 push。
- 不啟用 GitHub Actions、付費工具或部署，不寫遊戲引擎、戰棋原型，不操作硬體。
- 不沿用其他專案的平台或定價限制，不合併其他遊戲專案。
- 不複製 D&D 人物、地名、原文、關卡或未授權書籍。職業名稱、技能、規則與授權仍待後續設計。
- 不新增把故事內容開源的 LICENSE。若將來採用第三方程式或文件，先逐項保留相應來源與授權聲明。
- 設定變更要標示提案或已確認。每個重大選擇必須寫出玩家已知資訊、實際代價與後續可見後果。
- 每位核心同伴要有自己的目標、拒絕條件與離隊後的行動。主線不得因少一名可選同伴而無法完成。

本文件未授權自動接續未來 slices，也未要求新增代理或平行執行。

## UI Prototype Authorization — 2026-10-20

使用者本次明確授權 `ui-prototype/` 的 UI-01 至 UI-05、原創展示美術與 AI Governance 完整導入；此範圍優先於上方「不寫戰棋原型」的一般界線。原始故事正文、SLICES、docs 均保持不變（根 PLAN 可加下方明確授權的治理表頭），S4 仍未授權。參考 TacticalGo 僅限使用者指定的公開 skill 方法；不得挪用人物、美術、其他專案限制或正式設定。

本 repo 延伸 `AGENTS.base.md`，使用者明確限制優先：未另行授權不得 commit、push、PR、部署、付費或啟用 Actions。框架的自動流程不得自行擴張權限。

## Repo-Specific Risk Levels
<!-- governance:key=risk_levels -->

- domain: game-ui-prototype；risk_tier: low，由使用者「你直接幫我寫就好」授權代填。
- L0：文字、文件、純視覺資產檢視。
- L1：React UI 狀態、選擇後果、角色缺席與鍵盤操作；需實際操作證據。
- 低風險依據：僅本地 UI 展示，沒有生產資料、付款、連線、正式存檔、完整戰棋引擎。

## Must-Test Paths
<!-- governance:key=must_test_paths -->

- `ui-prototype/src/`：兩條故事選擇、部署缺席角色、移動／技能預覽／確認／撤銷、結果回戰役。
- `npm run build --prefix ui-prototype`，`python3 scripts/validate_ui_scope.py`。
- 瀏覽器實測 1920×1080、1280×720、放大文字、對白紀錄與 Esc；截圖必須來自執行畫面。

## L1 → L2 Escalation Triggers
<!-- governance:key=escalation_triggers -->

正式故事定案、正式戰鬥規則、永久資料、帳號、網路服務、安全設定、費用、公開部署及跨專案寫入，均超出本輪 UI 授權，需回報與取得相應授權。

## Repo-Specific Forbidden Behaviors
<!-- governance:key=forbidden_behaviors -->

不得把 A 美術或固定資料當正式設定；不得覆寫原始企劃、其他分支或使用者未提交檔案；不得複製商業遊戲素材；不得宣稱安裝 hooks 等於實際 commit/push 驗證。

## AI Governance Memory Workflow Router
<!-- governance:key=memory_workflow -->

開始工作讀 `memory/01_active_task.md` 與 `memory/02_project_facts.md`。里程碑更新 `ui-prototype/PLAN.md` 與相關記憶；使用者陳述與代理觀察分開記錄。依框架 session-end 定義才觸發結束紀錄；最終回覆本身不表示 session end。

治理工具以 `PYTHONPATH=ai-governance-framework python3 -m governance_tools.<tool>` 執行。UI 計畫位於 `ui-prototype/PLAN.md`；部分上游 readiness 工具硬編碼根目錄 PLAN，需如實列出差異，不能為通過檢查而修改故事企劃。框架更新使用 F7 流程；目前為首次 submodule 導入。

### 本輪 Git 授權更新

2026-10-20 使用者追加「做完一個段落幫我push」，授權本輪完成段落的正常 commit/push 到既有 campaign-forge repo；不含 PR、部署、Actions、強推或修改正式故事。

2026-10-20 使用者確認「允許只加治理表頭並繼續 push」；允許套用 governance/proposed-root-plan-header.patch 的確切 metadata，故事正文與 S3／S4 狀態不變。
