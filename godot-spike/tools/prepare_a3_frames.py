"""A3 surgical garment repaint. No original/reference/raw PNG is overwritten.

Preserve A2 registration, silhouette and all pixels outside explicit garment masks.
Warp generated cuff/hem cloth into A2 poses and copy the original leafy motif.
The masks deliberately exclude mace, hands, face, satchel, medallion and boots.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import hashlib
import json

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / 'shared-anim'
EVIDENCE = REPO / 'godot-spike/docs/evidence/spike02-a3'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

def solve(a, b):
    rows = [list(map(float, row)) + [float(v)] for row, v in zip(a, b)]
    for i in range(len(rows)):
        pivot = max(range(i, len(rows)), key=lambda j: abs(rows[j][i]))
        rows[i], rows[pivot] = rows[pivot], rows[i]
        div = rows[i][i]
        assert abs(div) > 1e-10
        rows[i] = [v / div for v in rows[i]]
        for j in range(len(rows)):
            if j != i:
                factor = rows[j][i]
                rows[j] = [v - factor * w for v, w in zip(rows[j], rows[i])]
    return [row[-1] for row in rows]

def warp_patch(out, source, src, dst, strength=255):
    equations, values = [], []
    for (x, y), (u, v) in zip(dst, src):
        equations += [[x,y,1,0,0,0,-u*x,-u*y], [0,0,0,x,y,1,-v*x,-v*y]]
        values += [u,v]
    warped = source.transform((512,512), Image.Transform.PERSPECTIVE, solve(equations, values), Image.Resampling.BICUBIC)
    mask = Image.new('L', (512,512))
    ImageDraw.Draw(mask).polygon(dst, fill=strength)
    mask = mask.filter(ImageFilter.GaussianBlur(0.65))
    # Never add alpha outside the A2 silhouette or replace it with a raw edge halo.
    mask = ImageChops.multiply(mask, out.getchannel('A').point(lambda x: 255 if x > 240 else 0))
    mask = ImageChops.multiply(mask, warped.getchannel('A').point(lambda x: 255 if x > 240 else 0))
    original_alpha = out.getchannel('A')
    out.paste(warped, (0,0), mask)
    out.putalpha(original_alpha)
    return mask

def rect(x0,y0,x1,y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]

# Each patch records four raw-image corners -> four A2 garment corners, clockwise.
# The selected interiors avoid hands and equipment; original silhouettes stay exact.
PATCHES = {
 '00': [
  ([(264,313),(321,286),(376,394),(270,411)], [(116,146),(134,140),(155,179),(121,182)]),
  ([(916,503),(971,522),(931,628),(864,590)], [(338,211),(356,220),(341,262),(319,246)]),
  ([(408,1002),(641,1074),(628,1090),(411,1020)], [(161,387),(238,414),(235,425),(157,401)]),
 ],
 '01': [
  ([(309,261),(411,233),(430,324),(354,336)], [(149,156),(178,145),(184,174),(160,175)]),
  ([(804,459),(887,461),(860,564),(829,545)], [(301,212),(328,215),(317,250),(307,240)]),
  ([(411,1029),(640,1091),(638,1112),(408,1050)], [(165,384),(235,410),(235,422),(161,398)]),
 ],
 '02': [
  ([(758,373),(856,336),(856,458),(716,448)], [(302,183),(337,173),(337,214),(290,211)]),
  ([(843,536),(912,559),(868,639),(824,605)], [(332,236),(354,246),(338,273),(322,259)]),
  ([(308,987),(529,1079),(521,1098),(292,1008)], [(145,392),(215,421),(208,431),(136,403)]),
 ],
 '03': [
  ([(688,340),(781,337),(754,440),(634,417)], [(300,184),(331,184),(320,219),(282,211)]),
  ([(701,507),(746,524),(708,602),(684,578)], [(313,243),(328,248),(316,268),(304,260)]),
  ([(270,969),(508,1074),(496,1092),(262,997)], [(155,396),(227,419),(222,429),(147,408)]),
 ],
 '04': [
  ([(721,560),(807,560),(887,631),(806,668)], [(275,252),(300,254),(330,277),(294,298)]),
  ([(377,402),(465,405),(477,460),(419,450)], [(176,201),(200,207),(203,224),(186,219)]),
  ([(327,952),(509,1040),(497,1060),(315,975)], [(151,375),(208,404),(201,414),(143,391)]),
 ]
}
# Exact original sprig, without the fringe or border; same motif in all poses.
MOTIF_SOURCE = rect(214,446,260,529)
MOTIFS = {
 '00': [[(242,324),(257,320),(274,366),(257,373)], [(310,299),(322,296),(341,333),(329,340)]],
 '01': [[(235,322),(251,323),(254,364),(236,365)], [(297,306),(309,303),(324,338),(311,343)]],
 '02': [[(226,331),(242,338),(230,373),(212,368)], [(328,313),(340,309),(352,345),(340,349)]],
 '03': [[(216,332),(231,338),(221,367),(205,363)], [(313,314),(326,309),(341,343),(328,348)]],
 '04': [[(218,323),(231,331),(212,358),(199,351)], [(126,294),(130,304),(157,291),(152,282)]],
}

def main():
    reference = Image.open(ROOT/'references/thoma.png').convert('RGBA')
    colors = [p[:3] for p in reference.getdata() if p[3] > 200]
    strip = Image.new('RGB',(len(colors),1)); strip.putdata(colors)
    palette = strip.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    attempts = json.loads((ROOT/'a3-swing-prompts.json').read_text(encoding='utf-8'))
    audit = json.loads((ROOT/'frame-audit.json').read_text(encoding='utf-8'))
    baseline = []
    for path in sorted((EVIDENCE/'baseline-a2').glob('*')):
        if path.name == 'hashes.json':
            continue
        baseline.append({'path':path.relative_to(REPO).as_posix(), 'sha256':sha(path)})
    write(EVIDENCE/'baseline-a2/hashes.json',baseline)
    masks = EVIDENCE/'repaint-masks'; masks.mkdir(exist_ok=True)
    for entry in attempts:
        index = Path(entry['frame']).stem
        raw = Image.open(ROOT/entry['raw']).convert('RGBA')
        old = Image.open(EVIDENCE/'baseline-a2'/f'{index}.png').convert('RGBA')
        out = old.copy(); combined = Image.new('L',(512,512))
        for src,dst in PATCHES[index]:
            combined = ImageChops.lighter(combined,warp_patch(out,raw,src,dst))
        for dst in MOTIFS[index]:
            combined = ImageChops.lighter(combined,warp_patch(out,reference,MOTIF_SOURCE,dst))
        # Re-quantize edited pixels only; original pixels remain byte-exact elsewhere.
        quantized = out.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
        quantized.putalpha(old.getchannel('A'))
        edit_mask = combined.point(lambda x:255 if x else 0)
        final = Image.composite(quantized,old,edit_mask)
        final.putalpha(old.getchannel('A'))
        final.save(ROOT/entry['frame'],optimize=True)
        edit_mask.save(masks/f'{index}.png',optimize=True)
        assert final.size == (512,512)
        assert final.getchannel('A').tobytes() == old.getchannel('A').tobytes()
        assert ImageChops.difference(final,old).convert('RGB').getbbox() is not None
        entry.update(raw_sha256=sha(ROOT/entry['raw']),runtime_sha256=sha(ROOT/entry['frame']),
            reference_sha256={p:sha(REPO/p) for p in entry['references']},
            accepted='garment-patches-only; full generated figure not adopted',
            generated_size=list(raw.size),runtime_size=[512,512],pivot=[256,464],
            cleanup='Perspective-warp interior cuff/hem patches; transplant original sprig; feather 0.65px; discard alpha <=240 at patch edges; quantize edited pixels to original 128-color palette; preserve entire A2 alpha and all unmasked pixels.',
            patch_quads=PATCHES[index],motif_source=MOTIF_SOURCE,motif_targets=MOTIFS[index],
            mask=f'godot-spike/docs/evidence/spike02-a3/repaint-masks/{index}.png',
            weapon_status='APPROVED',weapon_approval='Owner, 2026-10-24')
        for row in audit:
            if row['path']==entry['frame']:
                row.update(sha256=entry['runtime_sha256'],source=entry['raw'],raw_sha256=entry['raw_sha256'],
                    status='PLACEHOLDER',reason='A3 costume patches applied; detailed W3 style review pending.',
                    cleanup=entry['cleanup'])
    write(ROOT/'a3-swing-prompts.json',attempts)
    write(ROOT/'frame-audit.json',audit)
    source=(ROOT/'SOURCES.md').read_text(encoding='utf-8').split('\n## spike-02 A3')[0]
    lines=['','## spike-02 A3','',
      'Weapon APPROVED (Owner, 2026-10-24). Five image_gen attempts total, one per swing 00-04. Raw originals retained unchanged. Only garment patches are accepted; generated full-figure geometry is not adopted. No rejected attempt was discarded. No other character or environment generated.',
      'Reproduction: `godot-spike/tools/prepare_a3_frames.py`. A2 byte-copy baseline and hashes: `godot-spike/docs/evidence/spike02-a3/baseline-a2/`. No baseline path is in the manifest. Exact original embroidery is composited rather than invented. Canvas/pivot, mace/head/grip/contact geometry, source silhouette and timing stay fixed. Remaining contour/style drift is assessed separately in W3.','']
    for e in attempts:
        lines += [f"### {e['frame']} attempt {e['attempt']}",'Tool: image_gen (built-in).',e['prompt'],
            'References and SHA-256: '+json.dumps(e['reference_sha256']),
            f"Raw: `{e['raw']}` SHA-256 `{e['raw_sha256']}` ({e['generated_size']}); full generated figure is not a runtime asset.",
            'Cleanup: '+e['cleanup'],f"Runtime SHA-256: `{e['runtime_sha256']}`.",'']
    (ROOT/'SOURCES.md').write_text(source+'\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print('A3_REPAINT frames=5 attempts_per_frame=1 original_alpha_and_unmasked_pixels_preserved=true')

if __name__=='__main__':
    main()
