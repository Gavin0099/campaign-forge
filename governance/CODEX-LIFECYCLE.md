# Codex 原生接線與驗收

此接線只適用目前驗證的 Windows 本機 Codex。框架仍固定於既有 submodule commit，未修改上游程式或將 smoke 當成最新版更新。

## 事件與責任

| Codex 原生事件 | 本 repo 的工作 | 寫入界線 |
| --- | --- | --- |
| SessionStart | 綁定 Codex 提供的 session_id、驗證 repo、載入 UI 計畫與根記憶 | 保留原始開始時間；resume/compact 不重建身分 |
| UserPromptSubmit | 執行框架 pre-task、保存 prompt 雜湊與宣告來源 | 不保存完整 prompt 或讀取平台 transcript |
| Stop | 執行框架 post-task 與兩個領域 validator | 驗證故事保護、執行證據及導入宣稱；失敗要求繼續修正 |
| SessionEnd | 執行官方 canonical closeout entry 與 writer | 真正的聊天結束才進入正式日記與 consume-once 收尾 |

前三個事件只準備收尾候選及共享文字的所有權，不執行 session_end 或 canonical daily writer。候選自動摘要只記錄本 session 實際存在的治理判定，不把模型敘述、UI 工作或歷史測試升級為已驗證成果。SessionEnd 的官方 timeout 上限為三秒，因此 submodule／候選準備在較早的事件完成。

固定版上游的 Codex closeout installer 仍使用 Stop，與本 repo 的 session-end 規則衝突；不要執行該 installer 來覆蓋本接線。另有一個 process-local 相容處理：context builder 取得既有原生 envelope，不得以 legacy writer 覆寫它。上游檔案保持原樣。

## 安裝與信任

在 repo 根目錄執行：

```powershell
git submodule update --init -- ai-governance-framework
python scripts/install_codex_governance.py
python scripts/record_governance_checks.py
```

installer 從版本化範本產生本機 `.codex/hooks.json` 與 `.codex/governance-bindings.json`。兩者含本機絕對路徑，因此不提交；程式、範本與驗收證據可提交。修改 bridge、validator 或框架程式後必須重新安裝並重新檢閱信任；不會修改使用者的全域 Codex 設定或信任資料。

Codex 要求信任「目前內容雜湊對應的 hook 定義」。使用者須在 Codex 的 hooks 檢閱介面核對並信任四個事件；CLI 的入口是 `/hooks`。專案 `.codex/` 本身也須是受信任層。installer 不會寫入信任紀錄，也不使用任何 trust bypass。現有聊天可能需要重新載入／resume 才會載入新設定。

來源：[OpenAI Docs — Hooks](https://developers.openai.com/codex/hooks)。此官方文件亦定義 SessionEnd 為聊天封存／刪除、Codex 正常關閉，或沒有 client 開啟且閒置一段時間；Stop 與 final 回覆不代表 SessionEnd。本輪使用者未要求結束聊天，因此不為了驗收而自行封存此聊天。

## 驗收層次

1. 生成設定：確認四個事件、SessionEnd 三秒上限與本 repo 根目錄。
2. 真實命令 replay：從生成的 Windows 命令輸入原生 JSON；用隔離的本地 Git 副本驗證成功、拒絕、範圍保護、環境注入、重複 Stop、resume 與收尾路徑。分類為 replay，不能聲稱平台自動觸發。
3. 消費端 smoke：fixtures 提供明確的 post-task 正向案例，要求框架確實執行領域 validator，排除先前的 null／跳過狀態。
4. 真實平台觀察：信任並載入後，須看到同一自然 session 的 SessionStart、UserPromptSubmit、Stop、SessionEnd 成功紀錄；SessionEnd 還須有有效 canonical closeout 與可核對的記憶 writer receipt。缺少任一項時，不報完整導入。

本機原始紀錄在 `artifacts/runtime/codex/<session_id>/`；原生 callback 與 acceptance replay 分別標記。`scripts/validate_task_evidence.py` 的 native_status 只提供本機 receipt 檢查，仍須與 Codex 顯示的信任／執行狀態交叉核對，不是安全 attestation。

框架 R2 使用 repo 內的共享收尾文字，同時只允許一個 session 擁有它。遇到 owner 衝突、未完成的歷史 lifecycle 或不明紀錄時 fail closed；不得刪除使用者紀錄或偽造完成 marker。導入前本輪工具生成的手動 smoke runtime 可保留到工作區內的歷史目錄，但不能改寫成自然 session 證據。

## 執行器與證據界線

本機定義固定 Python、Git、Node 的絕對路徑、長度與 SHA-256。Codex 使用明確的 Windows 命令直接啟動 isolated Python；bootstrap 先檢查自身與 bridge，bridge 再檢查 Git、合約、領域 validator 與 framework Python inventory。legacy 的 bare Git 呼叫在此短生命週期程序內映射到固定 Git，只允許列出的唯讀命令並使用環境 allowlist。子程序不繼承憑證、PATH、PYTHONPATH 或 Git repo/object/config selector。Node 僅由建置 recorder 在使用前驗證，不在原生 hook 重複計算雜湊。

最初 PowerShell 轉接版約 3.28 秒，超出平台限制，已移除；目前直接 Python 的隔離命令收尾約 2.86 秒。此數字限本機 replay，較慢的機器必須重新驗收，不能調高平台的 SessionEnd 上限掩蓋失敗。

這項綁定不取代 Codex 的 hook trust、Windows／Python 已安裝元件的信任，也不涵蓋舊 Git hooks 的所有內部執行器。新增 lifecycle 鏈不使用 ambient executable lookup；既有上游 Git hooks 仍有 ambient shell/Python 選擇，因此未宣稱整個工具鏈已達安全邊界或能阻止惡意本機程式。

完成宣稱驗證是有限的 pattern／artifact 檢查：測試與建置成功需要當前 source digest 的真實執行 receipt；正式 S4 完成、缺乏原生事件卻宣稱完整導入會被拒絕。它不代表理解任意自然語言或證明完整遊戲故事、UI 可用性、正式規則正確。
