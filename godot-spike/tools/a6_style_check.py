"""Unscaled region evidence, explicit model observations and adjacent proxies."""
from prepare_a6_frames import *

PATHS=['thoma/idle/01.png']+[f'thoma/swing/{i:02}.png' for i in range(6)]
REGIONS={'stole':(150,140,350,410),'embroidery':(135,305,340,410),
 'cuffs':(100,100,415,305),'hem':(90,340,430,447),'seams':(150,140,390,335),
 'bag_count':(150,225,290,355),'feet':(90,390,430,470),
 'face_hair':(210,90,350,207),'palette':(150,145,345,435)}
CHECKS=['stole','embroidery','cuffs','hem','face_hair','palette','seams','bag_count','feet','mace','sequence']
BG=(34,40,38)
def mace_box(path):
    if '/idle/' in path or path.endswith('05.png'):return (155,265,265,365)
    return {'00':(95,60,225,155),'01':(150,55,290,160),'02':(325,55,490,215),
            '03':(320,155,490,235),'04':(300,280,475,410)}[path[-6:-4]]
def roi(im,box):
    m=Image.new('L',SIZE);ImageDraw.Draw(m).rectangle(box,fill=255)
    return ImageChops.multiply(m,im.getchannel('A'))
def table_row(r):
    flags=[r['region_review'][k].split(':')[0] for k in CHECKS];flags[7]='1 '+flags[7]
    return '| `'+r['path']+'` | '+r['status']+' | '+' | '.join(flags)+' | '+r['reason']+' |'

def sheets():
    regions=list(REGIONS)+['mace'];cell=350;block=cell*4
    sheet=Image.new('RGB',(len(regions)*block,1850),BG);d=ImageDraw.Draw(sheet);crops=[]
    d.text((8,5),'A6 1:1 SOURCE CROPS: idle / recover / A5 same-index / A6. Model review, not Owner acceptance.',fill='white')
    for row,path in enumerate(PATHS[1:6]):
        y=30+row*320
        for col,name in enumerate(regions):
            x=col*block;d.text((x+5,y),path+' '+name,fill='#d2b777')
            for j,src in enumerate([PATHS[0],PATHS[-1],path,path]):
                file=BASE/path[-6:] if j==2 else SHARED/src
                im=Image.open(file).convert('RGBA');box=mace_box(src) if name=='mace' else REGIONS[name]
                crop=im.crop(box);assert crop.width<=cell and crop.height<=290
                if name=='palette':
                    rgb=tuple(round(v) for v in ImageStat.Stat(im.convert('RGB'),roi(im,box)).mean)
                    d.rectangle((x+j*cell+8,y+30,x+j*cell+150,y+130),fill=rgb)
                    d.text((x+j*cell+8,y+140),str(rgb),fill='white')
                else:sheet.paste(crop,(x+j*cell+5,y+20),crop)
                d.text((x+j*cell+5,y+305),['idle/01','swing/05','A5 '+src[-6:-4],'A6 '+src[-6:-4]][j],fill='white')
                crops.append({'frame':src,'source':file.relative_to(REPO).as_posix(),'region':name,'box':box,'scale':1})
    d.text((8,1640),'Actual native 720p Godot movie crops are appended below after rendered playback; no rescaling.',fill='white')
    for i,path in enumerate(PATHS):
        file=OUT/'sequence-runtime'/('idle.png' if i==0 else f'{i-1:02}.png')
        if file.exists():
            im=Image.open(file).convert('RGB').crop((260,160,580,480))
            sheet.paste(im,(i*350,1670));d.text((i*350+5,1830),path+' native runtime crop',fill='white')
    # Native row is 320 high: expand canvas instead of scaling its pixels.
    if (OUT/'sequence-runtime/00.png').exists():
        expanded=Image.new('RGB',(sheet.width,2040),BG);expanded.paste(sheet,(0,0));sheet=expanded;d=ImageDraw.Draw(sheet)
        for i,path in enumerate(PATHS):
            file=OUT/'sequence-runtime'/('idle.png' if i==0 else f'{i-1:02}.png')
            im=Image.open(file).convert('RGB').crop((260,160,580,480));sheet.paste(im,(i*350,1670))
            d.text((i*350+5,2000),path+' actual 720p',fill='white')
    sheet.save(OUT/'region-check.png',optimize=True);write(OUT/'region-crops.json',crops)
    strip=Image.new('RGB',(3584,640),BG);d=ImageDraw.Draw(strip)
    for i,path in enumerate(PATHS):
        im=Image.open(SHARED/path).convert('RGBA');d.text((i*512+8,8),path,fill='white');strip.paste(im,(i*512,30),im)
        native=im.resize((68,68),Image.Resampling.LANCZOS);strip.paste(native,(i*512+10,560),native)
    d.text((100,600),'Equal 512px canvases; 68px rest approximation below. Real playback evidence separate. NOT full sequence PASS.',fill='white')
    strip.save(OUT/'sequence-strip.png',optimize=True);strip.save(SHARED/'thoma-weapon-style-check.png',optimize=True)

def metrics():
    pairs=[]
    heights=load(OUT/'geometry-check.json')['frames']
    for prev,cur in zip(PATHS,PATHS[1:]):
        ims=[Image.open(SHARED/p).convert('RGBA') for p in [prev,cur]]
        means={name:round(math.dist(*[ImageStat.Stat(im.convert('RGB'),roi(im,box)).mean for im in ims]),4) for name,box in REGIONS.items()}
        alphas=[im.getchannel('A').crop((100,275,420,440)).point(lambda a:255 if a>127 else 0) for im in ims]
        inter=sum(v>0 for v in ImageChops.darker(*alphas).getdata());union=sum(v>0 for v in ImageChops.lighter(*alphas).getdata())
        pairs.append({'from':prev,'to':cur,'region_mean_rgb_delta':means,'garment_silhouette_iou':round(inter/union,6),
            'character_height_delta_px':heights[cur]['head_to_ground_px']-heights[prev]['head_to_ground_px'],
            'visual_result':'FAIL','reason':'Changed motif/fringe width and drape/stance produce visible pops; intact anatomy does not establish sequence fidelity.'})
    write(OUT/'sequence-check.json',{'authority':'model inspection of actual rendered frame sequence, not human playtest',
        'pairs':pairs,'limits':'Rectangular alpha-intersected region masks include occlusion and moving pose. RGB/IoU/height are proxies only. No proxy threshold approves art.'})

def geometry():
    # Source-pixel landmarks manually selected on raw outputs; uncertainties are
    # retained. The contact transform is exactly anchored, not locally warped.
    raw={'00':{'head_top':[650,212],'ground':[350,1151],'mace_head':[477,130],'grip':[302,215]},
         '01':{'head_top':[650,195],'ground':[400,1182],'mace_head':[660,120],'grip':[475,180]},
         '02':{'head_top':[690,213],'ground':[295,1154],'mace_head':[1140,200],'grip':[935,335]},
         '03':{'head_top':[645,191],'ground':[270,1143],'mace_head':[1170,424],'grip':[910,424]},
         '04':{'head_top':[790,133],'ground':[865,1145],'mace_head':[1110,842],'grip':[900,695]}}
    frames={PATHS[0]:{'head_to_ground_px':360,'immutable':True},PATHS[-1]:{'head_to_ground_px':369,'immutable':True}}
    records=load(SHARED/'a6-swing-prompts.json')
    for r in records:
        if not r['adopted']:continue
        index=r['frame'][-6:-4];points=raw[index];settings=r['normalization']['settings'];s=settings['scale'];tx,ty=settings['translate']
        mapped={k:[round(p[0]*s+tx,4),round(p[1]*s+ty,4)] for k,p in points.items()}
        im=Image.open(SHARED/r['frame']).convert('RGBA');a=im.getchannel('A');bottom=a.point(lambda v:255 if v>127 else 0).getbbox()[3]-1
        frames[r['frame']]={'raw_landmarks':points,'mapped_landmarks':mapped,'landmark_uncertainty_raw_px':3,
            'head_to_ground_px':round(mapped['ground'][1]-mapped['head_top'][1],4),
            'head_to_ground_tolerance_px':18,'ground_bottom_opaque_y':bottom,'mace_grip_to_head_px':round(math.dist(mapped['grip'],mapped['mace_head']),4),
            'mace_design':'short one-handed flanged iron head / oak haft / brass collar; generated brush detail differs, not protected RGBA',
            'contact_anchor_exact_transform':mapped['mace_head']==[455.0,196.0] if index=='03' else None}
    write(OUT/'geometry-check.json',{'canvas':[512,512],'pivot':[256,464],'contact_frame_index':3,'contact_anchor':[455,196],
        'limits':'Manual landmarks, +/-3 raw pixels. Painted mace/hand pixels are newly generated; exact A5 pixel geometry is NOT claimed. 04 head is about19px above A5 pose; recorded mace FAIL.', 'frames':frames})

def audit():
    rows=load(SHARED/'frame-audit.json');provenance={r['frame']:r for r in load(SHARED/'a6-swing-prompts.json') if r['adopted']}
    for r in rows:
        if r['path'] not in PATHS:continue
        moving=r['path'] in provenance
        reviews={k:'PASS: immutable original reference endpoint; transition defects assigned to motion frame.' for k in CHECKS}
        if moving:
            reviews.update(stole='PASS: two continuous ivory bands and coherent shoulder drape; no pasted duplicate.',
                embroidery='FAIL: botanical sprigs are newly redrawn, fuller and differently spaced; fringe differs from immutable references.',
                cuffs='PASS: whole painted sleeve joins cuff/hand continuously; no loose sleeve fragment.',
                hem='PASS: continuous layered underskirt and teal robe; A5 triangular/floating scraps removed.',
                face_hair='FAIL: recognizable elderly grey-haired man, but fuller cheek/hair detail changes from immutable face.',
                palette='PASS: muted original families after recorded idle/01 nearest-palette remap; no Ferry Dusk.',
                seams='PASS: no A5 rectangular cutout join; continuous painted shoulder/waist/cuffs.',
                bag_count='PASS: exactly one satchel with one roll, no cloned bag.',
                feet='PASS: both brown boots connect naturally beneath continuous underskirt; no A5 ankle gap.',
                mace='PASS: short one-handed iron flanged head, oak haft and brass collar; original pose intent retained, painted details newly generated.',
                sequence='FAIL: actual playback still shows botanical/fringe and robe-width changes, especially entering/leaving fixed reference poses.')
            if r['path'].endswith('04.png'):reviews['mace']='FAIL: design retained, but generated head is about19px higher than A5 follow-through; exact pose geometry not met.'
            reason='Structural fragments/feet repaired; generated motif/fringe and face fidelity still drift; sequence retains visible pops.'
            if r['path'].endswith('04.png'):reason+=' Follow-through mace-head height differs from A5.'
            p=provenance[r['path']];r.update(source=p['raw'],raw_sha256=p['raw_sha256'],palette_distance=p['normalization']['palette_distance'],cleanup=p['normalization']['operations'])
        else:reason='Byte-identical reference endpoint; motion transition failures remain assigned to motion frames; not Owner approval.'
        r.update(sha256=sha(SHARED/r['path']),status='PLACEHOLDER' if moving else 'PASS',region_review=reviews,
            review_segment='spike-02 A6',review_authority='model observation only; not Owner approval or human playtest',bag_count=1,
            bag_count_authority='model count in whole figure and bag crop',reason=reason)
        r['style_review']={name:reviews[key] for name,key in [('face','face_hair'),('stole_cape_embroidery','embroidery'),('cuffs','cuffs'),
            ('hem_silhouette','hem'),('palette','palette'),('stroke','seams'),('satchel_medallion','bag_count')]}
        r['style_review'].update(proportions='PASS: common canvas/pivot, uniform whole-frame transform; 5% head-height tolerance.',light_direction='PASS: subdued top-left illumination.')
    write(SHARED/'frame-audit.json',rows)
    header='| Frame | Status | Stole | Embroidery | Cuffs | Hem | Face/hair | Palette | Seams | Bag count | Feet | Mace | Sequence | Reason |\n'
    header+='| '+' | '.join(['---']*14)+' |\n'
    (OUT/'frame-status-table.md').write_text(header+'\n'.join(table_row(r) for r in rows if r['path'] in PATHS)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    geometry();sheets();metrics();audit()
    print('A6_MODEL_AUDIT motion_placeholder=5 reference_pass=2 structural_improvement=true full_art_pass=false')
