# 本輪研究驗證與實際投入

狀態：**研究文件交付；Playable L03 未實作／未試玩。** 基線00146ba，研究分支codex/playable-l03-research。來源與證據不等於正式規則核准。

## 實際完成

- 已唯讀盤點指定六份程式，另核對main.tsx與package.json；來源SHA見manifest。
- 五個指定SKILL.md按固定commit讀取；六repo的metadata／樹／LICENSE與必要核心檔、五份官方文件查閱。23份下載檔的SHA256與Git blob皆與固定樹吻合；不散布下載正文、不執行外部安裝／遊戲／引擎。
- 使用現有TypeScript只在記憶體轉譯純l03Scene模組，做忽略占位／步數上限的地形洪泛搜尋。開閘三名我方皆無法到右岸絞盤，封閘有83格連通；完整方法及資料見connectivity-evidence.json。這不是新戰鬥模擬器或勝路驗證。
- 交付差距、技術比較與各PoC規格、Demo契約、P0–P6／10h估算、工程與人類去留門檻、追加授權文字；更新UI PLAN與兩份里程碑記憶。

## 執行檢查

本地暫存研究工具位於ignored scratch/playable-research，未加入app／公開提交。以下命令為實際本機執行；工具暫存檔不是產品測試套件。

| 命令／核對 | 結果與範圍 |
| --- | --- |
| `node scratch/playable-research/manifest.mjs` | 23份固定下載檔blob／SHA吻合；五Skill版本與八份本地輸入雜湊記錄 |
| `node scratch/playable-research/connectivity.mjs` | 既有通行圖連通性；不是敵方AI／勝敗測試 |
| `node scratch/playable-research/check-research.mjs` | 文件相對連結、輸入雜湊、改動白名單、src／public／tests／dependencies／原始故事不變、10h總和；結果見validation-record.json |
| `python scripts/validate_ui_scope.py` | PASS；13份原始企劃保護、無Actions／root LICENSE、原四素材存在 |
| `git diff --check` | 通過；提交前對所有本輪檔案再檢查 |
| `git ls-remote --heads origin`＋提交與改檔路徑唯讀核對 | 發現另一AI的review分支新2115942（父9b3daaa），先停止Git寫入並回報；核對只改quality-review下六檔，與本輪docs路徑無交集，未讀寫其worktree、未合併；main仍505fca7 |

紀錄中的node／python呼叫實際使用固定絕對執行檔，未安裝依賴。執行結果依validation-record.json、Git及本輪工具輸出為準。

## 未執行／不能宣稱

本輪沒有改src／runtime依賴，沒有重跑build或瀏覽器錄製；過去ArtGate11項／L03及兩流程23項仍是歷史證據。沒有新可玩版、兩分支勝路／敗路實測、平衡、人類3–5分鐘或樂趣評估，商業美術未通過。Phaser／Godot只有來源與PoC規格，相容性、效能、桌面匯出未測。沒有新正式故事、S4、正式引擎／D&D規則決策，沒有PR／合main／部署／Actions。

原生Codex hooks callback與自然SessionEnd尚無新證據，本次正常commit/push不改變其待驗狀態；本輪交付里程碑不觸發SessionEnd紀錄。

## 時間

台北2026-10-22 00:42左右開始讀取指示；00:43:26已有來源擷取腳本時間戳；00:51:58既有連通性分析，00:59:33來源manifest，01:02:29文件與範圍核對。這是約20分鐘的研究／規格工作時窗，依工具時間戳取分鐘近似，未假造逐秒計時；Git交付另列下方。**未來P0–P6的10h不是本輪實際耗時。**

交付版本與推送結果以本分支Git紀錄及最終回覆為準，不在同一commit內預填自己的SHA或未發生的push成功。
