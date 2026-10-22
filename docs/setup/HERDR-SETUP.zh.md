# 在 herdr 裡同時跑 Codex 和 Claude（campaign-forge）

適用：DESKTOP-EJOULKM、herdr 0.9.5、Codex 與 Claude 整合已安裝。以下 herdr 指令都取自官方文件（herdr.dev/docs/quick-start、/docs/cli-reference、/docs/agents、/docs/session-state、/agent-guide.md）。

## 0. 開始前

1. **規則檔要先在 Codex 的工作資料夾裡**：Codex 開機時讀 `D:\campaign-forge\AGENTS.md`；Claude 從 `scratch\quality-review` 往上找，會讀到 `D:\campaign-forge\CLAUDE.md`。所以 `AGENTS.md`、`CLAUDE.md`、`docs/handoff/TEMPLATE.md` 要先 commit 到 main，再合進 Codex 目前的 branch（見步驟 3）。
2. **關掉舊的 Codex**：同一個工作資料夾只能有一個 agent。先關掉還開著的 Codex 桌面版和舊的 Codex CLI 視窗。

## 1. 開 herdr

開一個新的 PowerShell 視窗：

```powershell
cd D:\campaign-forge
herdr
```

第一次會出現導覽；沒有 workspace 時 herdr 會自動建一個。

## 2. 命名 workspace，建立三個 tab

在 herdr 第一個窗格裡輸入（每個指令都會回傳 JSON，從裡面抄 id）：

```powershell
herdr workspace list
herdr workspace rename <workspace_id> campaign-forge
herdr tab list
herdr tab rename <tab_id> codex
herdr tab create --cwd D:\campaign-forge\scratch\quality-review --label claude
herdr tab create --cwd D:\campaign-forge --label logs
```

也可以用滑鼠：在畫面上按右鍵開選單建 tab，或按 `ctrl+b` 放開再按 `c`。`ctrl+b` 放開再按 `n`／`p` 可以切到下一個／上一個 tab。

## 3. 在 logs tab 準備 Codex 的 branch（只做一次）

點 `logs` tab：

```powershell
git fetch origin
git status -sb
git merge --no-edit origin/main
```

`git status` 要顯示 `codex/playable-l03-research` 而且沒有未存的修改，才能 merge。之後的 dev server 和測試也都在這個 tab 跑。

## 4. 啟動兩個 agent

- 點 `codex` tab，輸入 `codex`。
- 點 `claude` tab，輸入 `claude`。如果 Claude 問你要不要允許載入上層資料夾的 `AGENTS.md`，選允許。進去後輸入 `/memory`，確認清單裡有 `D:\campaign-forge\CLAUDE.md` 和 `AGENTS.md`。

左邊側邊欄會顯示每個 agent 的狀態：`working` 是在做、`blocked` 是在等你回答、`done` 是做完還沒看、`idle` 是可以給下一個指令。

在 logs tab 查狀態：

```powershell
herdr agent list
herdr integration status
```

想讓名字比較好認，可以從 `herdr pane list` 找窗格 id，再輸入 `herdr agent rename <pane_id> codex`（Claude 那格改成 `claude`）。狀態看起來不對的話，輸入 `herdr agent explain <pane_id>`。

## 5. 離開與回來

- **暫時離開**：按 `ctrl+b`，放開，再按 `q`，或直接關掉視窗。agent 會繼續跑。
- **回來**：開 PowerShell 輸入 `herdr`。
- **只看某一個 agent**：`herdr agent attach codex`，用 `ctrl+b` 放開再按 `q` 離開。
- **全部停掉**：`herdr server stop`。注意這會結束所有窗格裡的 Codex 和 Claude，不要在它們工作中途執行。

## 6. 試驗：Claude 審查 `codex/playable-l03-research`

先貼給 Codex，等它回報 push 完成、側邊欄變成 `done` 或 `idle`，再貼給 Claude。

### 貼給 Codex

```text
依 AGENTS.md 的「Multi-Agent Coordination — 2026-10-22」做一次交接試驗。這次不要改任何程式、美術或故事檔。
1. git fetch origin，確認目前在 codex/playable-l03-research、工作區乾淨。
2. 先把這個 branch（包含剛合進來的 main）push 到 origin/codex/playable-l03-research。
3. 依 docs/handoff/TEMPLATE.md 寫 docs/handoff/codex-playable-l03-research.md，說明這個 branch 相對 origin/main 改了什麼（b783cf9、00146ba、704c106）。「How to verify」只列你這次實際跑過的命令和 exit code，沒跑的寫 NOT RUN。
4. 只 commit 這個檔案，push 到同一個 branch。不碰 main、不開 PR、不 force push、不用 --no-verify。
5. 回報 push 後的 HEAD SHA，然後停下來，等我下一個指示。
```

### 貼給 Claude

```text
依 CLAUDE.md 審查 Codex 的 codex/playable-l03-research。
1. git fetch origin，確認這個工作資料夾（scratch\quality-review）乾淨。
2. git switch -c review/playable-l03-research origin/codex/playable-l03-research
3. 讀 docs/handoff/codex-playable-l03-research.md 和 git diff origin/main...origin/codex/playable-l03-research。
4. 自己跑交接檔「How to verify」裡的步驟，記下命令和 exit code。跑不了的標 NOT RUN 並說明原因。
5. 把結果寫到 docs/review/codex-playable-l03-research.md：結論（pass／fail／needs Owner）、P0–P2 問題（附檔案:行號和證據）、跑過的檢查、沒檢查的部分、要問 Codex 和要問我的問題。
6. 只 commit 這個審查檔，push 到 origin/review/playable-l03-research。不改 ui-prototype 的程式、不碰 D:\campaign-forge 主資料夾、不 merge main、不開 PR。
7. 用中文回報結論和最重要的三個問題，然後停下來。
```

### 你最後要看的

- `codex/playable-l03-research` 上的 `docs/handoff/codex-playable-l03-research.md`
- `review/playable-l03-research` 上的 `docs/review/codex-playable-l03-research.md`

要不要合併進 main，由你決定。
