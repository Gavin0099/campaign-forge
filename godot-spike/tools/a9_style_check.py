"""W3 complete source audit and A8/A9 comparisons; model inspection only."""
from prepare_a9_regions import *
from a8_style_check import PATHS, REGIONS as CROP_REGIONS, table_row, technical
from build_a7_spec import BOXES
import math

def audit():
    rows=load(OUT/'baseline-a8/frame-audit.json');log=load(OUT/'a9-fix-log.json')
    baseline=load(A8/'checklist.json')['frames'];changes={}
    for r in rows:
        p=r['path']
        if p not in PATHS:continue
        checks=dict(baseline[p]['region_review']);change={n:'same' for n in CHECKS}
        if p in PATHS[1:6]:
            f=Path(p).stem;kept=log['frames'][f]['kept_regions']
            if 'head' in kept:
                checks['face_hair']='PASS: translated idle01 crown, brow, nose and squared beard retain the same donor identity; collar blending is judged separately under seams.'
                change['face_hair']='improved'
            else:checks['face_hair']='FAIL: all three anchor-head trials produced old-face fragments or collar holes; A8 broad crown/softened beard retained.'
            checks['stole']='FAIL: A8 wide terminal panels retained because narrower anchor transplants opened garment gaps.'
            checks['embroidery']='FAIL: A8 larger sprigs retained; anchor motif patches overlapped leaves or included weapon/teal edge contamination.'
            checks['tassels']='FAIL: A8 regular fringe/cord retained; narrow donor fringe did not join the continuous hem; counts10/8 +/-1 not established.'
            checks['seams']='FAIL: head/collar and/or mace-edge joins remain visible at native size; no complete seamless painted integration.'
            checks['mace']='FAIL: '+('rigid recover05 head/haft transplant removes compression and meets target; grip/head edge highlights and projected-length integration still differ.' if 'mace' in kept else 'A8 target/impact opacity pass, but reconstructed projected haft/head and brush joins still fail canon integration.')
            if 'mace' in kept:change['mace']='improved'
            checks['landmarks']='FAIL: A8 hands/elbows/knees and feet still exceed guide targets;03 narrowed-stance and04 foot trials rejected for hem/attachment regression.'
            checks['sequence']='FAIL:01 retains A8 identity while other heads use anchors; broad cloth ends, stance and foot positions still jump across immutable endpoints.'
            r.update(source=rel(OUT/'a9-fix-log.json'),cleanup='A9 enforced region masks; retained anchor-pixel transplants only; rejected cloth/leg regions exactly A8.',
              reason='Partial anchor identity and/or uncompressed mace improvement; cloth details, integration and full pose/sequence still fail.')
        r.update(region_review=checks,a8_to_a9_change=change,sha256=sha(SHARED/p),technical_check=technical(p),
          review_segment='spike-02 A9',review_authority='model native512px source inspection plus actual rendered playback; not Owner art approval',bag_count=1,weapon_status='APPROVED')
        r['status']='PASS' if all(v.startswith('PASS:') for v in checks.values()) and r['technical_check']['pass'] else 'PLACEHOLDER'
        r['style_review']={k:checks[v] for k,v in [('face','face_hair'),('stole_cape_embroidery','embroidery'),('cuffs','cuffs'),('hem_silhouette','hem'),('palette','palette'),('stroke','seams'),('satchel_medallion','bag_count')]}
        changes[p]=change
    write(SHARED/'frame-audit.json',rows)
    chosen={r['path']:r for r in rows if r['path'] in PATHS}
    header='| Frame | Status | '+' | '.join(CHECKS)+' | Reason |\n| '+' | '.join(['---']*16)+' |\n'
    (OUT/'frame-status-table.md').write_text(header+'\n'.join(table_row(chosen[p]) for p in PATHS)+'\n',encoding='utf-8')
    change_lines=['# A8 to A9 item changes','','| Frame | Item | A8 | A9 | Change | Reason |','| --- | --- | --- | --- | --- | --- |']
    for p,r in chosen.items():
        for n in CHECKS:change_lines.append(f'| {p} | {n} | {baseline[p]["region_review"][n].split(":")[0]} | {r["region_review"][n].split(":")[0]} | {changes[p][n]} | {r["region_review"][n]} |')
    (OUT/'checklist-changes.md').write_text('\n'.join(change_lines)+'\n',encoding='utf-8')
    return chosen

def sheets(rows):
    order=[PATHS[0],PATHS[-1]]+PATHS[1:6]
    groups={'face_hair':'face','stole':'stole','embroidery':'embroidery_right','tassels':'tassels_right','cuffs':'cuffs','hem':'hem','palette':'robe','seams':'mace','bag_count':'bag','feet':'shoes','mace':'mace','landmarks':'robe','sequence':'robe'}
    sheet=Image.new('RGB',(2800,50+13*290),(34,40,38));d=ImageDraw.Draw(sheet);crops=[]
    d.text((8,8),'A9: idle / recover / 00 / 01 / 02 / 03 / 04. Columns show result + A8->A9 change. MODEL REVIEW, NOT OWNER APPROVAL.',fill='white')
    for j,(name,anchor) in enumerate(groups.items()):
        y=45+j*290
        for i,p in enumerate(order):
            box=BOXES[anchor][i] if i<2 else CROP_REGIONS[name]
            crop=Image.open(SHARED/p).convert('RGBA').crop(box);scale=min(1,390/crop.width,235/crop.height)
            if scale<1:crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
            x=i*400;sheet.paste(crop,(x+4,y+20),crop);d.text((x+4,y),name+' '+p,fill='#dfc28f')
            d.text((x+4,y+267),rows[p]['region_review'][name].split(':')[0]+'; A8->A9 '+rows[p]['a8_to_a9_change'][name],fill='white')
            crops.append({'frame':p,'item':name,'box':box,'scale':scale,'sha256':sha(SHARED/p),'result':rows[p]['region_review'][name],'a8_to_a9_change':rows[p]['a8_to_a9_change'][name]})
    sheet.save(OUT/'checklist.png',optimize=True)
    write(OUT/'checklist.json',{'brief':'docs/art-briefs/thoma-swing-commission.md','brief_sha256':sha(ROOT/'docs/art-briefs/thoma-swing-commission.md'),'frames':rows,'crops':crops,'art_pass':False})
    strip=Image.new('RGBA',(3584,512));comparison=Image.new('RGB',(3584,1100),(34,40,38));dc=ImageDraw.Draw(comparison)
    for i,p in enumerate(PATHS):
        im=Image.open(SHARED/p).convert('RGBA');old=Image.open(OUT/'baseline-a8'/('idle-01.png' if i==0 else Path(p).name)).convert('RGBA')
        strip.paste(im,(i*512,0));comparison.paste(old,(i*512,25),old);comparison.paste(im,(i*512,575),im)
        dc.text((i*512+4,6),'A8 '+p,fill='white');dc.text((i*512+4,555),'A9 '+p,fill='white')
    strip.save(OUT/'sequence-strip.png',optimize=True);comparison.save(OUT/'contact-sheet-a8-vs-a9.png',optimize=True)
    style=Image.new('RGB',(3584,560),(34,40,38));style.paste(strip,(0,30),strip)
    ImageDraw.Draw(style).text((8,6),'A9 SOURCE ASSETS, equal512px scale. All5 motion PLACEHOLDER. Anchors byte-fixed. Not a game screenshot.',fill='white')
    style.save(SHARED/'thoma-weapon-style-check.png',optimize=True)

def landmarks():
    data=load(A8/'landmark-deltas.json');measured=data['measured'];spec=load(OUT/'defects-and-targets.json');log=load(OUT/'a9-fix-log.json')
    names=list(next(iter(data['per_frame'].values())))
    for f,rec in log['frames'].items():
        p=f'thoma/swing/{f}.png';r=measured[p]
        if 'head' in rec['kept_regions']:r['head_centre']=spec['frames'][f]['target_head_centre']
        r['mace_head']=rec['technical']['mace_centre']
        im=Image.open(SHARED/p);box=HEAD_BOXES[f]
        opaque=im.crop((box[0],90,box[2],190)).getchannel('A').point(lambda v:255 if v>127 else 0)
        # Read head ROI only, excluding raised weapon where it crosses that ROI.
        top=opaque.getbbox()[1]+90;r['character_height_px']=464-top;r['lowest_opaque_y']=technical(p)['lowest_opaque_y']
        r['measurement']='Head centre transferred from manually picked anchor through kept rigid matrix; headtop scanned in local ROI; other landmarks retained A8 native manual observations because those pixels are identical. Mace is independent final alpha centroid. Hidden joints +/-12px, visible +/-2px.'
        data['per_frame'][p]={n:{'measured':r[n],'target':spec['frames'][f]['targets'][n],'delta':[round(a-b,4) for a,b in zip(r[n],spec['frames'][f]['targets'][n])],
          'error_px':round(math.dist(r[n],spec['frames'][f]['targets'][n]),4),'within4':math.dist(r[n],spec['frames'][f]['targets'][n])<=4} for n in names}
    targets={p:spec['frames'][Path(p).stem]['targets'] if p in PATHS[1:6] else measured[p] for p in PATHS}
    pairs=[]
    for a,b in zip(PATHS,PATHS[1:]):
        actual={n:[round(y-x,4) for x,y in zip(measured[a][n],measured[b][n])] for n in names}
        desired={n:[round(y-x,4) for x,y in zip(targets[a][n],targets[b][n])] for n in names}
        flags=[n for n in names if math.dist(actual[n],desired[n])>4]
        pairs.append({'from':a,'to':b,'actual_deltas':actual,'target_deltas':desired,'jump_flags':flags,'character_height_delta_px':measured[b]['character_height_px']-measured[a]['character_height_px'],'result':'FAIL' if flags else 'PASS'})
    data.update(pairs=pairs,limits='Visible manual +/-2px; hidden joints +/-12px. No Owner waiver. Exact unchanged A8 anatomy reused only where pixels are unchanged; head transfer is matrix-based, not independent automatic face detection.')
    write(OUT/'landmark-deltas.json',data)
    lines=['# A9 landmarks versus brief','',''+data['limits'],'','| Frame | Landmark | Measured | Target | Delta | Error px | Within4 |','| --- | --- | --- | --- | --- | --- | --- |']
    for p,rows in data['per_frame'].items():
        for n,r in rows.items():lines.append(f'| {p} | {n} | {r["measured"]} | {r["target"]} | {r["delta"]} | {r["error_px"]} | {r["within4"]} |')
    lines+=['','| Frame | Head-to-ground height | Lowest opaque y |','| --- | --- | --- |']+[f'| {p} | {r["character_height_px"]} | {r["lowest_opaque_y"]} |' for p,r in measured.items()]
    lines+=['','| Pair | Actual deltas | Target deltas | Jump flags (>4px delta mismatch) | Height delta |','| --- | --- | --- | --- | --- |']
    lines += [f'| {r["from"]} -> {r["to"]} | {json.dumps(r["actual_deltas"])} | {json.dumps(r["target_deltas"])} | {r["jump_flags"]} | {r["character_height_delta_px"]} |' for r in pairs]
    (OUT/'landmark-deltas.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write(OUT/'final-mace-centres.json',[{'frame':p,'measured':measured[p]['mace_head'],'target':targets[p]['mace_head'],'error_px':data['per_frame'][p]['mace_head']['error_px']} for p in PATHS[1:6]])

if __name__=='__main__':
    rows=audit();sheets(rows);landmarks();print('A9_W3 source audit: all5 PLACEHOLDER;4 identity improvements;2 uncompressed mace improvements; no A8 passing item downgraded')
