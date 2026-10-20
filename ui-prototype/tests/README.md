# 視覺與流程驗收

`npm ci --prefix ui-prototype` 安裝包含固定版 Playwright 的開發依賴。不需要付費瀏覽器服務或下載專用 Chromium；使用明確綁定的既有 Chrome。

在 repo 根目錄，先啟動 `npm run dev --prefix ui-prototype -- --host 127.0.0.1 --port 5173 --strictPort`。使用本機 Node 執行：

```powershell
node ui-prototype/tests/visual-sprint.mjs --bind 'C:/Program Files/Google/Chrome/Application/chrome.exe'
node ui-prototype/tests/visual-sprint.mjs
```

`--bind` 明確記錄所選瀏覽器的絕對實際路徑、長度與SHA-256至被Git忽略的 `.codex/visual-browser-binding.json`。每次測試在載入Playwright與建立profile前核對；瀏覽器更新後須檢查並重新綁定。不透過PATH搜尋Chrome；browser child使用縮減環境，profile及暫存限repo的scratch，封鎖非loopback請求。

測試真正點擊或鍵盤操作React畫面；報告位於 `docs/visual-sprint/browser-results.json`，After截圖位於 `screenshots/visual-sprint/after/`。Before保留基準提交的10張原始截圖，不由After測試覆蓋。測試會重設頁面記憶體展示狀態，沒有正式存檔。

執行後可用 `npm run test:evidence --prefix ui-prototype` 核對目前程式／素材與29張截圖。`python ui-prototype/tests/verify-art.py`另檢查原件、尺寸、雜湊與圖集透明分界；本輪既有Python3.12／Pillow12.2.0環境，沒有寫入或重新繪製圖像像素。

`python ui-prototype/tests/verify-governance.py`核對目前來源與已執行的治理驗收紀錄；它不重新執行lifecycle，也不把replay升級為平台原生事件。要重跑治理／scope／build使用repo根的 `scripts/record_governance_checks.py`。

包含99格地景／互動幾何對齊、原地形、兩條結果路線、缺席同伴、撤銷與確認、固定效果3、回合重設、modal焦點與Esc、放大文字、reduced motion、四人展示、HTTP及page errors。不是正式戰鬥引擎測試或人類美術審查。
