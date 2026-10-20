"""Generate repo-local, byte-bound Windows Codex hooks; never approve trust.

Re-run after changing bridge/validators/framework source. Review changed hooks
in Codex. Existing custom hooks/config are preserved; ambiguous edits fail.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(root=ROOT, executable_paths=None):
    if os.name != 'nt':
        raise ValueError('This binding is qualified for Windows only; do not install a guessed POSIX launcher')
    root = root.resolve()
    if any(c in str(root) for c in '\r\n"'):
        raise ValueError('Unsupported project path')
    files = ['scripts/governance_lifecycle.py', 'scripts/validate_ui_scope.py',
             'scripts/validate_task_evidence.py', 'contract.yaml']
    for folder in ('governance_tools', 'runtime_hooks', 'memory_pipeline'):
        files += [p.relative_to(root).as_posix() for p in
                  (root / 'ai-governance-framework' / folder).rglob('*.py')]
    if not any(p.startswith('ai-governance-framework/') for p in files):
        raise ValueError('Initialize the pinned framework submodule first')
    paths = {'python': Path(sys.executable).resolve(),
             'git': Path(shutil.which('git') or '').resolve(),
             'node': Path(shutil.which('node') or '').resolve()}
    if executable_paths is not None:
        paths = executable_paths
    executables = {}
    for name, path in paths.items():
        if not path.is_absolute() or not path.is_file() or path.resolve() != path or any(c in str(path) for c in '\r\n"'):
            raise ValueError(f'Invalid executable selection: {name}')
        executables[name] = {'path': str(path), 'size': path.stat().st_size, 'sha256': sha(path)}
    config_env = {key: value for key, value in os.environ.items() if not key.upper().startswith('GIT_')}
    autocrlf = subprocess.run([str(paths['git']), '-C', str(root), 'config', '--get', 'core.autocrlf'],
                             capture_output=True, text=True, env=config_env, timeout=10).stdout.strip().lower() or 'false'
    if autocrlf not in {'true', 'false', 'input'}:
        raise ValueError('Unsupported Git line-ending mode')
    binding = {'schema_version': 1, 'root': str(root), 'executables': executables, 'git_autocrlf': autocrlf,
               'sources': {rel: sha(root / rel) for rel in sorted(files)}}
    bindings_path = root / '.codex/governance-bindings.json'
    bindings_text = json.dumps(binding, indent=2) + '\n'
    bindings_sha = hashlib.sha256(bindings_text.encode()).hexdigest()
    template = json.loads((root / 'governance/codex-hooks.template.json').read_text(encoding='utf-8'))
    path = root / '.codex/hooks.json'
    config = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    if config and config.get('description') != template['description']:
        raise ValueError('Existing custom hook config: review/merge explicitly; no overwrite')
    config = {'description': template['description'], 'hooks': {}}
    bridge = root / 'scripts/governance_lifecycle.py'
    for event, options in template['events'].items():
        # The exact bootstrap is reviewed by Codex. Isolated Python ignores
        # PYTHONPATH/startup selectors before verifying itself and bridge bytes.
        # One process avoids spending SessionEnd's budget on shell startups.
        script = (
            "import hashlib,os,pathlib,sys; "
            f"p=pathlib.Path({str(paths['python'])!r}); "
            f"assert pathlib.Path(sys.executable).resolve()==p and hashlib.sha256(p.read_bytes()).hexdigest()=={executables['python']['sha256']!r},'Python binding changed'; "
            f"b=pathlib.Path({str(bridge)!r}); data=b.read_bytes(); "
            f"assert hashlib.sha256(data).hexdigest()=={sha(bridge)!r},'Bridge binding changed'; "
            "replay=os.environ.get('CAMPAIGN_GOVERNANCE_REPLAY')=='1'; "
            "env={k:os.environ[k] for k in ('SystemRoot','WINDIR','SystemDrive') if k in os.environ}; "
            "os.environ.clear(); os.environ.update(env); "
            f"os.chdir({str(root)!r}); "
            f"sys.argv=[str(b),'--bindings',{str(bindings_path)!r},'--bindings-sha256',{bindings_sha!r},'--event',{event!r}]+(['--replay'] if replay else []); "
            "exec(compile(data,str(b),'exec'),{'__name__':'__main__','__file__':str(b)})")
        command = subprocess.list2cmdline([str(paths['python']), '-I', '-B', '-X', 'utf8', '-c', script])
        handler = {'type': 'command', 'command': command, 'commandWindows': command,
                   'timeout': options['timeout'], 'statusMessage': 'Campaign Forge governance: ' + event}
        group = {'hooks': [handler]}
        if 'matcher' in options:
            group['matcher'] = options['matcher']
        config['hooks'][event] = [group]
    path.parent.mkdir(parents=True, exist_ok=True)
    bindings_path.write_text(bindings_text, encoding='utf-8', newline='\n')
    path.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8', newline='\n')
    return {'installed': True, 'events': list(config['hooks']), 'hook_trust': 'REQUIRES_USER_REVIEW',
            'native_execution': 'NOT_OBSERVED', 'bindings_sha256': bindings_sha}


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(install(), indent=2))
