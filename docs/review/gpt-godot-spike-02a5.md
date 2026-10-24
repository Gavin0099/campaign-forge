# GPT review — Godot spike-02 A5 (Thoma swing/00–04 seams, cuffs, bag, feet)

- Source: ChatGPT campaign-forge project, new chat "美術審查結論" (https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6adc2ee1-8d94-83ec-b23a-d7529a0de5c5)
- Mode: Thinking, effort High; date 2026-10-24
- Reviewed commit: codex/godot-spike 78bb38a (A5 W1–W6, cc164b2..78bb38a)
- Attachments: region-check.png, asset-sheet-a4-vs-a5.png, swing-smear.png (720p)
- Transcribed verbatim from page text; tables rebuilt as Markdown; embedded "Analysis output" images not included.

---

## 1. 逐格判定

| 幀 | 判定 | 主要原因 |
|---|---|---|
| swing/00 | FAIL | 右側鞋子與身體分離，下襬、腿部輪廓不連續。 |
| swing/01 | PASS | 五格中最完整，未見明顯的大型斷裂；仍須檢查播放時的接縫跳動。 |
| swing/02 | FAIL | 袖口碎片、下襬三角殘片、腿與鞋分離，問題明顯。 |
| swing/03 | FAIL | 揮擊手臂下方存在不自然的袖片、接縫與布料重疊。 |
| swing/04 | FAIL | 下襬殘片懸空，腿部、鞋子與衣料的連接仍不自然。 |

## 2. 分區判定

| 分區 | 判定 | 說明 |
|---|---|---|
| Stole（披肩／垂布） | PASS | 主體仍可辨識，沒有明顯重複布料。 |
| Embroidery（刺繡） | PASS | 刺繡圖案大致保留，並非目前主要問題。 |
| Cuffs（袖口） | FAIL | 局部袖片斷裂、重疊不自然。 |
| Hem（下襬） | FAIL | 殘片與腿部輪廓不連續。 |
| Seams（接縫） | FAIL | 多處拼接邊界與斷裂痕跡仍可見。 |
| Bag（包袋） | PASS | 重複包袋問題大致修正。 |
| Feet（腳部） | FAIL | 多格存在鞋子分離、腿部銜接異常。 |
| Sequence（序列） | FAIL | 動作順序大致合理，但逐格瑕疵造成視覺跳動。 |

## 3. P0 / P1 / P2 問題

- **P0：無。** 沒有證據顯示存在必須立即處理的核心功能性阻斷。
- **P1：美術驗收阻斷。** swing/00、02、03、04 的斷裂鞋子、袖片與下襬接縫，直接破壞角色完整性。
- **P2：驗證不足。** 720p 單張截圖只能確認特定時刻的畫面，無法證明連續播放時沒有閃爍或部件跳動。GUT 48 tests／2126 asserts 全過，只能證明測試涵蓋的程式行為，不代表美術合格。

## 4. 總結 Verdict

**REJECT**

這五格尚未達到美術可接受標準。

包袋問題已有進展，但接縫、袖口與腳部的結構性瑕疵仍然存在。單靠遊戲內縮小後不明顯，不能視為修復完成。

下一步建議：停止目前的 cutout rig 局部拼貼修補，改採整組重繪或受控生圖後人工修圖。

- 保留 idle/01 與 swing/05 不變，作為角色造型與比例錨點。
- 重新製作 swing/00–04 五格，優先確保完整人體輪廓、袖口、下襬與鞋子的連續性。
- 若採用生圖，建議逐格生成並以固定參考圖約束角色設計，再人工修正；不要直接生成整張五格圖後就當成可用素材。
- 先通過等比例透明背景逐格檢查，再以實機連續播放驗收。

判斷依據：A5 已證明局部修補能改善包袋等細節，卻沒有解決反覆出現的接縫與肢體斷裂。繼續投入相同修補方法，成本效益已不理想。
