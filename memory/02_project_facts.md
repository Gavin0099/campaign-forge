# Project facts

## Human-provided requirements (2026-10-20)

最新：Owner拒絕VQ1美術驗收，授權VD2與真實逐幀動畫／法術展示。比較實際候選畫面後選「①戰地測繪」作本輪深化方向，正式故事仍未選。0fc109f修正版hooks已由使用者確認重新信任與重新載入；此使用者陳述不等於代理觀察到自然回呼。

Owner Gavin。目標 Steam / PC 故事戰役、小隊養成奇幻戰棋 RPG；A/B/C 候選未選定。UI 僅可用 A 作展示，不制定正式故事、規則與骰子系統。

2026-10-20 使用者確認 Codex hooks 已完成信任與重新載入；Hooks 檢閱頁四個事件皆為已信任／啟用、沒有錯誤。此為使用者陳述；代理本機尚未觀察到原生回呼收據，不能與完整導入驗收混同。
授權 UI-01..05、React+TypeScript 展示、原創素材及治理導入。人物、戰鬥和地圖是當前優先成果。參考曹操傳／孔明傳的可讀性，不複製其素材。
所有讀寫限本 repo；公開指定 framework 與 TacticalGo 可唯讀參考。不啟用 Actions、不部署、不購買、不寫正式引擎。
使用者委託代理填 domain/risk；選定 game-ui-prototype / low。使用者後續明確指示「做完一個段落幫我push」，已授權本輪正常 commit/push，未授權 PR/部署。

## Agent-observed implementation facts

治理最新修正：重驗曾有SessionEnd 3.390秒失敗，原件保留；合併Git身分查詢並在單一hook程序重用已驗證root後，13項隔離驗收通過，三個新session為2.360／2.281／2.281秒。此次bridge及生成命令雜湊變更，修正版需重新檢閱信任；平台自然事件仍未觀察到。這是代理執行觀察，不是使用者對修正版的信任確認。

2026-10-20最新使用者授權：9.5小時、上限10小時Visual Quality Sprint；可查閱三款指定遊戲官方網站／截圖，研究副本限scratch。以四人、五種小人、渡口與對話為重點，原選擇後果與規則不變。這是使用者要求，並非正式角色或商品名定案。

本次Windows實際執行環境為Node24.13.0、Chrome155.0.8059.40、Python3.12與Pillow12.2.0；Playwright1.64.1是開發驗收依賴。新增8份原創v2素材（含3份保留草稿），v1四份原件雜湊未改。素材與互動格共享mapRows的投影，不依賴背景生成圖決定通行。

早期環境記錄為Node16 / React18 / Vite4 / TypeScript5.6；本次Windows版本見上方最新觀察。本地頁面狀態不屬正式存檔。四張v1 built-in image_gen原檔保留於ui-prototype/public/art。範圍與執行證據以artifacts、ui-prototype/docs為準。

使用者後續明確允許「只加治理表頭並繼續 push」，範圍是 governance/proposed-root-plan-header.patch，沒有授權修改故事正文或 S4。
