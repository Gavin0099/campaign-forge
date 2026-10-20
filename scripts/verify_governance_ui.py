#!/usr/bin/env python3
"""Verify the UI plan using the canonical repo memory, rules, and contract.

Use the repo as runtime root so Windows checkouts do not need symlink privileges.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'ai-governance-framework'))
from governance_tools.quickstart_smoke import run_quickstart_smoke
from governance_tools.domain_validator_loader import preflight_domain_validators
result=run_quickstart_smoke(project_root=ROOT,plan_path=ROOT/'ui-prototype/PLAN.md',contract_file=ROOT/'contract.yaml',task_text='Verify the authorized UI prototype scope; no formal story or rule changes.')
result['scope']='UI plan manual smoke using canonical repo runtime root; not automatic Codex lifecycle or real Git trigger evidence.'
result['validator_preflight']=preflight_domain_validators(ROOT/'contract.yaml')
result['ok']=result['ok'] and result['validator_preflight']['ok']
out=ROOT/'artifacts/governance-ui-quickstart.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'ok':result['ok'],'pre_task_ok':result['pre_task_ok'],'session_start_ok':result['session_start_ok'],'validator_preflight_ok':result['validator_preflight']['ok'],'evidence':str(out)},ensure_ascii=False))
sys.exit(0 if result['ok'] else 1)
