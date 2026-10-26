"""Offline spike05 evidence audit. No subprocess, network, or source-art writes.

Git scope snapshots are supplied by the operator; this is not a Git launcher.
Source hashes describe working-tree bytes before the containing commit, not HEAD.
"""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
OUT = PROJECT / 'docs/evidence/spike05'
TEXT = {'.gd', '.gdshader', '.py', '.tres', '.tscn', '.json', '.md', '.txt', '.log', '.godot', '.uid'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def text(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')


def read(path):
    return json.loads(text(path))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    for path in OUT.rglob('*.log'):
        if path.name.endswith('audit-run.log'):
            continue
        value = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text(path))
        path.write_text('\n'.join(line.rstrip() for line in value.splitlines()).rstrip() + '\n', encoding='utf-8', newline='\n')
    for name in ['w7-exit-codes.json', 'git-scope.json']:
        write(OUT / name, read(OUT / name))
    for name in ['changed-paths.txt', 'untracked-paths.txt', 'diff-stat.txt']:
        path = OUT / name
        path.write_text(text(path).rstrip() + '\n', encoding='utf-8', newline='\n')
    exits = read(OUT / 'w7-exit-codes.json')
    assert exits['import_exit'] == exits['gut_exit'] == 0
    log = text(OUT / 'test-run.log')
    count = int(re.search(r'Passing Tests\s+(\d+)', log).group(1))
    assertions = int(re.search(r'Asserts\s+(\d+)', log).group(1))
    assert count >= 123 and 'All tests passed!' in log
    for path in [OUT / 'test-run.log', OUT / 'w7-import.log', *OUT.glob('w6-*-final.log')]:
        assert not any(t in text(path) for t in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:', 'GUT WARNING']), path.name
    scope = read(OUT / 'git-scope.json')
    assert scope['branch'] == 'codex/godot-spike'
    assert scope['protected_diff_exit'] == scope['diff_check_exit'] == 0
    assert scope['profile_byte_match'] and scope['historical_profile_blob'] == scope['preserved_profile_blob']
    paths = set(text(OUT / 'changed-paths.txt').splitlines() + text(OUT / 'untracked-paths.txt').splitlines())
    paths.discard('')  # A clean untracked snapshot is valid on handoff refresh.
    for name in paths:
        assert name.startswith('godot-spike/') or name == 'docs/tasks/godot-spike-05-ai-los-polish.md', name
        assert not name.startswith(('godot-spike/art/', 'godot-spike/scripts/rules/grid_rules.gd')), name
        assert not (name.endswith('.png') and any(p in name.lower().split('/') for p in ['swing', 'idle', 'knight-a', 'knight-b'])), name
    old = {r['path']: r for r in read(PROJECT / 'docs/evidence/spike02-a9/source-hashes.json')}
    protected = []
    copied = PROJECT / 'art/anim-shared'
    for path in sorted(copied.rglob('*')):
        if not path.is_file() or path.suffix in {'.import', '.uid'}:
            continue
        source = REPO / 'shared-anim' / path.relative_to(copied)
        raw = source.read_bytes()
        assert path.read_bytes() == raw
        key = source.relative_to(REPO).as_posix()
        normalized = raw if path.suffix == '.png' else raw.replace(b'\r\n', b'\n')
        assert digest(normalized) == old[key]['sha256_working_tree' if path.suffix == '.png' else 'sha256_git_lf'], key
        protected.append({'path': key, 'sha256': digest(raw), 'matches_a9': True})
    rules = 'godot-spike/scripts/rules/grid_rules.gd'
    assert digest((REPO / rules).read_bytes().replace(b'\r\n', b'\n')) == old[rules]['sha256_git_lf']
    frozen = read(OUT / 'capture-source-hashes.json')['files']
    for row in frozen:
        assert digest((REPO / row['path']).read_bytes()) == row['sha256'], row['path']
    captures = {}
    for mode in ['qa', 'sight', 'intercept', 'result', '1080', 'enemy', 'sequence', 'runtime', 'perf']:
        data = read(OUT / f'capture-{mode}.json')
        assert data['pass'] and all(data['checks'].values()), mode
        for shot in data['shots']:
            assert shot.get('label_overlaps', 0) == 0, shot['name']
            assert Image.open(OUT / (shot['name'] + '.png')).size == tuple(shot['resolution'])
        captures[mode] = data['checks']
    for name, movie in read(OUT / 'movie-index.json').items():
        raw = (OUT / (name + '.avi')).read_bytes()
        assert digest(raw) == movie['sha256'] and len(raw) == movie['bytes']
        assert movie['resolution'] == [1280, 720] and abs(movie['fps'] - 60) < .01
    timing = read(OUT / 'hitfeel/timing.json')
    assert timing['pass'] and timing['readbacks'] == 0 and len(timing['runs']) == 9
    for row in timing['runs']:
        assert row['hp'] == 4 and row['cell'] == {1: [1, 6], 2: [1, 5], 3: [3, 4]}[row['setup']]
        assert row['same_frame_contact'] and row['input_ready']
        assert 0 < row['fixed_fps_seconds'] <= 1.7 and 0 < row['wall_seconds'] <= 1.7
    for setup in [1, 2, 3]:
        rows = {r['mode']: r for r in timing['runs'] if r['setup'] == setup}
        for clock in ['fixed_fps_seconds', 'wall_seconds']:
            assert rows['reduced'][clock] <= rows['normal'][clock]
    for policy, result, turn in [('road', 'win', 12), ('flank', 'lose', 7), ('turtle', 'lose', 3)]:
        before = read(OUT / f'baseline/{policy}.json')
        assert before['status'] == result and before['turns_to_result'] == turn and before['first_contact_turn'] == 2
    for policy, turn in [('road', 8), ('flank', 7), ('turtle', 6), ('bypass', 7), ('scout-retreat', 9)]:
        after = read(OUT / f'autoplay/{policy}.json')
        assert after['status'] == 'lose' and after['turns_to_result'] == turn
    attacks = read(OUT / 'runtime-attack-timings.json')
    assert len(attacks) == 40 and all(0 < r['wall_seconds'] <= 1.7 for r in attacks)
    assert 'run/main_scene="res://scenes/Skirmish.tscn"' in text(PROJECT / 'project.godot')
    write(OUT / 'audit.json', {'pass': True, 'tests': count, 'assertions': assertions,
        'scope_base': '905c0ce', 'git_scope': scope, 'protected_shared_files': protected,
        'grid_rules_a9_unchanged': True, 'capture_source_freeze_matches': len(frozen),
        'captures': captures, 'skirmish_timing_runs': 9, 'runtime_attacks': len(attacks),
        'limits': ['Automated operator only; HUMAN_PENDING.',
                   'All initial-deployment measured policies lose; whole-field win unverified.',
                   'Movie clock is not performance; no steady60FPS claim.',
                   'Scope snapshot HEAD precedes containing evidence/handoff commit.']})
    files = {PROJECT / 'project.godot', PROJECT / 'docs/HANDOFF.md', PROJECT / 'docs/VERIFICATION.md',
             REPO / 'docs/tasks/godot-spike-05-ai-los-polish.md'}
    for folder in ['scripts', 'config', 'scenes', 'shaders', 'tests', 'tools', 'data']:
        files.update(p for p in (PROJECT / folder).rglob('*') if p.is_file() and p.suffix in TEXT)
    for folder in [OUT, PROJECT / 'art/bigmap', copied, REPO / 'shared-anim']:
        files.update(p for p in folder.rglob('*') if p.is_file() and p.suffix not in {'.import', '.pyc'})
    files = {p for p in files if p.name != 'source-hashes.json' and not p.name.endswith('audit-run.log')}
    hashes = []
    for path in sorted(files):
        raw = path.read_bytes()
        hashes.append({'path': path.relative_to(REPO).as_posix(), 'sha256_working_tree': digest(raw),
            'sha256_git_lf': digest(raw.replace(b'\r\n', b'\n')) if path.suffix in TEXT else digest(raw)})
    write(OUT / 'source-hashes.json', hashes)
    print(f'SPIKE05_AUDIT pass=true tests={count} assertions={assertions} protected={len(protected)} sources={len(hashes)}')


if __name__ == '__main__':
    main()
