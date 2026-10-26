# GPT review — Godot spike-06 (balance, win route, reinforcements, multi-seed, scout role, flash 0.5)

- Reviewer: ChatGPT web, project "campaign-forge", Thinking effort Medium (new chat "Spike06 review verdict")
- Chat: https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6adf4c54-f6d0-83e8-a3a6-a59939940829
- Date: 2026-10-26 (Asia/Taipei)
- Reviewed: codex/godot-spike 8010bde..1cff2db (spike-06 W1–W8, GUT 165/165)
- Inputs: 3 images (docs/evidence/spike06/win-continuous.png, scout-flank-finish-retreat-60fps-strip.png, hitfeel/impact-strip-spike05-vs-spike06.png downscaled) plus a short text ask with the 20-seed before/after PACING table.
- Note: this is GPT's review from images and summary text only. It may be more lenient than Codex's own self-audit in HANDOFF.md, and it is not Owner (Gavin) approval or human playtest evidence.
- Transcribed verbatim from the page text (section 5 table re-rendered as Markdown).

---

campaign-forge Godot spike-06 審查結論
CONDITIONAL ACCEPT
玩法方向成立，尚未達到平衡驗收

1. 整體 Verdict：CONDITIONAL ACCEPT
- 敵軍主動推進、增援、斥候戰術與勝利路線都有實質改善。
- GUT 165/165 通過是正面訊號，但不能代替策略平衡、效能及實際遊玩驗收。

2. 是否有可靠、但不會過度簡單的勝利路線？
- 有初步可行路線：側翼策略 14/20 勝，勝利回合中位數 T13；道路策略 10/20 勝。
- 但尚不能稱為可靠：20 個 seeds 的樣本仍小，兩種策略的勝率差距也不足以證明側翼明顯優越。
- 必須處理快速繞過增援的漏洞：已知有 3 個 seed 在 T6 零陣亡、不接觸增援就獲勝。這比正常的 T13 勝利更值得優先調查。

3. 增援是否真的重要？
- 戰鬥過程中通常重要：道路路線 100%、側翼路線 95% 的對局有交戰增援，勝局的增援交戰率也達 100%。
- 但增援尚未成為勝利的必要戰略考驗。T6 繞過案例證明玩家可能跳過整段內容。
- 建議先調整增援與領袖目標的空間關係、接敵時機及勝利條件，不要直接增加敵軍 HP。

4. 斥候是否建立了側翼、攔截、收尾定位？
- 擊殺占比 40.9%
- 傷害占比 25.1%
- 收尾次數／攔截次數 61／87

定位基本成功。 斥候擊殺占比高於傷害占比，符合收尾角色；攔截數也支持其戰場控制價值。但仍會在 T3 陣亡，需要改善早期暴露與撤退路徑選擇，不宜只繼續增加輸出。

5. 20 個 seeds 有多少真正不同？樣本是否足夠？

| 策略 | 不同對局軌跡 |
|---|---|
| Road | 20/20 |
| Flank | 20/20 |
| Turtle | 12/20 |
| Scout-retreat | 14/20 |
| Scripted bypass | 10/20 |

這是不同軌跡數，不等於獨立有效樣本數；相同軌跡可能由不同 seed 重現。
20 seeds 足以發現明顯漏洞、淘汰失敗策略，但不足以確認平衡。側翼 70% 對道路 50% 仍只是初步訊號。
下一輪應增加不同 seeds，並按部署、策略與勝負原因分層分析。

6. Flash 0.5 是否合適？
暫時接受 0.5，不再優先調整。 相較 0.6，降低閃光強度是合理方向；其他打擊層保持不變也有助於隔離變因。不過，逐格對照不能完全代表實際播放的視覺感受，應保留正常速度的實機驗收。

7. 15–25 分鐘的節奏目標達成了嗎？
尚未達成驗收標準。 側翼估計約 17.2–28.4 分鐘，仍可能超過 25 分鐘；目前 0/20 的完整時間估計區間落在 15–25 分鐘內。應優先取得實際遊玩時間，而非只依模型估算。
另外，平均 frame time 從約 23 ms 升至 34 ms，退步約 48%。34 ms 已明顯超過 60 FPS 的 16.67 ms 預算，必須列為效能問題。

8. 建議下一步（依優先順序）
- P0：封堵快速繞過漏洞，確認勝利條件、領袖可達性及增援介入是否符合設計意圖。
- P0：效能剖析，定位 23→34 ms 的退步來源，恢復接近 60 FPS 的目標。
- P1：擴大多 seed 驗證，比較正常部署的 Road、Flank、Turtle，記錄勝率、回合、陣亡、增援參與率及繞過勝利。
- P1：修斥候早期生存，測試 T3 陣亡原因、攔截位置及攻擊後撤退是否可靠。
- P2：實際節奏與打擊感驗收，確認 15–25 分鐘目標、Flash 0.5 與不同裝置效能。

最終判斷：spike-06 已證明玩法比 spike-05 更有可玩性，但還沒有證明它已平衡。下一輪應優先解決「繞過增援」與效能退步，而不是繼續加內容或調高傷害。
