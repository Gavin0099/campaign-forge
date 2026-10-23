# GPT web review: playable-l03 P1v6 (per-event feedback and painted winch)

- Range: fc266cb...c980e5a on codex/playable-l03-research
- Reviewer: ChatGPT web, in Gavin's campaign-forge project, 2026-10-23 (Asia/Taipei). Chat "Review P1v6 fixes": https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6adb01fc-9ba4-83e8-92cd-7d695e3331a1
- Prompt included the P1v5 review's five findings.
- Claude review: none for this chunk.
- The reviewer did not run the tests itself.
- Verdict: **needs Owner**. No P0; two P1 and one P2. Resource check C FAIL only on the human 3-5 min playtest (HUMAN_PENDING).
- Below is the reply verbatim (captured via ChatGPT's Copy button; table cells re-joined as markdown tables; one inline web image in the reply is shown as a placeholder).

---


1. 結論

needs Owner

P1v6 在程式架構與戰場回饋上有實質進步，P1v5 的五項問題已獲得有針對性的修正，但尚不適合直接宣布完成正式遊戲品質驗收。

審查範圍：
fc266cb...c980e5a，共 9 個提交。

已由原始碼確認的改善：

- 逐事件回饋：feedback.ts:11–26 建立有序時間線，PlayableL03.tsx:141–183 在播放時觸發特效，不再全部集中在 finish()。
- 接觸火花：feedback.ts:36–54 透過移除相鄰隊友的反事實查詢，排除沒有證據的接觸；只有唯一確認的阻擋者才產生火花。
- 獨立落地：每個有效 move 事件都有自己的 landing cue、位置與到期時間。
- 受阻提示：presentation.tsx:36–47 提供斷鏈與「受阻」標記，不依賴動畫播放。
- 手繪絞盤：presentation.tsx:72–97 已使用四格影格圖集與兩種繩索圖像，取代先前的幾何輪盤與 SVG 繩索路徑。

這些是程式碼層級的確認，不等於我已在瀏覽器完成動態視覺驗收。

2. 問題

以下只列出原始碼中可以確認的問題；沒有查證的美術主觀判斷不列為程式缺陷。

| Priority | File:line | Issue | Evidence | Suggested fix |
|---|---|---|---|---|
| P1 | PlayableL03.tsx:168–183 | 最後一次落地與狀態提交共用同一個播放邊界，無法保證玩家實際看到落地後才進入下一回合。 | 最後一個步驟會先 playThrough()，緊接著呼叫 finish()；React 更新可能在同一個 render 批次完成。交接也明確承認此限制。 | 若要求每次落地都必須在回合結束前可見，需分離最後一個 landing 的呈現與結算邊界；但不應為了視覺特效任意延長輸入鎖。 |
| P1 | PlayableL03.tsx:166–168 | 沒有移動步驟的回合會立即結算，零時刻回饋不保證得到可見時間。 | 程式執行 playThrough(0) 後，若 steps.length === 0 就同步 finish()；例如零步驟的 blocked/progress cue 可能只在同一批 React 更新中出現。 | 將零步驟回饋另設呈現機制，例如短暫且不阻塞操作的視覺提示；增加 no-move blocked/progress 瀏覽器測試。 |
| P2 | PlayableL03.tsx:325–326 | 播放中的受阻標記使用最終預測的 blocked intent，位置卻使用正在播放的單位位置。 | intents 由目前已提交的 state 預測，而標記座標取自 visualUnits。因此播放期間可能出現「整個敵方回合的最終受阻狀態」與「目前正在演出的時間點」混用。 | 預覽階段保持目前做法；播放階段改為依事件索引顯示已發生的 blocked 狀態，或在動畫期間隱藏預測標記，避免提前揭露事件。 |

P1v5 五項問題的修復判定

| 原問題 | P1v6 判定 | 審查說明 |
|---|---|---|
| P1：任意選取相鄰友軍作為火花對象 | 已修正核心邏輯 | 必須相鄰，且移除該友軍後敵人確實恢復 approach；只有唯一候選才顯示火花 |
| P1：只替最後一個 mover 產生落地灰塵 | 已修正資料模型 | 所有有效移動事件各自產生 cue；最後落地與結算共用邊界的問題仍在 |
| P1：所有回饋集中在 finish() | 主要已修正 | 逐事件播放成立，但零步驟情境仍有呈現缺口 |
| P2：幾何輪盤與 SVG 繩索 | 程式實作已修正 | 改為生成圖片圖集；實際美術一致性仍待真人視覺驗收 |
| P2：受阻敵人沒有戰場標記 | 主要已修正 | 標記存在且不依賴動態特效；播放時的事件同步仍可改進 |

沒有查到需要立即否決整個 P1v6 的 P0 問題。 上述三項屬於呈現邊界或狀態同步問題，不代表戰鬥規則本身錯誤。

3. 與交接報告不符之處

核對 P1v6 交接報告 後，主要發現以下證據範圍上的差異：

- 「每個效果在事件當下播放」並非所有情境都能保證可見。 時間線確實會呼叫每個 cue，但零步驟回合立即結算的路徑尚未有獨立的視覺存活保證。
- 「受阻標記在預覽與結算期間持續顯示」在 DOM 存在性上有依據，但未等於逐事件同步。 標記依整回合的預測 intent 建立，而不是根據已播放到哪一個 intent。
- 「四個影格已完成動畫驗證」有原始驗證紀錄，但不是本次獨立實機驗證。 測試會檢查影格順序、圖像來源、截圖時間戳記與圖集遮罩；這不等於已證明四個影格在玩家眼中自然流暢。
- 「107 game checks」是交接端報告的統計，不是我重新執行所獲得的結果。其計數方式為 26 個既有純規則檢查、2 組新增純測試及 79 個瀏覽器檢查。

值得肯定的是，交接沒有隱藏曾經失敗的驗證。attempt-01、attempt-02 與 attempt-03 都有說明，而且明確指出 6d87c20 已由 1e6cb4d 的修正證據取代。

本次沒有 Claude 的 P1v6 審查可比較。

4. 遊戲性與故事觀點

比 P1v5 更接近真正可玩的遊戲，但主要是 Game Feel 進步，而不是戰術深度進步。

P1v6 讓「敵人移動」、「被阻擋」、「絞盤受到干擾」開始具有可追蹤的時間順序。玩家不再只能看最終數值，而是有機會從戰場上的動作理解發生了什麼。

尤其接觸火花的反事實檢查是一個正確方向：沒有實際接觸證據，就不製造假的物理碰撞。這比單純讓特效變多更重要，因為戰術遊戲的視覺回饋應該可信，而不是只有熱鬧。

[image: Rope Winch Windlass - 3D Model by Enterables]

美術評估

新絞盤從幾何圖形轉為圖像圖集，技術方向符合整體手繪化目標。不過，上圖僅是風格參考，並非專案的實際截圖。真正需要 Owner 判斷的是 64×58 場景單位中的可讀性、繩索連接是否自然，以及四格旋轉有沒有機械重量感。

目前我最希望看到的一項改變不是更多動畫，而是：

讓「敵人為何受阻」能在戰場上透過自然的動作與站位被理解。

這是玩法表達的建議，不是新增劇情或設定。當玩家不用看右側說明，就知道自己哪個站位成功防住騎士，這個戰場才更接近真正的戰術 RPG。

5. 沒檢查到的部分

本次已讀取主要程式、任務、交接、測試腳本、資源清單及驗證文件，但下列項目仍有限制：

- 沒有親自執行 Node、Vite、Playwright 或瀏覽器測試。 因此退出碼是交付證據的紀錄，不是我獨立取得的結果。
- 沒有實際開啟並逐幀檢視九張 P1v6 PNG，也沒有以運行中的畫面確認畫質、動畫與文字遮擋。
- 沒有對新 PNG 圖集進行獨立像素、Alpha、雜邊或視覺一致性鑑定。
- 沒有完整重審 P0～P1v5 的規則、全部事件搜尋空間，以及各分支是否存在真正具有深度的獲勝策略。
- 沒有進行未受引導的真人 3–5 分鐘試玩。
- 沒有重新驗證 GitHub 上全部歷史授權與第三方參考資料的完整來源鏈。

因此，我的結論是可繼續作為 P1v6 候選版進行 Owner 驗收，不是正式視覺品質的 PASS。

6. 給 Gavin 的決策

建議只做兩個決定：

1. 是否接受最後一次落地與 finish() 同一邊界？ 我建議現階段接受，不要為了 180ms 灰塵動畫增加回合等待時間，但應補足零步驟事件的可見性測試。
2. 是否接受這批手繪絞盤作為現階段美術基準？ 建議實際看 720p 的四格動畫、2/3 警告及斷鏈標記後決定。如果看起來像圖層切換而非機械旋轉，應優先修動畫一致性，而不是繼續生成更多道具。

我不建議因為 P1v6 的特效數量增加，就將它判定為「戰術系統已經好玩」。接下來對遊戲性最有價值的驗證，仍然是玩家能否理解站位、做出有代價的選擇，以及感受到敵人對自己決策的反應。

7. 資源檢核

依照 docs/review/RESOURCE-CHECKLIST.md 的 A～D 項逐條填寫。PASS 僅代表本次可確認的範圍；N/A 代表 P1v6 未涉及，不代表整個專案已通過。

A. Skills

| 檢核項目 | 結果 | 證據 |
|---|---|---|
| prototype-fast (P0) | PASS | Task brief:1–5、41–55 定義五項修復、90 分鐘時限、驗收及停止條件 |
| level-design (P0) | N/A | rules.ts、地形與部署未在本次修改；不能因此認定路線設計已合格 |
| game-ai (P0) | N/A | AI 決策政策未修改；feedback.ts:36–54 僅查詢現有 resolver |
| game-ui-ux (P1) | PASS | PlayableL03.tsx:227–231,259–273,325–335 有進度、敵方意圖、受阻狀態；既有移動高亮保留 |
| game-feel (P1) | PASS | feedback.ts:11–26、PlayableL03.tsx:141–183 有逐事件效果，未增加結算鎖；仍有零步驟呈現問題 |

Skill 的實際上游版本與閱讀紀錄由交接文件提供，本次未獨立重新讀取全部外部 SKILL.md，因此 PASS 是實作相符性判定。

B. Reference repos

| 檢核項目 | 結果 | 證據 |
|---|---|---|
| franciscobom/Grid-Tactics | PASS | 架構符合規則與呈現分離原則：rules.ts 純決策、feedback.ts 回饋查詢、React 負責播放；不表示使用其程式碼 |
| HopeMetal/2DTacticalRPGDemo | N/A | P1v6 交接未宣稱借用其實作、程式碼或素材 |
| 無核准的新引擎／相依套件 | PASS | 提交比較中未涉及 package.json 或 lockfile，呈現改動留在現有 React/SVG 架構 |

C. Playable acceptance bar

| 檢核項目 | 結果 | 證據 |
|---|---|---|
| 玩家可獨立進行完整 3–5 分鐘戰鬥 | FAIL | 缺真人獨立試玩及耗時紀錄；HUMAN_PENDING |
| 敵人依玩家狀態做出可理解行動 | PASS | rules.ts 以占位及尋路決定敵人行動，PlayableL03.tsx:259–273,325–335 提供意圖與阻擋回饋；真人理解程度待驗 |
| 玩家可以獲勝或失敗 | PASS | rules.ts 有明確成功與失敗判定，PlayableL03.tsx:367–373 有對應結果畫面；交接記錄兩種結局的自動化證據 |
| 兩種戰術選擇產生不同結果 | PASS | 現有站位與等待可以造成不同結果，原始 P0 測試及交接保留相關案例；不代表已具有足夠策略深度 |
| 可以重新開始並改變策略 | PASS | PlayableL03.tsx:128–134,367–372 的 Retry 重建初始狀態 |
| 無重複結算、卡回合、無效移動或動畫中斷問題 | PASS | PlayableL03.tsx:121–140,166–183 具備 busy/pending 防護；交接中的原始及中途取消測試均記錄為通過，但本次未重跑 |
| 1280×720、1920×1080 與基本鍵盤操作 | PASS | PlayableL03.tsx:215–220,278–288,361–365 有鍵盤控制；驗證文件記錄兩尺寸瀏覽器測試 |
| 自動化測試與真人試玩證據分開 | PASS | VERIFICATION.md:3–14,149–153 及 evidence-audit.json 明確標示 HUMAN_PENDING |

D. Project rules

| 檢核項目 | 結果 | 證據 |
|---|---|---|
| SRD 5.2.1／CC-BY、無 WotC IP、規則修改遵守契約 | PASS | 本次沒有修改規則或引入 WotC 內容；新素材有生成提示及 manifest，沒有新的規則改編。本次未進行完整歷史素材授權稽核 |
| AGENTS.md 授權範圍、未合併 main、未擅增世界觀 | PASS | fc266cb...c980e5a 改動集中於回饋、美術、測試與相關紀錄；未見規則、劇情或依賴套件修改。交接記錄未 push、PR、merge 或部署；實際授權程序未獨立審計 |

資源檢核總結： P1v6 符合限縮後的回饋與美術實作方向，但 C 項真人可玩性驗收仍為 FAIL／HUMAN_PENDING。我的正式建議維持 needs Owner，先解決已確認的零步驟回饋邊界，再以實際遊戲畫面與真人試玩判定是否接受 P1v6。
