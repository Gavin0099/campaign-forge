"""Compact ablation outcome tables; incomplete candidates are labelled, never accepted."""
import json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]/'docs/evidence/spike07'

def main():
    table=[]
    for p in sorted((OUT/'ablation').glob('*/runs.json')):
        rows=json.loads(p.read_text())
        summary={}
        for policy in ['road','flank','turtle','scout-retreat','leader-dash','bypass']:
            group=[r for r in rows if r['policy']==policy]
            summary[policy]={'n':len(group),'wins':sum(r['status']=='win' for r in group),
                'bypass_wins':sum(r['bypass_win'] for r in group),
                'zero_death_T6_wavefree':sum(r['bypass_win'] and r['turns_to_result']==6 and not r['ally_deaths'] for r in group)}
        table.append({'case':p.parent.name,'complete':len(rows)==240,'policies':summary})
    (OUT/'ablation/summary.json').write_text(json.dumps(table,indent=2)+'\n',encoding='utf-8')
    lines=['# Single-lever and combination ablations','',
        'Each complete row: same 40 seeds × six policies. Original spike06 operator; fixed HP/damage/move/ranges/LOS/kit/objective. Incomplete trials are excluded from acceptance.',
        '', '| Case | road wins | flank wins | turtle wins | retreat wins | dash wins / wave-free | scripted wins / wave-free / free T6 |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    for c in table:
        if not c['complete']: continue
        p=c['policies'];d=p['leader-dash'];b=p['bypass']
        lines.append('| '+c['case']+' | '+' | '.join(str(p[n]['wins'])+'/40' for n in ['road','flank','turtle','scout-retreat'])+f" | {d['wins']}/{d['bypass_wins']} | {b['wins']}/{b['bypass_wins']}/{b['zero_death_T6_wavefree']} |")
    lines += ['', 'post-one = leader and hold point(21,9); leader-post/post = (22,9), from(20,9). wave-t4 / wave-t3 = arrival4 /3, from5; warning always arrival−1; original birth rest retained. fallback = announced one-cell step toward wave, counter otherwise unchanged. No terrain or objective gate.',
        'T5 partial-start probes with earlier waves preserve authored birth age, but do not simulate pre-placement pursuit: staged full-HP allies and entry wave, explicitly not full battles.',
        'All compact traces use their own fixed-phase event collector; their hashes are not full-telemetry hashes. Distinct traces are not independent samples.']
    (OUT/'ablation/ABLATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for c in table:
        print(c['case'],'complete=',c['complete'],[(p,v['wins'],v['bypass_wins'],v['zero_death_T6_wavefree']) for p,v in c['policies'].items()])

if __name__=='__main__': main()
