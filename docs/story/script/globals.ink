// 《碑誓》全域狀態。信任為隱藏數值，對應 COMPANION-ARCS 的四段：0–1 疏離、2–3 同行、4–5 信賴、6+ 誓約。
// 數值只是故事狀態，不是戰鬥數值。寫入／讀取點見 docs/story/FLAGS.md。

VAR k1_gate = ""          // "open" 開閘救最後一艘船 / "sealed" 封閘保學院車隊
VAR teo_fate = ""         // "" 未定 / "safe" 隨最後一艘船靠岸 / "missing" 封閘後隨船失蹤
VAR notes_saved = false   // 韋恩教授筆記（含「名鑰」，可依名字釋放特定亡魂）
VAR maggie_alive = true   // 燈芯屋老闆娘瑪歌
VAR wick_wall = 0         // L01／L04 在燈芯牆掛上名字的隊員數
VAR odo_recruited = false
VAR sawin_sheltered = false
VAR quin_bond = 0         // 隊伍與學徒小昆的連結（L05–L06）
VAR quin_taken = false    // L07 小昆被大司碑帶走
VAR starplate_saved = false // L07 搶回星盤（名鑰副本）
VAR l07_saved = 0         // L07 撤出的學院倖存者人數（0–6）
VAR trust_lis = 1
VAR trust_thoma = 2
VAR trust_isera = 1
VAR trust_sawin = 1
VAR trust_odo = 2
VAR tide = 1              // 裂潮刻度 1–6
VAR key_explained = false // L01 魏德已交代名鑰用途；不是已證實收魂
VAR soul_cycle_known = false // L07 對峙後隊伍得知迴圈
VAR notes_holder = "weide" // weide / river；是否保有用 notes_saved
VAR starplate_holder = "tower" // tower / party / moriane（塔頂可攜副本）
VAR isera_recruited = false
VAR sawin_fate = "absent" // absent / party / injured / protected
VAR l07_protected = "" // quin / starplate / sawin
VAR thoma_refused = false // 核心道德拒絕：與信任無關
VAR thoma_public = false // 是否敢向莫瑞安公開質問：由前期行動支持

=== function stage(t) ===
{
  - t >= 6:
    ~ return "誓約"
  - t >= 4:
    ~ return "信賴"
  - t >= 2:
    ~ return "同行"
  - else:
    ~ return "疏離"
}

=== function name_key() ===
~ return notes_saved || starplate_saved
