# 旗標表（L01–L07）

**狀態　S3.5 工作稿。** 名稱以 [globals.ink](script/globals.ink) 為準。「後果檢查」欄是 [check/walk.js](script/check/walk.js) 或人工審查必須成立的條件；不只檢查可到達，也檢查狀態是否合理。

| 旗標 | 預設 | 寫入點 | 讀取點 | 後果檢查 |
| --- | --- | --- | --- | --- |
| `k1_gate` | "" | L03_pre（K1） | L03 戰鬥版本、L03_post、L05_pre（歐朵）、COMPANION-ARCS 蕾絲背叛條件 | 每條路徑 L03 後必為 open 或 sealed（自動） |
| `teo_fate` | "" | L03_post | L04_post 燈芯、第三章起提歐線（待寫）、ENDINGS 蕾絲收束 | open ⇔ safe；sealed ⇔ missing（自動）；missing 不得在後續無代價復活（人工） |
| `notes_saved` | false | L03（封閘） | L04_post、L06_pre、`name_key()`、ENDINGS E2 | sealed ⇔ true（自動） |
| `wick_wall` | 0 | L01_pre、L04_post | L20（待寫）營地與瑪歌回收 | 0–2；為 0 時 L20 需有對應台詞（人工） |
| `maggie_alive` | true | L01–L04（戰敗即重來，故本單元恆為 true） | L20（待寫） | L01–L07 不得改為 false（人工） |
| `odo_recruited` | false | L05_pre | L05 觸發、P01（待寫） | 僅 k1_gate=open 時為 true（人工；以腳本結構保證） |
| `sawin_sheltered` | false | L05_pre（Q-S1） | L05_post、L06 觸發、L07 最後選項、P02（待寫） | 為 false 時 L07 不得出現「護薩溫」選項（以條件選項保證） |
| `quin_bond` | 0 | L05_post、L06_post、L07（救小昆） | 第三章燈號伏筆（待寫） | L07 前 ≥ 2（自動） |
| `quin_taken` | false | L07_choice | L07_post、第三章起（待寫） | 與 `starplate_saved` 不可同時為「小昆獲救＋星盤保住」（自動） |
| `starplate_saved` | false | L07_choice | `name_key()`、ENDINGS E2 | 見上 |
| `l07_saved` | 0 | L07_pre（拖延 +1）、L07_result（戰果，遊戲寫入；文字試玩以 #sim 模擬） | L07_post | 0–6（人工；正式由戰鬥結果寫入） |
| `trust_*` | 見 globals | 各抉擇 | 階段門檻見 COMPANION-ARCS | 蕾絲任何值都不得觸發原諒內容；托瑪底線與信任無關（人工） |
| `tide` | 1 | L04_post（2）、L07_post（3） | 章節刻度 | L07 結尾必為 3（自動） |

函式 `name_key()` = `notes_saved || starplate_saved`，是 E2 與名鑰相關對白的唯一判斷。

## 自動檢查結果（最近一次）

inkjs 2 編譯零錯誤；窮舉 55,296 條終端路徑，自動後果檢查錯誤 0。K1 × L07 保護對象 × 薩溫收留的 10 種組合都可到達。
