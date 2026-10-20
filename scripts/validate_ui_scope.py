#!/usr/bin/env python3
"""Consumer scope validator. CLI and framework plugin share the same checks."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'ai-governance-framework'))
from governance_tools.validator_interface import DomainValidator,ValidatorResult
BASE='652ce0ea38cfe2bb4b07b942a5cdae3db823e0f2'
# Owner explicitly approved this exact metadata addition on 2026-10-20.
PLAN_HEADER='> **最後更新**: 2026-10-20\n> **Owner**: Gavin\n> **Freshness**: Phase (30d)\n> 本表頭僅記錄治理導入日；故事仍停在 S3，未授權 S4。UI 進度見 ui-prototype/PLAN.md。\n\n'.encode()

def git_read(*args, text=False):
    bindings=ROOT/'.codex/governance-bindings.json'
    item=json.loads(bindings.read_text(encoding='utf-8'))['executables']['git'] if bindings.exists() else None
    executable=Path(item['path'] if item else shutil.which('git') or '').resolve()
    if not executable.is_file(): raise RuntimeError('Git executable is unavailable')
    if item and (executable.stat().st_size!=item['size'] or hashlib.sha256(executable.read_bytes()).hexdigest()!=item['sha256']):
        raise RuntimeError('Git executable bytes changed')
    environment={key:os.environ[key] for key in ['SystemRoot','WINDIR'] if key in os.environ}
    environment.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_NO_REPLACE_OBJECTS='1',GIT_TERMINAL_PROMPT='0')
    return subprocess.check_output([str(executable),*args],cwd=ROOT,env=environment,text=text)

def inspect_scope():
    protected=['README.md','PLAN.md','SLICES.md']
    protected+=git_read('ls-tree','-r','--name-only',BASE,'docs',text=True).splitlines()
    errors=[]
    for rel in protected:
        original=git_read('show',f'{BASE}:{rel}')
        expected=(PLAN_HEADER+original) if rel=='PLAN.md' else original
        if not (ROOT/rel).exists() or (ROOT/rel).read_bytes()!=expected: errors.append(f'Planning modified: {rel}')
    if (ROOT/'.github/workflows').exists() and any((ROOT/'.github/workflows').iterdir()): errors.append('GitHub Actions are not authorized')
    if (ROOT/'LICENSE').exists(): errors.append('Story-wide LICENSE is not authorized')
    for rel in ['party-v1.png','units-v1.png','battlefield-v1.png','campaign-v1.png']:
        if not (ROOT/'ui-prototype/public/art'/rel).is_file(): errors.append(f'Missing art: {rel}')
    return errors,len(protected)

class UIPrototypeScopeValidator(DomainValidator):
    @property
    def rule_ids(self): return ['game-ui-prototype','UI_PLANNING_PRESERVED','UI_NO_ACTIONS','UI_ART_PRESENT']
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
