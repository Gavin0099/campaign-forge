# GPT web review — godot spike-04 (24×18 playable field + hit-feel tone-down)

- Reviewer: ChatGPT web, campaign-forge project, Thinking effort Medium
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6adcc364-90b4-83ec-b316-9220176413fc
- Date: 2026-10-24 (Asia/Taipei)
- Reviewed: codex/godot-spike cbf3608..905c0ce (GUT 123/123, 10,310 asserts)
- Images (3): spike03-vs-spike04 impact strip (downscaled), 24×18 O overview (720p), turn-4 reinforcement warning + scrolled view
- Note: this is GPT's review and may be more lenient (or differently focused) than Codex's own self-audit in HANDOFF.md "spike-04". Text below is verbatim from the rendered page (Markdown bold/bullets were lost in copying).

---

campaign-forge spike-04 審查結論

1. 總判定：CONDITIONAL ACCEPT

大地圖、鏡頭操作與增援機制已具備可玩的基礎，GUT 123/123 通過是正面訊號。但目前仍有戰鬥特效過強、敵方 AI 行為不足及職業定位失衡等問題，尚不適合視為可驗收的完整戰鬥體驗。

2. 打擊感降濃：仍太強。

相較 spike-03，粒子、數字及閃光確實朝正確方向收斂。

接觸瞬間的白色閃光仍過度搶眼，會遮住角色與武器接觸細節；傷害數字也偏突出。

建議再降低閃光覆蓋率與粒子密度，優先確保攻擊動作可辨識。Hitstop 與方向性震動先保留，避免一次改動太多參數。

3. 大地圖、鏡頭與提示

24×18 戰場： 地形種類與道路布局足以支撐戰術選擇，但全圖模式下人物過小，只適合總覽，不適合直接操作。

鏡頭： WASD、拖曳、縮放與定位的設計合理；局部畫面有角色被裁切、標籤重疊的情況，應優先檢查鏡頭邊界及 HUD 避讓。

小地圖： 位置與基本用途清楚，但需要驗證圖示能否在實際操作尺度下辨識，並確認點擊定位可靠。

目標與增援： 第 4 回合預告、第 5 回合增援的時間資訊清楚；但敵群文字與場景物件重疊，三個增援標記也較醒目，應改善標籤排版。

4. 戰鬥節奏：部分符合 15–25 分鐘目標。

主道策略 12 回合勝利，估計 12.9–21.2 分鐘，落在目標範圍的部分區間，尚不能宣稱穩定達標。北側包抄 7 回合敗、固守 3 回合敗，也顯示策略容錯可能不足。

尤其 72 個敵騎士無目標回合、增援可被繞過，代表問題不只是戰鬥時間，而是敵人沒有持續施加有效壓力。

5. 職業平衡

近戰： 貢獻 53% 傷害，應保留作為主要交戰核心，但還需確認承傷與生存是否合理。

遠程： 貢獻 31% 傷害、取得 60% 擊殺，且沒有 LOS 限制，可能過度主導收割。應先驗證射線、地形與射程規則。

高機動： 貢獻 15.6% 傷害且早死，角色的機動優勢未轉化成有效戰果。應檢查進場路線、脫離能力與定位，而不是直接增加傷害。

6. 下一步建議（依優先序）

修正敵方 AI： 解決無目標空轉、路徑選擇與領袖防守，讓增援無法被輕易繞過。

驗證戰鬥規則： 明確測試遠程 LOS、地形阻擋、威脅範圍及增援觸發條件。

調整特效： 降低接觸閃光與傷害數字的視覺權重，保留 hitstop、方向震動與後座力。

改善鏡頭與 HUD： 修正角色裁切、標籤碰撞及全圖模式下的人物可辨識性。

進行真人盲測： 至少測試主道、包抄、固守三種策略，記錄實際耗時、傷亡、操作困惑與勝敗原因，再決定平衡數值。

最重要的判斷： spike-04 已證明大地圖技術方向可行，但尚未證明它能形成有壓力、有取捨且能穩定控制在目標時間內的戰棋體驗。下一輪應優先改善敵人行為與規則可信度，而不是繼續擴大地圖或增加美術內容。
