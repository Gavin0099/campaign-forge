"""Offline evidence aggregation. No subprocess, network, or game simulation."""
import json
import statistics as stats
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def span(values):
    return {'median': stats.median(values), 'min': min(values), 'max': max(values)} if values else None

def finishes(row, kind):
    if 'finishing_kills' in row:
        return row['finishing_kills'].get(kind,0)
    units = {u['id']:u for u in row['final_units']}
    return sum(e['event']['type']=='damage' and e['event']['hp_after']==0
        and units[e['event']['source']]['side']=='ally'
        and units[e['event']['source']]['kind']==kind
        and e['event']['amount']<units[e['event']['unit']]['max_hp']
        for e in row['trace'] if e['event']['type']=='damage')

def aggregate(folder, write=True, verbose=True):
    index = json.loads((folder/'index.json').read_text(encoding='utf-8-sig'))
    runs = [json.loads((folder/p).read_text(encoding='utf-8-sig')) for p in index['runs']]
    result = {'seeds': index['seeds'], 'variant': index['variant'], 'variation': index['variation'], 'policies': {}}
    for name in index['policies']:
        rows = [r for r in runs if r['policy']==name]
        wins = [r for r in rows if r['status']=='win']
        idle = {g:sum(r['enemy_idle_by_group'].get(g,0) for r in rows) for g in rows[0]['enemy_idle_by_group']}
        observed = sum(sum(u['side']=='enemy' and u['eligible'] and u['observed'] for u in r['unit_turns']) for r in rows)
        classes = {}
        for kind in ('melee','ranged','mobile'):
            damage = sum(r['archetypes'].get(kind,{}).get('damage_dealt',0) for r in rows)
            kills = sum(r['archetypes'].get(kind,{}).get('kills',0) for r in rows)
            classes[kind] = {'damage':damage, 'kills':kills,
                'mean_casualties':sum(sum(d['kind']==kind for d in r['ally_deaths']) for r in rows)/len(rows),
                'death_turns':span([d['turn'] for r in rows for d in r['ally_deaths'] if d['kind']==kind]),
                'living_unit_turns':sum(r['archetypes'].get(kind,{}).get('unit_turns',0) for r in rows),
                'finishing_kills':sum(finishes(r,kind) for r in rows),
                'intercepts':sum(r.get('intercepts',{}).get(kind,0) for r in rows)}
        for c in classes.values():
            c['damage_share']=c['damage']/max(1,sum(v['damage'] for v in classes.values()))
            c['kill_share']=c['kills']/max(1,sum(v['kills'] for v in classes.values()))
        result['policies'][name] = {'runs':len(rows),'win_rate':len(wins)/len(rows),
            'win_turns':span([r['turns_to_result'] for r in wins]),
            'loss_turns':span([r['turns_to_result'] for r in rows if r['status']=='lose']),
            'first_contact':span([r['first_contact_turn'] for r in rows if r['first_contact_turn']>=0]),
            'mean_casualties':stats.mean(len(r['ally_deaths']) for r in rows),
            'reinforcement_engagement_rate':stats.mean(r['reinforcement_first_engage_turn']>=0 for r in rows),
            'reinforcement_engagement_in_wins':sum(r['reinforcement_first_engage_turn']>=0 for r in wins)/len(wins) if wins else None,
            'wave_first_engage':span([r['reinforcement_first_engage_turn'] for r in rows if r['reinforcement_first_engage_turn']>=0]),
            'wave_first_attack':span([r['reinforcement_first_attack_turn'] for r in rows if r['reinforcement_first_attack_turn']>=0]),
            'wave_first_attacked':span([r['reinforcement_first_attacked_turn'] for r in rows if r['reinforcement_first_attacked_turn']>=0]),
            'idle_by_group':idle,'observed_enemy_turns':observed,'true_idle_share':sum(idle.values())/max(1,observed),
            'classes':classes,'los_blocked_shots':sum(r['los_blocked_shots'] for r in rows),
            'los_blocked_opportunities':sum(r['los_blocked_opportunities'] for r in rows),
            'length_minutes':[min(r['battle_length_estimate_minutes'][0] for r in rows),max(r['battle_length_estimate_minutes'][1] for r in rows)],
            'median_length_minutes':[stats.median(r['battle_length_estimate_minutes'][i] for r in rows) for i in (0,1)],
            'length_intervals_inside_target':sum(15<=r['battle_length_estimate_minutes'][0] and r['battle_length_estimate_minutes'][1]<=25 for r in rows),
            'distinct_traces':len({r['trace_hash'] for r in rows}),
            'illegal_commands':sum(len(r['illegal_commands']) for r in rows)}
    if write:
        (folder/'aggregate.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    if verbose:
        print(json.dumps(result['policies'],indent=2))
    return result

if __name__=='__main__':
    aggregate(ROOT / sys.argv[1])
