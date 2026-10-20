# VD3 驗收與待審項目

VD2 已由 Owner 判定美術驗收未通過。VD3 的實作與證據交付完成，**工程功能通過；動畫重量感與整體美術尚未通過 Owner 驗收**。沒有以固定骨架、測試數或 GIF 數量宣稱商業品質。

| 判定 | 結果與界線 |
| --- | --- |
| 工程功能 | 22 項真實 Chromium 檢查通過，pageerror／HTTP 失敗為零；最後執行 2026-10-20T16:07:26.308Z 至 2026-10-20T16:09:56.339Z |
| 視覺技術 | 固定臉／衣物原件、42單位短劍；近戰腳點固定、刀刃與變形目標錨點對齊；敵人軀幹與頭部實際後仰；三枚獨立飛彈及同時命中。這些有實機與幾何證據，不等同自然演技評分 |
| 人工美術 | 待 Owner 審查；紙片感、關節與布料連續性、重量感及完整風格一致性尚未核准，不標示美術通過 |

## 可操作交付

原型：繼續旅程 → 營地 → 渡口事件 → 任一選擇 → 部署 → 確認出發 →「演出展示」。席恩只展示非魔法近戰；獨立測試 Wizard 才能施放 Magic Missile。三個選單可分別分配 A／B，支援全部同目標或多目標；預設2A＋1B。排練不修改原隊伍HP、位置、回合或行動。Esc 停止，再按 Esc 離開排練並還原原鏡頭。音效預設關閉，手動按「音效：關」開啟。

- [同狀態 Before／After、關鍵姿勢與兩解析度 GIF](comparison.html)。Before 固定為 main@0300c85 已保存的 VD2 完整載入預覽；沒有回填新圖。排練陣容與聚焦鏡頭和舊GIF不同，不能當作同狀態動態比較。
- [720p近戰](../../screenshots/vd3/melee-1280.gif)、[1080p近戰](../../screenshots/vd3/melee-1920.gif)、[720p Magic Missile](../../screenshots/vd3/missile-1280.gif)、[1080p Magic Missile](../../screenshots/vd3/missile-1920.gif)。均為實際 Chromium CDP 影格與擷取時間戳編碼，沒有生成戰鬥影片或合成補幀；GIF無聲。
- [管線決策](PIPELINE.md)、[SRD能力對照](SKILL-REFERENCE.md)、[授權與改寫聲明](SRD-NOTICE.md)、[PNG原件與Before雜湊](assets.json)、[生成前保存的完整提示](caster-prompt.txt)、[官方來源](reference-sources.json)、[實際投入](TIME-LEDGER.md)。

## 工程與實機證據

權威報告：[capture-record.json](../../screenshots/vd3/capture-record.json)，綁定全部src、art、公開notice、tests與package檔案的實際SHA-256；另有四份 recording-*.json 記錄逐幀原始JPEG時間戳／雜湊及GIF雜湊。原始JPEG留在ignored scratch，GIF與manifest可持久審查。

| 驗證 | 實測範圍 |
| --- | --- |
| 近戰完整週期 | Idle → 580ms準備 → 180ms出手 → 34ms接觸 → 88ms hitstop → 260ms敵人反應 → 680ms恢復；正常確認另保留880ms移動。使用同一RAF時鐘 |
| 真正刀刃接觸 | 十次近戰的 Impact 刀尖固定，與經SVG變形後敵人胸前錨點的最大畫面距離 1.431px；不是完整碰撞引擎，也不宣稱所有武器／方向均已解決 |
| 固定形體與連播 | 近戰、法術各10次，原始頭部image與靴點／武器尺寸一致，每次回到相同待機rig，特效清空、無卡死；攻擊期間靴點transform不變。自然肢體表演仍需人工看GIF |
| 狀態邊界 | 正常移動／技能預覽與出手不改HP與位置；Impact才套用既有固定3效果與一次行動；同步連按確認不重複 |
| 取消與換畫面 | Impact前取消不生效，之後取消保留一次結果；命中前後開設定再返回不殘留舊確認；排練與音源亦停止 |
| Magic Missile | 三枚分離飛彈、3:0與2:1目標分配、同一Impact時鐘令兩目標後仰；排練不扣HP或法術位。獨立身份閘拒絕席恩施法、正式隊伍目標、非三枚與committed測試法術 |
| 卸載／Reduced Motion | 實際React root卸載後無Impact／Done回呼；開場與中途切偏好皆無長動作／VFX，已確認效果只套用一次 |
| 既有流程 | 居民及軍糧兩分支→結果→戰役後果；只部署莉妲，真實Tab／Enter／Space選格與確認；完成視窗焦點循環／Esc；對白紀錄、資訊面板與鏡頭操作 |
| 720p／1080p | 99地景polygon與99點擊polygon完全相同；兩解析度實際PNG／GIF、無頁面橫向溢出。720p放大文字的法術選單computed font≥18px，面板可捲動，主流程完成 |
| 音效 | 本地原創Web Audio合成；測試監看真實Oscillator節點啟動及取消後active=0。未完成人工耳機／喇叭聆聽評分，不能由無聲GIF驗收聲音品質 |
| 效能觀察 | 20次重播逐RAF取樣，每次p50／p95記於JSON，本輪最慢p95=16.80ms。僅此台headless Chrome短樣本，錄影開銷另計，不是低階PC或跨平台效能認證 |

PNG關鍵姿勢分次重播擷取，capture-record記錄擷取前後stage；短暫Impact可能在截圖完成前進入Reaction，不能以檔名宣稱畫面精確停在某一毫秒。時序以完整GIF與逐RAF檢查為準。

| 實際錄製 | 原始影格數 | GIF長度 | bytes |
| --- | --- | --- | --- |
| melee 1280 | 121 | 3.04s | 1,813,486 |
| missile 1280 | 193 | 4.38s | 2,628,245 |
| melee 1920 | 119 | 2.93s | 3,774,033 |
| missile 1920 | 188 | 4.32s | 5,341,346 |

## 尚未達標／尚未核准

1. **動畫自然度與重量感未核准**：固定部件保持形體，但軀幹轉動仍有紙片感；沒有布料次動作、手指／表情演技、自然透視轉身或格擋交鋒。這些不由功能測試補足。
2. **畫風一致性未核准**：已把測試法師修為約五頭身並實機確認；其線條／材質仍需與原隊伍並列人工審查。測試角色不是正式同伴，也沒有配套立繪或故事身份。
3. **量產能力未證明**：只有席恩近戰、測試法師施法與兩種敵人受擊；其他同伴沒有這套完整骨架，沒有八方向、全部技能或正式職業系統。舊30幀PNG原件保留，沒有繼續生成整批姿態來充數。
4. **環境美術沿用限制**：平面河岸、重複材質和地景／人物透視仍是既有未達標項目，本輪不以新特效掩蓋；沒有稱Steam商業截圖品質通過。
5. **正式規則未定案**：僅SRD 5.2.1候選參考與Magic Missile識別；無完整5e、命中骰、法術位、集中系統、AI或數值平衡。正式故事／職業與S4未執行。

## 重驗與治理界線

使用既有工具鏈，先在ui-prototype以5175埠啟動Vite（例如 npm run dev -- --port 5175 --strictPort），再依序執行 tests/vd3-browser.mjs、Python tests/encode-vd3.py、tests/verify-vd3.mjs。Node／Python使用本機已核對的絕對路徑，Chromium須符合ignored .codex/visual-browser-binding.json。test:visual／test:evidence已指向VD3；VD2命令與舊報告保留為歷史，不能驗證已改版來源。

最後TypeScript／Vite、13份企劃保護與治理隔離測試的真實退出碼見 artifacts/governance-native-acceptance.json 與canonical delivery receipts。該治理檢查是隔離replay，**不是平台自然回呼**；使用者已信任／啟用修正版hooks並重新載入，不再待重複信任，目前仍不宣稱完整自動治理。

重驗曾發現截圖等待跨過短暫Impact，已改各姿勢分次重播；另遇兩次Windows覆寫既有PNG的UNKNOWN檔案錯誤，失敗報告留scratch，改用buffer→唯一暫存檔→替換並記錄有限重試，原始CDP亦使用每次獨立目錄。鏡頭復位檢查等待實際React效果完成後再斷言原viewBox，未省略復位條件。最後來源凍結後才執行本報告所連的完整驗證。
