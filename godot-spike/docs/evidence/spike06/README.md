# spike-06 evidence index

Owner2026-10-26 19:17授權；24×18 balance/deployment/scout/flash0.5，
僅本地W1–W8 commits。全部數值為spike測試值，無新美術、正式設定或32×24。

| 證據 | 用途與限制 |
| --- | --- |
| [WORK](WORK.md) | 預先固定門檻、根因／單槓桿試驗、每項before→after與保留失敗 |
| [Baseline](baseline/BASELINE.md) | 20 seeds×5 policies；24018重現舊8/7/6/9敗局，100組全敗 |
| [Old recheck](baseline-recheck/comparison.json) | W6再次100組逐一核對W1 trace／commands／outcome／metrics |
| [PACING](PACING.md), [targets](targets.json) | 各策略前後表、傷亡、職業、閒置群組、援軍／LOS；flank70%勝率但15–25min全面區間門檻FAIL |
| [Final runs](after/aggregate.json) | 100組JSON；seed24018與1001–1019，非隨機傷害，無部署jitter |
| [PERFORMANCE](PERFORMANCE.md) | 獨立未錄影720p效能／41次攻擊；平均影格明顯退步，無穩定60FPS宣稱 |
| [MOVIE](MOVIE.md), [index](movie-index.json) | ffmpeg缺席→Godot native AVI＋Pillow PNG strips；60 simulation FPS不是實際GPU FPS |
| [Enemy strip](enemy-wave-60fps-strip.png) | 援軍實際出手；同名AVI，從真實可達snapshot續播，非整場連續影片 |
| [Scout strip](scout-flank-finish-retreat-60fps-strip.png) | parsed滑鼠／Esc／Enter側移→收割→撤離；同名AVI，snapshot-scout.json與scout-sequence.json |
| [Deployment](deployment.png), [1080p](deployment-1080.png) | native執行畫面；既有stand-ins與terrain placeholder |
| [Midbattle](route-midbattle.png), [wave](reinforcement-engaging.png) | 連續初始部署實際操作，不編造HP／地形 |
| [Warning](warning.png), [arrival](arrival.png) | T4預告／T5到場；東側渡口入口，出生回合休息 |
| [ZoC](scout-zoc-preview.png), [finisher](scout-finisher-hit.png), [retreat](scout-retreated.png) | 紫色鄰格控制、半血收割＋1、攻後最多2成本撤離 |
| [Threat legend](threat-legend.png), [overview](overview.png) | 六色圖例／15px群組標籤；基本可讀性模型檢視，真人待驗 |
| [Continuous win](win-continuous.png), [lose](lose.png) | 初始部署一路操作，flank24018勝T13／road1001敗；非終局fixture |
| [Flash comparison](hitfeel/impact-strip-spike05-vs-spike06.png) | normal／crit contact±8，四套native AVI／contact still；field-melee-hit.png |
| [Timing](hitfeel/timing.json) | 三Skirmish setups×normal／crit／Reduced；固定模擬時鐘與獨立real-time wall分列 |
| [GUT](test-run.log), [exits](w7-exit-codes.json) | 最終完整回歸；歷史147測試保留，新增harness／balance／wave／scout／profile |
| [Scope](git-scope.json), [paths](changed-paths.txt), [stat](diff-stat.txt) | base6ee5cb7；brief是W1前既有的唯一project外變更 |
| [Audit](audit.json), [hashes](source-hashes.json) | 工作樹bytes與normalized-LF SHA256；排除self-hash與audit stdout，W8文件後刷新 |
| [Capture freeze](capture-source-hashes.json) | W6 runtime/data/config/scenes/shaders/GDScript operators；W7/W8不再改runtime |

W2與W4各候選、失敗parse／fixture測試及包裝stdout鎖定失敗均保留。
`attempts/`與WORK分開標明，不以歷史失敗當最終驗收。
PowerShell UTF16／ANSI／尾空白只做格式正規化，錯誤內容保留。

確定性變動：AI原有微量seed tie-break；policy同職業順序／同分目標的seed hash。
24018保留歷史順序。W1每20條distinct road10/flank9/turtle14/retreat9/bypass8；
W6為20/20/12/14/10，非20次重印同軌跡。此分布不是玩家勝率抽樣。

實際field adapter向來直接使用flash_mix，沒有把crit_flash_multiplier乘入亮度。
故field normal與crit實際峰值均.6→.5；.5×1.2=.6只是profile理論乘積。
Skirmish crit multiplier作用在fade時長。未為迎合舊文件錯誤改adapter。
固定60Hz模擬輸入就緒≤1.7s，但其wall normal／crit在此PC會超過1.7s；
獨立無錄影real-time九組全≤.928s。兩種時鐘不可互相替代或隱去。

唯讀固定版本skill方法（未安裝、未複製程式／美術）：

- [prototype-fast](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/workflows/prototype-fast/SKILL.md)：先訂keep/discard與可量測門檻。
- [level-design](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/level-design/SKILL.md)：先驗部署／路線與反制空間，記錄失敗試驗。
- [game-ai](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ai/SKILL.md)：顯式狀態、pure rules、事件播放、確定性。
- [game-ui-ux](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-ui-ux/SKILL.md)：preview／hover／合法性共源，圖例與native輸入證據。
- [game-feel](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills/disciplines/game-feel/SKILL.md)：接觸幀比較、保留其他層、分開輸入延遲與錄影效能。

本機external-executable-trust-audit：Owner指定完整執行檔與離線工具不啟動子程式／網路，
不宣稱完成PATH／DLL／繼承環境的整體信任根稽核。sandbox解析需escalation；
正常commit metadata位於共用.git也需escalation，未改全域trust或bypass hooks。

HUMAN_PENDING：Gavin先不讀攻略盲玩road／flank／turtle，記實際分鐘／傷亡／困惑／勝敗原因，
再評斥候與援軍理解、鏡頭舒適度、0.5閃白、圖例及聲音。自動勝利不是人類遊玩或Owner批准。
本段不執行canonical SessionEnd、不改共用PLAN／memory、不push／merge／PR／stash／部署。
