# Campaign Forge UI Prototype

> **最後更新**: 2026-10-20
> **Owner**: Gavin（需求與決策）；Codex（本輪執行）
> **Freshness**: Sprint (7d)

## Scope

獨立的 React / TypeScript 本地 PC UI 展示。原始 README、PLAN、SLICES、DECISIONS、EXECUTION、候選 A 與比較文件已閱讀。A/B/C 未選案；A 只供展示，人物外觀與地圖均是提案。不得以 UI 展示取代 S4 授權。

## Slices

- UI-01：流程、資訊層級、資料分離、風險界線完成。
- UI-02：主選單、六章24節點示意、營地人物、劇情抉擇完成。
- UI-03：隊伍部署、戰場、選角→移動→技能→確認及撤銷完成；規則固定示範。
- UI-04：選擇延續到支援、目標、同伴與戰後結果完成。
- UI-05：四位人物、五種戰場小人、渡口場景與戰役地圖已整合；實際驗收記錄見 docs/VERIFICATION.md。

## Design

視覺重心是人物與戰場。成熟低飽和奇幻插畫、羊皮紙地圖、低調金屬框，繁體中文。人物立繪與小人獨立生成；敵我用 ◆／▲、文字及色彩一起區分。24節點是容量示意，後續章名與路線不揭露。

## Decisions

- 使用 React 18 / Vite 4 / TypeScript 5.6，僅介面驗證，不指定正式引擎。
- 遊戲資料在 src/data.ts，素材路徑在資料設定中維護。
- 無正式儲存，狀態在本次頁面生命週期保留；重設按鈕明確清除。
- built-in image_gen 生成原創展示素材；不下載商業遊戲圖片。
- domain / risk 由使用者授權代填為 game-ui-prototype / low。

## Risks and pending decisions

正式故事、角色身分／外觀、地圖地理、職業／技能、勝敗判定、戰鬥數值都待選案與設計。手把只有映射提案。尚無外部玩家可用性測試與正式平台相容性測試。

## Verification

建置、範圍保護與 CUA 實際瀏覽器流程；保留 screenshots 與 docs/VERIFICATION.md。AI Governance 使用者後續已授權 commit/push，真實 hook 驗證於正常交付時執行；不得稱完整驗收完成。
