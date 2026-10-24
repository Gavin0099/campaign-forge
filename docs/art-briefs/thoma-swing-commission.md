# Thoma 揮擊動畫 5 格 — 手繪／外包說明包

- 專案：campaign-forge（原創戰棋 RPG，Godot 4.7.x）
- 版本：2026-10-24（spike-02 A7 之後）
- 負責人：Gavin Wu（Owner）
- 狀態：**草稿，待 Gavin 決定由誰畫、預算與期限**（見最後「待 Gavin 決定」）

> 背景：A5、A6、A7 三輪 AI 逐格修圖都沒過（A7：5 格 0 格合格；臉／頭髮、披帶、刺繡、流蘇、袖口、連續播放都會走樣）。
> Owner 於 2026-10-24 決定：swing/00–04 這 5 格改成手繪或外包。

---

## English summary (for artists)

**Job:** hand-paint 5 animation frames of one character ("Thoma", an elderly field-medic friar) swinging a short one-handed flanged mace. The poses sit between two existing finished frames: **idle/01** (rest, appearance master) and **swing/05** (recover). Both are included and are canon. Your 5 frames must look like the *same painting* as those two.

**Deliverables**
- `00.png` `01.png` `02.png` `03.png` `04.png`: 5 PNGs.
- Each one **512 × 512 px**, **RGBA 8-bit, straight (non-premultiplied) alpha, transparent background**, sRGB, no embedded ICC profile needed, no guide layers, no drop shadow or ground shadow.
- Also send the layered source file (PSD, Krita or CSP), with one layer per body part if you can.
- Character faces **screen-right**. Do not mirror.

**Canvas rules (must match or the game will misalign)**
- Registration pivot is **(256, 464)**. The ground line is **y = 464**. The lowest opaque pixel must be at y = 463–465, and at least one foot must stand on that line.
- Keep body scale identical to idle/01: about 360 px from the ground to the top of the head. Head is about 70 px tall. Shoulder width is about 99 px.
- Draw the character **in place**. The engine adds the forward step offset itself.
- Mace-head centre per frame (±4 px): 00 (192, 85) · 01 (259, 87) · 02 (449, 110) · **03 (455, 196) = impact; this pixel must be opaque** · 04 (421, 376).
- Full landmark targets (hands, elbows, knees, feet) are in `thoma-swing/guides/swing-NN-guide.png`. These are transparent 512×512 overlays; put them on a top layer and delete them before export.

**Timing (fixed in the engine):** 00 anticipation 180 ms → 01 raise 70 ms → 02 swing/smear 40 ms → 03 **contact** 80 ms (+80 ms hit-stop) → 04 follow-through 100 ms → 05 recover 150 ms (existing). In Reduced-Motion mode only 00 / 03 / 05 are shown, so 00 and 03 must read clearly on their own. Frame 02 may use a painted motion smear on the mace.

**Appearance must match the anchors:**
- Grey short-cropped hair and a squared grey beard; heavy brow, no smile.
- Desaturated dark-teal over-robe on an ivory under-robe.
- Two ivory stole panels, each with ONE grey-green leaf-sprig embroidery (2 in total) and a short uneven fringe.
- ONE long knotted pale waist cord.
- ONE brown satchel at the screen-left hip, with a rolled cloth under the flap.
- Ivory flared undersleeves.
- Small bronze medallion.
- Worn brown ankle boots.
- Mace: dark iron flanged head, worn oak haft and small brass collar.
- Brush: thin broken dark-brown contour (1–3 px) and mottled, low-contrast hand-painted shading. No black vector lines and no cel shading.

**Do NOT** copy details from the A7 placeholder strip. It is a pose reference only, and its faces and costume details are wrong. Do not add a sword, staff, book or magic glow. Use no third-party IP. Owner policy on AI-assisted painting is still to be confirmed.

Acceptance uses the 13-point checklist below (section 6). Payment and deadline are to be confirmed.

---

## 1. 要交的東西

| 檔名 | 放在 repo 的位置 | 動作 | 時長 | 備註 |
|---|---|---|---|---|
| `00.png` | `shared-anim/thoma/swing/00.png` | 預備（錘子舉到肩後上方） | 180 ms | Reduced Motion 會顯示 |
| `01.png` | `shared-anim/thoma/swing/01.png` | 舉起／蓄力最高點 | 70 ms | |
| `02.png` | `shared-anim/thoma/swing/02.png` | 揮下途中（可畫動態殘影） | 40 ms | Reduced Motion 會略過 |
| `03.png` | `shared-anim/thoma/swing/03.png` | **擊中（impact）** | 80 ms，另加 80 ms 停頓 | 火花與音效錨點在 (455,196)；Reduced Motion 會顯示 |
| `04.png` | `shared-anim/thoma/swing/04.png` | 收招（錘子往下帶過） | 100 ms | |
| （已有）`05.png` | `shared-anim/thoma/swing/05.png` | 收勢（recover） | 150 ms | **不要改**，這格是基準 |

技術規格（引擎的 `anim_manifest.gd` 和 `frame_player.gd`、`test_manifest.gd`、`shared-anim/README.md` 都這樣要求）：

- **512 × 512 px**。每格固定一樣大，引擎不會自動裁切或縮放，大小不對 `test_manifest` 會失敗。
- **PNG，RGBA 8-bit，直通（非預乘）alpha，透明背景**，sRGB。
- 不要地面陰影、背景、參考線、浮水印或簽名。
- 角色面朝**畫面右方**。往左時由引擎鏡像，畫師不用畫。
- 檔名固定兩位數 `00`–`04`，路徑全小寫、用正斜線。
- 另外請交**分層原始檔**（PSD、Krita 或 CSP 都可以），之後修改或做其他動作會用到。

## 2. 畫布與定位規則

- **定位點 (256, 464)** 是角色的登錄原點，不是哪一隻腳的中心。
- **地面線 y = 464**。最低的不透明像素要落在 y = 463–465，至少一隻腳要踩在地面線上。另一隻腳可以因為重心轉移稍微離地，例如 04 的左腳在 y≈455。
- **比例跟 idle/01 完全一樣**：
  - 地面到頭頂約 360 px（idle/01 頭頂在 y=103）。
  - 頭高約 70 px，肩寬約 99 px，軀幹約 104 px，腰到地面約 204 px。
  - 不能因為動作把人畫大或畫小。
- **原地畫**。往前踏一步的位移由引擎依 manifest 的 `offset` 處理，畫師不用移動角色。
- 遊戲裡的實際大小大約是：角色高約 49 px（1280×720 下），攻擊特寫時鏡頭放大 1.4 倍，約 68 px。所以**剪影和錘子的位置要一眼看得懂**。細節則以 512 px 原尺寸審查。

### 每格的目標點（容許誤差 ±4 px）

錘頭的軌跡是一條連續的弧線（cubic Hermite），通過下面 5 個錘頭點，最後在 05 收回到身側。

| 格 | 動作 | 頭部中心 | 持錘手 | **錘頭中心** | 左腳／右腳 |
|---|---|---|---|---|---|
| 00 | anticipation | (260,143) | (127,117) | **(192,85)** | (145,464) / (342,439) |
| 01 | raise | (260,141) | (194,109) | **(259,87)** | (167,464) / (326,443) |
| 02 | swing／smear | (282,145) | (372,160) | **(449,110)** | (135,464) / (372,448) |
| 03 | **contact** | (264,140) | (358,196) | **(455,196)**，必須不透明 | (120,464) / (354,447) |
| 04 | follow-through | (310,141) | (347,324) | **(421,376)** | (165,455) / (334,464) |

- 肩、肘、空手、髖和膝的完整座標在 `thoma-swing/guides/swing-NN-guide.png`（透明 512×512 參考層，疊在最上層，輸出前刪掉），也可以看 `thoma-swing/refs/pose-targets.png`。
- 錘子要跟手和手臂一起動：握把到錘頭的投影長度約 55 px，錘頭約 37×36 px，黃銅箍約 7 px 寬。透視可能讓投影長度看起來不同，但錘子本身不能變長或變短。
- 03 的錘頭必須蓋住 (455,196)，這一點是火花和音效的位置，**不能移動**。
- 畫師如果覺得某格姿勢可以更好（例如 00 和 01 目前太像），可以提出來。改動要先經 Gavin 同意，而且錘頭的點位仍要在誤差內。

## 3. 外觀規格（以 idle/01 為主、swing/05 為輔）

來源只有兩張：`thoma-swing/refs/anchor-idle-01.png`（外觀主檔）和 `anchor-swing-05-recover.png`（收勢）。兩張有已知的差異：05 頭頂高約 10 px，右側刺繡高約 7 px。**比例以 idle/01 為準。**完整的數字規格在 repo 的 `shared-anim/thoma-appearance-spec.md` 和 `.json`，各部位的放大裁切在 `thoma-swing/refs/spec-crops.png`。

| 部位 | 規格 |
|---|---|
| 臉 | 朝右的四分之三側臉，長而有稜角。眉骨重、眼窩深、鼻子突出。灰色短方鬍和八字鬍。眼睛是 1–2 px 的深色小點，眉毛 2–3 px 斜線，嘴巴閉著、不笑，沒有卡通圓眼。 |
| 頭髮 | 灰色、很短，邊緣不規則，額角後退，往右梳，有細小捲曲紋理。耳朵露出，髮尾停在後頸、青綠領口上方。**沒有中分線**。 |
| 外袍 | 低彩度深青綠色，短外袖，下擺分片長裙，裡面是及踝的象牙白內袍，褶子寬、有筆觸。 |
| 披帶（stole） | 兩片象牙白垂帶：肩膀處寬、腰部窄，往下到末端又變寬。上方有青綠色的兜帽領交叉。左片寬約 24–30 px，右片約 12–22 px。 |
| 刺繡 | **每片垂帶各一株灰綠色葉枝，全身共 2 株**：一根中心莖，葉片斜向交錯，可見約 4 對（左）和 6 對（右）分枝，底下有淡赭色短邊。**不要重複的花菱紋，不要額外的花樣**。左邊那株被錘子遮住一部分是正常的，不要補畫被遮住的部分。 |
| 流蘇 | 每片垂帶末端有一排短而不齊的淡色流蘇：左邊約 10 根、右邊約 8 根（±1），長 4–9 px。另外**只有一條**打結的長腰繩垂下。流蘇不是腰繩，也不要整排一樣長的 20 px 長穗。 |
| 袖口 | 象牙白內袖從短青綠外袖裡張開，到手腕收窄，內側有深色摺痕，手臂接手的地方連續、不斷開。 |
| 下擺 | 象牙白內袍是連續的鐘形下擺，有幾條長褶，上面是青綠外袍的分片。**不能有分離的三角碎片**。 |
| 背包 | **只有一個**棕色翻蓋背包，在畫面左側腰臀處，翻蓋下有一捲淡色布卷（布卷不是第二個包）。 |
| 腰帶與徽章 | 棕色腰帶，畫面右側有淡色繩結。腰帶上方有一枚小青銅圓徽章（聖徽）。 |
| 鞋 | 兩隻磨舊的棕色圓頭短靴，有深色縫線和鞋帶，**兩腳都要接在腿上**，不能浮空或分離。 |
| 錘子（canon） | 單手短釘頭錘：暗鐵星形凸緣錘頭，有三角形凸片；磨舊的橡木柄；錘頭下方一個小黃銅箍，呼應聖徽；圓形柄頭；拿在**右手**。**不要劍、杖、書或魔法光**。 |
| 筆觸 | 細而斷續的深棕或深青綠輪廓，大多 1–2 px，袖下和背包下最多 3 px。斑駁、低對比的手繪高光。**不要黑色向量線，不要賽璐璐平塗**。 |

### 色票（idle/01 的單點取樣）

以下是**單一像素的取樣**，不是平塗色。實際顏色以兩張基準圖的整體觀感為準。另見 `thoma-swing/refs/palette-samples.png`。

| 區域 | Hex | 區域 | Hex |
|---|---|---|---|
| skin_light | `#d5b99f` | teal_light | `#4f635f` |
| skin_mid | `#9e856c` | teal_mid | `#405350` |
| skin_shadow | `#5d4f40` | teal_shadow | `#2d3835` |
| hair_light | `#b29d84` | ivory_light | `#e8d6c1` |
| hair_mid | `#806b56` | ivory_mid | `#d8c4ad` |
| hair_shadow | `#5b4938` | ivory_shadow | `#c4ac92` |
| embroidery | `#8d7862` | leather | `#503323` |
| oak（暗部） | `#120a06` | iron | `#685a48` |
| brass（暗部） | `#503323` | outline | `#121210` |

> 注意：`brass` 和 `oak` 取到的是暗部像素，`brass` 跟 `leather` 是同一個值。畫黃銅箍時請看基準圖上實際的銅色高光，不要直接用這個 hex 平塗。

## 4. 時序（引擎固定，畫師不用調）

`00` 180 ms → `01` 70 ms → `02` 40 ms → `03` 80 ms（**擊中**，contact_frame_index = 3；另有 80 ms 停頓、火花、音效和鏡頭震動）→ `04` 100 ms → `05` 150 ms。總長約 880 ms。

- **Reduced Motion**（減少動態）模式只播 00、03、05，每格 100 ms，所以 00 和 03 要能單獨看懂。
- 02 只出現 40 ms，可以畫錘子的動態殘影或模糊。這是唯一可以「不清楚」的格子。
- 01→02→03 要讓人感覺到重量：錘頭從肩後上方甩出去，在 03 停在正前方。04 錘頭帶到身體右前下方，05 收回身側。

## 5. 附的參考資料（`thoma-swing/`）

| 檔案 | 用途 |
|---|---|
| `refs/anchor-idle-01.png` | **外觀主檔**，512×512 原檔，canon |
| `refs/anchor-swing-05-recover.png` | 收勢格，512×512 原檔，canon，動畫最後一格 |
| `refs/anchors-2x.png` | 兩張基準圖並排放大 2 倍（nearest），方便看細節 |
| `refs/spec-crops.png` | 臉、頭髮、外袍、披帶、刺繡、流蘇、袖口、下擺、背包、鞋、錘子各部位的 1x 和 2x 裁切 |
| `refs/pose-targets.png` | 5 格的目標點與錘頭弧線疊圖 |
| `refs/palette-samples.png` | 色票取樣 |
| `refs/POSE-REFERENCE-ONLY-a7-placeholders.png` | A7 的 AI 佔位圖。**只參考姿勢，不要照抄任何細節**，臉、頭髮、披帶、刺繡、流蘇和袖口都是不合格的 |
| `guides/swing-00-guide.png` … `swing-04-guide.png` | 512×512 透明參考層：地面線、定位點、全部關節目標點、錘頭弧線。**輸出前刪掉** |

## 6. 審查與驗收清單

這份清單跟 A4–A7 審查用的 13 項一樣（`frame-audit.json` 的 `region_review`）。每格每項都要 PASS，才能把該格從 PLACEHOLDER 改成 PASS。

| # | 項目 | PASS 條件 |
|---|---|---|
| 1 | face_hair | 臉型、鬍子、眉眼和髮型跟 idle/01 是同一個人，連續播放時不會換臉 |
| 2 | stole | 兩片垂帶，寬窄變化符合規格，沒有多出或少掉 |
| 3 | embroidery | 每片一株葉枝，共 2 株，沒有發明新圖案 |
| 4 | tassels | 兩排短而不齊的流蘇，加一條腰繩，數量 ±1 |
| 5 | cuffs | 象牙白喇叭內袖，手臂和手連續 |
| 6 | hem | 連續的鐘形內袍下擺加青綠分片，沒有碎片 |
| 7 | palette | 跟基準圖同一組顏色和明暗 |
| 8 | seams | 沒有拼貼縫、斷線、殘影碎片或分離的布塊 |
| 9 | bag_count | 只有 1 個背包，加 1 捲布卷 |
| 10 | feet | 兩隻靴子都接在腿上，至少一隻踩在 y=464，最低像素在 y 463–465 |
| 11 | mace | 符合 canon 錘子；投影長度一致；錘頭在目標點 ±4 px；03 的 (455,196) 不透明 |
| 12 | landmarks | 頭、手、肘、膝、腳都在目標 ±4 px 內，或者差異已經 Gavin 同意 |
| 13 | sequence | idle/01 → 00–04 → 05 連續播放時，衣服的寬度和站姿不跳，看起來是同一張畫在動 |

技術檢查：512×512、RGBA、透明背景、沒有參考層殘留、檔名正確。

最後由 **Gavin 本人**在遊戲裡看實際播放和打擊感（HUMAN_PENDING），才算完成。

## 7. 怎麼放進遊戲、怎麼跑測試

**引擎程式不用改**：manifest 的路徑、時長、定位點和擊中錨點都不變。

```powershell
# 0. GODOT = C:\Users\daish\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe
cd D:\campaign-forge\scratch\godot-spike
# 1. 覆蓋 5 張圖（只覆蓋 00–04，idle/01 和 swing/05 不要動）
Copy-Item <交件資料夾>\0[0-4].png shared-anim\thoma\swing\
# 2. 同步到 Godot 專案（shared-anim → godot-spike/art/anim-shared，test_shared_hashes 會比對位元組）
& $GODOT --headless --path godot-spike -s res://tools/sync_shared_anim.gd
# 3. 重新匯入
& $GODOT --headless --path godot-spike --import
# 4. 跑 GUT 測試
& $GODOT --headless --path godot-spike -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit
# 5. 實際播放、截圖（720p）
& $GODOT --path godot-spike --resolution 1280x720 --max-fps 60 --audio-driver Dummy -s res://tools/capture_a7.gd
```

**要先知道：**

- 一般的契約測試對新圖**不用改程式就會通過**：`test_manifest`（512×512、路徑、時長）、`test_shared_hashes`（同步後位元組一致）、`test_playback` 和 `test_spike02`（播放、擊中、Reduced Motion）。
- **`test_a7_contract.gd` 會刻意失敗**，因為它把 A7 佔位圖釘死了：
  - `frame-audit.json` 的 sha256 和 `a7-swing-prompts.json` 的 runtime_sha256 都是 A7 的值；
  - 它要求 y≥420 的下半身像素跟 A6 一模一樣、03 錘頭區域和 04 錘頭像素要對上，而且 5 格都必須是 PLACEHOLDER。
- 所以換圖時要做一段「A8 換圖整合」：
  1. 把 A7 的 5 張圖封存到 `docs/evidence/spike02-a8/baseline-a7/`；
  2. 照 A3–A6 測試已經用過的做法，把 `test_a7_contract` 改成讀封存檔；
  3. 在 `frame-audit.json` 加上新圖的雜湊和 13 項審查結果；
  4. 新增 `test_a8_contract.gd`，鎖住尺寸、地面、03 錘頭不透明和 idle/05 雜湊不變。

  這一段是我們（Grok Bot／Codex）的工作，不用畫師處理。

## 8. 待 Gavin 決定

1. **誰畫？** 你自己畫，還是外包？外包的話是找台灣或日本的接案畫師（Pixiv／Skeb／X），還是 ArtStation、Fiverr 或 Upwork 上的國外畫師？
2. **預算**：5 格的總價上限是多少？要不要同時買分層原始檔和修改次數（例如含 2 次修改）？
3. **期限**：希望哪一天交？要不要分兩階段，先交 00 和 03 草稿確認姿勢，再上色完稿？
4. **版權**：原創商業遊戲需要**著作財產權讓與或獨家商用授權**，以及署名方式。要不要我起草委託合約要點？
5. **AI 輔助**：可不可以讓畫師用 AI 輔助？還是要求全手繪（建議在合約裡寫清楚）？
6. **基準圖要不要一起重畫？** idle/01 和 swing/05 本身也是 AI 生成的。手繪的 5 格跟它們放在一起可能會有筆觸落差。要只畫 5 格，還是 7 格整組重畫，順便統一風格？
7. **姿勢可不可以調整**：00 和 01 目前很像。要不要讓畫師提出更好的預備姿勢？04 的錘頭目標 (421,376) 是 A7 往下修 19 px 的位置，要不要沿用？
8. **交付管道**：只寄 zip 給畫師，還是給他看 repo？要不要簽 NDA？

---
來源：`shared-anim/thoma-appearance-spec.md/.json`、`shared-anim/manifest.json`、`shared-anim/README.md`、`godot-spike/scripts/anim/{anim_manifest,frame_player}.gd`、`godot-spike/tests/test_{manifest,shared_hashes,a7_contract}.gd`、`godot-spike/docs/evidence/spike02-a7/`（branch `codex/godot-spike` @ 042810a）。
