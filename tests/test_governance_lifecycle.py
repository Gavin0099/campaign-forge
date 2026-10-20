"""Acceptance replay through the exact generated Windows command (no model call)."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import time
import unittest
import uuid

SOURCE = Path(__file__).resolve().parents[1]
ROOT = SOURCE
sys.path.insert(0, str(ROOT / 'scripts'))
from install_codex_governance import install
from validate_task_evidence import validate_claims, source_digest


class NativeCommandReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global ROOT
        if not (SOURCE / '.codex/hooks.json').exists():
            raise RuntimeError('Run scripts/install_codex_governance.py first')
        binding = json.loads((SOURCE / '.codex/governance-bindings.json').read_text())
        git = binding['executables']['git']['path']
        environment = {key: os.environ[key] for key in ('SystemRoot', 'WINDIR', 'SystemDrive') if key in os.environ}
        scratch = SOURCE / 'scratch'
        scratch.mkdir(exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(prefix='lifecycle-acceptance-', dir=scratch)
        ROOT = Path(cls.temporary.name) / 'consumer'
        subprocess.run([git, 'clone', '--config', 'core.autocrlf=false', '--local', '--no-hardlinks', str(SOURCE), str(ROOT)],
                       check=True, capture_output=True, env=environment)
        subprocess.run([git, 'clone', '--config', 'core.longpaths=true', '--config', 'core.autocrlf=false', '--local', '--no-hardlinks', str(SOURCE / 'ai-governance-framework'),
                        str(ROOT / 'ai-governance-framework')], check=True, capture_output=True, env=environment)
        for folder in ('scripts', '.codex', 'governance', 'fixtures', 'tests'):
            shutil.copytree(SOURCE / folder, ROOT / folder, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('hooks.json', 'governance-bindings.json', '__pycache__'))
        shutil.copyfile(SOURCE / 'contract.yaml', ROOT / 'contract.yaml')
        install(ROOT, executable_paths={name: Path(item['path']) for name, item in binding['executables'].items()})
        cls.config = json.loads((ROOT / '.codex/hooks.json').read_text())
        cls.binding = json.loads((ROOT / '.codex/governance-bindings.json').read_text())
        cls.host = cls.binding['executables']['python']['path']

    def setUp(self):
        runtime = ROOT / 'artifacts/runtime'
        if runtime.exists():
            if not runtime.resolve().is_relative_to(SOURCE / 'scratch'):
                raise RuntimeError('Unsafe test cleanup path')
            shutil.rmtree(runtime)
        text = ROOT / 'artifacts/session-closeout.txt'
        if text.exists():
            text.unlink()

    @classmethod
    def tearDownClass(cls):
        if not ROOT.resolve().is_relative_to(SOURCE / 'scratch'):
            raise RuntimeError('Unsafe test cleanup path')
        diagnostic = subprocess.run([cls.binding['executables']['git']['path'], '-C',
                                     str(ROOT / 'ai-governance-framework'), 'status', '--short'],
                                    capture_output=True, text=True)
        if diagnostic.stdout:
            print('FRAMEWORK DIAGNOSTIC:', diagnostic.stdout)
        cls.temporary.cleanup()

    def payload(self, event, sid=None, **fields):
        value = {'hook_event_name': event, 'session_id': sid or 'acceptance-' + uuid.uuid4().hex,
                 'cwd': str(ROOT)}
        value.update(fields)
        return value

    def invoke(self, event, payload, **environment):
        command = self.config['hooks'][event][0]['hooks'][0]['commandWindows']
        env = dict(os.environ, CAMPAIGN_GOVERNANCE_REPLAY='1', **environment)
        started = time.monotonic()
        # On Windows a string is passed unchanged to CreateProcess. Explicit
        # executable prevents CreateProcess's ambient executable search.
        result = subprocess.run(command, executable=self.host,
                                input=json.dumps(payload), text=True, encoding='utf-8',
                                capture_output=True, env=env, cwd=ROOT, timeout=30)
        result.elapsed = time.monotonic() - started
        return result

    def begin(self):
        payload = self.payload('SessionStart', source='startup')
        result = self.invoke('SessionStart', payload)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        sid = payload['session_id']
        result = self.invoke('UserPromptSubmit', self.payload('UserPromptSubmit', sid,
                             turn_id='turn1', prompt='Inspect local governance wiring.'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return sid

    def test_lifecycle_and_stop_does_not_close_session(self):
        daily = {p.name: p.read_bytes() for p in (ROOT / 'memory').glob('????-??-??.md')}
        sid = self.begin()
        result = self.invoke('Stop', self.payload('Stop', sid, turn_id='turn1',
                             last_assistant_message='The local governance configuration is ready for review.'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        record = json.loads((ROOT / 'artifacts/runtime/codex' / sid / 'Stop.json').read_text(encoding='utf-8'))
        self.assertTrue(record['ok'])
        self.assertEqual(len(record['result']['domain_validator_results']), 2)
        self.assertFalse((ROOT / 'artifacts/runtime/closeout-completions' / (sid + '.json')).exists())
        self.assertEqual(daily, {p.name: p.read_bytes() for p in (ROOT / 'memory').glob('????-??-??.md')})

    def test_session_end_calls_canonical_entry_within_native_timeout(self):
        sid = self.begin()
        result = self.invoke('SessionEnd', self.payload('SessionEnd', sid, reason='other'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = json.loads((ROOT / 'artifacts/runtime/codex' / sid / 'SessionEnd.json').read_text(encoding='utf-8'))
        self.assertTrue(record['result']['ok'], record)
        self.assertEqual(record['result']['canonical_entry']['closeout_status'], 'valid', record)
        self.assertFalse(record['result']['ledger_write_allowed'])
        print(f'\nSessionEnd exact command elapsed: {result.elapsed:.3f}s', flush=True)
        self.assertLess(result.elapsed, 3, 'Native SessionEnd timeout is at most three seconds')

    def test_replay_cannot_claim_full_native_adoption(self):
        sid = self.begin()
        result = self.invoke('Stop', self.payload('Stop', sid, turn_id='turn1',
                             last_assistant_message='已完成完整導入'))
        self.assertEqual(json.loads(result.stdout)['decision'], 'block')
        self.assertIn('native callbacks', result.stdout)

    def test_missing_closeout_owner_fails_end_without_writing_memory(self):
        sid = self.begin()
        daily = {p.name: p.read_bytes() for p in (ROOT / 'memory').glob('????-??-??.md')}
        # Simulate a lost/corrupted prepared shared closeout, never a real one.
        (ROOT / 'artifacts/session-closeout.txt').unlink()
        result = self.invoke('SessionEnd', self.payload('SessionEnd', sid, reason='other'))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(daily, {p.name: p.read_bytes() for p in (ROOT / 'memory').glob('????-??-??.md')})

    def test_missing_identity_or_wrong_workspace_rejected_before_output(self):
        for fields in ({'session_id': '../escape'}, {'cwd': str(ROOT.parent)}):
            payload = self.payload('SessionStart', source='startup')
            payload.update(fields)
            result = self.invoke('SessionStart', payload)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn('Governance SessionStart', result.stdout)

    def test_missing_pre_task_is_blocked(self):
        payload = self.payload('SessionStart', source='startup')
        self.assertEqual(self.invoke('SessionStart', payload).returncode, 0)
        result = self.invoke('Stop', self.payload('Stop', payload['session_id'], turn_id='absent',
                             last_assistant_message='Ready.'))
        self.assertEqual(result.returncode, 2)

    def test_scope_and_repeated_stop_cannot_bypass(self):
        sid = self.begin()
        for repeated in (False, True):
            result = self.invoke('Stop', self.payload('Stop', sid, turn_id='turn1',
                                 stop_hook_active=repeated, last_assistant_message='S4 已完成'))
            self.assertEqual(json.loads(result.stdout).get('decision'), 'block', result.stdout + result.stderr)
            self.assertIn('Formal story', result.stdout)

    def test_protected_document_change_blocks_stop(self):
        sid = self.begin()
        path = ROOT / 'README.md'
        original = path.read_bytes()
        try:
            path.write_bytes(original + b'\nunauthorized fixture mutation\n')
            result = self.invoke('Stop', self.payload('Stop', sid, turn_id='turn1',
                                 last_assistant_message='Ready for review.'))
            self.assertEqual(json.loads(result.stdout)['decision'], 'block')
            self.assertIn('Planning modified', result.stdout)
        finally:
            path.write_bytes(original)

    def test_resume_preserves_original_identity(self):
        sid = self.begin()
        path = ROOT / 'artifacts/runtime/sessions' / sid / 'session-envelope.json'
        original = path.read_bytes()
        for source in ('resume', 'compact'):
            result = self.invoke('SessionStart', self.payload('SessionStart', sid, source=source))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(path.read_bytes(), original)

    def test_hostile_environment_cannot_redirect_executables(self):
        scratch = ROOT / 'scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as folder:
            fake = Path(folder)
            marker = fake / 'launched.txt'
            (fake / 'git.cmd').write_text('@echo hijacked > "' + str(marker) + '"\n')
            (fake / 'sitecustomize.py').write_text('raise RuntimeError("injected")\n')
            result = self.invoke('SessionStart', self.payload('SessionStart', source='startup'),
                                 PATH=str(fake), PYTHONPATH=str(fake), GIT_DIR=str(fake),
                                 GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.hooksPath',
                                 GIT_CONFIG_VALUE_0=str(fake))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(marker.exists())

    def test_changed_binding_is_refused_before_runtime_write(self):
        binding_file = ROOT / '.codex/governance-bindings.json'
        original = binding_file.read_bytes()
        payload = self.payload('SessionStart', source='startup')
        try:
            binding_file.write_bytes(original + b' ')
            result = self.invoke('SessionStart', payload)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((ROOT / 'artifacts/runtime/codex' / payload['session_id']).exists())
            self.assertFalse((ROOT / 'artifacts/runtime/sessions' / payload['session_id']).exists())
        finally:
            binding_file.write_bytes(original)

    def test_missing_and_stale_claim_evidence_rejected(self):
        scratch = ROOT / 'scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as folder:
            root = Path(folder)
            self.assertTrue(validate_claims('build passed', root))
            path = root / 'artifacts/runtime/governance-checks.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({'source_sha256': 'stale', 'checks': {}}))
            for rel in ('contract.yaml', 'ui-prototype/package.json', 'ui-prototype/package-lock.json'):
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text('{}')
            self.assertTrue(validate_claims('build passed', root))


if __name__ == '__main__':
    unittest.main(verbosity=2)
