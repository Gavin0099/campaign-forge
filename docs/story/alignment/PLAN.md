# 敘事與產品對齊 Sprint

狀態：本輪可獨立完成的實作／模型審查／候選規格完成，進入交付核對；12 小時是上限預算，不是已投入工時。G004／G005 未決。

授權來源：Owner 2026-10-21 貼入的 12-Hour Continuous Narrative & Product Alignment Sprint。可連續執行本計畫 S0–S6、修改 L01–L07 工作稿、驗證與正常推送 story/strengthen-narrative；不合併 main、不替換 UI、不寫 L08 起劇本。

| Slice | 狀態 | 驗收 |
| --- | --- | --- |
| S0 基準 | 完成；三項 SOURCE_NOT_FOUND | [BASELINE](BASELINE.md)，無原稿不補造 |
| S1 連續性 | 已修可定位問題；人工敘事待審 | [CONTINUITY](CONTINUITY.md)，托瑪、伊瑟拉、物件及出場；缺稿三項不列修復成功 |
| S2 語意驗證 | PASS | 55,296終點、37,791選項邊界；14種破壞由實際CLI拒絕 |
| S3 互動試玩 | 工程PASS；人類試讀待審 | 同源 React／TS、重播版本、選項匯出與回退；32項瀏覽器檢查 |
| S4 深度審查 | 模型兩種視角已做；獨立真人／Owner待審 | [NARRATIVE-REVIEW](NARRATIVE-REVIEW.md)，不冒充兩名獨立審查者 |
| S5 產品規格 | 候選規格完成；待Owner決策 | [Creative Bible](../CREATIVE-BIBLE.md)、[L03](../L03-VERTICAL-SLICE.md)；G004／G005界線不變 |
| S6 交付 | 檢查完成，Git交付核對中 | [VERIFICATION](VERIFICATION.md)；實際提交／push以最後Git核對為準 |

## 計時

第一個可核對時點 2026-10-21 00:39:54 +08:00（UTC 2026-10-20 16:39:54）。此前讀取任務的時間不臆測。各活動時窗將依真實 clock 記錄；重疊只算一次。不以文字字數、測試次數或滿 12 小時作完成指標。

## 治理與來源

保留 [既有正典優先順序](../CODEX-HANDOFF.md)。本計畫授權覆蓋交接文件較早的「不得新增測試／安裝暫存工具／push」限制，範圍只限本 Sprint。原 A／B／C、README／STORY-GATE 與 main UI 均保留。

依 [.codex dnd-framework](../../../.codex/skills/dnd-framework/SKILL.md) 執行；本輪人工讀取 skill，不宣稱新 session 自動發現已驗證。平台自然 hooks 仍未取得回呼證據，不能宣稱完整自動導入。使用既有共用 Git hooks，不停用、不改 framework。
