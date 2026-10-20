// 《碑誓》全域狀態。信任為隱藏數值，對應 COMPANION-ARCS 的四段：0–1 疏離、2–3 同行、4–5 信賴、6+ 誓約。
// 數值只是故事狀態，不是戰鬥數值。

VAR k1_gate = ""          // "open" 開閘救小舟 / "sealed" 封閘保車隊
VAR maggie_alive = true   // 燈芯屋老闆娘瑪歌
VAR teo_found = false     // 蕾絲的弟弟提歐
VAR notes_saved = false   // 伊瑟拉導師筆記
VAR odo_recruited = false
VAR sawin_sheltered = false
VAR quin_taken = false    // 學徒小昆被大司碑帶走
VAR trust_lis = 1
VAR trust_thoma = 2
VAR trust_isera = 1
VAR trust_sawin = 1
VAR trust_odo = 2
VAR tide = 1              // 裂潮刻度 1–6

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
