"""Execute bounded acceptance checks and record real exit codes, never supplied ones."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install_codex_governance import install
from validate_task_evidence import source_digest, native_status


def main():
    install()
    binding = json.loads((ROOT / '.codex/governance-bindings.json').read_text())
    python = binding['executables']['python']['path']
    node = binding['executables']['node']['path']
    environment = {key: os.environ[key] for key in ('SystemRoot', 'WINDIR', 'SystemDrive', 'TEMP', 'TMP') if key in os.environ}
    # These test/build children do not receive credential or module selectors.
    checks = {}
    commands = {
        'lifecycle-tests': ([python, '-I', '-B', str(ROOT / 'tests/test_governance_lifecycle.py')], ROOT),
        'scope': ([python, '-I', '-B', str(ROOT / 'scripts/validate_ui_scope.py')], ROOT),
        'typecheck': ([node, str(ROOT / 'ui-prototype/node_modules/typescript/bin/tsc'), '--noEmit'], ROOT / 'ui-prototype'),
        'vite': ([node, str(ROOT / 'ui-prototype/node_modules/vite/bin/vite.js'), 'build'], ROOT / 'ui-prototype'),
    }
    for name, (argv, cwd) in commands.items():
        # Exact executable bytes are re-verified immediately before launch.
        from governance_lifecycle import digest
        key = 'python' if argv[0] == python else 'node'
        item = binding['executables'][key]
        if digest(Path(argv[0])) != item['sha256'] or Path(argv[0]).stat().st_size != item['size']:
            raise ValueError('Check executable bytes changed')
        child_env = dict(environment)
        result = subprocess.run(argv, cwd=cwd, env=child_env, text=True, encoding='utf-8',
                                errors='replace', capture_output=True, timeout=180)
        checks[name] = {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        print(f'{name}: exit_code={result.returncode}', flush=True)
        if result.returncode:
            print(result.stdout + result.stderr, flush=True)
    checks['build'] = {'exit_code': max(checks['typecheck']['exit_code'], checks['vite']['exit_code'])}
    receipt = {'generated_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': source_digest(ROOT),
               'origin': 'executed_commands', 'checks': checks, 'native_execution_claimed': False}
    path = ROOT / 'artifacts/runtime/governance-checks.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # Durable reviewer-visible evidence distinguishes command replay from
    # actual host callbacks; it never upgrades replay to natural execution.
    exported = dict(receipt, native_status=native_status(ROOT),
                    boundary='Isolated command replay plus build/scope checks; platform trust is separate')
    (ROOT / 'artifacts/governance-native-acceptance.json').write_text(
        json.dumps(exported, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0 if all(check['exit_code'] == 0 for check in checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
