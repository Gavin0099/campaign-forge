"""Build explicitly labeled asset sheets and per-frame model style observations."""
from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import json, math, hashlib
ROOT=Path(__file__).resolve().parents[2]/'shared-anim'
OUT=ROOT.parent/'godot-spike/docs/evidence/spike02-a3'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

PATHS=['thoma/idle/00.png','thoma/idle/01.png']+[f'thoma/swing/{i:02}.png' for i in range(6)]
# Stole / cuffs / hem crops in fixed 512px coordinates. No frame auto-fit.
DETAILS=[
 [(202,304,303,387),(151,237,203,286),(164,356,326,423)],
 [(209,302,306,386),(151,239,202,287),(163,357,328,424)],
 [(225,293,356,396),(108,133,169,192),(143,359,371,433)],
 [(222,300,337,385),(140,126,199,191),(151,353,365,429)],
 [(198,304,369,392),(278,161,353,227),(126,357,387,436)],
 [(192,302,352,386),(272,170,341,231),(138,357,366,434)],
 [(109,278,259,374),(262,235,342,311),(130,348,352,422)],
 [(211,300,307,386),(151,238,202,287),(163,354,330,426)],
]
REASONS={
 '00':'Leaf sprigs now come from the original, but doubled border/leaf density remains at patch edges; raised cuff transition and broad fan hem still differ from idle/recover.',
 '01':'Original sprigs improve identity, but stole border blending and raised cuff folds still differ; the bell-shaped hem is retained from A2.',
 '02':'Original sprigs and cuff cloth improve continuity, but compressed leaf detail, cuff patch boundary and swept underskirt contour still drift.',
 '03':'Contact geometry is byte-preserved; stole seam/leaf density and broad underskirt hem remain inconsistent at detail scale.',
 '04':'Trailing sprigs reuse original pixels, but stretched diagonal embroidery, front cuff transition and trailing hem remain visibly different.',
}

def main():
    sheet=Image.new('RGB',(2048,1040),(34,40,38));d=ImageDraw.Draw(sheet)
    d.text((8,6),'A3 MODEL STYLE CHECK - ASSET SHEET, NOT A RUNTIME SCREENSHOT',fill='#eee7d6')
    for col,path in enumerate(PATHS):
        im=Image.open(ROOT/path).convert('RGBA');x=col*256
        d.text((x+5,27),'ORIGINAL' if col==0 else path,fill='#eee7d6')
        small=im.resize((256,256),Image.Resampling.LANCZOS);sheet.paste(small,(x,48),small)
        for row,(label,box) in enumerate(zip(['STOLE / EMBROIDERY','CUFF','HEM'],DETAILS[col])):
            top=316+row*195;d.text((x+5,top),label,fill='#d2b777')
            crop=im.crop(box);crop.thumbnail((246,170),Image.Resampling.LANCZOS)
            # Enlarge every detail 2x, within each column; cropping is explicit.
            scale=min(246/(box[2]-box[0]),170/(box[3]-box[1]))
            crop=im.crop(box).resize((round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)),Image.Resampling.NEAREST)
            sheet.paste(crop,(x+(256-crop.width)//2,top+20),crop)
        runtime=im.resize((68,68),Image.Resampling.LANCZOS);sheet.paste(runtime,(x+94,939),runtime)
    d.text((8,914),'Native 720p-size row: ~48px body / 68px canvas. Detail rows are enlarged for inspection.',fill='#eee7d6')
    sheet.save(ROOT/'thoma-weapon-style-check.png',optimize=True)
    before_after=Image.new('RGB',(1536,596),(34,40,38));draw=ImageDraw.Draw(before_after)
    for row in range(2):
        draw.text((8,row*298+5),'A2 BASELINE - asset sheet' if row==0 else 'A3 REPAINT - asset sheet; runtime evidence is separate',fill='#eee7d6')
        for i in range(6):
            path=OUT/'baseline-a2'/f'{i:02}.png' if row==0 else ROOT/'thoma/swing'/f'{i:02}.png'
            im=Image.open(path).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
            before_after.paste(im,(i*256,row*298+30),im)
            draw.text((i*256+8,row*298+280),f'swing/{i:02}',fill='#eee7d6')
    before_after.save(OUT/'contact-sheet-old-vs-new.png',optimize=True)
    reference=Image.open(ROOT/'references/thoma.png').convert('RGBA')
    colors=[p[:3] for p in reference.getdata() if p[3]>200]
    strip=Image.new('RGB',(len(colors),1));strip.putdata(colors)
    palette=strip.quantize(colors=128,method=Image.Quantize.MEDIANCUT).getpalette()
    rgb=[tuple(palette[i:i+3]) for i in range(0,384,3)]
    audit=json.loads((ROOT/'frame-audit.json').read_text(encoding='utf-8'))
    for row in audit:
        if not row['path'].startswith('thoma/'):continue
        im=Image.open(ROOT/row['path']).convert('RGBA')
        counts=Counter(p[:3] for p in im.getdata() if p[3]>240)
        mean=sum(n*min(math.dist(c,p) for p in rgb) for c,n in counts.items())/sum(counts.values())
        motion='/swing/' in row['path'] and not row['path'].endswith('05.png')
        reason=REASONS[Path(row['path']).stem] if motion else 'Recognizable original face, paired ivory leafy stole, layered cuffs/hem and equipment continuity at review and runtime scale; not Owner art approval.'
        row.update(status='PLACEHOLDER' if motion else 'PASS',reason=reason,sha256=sha(ROOT/row['path']),
            review_segment='spike-02 A3',review_authority='model visual inspection; Owner art approval not claimed',
            palette_distance={'metric':'mean nearest original 128-color Euclidean RGB distance, opaque alpha >240','value':round(mean,6),'not_a_perceptual_quality_score':True},
            style_review={
                'face':'PASS: A2 face retained, original grey hair/beard and aged features recognizable',
                'stole_cape_embroidery':('FAIL: original sprigs transferred but seam/density/shape consistency remains unresolved' if motion else 'PASS: paired ivory band and sparse leafy lower ends retained'),
                'cuffs':('FAIL: new cloth patches do not fully resolve fold/edge transitions' if motion else 'PASS: layered linen cuffs consistent at review scale'),
                'hem_silhouette':('FAIL: A2 motion contour deliberately retained to preserve geometry; broader fan/trailing silhouette remains' if motion else 'PASS: near-idle layered ivory underskirt/teal hem'),
                'palette':'PASS: original muted teal/ivory/brown palette; see numerical distance',
                'proportions':'PASS: fixed A2 registration and body proportions retained',
                'light_direction':'PASS: original top-left light retained',
                'stroke':('FAIL: local composite texture/seams remain apparent at enlarged detail scale' if motion else 'PASS at runtime scale; exact brush identity not claimed'),
                'satchel_medallion':'PASS: retained A2 pixels; holy medallion remains separate from mace',
            })
    write(ROOT/'frame-audit.json',audit)
    source=(ROOT/'SOURCES.md').read_text(encoding='utf-8').split('\n### A3 W3 style verdict')[0].rstrip()
    lines=['','### A3 W3 style verdict','',
        'Model inspection, not Owner/commercial approval. All five repaints remain PLACEHOLDER: exact source sprigs improve costume continuity but composite seams/cuffs and A2 hem contours still fail the detailed criterion. One generation attempt per frame; further whole-frame regeneration was not adopted because it moved protected geometry. Idle/recover remain unchanged PASS.','',
        '| Frame | Status | Reason |','| --- | --- | --- |']
    for row in audit:
        if row['path'].startswith('thoma/'):lines.append(f"| {row['path']} | {row['status']} | {row['reason']} |")
    lines+=['',f"Style sheet SHA-256 `{sha(ROOT/'thoma-weapon-style-check.png')}`."]
    (ROOT/'SOURCES.md').write_text(source+'\n'+'\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print('A3_STYLE_CHECK pass_frames=2 placeholder_frames=5 owner_art_approval=false')

if __name__=='__main__':main()
