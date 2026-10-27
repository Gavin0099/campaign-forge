"""Supplementary native viewport render timers, measured separately from W4/W5."""
import json
from pathlib import Path
from summarize_perf07 import stat
OUT=Path(__file__).resolve().parents[1]/'docs/evidence/spike07'
def main():
    summary={};lines=['','## W6 supplemental native viewport render timers','',
        'Same common states/event replay,3 repetitions/cell, separate sequential native720p runs. RenderingServer viewport measurement enabled explicitly; no movie/readback. Samples are previous completed viewport render CPU/GPU milliseconds, not whole-frame CPU; scopes overlap and must not be added. W4/W5 original tables remain unchanged.','',
        '| Build | Workload | Wall mean / p95 / worst | Render CPU mean / p95 / worst | Render GPU mean / p95 / worst |',
        '| --- | --- | --- | --- | --- |']
    for tag in ['spike05','spike06','before','after']:
        data=json.loads((OUT/'perf'/f'render-{tag}.json').read_text(encoding='utf-8-sig'))
        assert data['render_timers'],tag
        if tag=='spike05' and (OUT/'perf/render-spike05-clean-scroll.json').exists():
            clean=json.loads((OUT/'perf/render-spike05-clean-scroll.json').read_text(encoding='utf-8-sig'))
            data['reports']=[r for r in data['reports'] if not r['workload'].startswith('scroll-')]+clean['reports']
        summary[tag]={}
        for workload in ['scroll-T2','scroll-wave','enemy-normal','enemy-2x']:
            reports=[r for r in data['reports'] if r['workload']==workload];assert len(reports)==3
            frames=[f for r in reports for f in r['frames']]
            metrics={k:stat([f[k] for f in frames]) for k in ['ms','render_cpu_ms','render_gpu_ms']}
            assert metrics['render_gpu_ms']['mean']>0
            summary[tag][workload]=metrics
            def fmt(s):return f"{s['mean']:.2f} / {s['p95']:.2f} / {s['worst']:.2f}"
            lines.append(f"| {tag} | {workload} | {fmt(metrics['ms'])} | {fmt(metrics['render_cpu_ms'])} | {fmt(metrics['render_gpu_ms'])} |")
    (OUT/'perf/render-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines+=['','### Actual enemy phases including synchronous AI','',
        'Same reached input wave state; each build plays its own AI result, and measurement begins BEFORE AI evaluation. First-frame CPU/action spikes are included. Three repeats per speed; no readback/movie/concurrent Godot. Pre-kit05 results may differ; original matched-event table isolates rendering separately.','',
        '| Build | Workload | Mean / p95 / worst ms | Render CPU mean | Render GPU mean |','| --- | --- | --- | --- | --- |']
    full={}
    for tag in ['spike05','spike06','after']:
        path=OUT/'perf'/f'actual-{tag}.json'
        if not path.exists():continue
        actual=json.loads(path.read_text(encoding='utf-8-sig'))
        assert actual['include_ai'] and actual['render_timers']
        full[tag]={}
        for workload in ['enemy-normal','enemy-2x']:
            rows=[r for r in actual['reports'] if r['workload']==workload];assert len(rows)==3
            frames=[f for r in rows for f in r['frames']]
            s=stat([f['ms'] for f in frames]);cpu=stat([f['render_cpu_ms'] for f in frames]);gpu=stat([f['render_gpu_ms'] for f in frames])
            full[tag][workload]={'wall_ms':s,'render_cpu_ms':cpu,'render_gpu_ms':gpu}
            lines.append(f"| {tag} | {workload} | {s['mean']:.2f} / {s['p95']:.2f} / {s['worst']:.2f} | {cpu['mean']:.2f} | {gpu['mean']:.2f} |")
    (OUT/'perf/actual-after-summary.json').write_text(json.dumps(full,indent=2)+'\n')
    path=OUT/'PERFORMANCE.md'
    old=path.read_text(encoding='utf-8-sig').split('\n## W6 supplemental native viewport render timers')[0]
    path.write_text(old+'\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines))
if __name__=='__main__':main()
