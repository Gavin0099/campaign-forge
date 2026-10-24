"""W1: freeze A8 and define region-local A9 experiments; no runtime writes."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[2]
SHARED = ROOT/'shared-anim'
OUT = ROOT/'godot-spike/docs/evidence/spike02-a9'
A8 = ROOT/'godot-spike/docs/evidence/spike02-a8'
CHECKS = ['face_hair','stole','embroidery','tassels','cuffs','hem','palette','seams','bag_count','feet','mace','landmarks','sequence']
REGIONS = ['head','stole','embroidery','tassels','mace','legs_feet']
ORDER = ['03','02','04','00','01']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def rel(p): return Path(p).relative_to(ROOT).as_posix()
def mask(polygons):
    im=Image.new('L',(512,512));d=ImageDraw.Draw(im)
    for poly in polygons:d.polygon(poly,fill=255)
    return im
def rect(x0,y0,x1,y1):return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]

# Hand-picked outlines from A8 at native resolution, generous only at empty
# silhouette margins. Separate terminal panels let the two motifs stay distinct.
PANELS = {
 '00': [[(218,263),(239,265),(250,391),(222,393)],[(291,249),(308,249),(344,364),(312,378)]],
 '01': [[(222,265),(242,265),(252,392),(225,394)],[(294,253),(311,250),(347,366),(318,381)]],
 '02': [[(226,260),(245,265),(223,390),(191,393)],[(291,251),(309,250),(329,362),(301,371)]],
 '03': [[(210,266),(230,272),(184,399),(139,396)],[(246,264),(269,262),(278,358),(240,373)]],
 '04': [[(221,258),(243,264),(198,386),(158,381)],[(278,253),(302,251),(328,380),(290,390)]]}
HEAD_BOXES={'00':(221,99,300,179),'01':(222,99,300,178),'02':(246,99,322,178),'03':(225,99,301,176),'04':(277,99,350,180)}
HEAD_POLYS={f:[(b[0]+8,b[1]),(b[2]-12,b[1]),(b[2],b[1]+18),(b[2]-3,b[3]-10),(b[2]-20,b[3]),(b[0]+14,b[3]-5),(b[0],b[1]+35)] for f,b in HEAD_BOXES.items()}
ANCHOR_HEAD=[(224,110),(236,103),(267,101),(284,111),(287,149),(280,168),(265,175),(245,165),(230,147)]
ANCHOR_MACE=[(171,294),(179,290),(199,306),(211,317),(216,317),(217,312),(224,315),(232,315),(234,324),(241,329),(238,338),(235,348),(226,341),(218,344),(215,335),(207,329),(184,308)]

def main():
    assert not (OUT/'defects-and-targets.json').exists(),'W1 already frozen'
    base=OUT/'baseline-a8';base.mkdir(parents=True)
    for i in range(6):shutil.copyfile(SHARED/f'thoma/swing/{i:02}.png',base/f'{i:02}.png')
    for src,name in [(SHARED/'thoma/idle/01.png','idle-01.png'),(SHARED/'manifest.json','manifest.json'),(SHARED/'frame-audit.json','frame-audit.json')]:shutil.copyfile(src,base/name)
    shutil.copyfile(SHARED/'thoma-weapon-style-check.png',OUT/'style-check-a8.png')
    write(base/'hashes.json',[{'path':rel(p),'sha256':sha(p)} for p in sorted(base.iterdir())])
    baseline=load(A8/'checklist.json')['frames'];landmarks=load(A8/'landmark-deltas.json')
    spec=load(SHARED/'thoma-appearance-spec.json')
    frames={}
    for f in ['00','01','02','03','04']:
        path=f'thoma/swing/{f}.png';target=spec['pose_targets'][f]['landmarks']
        # Detailed submasks are further intersected with these W1 permission masks.
        regions={'head':[HEAD_POLYS[f]],'stole':PANELS[f],
          'embroidery':[rect(130,290,350,403)],'tassels':[rect(130,340,350,415)],
          'mace':[rect(96,60,299,140) if f=='00' else rect(170,57,309,120) if f=='01' else rect(352,85,480,188) if f=='02' else rect(350,168,480,221) if f=='03' else rect(349,301,447,401)],
          'legs_feet':[rect(28,385,395,468)]}
        records={}
        for name,polys in regions.items():
            p=OUT/f'masks/{f}/{name}.png';p.parent.mkdir(parents=True,exist_ok=True)
            m=mask(polys);m.save(p)
            records[name]={'path':rel(p),'sha256':sha(p),'polygons':polys,'bbox':m.getbbox()}
        frames[f]={'frame':path,'a8_sha256':sha(base/f'{f}.png'),'a8_checklist':baseline[path]['region_review'],
          'a8_landmarks':landmarks['per_frame'][path],'targets':target,'masks':records,
          'measured_a8_head_box':HEAD_BOXES[f],'stance_width_target':abs(target['foot_right'][0]-target['foot_left'][0]),
          'target_head_size':[60,70],'target_head_centre':target['head_centre'],
          'pose_repair':'narrow left stance 59 ->120, right319 ->354' if f=='03' else 'front foot351 ->334, rear93,464 ->165,455' if f=='04' else 'replace compressed mace with rigid canon donor' if f in ['00','01'] else 'identity/terminal cloth only'}
    anchors={}
    for name,path,shift in [('idle-01','thoma/idle/01.png',(0,0)),('swing-05','thoma/swing/05.png',(-5,-10))]:
        polys={'head':[ANCHOR_HEAD], 'stole':[[(191,155),(210,158),(247,242),(254,382),(220,384),(220,265)],[(277,157),(290,160),(312,354),(287,363)]],
          'embroidery':[rect(222,337,253,373),rect(285,300,309,350)],'tassels':[rect(220,369,255,386),rect(285,346,313,366)],
          'mace':[ANCHOR_MACE],'legs_feet':[rect(179,389,333,465)]}
        regions={}
        for region,p in polys.items():
            adjusted=[[(x+shift[0],y+shift[1]) for x,y in poly] for poly in p]
            # Recover weapon/boots are separately picked (not head shift).
            if name=='swing-05' and region=='mace':adjusted=[ANCHOR_MACE]
            if name=='swing-05' and region=='legs_feet':adjusted=[rect(178,394,332,465)]
            mp=OUT/f'masks/{name}/{region}.png';mp.parent.mkdir(parents=True,exist_ok=True)
            mask(adjusted).save(mp);regions[region]={'path':rel(mp),'sha256':sha(mp),'polygons':adjusted}
        anchors[name]={'path':rel(SHARED/path),'sha256':sha(SHARED/path),'regions':regions}
    measurements={'head':{'idle_centre':[256,138],'width_height':[60,70],'hair_bbox':[227,103,285,149],'brow_extents':[[258,132],[281,136]],'beard_bbox':[249,151,281,174],'uncertainty_px':2},
       'stole':spec['costume']['stole'],'embroidery':spec['costume']['embroidery'],'tassels':spec['costume']['tassels'],
       'mace':spec['mace'],'feet':spec['costume']['shoes']}
    # Preserve anchor observations verbatim. Pose targets and hand-measured boxes
    # are explicitly distinct from exact donor pixels and testable alpha scans.
    data={'base_commit':'dcc949c','start_commit':'8b6d957','order':ORDER,'checks':CHECKS,'anchors':anchors,'frames':frames,
      'anchor_measurements':measurements,'limits':'Manual visible landmarks +/-2px, hidden joints +/-12px. Masks are permission ceilings, not anatomical acceptance. Exact anchor pixels take precedence. No Owner art approval.',
      'protected_a8_pass_items':[n for n in CHECKS if baseline['thoma/swing/03.png']['region_review'][n].startswith('PASS')]}
    write(OUT/'defects-and-targets.json',data)
    lines=['# A9 defects, recorded masks and measured targets','','A8 baseline is byte-archived; anchors are immutable. Fix order: 03,02,04,00,01.','',
      'Anchor head centre (256,138), about60x70px, hair bbox(227,103)-(285,149), brow(258,132)-(281,136), squared beard(249,151)-(281,174). Visible manual uncertainty +/-2px; hidden joints +/-12px.',
      'Stole widths L24-30 / R12-22px; two sprigs at L(230,340)-(248,371), R(291,302)-(306,345). Fringes10/8 +/-1; one cord. Canon head37x36px, exposed haft39px, grip-to-head~55px (recover~52.5); collar7px.',
      'Full per-height panel edges, target joints, foot stance widths, donor regions and SHA-256 are in defects-and-targets.json. RGB/alpha donors are exact; manual picks are estimates.','']
    for f,r in frames.items():
        lines += [f'## swing/{f}',f"Head {r['target_head_centre']}; feet {r['targets']['foot_left']} / {r['targets']['foot_right']}; stance {r['stance_width_target']}px; mace {r['targets']['mace_head']}.",f"Pose repair: {r['pose_repair']}.",'','| Item | A8 regression baseline |','| --- | --- |']
        lines += [f'| {n} | {r["a8_checklist"][n]} |' for n in CHECKS]
        lines += ['','Masks: '+', '.join(f'[{n}](masks/{f}/{n}.png)' for n in REGIONS), '']
    (OUT/'defects-and-targets.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('A9_W1 baseline5+anchors archived,48 region masks, all13 baseline items/frame recorded')

if __name__=='__main__':main()
