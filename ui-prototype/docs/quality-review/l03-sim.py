"""Paper-prototype simulator for the L03 playable spec (docs/quality-review/L03-PLAYABLE-SPEC.md).

Standalone and deterministic. It is NOT game code and not a rules decision (G005):
it only checks that the provisional numbers make L03 losable by a passive player
and winnable by a reasonable one. Run:  python -I l03-sim.py
"""
from collections import deque

ROWS = [
    "FFF.~~.....",
    "FF..~~.....",
    "F...~~..F..",
    "....~~.....",
    "...RRRRRR..",
    "....~~.....",
    "....~~...FF",
    "....~~..FFF",
    "....~~.FFFF",
]
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def terrain_ok(c, gate):
    x, y = c
    if not (0 <= y < 9 and 0 <= x < 11):
        return False
    if ROWS[y][x] == "~":
        return False
    return not (gate == "open" and y == 4 and x in (4, 5))


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Unit:
    def __init__(s, uid, side, pos, hp, move, rng, dmg, heal=0):
        s.id, s.side, s.pos, s.hp, s.max = uid, side, pos, hp, hp
        s.move, s.rng, s.dmg, s.heal = move, rng, dmg, heal

    def __repr__(s):
        return f"{s.id}@{s.pos}:{s.hp}"


class Battle:
    def __init__(s, gate):
        s.gate, s.turn, s.log = gate, 0, []
        s.allies = [
            Unit("karen", "ally", (2, 5), 9, 3, 1, 3),
            Unit("lace", "ally", (1, 3), 7, 3, 2, 2),
            Unit("thoma", "ally", (1, 4), 8, 3, 2, 0, heal=3),
        ]
        s.enemies, s.objects = [], set()
        if gate == "open":
            s.winch, s.progress = (2, 1), 0
            s.objects.add(s.winch)
            s.spawns = {0: [(1, 8), (3, 8)], 1: [(0, 8)], 2: [(3, 0)], 3: [(2, 8)]}
        else:
            s.convoy, s.convoy_hp = (8, 4), 12
            s.convoy_path = [(x, 4) for x in range(7, -1, -1)]
            s.spawns = {0: [(6, 1), (6, 7)], 1: [(3, 2)], 2: [(6, 6)], 3: [(3, 6)], 4: [(6, 2)]}
        s.spawn(0)

    # --- helpers ---
    def units(s):
        return [u for u in s.allies + s.enemies if u.hp > 0]

    def occupied(s, ignore=None):
        occ = {u.pos for u in s.units() if u is not ignore} | s.objects
        if s.gate == "sealed":
            occ.add(s.convoy)
        return occ

    def reach(s, u):
        """Cells u can end on: BFS through terrain, blocked by the other side's units."""
        foes = {v.pos for v in s.units() if v.side != u.side}
        block = foes | s.objects | ({s.convoy} if s.gate == "sealed" else set())
        seen, q = {u.pos: 0}, deque([u.pos])
        while q:
            c = q.popleft()
            if seen[c] == u.move:
                continue
            for dx, dy in DIRS:
                n = (c[0] + dx, c[1] + dy)
                if n in seen or not terrain_ok(n, s.gate) or n in block:
                    continue
                seen[n] = seen[c] + 1
                q.append(n)
        occ = s.occupied(ignore=u)
        return [c for c in seen if c not in occ]

    def path_len(s, start, goal_cells, mover):
        foes = {v.pos for v in s.units() if v.side != mover.side}
        block = foes | s.objects | ({s.convoy} if s.gate == "sealed" else set())
        seen, q = {start: 0}, deque([start])
        while q:
            c = q.popleft()
            if c in goal_cells:
                return seen[c]
            for dx, dy in DIRS:
                n = (c[0] + dx, c[1] + dy)
                if n in seen or not terrain_ok(n, s.gate) or n in block:
                    continue
                seen[n] = seen[c] + 1
                q.append(n)
        return 99

    def spawn(s, t):
        occ = s.occupied()
        for i, c in enumerate(s.spawns.get(t, [])):
            if c in occ:
                continue
            if s.gate == "open":
                s.enemies.append(Unit(f"knight{len(s.enemies)}", "enemy", c, 5, 3, 1, 3))
            else:
                s.enemies.append(Unit(f"crawler{len(s.enemies)}", "enemy", c, 4, 2, 1, 2))

    def neighbours(s, c):
        return {(c[0] + dx, c[1] + dy) for dx, dy in DIRS}

    # --- enemy phase ---
    def enemy_phase(s):
        if s.gate == "open":
            # A knight turns the winch only if it was already adjacent when the
            # enemy phase began, i.e. it survived a whole player phase there.
            ready = sum(1 for e in s.enemies if e.hp > 0 and dist(e.pos, s.winch) == 1)
            s.progress += ready
            if ready:
                s.log.append(f"T{s.turn} gate progress +{ready} -> {s.progress}")
        target = s.winch if s.gate == "open" else s.convoy
        goals = {c for c in s.neighbours(target) if terrain_ok(c, s.gate)}
        for e in [e for e in s.enemies if e.hp > 0]:
            options = s.reach(e)
            best = min(options, key=lambda c: (s.path_len(c, goals, e), dist(c, target)))
            e.pos = best
            if s.gate == "sealed" and dist(e.pos, s.convoy) == 1:
                s.convoy_hp -= e.dmg
                s.log.append(f"T{s.turn} {e.id} hits convoy -> {s.convoy_hp}")
                continue
            adj = [a for a in s.allies if a.hp > 0 and dist(a.pos, e.pos) <= e.rng]
            if adj:
                a = min(adj, key=lambda a: a.hp)
                a.hp -= e.dmg
                s.log.append(f"T{s.turn} {e.id} hits {a.id} -> {a.hp}")

    def convoy_phase(s):
        for _ in range(2):
            if not s.convoy_path:
                return
            nxt = s.convoy_path[0]
            if nxt in {u.pos for u in s.units()}:
                s.log.append(f"T{s.turn} convoy blocked at {s.convoy}")
                return
            s.convoy = s.convoy_path.pop(0)

    def outcome(s):
        if s.allies[0].hp <= 0:
            return "LOSE: 凱倫倒下"
        if s.gate == "open":
            if s.progress >= 3:
                return "LOSE: 閘門落下"
            if s.turn >= 5:
                return "WIN: 三船靠岸"
        else:
            if s.convoy_hp <= 0:
                return "LOSE: 車隊被毀"
            if s.convoy == (0, 4):
                return "WIN: 車隊過橋"
            if s.turn >= 7:
                return "LOSE: 時限到"
        return None

    def run(s, policy):
        while True:
            s.turn += 1
            policy(s)
            s.enemy_phase()
            if s.gate == "sealed":
                s.convoy_phase()
            r = s.outcome()
            if r:
                return r
            s.spawn(s.turn)


# --- player policies ---
def passive(b):
    pass


def attack_best(b, u):
    if u.heal:
        hurt = [a for a in b.allies if a.hp > 0 and a.hp < a.max and dist(a.pos, u.pos) <= u.rng]
        if hurt:
            a = min(hurt, key=lambda a: a.hp - a.max)
            a.hp = min(a.max, a.hp + u.heal)
        return
    foes = [e for e in b.enemies if e.hp > 0 and dist(e.pos, u.pos) <= u.rng]
    if foes:
        e = min(foes, key=lambda e: e.hp)
        e.hp -= u.dmg


def objective_pressure(b, e):
    """How close an enemy is to doing damage to the objective (lower = more urgent)."""
    target = b.winch if b.gate == "open" else b.convoy
    return dist(e.pos, target)


def hold_line(posts):
    """Objective-aware play: hit the enemy nearest the objective if one is in range
    from a reachable cell; otherwise move toward a post. Thoma stays near Karen and
    heals. On the sealed map, allies avoid standing on the convoy's remaining path."""
    def policy(b):
        ahead = set(b.convoy_path) if b.gate == "sealed" else set()
        for u in b.allies:
            if u.hp <= 0:
                continue
            post = posts[b.gate][u.id]
            options = b.reach(u) + [u.pos]
            if b.gate == "open":  # stay near the winch instead of chasing south
                options = [c for c in options if dist(c, b.winch) <= 3] or options
            penalty = lambda c: 5 if c in ahead else 0
            if u.heal:
                karen = b.allies[0]
                u.pos = min(options, key=lambda c: (penalty(c), max(0, dist(c, karen.pos) - 2), dist(c, post), c))
            else:
                foes = [e for e in b.enemies if e.hp > 0]
                scored = []
                for c in options:
                    hit = [e for e in foes if dist(e.pos, c) <= u.rng]
                    if hit:
                        e = min(hit, key=lambda e: (objective_pressure(b, e), e.hp))
                        scored.append((penalty(c), objective_pressure(b, e), dist(c, post), c))
                if scored:
                    u.pos = min(scored)[3]
                else:
                    u.pos = min(options, key=lambda c: (penalty(c), dist(c, post), c))
            attack_best(b, u)
    return policy


def chase(b):
    """Greedy: every attacker charges the nearest enemy; ignores the objective."""
    for u in b.allies:
        if u.hp <= 0:
            continue
        foes = [e for e in b.enemies if e.hp > 0]
        if foes and not u.heal:
            near = min(foes, key=lambda e: dist(e.pos, u.pos))
            u.pos = min(b.reach(u), key=lambda c: (abs(dist(c, near.pos) - u.rng), c))
        attack_best(b, u)


POSTS = {
    # open: plug the 4-wide west-bank corridor two rows south of the winch
    "open": {"karen": (1, 3), "lace": (3, 1), "thoma": (2, 2)},
    # sealed: clear the bridge mouth ahead of the convoy without standing on row 4
    "sealed": {"karen": (7, 3), "lace": (3, 3), "thoma": (6, 5)},
}

if __name__ == "__main__":
    for gate in ("open", "sealed"):
        for name, pol in (("passive", passive), ("chase", chase), ("hold", hold_line(POSTS))):
            b = Battle(gate)
            result = b.run(pol)
            print(f"{gate:6} {name:7} T{b.turn}: {result} | allies {b.allies}"
                  + (f" | gate {b.progress}" if gate == "open" else f" | convoy {b.convoy}:{b.convoy_hp}"))
