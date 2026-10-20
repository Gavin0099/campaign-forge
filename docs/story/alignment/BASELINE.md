# S0 基準與來源差異

核對日：2026-10-21（Asia/Taipei）。

| 類別 | 觀察 |
| --- | --- |
| 遠端 main | 505fca779ca92c0ecd9f8fab263284e04423e723 |
| 遠端故事 | 4f5e447c9e45cc47ecc34d4751c4db49923627b8 |
| 既有本機 | 僅 main worktree，乾淨；沒有本機故事 branch 或 staged／unstaged 故事稿 |
| 隔離位置 | 本企劃 ignored scratch/narrative-alignment，正常 linked worktree，story/strengthen-narrative 追蹤既有 origin 分支 |
| 三項缺稿 | 在兩 refs 的 docs／memory 搜尋「貝恩／燈號簿／洩潮地」均沒有命中；本輪不能把描述當成已存在的稿本 |
| Owner 回答 | 表示在 GitHub branch；再查 ls-remote 仍僅上述兩 refs，已請求分支名或檔案連結。這是使用者陳述，非已定位來源 |
| 現有內容 | L01–L07、FLAGS、同伴弧線、反派、結局矩陣；L08–L28 只有既有提案表，本輪不擴寫 |

正典順序：DECISIONS → STORY → COMPANION-ARCS／ANTAGONIST／ENDINGS → levels／FLAGS → Ink；Ink 變數命名以 globals 為準。狀態有衝突時修正工作稿對應，不能讓程式悄悄取代上層設定。

`main` 的 VD3 是工程展示基準。席恩／莉妲／奧倫／瑪芮與測試法師不等於凱倫／蕾絲／托瑪／伊瑟拉；不藉名稱映射宣告角色設計完成。

## 已知待核對問題

- 原 walker 收集錯誤但不設定失敗 exit；僅終點少量檢查，不能證明物件／知識／中途出場合理。
- 托瑪 core 拒絕台詞只在 trust >= 3；現有角色表要求底線與信任無關。約 2% 是外部描述，尚無對應資料與分母，不當成玩家機率。
- L06「如果是我，我會選另一邊」在封閘路線也出現，與後續偏重名鑰的論述矛盾。
- L07 薩溫在其他兩路受創只有角色表提到，Ink 沒有狀態與後果段落；三物件救援的時空限制缺具體交代。
- STORY 將「植入碎片」稱為「與生俱來」，與既有背景矛盾。修正文義，仍不決定 Sorcerer 正式規則。

## 缺稿的處理

燈號簿不是星盤／名鑰／未來先民名冊的別名。沒有原稿，不新增其持有者、不替貝恩發明身份、不將洩潮地寫入 Ink。三項保留為來源待核對，收到精確稿本再整合。

Owner 後續澄清：這三項來自先前代理進度描述，不是其實際讀到的 GitHub 文件；指示找不到就標 SOURCE_NOT_FOUND，其餘工作繼續。本機唯讀擴查結果：stash 清單為空，原有 main 乾淨，worktree 清單只有 main 與本輪新建的隔離工作區；在本企劃 docs／memory／scratch 文字稿擴查亦無原稿（排除本輪描述缺稿的報告）。**三項正式標記 SOURCE_NOT_FOUND**，不是修復完成、不是 Owner 已批准的新設定。
