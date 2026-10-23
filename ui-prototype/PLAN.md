# Campaign Forge UI Prototype

> **最後更新**: 2026-10-23
> **Owner**: Gavin（需求與決策）；Codex（本輪執行）
> **Freshness**: Sprint (7d)

## Scope

獨立的 React / TypeScript 本地 PC UI 展示。原始 README、PLAN、SLICES、DECISIONS、EXECUTION、候選 A 與比較文件已閱讀。A/B/C 未選案；A 只供展示，人物外觀與地圖均是提案。不得以 UI 展示取代 S4 授權。

## Slices

### Authorized P1v6: per-event feedback and painted winch — 2026-10-23

See the P1v6 milestone at the end of this file and
`docs/playable-l03-p1v6/VERIFICATION.md`. Latest Owner authority is commit only;
the older push instructions below are historical. Five priorities implemented;
engineering evidence and human acceptance remain separate.

### Authorized P1v5: battlefield interaction feedback — 2026-10-23

使用者：以乾淨且同步的 `codex/playable-l03-research@3c95f0e` 接續，只做四項P1v5互動回饋，60分鐘上限，依序每步commit；不pull、不改rules.ts、不碰scratch worktrees、不加依賴。Owner確認本worktree無其他代理。commit後嘗試正常push，失敗留本機。

代理觀察：四步分別保存為f3aba38／0483147／c3a65ea／435c886。絞盤轉動、拉索震動、新刻度閃光、數字、2/3警示與失敗淡入；真實blocked事件的反衝、塵土、相鄰友軍阻擋火花與視覺層3px震動；原規則意圖目標脈動／箭頭流動；hover光、移動確認與落腳塵土。effects不延長busy、不改格位，skip及Reduced Motion抑制且可中途取消。規則沒有傷害或推人事件，因此不新增傷害數字或推人規則。26項純規則、53項既有browser、14項新browser皆exit0（合93項）；build、scope通過。實機截圖、失敗修正、來源雜湊與交付見 `docs/playable-l03-p1v5/` 及handoff「P1v5 feedback」。HUMAN_PENDING；共享PLAN與active_task持自有lock、不pull指示優先。這是任務里程碑，不是SessionEnd。

### Authorized P1v4: hand-painted art pass — 2026-10-22

使用者：從乾淨且已同步的 `f1e0ab6` 接續，只做 P1v4，120分鐘上限，不pull；確認同worktree無其他代理。明確允許built-in image_gen生成渡口、手繪道具、第二騎士肖像與放大角色；不改rules.ts、不加依賴、不碰scratch/p2或scratch/p0d。正常commit後嘗試push，失敗留本機。

代理觀察：單張連續手繪地景取代99格重複材質，精確配置參考約束河道，透明手繪絞盤／斷橋／車輛接入原格位，五個肖像簽名互異。4張生成原件含1張棄用寬河稿，完整Prompt／SHA留存。1.3格高實測重疊，保留失敗證據，採共同viewport幾何上限52/52=1.00，可見alpha高度0.960–0.979；既有深度排序與五點點擊測試不弱化。最終實機、79項檢查、命令exit codes及限制見 `docs/playable-l03-p1v4/`；Git結果以handoff「P1v4 art pass」為準。原規則／劇情／依賴不變，兩騎士身體仍共用舊圖，額外動畫幀未做。HUMAN_PENDING；非Owner美術驗收、非SessionEnd。共享PLAN及active_task持自有lock，使用者不pull指示優先。


### Authorized P1v3: visual pass — 2026-10-22

使用者：螢幕弱、不像遊戲、風格不一致；只做 `docs/tasks/playable-l03-P1v3-visual.md`，90分鐘上限，沿用乾淨且同步的 `7319ef0`，不pull。只用既有素材，不生圖、不加依賴、不改rules.ts與故事；不碰scratch/p2。Owner確認本worktree無另一代理。正常commit後嘗試push，失敗留本機。

代理觀察：本畫面改為較深等角投影、全強度地表貼圖、岸壁與低水面、樹木／貨物裁切、原角色放大、同源肖像卡、暗金屬框、圖示進度、路徑預覽與短促回合／抵達回饋。原有100次群聚點擊與零重疊斷言保持；P0/P0b/P0c為8/9/9項，P1v/P1v2/P1v3為26/9/9項，build／scope均exit 0。720p與1080p Before／After、失敗嘗試及完整輸出見 `docs/playable-l03-p1v3/`。字面1.2–1.5全菱形高度與零重疊衝突，保留50單位高（原26），未宣稱尺寸目標全部達成。幾何機關與單幀小人仍是限制；HUMAN_PENDING，不構成美術或正式規則驗收。共享檔持自有lock、不pull指示優先；交付不是SessionEnd。

### Authorized P1v2: battle-screen readability — 2026-10-22

使用者：只做 `docs/tasks/playable-l03-P1v2-readability.md`，60分鐘上限；從乾淨且同步的 `63a1f11` 接續，不pull。Owner確認同worktree無其他代理。規則保持不變，A僅在本畫面；commit後嘗試push，失敗留本機，不開始P2。

代理觀察：角色依實際投影腳點及橫向位置排序，縮小原圖並移除腳底透明padding；原圖檔不改。格子為唯一hit area，敵我以圓形／菱形底座及顏色區分；完整姓名在獨立資訊列隨hover／focus／點選顯示，敵人與已行動角色僅檢視，不取得行動權。新增原P0絞盤群聚與同列站位之雙尺寸實機測試、Before／After，完整結果以 `docs/playable-l03-p1v2/` 與handoff「P1v2 readability」為準。小人細節因縮小受限，真人辨識／3–5分鐘試玩仍HUMAN_PENDING；A仍THIN，未提升為玩法或商業美術通過。里程碑不是SessionEnd。

### Authorized P1v: first playable L03 screen — 2026-10-22

使用者：只完成 `docs/tasks/playable-l03-P1v-screen.md`，90分鐘上限；基線 `13a6e17`，不pull。Owner確認同worktree沒有另一代理。A（存活六回合）僅供新畫面；規則預設與P0／P0b／P0c程式、輸出保持不變。正常commit後嘗試push，失敗留本機；P0d延後，P2未授權。

代理觀察：新增主選單「Playable L03 (P1v)」與獨立React／SVG戰場，直接採用既有純規則的合法移動、敵方意圖、events、勝敗與Retry。原11×9／五單位素材、絞盤(2,1)、六回合與三格干擾可操作；逐格移動、Wait、Enter／Esc、跳過動畫、Reduced Motion與退出清理有瀏覽器驗證。最終實測、兩尺寸起始／意圖／動畫中／勝／敗截圖、exit codes、限制與Git交付狀態見 `docs/playable-l03-p1v/` 及handoff的「P1v playable screen」。A仍為THIN實驗；真人試玩與3–5分鐘節奏為HUMAN_PENDING，不宣稱正式規則、玩法或商業美術通過。里程碑不是SessionEnd。

### Authorized P0c: opt-in victory variants — 2026-10-22

使用者：只完成 `docs/tasks/playable-l03-P0c-variants.md`，45分鐘驗證；沿用 `codex/playable-l03-research` @ d42024b，不pull。Owner確認同worktree沒有另一代理。比較Baseline／A／B／C／B+ N=2及3，預設關閉、P0及P0b輸出不變，commit後嘗試push；失敗留本機，P1未授權。

代理觀察：Baseline／B／C／B+皆 **CHEESE**；A僅 **THIN**，是本輪建議保留比較的候選，並非採用。A第一回合站位後等待5勝／6791敗，至多一次移動0勝／217敗，原P0守點仍勝；最低已找到3人3次8格，單／雙人於P0b有限搜尋未找到勝法。B與B+均有蕾絲一人兩次4格後等待的廉價解；B可最後回合才守點。5／6回合、每回合及全場至多兩次移動的完整有界搜尋結果與上限、陣容cap、可重播trace、兩次一致性與exit codes見 `docs/playable-l03-p0c/` 和 `../docs/handoff/codex-playable-l03-research.md` 的P0c章節。沒有改預設、UI、美術、正式故事／規則，沒有真人樂趣或Owner接受證據。里程碑不構成SessionEnd。

### Authorized P0b: stance validation — 2026-10-22

使用者：本輪只完成 `docs/tasks/playable-l03-P0b-stance.md`，保存搜尋、站位／平手測試，補 `walkable()` 邊界、更新handoff與正常commit／push；P1未授權。14:51確認同worktree沒有另一工作session，可繼續寫入。

代理觀察：結論 **CHEESE**。全6796種第一回合結束站位、之後只等待，493勝／6303敗；最低1人移動1次3格。五回合最多移動一次217策略，6勝／211敗；蕾絲第二回合(1,3)→(0,3)後等待，進度2勝利，僅1人1次1格。移除其他同伴的三個單人與三個雙人陣容均找到可重播勝法（每回合至多一個移動指令的有限搜尋，不是完整策略勝率）。五種站位、敵人爭格／平手／順序與bounds回歸已保存；只改一行明確矩形邊界，未調整規則或地圖。完整命令、exit codes、提交與推送狀態見 `../docs/handoff/codex-playable-l03-research.md` 的 P0b stance validation。調整均為提案，未開始P1；沒有UI、人類試玩、樂趣或完整兩路線驗收。

### Authorized P0: west-bank winch rules PoC — 2026-10-22

使用者本次只授權 `docs/tasks/playable-l03-P0.md` 的60分鐘純規則PoC，並要求合入origin/main的協作文件、commit及正常push；P1–P6仍未授權。這取代下方研究階段的P0未開始狀態，不改正式故事。

代理觀察：獨立 `src/playable-l03/rules.ts` 重用11×9地形，絞盤(2,1)，同一固定西岸部署；移動驗證、兩名騎士阻擋／繞路、階段開始時計進度、5回合存活／3進度失敗及重試皆可同步結算。8項Node檢查通過：守點成功(進度1)、不動失敗(進度4)、重試換策略成功，三份trace逐byte重播相同；禁止穿越存活單位預設開啟仍有解。Build與scope通過。封閘僅地圖可達，沒有護送勝敗、UI、傷害或新增美術；QR-11未解、真人可玩性未驗。交接見 `../docs/handoff/codex-playable-l03-research.md`；P0完成即停止，不自行接P1。

### Gameplay First / Playable L03 Research — 2026-10-22

使用者要求先研究與實作規格，暫不實作新規則、不安裝引擎、不動其他AI worktree、不合main。B美術保留候選，不代表人工通過。研究基線00146ba，成果見 [docs/playable-l03-research/README.md](docs/playable-l03-research/README.md)。

- R-01：六份指定UI／演出程式盤點、五個指定Skill按固定commit讀取，六個公開repo版本／LICENSE與官方文件查核；23份下載檔核對Git blob／SHA256，未安裝或搬入外部實作。
- R-02：現有純地形的唯讀連通性分析確認開閘三我方均不能到右岸絞盤；記錄方法、SHA與結果，未把它稱為戰鬥驗證。
- R-03：建議先沿用React＋SVG；列Phaser／Godot隔離PoC規格、Demo狀態機／獨立行動／兩種AI／接船與護送目標／勝敗Retry、10h未來估算、工程與人類keep/kill/refactor驗收、最小追加授權。
- 研究文件已備；P0–P6 Gameplay實作全為NOT_STARTED、需Owner追加批准。兩分支可勝性、平衡、3–5分鐘真人試玩與樂趣尚無證據，正式故事／G004／G005／S3／S4不變。

### L03 Art Quality Gate — 2026-10-22

Owner 明確拒絕 `codex/l03-battle-ui@b783cf9` 商業美術品質；23項工程 PASS 不能抵消。另開 `codex/l03-art-quality-gate`，先做實際 Skill 路徑／版本／SHA／規則對應審查，再交付同一 K1 抉擇前狀態的 A手繪奇幻／B立體造型兩套可執行靜態樣板。B 是預繪2.5D外觀，沒有3D模型。原操作頁保留，不合併 main，不進動畫／規則／量產。

- AG-01：四份 Skill 本輪實際讀取及摘要留存；dnd-framework 只在故事分支，唯讀引用。上一輪完整遵循證據不足，不補作歷史證明。
- AG-02：新整體渡口繪景／造型候選，三船、三箱、提歐的燈、瑪歌、群眾、閘門與洪水同時可見；原件與四份提示留存，不重用舊 terrain／props。B 角色為相同五人造型轉換，非新角色。
- AG-03：原React入口、A/B共用固定資料、獨立人物、接地影與橋欄固定遮擋、靠邊HUD、七地標檢視／Esc／大字／返回焦點整合。新圖尚未接回11×9導航／技能，不把靜態樣板說成完整戰鬥改版。
- AG-04：A/B各720p／1080p真實截圖，新樣板11項檢查、原L03與舊兩流程23項回歸、build與範圍保護通過；歷史Before不覆寫。詳見 [docs/art-gate/VERIFICATION.md](docs/art-gate/VERIFICATION.md) 及來源綁定報告。
- 商業美術仍待Owner選A／B或拒絕兩案。固定角色立牌感、閘門水利拓撲、NPC／船分層、新地形走格對齊、素材邊緣與原生1080p列為未達標；動畫Gate未進入。實際投入見TIME-LEDGER，不將9.5／12小時舊預算寫成實際時間。

### L03 戰鬥畫面與 UI 追加（2026-10-21）

使用者指出故事試玩交付沒有修改戰鬥畫面，明確追加「戰鬥畫面和 UI 也要改」。上一輪十二小時計畫原限定規格，本輪另開 `codex/l03-battle-ui` 自 `main` 505fca7 實作候選，不合併 `story/strengthen-narrative`，不作 G004／G005 定案。

- 新增可直接進入的 L03 渡口閘門，開／封閘切換、同源99格、實際路徑繞障、斷橋禁行、目標／損失與確認預覽。
- 新繪三名隊員／兩種敵方手繪透明圖集；同一人物素材用於戰場、隊伍與選取資訊，舊人物圖集與原稿保留。
- 凱倫盾劍／蕾絲繩索以固定−3操作示例表達；托瑪只有支援標記，無治療、資源／集中或正式技能實作。
- 戰地測繪版面、720p常駐確認區、1080p與放大／窄屏實測。原兩完整路線、單人莉妲與取消／卸載納入回歸。
- 驗證結果、實際時窗、提示與已知限制以 [docs/l03/VERIFICATION.md](docs/l03/VERIFICATION.md) 和來源綁定 capture-record 為準。功能通過不代表重量感、商業美術或人類可用性驗收。

### VD3：D&D Combat Identity & Animation Quality Gate

Owner 已判 VD2 美術未通過，工程歷史保留。目標9.5小時／上限10小時，以實際投入計算。範圍：官方SRD能力參考、動畫管線比較、非魔法近戰與獨立測試法師的三枚Magic Missile、雙解析度實機錄影與狀態驗證；不定故事、職業與正式規則。實作與證據交付完成；工程功能通過，動畫重量感與商業美術品質尚未獲Owner核准。決策、來源、工時及未達標項目見 docs/vd3/。

- VD3-01：官方SRD5.2.1七項候選能力與職業／條件／資源對照，保留CC BY4.0聲明與遊戲內來源頁；沒有把席恩改成法師。
- VD3-02：製作動作前比較生成逐幀、固定2D部件與長期3D成本；採用固定部件／骨架錨點，原30幀PNG與全部原件保留。
- VD3-03/04：非魔法近戰的準備／出手／接觸／hitstop／敵人實際後仰／恢復，以及獨立測試Wizard的三飛彈凝聚、單／多目標與同步命中。兩段不增正式規則。
- VD3-05：22項實機檢查通過，近戰與法術各10次連播、真實React卸載、Impact一次更新、取消／切畫面／Reduced Motion、兩完整分支及缺席鍵盤流程；720p／1080p共四段實機錄製與同狀態比較，來源及媒體雜湊核對。保留紙片感、次動作、量產與整體畫風待審，沒有自行判美術通過。


### Visual Direction 2.0 & Combat Animation Sprint — 2026-10-20

使用者判定上一輪為「工程驗證通過，但美術驗收未通過」。本輪預算9.5小時、上限10小時，以實際投入記錄；維持11×9與固定數值、兩分支及缺席角色流程。可自主接續並正常commit/push。

使用者已比較兩張實際戰場候選並選擇「①戰地測繪」深入打磨；這是本輪展示方向核准，不是故事選案、正式世界觀或最終美術品質通過。

- VD-01：全寬戰場、可收合資訊、Fit／Zoom／Pan／Focus；實測720p地面寬71.875%、1080p78.99%，99格與點擊區一致。
- VD-02：同狀態兩套候選已交付；深化戰地測繪的紙金、封蠟紅、裂潮青、界碑與測繪器具。
- VD-03：席恩30張真正姿態影格、腳點錨定、待機／步行／揮劍／受擊／回復；其他角色仍靜態，未冒稱全員動畫。
- VD-04：即時光矢、護印與受擊展示；不加入正式職業、規則或數值效果。
- VD-05：RAF時鐘與遊戲狀態分離，Impact套用一次，取消／Reduced Motion／切畫面／React卸載通過瀏覽器檢查；補強命中後進設定的舊預覽重複確認風險。
- VD-06：720p／1080p真實錄製、同狀態比較及來源綁定報告備齊；兩分支、莉妲單人鍵盤與閱讀設定通過。最終Owner美術待審，平面河岸、生成幀波動、其他角色仍靜態列為未達標，沒有稱商業美術驗收通過。

前輪報告保留為歷史，不能充當改版後來源綁定的驗證。新交付集中在docs/vd2/、screenshots/vd2/。

### Visual Quality Sprint — 2026-10-20 使用者授權

9.5 小時預算、10 小時上限；以實際投入記錄，不等待逐片確認。保留全部既有流程與固定示範規則，僅候選 A 展示美術；不選案、不執行 S4。完成段落沿用正常 commit/push 授權。

- VQ-01：完成官方競品研究、Benchmark Matrix、Art Direction、10張同狀態 Before。
- VQ-02：完成四人透明立繪、明確裁切與辨識規格；人工人物品質待審。
- VQ-03：完成五種小人、相同色塊與道具、圖集邊界檢查；風格一致性人工待審。
- VQ-04：完成渡口材質／道具、手繪近景及99格地景／互動幾何比對，原11×9資料未改。
- VQ-05：完成生命比例、選取邊線、移動虛影、確認位移及局部−3；720p預覽與操作重排。
- VQ-06：13項真實瀏覽器檢查、綁定After／範圍／縮圖及比較頁；功能與視覺技術通過，商業美術品質人工待審。

證據集中於 docs/visual-sprint/ 與 screenshots/visual-sprint/。視覺技術檢查、功能驗證及人工美術審查分開；既有 Codex 平台信任／自然回呼仍待驗。

- UI-01：流程、資訊層級、資料分離、風險界線完成。
- UI-02：主選單、六章24節點示意、營地人物、劇情抉擇完成。
- UI-03：隊伍部署、戰場、選角→移動→技能→確認及撤銷完成；規則固定示範。
- UI-04：選擇延續到支援、目標、同伴與戰後結果完成。
- UI-05：四位人物、五種戰場小人、渡口場景與戰役地圖已整合；實際驗收記錄見 docs/VERIFICATION.md。

## Design

視覺重心是人物與戰場。成熟低飽和奇幻插畫、羊皮紙地圖、低調金屬框，繁體中文。人物立繪與小人獨立生成；敵我用 ◆／▲、文字及色彩一起區分。24節點是容量示意，後續章名與路線不揭露。

## Decisions

- 使用 React 18 / Vite 4 / TypeScript 5.6，僅介面驗證，不指定正式引擎。
- 遊戲資料在 src/data.ts，素材路徑在資料設定中維護。
- 無正式儲存，狀態在本次頁面生命週期保留；重設按鈕明確清除。
- built-in image_gen 生成原創展示素材。使用者本輪授權的官方競品截圖只存scratch研究，不進app或公開提交。
- domain / risk 由使用者授權代填為 game-ui-prototype / low。

## Risks and pending decisions

正式故事、角色身分／外觀、地圖地理、職業／技能、勝敗判定、戰鬥數值都待選案與設計。手把只有映射提案。尚無外部玩家可用性測試與正式平台相容性測試。

Visual Sprint已知限制：平面沙盤／河岸方格感、材質重複、靜態小人姿態、12–14px戰鬥metadata的真人閱讀舒適度。沒有用build或代理自評宣告商業美術品質通過；人工檢查見docs/visual-sprint/VERIFICATION.md。實際時間以TIME-LEDGER.md記錄，不把9.5小時預算填作實際工時。

## Verification

最新研究只核對來源／文件／既有程式不變與故事範圍保護，未進行新玩法實機或人類試玩；詳細命令、結果及實際投入見docs/playable-l03-research/VERIFICATION.md。下方Art Gate等是歷史版本工程證據，不能當Playable L03通過。

目前最新為 Art Quality Gate：靜態樣板工程與既有功能回歸通過；Owner美術待審，b783cf9美術已明確FAIL。原L03／VD3等報告為各版歷史，不能代表本輪新場景完整導航／動畫通過。原生hooks callback證據仍待驗，信任／reload不再要求重做。

最新VD3：功能與實機證據見docs/vd3/VERIFICATION.md及其來源綁定report；VD2／VQ1報告僅保留歷史。使用者已確認0fc109f修正版hooks重新信任與重新載入，該步驟不再待辦；平台原生事件仍無成功收據。下方「需重新信任」為歷史。

2026-10-20 最新平台確認：使用者已完成信任／重新載入，並確認四事件已信任／啟用、無錯誤；本機綁定核對一致，但尚無原生回呼收據。後續重驗發現 SessionEnd 曾達3.39秒，超過平台三秒限制；本輪改為一次 Git 身分查詢，單一 hook 程序內重用已驗證的 consumer root，保留每次路徑核對、完整 envelope／guard／writer 檢查，延後非本事件的 import。新增跨 root 偽造 envelope 拒絕測試及三個全新 session 的計時樣本。結果以 artifacts/governance-native-acceptance.json 為準；失敗原件保留為 governance-native-timeout-regression.json。此次程式修正改變 hook 定義雜湊，須重新檢閱信任修正版，再驗證平台實際執行與自然 SessionEnd／canonical writer；不是否定使用者已完成前一版本的信任。

建置、範圍保護與 CUA 實際瀏覽器流程；保留 screenshots 與 docs/VERIFICATION.md。先前環境已於正常交付驗證 Git hooks；本輪已補四事件 lifecycle 程式與隔離 replay，Codex 信任及自然回呼仍待驗，不得稱完整自動治理。

2026-10-20 Windows 工作副本：恢復固定框架並安裝本機 hooks；UI 治理 smoke 改用 repo runtime root 與明確的 UI 計畫，不再依賴符號連結。readiness 17/17、drift、hook 安裝檢查與 UI runtime smoke 通過；證據及本機交付界線見 governance/ADOPTION-STATUS.md。本輪僅處理治理，未修改 UI 行為或重新宣稱瀏覽器驗收。

2026-10-20 治理補線：SessionStart／UserPromptSubmit／Stop／SessionEnd 分工、故事保護的 hard stop、執行證據及完整導入宣稱檢查已實作。Stop 不作正式收尾，SessionEnd 經 canonical entry 執行；設定為本機產生，須由使用者檢閱信任。本輪不改故事、UI 行為或 S4 狀態。

## P1v6 feedback and winch — 2026-10-23

Owner instruction: execute the five P1v6 presentation priorities on the existing
`codex/playable-l03-research` branch, commit each step, then verification and
handoff; **commit only, no push**. Gavin confirmed this is the only session in
this worktree. Rules, outcomes, dependencies and story remain outside this change.

Implemented per-event feedback on the existing path-step clock, counterfactual
contact checks using the unchanged resolver, independent landing lifetimes,
static broken-chain markers, and two built-in image_gen atlases (four painted
winch frames and slack/taut rope). The rule state still settles once in finish;
the final landing shares that boundary rather than adding an animation lock.
Skip and Reduced Motion cancel transient cues; static blocked state remains.

Actual screenshot review found the warning filter exposing adjacent atlas
frames. The correction filters pixels inside explicit SVG viewport clipping.
The failed timing capture and visually defective first verification remain in
`docs/playable-l03-p1v6/attempts/`; generation itself had no rejected attempts.
Current commands, source-bound execution evidence and actual 720p / 1080p
captures are documented in `docs/playable-l03-p1v6/VERIFICATION.md`.
Human playtest remains HUMAN_PENDING; no Owner art acceptance is claimed.
