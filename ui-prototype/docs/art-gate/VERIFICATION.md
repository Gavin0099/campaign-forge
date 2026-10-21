# L03 Art Quality Gate — 驗證與判定

本輪不更改 Owner 對 `b783cf9` 的美術 FAIL。A/B 是新靜態候選，**商業美術品質 PENDING_OWNER_REVIEW**；不合併 main，不進動畫 Gate。

## 工程結果

| 檢查 | 結果／證據 |
|---|---|
| TypeScript + Vite production build | PASS；46 modules，JS 228.02 kB／gzip 80.43 kB，CSS 73.24 kB／gzip 17.22 kB；不含圖片，不代表效能通過 |
| 原企劃範圍保護 | PASS；`scripts/validate_ui_scope.py`，13份企劃、無新增 Actions／根 LICENSE、四原始素材仍在 |
| 新樣板實機檢查 | **11 PASS**；[capture-record.json](../../screenshots/art-gate/capture-record.json)，7張截圖，綁定全部 src、新資產、原圖集與測試程式摘要 |
| 原 L03／兩條舊流程回歸 | **23 PASS**；[最新回歸報告](../../screenshots/art-gate/legacy-regression/capture-record.json)，10張新截圖；不覆寫原 `screenshots/l03/` |
| 素材來源與提示 | 四份完整 Prompt、[asset-provenance.json](asset-provenance.json)，複製品與生成原件位元組一致；兩張 B 圖集實測 RGBA、alpha 範圍 0–255 |
| Skill 證據 | 見 [SKILL-AUDIT.md](SKILL-AUDIT.md)；本輪讀取有路徑／SHA／用途，歷史完整遵循仍無足夠證據 |
| diff whitespace | `git diff --check` PASS |

11項包含 A/B 各 720p／1080p 的真實載入與範圍、同一狀態切換、7地標鍵盤與 Esc、地標顯示、大字／390寬重排、實際中止場景圖片請求再重試、Reduced Motion 下選取，以及原選單進入／返回焦點還原。瀏覽器為固定大小／摘要的本機 Chrome 155，Playwright 1.64.1；網頁請求僅允許 loopback，沒有部署。

A/B 同狀態 SHA-256：`64d6f876bc0632366b7b595bae1a8d7a5c32806a3d2a191aafb215c05a9f178c`。此摘要證明資料相同，**不證明生成底圖自動符合所有敘事、地形與視覺條件**。

23項回歸重跑既有 L03 的兩尺寸、兩分支、繞障／斷橋、確認一次結算、切換取消、命中前後撤銷、繩索／支援、鍵盤／對話焦點、放大／窄屏、真卸載、失敗圖集 fallback，以及原居民完整路線和缺席席恩／奧倫的單人莉妲軍糧路線。測試本輪只改輸出目錄以保留 Before，沒有放寬原斷言。

## 實際視覺檢視

代理以工具開啟實際輸出的 A/B 720p、A 1080p、Maggie 檢視及390寬大字截圖。第一輪發現爬行者落在岸壁、敵方標籤遭欄杆遮擋，已移至橋面並分離標籤層，之後重新擷取最終版本。最終 A/B 四張主截圖均來自同一套程式，未手工拼貼 HUD 或替換渲染內容。

可觀察：畫面鋪滿場景，三船與三箱可見，Maggie 作為人物位於車前，Teo 的燈與兩人名稱常駐；A/B 地景造型不同，人物／HUD 是獨立 React 圖層。尚未完成：動態前後遮擋、全方向人物、導航格與新背景精準對位、NPC／船獨立圖層、清楚的水利拓撲、原生1080p底圖與正式壓縮。完整逐項差距在 [ART-GATE.md](ART-GATE.md)。

大字模式將 HUD 放入文件流，可捲動到所有資訊。390寬是閱讀與鍵盤退路，**不視為合格的手機戰棋畫面**。未做真人試玩、螢幕閱讀器測試或完整 WCAG 稽核；沒有用操作自動化宣稱美術／可用性通過。

## 重現

在 `ui-prototype` 啟動現有 Vite，port 5175。使用既有 Node／Chrome 及本機 browser binding：

```powershell
npm run build --prefix ui-prototype
npm run test:art-gate --prefix ui-prototype
npm run test:evidence:art-gate --prefix ui-prototype
npm run test:l03 --prefix ui-prototype
npm run test:evidence:l03 --prefix ui-prototype
```

`test:visual`／`test:evidence` 預設指向本輪品質樣板；`test:l03`／`test:evidence:l03` 指向保留的操作回歸。歷史資料夾保留當時報告，不拿舊雜湊冒充新版驗證。生產 build 已完成，但截圖來自本地 Vite 執行畫面，未聲稱已部署產品。

## 最終關卡

- 工程／靜態檢視功能：PASS（上述明確範圍）。
- 視覺技術整合：有實機與逐張觀察；新地形／導航整合未完成。
- 商業美術：**待 Owner，可選 A／B 或兩案都不採用**。
- 動畫／正式戰鬥規則：本輪未實作。下一階段須先有 Owner 選定方向。
- 治理：使用者完成 hooks 信任與 reload 的陳述保留；原生 callback 證據仍待驗。本輪 commit/push hook 成功不取代該證據。
