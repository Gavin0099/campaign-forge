#!/usr/bin/env python3
"""Consumer scope validator. CLI and framework plugin share the same checks."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'ai-governance-framework'))
from governance_tools.validator_interface import DomainValidator,ValidatorResult
BASE='652ce0ea38cfe2bb4b07b942a5cdae3db823e0f2'
# Owner explicitly approved this exact metadata addition on 2026-10-20.
PLAN_HEADER='> **最後更新**: 2026-10-20\n> **Owner**: Gavin\n> **Freshness**: Phase (30d)\n> 本表頭僅記錄治理導入日；故事仍停在 S3，未授權 S4。UI 進度見 ui-prototype/PLAN.md。\n\n'.encode()

def inspect_scope():
    protected=['README.md','PLAN.md','SLICES.md']
    protected+=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'docs'],cwd=ROOT,text=True).splitlines()
    errors=[]
    for rel in protected:
        original=subprocess.check_output(['git','show',f'{BASE}:{rel}'],cwd=ROOT)
        expected=(PLAN_HEADER+original) if rel=='PLAN.md' else original
        if not (ROOT/rel).exists() or (ROOT/rel).read_bytes()!=expected: errors.append(f'Planning modified: {rel}')
    if (ROOT/'.github/workflows').exists() and any((ROOT/'.github/workflows').iterdir()): errors.append('GitHub Actions are not authorized')
    if (ROOT/'LICENSE').exists(): errors.append('Story-wide LICENSE is not authorized')
    for rel in ['party-v1.png','units-v1.png','battlefield-v1.png','campaign-v1.png']:
        if not (ROOT/'ui-prototype/public/art'/rel).is_file(): errors.append(f'Missing art: {rel}')
    return errors,len(protected)

class UIPrototypeScopeValidator(DomainValidator):
    @property
    def rule_ids(self): return ['UI_PLANNING_PRESERVED','UI_NO_ACTIONS','UI_ART_PRESENT']
    def validate(self,payload):
        errors,count=inspect_scope()
        return ValidatorResult(ok=not errors,rule_ids=self.rule_ids,violations=errors,
            evidence_summary=f'{count} planning files checked (only owner-approved PLAN metadata allowed) against {BASE}; no Actions/root LICENSE; four art assets checked.',
            metadata={'scope':'local current worktree; does not verify gameplay or authorise publication'})

if __name__=='__main__':
    result=UIPrototypeScopeValidator().validate({})
    print(('PASS: ' if result.ok else 'FAIL: ')+result.evidence_summary)
    for violation in result.violations: print(violation)
    sys.exit(0 if result.ok else 1)
