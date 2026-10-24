"""A7 constrained edits and separately recorded anchor touch-ups; no body rig.

Runtime geometry remains A6 except the declared connected follow-through patch.
Raw tool returns are immutable, all intermediate results retained per attempt.
"""
from build_a7_spec import ROOT, SHARED, OUT, sha, write, load
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import argparse, shutil, math, json

ORDER=['01','02','00','03','04']
BASE=OUT/'baseline-a6'
def archive():
    BASE.mkdir(parents=True,exist_ok=True)
    pairs=[(SHARED/f'thoma/swing/{i:02}.png',BASE/f'{i:02}.png') for i in range(6)]
    pairs += [(SHARED/'thoma/idle/01.png',BASE/'idle-01.png'),(SHARED/'manifest.json',BASE/'manifest.json'),(SHARED/'frame-audit.json',BASE/'frame-audit.json')]
    for src,dst in pairs:
        if not dst.exists():shutil.copyfile(src,dst)
    if not (OUT/'style-check-a6.png').exists():shutil.copyfile(SHARED/'thoma-weapon-style-check.png',OUT/'style-check-a6.png')
    write(BASE/'hashes.json',[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for _,p in pairs])

def prepare(frame):
    folder=OUT/f'attempts/{frame}';folder.mkdir(parents=True,exist_ok=True)
    if (folder/'attempt-1.json').exists():raise ValueError('Frame already prepared; do not overwrite attempt')
    refs=[]
    for src,label,role in [(BASE/f'{frame}.png','edit-target.png','EDIT TARGET: A6 structure/pose; retain feet, bag, weapon'),
       (SHARED/'thoma/idle/01.png','anchor-idle.png','APPEARANCE MASTER ONLY'),(SHARED/'thoma/swing/05.png','anchor-recover.png','APPEARANCE corroboration ONLY')]:
        dest=folder/label;shutil.copyfile(src,dest)
        refs.append({'path':src.relative_to(ROOT).as_posix(),'input_copy':dest.relative_to(ROOT).as_posix(),'sha256':sha(src),'role':role})
    spec=load(SHARED/'thoma-appearance-spec.json')
    target=spec['pose_targets'][frame]
    prompt=(f'Use case: identity-preserve / precise-object-edit. EDIT the FIRST image, an EXISTING swing/{frame} animation frame. Do NOT generate an independent new full-body pose. '
      'Images 2 and 3 are immutable appearance anchors: same elderly man, angular weathered face, close grey swept hair, short grey beard, narrow dark eyes, teal cowl and robe, ivory stole/undersleeves, brown single satchel with one cloth roll, bronze medallion. '
      'Retain the FIRST image exact canvas framing, scale, complete silhouette, pose, hands/grip, connected feet and ONE bag. Preserve its fine worn hand-painted edges and muted original colours. '
      'Make only small controlled identity and costume corrections to the first image: match the anchor face/hair features, narrow ivory stole falls and their exact small grey-green botanical sprigs, short irregular ivory fringes, cuff edge and layered continuous hem. '
      'There are TWO sprigs total, one at each stole end: a simple central stem with alternating oblique leaf strokes, about 18x31px left and 15x43px right on 512px canvas, no new motifs or trim. '
      'Short fringe tips 4-9px, approximately 10 left/8 right visible, plus ONE long waist rope, no long new tassels. Match exact anchor motif scale, not a large decorative plant. '
      'Use the anchors to restore the SAME character, not a younger/redesigned face. Repair local details while retaining all already-correct structure. '
      f"512x512 transparent canvas, pivot [256,464]. Pose intent: {target['intent']}; mace head target {target['landmarks']['mace_head']}, grip {target['landmarks']['mace_grip']}. "
      'Keep existing A6 mace head/haft/collar/grip dimensions and orientation, single short one-handed dark iron flanged mace on worn oak haft with small brass collar. '
      + ('For this follow-through ONLY, lower the connected weapon hand/forearm AND mace about19px so head centre moves from [421,357] to [421,376]; keep weapon dimensions; blend the sleeve naturally. ' if frame=='04' else 'Do not move the weapon, hands, body or feet. ')
      +'No scene, other figures, labels, cast shadow, new ornament, duplicate bag, detached footwear, geometric fragments, bright recolouring or Ferry Dusk palette. Output ONLY the edited first sprite on genuine alpha.')
    (folder/'attempt-1.prompt.txt').write_text(prompt+'\n',encoding='utf-8',newline='\n')
    a5=ROOT/f'godot-spike/docs/evidence/spike02-a6/baseline-a5/{frame}.png'
    raw=[p for p in sorted((ROOT/f'godot-spike/docs/evidence/spike02-a6/candidates/{frame}').glob('*.png'))]
    rec={'frame':f'thoma/swing/{frame}.png','attempt':1,'tool':'image_gen (built-in)', 'mode':'edit existing A6 target with two immutable anchors, not independent regeneration',
      'prompt':prompt,'references':refs,'spec_sha256':sha(SHARED/'thoma-appearance-spec.json'),
      'base_selection':{'structure':'A6 adopted: connected shoes, one bag, no cutout joins; retain original pixels outside local masks.',
        'face_hair':'idle/01 exact source pixels, swing/05 corroboration; A5 candidate has correct face but no better body structure.',
        'embroidery_tassels':'idle/01 crop pixels, not A5 deformation or A6 larger invented sprigs.',
        'cuffs_hem_bag_feet_weapon':'A6 adopted pose geometry; generator only supplies local surface touch-up, not replacement anatomy.',
        'a5_considered':{'path':a5.relative_to(ROOT).as_posix(),'sha256':sha(a5),'reason':'01 is best A5 frame but silhouette/hem pop against A6 neighbours; other A5 frames have known structural scraps/gaps.'},
        'a6_raw_considered':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'reason':'Higher resolution same structural base; normalized adopted version preserves established registration. 02 attempt2 has bulbous shoulder/stole.'} for p in raw]},
      'settings':{'transparent_background':True,'seed':'not exposed','model':'not exposed','quality':'not exposed','requested_size':[512,512]},
      'status':'PREPARED','adopted':False,'touchups':[]}
    write(folder/'attempt-1.json',rec)
    print(prompt)

def feather_mask(box, radius=2):
    m=Image.new('L',(512,512));ImageDraw.Draw(m).rectangle(box,fill=255)
    return m.filter(ImageFilter.GaussianBlur(radius))

def record(frame):
    folder=OUT/f'attempts/{frame}';rec=load(folder/'attempt-1.json')
    raw=folder/'attempt-1.png';im=Image.open(raw).convert('RGBA')
    rec.update(raw=raw.relative_to(ROOT).as_posix(),raw_sha256=sha(raw))
    rec['settings']['returned_size']=list(im.size)
    rec['status']='RAW_SAVED'
    write(folder/'attempt-1.json',rec)
    print('A7_RAW_RECORDED',frame,im.size,sha(raw))

def finish(frame):
    folder=OUT/f'attempts/{frame}';rec=load(folder/'attempt-1.json')
    if rec['status']!='RAW_SAVED':raise ValueError('Must save raw before touch-up; never overwrite completed attempt')
    index=ORDER.index(frame)
    if index:
        previous=load(OUT/f'attempts/{ORDER[index-1]}/attempt-1.json')
        assert previous['status']=='FINISHED', 'Sequential frame order required'
    base=Image.open(BASE/f'{frame}.png').convert('RGBA');out=base.copy()
    raw=Image.open(folder/'attempt-1.png').convert('RGBA')
    raw.resize((512,512),Image.Resampling.LANCZOS).save(folder/'attempt-1-normalized-preview.png',optimize=True)
    rec['normalization']={'scale':512/raw.width,'translate':[0,0],'method':'uniform scale only, preview retained; not adopted because generator reframed the target and changed local identity/motif',
       'output':(folder/'attempt-1-normalized-preview.png').relative_to(ROOT).as_posix(),'sha256':sha(folder/'attempt-1-normalized-preview.png')}
    rec['generated_pixels_adopted']=False
    rec['raw_result']='REJECT: constrained edit returned reframed/repainted details; using it as a whole frame would violate A6 geometry. Preserve A6 structure and finish the authorized anchor touch-ups instead.'
    anchor=Image.open(SHARED/'thoma/idle/01.png').convert('RGBA')
    centre=load(SHARED/'thoma-appearance-spec.json')['pose_targets'][frame]['landmarks']['head_centre']
    delta=[centre[0]-256,centre[1]-138]
    def apply_layer(name,layer,mask,details):
        nonlocal out
        before=folder/f'touchup-{len(rec["touchups"])+1:02}-input.png';out.save(before,optimize=True)
        # RGB texture replacement: preserve A6 structural alpha, feet and bag.
        structural_alpha=out.getchannel('A')
        mask=ImageChops.multiply(mask,structural_alpha.point(lambda a:255 if a>240 else 0))
        out=Image.composite(layer,out,mask);out.putalpha(structural_alpha)
        n=len(rec['touchups'])+1
        mpath=folder/f'touchup-{n:02}-mask.png';mask.save(mpath,optimize=True)
        after=folder/f'touchup-{n:02}-output.png';out.save(after,optimize=True)
        rec['touchups'].append({'name':name,'input':before.relative_to(ROOT).as_posix(),'input_sha256':sha(before),
          'output':after.relative_to(ROOT).as_posix(),'output_sha256':sha(after),'mask':mpath.relative_to(ROOT).as_posix(),
          'mask_sha256':sha(mpath),'source':'shared-anim/thoma/idle/01.png','source_sha256':sha(SHARED/'thoma/idle/01.png'),
          'details':details,'alpha_policy':'A6 silhouette alpha retained exactly; inward blend; no body/limb warping'})
    # Full identity interior at unit scale; keep A6 head silhouette rather than
    # detach/rebuild neck. Remaining silhouette discrepancy is an explicit FAIL.
    shifted=Image.new('RGBA',(512,512));shifted.alpha_composite(anchor,tuple(delta))
    m=Image.new('L',(512,512));poly=[(232,118),(239,109),(252,106),(270,110),(281,121),(283,149),(273,163),(258,169),(244,158),(236,145)]
    ImageDraw.Draw(m).polygon([(x+delta[0],y+delta[1]) for x,y in poly],fill=255)
    m=m.filter(ImageFilter.GaussianBlur(1.25));m=ImageChops.multiply(m,shifted.getchannel('A'))
    apply_layer('anchor face/hair interior',shifted,m,{'source_polygon':poly,'uniform_scale':1,'translate':delta,'feather_px':1.25,
      'limit':'Exact interior source features, but A6 outer hair silhouette retained; identity outline still requires visual acceptance.'})
    # Place source ivory/motif/fringe texture into existing A6 panel interiors.
    # These offsets were chosen from A6 panel ends, NOT generated appearance.
    config={'01':[(0,0),(0,-4)],'02':[(0,0),(0,-5)],'00':[(-10,0),(2,-1)],
            '03':[(-20,12),(-12,9)],'04':[(-26,0),(-14,8)]}[frame]
    # Visible left sprig is partly obscured by anchor mace: do not invent its
    # hidden apex. The donor starts below the original mace silhouette.
    polys=[[(224,349),(251,349),(254,377),(247,383),(221,381)],
           [(288,300),(305,299),(310,348),(309,358),(289,364)]]
    for j,(poly,delta) in enumerate(zip(polys,config)):
        layer=Image.new('RGBA',(512,512));layer.alpha_composite(anchor,tuple(delta))
        m=Image.new('L',(512,512));ImageDraw.Draw(m).polygon([(x+delta[0],y+delta[1]) for x,y in poly],fill=255)
        m=m.filter(ImageFilter.GaussianBlur(1.2))
        apply_layer('anchor '+['left','right'][j]+' sprig/fringe',layer,m,{'source_polygon':poly,'uniform_scale':1,'translate':delta,'feather_px':1.2,
          'limit':'Visible anchor sprig only; underlying A6 stole outline retained; donor may not cover every old fringe edge. No hidden embroidery inferred.'})
    if frame=='04':
        # Translate the existing contiguous hand/weapon patch down by 19px.
        # No resizing or redrawing the mace; patch starts inside opaque cuff.
        before=out.copy();mask=Image.new('L',(512,512));d=ImageDraw.Draw(mask)
        poly=[(331,286),(354,297),(385,321),(444,344),(452,373),(427,388),(389,363),(352,331),(334,319)]
        d.polygon(poly,fill=255)
        # Only hand and weapon outward of cuff; original alpha extraction.
        patch=before.copy();patch.putalpha(ImageChops.multiply(before.getchannel('A'),mask))
        cleared=before.copy();cleared.putalpha(ImageChops.subtract(before.getchannel('A'),patch.getchannel('A')))
        moved=Image.new('RGBA',(512,512));moved.alpha_composite(patch,(0,19));cleared.alpha_composite(moved)
        # Fill only newly exposed opaque cuff interior from adjacent A6 sleeve.
        fill=before.copy();fill.alpha_composite(before,(0,10))
        join=Image.new('L',(512,512));ImageDraw.Draw(join).polygon([(331,289),(347,297),(355,321),(339,330),(327,309)],fill=255)
        join=join.filter(ImageFilter.GaussianBlur(2))
        cleared=Image.composite(fill,cleared,join)
        step=folder/'touchup-04-output.png';cleared.save(step,optimize=True)
        mpath=folder/'touchup-04-mask.png';mask.save(mpath,optimize=True)
        rec['touchups'].append({'name':'connected follow-through hand/weapon translation','input':rec['touchups'][-1]['output'],
          'input_sha256':rec['touchups'][-1]['output_sha256'],'output':step.relative_to(ROOT).as_posix(),'output_sha256':sha(step),
          'mask':mpath.relative_to(ROOT).as_posix(),'mask_sha256':sha(mpath),'source':(BASE/'04.png').relative_to(ROOT).as_posix(),
          'source_sha256':sha(BASE/'04.png'),'details':{'polygon':poly,'scale':1,'translate':[0,19],'cuff_join_polygon':[(331,289),(347,297),(355,321),(339,330),(327,309)],'feather_px':2},
          'limit':'Weapon geometry unchanged; cuff continuity must be inspected; no automatic seam PASS.'})
        out=cleared
    runtime=folder/'attempt-1-runtime.png';out.save(runtime,optimize=True)
    shutil.copyfile(runtime,SHARED/f'thoma/swing/{frame}.png')
    rec.update(status='FINISHED',adopted=True,runtime=runtime.relative_to(ROOT).as_posix(),runtime_sha256=sha(runtime),
      placeholder=True,reason='Anchor interior texture corrections only. Outer silhouette/drape and remaining motif fringes are not proven consistent; retain PLACEHOLDER.',
      completed_order=index+1,previous_frame=ORDER[index-1] if index else None)
    rec['neighbour_check']={'role':'consistency check ONLY, never appearance source','previous_frame':ORDER[index-1] if index else None,
      'sha256':sha(SHARED/f'thoma/swing/{ORDER[index-1]}.png') if index else None}
    write(folder/'attempt-1.json',rec)
    records=[load(OUT/f'attempts/{f}/attempt-1.json') for f in ORDER if (OUT/f'attempts/{f}/attempt-1.json').exists() and load(OUT/f'attempts/{f}/attempt-1.json')['status']=='FINISHED']
    write(SHARED/'a7-swing-prompts.json',records)
    # Append-only per-finished-frame provenance; never edit prior source entries.
    with (SHARED/'SOURCES.md').open('a',encoding='utf-8',newline='\n') as stream:
      stream.write('\n\n'+('## spike-02 A7 — constrained edits and anchor touch-ups\n\n' if index==0 else '')+f'### A7 swing/{frame}, attempt 1\n\n')
      stream.write('Exact attempt record (all prompts, inputs, masks, intermediate hashes, settings): `'+(folder/'attempt-1.json').relative_to(ROOT).as_posix()+'`.\n\n')
      stream.write(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
    print('A7_FINISHED',frame,'order',index+1,'raw_adopted=false runtime',sha(runtime),'PLACEHOLDER')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',action='store_true');p.add_argument('--prepare');p.add_argument('--record');p.add_argument('--finish');args=p.parse_args()
    if args.archive:archive()
    if args.prepare:prepare(args.prepare)
    if args.record:record(args.record)
    if args.finish:finish(args.finish)
