# 規則改編契約（範本）

**狀態　範本。** 規則基礎（DECISIONS G005）未決前，本檔只提供欄位與格式，不填正式數值。依 [dnd-framework skill](../../.codex/skills/dnd-framework/SKILL.md) 使用。建議以 SRD 5.2.1 為來源候選，但這不等於採用完整 5.5e 戰鬥規則。

## 欄位

| 欄位 | 說明 |
| --- | --- |
| `id` | 本遊戲能力 ID（英文 snake_case） |
| `name_zh` | 原創中文名稱 |
| `source_id` | SRD 版本＋章節，並註明所選授權；原創則 `ORIGINAL` |
| `class_id` | Fighter／Wizard／Cleric／Rogue／Ranger／Sorcerer 等 |
| `action_cost` | action／bonus_action／reaction／move |
| `resource_cost` | 法術欄、次數、冷卻、其他 |
| `targeting` | 射程（格）、形狀、LOS、掩體規則 |
| `resolution` | 攻擊或豁免、傷害、狀態與持續回合 |
| `adaptation_reason` | 與來源差異與理由（以 SRD 第 13 頁 Playing on a Grid 為基準） |
| `visual_contract` | 動畫動作、VFX、命中／受擊；連到美術規格 |
| `verification` | 自動化測試路徑、試玩紀錄路徑 |
| `story_hook` | 對應的角色或劇情（選填） |

## 範例佔位（G005 後填寫）

```yaml
id: example_guard_strike
name_zh: （待定）
source_id: TBD  # 例：SRD5.2.1 / CC-BY-4.0 / <章節>
class_id: Fighter
action_cost: TBD
resource_cost: TBD
targeting: { range_squares: TBD, shape: TBD, los: TBD, cover: TBD }
resolution: { check: TBD, damage: TBD, condition: TBD, duration_turns: TBD }
adaptation_reason: TBD
visual_contract: { animation: TBD, vfx: TBD, impact: TBD }
verification: { automated_test: TBD, playtest: TBD }
story_hook: 凱倫守線
```

任一欄為 TBD 時不得進入實作。
