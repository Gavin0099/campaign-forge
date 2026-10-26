"""Offline evidence only: no process launches, network, game art or rule edits."""
import hashlib
import json
import re
import shutil
import struct
from io import BytesIO
from pathlib import Path
from statistics import mean
from PIL import Image, ImageDraw
from package_spike03 import chunks

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / 'docs/evidence/spike05'


def read(name):
    raw = (OUT / name).read_bytes()
    return json.loads(raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig'))


def write(name, value):
    (OUT / name).write_text(value + '\n', encoding='utf-8', newline='\n')


def idle_counts(data):
    counts = dict.fromkeys(('front', 'flank', 'south', 'reserve', 'rear', 'leader', 'reinforcements'), 0)
    observed = {(r['turn'], r['event']['unit']) for r in data['trace']
                if r['event']['type'] in ('intent', 'move', 'attack', 'wait')}
    for row in data['unit_turns']:
        # W1 registered every enemy at phase start, including those never reached
        # after terminal. Recompute BOTH versions using completed actor evidence.
        if row['side'] != 'enemy' or not row['eligible'] or (row['turn'], row['id']) not in observed:
            continue
        if not row['role_reason'] and not row['could_reach_target'] and not row['move_steps'] and not row['attacks']:
            counts[row['group']] += 1
    return counts


def reports():
    runtime = read('runtime-battle.json')
    phase_mean = mean(p['seconds'] for p in runtime['enemy_phase_seconds'])
    perf = read('performance.json')
    before = json.loads((PROJECT / 'docs/evidence/spike04/performance.json').read_text(encoding='utf-8'))
    lines = ['# Measured performance — 720p, AMD Radeon 780M', '', perf['method'], '',
             '| Operation | Before mean/worst ms | After n | After mean/worst ms | Mean delta |',
             '| --- | --- | ---: | --- | ---: |']
    performance = {}
    for kind in ('scroll', 'enemy-normal', 'enemy-fast'):
        old = [p['ms'] for p in before['samples'] if p['phase'] == kind]
        new = [p['ms'] for p in perf['samples'] if p['phase'] == kind]
        assert old and new
        performance[kind] = {'samples': len(new), 'mean_ms': mean(new), 'worst_ms': max(new),
                             'before_mean_ms': mean(old), 'delta_ms': mean(new)-mean(old)}
        lines.append(f'| {kind} | {mean(old):.3f}/{max(old):.3f} | {len(new)} | {mean(new):.3f}/{max(new):.3f} | {mean(new)-mean(old):+.3f}ms |')
    lines += ['', 'Positive deltas are measured regressions in these short samples; scheduling, camera',
              'safety and label work are included. This does not isolate AI cost or prove causation.',
              'No steady60FPS claim. Captured movies are separate and are NOT performance samples.', '',
              'Enemy turn2 presentation: '+', '.join(('2×' if p['fast'] else 'normal')+f' {p["seconds"]:.3f}s' for p in perf['enemy_phases'])+'.',
              f'Continuous road run normal enemy mean {phase_mean:.6f}s across {len(runtime["enemy_phase_seconds"])} phases; includes terminal partial phase.', '',
              '| Unrecorded runtime attacks | n | Mean / max wall s | Max process s |',
              '| --- | ---: | --- | ---: |']
    attacks = read('runtime-attack-timings.json')
    assert attacks and all(a['wall_seconds'] <= 1.7 for a in attacks)
    for kind in sorted({a['kind'] for a in attacks}):
        values = [a for a in attacks if a['kind'] == kind]
        lines.append(f'| {kind} | {len(values)} | {mean(a["wall_seconds"] for a in values):.3f}/{max(a["wall_seconds"] for a in values):.3f} | {max(a["process_seconds"] for a in values):.3f} |')
    lines += ['', 'One runtime melee contact PNG readback is included in these attack wall samples;',
              'the perf mode has none. Input readiness≤1.7s verified; target≤1.2s is reported per row.',
              'Dummy audio was driven, not auditioned. HUMAN_PENDING.']
    write('PERFORMANCE.md', '\n'.join(lines))
    lines = ['# Before/after pacing — seed24018, automated policies', '',
             'Same original 24×18 terrain/deployment, HP/damage/move4/3/6, leader objective, limit15, warning4/arrival5.',
             'W1 reproduced road win12, flank lose7, turtle lose3; W2-only intermediates retained in w2/.', '',
             '| Policy/version | Result/turn | Contact | Wave first engaged | LOS-blocked actual shots | Living ally turns | Estimate min |',
             '| --- | --- | ---: | --- | ---: | ---: | --- |']
    all_data = {}
    for name in ('road', 'flank', 'turtle', 'bypass', 'scout-retreat'):
        for version, folder, enemy_mean in [('before', 'baseline', 1.999), ('after', 'autoplay', phase_mean)]:
            path = OUT / folder / (name+'.json')
            if not path.exists(): continue
            data = read(folder+'/'+name+'.json')
            all_data[name, version] = data
            living = data['living_ally_unit_turns']
            turn = data['turns_to_result']
            low, high = [(living*t+turn*enemy_mean)/60 for t in (15, 25)]
            wave = data['reinforcement_first_engage_turn']
            lines.append(f'| {name}/{version} | {data["status"]}/{turn} | {data["first_contact_turn"]} | {wave if wave >= 0 else "never"} | {data["los_blocked_shots"]} | {living} | {low:.1f}–{high:.1f} |')
    lines += ['', f'Formula: turns × (measured enemy mean + mean living allies/turn × assumed15–25s). Before mean1.999s; after mean{phase_mean:.6f}s from actual road scene.',
              'Menu/reading breaks omitted; extra conservative phase counted on a winning turn. Bypass begins at scripted turn5, so its estimate uses only observed ally turns plus the absolute result turn; it is NOT full-battle pacing.',
              '15–25min target is not established: all three fixed simple policies lose, road victory regresses.',
              'Flank7 and turtle6 still collapse. AI adds pressure and LOS removes some shots; policy mistakes',
              'and difficulty are confounded. No stat/objective/terrain relaxation was made to manufacture wins.', '',
              '| Policy/version | front | flank | south | reserve | rear | leader | wave | Total true idle / observed enemy turns |',
              '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    idle_report = {}
    for (name, version), data in all_data.items():
        counts = idle_counts(data)
        idle_report[name+'/'+version] = counts
        observed = {(r['turn'], r['event']['unit']) for r in data['trace'] if r['event']['type'] == 'intent'}
        denominator = sum(1 for row in data['unit_turns'] if row['side'] == 'enemy' and row['eligible'] and (row['turn'], row['id']) in observed)
        lines.append(f'| {name}/{version} | '+ ' | '.join(str(v) for v in counts.values())+f' | {sum(counts.values())}/{denominator} ({sum(counts.values())/max(1,denominator):.1%}) |')
    lines += ['', 'True idle = eligible enemy with observed actor phase, no reachable attack, no move, no attack, and no explicit deliberate hold. Inactive guard phases count idle. Born-turn and unprocessed actors after terminal do not.',
              'W1 raw enemy_idle_by_group predates the terminal-tail correction; this table recomputes BOTH versions',
              'from their preserved trace/rows. Original JSON untouched; raw historical idle_turns still includes advancing enemies.',
              'Bodyguard at the radius boundary is now explicitly logged as a protection hold, not silent idle.', '',
              '| Policy/version/class | Damage/share | Kills/share | Ally deaths (id@turn) |',
              '| --- | --- | --- | --- |']
    for (name, version), data in all_data.items():
        for kind in ('melee', 'ranged', 'mobile'):
            row = data['archetypes'][kind]
            deaths = ', '.join(f'{d["id"]}@{d["turn"]}' for d in data['ally_deaths'] if d['kind'] == kind) or 'none'
            lines.append(f'| {name}/{version}/{kind} | {row["damage_dealt"]}/{row["damage_share"]:.1%} | {row["kills"]}/{row["kill_share"]:.1%} | {deaths} |')
    lines += ['', 'Road ranged kill share60% before →16.7% after, damage31.25%→23.8%; cover/LOS and AI both changed, so this is not isolated LOS causality.',
              'Road mobile damage15.6%→33.3% but both still die early. Scout-retreat preserves scouts longer at the cost of very little damage; noHP/damage buff, no route edits. Mobility role remains an Owner question.',
              'Wave never engages the three short western fights. Full-roster scripted bypass is first contested on turn7',
              '(either side attacking counts engagement); isolated pursuit test/capture separately proves wave actively attacks',
              'within two eligible turns. Neither proves the wave cannot ever be bypassed; leader-kill objective stays.',
              'No initial-deployment winning policy was established after the AI change. The staged terminal win capture',
              'only proves the objective/result screen, not whole-map winnability. Human blind road/flank/turtle tests pending.',
              'No terrain or position changes to authored level data. All values are spike tests, not canon.']
    write('PACING.md', '\n'.join(lines))
    write('metrics-summary.json', json.dumps({'enemy_mean_seconds': phase_mean, 'performance': performance, 'idle_recomputed': idle_report}, indent=2))


def movies():
    index = {}
    for mode, name in [('enemy', 'enemy-phase-60fps'), ('sequence', 'select-move-ranged-60fps')]:
        capture = read('capture-'+mode+'.json')
        assert capture['pass'] and all(capture['checks'].values())
        source = PROJECT / '.godot/spike05-field' / (mode+'.avi')
        raw = source.read_bytes()
        parts = list(chunks(raw, 12, len(raw)))
        header = next(value for key, value in parts if key == b'avih')
        fps = 1_000_000 / struct.unpack_from('<I', header)[0]
        assert abs(fps-60) < .01
        frames = [v for k, v in parts if k in (b'00dc', b'00db')]
        assert frames
        for frame in frames:
            with Image.open(BytesIO(frame)) as im: assert im.size == (1280, 720)
        shutil.copyfile(source, OUT / (name+'.avi'))
        sheet = Image.new('RGB', (1440, 600), '#101a19')
        draw = ImageDraw.Draw(sheet)
        native = OUT / (mode+'-frames')
        native.mkdir(exist_ok=True)
        for i in range(6):
            frame = i*(len(frames)-1)//5
            im = Image.open(BytesIO(frames[frame])).convert('RGB')
            im.save(native / f'{frame:04d}.png')
            x, y = i%3*480, i//3*300
            sheet.paste(im.resize((480, 270)), (x, y+30))
            draw.text((x+6, y+6), f'{mode} F{frame} /60FPS', fill='#eee7d6')
        sheet.save(OUT / (name+'-strip.png'))
        index[name] = {'fps': fps, 'frames': len(frames), 'resolution': [1280, 720], 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    write('movie-index.json', json.dumps(index, indent=2))
    write('MOVIE.md', '''# Native runtime AVI + PNG strips

ffmpeg is not installed. Godot --write-movie records native1280×720 MJPEG AVI at60 simulation FPS.
Pillow verifies AVI headers/every frame dimension and extracts native frames/PNG strips; no generated screenshot.

- [Enemy phase AVI](enemy-phase-60fps.avi) / [strip](enemy-phase-60fps-strip.png): real road-turn2 state, advancing front, normal speed.
- [Select→move→ranged attack AVI](select-move-ranged-60fps.avi) / [strip](select-move-ranged-60fps-strip.png): explicitly staged four-unit original-field fixture. Real parsed mouse select, move preview, Esc, move confirm, attack preview, Enter, return. Not a continuous battle.
- [Hitfeel](hitfeel/impact-strip-spike04-vs-spike05.png): normal/crit04 vs05, contact±8; four native AVI/contact sets.
- Continuous road scene is separately automated through actual scene actions to lose8; runtime-battle.json is not human play.
- reinforcement-interception.png isolates thoma+leader+wave on original map/stats; first attempted full-probe capture failed to produce an enemy wave strike and is preserved in attempts/.
- win-staged-terminal.png is a staged lethal rules/result fixture. lose.png is continuous road defeat.

AVI encoding/readbacks stretch wall time; fixed movie clock is not measured runtime FPS. PERFORMANCE.md uses a separate unrecorded run.
Dummy audio triggers were recorded, not auditioned. Human feel/art/pacing remain HUMAN_PENDING.
''')


def normalize_logs():
    for path in OUT.rglob('*.log'):
        raw = path.read_bytes()
        value = raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')
        value = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', value)
        path.write_text('\n'.join(line.rstrip() for line in value.splitlines()).rstrip()+'\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    reports()
    movies()
    normalize_logs()
    print('SPIKE05_FIELD packaged metrics, actual movies/strips and normalized logs')
