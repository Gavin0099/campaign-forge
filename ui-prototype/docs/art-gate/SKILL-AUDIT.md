# L03 Skill Compliance Audit

本輪基線：`codex/l03-battle-ui@b783cf9093ce878bbb2bfdb6462364fb464e188a`。Owner 已判定該版美術 **FAIL**；其 23 項工程報告不構成美術通過。本輪另開 `codex/l03-art-quality-gate`，不合併 main。

## 可以證實的範圍

本輪在實作前以工具讀取下表四份 Skill，並另讀 external-executable checklist。完整位元組摘要與記錄產生時間見 [skill-receipts.json](skill-receipts.json)。這是本輪的讀取紀錄，**不能補證上一輪曾完整執行**。先前聊天有部分 Skill 使用敘述，但缺少當時檔案版本、雜湊與逐項成果對應，因此歷史結論為 `INSUFFICIENT_VERSIONED_EVIDENCE`；不能推導為完全未使用，也不能宣稱完整合規。

| Skill／實際路徑 | 版本／本次 SHA-256 | 觸發與本輪使用範圍 |
|---|---|---|
| frontend-design · `C:/Users/daish/.codex/skills/frontend-design/SKILL.md` | frontmatter 2.0；`15dec421f25b266e7df5366e18a2321df946de05556bb07dfe07e942aa20a742` | 使用者要求重作戰場與 HUD，採 immersive 模式；場景優先、邊緣 HUD、相同狀態 A/B、真實尺寸與輸入檢查 |
| imagegen · `C:/Users/daish/.codex/skills/.system/imagegen/SKILL.md` | 未宣告語義版本；`706d4d96e1d5c9e6023fe3ccabba1bb34b364024d344fd25b8515ec7d28fe3c4` | 本輪需要新繪景及同角色造型轉換；使用 built-in image_gen，保留透明度、原件、完整提示和來源，不使用 CLI／API fallback |
| external-executable-trust-audit · `C:/Users/daish/.codex/skills/external-executable-trust-audit/SKILL.md` | 未宣告語義版本；`5ca3988fc2e963dbd24127e476b34727d1bcbd18906c4277e8781ae95190265a` | 查驗本地 Git／Node／Python／Chrome 固定路徑、大小及摘要；瀏覽器啟動使用 allowlist 環境。僅執行身分查驗，未做完整對抗性安全審查 |
| dnd-framework · `D:/campaign-forge/scratch/narrative-alignment/.codex/skills/dnd-framework/SKILL.md` | story `0be4c94cee65036037707f9fc25b432f6b266e9d`；`c07764e756590c286dd88421e82ad374601a6732e2c2876f958a6dd8dfa5427b` | 使用者明確要求查核；唯讀核對原創 IP 界線、既有敘事錨點及 G005 尚未定案；不新增職業、規則或法術 |

### dnd-framework 分支核對

- `git ls-tree -r b783cf9 -- .codex/skills` 無該檔；本輪 UI 工作區路徑亦不存在。
- 故事分支 `0be4c94` 有 `.codex/skills/dnd-framework/SKILL.md`，Git blob `7983f232e6f61ed537fc1a5e2abfab4217d9ffda`；故事 worktree 無未提交變更。
- 本輪直接唯讀上述實際檔案，沒有複製一份到 UI 分支來營造歷史載入證據。
- Git blob ID 與工作區檔案 SHA-256 分屬不同演算法／換行表示，不混為同一種版本號。

## 規則如何落到成果

| 規則 | 可核對成果 | 證據上限／缺口 |
|---|---|---|
| 先確立模式、視覺命題與資訊層級 | [ART-GATE.md](ART-GATE.md)；`src/ArtGate.tsx` 的整幅場景、邊緣工具、可選地標及單一檢視區 | 代理提出與實作；是否令人滿意由 Owner 決定 |
| 真實尺寸、鍵盤、放大、窄屏與失敗狀態 | `tests/art-gate-browser.mjs`；`screenshots/art-gate/capture-record.json` | 操作與畫面技術檢查；沒有真人試玩、螢幕閱讀器或完整 WCAG 認證 |
| 圖片先檢視、透明資產不破壞、專案複製留存 | 先檢視原三人／兩敵圖集再轉換 B 造型；原圖不改；[asset-provenance.json](asset-provenance.json)、四份 `*-prompt.txt` | 圖片生成模型／seed 未由工具提供；不捏造。B 是預繪外觀，沒有 3D 原始模型 |
| 不把美術規格與 Prompt 冒充 Skill 載入 | 本檔分開記錄實際讀取、檔案摘要與成果，歷史證據不足保留 | 讀取不是完整遵循的自動證明；仍逐項列未完成事項 |
| 原創、不引用未授權人物與正式規則 | 沿故事分支既有 Teo／Maggie／三船／三箱；外觀皆為提案；無 SRD 規則新增 | 本輪未取用 SRD 條文，因此不以 Skill 本身作新規則來源或授權證明 |
| 分離工程與藝術驗收 | 舊版 Owner FAIL、本輪工程報告、A/B 待選，各自記錄 | 不宣稱商業品質通過；不進動畫關卡 |

## 執行鏈查驗範圍

Git、Node、Python、Chrome 實際大小及 SHA-256 與現有本機 binding 一致。新瀏覽器測試會在載入 Playwright／啟動 Chrome 前驗證 Chrome 路徑、大小及摘要，並僅允許 `127.0.0.1` 網頁請求。Node/Python/Git 使用絕對路徑執行。

**結論：完整外部執行信任鏈證據不足。** 未對桌面外層 launcher、npm 子程序、Git credential helper／動態函式庫、所有環境選擇器做對抗測試；不能宣稱沒有 ambient trust roots。本輪未修改憑證、安全設定或治理 hooks。使用者已完成 hooks 信任／reload；原生平台回呼證據仍待驗，兩者分開。
