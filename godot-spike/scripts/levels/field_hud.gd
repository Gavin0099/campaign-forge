extends CanvasLayer
var battle
var root: Control
var title: Label
var objective: Label
var notice: Label
var selected: Label
var inspect: Label
var debug: Label
var end_button: Button
var wait_button: Button
var confirm_button: Button
var result_panel: Panel
var result_label: Label
var minimap
var minimap_panel: Panel
var indicators
var warning := {}
var minimap_collapsed := false
var camera_hints: Label
var threat_legend: Control

func panel(at: Vector2, dimensions: Vector2) -> Panel:
	var p := Panel.new()
	p.position=at
	p.size=dimensions
	var style := StyleBoxTexture.new()
	style.texture=preload("res://art/ui/field-frame.png")
	for side in [SIDE_LEFT,SIDE_TOP,SIDE_RIGHT,SIDE_BOTTOM]: style.set_texture_margin(side,12)
	p.add_theme_stylebox_override("panel",style)
	root.add_child(p)
	return p

func label(parent: Node, text: String, at: Vector2, size: int = 18, color: Color = Color("eee7d6")) -> Label:
	return battle.make_label(parent,text,at,size,color)

func button(parent: Node, text: String, at: Vector2, dimensions: Vector2, action: Callable) -> Button:
	var b := Button.new()
	b.text=text
	b.position=at
	b.size=dimensions
	b.add_theme_font_size_override("font_size",17)
	b.pressed.connect(action)
	parent.add_child(b)
	return b

func _ready() -> void:
	root=Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter=Control.MOUSE_FILTER_IGNORE
	add_child(root)
	var font := SystemFont.new()
	font.font_names=PackedStringArray(["Microsoft JhengHei","Noto Sans TC"])
	var theme := Theme.new()
	theme.default_font=font
	theme.default_font_size=18
	root.theme=theme
	var top := panel(Vector2(18,12),Vector2(850,96))
	title=label(top,"",Vector2(16,9),24,Color("d2b777"))
	objective=label(top,"",Vector2(18,44),17)
	notice=label(root,"",Vector2(34,122),20,Color("e5be7c"))
	threat_legend=Control.new()
	threat_legend.position=Vector2(34,158)
	threat_legend.mouse_filter=Control.MOUSE_FILTER_IGNORE
	root.add_child(threat_legend)
	var entries := [["移動","73b0a1"],["敵威脅","bd5742"],["可攻擊","d97045"],["LOS阻擋","909999"],["森林−1","d2b777"],["斥候攔截","9470d1"]]
	for i in range(entries.size()): label(threat_legend,"■ "+entries[i][0],Vector2(i*142,0),15,Color(entries[i][1]))
	var bottom := panel(Vector2(18,572),Vector2(1244,132))
	selected=label(bottom,"",Vector2(16,9),20,Color("d2b777"))
	inspect=label(bottom,"",Vector2(16,41),16)
	label(bottom,"Tab 選隊員 · IJKL 移游標 · Enter 選擇／確認 · T 換目標 · Esc／右鍵 取消",Vector2(16,79),15)
	label(bottom,"N 結束回合 · Space 等待 · G 格線 · V 威脅 · M 減少動態 · B 2× · X 略移動 · R 重來",Vector2(16,103),14)
	confirm_button=button(bottom,"確認 Enter",Vector2(813,18),Vector2(128,42),battle.confirm)
	wait_button=button(bottom,"等待 Space",Vector2(949,18),Vector2(126,42),battle.wait_selected)
	end_button=button(bottom,"結束回合 N",Vector2(1083,18),Vector2(144,42),battle.end_turn)
	debug=label(root,"",Vector2(30,180),16)
	debug.hide()
	result_panel=panel(Vector2(420,224),Vector2(440,230))
	result_label=label(result_panel,"",Vector2(26,22),26,Color("d2b777"))
	label(result_panel,"展示規則／美術均為 PLACEHOLDER\nR 或下方按鈕重新部署，改用另一條路線",Vector2(26,78),17)
	button(result_panel,"重新部署 R",Vector2(120,154),Vector2(200,46),battle.restart)
	result_panel.hide()
	minimap_panel=panel(Vector2(1012,12),Vector2(250,206))
	button(minimap_panel,"小地圖 P　□我方 △敵 ◆領袖",Vector2(8,6),Vector2(234,32),toggle_minimap)
	minimap=preload("res://scripts/levels/field_minimap.gd").new()
	minimap.battle=battle
	minimap.position=Vector2(12,48)
	minimap.size=Vector2(226,150)
	minimap.clip_contents=true
	minimap_panel.add_child(minimap)
	indicators=preload("res://scripts/levels/field_indicators.gd").new()
	indicators.battle=battle
	indicators.mouse_filter=Control.MOUSE_FILTER_IGNORE
	root.add_child(indicators)
	camera_hints=label(root,"WASD／方向鍵 捲動 · 中鍵 拖曳 · 滾輪 縮放 · O 全圖 · F 定位 · E 邊緣 OFF",Vector2(34,548),14)
	update_state()

func toggle_minimap() -> void:
	minimap_collapsed=not minimap_collapsed
	minimap.visible=not minimap_collapsed
	minimap_panel.size.y=44 if minimap_collapsed else 206

func warning_entries() -> Array:
	if battle.state.spawned: return []
	if not warning.is_empty(): return warning.entries
	return battle.state.level.entries if battle.state.warned else []

func warning_marker() -> Dictionary:
	var entries := warning_entries()
	return {} if entries.is_empty() else {"cell":entries[1],"count":entries.size(),"radius":12.0,"alpha":.55}

func on_event(event: Dictionary) -> void:
	if event.type=="reinforcement_warning": warning=event.duplicate(true)

func update_state() -> void:
	var s: Dictionary = battle.state
	threat_legend.visible=battle.threat_visible
	title.text="渡口・PLACEHOLDER  |  第 %d / %d 回合・%s" % [s.turn,s.level.turn_limit,"戰鬥結束" if s.status!="playing" else ("我方" if s.phase=="player" else "敵方")]
	objective.text="目標：擊敗領袖 ◆　失敗：托瑪倒下／超過 %d 回合　｜24×18・無迷霧・測試值" % s.level.turn_limit
	var u: Dictionary = battle.Rules.unit(s,battle.selected_id)
	selected.text="選擇隊員" if u.is_empty() else "%s　%s　HP %d/%d　移動 %d　射程 %d–%d　%s" % [battle.display_name(u),battle.kind_name(u.kind),u.hp,u.max_hp,s.level.stats[u.kind].move,s.level.stats[u.kind].min_range,s.level.stats[u.kind].max_range,"已行動" if u.acted else ("已移動／可攻擊或等待" if u.moved else "可移動後攻擊或等待")]
	if battle.Rules.scout_kit(s,u):
		selected.text="%s HP%d/%d · 移6 · 半血收割+1／鄰格攔截 · %s" % [u.id,u.hp,u.max_hp,"可撤離≤%d格" % u.get("retreat_left",0) if battle.Rules.can_escape(s,u) else ("已行動" if u.acted else "攻後剩餘移動撤離≤2格")]
	selected.add_theme_font_size_override("font_size",17 if battle.Rules.scout_kit(s,u) else 20)
	confirm_button.disabled=battle.busy or battle.pending.is_empty() or s.status!="playing"
	wait_button.disabled=battle.busy or u.is_empty() or (u.get("acted",true) and not battle.Rules.can_escape(s,u)) or u.get("side","")!="ally" or s.phase!="player" or s.status!="playing"
	end_button.disabled=battle.busy or s.status!="playing"
	result_panel.visible=s.status!="playing"
	if s.warned and not s.spawned:
		notice.text="增援：第 %d 回合，%s，3 名騎士（到場當回合休息）" % [s.level.reinforcement_turn,s.level.get("entry_label","東北入口")]
	if result_panel.visible:
		result_label.text=("勝利・領袖已敗" if s.status=="win" else "敗北・重新整隊")+" · 第 %d 回合" % s.turn
		result_label.add_theme_font_size_override("font_size",22)
		result_panel.get_child(result_panel.get_child_count()-1).grab_focus()
	debug.visible=battle.debug_visible
	debug.text="F1 DEBUG  ·  PLACEHOLDER\nzoom %.2f · 96px figures · 160×94.5px diamond\nM Reduced Motion: %s · B fast: %s · X skip move: %s\nAttacks: %d · last %.3fs" % [battle.camera.zoom.x,battle.reduced_motion,battle.fast_forward,battle.skip_enemy_movement,battle.attack_timings.size(),battle.impact.last_seconds]
	debug.text+="\nFirst contact: turn %d · JSON: .godot/spike05/live-telemetry.json" % battle.telemetry.first_contact_turn
	debug.text+="\nResult: %s / turn%d · last enemy phase %.3fs" % [s.status,s.turn,0.0 if battle.enemy_times.is_empty() else battle.enemy_times.back().seconds]
	for kind in battle.telemetry.totals:
		var t: Dictionary = battle.telemetry.totals[kind]
		debug.text+="\n%s move %.2f · attacks%d · dmg%d/%d · kills%d · idle%d" % [kind,float(t.move_steps)/maxi(1,t.unit_turns),t.attacks,t.damage_dealt,t.damage_taken,t.kills,t.idle_turns]

func hover(cell: Vector2i) -> void:
	var u: Dictionary = battle.Rules.occupant(battle.state,cell)
	var tile: String = battle.Rules.terrain(battle.state.level,cell)
	inspect.text="%s (%d,%d)　成本 %d%s" % [battle.state.level.terrain[tile].name,cell.x,cell.y,battle.Rules.cost(battle.state.level,cell,"melee"),"／高機動森林3" if tile=="f" else ""]
	if not u.is_empty():
		var stats: Dictionary = battle.state.level.stats[u.kind]
		inspect.text+="　｜%s・%s HP%d/%d　移%d／射程%d–%d" % [battle.display_name(u),battle.kind_name(u.kind),u.hp,u.max_hp,stats.move,stats.min_range,stats.max_range]
		if battle.Rules.scout_kit(battle.state,u): inspect.text+=" · 收割半血+1／鄰格停步／攻後撤≤2（總移≤6）"
		var shooter: Dictionary = battle.Rules.unit(battle.state,battle.selected_id)
		if not shooter.is_empty() and shooter.side!=u.side:
			var info: Dictionary = battle.Rules.attack_info(battle.state,shooter,u)
			inspect.text+=" · "+info.reason
