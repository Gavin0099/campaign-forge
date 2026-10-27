"""Offline native-frame statistics; inclusive CPU scopes are not additive."""
import json
import statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'docs/evidence/spike07'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def stat(values):
    values=sorted(values)
    return {'n':len(values),'mean':statistics.mean(values),'p95':values[min(len(values)-1,int(.95*len(values)))],'worst':max(values)} if values else None
def main():
    builds={}
    for name in ['spike05','spike06','before','diagnostic','after']:
        path=ROOT/'perf'/f'{name}.json'
        if not path.exists(): continue
        data=read(path); groups={}
        for r in data['reports']: groups.setdefault(r['workload'],[]).append(r)
        builds[name]={}
        for workload,rows in groups.items():
            frames=[f for r in rows for f in r['frames']]
            scopes={}
            for r in rows:
                for key,s in r['scopes'].items():
                    v=scopes.setdefault(key,{'calls':0,'usec':0,'max_usec':0})
                    v['calls']+=s['calls'];v['usec']+=s['usec'];v['max_usec']=max(v['max_usec'],s['max_usec'])
            for s in scopes.values():
                s['ms_per_frame']=s['usec']/1000/len(frames)
                s['calls_per_frame']=s['calls']/len(frames)
            builds[name][workload]={
                'repetitions':len(rows),'wall_ms':stat([f['ms'] for f in frames]),
                'repeat_wall_ms':[stat([f['ms'] for f in r['frames']]) for r in rows],
                'process_ms':stat([f['process_ms'] for f in frames]),
                'physics_ms':stat([f['physics_ms'] for f in frames]),
                'draw_calls':stat([f['draw_calls'] for f in frames]),
                'objects':stat([f['objects'] for f in frames]),'nodes':stat([f['nodes'] for f in frames]),
                'scopes':scopes,'ai_ms':stat([r['ai_ms'] for r in rows if 'ai_ms' in r]),
                'ai_scopes':[r['ai_scopes'] for r in rows if 'ai_scopes' in r]}
    (ROOT/'perf/profile-before.json').write_text(json.dumps({k:v for k,v in builds.items() if k!='after'},indent=2)+'\n')
    if 'after' in builds: (ROOT/'perf/profile-after.json').write_text(json.dumps(builds['after'],indent=2)+'\n')
    lines=['# Native 720p performance','',
        'Three repetitions per cell; GL Compatibility, AMD780M, max60FPS, VSync off. No movie/readbacks/concurrent Godot. Exact git exports; same reached spike06 flank24018 T2 and waveT8, same enemy event replay. AI evaluated separately. CPU scopes inclusive and overlapping; wall minus process is not GPU time. No GPU timer is claimed.','',
        '| Build | Workload | Mean / p95 / worst ms | Sampled TIME_PROCESS monitor ms | Draw calls mean | Pure AI ms mean |',
        '| --- | --- | --- | --- | --- | --- |']
    for name,workloads in builds.items():
        for key,v in workloads.items():
            s=v['wall_ms'];ai=v['ai_ms']
            lines.append(f"| {name} | {key} | {s['mean']:.2f} / {s['p95']:.2f} / {s['worst']:.2f} | {v['process_ms']['mean']:.2f} | {v['draw_calls']['mean']:.1f} | {ai['mean'] if ai else '—'} |")
    (ROOT/'PERFORMANCE.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines[4:]))
if __name__=='__main__':main()
