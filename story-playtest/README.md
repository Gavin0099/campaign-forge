# L01–L07 離線文字試讀

React 18.3.1／TypeScript 5.6.3，與既有 UI 技術一致但獨立入口，不改 `ui-prototype/`。Ink 由同一份 `docs/story/script/main.ink` 編譯；沒有第二套劇情、帳號、網路服務或正式存檔。

本次 build 已生成 `scratch/story-playtest/index.html`，直接用瀏覽器開啟。所有程式、樣式與劇情都在同一資料夾，可離線使用。

## 從乾淨 checkout 重建

Node 24.13.0／npm。依賴只裝 ignored scratch，不把 node_modules 或第三方套件整包提交：

```powershell
npm install --prefix scratch/ink-tools --ignore-scripts --no-audit --no-fund inkjs@2.3.2 react@18.3.1 react-dom@18.3.1 typescript@5.6.3 @types/react@18.3.12 @types/react-dom@18.3.1
node scratch/ink-tools/node_modules/inkjs/bin/inkjs-compiler.js -o scratch/current.json docs/story/script/main.ink
$env:INKJS = (Resolve-Path scratch/ink-tools/node_modules/inkjs).Path
node docs/story/script/check/walk.js scratch/current.json --out=docs/story/alignment/evidence/walk.json
node story-playtest/tools/build.cjs
```

本輪執行使用已驗證的絕對 Node 路徑；以上是可攜命令範例，不代表信任任意 PATH 中的程式。build 不啟動子程序，檢查依賴版本、編譯 Ink、完整 TypeScript 檢查與證據 sourceHash；舊路徑證據會拒絕使用。輸出含來源／檔案 hash manifest 及套件授權原文 THIRD-PARTY.txt。

負例測試啟動固定 Node 子程序前讀取既有主工作區的 `.codex/governance-bindings.json`（以 `STORY_BINDING` 明確指定），核對目前執行檔路徑、位元組與 SHA-256，使用 allowlist 環境，無 shell。瀏覽器驗證另以 `STORY_BROWSER_BINDING` 指定已檢閱 Chrome 綁定、`STORY_BROWSER_TOOLS` 指定既有 Playwright node_modules；不自動搜尋或安裝瀏覽器，不新增憑證。

```powershell
# 下列環境變數由本機已檢閱的 bindings／工具實際位置填寫，不從網路取得。
node story-playtest/tests/negative.cjs
node story-playtest/tests/consistency.cjs
node story-playtest/tests/browser.cjs
```

檢查詳情與退出碼見 [驗收報告](../docs/story/alignment/VERIFICATION.md)，試讀題目與來源界線見 [試讀說明](../docs/story/playtest/L01-L07.md)。匯出紀錄中的URL含 `?route=0,1,...&source=<sourceHash>`；只接受同一 sourceHash，未標版本／舊版本／無效索引會顯示錯誤並允許重新開始。

## 來源及授權

- [inkjs](https://github.com/y-lohse/inkjs) 2.3.2：MIT；[React](https://github.com/facebook/react) 18.3.1：MIT。
- [TypeScript](https://github.com/microsoft/TypeScript) 5.6.3：Apache-2.0；僅 build 工具。
- @types/react 18.3.12／@types/react-dom 18.3.1：DefinitelyTyped MIT，僅型別檢查。
- 這些授權僅適用第三方程式；不替原創故事新增 LICENSE。原創故事與文案的既有權利界線維持。
