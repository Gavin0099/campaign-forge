# spike-07 證據索引

範圍：24×18、本地 `codex/godot-spike`，W1–W8 分段 commit；沒有 push／merge／PR／stash。
所有數值為 spike 測試值。工程結果、固定 operator 統計與人工判定分開。

- [WORK.md](WORK.md)：事前目標、因果分析、所有變更值、失敗候選、命令與限制。
- [baseline/BASELINE.md](baseline/BASELINE.md)：凍結 spike06，40 種子 × 六種 operator；原 100 場逐軌跡再現。
- [ablation/ABLATION.md](ablation/ABLATION.md)：九組完整 240 場消融，單獨位置／時點及組合；保留原始 runs。
- [scout/BASELINE.md](scout/BASELINE.md)：W3 道路／側翼 80 場，法定威脅與撤退選點。
- [PACING.md](PACING.md)：W1→W6 的 policy × outcome 分層、Wilson、傷亡、輸出、增援、idle、分鐘估算與明列未達標項。
- `after/`、`baseline-recheck/`：各 240 場詳細 JSON；`baseline-reproduction.json` 全 240 場一致，`optimized-trace-reproduction.json` 的 80 場一致。
- `spike05-spot/`：24018 的 road／flank 舊版抽查。
- [PERFORMANCE.md](PERFORMANCE.md)：05／06／07 同負載三次測量，scope、render CPU／GPU、AI 納入／分離兩種表及限制。
- `perf/`：精確 export 雜湊、每幀原始資料、三次統計與原生記錄；沒有用 AVI 編碼時間充當 FPS。
- `pixels-before/after-*.png`、`pixel-diff.json`：部署／V／O 各 0 個 RGB 像素差異。
- [MOVIE.md](MOVIE.md)：AVI／PNG 的來源、固定時鐘、snapshot 與完整連續操作的區別。
- `enemy-60fps.avi`、`scout-60fps.avi`、對應 `*-strip.png`／`*-frames/`：真實可達場景續播，非整場影片。
- `win-continuous.png`／`runtime-runtime.json`：真實初始部署 flank1006 勝 T14；`lose.png`／`runtime-lose.json`：road1011 托瑪倒下。
- `bypass-before/after-T5,T6,outcome.png` 與 JSON：1014 的部分起始探針；原版 T6 無接觸勝利，新版 T5 交戰、T6 敗北。
- `scout-sequence.json`：mouse／keyboard、Esc、預覽／確認、法定安全撤退與成本；`capture-qa.json`：V／F1／B／Tab／Esc／R。
- `deployment-1080.png`、`overview.png`、`threat-legend.png`：原生執行畫面；已視覺檢查，非美術批准。
- `field-timing.json`、`hitfeel/timing-runtime.json`：無 readback 原生 normal／crit／Reduced；Skirmish 三種 setup × 三模式。
- `attacks-measure.json`／`runtime-measure.json`：無錄影、無截圖的整場勝利，43 次攻擊與 13 次敵方階段。
- `w7-exit-codes.json`、`test-run.log`、`audit.json`：真正退出碼與完整 GUT／離線稽核。
- `git-scope.json`、`changed-paths.txt`、`untracked-paths.txt`、`diff-stat.txt`、`frozen-profiles.json`：保護路徑與五套 profile blob 不變。
- `capture-source-hashes.json` 固定 W6 runtime／operator；`source-hashes.json` 為包含自身的 commit **之前**來源快照，W8 僅刷新文件雜湊。均非含自身的 commit ID。

最低效能均值門檻通過；**嚴格 60 FPS／最差幀 <33ms、斥候死亡中位數 ≥8、側翼斥候收尾領先未達標**。
完整 AI 敵方階段為 16.85／17.03ms 平均，最差 64.28／66.80ms；不能只引動畫重播的較小最差幀。
模型的相異軌跡不是獨立樣本、不是人類勝率。真人分鐘、盲玩、可讀性、公平性、SFX／手感與美術均 HUMAN_PENDING。

暫存歷史 exports 位於本 worktree 的 ignored `.godot/spike07-perf`，W7 核對後刪除；未建立或碰觸其他 worktree。
匯入會生成 `.uid`；不是影格或正式設定變更。治理 hook 僅 advisory，未宣稱 canonical SessionEnd。
