# Campaign Forge UI Prototype

> **最後更新**: 2026-10-20
> **Owner**: Gavin（需求與決策）；Codex（本輪執行）
> **Freshness**: Sprint (7d)

## Scope

獨立的 React / TypeScript 本地 PC UI 展示。原始 README、PLAN、SLICES、DECISIONS、EXECUTION、候選 A 與比較文件已閱讀。A/B/C 未選案；A 只供展示，人物外觀與地圖均是提案。不得以 UI 展示取代 S4 授權。

## Slices

### Visual Quality Sprint — 2026-10-20 使用者授權

9.5 小時預算、10 小時上限；以實際投入記錄，不等待逐片確認。保留全部既有流程與固定示範規則，僅候選 A 展示美術；不選案、不執行 S4。完成段落沿用正常 commit/push 授權。

- VQ-01：完成官方競品研究、Benchmark Matrix、Art Direction、10張同狀態 Before。
- VQ-02：完成四人透明立繪、明確裁切與辨識規格；人工人物品質待審。
- VQ-03：完成五種小人、相同色塊與道具、圖集邊界檢查；風格一致性人工待審。
- VQ-04：完成渡口材質／道具、手繪近景及99格地景／互動幾何比對，原11×9資料未改。
- VQ-05：完成生命比例、選取邊線、移動虛影、確認位移及局部−3；720p預覽與操作重排。
- VQ-06：13項真實瀏覽器檢查、綁定After／範圍／縮圖及比較頁；功能與視覺技術通過，商業美術品質人工待審。

證據集中於 docs/visual-sprint/ 與 screenshots/visual-sprint/。視覺技術檢查、功能驗證及人工美術審查分開；既有 Codex 平台信任／自然回呼仍待驗。

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
- built-in image_gen 生成原創展示素材。使用者本輪授權的官方競品截圖只存scratch研究，不進app或公開提交。
- domain / risk 由使用者授權代填為 game-ui-prototype / low。

## Risks and pending decisions

正式故事、角色身分／外觀、地圖地理、職業／技能、勝敗判定、戰鬥數值都待選案與設計。手把只有映射提案。尚無外部玩家可用性測試與正式平台相容性測試。

Visual Sprint已知限制：平面沙盤／河岸方格感、材質重複、靜態小人姿態、12–14px戰鬥metadata的真人閱讀舒適度。沒有用build或代理自評宣告商業美術品質通過；人工檢查見docs/visual-sprint/VERIFICATION.md。實際時間以TIME-LEDGER.md記錄，不把9.5小時預算填作實際工時。

## Verification

2026-10-20 最新平台確認：使用者已完成信任／重新載入，並確認四事件已信任／啟用、無錯誤；本機綁定核對一致，但尚無原生回呼收據。後續重驗發現 SessionEnd 曾達3.39秒，超過平台三秒限制；本輪改為一次 Git 身分查詢，單一 hook 程序內重用已驗證的 consumer root，保留每次路徑核對、完整 envelope／guard／writer 檢查，延後非本事件的 import。新增跨 root 偽造 envelope 拒絕測試及三個全新 session 的計時樣本。結果以 artifacts/governance-native-acceptance.json 為準；失敗原件保留為 governance-native-timeout-regression.json。此次程式修正改變 hook 定義雜湊，須重新檢閱信任修正版，再驗證平台實際執行與自然 SessionEnd／canonical writer；不是否定使用者已完成前一版本的信任。

建置、範圍保護與 CUA 實際瀏覽器流程；保留 screenshots 與 docs/VERIFICATION.md。先前環境已於正常交付驗證 Git hooks；本輪已補四事件 lifecycle 程式與隔離 replay，Codex 信任及自然回呼仍待驗，不得稱完整自動治理。

2026-10-20 Windows 工作副本：恢復固定框架並安裝本機 hooks；UI 治理 smoke 改用 repo runtime root 與明確的 UI 計畫，不再依賴符號連結。readiness 17/17、drift、hook 安裝檢查與 UI runtime smoke 通過；證據及本機交付界線見 governance/ADOPTION-STATUS.md。本輪僅處理治理，未修改 UI 行為或重新宣稱瀏覽器驗收。

2026-10-20 治理補線：SessionStart／UserPromptSubmit／Stop／SessionEnd 分工、故事保護的 hard stop、執行證據及完整導入宣稱檢查已實作。Stop 不作正式收尾，SessionEnd 經 canonical entry 執行；設定為本機產生，須由使用者檢閱信任。本輪不改故事、UI 行為或 S4 狀態。
