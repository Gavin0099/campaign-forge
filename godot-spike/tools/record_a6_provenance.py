"""Complete records from retained files; never change generation prompt text."""
from prepare_a6_frames import *

def main():
    rows=load(SHARED/'a6-swing-prompts.json')
    for row in rows:
        row['raw_sha256']=sha(REPO/row['raw'])
        for ref in row['references']:
            path=REPO/ref['path']
            if ref['role'].startswith('A5') and BASE.exists():
                path=BASE/row['frame'].split('/')[-1]
                ref['path']=path.relative_to(REPO).as_posix()
            ref['sha256']=sha(path)
        normalized=OUT/f"normalized/{row['frame'][-6:-4]}-attempt-{row['attempt']}.json"
        if normalized.exists():row['normalization']=load(normalized)
        if row['adopted']:
            row['runtime_sha256']=sha(SHARED/row['frame'])
            assert row['runtime_sha256']==row['normalization']['normalized_sha256']
    write(SHARED/'a6-swing-prompts.json',rows)
    path=SHARED/'SOURCES.md'
    text=path.read_text(encoding='utf-8-sig').split('\n## spike-02 A6')[0]
    text+='\n## spike-02 A6 — complete per-frame regeneration\n\n'
    text+='Built-in image_gen. Exactly idle/01 + swing/05 for identity/costume/style/mace; A5 same-index ONLY for pose. No rig/region compositing. Seed/model/quality: not exposed. Transparent background requested. Maximum 4 attempts per frame. Every unchanged raw candidate retained under godot-spike/docs/evidence/spike02-a6/candidates/. Full normalization transforms, cleanup masks, palette distances and hashes in a6-swing-prompts.json. Uniform scale/translate, alpha<24 cleanup, idle/01 nearest-128-colour remap only. See A6 METHOD.md for gate and limits. Human playtest HUMAN_PENDING; model checks are not Owner art approval.\n'
    for r in rows:
        text+=f"\n### {r['frame']} attempt {r['attempt']}\n\nTool: {r['tool']}; settings: {json.dumps(r['settings'])}\n\n"
        text+='References: '+json.dumps(r['references'])+'\n\n'
        text+=r['prompt']+'\n\n'
        text+=f"Raw: {r['raw']} SHA-256 `{r['raw_sha256']}`\n\nRuntime SHA-256: `{r['runtime_sha256']}` (null = not adopted). Pick={r['pick']}, adopted={r['adopted']}. {r['reason']}\n"
        if 'normalization' in r:text+='\nNormalization and cleanup: '+json.dumps(r['normalization'])+'\n'
    path.write_text(text,encoding='utf-8',newline='\n')
    print(f'A6_PROVENANCE attempts={len(rows)} adopted={sum(r["adopted"] for r in rows)}')

if __name__=='__main__':main()
