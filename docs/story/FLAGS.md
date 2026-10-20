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

## 2026-10-21 語意修正（工作稿）

上表是原版檢查紀錄；本輪擴充驗證以 [walk.json](alignment/evidence/walk.json) 的 sourceHash 為準。每個選項邊界與終點都驗證，不變條件錯誤回傳 exit 1；刻意破壞狀態的實際 CLI 負例見 [negative.json](alignment/evidence/negative.json)。

| 狀態 | 初值 | 寫入／讀取與不變條件 |
| --- | --- | --- |
| `key_explained` | false | L01 魏德說明後 true；K1 必須已聽用途，並非已證實收魂 |
| `soul_cycle_known` | false | L07 莫瑞安／伊瑟拉對峙後 true；必須有獲救的伊瑟拉在場 |
| `notes_holder` | weide | L03 開閘→river，封閘仍 weide；L04／L06確認與 L07 搬箱撤離只改描述、不改 K1 持有狀態 |
| `starplate_holder` | tower | L07 救星盤→party，其餘→moriane；固定書庫星盤不是這個變數 |
| `isera_recruited` | false | L06_post 獲救後 true；L07 必須在隊，低信任不自動離隊 |
| `sawin_fate` | absent | L05 收留→party；L07 非護薩溫→injured，護薩溫→protected；拒收者始終 absent |
| `l07_protected` | 空字串 | L07 三個選項→quin／starplate／sawin；sawin 僅收留可選，決定被帶走者、持有者與受創 |
| `thoma_refused` | false | L07 認出碑衛後任何信任都 true；不對收魂祝聖，不改信任分數 |
| `thoma_public` | false | L07 trust_thoma >= 3 才公開作證；這個門檻在 T1 內，不是 T2 |

原旗標新增自動檢查：`wick_wall` 0–2、`maggie_alive` 本單元 true、歐朵僅 open 招募、薩溫拒收時無救援選項與復現、`l07_saved` 整數 0–6、信任整數在本單元可接受範圍（−5 至 9），名鑰函式與持有資料一致。L07 模擬多數改為 5 人＋拖延 1 人，使原有「最多六人」可達；少數仍 1 人＋拖延 1 人。這是文字戰果模擬，未制定戰棋規則。

原版實測：trust_thoma=2 有 23,040 條終端組合，3 有 25,344，4 有 6,912；原台詞可見 32,256／55,296（58.33%），未能重現「約 2%」。終端組合包含不影響信任的選項及 #sim，不是人類選擇機率。四段信任函式仍為 0–1／2–3／4–5／6+；每位同伴在本單元不必可到每段。

程式只證明列明的不變條件。角色語意、誤導感、亡魂制度的道德判讀仍要模型反例審查與人類試讀；不宣稱所有自然語言知識洩漏都可自動檢出。

| 信任狀態 | 初值 | 寫入／本單元用途 |
| --- | --- | --- |
| `trust_lis` | 1 | L01、K1、L04信件、L05收留、L07選擇；影響後續提案，任何值都不原諒 |
| `trust_thoma` | 2 | L05請他壓制裂潮＋1、L07向莫瑞安問收容禮＋1；L07公開作證門檻3 |
| `trust_isera` | 1 | K1、L06筆記／價值對話、L07；低值不自動在本單元離隊 |
| `trust_sawin` | 1 | L05收留／拒收、漿果、L07護住；缺席也保留既有歷史值，不能當已招募 |
| `trust_odo` | 2 | 本單元未加減；招募由 K1，而非信任值自動決定 |
