"""Verify current source against executed governance checks; no native upgrade."""
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'scripts'))
from validate_task_evidence import source_digest, validate_claims, native_status

record = json.loads((root / 'artifacts/governance-native-acceptance.json').read_text(encoding='utf-8'))
if record['source_sha256'] != source_digest(root):
    raise ValueError('Stale governance execution evidence')
if not all(check['exit_code'] == 0 for check in record['checks'].values()):
    raise ValueError('Failed recorded acceptance check')
response = '建置與功能測試已通過；商業美術品質人工待審，平台自然回呼仍待驗。'
errors = validate_claims(response, root)
if errors:
    raise ValueError(errors)
print('PASS: current source matches stored lifecycle replay, scope, TypeScript and Vite execution. This verifies stored checks, not a new lifecycle execution.')
print(json.dumps({'native_status': native_status(root), 'commercial_art_quality': 'human_review_pending'}, ensure_ascii=False))
