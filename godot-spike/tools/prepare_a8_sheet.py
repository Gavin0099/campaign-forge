"""A8 W1: immutable anchors and brief guide layers in one 4+3 edit canvas."""
from pathlib import Path
from PIL import Image
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'godot-spike/docs/evidence/spike02-a8'
SHARED = ROOT / 'shared-anim'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def main():
    inputs = OUT / 'inputs'
    inputs.mkdir(parents=True, exist_ok=True)
    if (inputs/'hashes.json').exists():
        raise RuntimeError('W1 inputs already frozen; do not overwrite')
    baseline = OUT/'baseline-a7'
    baseline.mkdir(exist_ok=True)
    for name in ['00','01','02','03','04','05']:
        shutil.copyfile(SHARED/f'thoma/swing/{name}.png', baseline/f'{name}.png')
    for src, name in [(SHARED/'thoma/idle/01.png','idle-01.png'),
                      (SHARED/'manifest.json','manifest.json'),
                      (SHARED/'frame-audit.json','frame-audit.json')]:
        shutil.copyfile(src, baseline/name)
    shutil.copyfile(SHARED/'thoma-weapon-style-check.png', OUT/'style-check-a7.png')
    write(baseline/'hashes.json', [{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(baseline.iterdir())])
    canvas = Image.new('RGBA',(2048,1024))
    mask = Image.new('L',canvas.size,0)
    panels = []
    names = ['idle/01','swing/00','swing/01','swing/02','swing/03','swing/04','swing/05']
    for i,name in enumerate(names):
        x,y = (i%4)*512,(i//4)*512
        fixed = i in [0,6]
        source = SHARED/f'thoma/{name}.png' if fixed else ROOT/f'docs/art-briefs/thoma-swing/guides/{name.replace("/","-")}-guide.png'
        im = Image.open(source).convert('RGBA')
        if not fixed:
            im.putalpha(im.getchannel('A').point(lambda a:round(a*.38)))
            mask.paste(255,(x,y,x+512,y+512))
        # Paste rather than composite: anchor RGBA bytes retained, including hidden RGB.
        canvas.paste(im,(x,y))
        panels.append({'panel':i+1,'frame':name,'rect':[x,y,x+512,y+512],
                       'fixed':fixed,'source':source.relative_to(ROOT).as_posix(),'source_sha256':sha(source)})
    canvas.save(inputs/'sheet-canvas.png')
    mask.save(inputs/'sheet-mask.png')
    for name in ['anchors-2x.png','spec-crops.png']:
        shutil.copyfile(ROOT/f'docs/art-briefs/thoma-swing/refs/{name}',inputs/name)
    write(inputs/'sheet-layout.json', {'size':[2048,1024], 'panel_size':[512,512],
       'layout':'4+3 row-major; lower-right eighth cell intentionally empty; 2:1 avoids 7:1 tool aspect limits',
       'background':'transparent straight alpha','mask':'white editable; black fixed; native tool has no mask parameter: supply as supporting image and prose constraint, never claim enforced masking',
       'panels':panels})
    prompt = '''Use case: identity-preserve / sketch-to-render. EDIT TARGET is image 1, a seven-panel animation sheet on a 2048x1024 transparent canvas. Layout is FOUR equal 512x512 panels across TOP and THREE across BOTTOM, bottom-right cell EMPTY. Image 2 is the edit mask: WHITE opens the five middle panels; BLACK protects both anchor panels and empty cell. Images 3 and 4 are immutable appearance references. Paint ALL FIVE middle poses TOGETHER in this ONE sheet, sharing a single character design, same face, same costume, same brushwork. Do not deliver separate images.
Panel order: TOP: 1 idle/01 FIXED EXACTLY, 2 anticipation00, 3 raise01, 4 swing02. BOTTOM: 5 contact03, 6 follow-through04, 7 recover05 FIXED EXACTLY, 8 empty. Preserve panels 1 and 7 pixels; change only panels 2-6. Each figure has identical approximately 360px head-to-ground height; head about70px; shoulder width99px. Faces SCREEN RIGHT in three-quarter view. In-place registration pivot(256,464), ground y464 in EACH cell; no cast shadow. Follow the light joint scaffold as pose targets, then REMOVE ALL guide lines, text, dots and arc from finished art.
Local cell coordinates: 00 head(260,143), right weapon hand(127,117), mace HEAD(192,85), feet(145,464)/(342,439); bent arm drawn back above shoulder. 01 head(260,141), grip(194,109), mace HEAD(259,87), feet(167,464)/(326,443); raised highest anticipation. 02 head(282,145), grip(372,160), mace HEAD(449,110), feet(135,464)/(372,448); forward downswing, modest painted weapon smear allowed. 03 head(264,140), grip(358,196), mace HEAD(455,196), feet(120,464)/(354,447); horizontal fully opaque IMPACT head centered exactly455,196. 04 head(310,141), grip(347,324), mace HEAD(421,376), feet(165,455)/(334,464); forward lean with weapon following downward. All coordinates are LOCAL to each512px cell, not whole sheet. Match every target within4px. Keep the short weapon attached to the right hand and ivory sleeve. Never move the head target by moving the entire character away from its pose.
Same elderly field-medic friar as the two anchors: angular long weathered face, heavy brow, deep tiny dark eyes, projecting nose, CLOSED unsmiling mouth, grey short squared beard and moustache; very short irregular receding grey hair swept right, ear visible, NO centre part. Muted dark-teal short-sleeved overrobe and divided skirt over continuous ivory bell-shaped underrobe; ivory flared undersleeves taper to connected wrists. TWO ivory stole panels, broad shoulders/narrow waist/wider ends. EXACTLY ONE small grey-green leaf sprig on EACH stole end, TWO total, one central stem alternating oblique leaves, about4 pairs left and6 right; no diamonds, repeated flowers or extra ornaments. Short uneven ivory fringe tips4-9px, approximately10 left and8 right (+/-1), plus EXACTLY ONE long knotted waist cord. ONE brown flap satchel at SCREEN LEFT hip with ONE pale cloth roll under flap. Small round bronze medallion above belt. Two worn brown round-toed ankle boots, both attached to legs, at least one grounded at464.
Approved weapon: SHORT ONE-HANDED FLANGED MACE, dark iron angular star head with triangular fins about37x36px, worn oak haft, small brass collar, rounded pommel. Never a staff, sword, hammer block or glowing weapon. Same weapon dimensions across panels, accounting only for projection.
Match the anchors' exact muted colours and thin broken dark-brown/teal1-3px contour, mottled low-contrast hand-painted texture; no black vector lines, no cel shading, no new palette. Palette samples are not flat fill instructions: teal#405350, ivory#d8c4ad, skin#9e856c, embroidery#8d7862, leather#503323. No detached cloth triangles, duplicate bags, floating shoes, stage, scenery, labels, signatures or ground shadows. Genuine transparent RGBA background. Preserve first and last anchor panels. This is ONE SAME PAINTING moving through five poses, not five redesigned men.'''
    (inputs/'sheet-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
    write(inputs/'hashes.json',[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(inputs.iterdir())])
    print('A8_W1_PREPARED',len(panels),'panels; anchors exact; five A7 frames plus endpoint archived')

if __name__ == '__main__':
    main()
