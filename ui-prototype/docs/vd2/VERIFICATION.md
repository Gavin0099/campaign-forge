# VD2驗收與未達標項目

VQ1的正式Owner判定是「工程驗證通過，但美術驗收未通過」。本輪Owner已選「①戰地測繪」作展示方向；**本輪整體美術品質仍待Owner人工審查**。正式故事、人物身分、職業與規則沒有定案。

## 看得到的交付

- [實際Before／After比較與兩候選](comparison.html)：固定main@0fc109f基準，兩種解析度、同一完整載入的預覽狀態；未把After回填成Before。兩張Before待命圖有材質載入不全，保留原件但排除品質比較。
- [720p實際戰鬥GIF](../../screenshots/vd2/after/combat-live-1280.gif)、[1080p實際戰鬥GIF](../../screenshots/vd2/after/combat-live-1920.gif)：移動與揮劍→光矢→護印→受擊回復。只使用真正執行中的Chromium影格，沒有預先生成戰鬥影片。
- [方向與管線](ART-DIRECTION.md)、[原創素材與原件SHA-256](assets.json)、[生成來源與提示紀錄](generation-record.json)、[實際時窗](TIME-LEDGER.md)。舊v1/v2素材原件保留。
- 原型操作：繼續旅程→營地→渡口事件→選擇→部署→戰場；上方「演出展示」可重播四種演出。Alt＋拖曳或方向按鈕平移，Fit／縮放／聚焦可用；資訊面板可收合。

## 工程與瀏覽器結果

權威結果是[來源綁定瀏覽器報告](../../screenshots/vd2/after/capture-record.json)，以及兩份recording-*.json。報告保存執行起訖、檔案雜湊、實際截圖與觀測數值；它不是人工美術評分。

| 驗證 | 可判定範圍 |
| --- | --- |
| 戰場尺寸 | 720p地面實際寬920px／71.875%；1080p約1516.7px／78.99%，均完整放入畫面。這是地面polygon的瀏覽器bounding box，不拿整個背景寬度灌大比例 |
| 格線與鏡頭 | 99地景polygon與99互動polygon逐格相同；縮放、平移、聚焦、Fit後點擊投影格正確；維持原11×9資料 |
| 真正動作 | 席恩30連通姿態輪廓，步行row1、劍擊row2、受擊row3、施法row4實際播放；不是一張站姿平移 |
| 狀態事件 | Preview及Release仍為原位置／HP6；Impact才移動、HP6→3與一次行動；同步連按確認只更新一次 |
| 撤銷與中斷 | 未確認撤銷無狀態變化；命中前取消無效果；命中後取消保留一次效果；命中前後進設定再返回均無舊確認可重播 |
| 重播與規則 | 兩法術、物理及受擊展示可重播；不改HP、位置、回合與行動次數，沒有新增正式技能 |
| 卸載 | 真正React root在動畫中卸載後，Impact與Done callback皆未執行；切畫面另走真實App操作 |
| 減少動態 | 進場前與演出中更改偏好均驗證，VFX抑制，接受的行動只套用一次；不要求觀看長動畫 |
| 既有流程 | 兩條結果後果與返回戰役；只部署莉妲、真實Tab／Enter／Space選格與確認；modal焦點循環、Esc及焦點回復 |
| 閱讀與畫面 | 720p放大文字完整流程，computed font確認新指令與確認鍵實際達18px、無橫向溢出；資訊開關、對白紀錄、四人營地顯示、比較頁載入；無pageerror／HTTP失敗資源 |
| 效能觀察 | 本機Chrome headless的idle與光矢演出RAF median／p95記於JSON。這是單機短樣本觀測，非低階PC、跨OS或商業效能認證；GIF錄製另有開銷，不能用其影格率代替原型幀率 |

額外驗證：TypeScript／Vite build、13份原始企劃保護、四份v1及八份v2原件、v3的30影格metadata、媒體及來源雜湊。治理的真實退出碼由scripts/record_governance_checks.py記錄，原生平台回呼仍另外待驗。

## 可重跑

使用既有固定版Playwright和已安裝Chrome，不下載新瀏覽器。首次瀏覽器綁定沿用tests/visual-sprint.mjs的明確--bind介面，Chrome換版須重驗bytes／SHA-256；測試前先核對安裝的執行檔。以下以本機明確路徑示例，在repo根執行：

```powershell
& 'C:/Program Files/nodejs/node.exe' ui-prototype/node_modules/vite/bin/vite.js ui-prototype --host 127.0.0.1 --port 5174 --strictPort
# 另一個本地終端
& 'C:/Program Files/nodejs/node.exe' ui-prototype/tests/vd2-browser.mjs
& 'C:/Users/daish/AppData/Local/Programs/Python/Python312/python.exe' -I -B ui-prototype/tests/encode-recordings.py
& 'C:/Program Files/nodejs/node.exe' ui-prototype/tests/verify-vd2.mjs
& 'C:/Users/daish/AppData/Local/Programs/Python/Python312/python.exe' -I -B ui-prototype/tests/inspect-animation.py --check
```

Chrome child只收縮減環境、使用repo scratch profile及暫存，路由只允許127.0.0.1。原始錄製JPEG留scratch（不提交大量暫存）；每張SHA-256與時間戳保存在公開manifest，GIF雜湊另行驗證。僅靠公開GIF不能獨立還原每張原始JPEG；重跑可重新取得真正畫面。

## 美術仍未達標／待人工

1. Owner尚未對本輪動畫、構圖與商業吸引力給出通過決定。方向選擇不能代替這項判定；不宣稱已達成熟商業品質。
2. 地形仍是平面沙盤，河岸硬轉角與材質重複可見。放大與加入測繪地標改善焦點，沒有消除全部沙盤感。
3. 完整動畫只有席恩；其他我方與敵人仍採靜態小人，未具備完整受擊、轉身或八方向動畫。正式物理攻擊目標目前靠命中弧與數字回饋，敵方逐幀受擊尚缺。
4. 30幀雖有真正姿態差異，輪廓、臉部與體積仍有生成逐幀波動；腳底錨點保持接地，但步行循環並未逐像素人工修幀，是否有足夠重量需觀看GIF人工審查。
5. 法術是即時SVG演出，尚缺音效、動態照明與全套材質反應。護印只有視覺，沒有護盾數值；沒有新增戰鬥規則。
6. 營地與四人立繪本輪沿用v2；優先花在已選戰場與席恩，未宣稱全七頁完成重新美術驗收。
7. 動作圖集完整原始提示留在本聊天imagegen tool transcript；repo保留來源ID、精確開頭與摘要，尚未獨立匯出全文。地標提示已完整落盤；這項封存限制明示，不把摘要標成逐字原文。
8. 未做陌生玩家、跨OS、手把與低階PC驗收；沒有以build、PNG數量或自動檢查數量取代以上美術問題。
9. 擷取初版未等待SVG圖片解碼，曾得到素材未完整載入的待命圖；After已補解碼等待並重新錄製／核對。Before待命原件不覆寫、明示不作評比；同狀態比較採完整載入的Preview。

本次正常commit/push是段落交付，不是自然SessionEnd。使用者已完成修正版hooks信任與重新載入；尚無原生回呼成功收據，完整治理驗收不因此變更為通過。
