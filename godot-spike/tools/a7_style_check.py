"""Source-pixel spec audit; measured proxies do not approve art."""
from build_a7_spec import *
from prepare_a7_frames import BASE, ORDER
from PIL import ImageChops, ImageStat

PATHS=['thoma/idle/01.png']+[f'thoma/swing/{i:02}.png' for i in range(6)]
CHECKS=['face_hair','stole','embroidery','tassels','cuffs','hem','palette','seams','bag_count','feet','mace','landmarks','sequence']
REGIONS={'face_hair':(210,90,350,207),'stole':(180,140,330,400),'embroidery':(190,295,325,395),
 'tassels':(190,335,325,400),'cuffs':(100,110,410,310),'hem':(100,345,400,445),
 'palette':(165,165,335,430),'seams':(180,140,350,400),'bag_count':(160,230,255,335),
 'feet':(100,390,400,470),'mace':(95,65,480,402),'landmarks':(95,65,480,470),'sequence':(95,65,480,470)}

def row(record):
    values=[(('1 ' if name=='bag_count' else '')+record['region_review'][name].split(':')[0]) for name in CHECKS]
    return '| `'+record['path']+'` | '+record['status']+' | '+' | '.join(values)+' | '+record['reason']+' |'

def audit():
    rows=load(SHARED/'frame-audit.json');records={r['frame']:r for r in load(SHARED/'a7-swing-prompts.json') if r['adopted']}
    for r in rows:
      if r['path'] not in PATHS:continue
      fixed=r['path'] not in records
      checks={k:'PASS: byte-identical anchor endpoint, appearance source; transition failures assigned to motion frames.' for k in CHECKS}
      if not fixed:
        checks.update(face_hair='FAIL: copied anchor interior improves features, but A6 outer hair/cheek silhouette and clipped edge remain; full anchor identity not reproduced.',
          stole='FAIL: A6 panel widths/fall remain; small texture patches cannot establish anchor drape through the pose.',
          embroidery='FAIL: visible source sprig pixels transferred, but partial occlusion, alignment and residual A6 strokes do not establish the exact two motifs.',
          tassels='FAIL: source fringe interior does not replace every A6 panel-edge tip; attachment/edge count still varies.',
          cuffs='FAIL: retained A6 fold/edge shape differs from anchors; coherent structure alone does not meet exact appearance spec.',
          hem='FAIL: A6 silhouette is continuous, but width and inner pleats still pop relative to fixed endpoints.',
          palette='PASS: only original A6 and anchor colours, no new grading; masked blends remain in original muted teal/ivory/leather families.',
          seams='FAIL: local face/stole texture transitions remain visible at 1x; seam-free anchor transfer is not achieved.',
          bag_count='PASS: exactly one unchanged A6 satchel with one cloth roll; no bag-bearing patch used.',
          feet='PASS: both connected A6 boots and lower leg pixels unchanged; no detached shoe or cropped ground.',
          mace='PASS: A6 mace/haft/collar/grip source pixels retained; 04 moves the connected hand/weapon19px without rescaling.',
          landmarks='FAIL: target vs actual full joint/hand/face positions exceed4px on multiple landmarks; exact contact03 and head arc alone do not pass all joints.',
          sequence='FAIL: face silhouette, panel/hem outline and motif/fringe changes remain through consecutive actual rendered poses.')
        if r['path'].endswith('02.png'):
          checks['embroidery']='FAIL: right donor is visibly misregistered and leaves a residual A6 sprig alongside the transferred patch; exact motif count/placement fails.'
        if r['path'].endswith('04.png'):
          checks['cuffs']='FAIL: local cloth bridge above lowered hand is visible; smooth arm/cuff continuity not achieved.'
          checks['seams']='FAIL: rectangular-looking cloth bridge and local stole texture joins remain; this is a regression from A6 seamless whole painting.'
        source=records[r['path']]
        r.update(source=source['raw'],raw_sha256=source['raw_sha256'],cleanup='A6 structural base + recorded masked anchor interior transfers; 04 connected weapon translation19px; raw generated full frames not adopted.')
      reason='Immutable reference endpoint, not Owner art approval.' if fixed else 'Anchor interior details corrected; outer face, drape, fringe and local seams remain unacceptable; full art acceptance FAIL.'
      r.update(sha256=sha(SHARED/r['path']),status='PASS' if fixed else 'PLACEHOLDER',region_review=checks,review_segment='spike-02 A7',
        review_authority='model inspection; not Owner approval or human playtest',bag_count=1,reason=reason)
      r['style_review']={k:checks[v] for k,v in [('face','face_hair'),('stole_cape_embroidery','embroidery'),('cuffs','cuffs'),('hem_silhouette','hem'),('palette','palette'),('stroke','seams'),('satchel_medallion','bag_count')]}
    write(SHARED/'frame-audit.json',rows)
    table='| Frame | Status | '+' | '.join(CHECKS)+' | Reason |\n| '+' | '.join(['---']*(len(CHECKS)+3))+' |\n'
    table+='\n'.join(row(r) for r in rows if r['path'] in PATHS)+'\n'
    (OUT/'frame-status-table.md').write_text(table,encoding='utf-8',newline='\n')
    return {r['path']:r for r in rows if r['path'] in PATHS}

def sheets(rows):
    # Every appearance item gets matching anchor crops; scaled previews are
    # explicitly labelled and native-pixel crops are retained in the sheet.
    groups={'face_hair':'face','stole':'stole','embroidery':'embroidery_right','tassels':'tassels_right',
      'cuffs':'cuffs','hem':'hem','bag_count':'bag','feet':'shoes','mace':'mace','palette':'robe',
      'seams':'outline','landmarks':'face','sequence':'robe','robe':'robe','belt':'belt',
      'hair':'hair','embroidery_left':'embroidery_left','tassels_left':'tassels_left','body_proportions':'robe'}
    # Full motion ROIs avoid pretending an unregistered crop is an exact match.
    sheet=Image.new('RGB',(7*400,60+len(groups)*290),(34,40,38));d=ImageDraw.Draw(sheet)
    crops=[]
    ordered=[PATHS[0],PATHS[-1]]+PATHS[1:6]
    for j,(name,anchor_name) in enumerate(groups.items()):
      y=45+j*290
      for i,path in enumerate(ordered):
        box=BOXES[anchor_name][0 if i==0 else 1] if i<2 else REGIONS.get(name,REGIONS['stole'])
        # Larger whole-weapon boxes use labelled 0.65x previews, all other source crops are1x.
        im=Image.open(SHARED/path).convert('RGBA');crop=im.crop(box);scale=1
        if crop.width>390 or crop.height>245:
          scale=min(390/crop.width,245/crop.height);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
        x=i*400;d.text((x+5,y),name+' / '+path,fill='#dfc28f');sheet.paste(crop,(x+4,y+20),crop)
        check={'hair':'face_hair','robe':'stole','belt':'bag_count','body_proportions':'landmarks','embroidery_left':'embroidery','tassels_left':'tassels'}.get(name,name)
        result=rows[path]['region_review'][check].split(':')[0]
        d.text((x+5,y+268),f'{result} source crop scale={scale:.3f}',fill='white')
        crops.append({'frame':path,'item':name,'box':box,'scale':scale,'result':result,'source_sha256':sha(SHARED/path),
           'reason':rows[path]['region_review'][check]})
    d.text((8,6),'A7 spec compliance: anchor idle / recover /00 /01 /02 /03 /04. FAIL retained; model inspection only.',fill='white')
    sheet.save(OUT/'spec-check.png',optimize=True)
    write(OUT/'spec-check.json',{'spec_sha256':sha(SHARED/'thoma-appearance-spec.json'),'crops':crops,'frames':rows,
       'limits':'Source-crop visual evidence, not human/Owner approval. Motion ROIs include changing pose. Raw pixels, not the approximate branch/fringe count, are appearance authority.'})
    strip=Image.new('RGBA',(7*512,560),(0,0,0,0));ds=ImageDraw.Draw(strip)
    for i,path in enumerate(PATHS):
      im=Image.open(SHARED/path).convert('RGBA');strip.alpha_composite(im,(i*512,30));ds.text((i*512+8,8),path,fill='#dfc28f')
    strip.save(OUT/'equal-scale-transparent-sheet.png',optimize=True)
    bg=Image.new('RGB',strip.size,(34,40,38));bg.paste(strip,(0,0),strip)
    bg.save(OUT/'sequence-strip.png',optimize=True);bg.save(SHARED/'thoma-weapon-style-check.png',optimize=True)

def landmarks():
    spec=load(SHARED/'thoma-appearance-spec.json')
    a6=load(ROOT/'godot-spike/docs/evidence/spike02-a6/geometry-check.json')['frames']
    # Manual picks on runtime 1x pixels. Hidden joints are uncertain and never
    # substituted with targets. Primary deltas are visible face/hand/feet/head.
    picks=[([258,142],[185,297],[324,266],[230,328],[201,462],[312,414],361),
      ([260,146],[128,117],[392,250],None,[145,463],[351,433],None),
      ([260,145],[194,109],[287,214],None,[167,463],[335,421],None),
      ([284,147],[372,160],[384,261],None,[135,463],[371,442],None),
      ([266,143],[358,196],[313,272],None,[120,463],[342,446],None),
      ([311,144],[347,325],[136,235],None,[125,456],[334,464],None),
      ([251,132],[183,299],[320,266],[223,333],[198,463],[311,425],371)]
    names=['head_centre','hand_weapon','hand_free','mace_head','foot_left','foot_right','character_height_px']
    measured={}
    for path,values in zip(PATHS,picks):
      v=dict(zip(names,values));motion=path in PATHS[1:6]
      if motion:
        old=a6[path];v['mace_head']=list(old['mapped_landmarks']['mace_head'])
        if path.endswith('04.png'):v['mace_head'][1]+=19
        v['character_height_px']=old['head_to_ground_px']
      v['uncertainty_px']=2;v['measurement']='1x manual source landmarks; weapon centre inherited from A6 verified affine and exact19px translation; height from unchanged A6 silhouette'
      measured[path]=v
    pairs=[]
    for a,b in zip(PATHS,PATHS[1:]):
      rec={'from':a,'to':b,'actual_deltas':{},'target_deltas':{},'target_error_px':{},'jump_flags':[]}
      def target(path):
        return spec['pose_targets'][path[-6:-4]]['landmarks'] if path in PATHS[1:6] else measured[path]
      ta,tb=target(a),target(b)
      for name in names[:-1]:
        da=[round(y-x,4) for x,y in zip(measured[a][name],measured[b][name])]
        dt=[round(y-x,4) for x,y in zip(ta[name],tb[name])]
        err=round(math.dist(da,dt),4);rec['actual_deltas'][name]=da;rec['target_deltas'][name]=dt;rec['target_error_px'][name]=err
        if err>4:rec['jump_flags'].append(name+' delta differs from target >4px')
      rec['character_height_delta_px']=round(measured[b]['character_height_px']-measured[a]['character_height_px'],4)
      if abs(rec['character_height_delta_px'])>10:rec['jump_flags'].append('character height changes >10px')
      rec['result']='FAIL' if rec['jump_flags'] else 'PASS';pairs.append(rec)
    write(OUT/'landmark-deltas.json',{'measured':measured,'pairs':pairs,'limits':'Targets are design targets, not observations. Manual landmarks +/-2px, large occlusion uncertainty on hidden joints. Do not equate a valid weapon arc with full pose compliance.'})
    lines=['# A7 landmark deltas','','Coordinates: source512px, top-left origin. Manual visible landmarks ±2px. Deltas are destination minus origin. Targets are design targets, never measured success.','',
      '| Pair | Face | Weapon hand | Free hand | Mace head | Left foot | Right foot | Height | Target-error flags |',
      '| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in pairs:
      lines.append('| '+r['from'].split('/')[-1]+' → '+r['to'].split('/')[-1]+' | '+' | '.join(str(r['actual_deltas'][n]) for n in names[:-1])+f" | {r['character_height_delta_px']} | "+'; '.join(r['jump_flags'])+' |')
    lines+=['','04 mace head: A6 [420.72,357.384] → A7 [420.72,376.384], target [421,376], error0.475px. The moved head/haft/grip is not rescaled. The cuff bridge still fails appearance/seam acceptance.','',
      'Full per-pair target deltas and errors, and actual visible-point picks, are in landmark-deltas.json. Body joints not visible beneath cloth cannot be measured precisely from pixels; no hidden joint PASS is claimed.']
    (OUT/'landmark-deltas.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    write(OUT/'geometry-check.json',{'canvas':[512,512],'pivot':[256,464],'contact_frame_index':3,'contact_anchor':[455,196],
      'mace_before_after_04':{'before':[420.72,357.384],'after':[420.72,376.384],'target':[421,376],'error_px':round(math.dist([420.72,376.384],[421,376]),6)},'frames':measured})

if __name__=='__main__':
    rows=audit();sheets(rows);landmarks()
    print('A7_SPEC_AUDIT anchors_pass=2 motion_placeholder=5 art_pass=false local_seam_regressions=true')
