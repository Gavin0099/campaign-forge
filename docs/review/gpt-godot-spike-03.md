# GPT review — Godot spike-03 (hit feel + big-map proposal)

- Segment: codex/godot-spike 20d9844..a0ae42c (spike-03 W1–W7, 7 commits; GUT 89/89, 8958 assertions)
- Date: 2026-10-24 (Asia/Taipei)
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6adc9d22-7740-83ee-a19b-3a0f0e7a21b2
- Model / effort: ChatGPT Thinking, effort Medium
- Images: godot-spike/docs/evidence/spike03/impact-strip-before-vs-after.png, docs/proposals/big-map/scroll-west.png, docs/proposals/big-map/overview.png
- Prompt: hit-feel value table + big-map proposal summary pasted as text; answer saved verbatim below.

---

1. 打擊感：CONDITIONAL PASS

比 A9 明顯更強，但目前有些過頭。

Flash：調低。 白色輪廓過曝，人物細節幾乎消失；建議 0.8 左右，保留命中辨識。

火花：適度減量。 現在爆發感夠，但過密且遮擋角色；優先保留方向性火花。

傷害數字：縮小約 10–15%。 現在視覺重量過大，容易搶走角色與戰場焦點。

Shake：先保留。 8／12 px 有力，但須實測是否影響辨識與暈動症體驗。

Hitstop、後仰、揚塵：先保留，再實機調整。 音效仍是 placeholder，不能算完整驗收。

2. 大地圖：推薦 C，但分階段落地

160 px 菱形格、96 px 人物，視覺辨識度合理；B 的美術重製成本不值得現階段承擔。

主要風險是地圖變大不等於戰術變深：移動距離過長會拖慢開戰，遠程與高機動角色可能取得不成比例的優勢。

建議先驗證 24×18，再擴至 32×24；L03 保留 11×9 教學地圖。

Gavin 必須先決定：

首版尺寸：建議 24×18。

人物：採 96 px。

無 fog：首版可接受。

操作：WASD、中鍵拖曳、O 總覽。

單場目標：建議 15–25 分鐘，需實測。

接受 hybrid 地景：建議接受。

3. 總評

CONDITIONAL ACCEPT

打擊感方向正確，但特效層級需要收斂。C 案值得進入可玩原型，兩張地圖圖像仍不足以證明實際操作體驗合格。

4. 下一步

微調 Flash、火花、傷害數字，補上正式音效。

建立 24×18 可操作戰場，驗證鏡頭、捲動、尋敵與交戰節奏。

測試近戰、遠程、高機動三種戰術的平衡。

通過後擴至 32×24，才投入完整地景製作。
