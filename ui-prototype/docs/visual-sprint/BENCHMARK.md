# Visual Quality Sprint — benchmark

2026-10-20；基準 commit `6f5109e`。評估對象是候選 A 的展示畫面，沒有選定正式故事或角色。以下是代理對官方截圖的視覺觀察，不是玩家研究或商業品質認證。

## 官方頁面與實際截圖

| 遊戲 | 官方來源 | 本輪實際檢視 | 可借鑑的方法 |
| --- | --- | --- | --- |
| The Banner Saga | https://store.steampowered.com/app/237990/The_Banner_Saga/ | publisher gallery 0：大廳戰場；2：雪地行旅 | 大塊明暗、人物剪影、色彩節制；場景留白承載敘事 |
| Fell Seal: Arbiter's Mark | https://store.steampowered.com/app/699170/Fell_Seal_Arbiters_Mark/ | gallery 1：洞穴戰場；gallery 0 是宣傳評分圖，排除戰場比較 | 畫面可分出可行走平面；藍色移動格與地景、角色相互區別 |
| Tactics Ogre: Reborn | https://store.steampowered.com/app/1451090/Tactics_Ogre_Reborn/ | gallery 0：角色對話；2：技能特效 | 對話的說話者層級與選項；效果以局部亮度指出作用位置 |

原始官方 HTML、Steam appdetails JSON 與六張官方圖已保存於本工作區 `scratch/visual-benchmarks/`，僅供私下研究，不提交商業素材到公開 repo、不放入 app、不作生成參考輸入。URL、雜湊及用途見 [reference-sources.json](reference-sources.json)。另外查閱 Square Enix 官方產品與介紹頁：https://www.square-enix-games.com/en_US/games/tactics-ogre-reborn 、https://www.square-enix-games.com/en_US/news/tactics-ogre-reborn-preview 。

## 差距矩陣

| 面向 | 成熟作品截圖的可見方法 | Campaign Forge Before | 本輪動作與驗收 |
| --- | --- | --- | --- |
| 人物 | 外輪廓、服裝大色塊、道具能區分身份 | 原立繪細節足夠，但有棕底，頭像用不穩定的共用裁切；小人偏Q版 | 透明立繪；四人各自裁切規格；綠／青／酒紅／赭黃與地圖筒／醫藥袋／盾／船鉤固定 |
| 戰場 | 行走面、遮擋物與角色站位對得上 | 河道與資料格偏移；部署小地圖只縮放底圖，無相同地形生成規則 | 以原始11×9資料生成共享地形層；斜俯視投影與點擊格同源，逐格比對 |
| 配色 | 地景低對比，交互狀態與角色局部高對比 | 全圖黃綠細節偏亮；白色格框與粗名稱條搶注意力 | 冷河水、苔綠地面、暖象牙文字；青移動／金選取／朱紅敵方，另加線型及符號 |
| 構圖 | 戰場主體占大面積；資訊有主次，不分散視線 | 棋盤與三個相同重點的資訊盒並排，選取角色缺少視覺錨點 | 主戰場＋角色檢視＋短指令列，目標、回合與技能預覽集中，次要紀錄可展開 |
| 可讀性 | 角色腳點、目標與行動範圍分層 | 小人姓名帶和生命數字密集；沒有生命上限比例或動作視覺反應 | 角色底座與小血條；選取卡保留姓名與HP數字；預覽幽靈、確認後短移動／打擊／傷害數字 |
| 敘事畫面 | 說話者、表情與文字平衡 | 舊地圖當對話底圖；人物窄條與多面板像工具畫面 | 場景插畫與完整半身立繪，保留原對白、已知情報及兩個代價選項 |
| 商店小圖 | 有明確焦點、能看出類型 | 縮圖後白格框先於角色 | 產生實際1080p戰鬥圖的640×360／460×259縮圖，代理目視＋待人類審圖 |

## 品質判定規則

商品名稱提醒：另有同名 [Campaign Forge 的 Steam 頁面](https://store.steampowered.com/app/4918080/)，本次查閱顯示預計2026-11-27推出。這只是命名風險的觀察，沒有變更repo名稱或替本企劃定正式商品名；未來上市命名另行決策。

功能通過要求兩條原流程、角色缺席、未確認撤銷、確認效果、結果回戰役與鍵盤操作不退化。視覺技術通過要求共同座標、裁切無鄰角污染、720p重要操作可達、無橫向溢出。美術是否達到「值得陌生玩家觀看」留待 Gavin／人類美術審查，不能由 build 或代理自評取代。
