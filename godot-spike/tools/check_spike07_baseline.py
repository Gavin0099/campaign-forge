"""Compare recorded original seeds; never re-label or synthesize simulations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/evidence/spike07'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def main():
    checks=[]
    for policy in ['road','flank','turtle','scout-retreat','bypass']:
        for seed in [24018,*range(1001,1020)]:
            a=read(ROOT/f'docs/evidence/spike06/after/runs/{policy}-{seed}.json')
            b=read(OUT/f'baseline/runs/{policy}-{seed}.json')
            for key in ['trace_hash','commands','status','turns_to_result','archetypes','unit_turns','reinforcement_first_engage_turn']:
                assert a[key]==b[key],(policy,seed,key)
            for old,new in zip(a['ally_deaths'],b['ally_deaths']):
                assert all(new[k]==v for k,v in old.items())
            checks.append({'policy':policy,'seed':seed,'original_metrics_match':True})
    for policy,k in [('road',10),('flank',14)]:
        assert sum(read(OUT/f'baseline/runs/{policy}-{s}.json')['status']=='win' for s in [24018,*range(1001,1020)])==k
    for s in [1014,1015,1017]:
        r=read(OUT/f'baseline/runs/bypass-{s}.json')
        assert r['bypass_win'] and r['turns_to_result']==6 and not r['ally_deaths']
    (OUT/'baseline/original20-reproduction.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print('PASS: 100 original runs match traces/commands/outcomes/original metrics; 14/20 flank, 10/20 road, three T6 zero-death bypasses.')

if __name__=='__main__': main()
