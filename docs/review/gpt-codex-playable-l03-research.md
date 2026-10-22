# GPT web review: codex/playable-l03-research

- Reviewer: ChatGPT web, project campaign-forge (static source review; no tests run)
- Date: 2026-10-22 10:31 Asia/Taipei
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ad974e7-ed98-83ee-b272-0703cb6e528f
- Scope: main...codex/playable-l03-research (b783cf9, 00146ba, 704c106)
- Prompt: docs/review/GPT-REVIEW-PROMPT.md (no handoff file existed on this branch)
- Note: the text was transcribed from the rendered page; tables were rebuilt from the page text. Use the chat link above as the source of record.

## 1. 結論：needs Owner

這個 branch 可以作為下一階段 Gameplay 開發的研究基礎，但不能判定為可玩遊戲通過，也不建議直接合併 main。

| 項目 | 結果 |
|---|---|
| Branch 領先共同基線 | 3 commits |
| Branch 落後目前 main | 1 commit |
| Gameplay 狀態 | 有互動預演，沒有完整戰鬥循環 |
| 人工美術審查 | 未通過，仍待 Owner |
| 真人可玩性驗證 | 無 |
| 本次審查性質 | 原始碼與文件靜態審查，未執行測試 |

前兩個 commit 主要改善畫面與美術展示，第三個 commit 提出可玩化研究與規格；但可玩化尚未實作。

## 2. 問題

| 優先級 | 檔案:行號 | 問題 | 證據 | 建議修法 |
|---|---|---|---|---|
| P0 | l03Scene.ts:24–84, 86–105, 124–130 | 開閘目標與初始部署在地形上不相容 | 我方三人皆位於左岸，絞盤在 (8,1)；開閘時 (4,4)、(5,4) 不可通行，沒有另一條跨河路線 | 重新設計初始部署或加入明確的跨河途徑；驗證完整勝利路徑 |
| P0 | L03Preview.tsx:1157–1169 | 沒有敵方回合 | 下一輪按鈕只清除 acted，沒有 AI、移動、反擊或敵方目標行動 | 建立玩家回合、敵方回合、環境結算的狀態機 |
| P0 | L03Preview.tsx:1010–1020, 1157–1182 | 任務文字沒有對應的勝敗結算 | 「接應三艘船」「護送學院車隊」沒有進度或勝敗；頁尾標示無勝敗 | 為兩分支建立進度、成功、失敗、回合期限與重試 |
| P1 | L03Preview.tsx:803–857 | 移動與攻擊綁成單次演出 | 必須選人→移動→目標→確認；不能只移動、攻擊或待命；兩格目標沒有障礙或射線判定 | 拆成 Move、Attack、Support、Wait 指令 |
| P1 | L03Preview.tsx:858–878 | 戰鬥結果受動畫時間控制 | impact 時才更新位置、HP 與行動次數 | 先以純函式結算產出事件，再由動畫播放 |
| P1 | L03Preview.tsx:854–873 | 支援行動沒有資源或生命效果 | 托瑪支援只留文字；攻擊固定扣 3 HP | 加入真正的狀態變化與可預見代價 |
| P1 | artGateScene.ts:1–25、ArtGate.tsx:112–146 | 美術角色位置未連接世界座標 | ArtGate 用螢幕錨點百分比定位，不是 11×9 地圖座標 | 以同一 MapDef 驅動通行、位置、點擊與渲染 |
| P1 | l03Scene.ts:162–193 | 不可達路徑與原地操作無法區分 | movementPath() 失敗回傳 [actor]，與原地成功相同 | 改成明確的結果型別（UNREACHABLE、NO_MOVE…） |
| P2 | DEMO-CONTRACT.md:77–84 | 凱倫死亡即敗北缺乏玩法論證 | 任一我方可達成目標，卻額外指定凱倫 HP 歸零即失敗 | 保留為待驗假設，與全隊倒地才失敗比較 |

最嚴重的是 P0：地圖、任務目標與戰鬥結算尚未構成可完成的循環。

## 3. 與 Codex 說法不符之處

| Codex 宣稱 | 實際 | 判定 |
|---|---|---|
| b783cf9：interactive tactical UI candidate | 有選人、格子預覽、動畫與固定傷害，但沒有 AI、勝敗或獨立行動 | 部分成立 |
| 00146ba：audited A/B scene studies | A/B 場景已接入 React；角色仍用螢幕錨點 | 成立但有限制 |
| 704c106：gameplay-first research、demo contract、acceptance gates | 只有文件與研究記錄，沒有新 runtime | 成立 |
| COMPARISON.md：A/B/C 有非假分支 | 文件層級設計，沒有可玩實作 | 文件層級成立 |
| STORY-GATE.md：S1～S3 已完成 | 選案留給 Gavin | 未發現不符 |

另外：ui-prototype/docs/playable-l03-research/README.md:17 把 l03Scene.ts 範圍寫成 131–229，但該檔只有 195 行，應以固定 commit 的實際行號更正。沒有證據顯示 Codex 宣稱已完成新的戰鬥系統。

## 4. 遊戲性與故事觀點

比之前更像戰棋的操作展示，但還不是能完整遊玩的戰棋 RPG。戰場視覺已有實作，基本互動部分實作，戰術決策與敵方反應尚未形成循環，完整任務與勝敗重試未實作。

故事三案：A《界碑之外》適合長篇戰役；B《欠命人的遠行》讓同伴關係影響玩法；C《最後一頭守路獸》辨識度高但風險大。同意 A 有長戰役潛力，但不認為必須先選 A 才能推進玩法；過早承諾 24 關會放大未驗證機制的成本。

最值得做的一個改動：先完成一場真正可輸、可贏、可重玩的 L03 戰鬥（移動／攻擊／支援／守位、敵方干擾與追擊、船隻或車隊進度、勝敗與重試）。DEMO-CONTRACT.md 可作實作候選，但不是已驗證的平衡。要先證明：玩家會不會因敵人干擾任務而主動改變站位、行動順序與分工。

## 5. 沒檢查到的部分

未執行 build、23 項瀏覽器測試、ArtGate 11 項檢查、720p／1080p 實機畫面、視覺品質審查、AI／移動／回合模擬、兩種任務勝敗路徑、真人試玩、外部 skills／repo 授權重核、SRD 與素材逐項稽核、全 repo 逐行稽核。沒有執行 connectivity-evidence 研究腳本。

## 6. 給 Gavin 的決策

1. 是否授權 Codex 依 704c106 的 P0–P6 計畫，先用 React 做 10 小時內的 L03 可玩 Demo？（同意，限定 Demo 與獨立驗收／先縮成 60 分鐘機制 PoC／暫不授權）
2. 是否接受 Demo 暫用簡化棋盤與現有角色素材？（接受，玩法優先／必須先確認美術方向）
3. 主線故事 A／B／C 是否保持未決，直到 L03 完成最小可玩驗證？（保持未決／先選 A／B／C）

GPT 的建議：授權最小可玩 Demo、簡化美術、故事暫不定案。
