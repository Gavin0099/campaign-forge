extends RefCounted
## SPIKE TEST VALUES ONLY. No canon, SRD, G005 or L03 rules.
const SIZE = Vector2i(24,18)
const TURN_LIMIT = 15
const SEED = 24018
const ALERT_RADIUS = 6
## SPIKE06 AI test values, not canon. Manhattan distances; activation latches.
const AI = {"march_turn":6,"neighbour_radius":5,"support_radius":3,"bodyguard_radius":3,"intercept_radius":6}
const LEADER_CONTEST_RADIUS = 2
const REINFORCEMENT_TURN = 5
const ENTRIES = [Vector2i(23,8),Vector2i(23,9),Vector2i(23,10)]
const STATS = {
	"melee":{"move":4,"hp":8,"min_range":1,"max_range":1,"damage":2,"knockback":true,"forest_extra":0},
	"ranged":{"move":3,"hp":6,"min_range":2,"max_range":3,"damage":2,"knockback":false,"forest_extra":0},
	"mobile":{"move":6,"hp":6,"min_range":1,"max_range":1,"damage":2,"knockback":true,"forest_extra":1},
	"knight":{"move":4,"hp":6,"min_range":1,"max_range":1,"damage":2,"knockback":true,"forest_extra":0},
	"leader":{"move":4,"hp":10,"min_range":1,"max_range":1,"damage":2,"knockback":true,"forest_extra":0}}
const TERRAIN = {
	".":{"name":"荒地","cost":1},"=":{"name":"道路","cost":1},
	"f":{"name":"森林","cost":2},"w":{"name":"淺灘","cost":2},
	"~":{"name":"深水","cost":0},"^":{"name":"峭壁","cost":0},
	"d":{"name":"守備高地（僅地標）","cost":1}}
const DEPLOYMENT = [
	["thoma","ally","melee",Vector2i(3,10),"party"],
	["guard","ally","melee",Vector2i(4,9),"party"],
	["bow-1","ally","ranged",Vector2i(3,8),"party"],
	["bow-2","ally","ranged",Vector2i(3,11),"party"],
	["scout-1","ally","mobile",Vector2i(2,8),"party"],
	["scout-2","ally","mobile",Vector2i(2,11),"party"],
	["knight-1","enemy","knight",Vector2i(14,8),"front"],
	["knight-2","enemy","knight",Vector2i(14,10),"front"],
	["knight-3","enemy","knight",Vector2i(11,15),"south"],
	["knight-5","enemy","knight",Vector2i(18,3),"flank"],
	["knight-8","enemy","knight",Vector2i(19,8),"reserve"],
	["leader","enemy","leader",Vector2i(20,9),"leader"]]

static func build() -> Dictionary:
	# Authored geometry: east river, two road crossings and a northern ford.
	var rows: Array[String] = []
	for y in range(SIZE.y):
		var row := ""
		for x in range(SIZE.x):
			var tile := "."
			if y in [9,10] or x==5: tile = "="
			elif (y in [4,5,6] and x in range(6,14)) or (y>=13 and x in range(8,13)): tile = "f"
			if x==15: tile = "w" if y in [5,6] else ("=" if y in [9,10] else "~")
			if y in [0,17] and x in range(9,13): tile = "^"
			if x in [20,21] and y in [9,10]: tile = "d"
			row += tile
		rows.append(row)
	return {"size":SIZE,"rows":rows,"stats":STATS.duplicate(true),"terrain":TERRAIN.duplicate(true),
		"turn_limit":TURN_LIMIT,"seed":SEED,"alert_radius":ALERT_RADIUS,"ai":AI.duplicate(true),"leader_contest_radius":LEADER_CONTEST_RADIUS,
		"objective":"defeat_leader","hold_point":Vector2i(20,9),"reinforcement_turn":REINFORCEMENT_TURN,
		"entries":ENTRIES.duplicate(),"entry_label":"東側渡口入口","reinforcement_kinds":["knight","knight","knight"],
		"deployment":DEPLOYMENT.duplicate(true),"label":"PLACEHOLDER / SPIKE TEST VALUES","line_of_sight":"centre supercover; cliff/deep water/units block intermediate; forest line/target cover -1 min1; exact corners check both sides"}
