# 來源、版本與 Skill 使用證據

查閱日期：2026-10-22（台北）。以下是公開來源的唯讀研究；沒有安裝 Skills／引擎／套件、執行外部範例，或把外部原始碼／圖像搬進 app。GitHub API metadata 之外，另查實際樹、LICENSE、指定 Skill／關鍵程式。完整 commit、Git blob、下載檔 SHA256、查閱範圍見 [source-manifest.json](source-manifest.json)。授權判斷限於已查檔案，不把根 LICENSE 推論為每張素材都可使用。

## Repo 評估

| Repo／固定研究版本 | 實際授權證據 | 可學習與限制／本輪決定 |
| --- | --- | --- |
| [awesome-gamedev-agent-skills@0a70cfc](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd) | [Apache-2.0 LICENSE](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/blob/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/LICENSE)、同版 NOTICE | 五個 Skill 作研究方法，不批次安裝。若日後散布原文或修改版，保留授權／NOTICE 並標示修改；本輪只寫原創摘要與連結 |
| [Grid-Tactics@8d1952b](https://github.com/franciscobom/Grid-Tactics/tree/8d1952b46c771318b6f798b44038bac4490afe64) | 完整 35 檔樹未見 LICENSE，API license=null；**未確認重用授權** | 讀 TurnManager／AIController 的階段與有界行動方法：決策和畫面分開、無路時結束行動。不複製碼／美術；不採用其全滅即勝利替代 L03 目標。小型 repo，不當成熟引擎保證 |
| [template-react@7d29228](https://github.com/phaserjs/template-react/tree/7d292284722f6cccd6a8bfa5dccf668e383e0156) | 實際 [MIT LICENSE](https://github.com/phaserjs/template-react/blob/7d292284722f6cccd6a8bfa5dccf668e383e0156/LICENSE) | package 1.2.0；Phaser 4.0.0／React ^19／Vite ^6.3.1。PhaserGame 的掛載／destroy 與 EventBus 可作橋接參照，監聽須依實例精確解除；不照搬全域 removeListener 管法。不執行 scripts（包含 log.js） |
| [2DTacticalRPGDemo@c58849b](https://github.com/HopeMetal/2DTacticalRPGDemo/tree/c58849b67a89897ecdb6b3dbb7f25183d3be96ac) | 根 [MIT LICENSE](https://github.com/HopeMetal/2DTacticalRPGDemo/blob/c58849b67a89897ecdb6b3dbb7f25183d3be96ac/LICENSE)；[imagese/LICENSE.TXT](https://github.com/HopeMetal/2DTacticalRPGDemo/blob/c58849b67a89897ecdb6b3dbb7f25183d3be96ac/imagese/LICENSE.TXT) 為 **CC-BY-SA 3.0**，README 指 DENZI 圖像來源 | project.godot 宣告 4.4。研究格位／占位／地形 Cost／Blocks 與訊號；Combat 和 Controller 有節點、sprite 及 await 移動耦合，不直接移植；簡單近戰 AI 不等於完整策略系統。不使用圖像，不能說整包 MIT；也不推論資產 SA 必然套到整個遊戲原始碼 |
| [EasyStar.js@1061514](https://github.com/prettymuchbryce/easystarjs/tree/10615147add3af46f76a5d86ee7b7e7bebf83ac5) | 實際 [MIT LICENSE](https://github.com/prettymuchbryce/easystarjs/blob/10615147add3af46f76a5d86ee7b7e7bebf83ac5/LICENSE)；package 0.4.4 | 非同步 A*、分次計算、地形成本及 cancelPath；版本提交較舊，未驗證現代工具鏈。99 格等成本 BFS 已足夠，不增加依賴；未來真有權重／大型圖再比較 |
| 補充 [godot-tactical-rpg@cfe785e](https://github.com/ramaureirac/godot-tactical-rpg/tree/cfe785e5b6f88fe8b24559616dfb9a3f8b433f6e) | 根 MIT LICENSE；第三方個別素材未完成清查 | development 的 project.godot 為 4.3，README 列走格、回合、鏡頭與基本 AI，也自述不是完整框架。僅讀 README／專案與授權；不聲稱深入審核控制器、不取素材、不因此換引擎 |

若後續真的引入第三方程式，需新增逐項來源／版本／授權聲明；此研究不新增讓原創故事開源的 LICENSE。

## 五個 Skill：實際讀取 → 具體落點

觸發：使用者在本次研究指示中明確指定這五個 Skill。本輪已告知採用，從固定 commit 讀取五份完整 SKILL.md；沒有語意版本欄位，**用 commit＋blob＋SHA256 識別版本**。本次使用方式是外部檔案唯讀套用研究方法，不冒稱已安裝於 `.codex/skills`，也不補造前輪歷史載入證據。未讀其他 engine skills 或全部 references，不聲稱完整載入整套包。

下列相對路徑均位於 [固定 skills 目錄](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/0a70cfc64672d512c5b5b6006b5dcb5cf90dbdbd/skills)，manifest 另列每檔永久 URL／雜湊。

| 路徑 | 採用的方法 | 本輪具體成果／未驗證項 |
| --- | --- | --- |
| `workflows/prototype-fast/SKILL.md` | 一個問題；先決定 throwaway／可維護；短時間盒；外部玩家；keep／kill／refactor | README 單一問題；P1先聲明採可維護的獨立Demo、60min機制時間盒；ACCEPTANCE去留條件。尚未做PoC或人類試玩；沒有把throwaway spike混成正式程式 |
| `disciplines/level-design/SKILL.md` | 先定移動尺度、灰盒關鍵路徑、確認可達、再加美術 | 現有開閘目標不可達證據；Demo 起點、橋與護送路線；第一次操作無計時教學。未把平台跳躍範例數值搬成戰棋規則 |
| `disciplines/game-ai/SKILL.md` | 決策／尋路分離；少量狀態；無路退出；按狀態變化重算 | 兩種確定性策略、可解釋 intent、行動上限與重驗；只在 revision 變動重算。不做 BT 框架／逐幀尋路 |
| `disciplines/game-ui-ux/SKILL.md` | 邊緣錨定與流式容器、焦點、畫面堆疊、事件更新 HUD | P5 的操作列／意圖／目標；Esc、modal 焦點返回、720/1080及文字放大驗收。未冒稱新增手把支援 |
| `disciplines/game-feel/SKILL.md` | 先有正確機制與事件；2–3種有界回饋；不阻塞模擬 | ActionResolved 驅動位移／受擊／數字，Reduced Motion／跳過；演出不掌握 HP 與勝敗。本輪不新增動畫、美術或 hitstop 系統 |

## 官方文件與資料化邊界

| 官方來源 | 本輪讀到的能力／採用範圍 |
| --- | --- |
| [Phaser Scenes](https://docs.phaser.io/phaser/concepts/scenes) | SceneManager、生命週期、pause/resume/sleep；供 PoC 的掛載卸載設計，不拿 Scene 當戰鬥領域模型 |
| [Phaser Tilemap，固定 v4.0.0 API](https://docs.phaser.io/api-documentation/4.0.0/class/tilemaps-tilemap) | Tilemap 存資料，TilemapLayer 顯示；可由 Tiled JSON／CSV／array 載入，支援 isometric 等。不能把 renderer 座標當導航資料；原嘗試的 concepts/tilemaps 與 gameobjects/tilemap URL 讀取失敗，改查此有效頁 |
| [Phaser Tweens](https://docs.phaser.io/phaser/concepts/tweens) | Scene 所屬的時間插值；用於外觀，完成回呼不決定是否命中 |
| [Tiled Custom Properties](https://doc.mapeditor.org/en/stable/manual/custom-properties/) | 查閱頁標 1.12.2；型別屬性／enum／class，可對應 walkable、objectiveId、spawnGroup；尚不導入編輯器 |
| [Tiled JSON Map](https://doc.mapeditor.org/en/stable/reference/json-map-format/) | 查閱頁標 1.12.2；width/height、orientation、layers、properties；version 為格式，tiledversion 為產生器版本。未來轉換成自己的 MapDef，驗證尺寸／越界／屬性，不直接信任可執行腳本或外部路徑 |

官方網頁是查閱時快照，除明示的 v4.0.0 API 外，不宣稱永久凍結或與模板同版。這些文件是研究來源，未複製其範例碼或圖檔。
