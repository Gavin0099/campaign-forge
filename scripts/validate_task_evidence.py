"""Bounded claim checks. Does not prove story quality or general correctness."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ai-governance-framework'))
from governance_tools.validator_interface import DomainValidator, ValidatorResult


def source_digest(root: Path) -> str:
    files = sorted(p for folder in ("scripts", "tests", "fixtures", "ui-prototype/src", "governance/rules")
                   for p in (root / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    files += [root / rel for rel in ('contract.yaml', 'ui-prototype/package.json',
              'ui-prototype/package-lock.json',
              'governance/codex-hooks.template.json', 'AGENTS.md', 'AGENTS.base.md',
              'ui-prototype/PLAN.md') if (root / rel).is_file()]
    checksum = hashlib.sha256()
    for path in files:
        checksum.update(path.relative_to(root).as_posix().encode())
        checksum.update(path.read_bytes())
    return checksum.hexdigest()


def validate_claims(response: str, root: Path) -> list[str]:
    errors = []
    if re.search(r"(?:S4|正式故事).{0,8}(?:已完成|已定案|完成了)", response):
        errors.append("Formal story completion exceeds the current authorization")
    wants_tests = re.search(r"(?:測試|檢查|驗收|建置|build|tests?).{0,30}(?:全數|均|全部|已|all)?.{0,8}(?:通過|成功|pass(?:ed)?|success)", response, re.I)
    if wants_tests:
        receipt = root / "artifacts/runtime/governance-checks.json"
        try:
            data = json.loads(receipt.read_text(encoding="utf-8"))
            if data.get("source_sha256") != source_digest(root):
                errors.append("Check evidence is stale for the current source")
            required = {"scope", "build", "lifecycle-tests"}
            results = data.get("checks", {})
            if not required.issubset(results) or any(results[key].get("exit_code") != 0 for key in required):
                errors.append("Missing or failed scope/build/lifecycle test evidence")
        except (OSError, ValueError, TypeError, KeyError):
            errors.append("No current execution receipt; run scripts/record_governance_checks.py")
    full_claim = re.search(r"(?:已完成|已達|完成了).{0,8}完整(?:自動)?(?:治理|導入)|full governance adoption (?:is )?(?:complete|verified)", response, re.I)
    if full_claim and not native_status(root)['complete']:
        errors.append("Full adoption requires trusted native callbacks including successful canonical closeout; replay is insufficient")
    return errors


def native_status(root: Path) -> dict:
    sessions = root / 'artifacts/runtime/codex'
    observations = {}
    complete = False
    for session in sessions.iterdir() if sessions.exists() else []:
        found = {}
        for event in ('SessionStart', 'UserPromptSubmit', 'Stop', 'SessionEnd'):
            path = session / (event + '.json')
            try:
                value = json.loads(path.read_text(encoding='utf-8'))
                if value.get('origin') == 'native_callback' and value.get('ok'):
                    found[event] = True
            except (OSError, ValueError, AttributeError):
                pass
        for event in found:
            observations[event] = True
        if len(found) == 4:
            value = json.loads((session / 'SessionEnd.json').read_text(encoding='utf-8'))
            entry = value['result']['canonical_entry']
            receipt_path = Path(entry.get('closeout_receipt_artifact') or '')
            if receipt_path.is_absolute() and receipt_path.resolve().is_relative_to(root):
                try:
                    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
                    complete = (receipt.get('exit_code') == 0 and receipt.get('memory_write_claim_verified') is True
                                and receipt.get('daily_memory_write_status') in {'written', 'already_present'}
                                and entry.get('closeout_status') == 'valid')
                except (OSError, ValueError):
                    pass
            if complete:
                break
    return {'complete': complete, 'observed_native_events': sorted(observations),
            'boundary': 'Local callback receipts; corroborate with Codex hook trust and host execution. Not a security attestation.'}


class TaskEvidenceValidator(DomainValidator):
    @property
    def rule_ids(self):
        return ['game-ui-prototype', 'TASK_EVIDENCE', 'TASK_SCOPE', 'TASK_NATIVE']

    def validate(self, payload):
        errors = validate_claims(payload.get('response_text', ''), ROOT)
        return ValidatorResult(ok=not errors, rule_ids=self.rule_ids, violations=errors,
            evidence_summary='Check bounded formal-story, execution-evidence and native-adoption claims.',
            metadata={'scope': 'pattern-based claim checks; not general semantic understanding'})
