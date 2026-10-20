# Visual Quality Sprint 驗收

2026-10-20；基準 `main@6f5109e`。候選A展示美術提案，故事仍停在S3。

**功能測試通過、視覺技術檢查通過；商業美術品質仍需人工審查。** 沒有陌生玩家測試或Gavin美術核准，不能宣稱已達到成熟商業作品品質。

## 已交付

- [Benchmark Matrix](BENCHMARK.md)、[Art Direction](ART-DIRECTION.md)、[官方來源與截圖雜湊](reference-sources.json)。官方HTML與圖片研究副本留在被忽略的scratch，原型與公開提交不含競品素材。
- 四位透明立繪、五種戰場小人、四種地表材質、樹叢／渡船／糧箱及手繪渡口對話近景。v1原件與三份被取代的v2草稿全部保留。
- [初次提示](generation-prompts.json)、[圖集與材質生成迭代](generation-iterations.json)、[場景手繪修整](scene-refinement.json)、[素材原檔雜湊與尺寸](art-manifest.json)。
- [互動Before／After比較頁](comparison.html)，可選營地、對話、部署、待命與預覽及兩種解析度；原始PNG位於 `../../screenshots/visual-sprint/`。
- 原11×9地形與互動格共用投影；直立小人、生命比例、選取邊線、目的地虛影、確認位移與局部−3回饋。兩個選擇的代價與後果保持原資料。

## 可重複執行的功能驗收

[browser-results.json](browser-results.json) 記錄本機Chrome的真實React操作、13項檢查、輸入檔雜湊及29張綁定截圖，包含移動／技能範圍。另有比較頁PNG。執行方式見 [tests/README.md](../../tests/README.md)；`verify-evidence.mjs` 會拒絕與目前程式／素材不符的舊報告。

| 檢查 | 結果與證據 |
| --- | --- |
| 1920×1080、1280×720 | 兩種尺寸均走完整居民路線，保留同狀態待命／預覽與確認回饋 |
| 兩條結果 | 居民分支保留補給缺口／奧倫立場；軍糧分支保留失散者／莉妲尋人要求；均返回戰役 |
| 缺席角色 | 軍糧路線只部署莉妲，席恩與奧倫不在戰場，仍完成主線展示 |
| 未確認與撤銷 | 預覽時原角色未移動、追兵HP仍6；撤銷無位置／HP變更，確認鍵恢復停用 |
| 確認與回合 | 確認才移動並套用固定3；追兵6→3；結束回合恢復可行動狀態 |
| 地景／格線 | 99個地景polygon逐格與互動polygon的座標、地形一致，另比對原9列資料 |
| 720p操作 | 目標預覽不被按鈕覆蓋；確認鍵在視窗內；撤銷鍵不被面板裁切；無橫向溢出 |
| 鍵盤與Esc | 以真實Tab巡覽到SVG格，Enter／Space啟動，未用程式focus代替戰鬥導航；modal循環焦點、Esc取消並回到觸發鍵、結果回旅程 |
| 放大文字 | 720p放大文字後完成操作／結果；採正常垂直捲動，未壓縮正文換單屏 |
| 減少動態 | 停用局部動效，保留位置、HP與live文字結果 |
| 敘事／人物 | 對白紀錄開關、Esc返回、四人切換；四人1080p與720p實際截圖 |
| 執行錯誤 | 無page error或HTTP失敗資源 |

`npm run build --prefix ui-prototype` 與 `python scripts/validate_ui_scope.py` 另行執行。範圍檢查保護13份原始企劃檔、無Actions及根LICENSE；不把build當作美術驗收。

## 視覺技術與代理目視

| 面向 | 本輪結果 | 判定界線 |
| --- | --- | --- |
| 四人辨識 | 綠外套／象牙圍巾、青裙／銅辮、酒紅鋼甲／長盾、赭衣／船鉤可分；裁切無鄰角 | 代理目視，最終人物設計待人工 |
| 一致性 | 三名我方小人依精修立繪生成，同色塊與道具；瑪芮維持營地角色 | 4頭身程度與成熟感仍待人工判斷 |
| 圖集邊界 | 四欄／五欄分界的最大alpha為0或1，低於可見門檻16；不把透明壓縮殘值當跨欄人物 | `verify-art.py`讀取原PNG；未修改像素 |
| 場景協調 | 統一冷霧、苔綠、磨舊木材與左上光；偏寫實近景另作手繪修整 | 人物與背景的整體畫風仍需人類審圖 |
| 戰鬥閱讀 | 腳點底座／小血條／敵方三角與虛線／選取金邊；未確認虛影與已確認打擊分開 | 動作是展示回饋，沒有新增規則 |
| Steam小圖 | 真正1080p執行圖由Chrome縮至640×360及460×259，能看出沙盤、渡口與角色對峙 | 代理初審可辨；是否吸引陌生玩家尚未測試，不要求縮圖讀完整技能文字 |

## 字體與工具邊界

使用typography-audit的相關規則檢查，非完整78條認證：`font-fallbacks`、`size-body-text`、`size-line-height`及`brand-color`。新增Windows中文字型備援，正文基準16px、中文段落unitless行距1.7；小型戰鬥metadata為12–14px，放大文字流程已實測，仍需真人確認舒適度。

- 已修正 `font-fallbacks`：`ui-prototype/src/visual.css:7` 提供Microsoft JhengHei及系統sans備援；標題有PMingLiU／serif備援。沒有執行時下載字型。
- 已修正 `brand-color`：`ui-prototype/src/visual.css:24` 以明確色值取代停用按鈕整體半透明。7組指定純色文字配對為5.84–10.58:1，見 [contrast-checks.json](contrast-checks.json)；未宣稱所有插畫疊色像素均達標。
- `size-body-text`／`size-line-height`：正文及對白有明確層級；小型metadata是本輪保留的閱讀風險，未將它混稱正文品質認證。不同OS字型與真人閱讀未驗。

Chrome為test-only執行檔，固定絕對路徑／長度／SHA-256，驗證後才載入Playwright與建立profile；縮減child環境、封鎖非loopback請求。相對路徑、錯誤長度及錯誤雜湊三種外層失敗均未啟動profile或改寫驗收報告，見 [browser-binding-checks.json](browser-binding-checks.json)。這不是生產授權或一般瀏覽器安全認證。

## 待人工審圖與已知限制

1. 請以比較頁與四人1080p畫面判斷：是否已值得直接給陌生玩家看、4頭身小人與成熟立繪是否一致、460px圖是否有足夠吸引力。這三項尚未取得人工通過。
2. 原地形保持平面，方格河岸與材質重複仍有沙盤感；未把它改造成正式地理或新增高低差規則。
3. 小人仍是靜態姿態；本輪提供短位移、選取與打擊回饋，沒有逐幀走路、轉身及攻擊動畫。人物與素材仍是展示提案。
4. 沒有跨OS、手把或外部玩家驗收；正式戰鬥AI、平衡、規則、永久資料與新關卡未加入。
5. 先前治理的本機接線已交付；Codex平台信任與自然SessionStart／UserPromptSubmit／Stop／SessionEnd仍缺原生證據。視覺測試不能取代完整導入驗收，也未自行宣告聊天結束。

實際時間與計時限制見 [TIME-LEDGER.md](TIME-LEDGER.md)。
