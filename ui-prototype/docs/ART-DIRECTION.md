# 美術提案與來源

2026-10-20，四張圖均使用 **built-in image_gen** 生成，並將原始 PNG 複製到本工作區；沒有 API CLI 呼叫或購買素材。

| 檔案 | 用途 | 尺寸 |
| --- | --- | --- |
| public/art/party-v1.png | 席恩、莉妲、奧倫、瑪芮四人立繪圖集；人物外觀提案 | 1536×1024 |
| public/art/units-v1.png | 三名我方、兩名敵方的獨立戰場小人圖集；透明背景 | 1983×793 |
| public/art/battlefield-v1.png | 渡口戰場底圖，同時用於劇情場景與部署預覽 | 1387×1134 |
| public/art/campaign-v1.png | 戰役旅程地圖；場景地理為展示假設 | 1672×941 |

精確提示與圖像雜湊分別見 [art-prompts.json](art-prompts.json)、[art-manifest.json](art-manifest.json)。人物和圖片路徑在 `src/data.ts` 的 scenario / artwork；渲染採 CSS 圖集，不修改生成原檔。立繪依四欄、小人依五欄排列，替換時需維持圖集配置或同步改 CSS。小人沒有動作幀，不能視為可直接交付正式遊戲的角色動畫。

## 參考的工作方法

參考使用者指定的 [TacticalGo character-style skill](https://github.com/Gavin0099/TacticalGo/blob/31ac5413d4b20b6f4cb95048dc8e73a0ea55e325/.agents/skills/tacticalgo-character-style/SKILL.md) 與 [game-feel skill](https://github.com/Gavin0099/TacticalGo/blob/31ac5413d4b20b6f4cb95048dc8e73a0ea55e325/.agents/skills/tacticalgo-game-feel/SKILL.md)：角色身分一致、立繪與小人分開、保留原稿與提示、用實際遊戲畫面檢查選取／預覽／確認。未匯入該專案的角色、美術、程式或平台限制。

曹操傳／孔明傳只作格線戰場與人物敘事的體驗參考；沒有擷取商業遊戲圖片，也沒有仿作其人物或介面配置。

## 視覺判斷與待驗證

人物採成熟插畫，戰場小人簡化比例以辨識職責。上左光源、土色與低飽和綠藍保持一致。棋格以互動層定義，地景繪畫與格位只是近似對齊，正式關卡需要按正式地形資料重製或拆成 tiles。

已在 1920×1080 與 1280×720 實際戰場檢視；未宣稱完成獨立 32/48/64 px 美術 QA、Steam/原生引擎測試或正式商用法律審查。這些圖是生成展示提案，尚未經擁有者選定人物外觀，也不構成故事定案或對素材授權的額外承諾。

## 第三方依賴

依賴版本見 package-lock.json；React、React DOM、Vite 及多數工具為 MIT，TypeScript 為 Apache-2.0，實際各套件授權原文見 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。TypeScript 官方 tarball 保存於 vendor 以避免當時 registry metadata 連線不穩。故事企劃與生成美術沒有新增開源 LICENSE。
