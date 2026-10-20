# VD3 — Skill Reference Matrix

查閱日：2026-10-20。**候選規則參考**，不是完整採用5e／2024規則，也不決定故事人物職業。席恩只示範非魔法軍官近戰；獨立測試法師具 Wizard 展示身份。SRD 事實與本輪視覺設計分欄，不能把動畫當作規則已實作。

主要來源：[官方SRD下載頁](https://www.dndbeyond.com/srd)、[英文SRD 5.2.1 PDF](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf)。以下頁碼為PDF印刷頁碼，與PDF閱讀器頁序一致。規則以中文摘要改寫，保留必要英文識別名稱；原文授權聲明見 SRD-NOTICE.md。

| 候選能力／來源頁 | 可用身份、來源 | 動作與成分 | 目標／距離／效果 | 資源、集中與期限 | 對應演出與UI回饋（本企劃提案） |
| --- | --- | --- | --- | --- | --- |
| Weapon attack；pp.14–15、47、89–91 | 非Fighter獨占；訓練／熟練依角色與武器，Fighter熟練簡易及軍用武器 | Attack action；非施法，V/S/M不適用 | 武器reach／range與傷害型別依武器表；一般近戰reach5ft；命中需攻擊擲骰對AC | 一般武器攻擊不消耗法術位；次數與特性另計；不需集中 | 預備、出手、刀刃接觸、hitstop、敵人後仰、回復。現有「固定3」仍只是UI示範，不宣稱SRD武器傷害 |
| Second Wind；pp.47–48 | Fighter1；職業體能能力，非法術 | Bonus Action；無V/S/M | 自身回復1d10＋Fighter等級HP | 初始2次，短休回1、長休全回；高等級次數見表；無集中 | 呼吸／穩住身體與HP回復，不做神聖光束；僅參考，未實作 |
| Magic Missile；p.146，Wizard pp.77–80 | Wizard／Sorcerer法表；本輪只給獨立測試Wizard；需準備且有可用法術位 | 1級Evocation；Action；V、S；無M | 可見生物、120ft；3枚力場飛彈，每枚1d4＋1 Force；可同／多目標，同時命中 | 瞬間、無集中；更高每級法術位多1枚 | 手勢凝聚→3枚分離飛彈→分配目標→同時命中／受擊→消散。本輪只視覺，不擲骰、不扣位、不改HP |
| Fire Bolt；p.132 | Wizard／Sorcerer法表；必須學得戲法 | Evocation cantrip；Action；V、S | 生物或物件、120ft；遠程法術攻擊命中1d10 Fire；未被穿戴攜帶的易燃物可點燃 | 瞬間、無集中、戲法不耗位；角色5/11/17級提升傷害骰 | 火種／火焰尾流／熱與燃燒；不可讓所有生物必定持續燃燒。僅參考，未實作 |
| Cure Wounds；p.121，Cleric pp.36–38 | 本表參考Cleric；也列於Bard／Druid／Paladin／Ranger法表；需準備及可用位 | 1級Abjuration；Action；V、S | 接觸一生物，回復2d8＋施法屬性修正HP | 瞬間、無集中；每提升1級位多2d8 | 手真正接觸目標，再顯示生命回復；不是遠程泛用光圈。僅參考，不把莉妲自動改成Cleric |
| Shield of Faith；p.162，法表pp.38、56 | Cleric／Paladin；需準備及可用位 | 1級Abjuration；Bonus Action；V、S、M（prayer scroll，可依一般材料／法器規則處理） | 60ft一生物，持續＋2 AC | 集中至多10分鐘；花1級以上法術位；非瞬間護盾 | 施放後保留低調護持輪廓、集中圖示與剩餘時間，失去集中才消散；僅參考，不沿用VD2一次性護印冒充此法術 |
| Sneak Attack；pp.61–62 | Rogue1；需Finesse或Ranged武器攻擊命中；有優勢，或目標5ft內有非Incapacitated盟友且攻擊沒有劣勢 | 隨合格攻擊觸發，不另耗Action；無V/S/M | 一生物，額外1d6，型別同武器；隨Rogue等級增長 | 每turn一次，不是每round一次；無法術位／集中 | 預覽先顯示資格理由，再表現趁隙精準命中；僅參考，不把背刺動畫等同資格判定 |

所有上述SRD參考材料均依 **CC BY 4.0**；這不是整個repo故事的授權，不新增故事LICENSE。沒有取得D&D商標、專有世界、角色或競品美術的使用權。法術位、準備法術、成分、命中與傷害等完整規則尚未導入；排練UI不假裝資源已消耗。

## 真正D&D遊戲的可借鑑方向

| 官方來源 | 核實事項 | 對本輪的設計推論／界線 |
| --- | --- | --- |
| [BG3官方Projectile Spell指南](https://docs.baldursgate3.game/index.php?title=Making_a_Projectile_Spell)、[Patch4](https://baldursgate3.game/news/patch-4-now-live_96) | 指南以Magic Missile為繞障礙飛彈例子；Patch4記錄它曾因地形未命中 | 推論：飛彈要真的連到指定生物，不能只在任意位置放光。只取表達原理，沒有導入BG3規則差異或複製動畫／音效 |
| [Solasta官方Game Info](https://www.solasta-game.com/solasta-crown-of-the-magister/game-info)、[SRD5.1授權公告](https://www.solasta-game.com/solasta-crown-of-the-magister/news/30-wotc-granted-us-a-license-to-use-the-dd-srd) | 團隊明述採SRD5.1；強調位置、高低與地形 | 推論：技能UI先講能力、範圍與目標。本輪仍平面既有渡口，不新增高地、掩護或正式職業系統；Solasta5.1不作5.2.1數值來源 |

官方網站圖片與影片僅供研究觀看；不複製進app、不打包公開。這份來源與機制比較不是自稱已完成BG3或Solasta的動畫品質。
