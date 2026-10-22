# GPT web review: playable-l03 P1v3 (painted battlefield and fantasy HUD)

- Reviewer: ChatGPT web, campaign-forge project (static source review; no tests run, PNG screenshots not viewed directly)
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2/c/6ad9fbcf-1180-83ee-98b8-49d382cfbc74
- Reviewed: codex/playable-l03-research, 7319ef0..1803cfe (P1v3 brief 7319ef0, implementation 5f7cc41, handoff 1803cfe)
- Date: 2026-10-22 20:05 Asia/Taipei
- Prompt: docs/review/GPT-REVIEW-PROMPT.md, with section 7 資源檢核 against docs/review/RESOURCE-CHECKLIST.md
- Claude review: none for this chunk at review time.
- Transcription: Grok Bot copied this from the rendered page text. Tables are rebuilt as pipe rows; the wording is unchanged. Use the chat link above as the source of record.

---

## 1. 結論

needs Owner

P1v3 的程式與視覺工程方向可以接受，但尚未達到 Gavin 要求的「統一暗黑奇幻手繪風格、看起來像正式遊戲」之美術驗收標準。

審查範圍：8f8a42b...1803cfe，共 3 個 commits，聚焦 P1v3，不重新審查 P1v、P1v2 的既有問題。

從實際程式碼可以確認的進步：
- 戰場不再只靠單色格線，而是使用既有地形素材、格塊厚度、場景背景與裝飾。
- UI 從一般資訊面板轉向苔綠、古銅與深色金屬框架。
- 五名角色有戰場立繪及肖像，增加角色辨識資訊。
- 行走路徑、落地回饋、敵我回合提示均有實作。
- 視覺改動仍與純規則運算分離，沒有在這個 chunk 修改戰鬥規則。

核心保留意見：目前是「遊戲化的可操作戰術原型」，不能因為採用了手繪素材，就認定整張戰場已有一致的手繪美術。

另外，這次審查讀取了原始碼與提交的驗證紀錄；下述 PASS 如引用 Codex 執行紀錄，並不表示我親自重跑了測試。

## 2. 問題

以下僅列出從 P1v3 實際檔案確認的問題，依 P0～P2 排序。

| priority | file:line | issue | evidence | suggested fix |
|---|---|---|---|---|
| P1 | presentation.tsx:44–54 | 戰場仍是重複貼圖格塊，而非整體手繪場景。 | 地形由 99 個獨立菱形 polygon 組成，使用四類材質 pattern；水面與地面再以半透明色塊處理。 | 保留邏輯格網，但將視覺層改為整體地景或連續地形過渡，避免每格都有相似的材質切割痕跡。 |
| P1 | presentation.tsx:68–92 | 關鍵場景物件與手繪人物的製作語言不一致。 | 絞盤、斷橋、車隊底盤主要由 SVG 幾何路徑與基本圖形繪製，而樹木、貨物、角色則裁切自繪製素材。 | 下一個美術工作應優先統一絞盤、斷橋、車隊底盤的素材風格，而不是增加 HUD 裝飾。 |
| P1 | presentation.tsx:12–19 | 人物仍無真正的動作影格。 | Figure 顯示單張裁切圖，移動由既有 AnimatedActor 與外部座標動畫完成。 | 製作少量符合既有尺寸的待機／移動影格，先驗證一名角色，避免一次重做全隊。 |
| P1 | presentation.tsx:7–18 | 角色大小未滿足任務簡報的要求。 | 菱形高 52 scene units，角色高 50，比例約 0.96，低於要求的 1.2～1.5；STYLE 與 handoff 也承認此取捨。 | 不應單純放大角色而破壞 P1v2 的零重疊驗收。可考慮調整攝影機投影、角色可視區或遮擋設計後重新驗證。 |
| P2 | PlayableL03.tsx:172–177 | HUD 仍依賴文字與小型計量元件表達戰況。 | 回合、干擾與勝敗條件使用文字、數字及 pips，雖然比原型更有裝飾感，但重要狀態主要集中在頂端。 | 保留精確數字，同時讓戰場上的絞盤具備對應的視覺危險提示，形成場景內與 HUD 的一致回饋。 |
| P2 | playable.css:40–41 | 完整手繪場景未成為主要戰場視覺。 | ferry-scene-v2.png 只作為透明度 .2、模糊 5px、低飽和度的背景，主畫面仍由程式生成格塊。 | 將背景與可操作地形重新整合為一個連續場景，而不是只在棋盤後面放模糊插圖。 |

目前沒有從程式碼確認需要標為 P0 的新缺陷。

## 3. 與交接報告不符之處

核對 handoff P1v3 visual pass 後，沒有找到足以認定交接報告刻意誤述功能的證據，但有三項需要精確解讀。

| 交接宣稱 | 核對結果 |
|---|---|
| Painted battlefield | 部分成立。 有手繪材質與裝飾，但大部分戰場仍由重複 SVG 菱形格塊構成，不是完整手繪地景。 |
| Five original portraits | 成立，但應限定為五個肖像位置。 程式對兩名敵人使用同一份素材的相同裁切區域，不能理解成五張不同的角色肖像。見 presentation.tsx:22–27。 |
| 70 final checks pass | 有提交的成功紀錄支持，但非本次獨立重跑。 command-results.json 保留過程中的 exit 1 與後續成功紀錄；數字也包含既有回歸測試，不能等同 70 項美術品質測試。 |

交接報告明確承認角色比例未達標、幾何道具、重複地形、缺少真正動作影格及 HUMAN_PENDING，因此這些屬於未解決的品質缺口，不是隱瞞問題。

本 chunk 沒有 Claude review，無法比較 Claude 的獨立意見。

## 4. 遊戲性與故事觀點

比 P1v2 更像遊戲嗎？是。是否因此更好玩？尚無證據。

P1v3 改善的是遊戲的呈現與操作回饋，而非決策深度。

從原始碼看，玩家現在可以在同一畫面看到角色、可行走範圍、預測路徑、敵方意圖與目標進度。這是由技術展示走向遊戲介面的明確進展。

但故事與玩法的關係仍偏薄弱：玩家的主要目標是守住絞盤六回合，程式透過站位與敵方路徑計算產生勝敗。本次沒有增加新故事事件，也沒有改變既有策略容易收斂為前期站位、後續等待的問題。

我認為下一個最有效的改變：把戰場做成具有連續地景、可辨識物件與一致材質的真正手繪戰術場景。

這是下一輪建議，不是 P1v3 已完成的內容。

優先處理地景、角色和關鍵物件之間的美術一致性。不要再先增加側邊欄、徽章、數字條或新動畫；否則很可能只是讓原型更精緻，而不是讓玩家更投入遊戲。

## 5. 沒檢查到的部分

本次審查確認讀取了 GitHub 版本 1803cfe 的實際 TSX、CSS、測試程式、STYLE、VERIFICATION、asset manifest、command-results 及交接內容。

但以下證據界線必須保留：
- 未自行啟動 React／Playwright：無法獨立宣稱建置、滑鼠操作、動畫與截圖產生成功。
- 未完成二進位 PNG 的直接視覺比對：GitHub 變更清單確認截圖檔存在，但不能把尚未逐張觀看的 before/after 當成已驗證的美術改善幅度。
- 未親自量測 FPS、GPU 負載、長時間操作與低階硬體效能。
- 沒有真人遊玩紀錄：不能確認 3～5 分鐘的實際遊玩時長、角色是否一眼可辨，以及玩家是否有重玩的動機。
- 沒有確認商業美術權利的完整授權鏈：現有檔案提供來源與雜湊紀錄，但 provenance 不等於最終商用權利核准。

因此，本次對視覺一致性的評語是根據素材組合方式與樣式原始碼的工程審查，而非最終視覺品管簽核。

## 6. 給 Gavin 的決策

建議維持 P1v3 為可接受的技術基底，暫不將它標記為美術完成或正式遊戲品質達標。

最多需要兩個 Owner 決策：
1. 是否同意下一輪以整體手繪戰場替換重複棋盤材質為優先？ 我建議同意，但保留透明的互動格網、純規則引擎與現有測試。
2. 是否接受目前的 50-unit 角色比例作為暫時基準？ 我建議暫時接受，直到實際畫面證明放大角色能帶來更好的辨識度且不破壞重疊和點選測試。

不建議因 P1v3 尚未達標，就推倒既有遊戲邏輯重做。

## 7. 資源檢核

檢核依據：RESOURCE-CHECKLIST.md。

本次 PASS 代表在已讀原始碼或提交紀錄的範圍內有對應證據；未獨立執行的測試均明確標示。

### A. Skills

| 項目 | 結果 | 證據 |
|---|---|---|
| prototype-fast | PASS | P1v3 限定呈現層，未增加新規則；PlayableL03.tsx:10–11。但美術完成標準尚未達成。 |
| level-design | N/A | 本次未修改地圖與路線；既有 P0 測試紀錄為 exit 0，不視為重新完成關卡驗收。 |
| game-ai | N/A | 敵方意圖仍來自純規則 resolve，見 PlayableL03.tsx:88–90；未新增 AI。 |
| game-ui-ux | PASS | 合法範圍、路徑、意圖、目標、輸入說明皆有對應程式；PlayableL03.tsx:172–177,202–225,245–269。人類理解度未驗證。 |
| game-feel | PASS | 實作選取脈動、落地動畫與回合橫幅；playable.css:68–70,99–114。本遊戲無攻擊事件，打擊反饋為 N/A。 |

### B. Reference repos

| 項目 | 結果 | 證據 |
|---|---|---|
| Grid-Tactics | PASS | rules.ts 提供純邏輯結果，presentation.tsx 處理顯示，PlayableL03.tsx:91–96 從 command 取得移動路徑。未發現本 chunk 複製參考 repo 程式碼。 |
| HopeMetal / 2DTacticalRPGDemo | N/A | 未新增從該 repo 借用的程式或素材；STYLE.md:42–55 及 asset manifest 記錄使用既有專案素材。 |
| 無新引擎或 dependency | PASS | P1v3 變更清單沒有 package／lockfile 變更；既有 React、SVG、CSS 架構延續使用。 |

### C. Playable acceptance bar

| 項目 | 結果 | 證據 |
|---|---|---|
| 完整 3～5 分鐘單人戰鬥 | FAIL | 沒有真人計時遊玩；command-results.json:4 明列 HUMAN_PENDING。 |
| 敵人依玩家狀態作出可理解行動 | PASS | PlayableL03.tsx:88–90,202–204,245–255 顯示根據目前狀態求出的意圖與理由；真人理解度待驗。 |
| 玩家可以獲勝或失敗 | PASS | PlayableL03.tsx:63–64,272–276 有勝敗狀態及畫面；原有 P1v 測試紀錄包含成功、失敗回放。 |
| 兩種戰術選擇導致不同結果 | PASS | 既有 hold 與 idle trace 分別成功、失敗；但 A 仍屬 THIN，策略深度並未在 P1v3 改善。 |
| 玩家可重試並改變策略 | PASS | PlayableL03.tsx:103–108,276 有重設邏輯，並有既有回歸紀錄。 |
| 無重複結算、卡住、非法移動及動畫中斷問題 | PASS | PlayableL03.tsx:98–133 使用 busy、pending、RAF 管理；提交的 P1v regression 有相關測試，非全路徑形式證明。 |
| 1280×720、1920×1080 與鍵盤 | PASS | playable-l03-p1v3-browser.mjs:44–105 含兩種尺寸與鍵盤檢查；提交紀錄 exit 0。 |
| 自動化與真人回饋分開記錄 | PASS | visual-results.json 與 command-results.json 分別記錄自動化結果，真人狀態明列 HUMAN_PENDING。 |

### D. Project rules

| 項目 | 結果 | 證據 |
|---|---|---|
| SRD 5.2.1／CC-BY、無 WotC IP，規則修改遵循契約 | PASS | P1v3 未修改 rules.ts 或新增故事與規則內容。asset-manifest.json 記錄五項既有素材來源，但商用授權仍須另行確認。 |
| AGENTS.md 授權範圍、未合併 main、未新增未授權世界觀 | PASS | 比較結果只有此分支三個 commits；交接記錄正常推送至工作分支，未新增劇情或設定。對工作環境操作歷史的判斷依交接紀錄，非完整獨立鑑識。 |

最終判定：P1v3 可以作為後續改善的程式基底，但美術驗收仍需 Owner。主要阻礙不是缺少特效，而是地景、角色與互動物件尚未形成真正一致的手繪遊戲畫面。
