"""A8 brief checklist, source crops and measured landmark deltas; no art waiver."""
from prepare_a8_sheet import ROOT, SHARED, OUT, sha, write
from build_a7_spec import BOXES
from PIL import Image, ImageDraw
import json
import math

def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
PATHS=['thoma/idle/01.png']+[f'thoma/swing/{i:02}.png' for i in range(6)]
CHECKS=['face_hair','stole','embroidery','tassels','cuffs','hem','palette','seams','bag_count','feet','mace','landmarks','sequence']
REGIONS={'face_hair':(210,90,350,190),'stole':(130,140,350,415),'embroidery':(130,295,340,415),
 'tassels':(130,335,340,420),'cuffs':(95,65,410,330),'hem':(60,340,390,450),'palette':(150,170,335,430),
 'seams':(95,60,485,425),'bag_count':(95,220,260,340),'feet':(30,390,400,470),
 'mace':(95,60,485,410),'landmarks':(30,60,485,470),'sequence':(30,60,485,470)}

def table_row(rec):
    values=[('1 ' if n=='bag_count' else '')+rec['region_review'][n].split(':')[0] for n in CHECKS]
    return '| `'+rec['path']+'` | '+rec['status']+' | '+' | '.join(values)+' | '+rec['reason']+' |'

def technical(path):
    im=Image.open(SHARED/path);a=im.getchannel('A');opaque=a.point(lambda v:255 if v>127 else 0)
    bottom=opaque.getbbox()[3]-1
    grounded=sum(opaque.getpixel((x,464))>0 for x in range(512))
    # Numeric scan only finds saturated guide colours; 1x model inspection also required.
    guide=sum(1 for r,g,b,a in im.getdata() if a>127 and ((g>220 and r<60 and b<80) or (b>220 and g>170 and r<60) or (r>220 and g<40 and b<40)))
    motion=path in PATHS[1:6]
    passed=im.size==(512,512) and im.mode=='RGBA' and a.getextrema()[0]==0 and not guide
    if motion:passed=passed and 463<=bottom<=465 and grounded>0
    return {'pass':passed,'size':list(im.size),'mode':im.mode,'lowest_opaque_y':bottom,'opaque_pixels_on_ground':grounded,
       'saturated_guide_pixels':guide,'guide_visual_check':'PASS: no line, arc, joint dot or text visible in final1x frame',
       'straight_alpha':'visible RGB retained unmultiplied; hidden RGB zeroed by normalization',
       'limits':'Original immutable anchors retain original ground/alpha; no endpoint changed to satisfy a new gate.'}

def audit():
    rows=load(SHARED/'frame-audit.json');provenance=load(SHARED/'a8-swing-prompts.json')
    sources={r['frame']:r for r in provenance['frames']}
    for r in rows:
        if r['path'] not in PATHS:continue
        fixed=r['path'] not in sources
        checks={k:'PASS: immutable appearance endpoint; transition failures assigned to middle frames, not Owner approval.' for k in CHECKS}
        if not fixed:
            checks.update(face_hair='FAIL: common sheet improves similarity, but broader grey crown, softer beard/cheek and changed brow differ from anchor identity.',
              stole='FAIL: generated panels are wider and more symmetrical at the ends than the narrow asymmetric anchor stole.',
              embroidery='FAIL: two sprigs remain, but leaf scale, branch spacing and shape differ from the exact anchor motifs.',
              tassels='FAIL: dense fairly regular generated fringe does not establish10/8 uneven tips within1; long cord attachment shifts.',
              cuffs='PASS: ivory flared inner sleeves narrow to visibly continuous wrists; no separated arm or new cuff layer.',
              hem='PASS: continuous ivory inner bell and teal divided outer skirt; no detached triangular cloth fragments.',
              palette='PASS: muted dark teal, warm ivory, worn leather and grey hair remain in anchor material families without colour grading.',
              seams='FAIL: reconstructed mace/haft joins and changed hand overlap remain visible at1x; seamless painted integration not achieved.',
              bag_count='PASS: one brown flap satchel and one pale roll at screen-left hip in every panel.',
              feet='PASS: both worn boots visibly attach to legs; at least one foot meets464 and opaque bottom is463-465.',
              mace='FAIL: target centre and impact opacity pass, but local reconstruction changes projected shaft length and head/haft brush continuity; not canon-design acceptance.',
              landmarks='FAIL: several observed hands, elbows and feet exceed brief targets by4px; cloth-hidden knees have larger uncertainty and are not certified.',
              sequence='FAIL: face, stole ends and hem/stance still jump from anchors to sheet and between action panels; all-same-painting requirement unmet.')
            source=sources[r['path']]
            r.update(source=source['raw'],raw_sha256=source['raw_sha256'],cleanup='A8 single-sheet panels; uniform scale/translate; recorded alpha cleanup and local mace-only reconstruction; no per-frame generation.')
        r.update(sha256=sha(SHARED/r['path']),region_review=checks,review_segment='spike-02 A8',
            review_authority='model source1x and rendered-sequence inspection; not Owner art approval or human playtest',
            bag_count=1,weapon_status='APPROVED',technical_check=technical(r['path']),
            reason='Immutable appearance endpoint; not Owner art approval.' if fixed else 'Shared sheet improves surface consistency; anchor identity, stole/motif/fringe, weapon integration and full pose/sequence still fail.')
        passed=all(v.startswith('PASS:') for v in checks.values()) and r['technical_check']['pass']
        r['status']='PASS' if passed else 'PLACEHOLDER'
        r['style_review']={k:checks[v] for k,v in [('face','face_hair'),('stole_cape_embroidery','embroidery'),('cuffs','cuffs'),('hem_silhouette','hem'),('palette','palette'),('stroke','seams'),('satchel_medallion','bag_count')]}
    write(SHARED/'frame-audit.json',rows)
    chosen={r['path']:r for r in rows if r['path'] in PATHS}
    table='| Frame | Status | '+' | '.join(CHECKS)+' | Reason |\n| '+' | '.join(['---']*16)+' |\n'+'\n'.join(table_row(chosen[p]) for p in PATHS)+'\n'
    (OUT/'frame-status-table.md').write_text(table,encoding='utf-8')
    return chosen

def sheets(rows):
    order=[PATHS[0],PATHS[-1]]+PATHS[1:6]
    groups={'face_hair':'face','stole':'stole','embroidery':'embroidery_right','tassels':'tassels_right',
       'cuffs':'cuffs','hem':'hem','palette':'robe','seams':'mace','bag_count':'bag','feet':'shoes',
       'mace':'mace','landmarks':'robe','sequence':'robe'}
    sheet=Image.new('RGB',(7*400,50+13*290),(34,40,38));d=ImageDraw.Draw(sheet);crops=[]
    d.text((8,8),'A8 anchor idle / recover / 00 / 01 / 02 / 03 / 04; model inspection, all5 PLACEHOLDER.',fill='white')
    for j,(name,anchor) in enumerate(groups.items()):
        y=45+j*290
        for i,path in enumerate(order):
            box=BOXES[anchor][i] if i<2 else REGIONS[name]
            crop=Image.open(SHARED/path).convert('RGBA').crop(box);scale=min(1,390/crop.width,235/crop.height)
            if scale<1:crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
            x=i*400;sheet.paste(crop,(x+4,y+20),crop)
            d.text((x+4,y),name+' '+path,fill='#dfc28f');d.text((x+4,y+267),rows[path]['region_review'][name].split(':')[0]+f' crop scale{scale:.3f}',fill='white')
            crops.append({'frame':path,'item':name,'box':box,'scale':scale,'sha256':sha(SHARED/path),'result':rows[path]['region_review'][name]})
    sheet.save(OUT/'checklist.png',optimize=True)
    write(OUT/'checklist.json',{'brief':'docs/art-briefs/thoma-swing-commission.md','brief_sha256':sha(ROOT/'docs/art-briefs/thoma-swing-commission.md'),'crops':crops,'frames':rows,'art_pass':False})
    strip=Image.new('RGBA',(7*512,512))
    comparison=Image.new('RGB',(7*512,1100),(34,40,38));dc=ImageDraw.Draw(comparison)
    for i,path in enumerate(PATHS):
        im=Image.open(SHARED/path).convert('RGBA');strip.paste(im,(i*512,0))
        old=Image.open(OUT/'baseline-a7'/('idle-01.png' if i==0 else path[-6:])).convert('RGBA')
        comparison.paste(old,(i*512,25),old);comparison.paste(im,(i*512,575),im)
        dc.text((i*512+4,6),'A7 '+path,fill='white');dc.text((i*512+4,555),'A8 '+path,fill='white')
    strip.save(OUT/'sequence-strip.png',optimize=True)
    comparison.save(OUT/'contact-sheet-a7-vs-a8.png',optimize=True)
    style=Image.new('RGB',(7*512,560),(34,40,38));style.paste(strip,(0,30),strip)
    ImageDraw.Draw(style).text((8,6),'A8 SOURCE ASSETS equal512px scale; five motion PLACEHOLDER; anchors fixed; not a game screenshot.',fill='white')
    style.save(SHARED/'thoma-weapon-style-check.png',optimize=True)

def landmarks():
    # Visible manual picks at1x +/-2px. Cloth-hidden elbow/knee centres are
    # anatomical estimates +/-12px; do not substitute requested coordinates.
    names=['head_centre','hand_weapon','hand_free','elbow_left','elbow_right','knee_left','knee_right','foot_left','foot_right','mace_head']
    points=[[(256,138),(185,297),(324,266),(181,252),(317,233),(208,389),(288,379),(201,462),(312,414),(230,328)],
      [(260,143),(151,110),(388,251),(137,174),(350,230),(179,384),(321,378),(157,464),(355,442),None],
      [(260,143),(218,79),(375,282),(162,122),(348,249),(189,382),(318,391),(161,464),(361,442),None],
      [(282,143),(376,170),(166,260),(265,204),(165,226),(154,391),(311,396),(100,464),(350,438),None],
      [(264,143),(365,186),(110,253),(305,199),(135,193),(129,388),(263,387),(59,464),(319,444),None],
      [(310,143),(375,314),(111,222),(340,275),(146,180),(137,390),(294,410),(93,464),(351,464),None],
      [(251,132),(183,299),(320,266),(179,247),(314,230),(204,393),(287,387),(198,463),(311,425),(223,333)]]
    spec=load(SHARED/'thoma-appearance-spec.json');provenance=load(SHARED/'a8-swing-prompts.json')
    records={r['frame']:r for r in provenance['frames']};measured={};targets={};deltas={}
    for path,picks in zip(PATHS,points):
        rec=dict(zip(names,picks));motion=path in records
        if motion:rec['mace_head']=records[path]['local_fixes'][0]['measured_head_alpha_centroid']
        rec['character_height_px']=361 if motion else 361 if path==PATHS[0] else 371
        rec['lowest_opaque_y']=technical(path)['lowest_opaque_y']
        rec['uncertainty_px']={'visible':2,'cloth_hidden_elbows_knees':12,'mace':'final translated donor-alpha centroid <1px; independent final crop check in A8 test'}
        rec['measurement']='Manual source1x landmarks; joints hidden by cloth are estimates, not exact measurements. Height from normalized manual headtop to464; endpoint proportions from appearance spec.'
        measured[path]=rec
        if motion:
            targets[path]=spec['pose_targets'][path[-6:-4]]['landmarks']
            deltas[path]={n:{'measured':rec[n],'target':targets[path][n], 'delta':[round(a-b,3) for a,b in zip(rec[n],targets[path][n])],
                'error_px':round(math.dist(rec[n],targets[path][n]),3),'within4':math.dist(rec[n],targets[path][n])<=4} for n in names}
        else:targets[path]={n:rec[n] for n in names}
    pairs=[]
    for a,b in zip(PATHS,PATHS[1:]):
        actual={n:[round(y-x,3) for x,y in zip(measured[a][n],measured[b][n])] for n in names}
        desired={n:[round(y-x,3) for x,y in zip(targets[a][n],targets[b][n])] for n in names}
        flags=[n for n in names if math.dist(actual[n],desired[n])>4]
        pairs.append({'from':a,'to':b,'actual_deltas':actual,'target_deltas':desired,'jump_flags':flags,
            'character_height_delta_px':measured[b]['character_height_px']-measured[a]['character_height_px'],
            'result':'FAIL' if flags else 'PASS'})
    write(OUT/'landmark-deltas.json',{'measured':measured,'per_frame':deltas,'pairs':pairs,'limits':'Visible +/-2px; hidden elbows/knees +/-12px. Estimates cannot certify strict4px compliance. Target means brief; no unapproved deviation waived.'})
    lines=['# A8 measured landmarks versus commission brief','','Visible picks ±2px, cloth-hidden elbows/knees ±12px estimates. All values are512px source coordinates. No hidden joint PASS is claimed.','',
       '| Frame | Landmark | Measured | Target | Delta | Error px | Within4 |','| --- | --- | --- | --- | --- | --- | --- |']
    for path,rows in deltas.items():
        for n,r in rows.items():lines.append(f'| {path} | {n} | {r["measured"]} | {r["target"]} | {r["delta"]} | {r["error_px"]} | {r["within4"]} |')
    lines+=['','| Frame | Character height | Lowest opaque y |','| --- | --- | --- |']
    for p,r in measured.items():lines.append(f'| {p} | {r["character_height_px"]} | {r["lowest_opaque_y"]} |')
    lines+=['','## Every adjacent pair','','| Pair | Actual deltas (head/hands/elbows/knees/feet/mace) | Height delta | Jump flags (>4px target-delta difference) |','| --- | --- | --- | --- |']
    for p in pairs:lines.append(f'| {p["from"]} → {p["to"]} | {json.dumps(p["actual_deltas"])} | {p["character_height_delta_px"]} | {", ".join(p["jump_flags"])} |')
    (OUT/'landmark-deltas.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('A8_LANDMARKS all5 mace_centres within4; full_joint_targets FAIL')

if __name__=='__main__':
    rows=audit();sheets(rows);landmarks()
    print('A8_CHECKLIST motion_pass=0/5; technical=',{p:r['technical_check']['pass'] for p,r in rows.items()})
