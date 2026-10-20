// 第二章　灰燈廢塔（本批寫 L05–L06；L07–L08 待 Codex 依 LEVEL-LIST 續寫）

=== L05_pre ===
#scene:L05_pre #bg:灰燈廢塔外環_晨霧
灰燈學院的廢塔立在斷崖上，塔身爬滿會發光的符文藤。外環的石像守衛還在巡邏，像沒人通知它們學院已經關門。
{ k1_gate == "open":
    樹林裡一支箭釘在凱倫腳邊。一個獵裝女子從樹上躍下。
    #speaker:歐朵
    「渡口那晚開閘的人是你？我在下游撈起了十二個人。他們說，是一個舊騎士讓船進來的。」
    #speaker:歐朵
    「我欠你一條路。廢塔的外環我熟，跟我走。」
    ~ odo_recruited = true
    #flag:odo_recruited
- else:
    #speaker:蕾絲
    「外環的守衛只認學院的燈。我們沒有燈，只能硬闖。」
}
石像之間有一個蜷縮的人影，手臂上爬著黑色的裂紋，在晨霧裡發著暗紅的光。
#speaker:薩溫
「別、別殺我……我不是他們的人了。我逃出來了。」
#speaker:托瑪
「他身上有裂潮。這是裂潮之子的烙印。」
#speaker:蕾絲
「昨晚想把我弟弟推進河裡的，就是這群人。」
#speaker:薩溫
「我知道塔裡有什麼。我知道他們為什麼要推倒界碑。讓我跟著你們——求你。」
// Q-S1：是否收留薩溫
* [「跟上。但你敢背叛，我第一個砍你。」]
    ~ sawin_sheltered = true
    ~ trust_sawin += 2
    ~ trust_lis -= 1
    #flag:sawin_sheltered
    #speaker:薩溫
    「……謝謝。我會證明的。」
    #speaker:蕾絲
    「我會盯著你。」
* [請托瑪先替他驅除裂潮再說。]
    ~ sawin_sheltered = true
    ~ trust_thoma += 1
    #flag:sawin_sheltered
    #speaker:托瑪
    「我只能壓住它，沒辦法拔出來。……忍著點。」
    薩溫咬著牙，沒有叫出聲。
* [「我們不收裂潮之子。走吧。」]
    ~ trust_sawin -= 2
    ~ trust_lis += 1
    #speaker:薩溫
    「好……好。那你們進塔的時候，記得別碰三樓的鏡子。」
    他踉蹌地消失在霧裡。
-
-> L05_battle

=== L05_battle ===
#battle:L05 #objective:突破外環，啟動兩座學院燈柱以停止石像守衛
#trigger:turn1
{odo_recruited:「石像只追會動的東西。站在燈柱的影子裡！」|凱倫注意到石像總會繞過燈柱的影子。}
#trigger:pillar_lit #speaker:托瑪
「燈柱裡也有聲音……這座塔也在收容什麼。」
-> L05_post

=== L05_post ===
#scene:L05_post
石像一座座停下，跪向塔門。門上刻著一行學院銘文：「凡守護者，皆被守護之物所囚。」
{ sawin_sheltered:
    #speaker:薩溫
    「裂潮之子把這句話刻在每個祭壇上。他們說，界碑就是監牢。」
}
-> L06_pre

=== L06_pre ===
#scene:L06_pre #bg:廢塔書庫
書庫裡的書架懸在半空，緩慢地繞著中央的星盤轉動。星盤上綁著一個女子，四周是一圈正在收緊的符文光環。
#speaker:伊瑟拉
「別過來！光環會把靠近的人一起——等等，你們不是議會的人？」
#speaker:凱倫
「我們來找韋恩教授的學生。」
#speaker:伊瑟拉
「那就是我。先把我放下來，再自我介紹也不遲。」
{ notes_saved:
    #speaker:魏德
    「伊瑟拉小姐！教授的筆記，我帶出來了！」
    #speaker:伊瑟拉
    「……你們保住了它？」她的聲音有一瞬間不穩。「謝謝。」
    ~ trust_isera += 1
- else:
    #speaker:伊瑟拉
    「教授的筆記呢？他寄去渡口的那批？」
    #speaker:凱倫
    「……沉在河裡了。為了讓三艘船進港。」
    伊瑟拉沉默了很久。
    -> notes_lost
}
-> L06_battle

= notes_lost
#speaker:伊瑟拉
「三艘船。你算過那值不值得嗎？」
* [「我沒算。我只是不想再封一次門。」]
    ~ trust_isera += 1
    #speaker:伊瑟拉
    「……真是不像騎士的回答。我反而比較相信。」
* [「船上的人比筆記重要。」]
    #speaker:伊瑟拉
    「說得輕鬆。那些筆記裡，記著好幾千個人的名字。」
-
-> L06_battle

=== L06_battle ===
#battle:L06 #objective:在光環收緊前（八回合）轉動三座書架，打開解鎖路徑；擊敗書庫守衛「索引者」
#trigger:turn2 #speaker:伊瑟拉
「左邊那座書架，符文是倒的！轉兩格，別轉三格！」
#trigger:turn5 #speaker:伊瑟拉
「光環快碰到星盤了，如果它碰到，我會變成這座塔的燈芯！」
#trigger:boss_half
{sawin_sheltered:「它怕裂潮！讓我來——」|索引者的身體閃了一下，像在避開什麼。}
-> L06_post

=== L06_post ===
#scene:L06_post
光環碎成灰燼。伊瑟拉從星盤上滑落，凱倫接住了她。
#speaker:伊瑟拉
「……你的手很冷。」
#speaker:凱倫
「是你的手太燙。符文燒的。」
她看了他一眼，沒有把手抽回去。
~ trust_isera += 1
#speaker:伊瑟拉
「教授不是失蹤。是被帶走的。帶他走的人，戴著大司碑的指環。」
#speaker:托瑪
「大司碑……誓院跟他到底做了什麼交易？」
塔頂傳來鐘聲。一下，兩下，三下。整座塔的符文同時熄滅。
#speaker:伊瑟拉
「這是學院的召回鐘。……他來了。」
-> L07_pre

=== L07_pre ===
// TODO（Codex）：依 docs/story/levels/LEVEL-LIST.md 與 ANTAGONIST.md 第二章出場寫 L07 塔頂星室：莫瑞安對峙並獲勝、帶走小昆。
#scene:L07_pre
（L07 腳本待寫。）
-> END
