"""Offline stratification; fixed seeds are deterministic probes, not independent samples."""
import json
import math
import sys
from pathlib import Path
from summarize_spike06 import aggregate, span

ROOT = Path(__file__).resolve().parents[1]

def wilson(k, n):
    if not n:
        return None
    z = 1.96
    p = k / n
    den = 1 + z*z/n
    mid = (p + z*z/(2*n))/den
    half = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return [mid-half, mid+half]

def summarize(folder):
    result = aggregate(folder, write=False, verbose=False)
    index = json.loads((folder/'index.json').read_text(encoding='utf-8-sig'))
    runs = [json.loads((folder/p).read_text(encoding='utf-8-sig')) for p in index['runs']]
    result['sample_caveat'] = 'Distinct traces are not independent samples; Wilson intervals describe probe counts, not human win probability.'
    for policy, v in result['policies'].items():
        rows = [r for r in runs if r['policy']==policy]
        v['win_interval95'] = wilson(sum(r['status']=='win' for r in rows),len(rows))
        v['bypass_wins'] = sum(r['bypass_win'] for r in rows)
        v['bypass_interval95'] = wilson(v['bypass_wins'],len(rows))
        v['scout_early_death_runs'] = sum(any(d['kind']=='mobile' and d['turn']<4 for d in r['ally_deaths']) for r in rows)
        v['scout_no_early_death_rate'] = 1-v['scout_early_death_runs']/len(rows)
        v['strata'] = {}
        for outcome in ['bypass-win','engaged-win','loss-Thoma','loss-timeout']:
            group = [r for r in rows if r['outcome']==outcome]
            v['strata'][outcome] = {
                'count':len(group), 'rate':len(group)/len(rows), 'interval95':wilson(len(group),len(rows)),
                'turns':span([r['turns_to_result'] for r in group]),
                'deaths':{kind:span([sum(d['kind']==kind for d in r['ally_deaths']) for r in group]) for kind in ['melee','ranged','mobile']},
                'wave_engaged':sum(r['reinforcement_first_engage_turn']>=0 for r in group),
                'wave_first_engage':span([r['reinforcement_first_engage_turn'] for r in group if r['reinforcement_first_engage_turn']>=0]),
                'scout_death_turns':span([d['turn'] for r in group for d in r['ally_deaths'] if d['kind']=='mobile']),
                'distinct_traces':len({r['trace_hash'] for r in group})}
    (folder/'aggregate.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines = ['# Stratified deterministic probes','',result['sample_caveat'],'',
        '| Policy | Wins (95% Wilson) | Bypass wins | No scout death <T4 | Distinct traces |',
        '| --- | --- | --- | --- | --- |']
    for name,v in result['policies'].items():
        lo,hi=v['win_interval95']
        lines.append(f"| {name} | {v['win_rate']:.1%} [{lo:.1%}, {hi:.1%}] | {v['bypass_wins']}/{v['runs']} | {v['scout_no_early_death_rate']:.1%} | {v['distinct_traces']}/{v['runs']} |")
    lines += ['', '| Policy × outcome | n | Rate [95%] | Turn median [range] | Wave engaged | Scout death turns |','| --- | --- | --- | --- | --- | --- |']
    for name,v in result['policies'].items():
        for key,s in v['strata'].items():
            lo,hi=s['interval95']
            lines.append(f"| {name} / {key} | {s['count']} | {s['rate']:.1%} [{lo:.1%}, {hi:.1%}] | {s['turns']} | {s['wave_engaged']} | {s['scout_death_turns']} |")
    (folder/'BASELINE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines[:11]))
    return result

if __name__=='__main__':
    summarize(ROOT / sys.argv[1])
