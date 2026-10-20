# Project facts

## Human-provided requirements (2026-10-20)

Owner Gavin。目標 Steam / PC 故事戰役、小隊養成奇幻戰棋 RPG；A/B/C 候選未選定。UI 僅可用 A 作展示，不制定正式故事、規則與骰子系統。
授權 UI-01..05、React+TypeScript 展示、原創素材及治理導入。人物、戰鬥和地圖是當前優先成果。參考曹操傳／孔明傳的可讀性，不複製其素材。
所有讀寫限本 repo；公開指定 framework 與 TacticalGo 可唯讀參考。不啟用 Actions、不部署、不購買、不寫正式引擎。
使用者委託代理填 domain/risk；選定 game-ui-prototype / low。使用者後續明確指示「做完一個段落幫我push」，已授權本輪正常 commit/push，未授權 PR/部署。

## Agent-observed implementation facts

Node16 / React18 / Vite4 / TypeScript5.6，本地頁面記憶狀態，不是存檔。四張 built-in image_gen 圖像原檔保留於 ui-prototype/public/art。範圍與執行證據以 artifacts、ui-prototype/docs 為準。

使用者後續明確允許「只加治理表頭並繼續 push」，範圍是 governance/proposed-root-plan-header.patch，沒有授權修改故事正文或 S4。
