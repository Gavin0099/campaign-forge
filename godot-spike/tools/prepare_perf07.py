"""Offline exact-export instrumentation; no subprocess/network. Archives made by git."""
import hashlib
import json
import re
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'.godot/spike07-perf'
SCOPES = {
    'scripts/levels/field_minimap.gd': ['_draw', '_process'],
    'scripts/levels/field_minimap_terrain.gd': ['_draw'],
    'scripts/levels/field_labels.gd': ['_draw', '_process', 'refresh_layout'],
    'scripts/levels/field_indicators.gd': ['_draw', '_process', 'refresh_items'],
    'scripts/levels/field_ground.gd': ['_draw'],
    'scripts/levels/field_hud.gd': ['update_state', 'hover'],
    'scripts/levels/field_battle.gd': ['refresh', '_process'],
    'scripts/rules/field_rules.gd': ['reach', 'distance_map', 'ai_plan', 'threat', 'zoc_cells'],
}

def instrument(folder):
    manifest = {}
    for path, names in SCOPES.items():
        file = folder/path
        if not file.exists(): continue
        source = file.read_text(encoding='utf-8-sig')
        manifest[path] = hashlib.sha256(source.encode()).hexdigest()
        wrappers = []
        for name in names:
            pattern = rf'^(static )?func {name}\(([^\n]*)\)( -> [^:\n]+)?:$'
            m = re.search(pattern, source, re.M)
            if not m:
                continue
            args = [x.strip().split(':')[0].split('=')[0].strip() for x in m[2].split(',') if x.strip()]
            # Defaults contain no commas for selected signatures except Vector2i;
            # none selected here have such a default.
            signature = m[0]
            source = source[:m.start()]+signature.replace(f'func {name}(', f'func _meter_original_{name}(')+source[m.end():]
            call = f'_meter_original_{name}({", ".join(args)})'
            body = ['\tvar meter_started := Time.get_ticks_usec()']
            is_void = not m[3] or m[3].strip()=='-> void'
            body.append('\t'+call if is_void else '\tvar meter_result = '+call)
            body.append(f'\tPerfMeter07.add("{Path(path).stem}.{name}",meter_started)')
            if not is_void:
                body.append('\treturn meter_result')
            wrappers.append(signature+'\n'+'\n'.join(body)+'\n')
        # Insert const after extends/class_name (class_name can precede extends).
        source += '\nconst PerfMeter07 = preload("res://tools/perf_meter07.gd")\n\n'+'\n'.join(wrappers)
        file.write_text(source, encoding='utf-8')
    return manifest

def prepare(tag):
    folder = BASE/tag
    folder.mkdir(parents=True, exist_ok=True)
    archive = BASE/(tag+'.tar')
    with tarfile.open(archive) as tar:
        for member in tar:
            p = Path(member.name)
            if not member.isfile() or not p.parts or p.parts[0]!='godot-spike' or '..' in p.parts:
                continue
            target = folder/Path(*p.parts[1:])
            target.parent.mkdir(parents=True, exist_ok=True)
            with tar.extractfile(member) as src, target.open('wb') as dst:
                shutil.copyfileobj(src,dst)
    (folder/'tools').mkdir(exist_ok=True)
    overrides={}
    if tag=='after':
        for tree in ['scripts','data']:
            for source in (ROOT/tree).rglob('*'):
                if not source.is_file() or source.suffix not in {'.gd','.uid','.gdshader'}: continue
                relative=source.relative_to(ROOT)
                shutil.copyfile(source,folder/relative)
                overrides[relative.as_posix()]=hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for name in ['perf_field07.gd','perf_meter07.gd','perf_states07.bin']:
        shutil.copyfile(ROOT/'tools'/name,folder/'tools'/name)
    manifest = instrument(folder)
    (ROOT/f'docs/evidence/spike07/perf/export-{tag}.json').write_text(json.dumps({'tag':tag,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'working_source_overrides_LF_sha256':overrides,'pre_instrument_LF_sha256':manifest},indent=2)+'\n')
    print(folder)

if __name__=='__main__':
    prepare(sys.argv[1])
