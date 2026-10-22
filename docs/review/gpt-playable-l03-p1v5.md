# GPT web review: playable-l03 P1v5 (battlefield interaction feedback)

- Range: 024292b...a42a4f4 on codex/playable-l03-research
- Reviewer: ChatGPT web, in Gavin's campaign-forge project, 2026-10-23 (Asia/Taipei). Chat "Review P1v5 Feedback": https://chatgpt.com/g/g-p-6ad7456d80a081919d343a5268d535c2-campaign-forge/c/6ada516b-9018-83ee-a0ff-6e6863c56c16
- Claude review: none for this chunk.
- The reviewer did not run the tests itself.
- Verdict: **needs Owner**. Resource check: 13 PASS / 2 FAIL / 2 N/A, as GPT reported it. The two FAILs are game-feel event accuracy and the missing human playtest.

## 1. 結論
needs Owner. P1v5 的事件驅動回饋架構基本成立，但尚不足以認定已達正式遊戲的視覺與操作品質。功能可進入 Owner 試玩，但不宜直接宣告 P1v5 視覺品質驗收 PASS。

## 2. 問題
| Priority | File:line | Issue | Evidence | Suggested fix |
|---|---|---|---|---|
| P1 | PlayableL03.tsx:64–75 | 阻擋特效可能暗示不存在的實際接觸 | blocked 只代表敵人找不到可行路徑；程式另行選取任意相鄰友軍作為火花對象，並非規則事件提供的阻擋者。 | 將一般路徑受阻與確認的敵我接觸分開。沒有接觸證據時只顯示「通道受阻」，不播放碰撞火花。 |
| P1 | PlayableL03.tsx:78–79 | 落地煙塵只附著於最後一筆移動事件 | reverse().find(type === "move") 只選最後一名移動角色。 | 以每個 move event 建立獨立落地事件。 |
| P1 | PlayableL03.tsx:60–79, 158–174 | 阻擋與干擾效果集中在整段移動播放結束後 | finish() 才一次設定 winch、blocks、arrival。 | 將回饋排程對應到各事件的視覺播放節點。 |
| P2 | presentation.tsx:68–72 | 絞盤新增幾何疊圖，尚未延續 P1v4 的手繪材質語言 | 新增圓形輪盤、交叉線條及 SVG 拉索。 | 使用原有絞盤素材的局部動畫影格或相同筆觸的透明疊圖。 |
| P2 | PlayableL03.tsx:250–264 | 預測意圖對 blocked 敵人缺少地圖上的明確落點 | blocked 沒有預測目標，主要依賴右側意圖文字。 | 在敵人腳下顯示受阻標記。 |

P0：未確認有新的 P0 規則破壞或阻斷遊戲流程問題。

## 3. 與交接報告不符之處
| 交接宣稱 | 審查結果 |
|---|---|
| Body-block clash spark | 部分成立。相鄰友軍並不一定是造成敵人無路可走的角色。 |
| Arrival dust | 部分成立。只綁定最後一筆 move event。 |
| Feedback at the point of action | 部分成立。整段動畫結束後統一顯示。 |
| All transient feedback respects Reduced Motion / Skip Animation | 程式碼支持；獨立實機驗證尚未完成。 |
| 93 game checks PASS | 報告有記錄；本次沒有重新執行。 |
| No priority was dropped | hit、shove、damage 沒有對應規則事件，僅能算原始事件範圍內的部分完成。 |

交接報告主動承認輪盤與拉索仍是幾何疊圖，並標記 HUMAN_PENDING，不構成虛假交付。

## 4. 遊戲性與故事觀點
比 P1v4 更像可以玩的遊戲，提升主要來自操作回饋，而非戰術深度。下一個最值得投入的改動：建立事件與演出的逐事件對應機制，讓每件事在發生當下得到自己的回饋。本次沒有新增劇情。

## 5. 沒檢查到的部分
GPT did not run any tests, did not do a human playtest, and did not open the PNGs or watch the animation. It also could not read gpt-playable-l03-p1v4.md or docs/design/RULE-ADAPTATION-CONTRACT.md at the reviewed version.

## 6. 給 Gavin 的決策
1. 事件回饋：先修正碰撞語意、逐事件動畫與落地特效（建議），或接受現況。
2. 絞盤幾何動畫：改成與手繪場景一致的動畫素材（建議），或暫時保留 CSS/SVG。
3. 下一個品質門檻：自動化回歸後交給 Owner 實際玩一局（建議）／只做自動化與截圖比對／產生下一輪 Codex 任務。

## 7. 資源檢核
| Section | Item | Result | Evidence |
|---|---|---|---|
| A | prototype-fast | PASS | Brief 第 1～4 項限定範圍，四個實作提交可核對 |
| A | level-design | N/A | 沒有地圖或路線修改 |
| A | game-ai | PASS | PlayableL03.tsx:125–130 使用 resolve() 預測事件 |
| A | game-ui-ux | PASS | PlayableL03.tsx:217–223, 250–284 |
| A | game-feel | FAIL | PlayableL03.tsx:64–79 阻擋者判斷與落地回饋 |
| B | Grid-Tactics 架構分離 | PASS | rules.ts:38–46, 97–156，React 只播放 |
| B | HopeMetal 授權 | N/A | 未引入 |
| B | 無新引擎或相依套件 | PASS | 沒有 package.json 變更 |
| C | 3–5 分鐘戰鬥 | FAIL | HUMAN_PENDING |
| C | 敵人行動可理解 | PASS | PlayableL03.tsx:125–130, 250–264, 325–335 |
| C | 可勝可敗 | PASS | rules.ts:142–153 |
| C | 兩種戰術不同結果 | PASS | command-results.json |
| C | 重試 | PASS | PlayableL03.tsx:145–150, 352–356 |
| C | 無重複結算或卡回合 | PASS | PlayableL03.tsx:138–175 |
| C | 解析度與鍵盤 | PASS | P1v～P1v4 回歸，PlayableL03.tsx:269–278 |
| C | 自動化與真人分開 | PASS | VERIFICATION.md |
| D | SRD/CC-BY/no WotC/Rule Contract | PASS | 本輪沒有新規則 |
| D | AGENTS.md、未合併 main | PASS | 只在指定分支 |

Note: GPT's own total was 13 PASS / 2 FAIL / 2 N/A, but the table above has 18 rows: 14 PASS, 2 FAIL and 2 N/A.
