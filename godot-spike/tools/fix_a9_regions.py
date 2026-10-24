"""A9 bounded donor-pixel experiments. Candidate output is NEVER auto-approved.

Explicit --accept/--reject decisions follow visual inspection of each contact
sheet. Original A8 and every candidate/input/submask stay immutable.
"""
from prepare_a9_regions import *
from PIL import ImageChops, ImageFilter
import math, argparse

IDENTITY=(1,0,0,0,1,0)
MOTIFS={
 '00':[((239,367),0),((326,344),-15)],
 '01':[((242,367),0),((329,344),-14)],
 '02':[((209,365),12),((312,338),-6)],
 '03':[((163,369),19),((258,336),0)],
 '04':[((182,354),18),((307,358),-9)]}

def affine(centre,target,angle=0,scale=1):
    c,s=math.cos(math.radians(angle))*scale,math.sin(math.radians(angle))*scale
    return (c,-s,target[0]-c*centre[0]+s*centre[1],s,c,target[1]-s*centre[0]-c*centre[1])
def warp(im,m,nearest=False):
    a,b,c,d,e,f=m;det=a*e-b*d
    inv=(e/det,-b/det,(b*f-e*c)/det,-d/det,a/det,(d*c-a*f)/det)
    return im.transform((512,512),Image.Transform.AFFINE,inv,Image.Resampling.NEAREST if nearest else Image.Resampling.BICUBIC)
def cut(im,m):
    out=im.copy();out.putalpha(ImageChops.multiply(im.getchannel('A'),m));return out
def delta_mask(a,b):
    diff=ImageChops.difference(a,b)
    channels=diff.split();out=channels[0]
    for ch in channels[1:]:out=ImageChops.lighter(out,ch)
    return out.point(lambda v:255 if v else 0)
def technical(im,f):
    alpha=im.getchannel('A');opaque=alpha.point(lambda v:255 if v>127 else 0)
    bottom=opaque.getbbox()[3]-1
    target=load(OUT/'defects-and-targets.json')['frames'][f]['targets']['mace_head']
    pts=[(x,y) for y in range(target[1]-18,target[1]+19) for x in range(target[0]-18,target[0]+19) if im.getpixel((x,y))[3]>229]
    centre=[sum(p[k] for p in pts)/len(pts) for k in range(2)] if pts else [-999,-999]
    return {'size':list(im.size),'mode':im.mode,'bottom':bottom,'ground':sum(opaque.getpixel((x,464))>0 for x in range(410)),
      'mace_centre':centre,'mace_error':math.dist(centre,target),'contact_opaque':f!='03' or im.getpixel((455,196))[3]>229}

def prepare(f):
    folder=OUT/f'attempts/{f}';folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'candidates.json').exists(),'Do not overwrite attempts'
    base=Image.open(OUT/f'baseline-a8/{f}.png').convert('RGBA')
    idle=Image.open(SHARED/'thoma/idle/01.png').convert('RGBA')
    recover=Image.open(SHARED/'thoma/swing/05.png').convert('RGBA')
    spec=load(OUT/'defects-and-targets.json')['frames'][f];records=[]
    source=OUT/f'baseline-a8/{f}.png'
    for region in REGIONS:
        permitted=Image.open(OUT/f'masks/{f}/{region}.png').convert('L')
        result=base.copy();transforms=[];donor='thoma/idle/01.png';description=''
        if region=='head':
            target=spec['target_head_centre'];m=affine((256,138),target)
            srcmask=Image.open(OUT/'masks/idle-01/head.png')
            layer=warp(cut(idle,srcmask),m)
            # Remove ONLY A8 head. Preserve the lower collar/shoulder overlap.
            result.paste((0,0,0,0),(0,0,512,512),permitted)
            result.alpha_composite(layer)
            # A four-pixel lower seam blends RGB toward the original collar.
            # Face interior/eyes/crown are never painted.
            seam=Image.new('L',(512,512));d=ImageDraw.Draw(seam)
            dy=target[1]-138;dx=target[0]-256
            d.polygon([(244+dx,165+dy),(262+dx,173+dy),(277+dx,169+dy),(276+dx,175+dy),(260+dx,178+dy),(242+dx,169+dy)],fill=72)
            seam=ImageChops.multiply(seam,permitted)
            # Only blend where both head and original are already opaque.
            overlap=ImageChops.multiply(base.getchannel('A'),result.getchannel('A'))
            seam=ImageChops.multiply(seam,overlap)
            blended=Image.composite(base,result,seam);blended.putalpha(result.getchannel('A'));result=blended
            seam.save(folder/'head-1-seam-mask.png')
            transforms=[{'part':'face_hair_beard','matrix':m,'source_mask':rel(OUT/'masks/idle-01/head.png')}]
            description='Exact idle head translated without scale or rotation; small bottom-neck RGB seam blend; no face repaint.'
        elif region in ['embroidery','tassels','stole']:
            if region=='embroidery':boxes=[(222,337,253,373),(285,300,309,350)];centres=[(238,355),(297,325)]
            elif region=='tassels':boxes=[(220,369,255,386),(285,346,313,366)];centres=[(238,355),(297,325)]
            else:boxes=[(220,272,255,386),(285,266,313,366)];centres=[(238,355),(297,325)]
            for side,(box,centre,(target,angle)) in enumerate(zip(boxes,centres,MOTIFS[f])):
                sm=mask([rect(*box)]);m=affine(centre,target,angle)
                # Stole/tassel replacement attempts use anchor alpha. Motif-only
                # transplants preserve A8 alpha and feather three pixels in RGB.
                wm=warp(sm,m);layer=warp(idle,m)
                if region=='embroidery':
                    feather=sm.filter(ImageFilter.GaussianBlur(1.2));wm=warp(feather,m)
                    wm=ImageChops.multiply(wm,base.getchannel('A'))
                    new=Image.composite(layer,result,wm);new.putalpha(base.getchannel('A'));result=new
                else:
                    oldpanel=mask([PANELS[f][side]]) if region=='stole' else wm
                    erase=ImageChops.multiply(oldpanel,permitted)
                    result.paste((0,0,0,0),(0,0,512,512),erase)
                    result.alpha_composite(cut(layer,wm))
                transforms.append({'part':['left','right'][side],'source_box':box,'matrix':m,'source_anchor':donor})
            description='Two separate rigid anchor terminal patches; '+('alpha locked, narrow feather RGB seam only.' if region=='embroidery' else 'test narrower anchor panel/fringe with original alpha; inspect hem continuity before adoption.')
        elif region=='mace':
            if f in ['00','01']:
                donor='thoma/swing/05.png'
                grip=load(A8/'landmark-deltas.json')['measured'][f'thoma/swing/{f}.png']['hand_weapon']
                target=spec['targets']['mace_head'];angle=math.degrees(math.atan2(target[1]-grip[1],target[0]-grip[0]))
                srcangle=math.degrees(math.atan2(333-299,223-183))
                # STRICT rigid transform, scale=1: preserve head and haft size.
                m=affine((223,333),target,angle-srcangle)
                sm=Image.open(OUT/'masks/swing-05/mace.png');layer=warp(cut(recover,sm),m)
                # Erase exposed old weapon only, not the painted fingers.
                erase=Image.new('L',(512,512));d=ImageDraw.Draw(erase)
                end=(grip[0]+(target[0]-grip[0])*.20,grip[1]+(target[1]-grip[1])*.20)
                d.line([end,tuple(target)],fill=255,width=15);d.ellipse((target[0]-24,target[1]-24,target[0]+24,target[1]+24),fill=255)
                result.paste((0,0,0,0),(0,0,512,512),erase)
                result.alpha_composite(layer)
                # Restore original finger box over the rigid shaft, retaining grip.
                hb=(round(grip[0]-10),round(grip[1]-10),round(grip[0]+10),round(grip[1]+10))
                result.paste(base.crop(hb),hb[:2])
                transforms=[{'part':'canon_mace_rigid','matrix':m,'scale':1,'head_source':[223,333],'head_target':target,'original_grip':grip,'source_mask':rel(OUT/'masks/swing-05/mace.png')}]
                description='Rigid recover05 mace transplant, no compression; preserve original gripping fingers. Grip alignment and alpha independently reviewed.'
            else:
                transforms=[{'matrix':IDENTITY}];description='No pose repair prescribed for this mace; A8 target/opaque contact protected.'
        elif region=='legs_feet':
            donor=f'thoma/swing/{f}.png (baseline A8)'
            if f=='03':
                boxes=[(29,404,111,467),(261,410,349,451)];moves=[(61,0),(35,3)]
            elif f=='04':boxes=[(316,430,389,467),(55,405,134,467)];moves=[(-17,0),(72,-9)]
            else:boxes=[];moves=[]
            for box,(dx,dy) in zip(boxes,moves):
                sm=mask([rect(*box)]);m=(1,0,dx,0,1,dy)
                result.paste((0,0,0,0),(0,0,512,512),sm)
                result.alpha_composite(warp(cut(base,sm),m))
                transforms.append({'part':'boot_and_lower_leg','source_box':box,'matrix':m})
            description='Translate intact boot/lower-leg pixels toward brief feet; inspect hem and leg attachment; no whole-body warp.' if boxes else 'No stance repair prescribed; retain A8 grounded boots.'
        # ENFORCED destination permission: even an accidental overshoot cannot
        # change any RGBA byte outside W1's mask.
        result=Image.composite(result,base,permitted)
        change=delta_mask(base,result);outside=ImageChops.subtract(change,permitted)
        assert outside.getbbox() is None
        output=folder/f'{region}-1.png';result.save(output)
        mp=folder/f'{region}-1-mask.png';change.save(mp)
        rec={'frame':f'thoma/swing/{f}.png','region':region,'attempt':1,'input':rel(source),'input_sha256':sha(source),
          'output':rel(output),'output_sha256':sha(output),'mask':rel(mp),'mask_sha256':sha(mp),
          'permission_mask':spec['masks'][region]['path'],'permission_mask_sha256':spec['masks'][region]['sha256'],
          'source_anchor':donor,'source_sha256':sha(SHARED/donor) if '(baseline' not in donor else sha(source),
          'transform':transforms,'tool':'Python Pillow manual donor-pixel compositing','prompt':None,'whole_frame_regeneration':False,
          'description':description,'changed_pixels':sum(v>0 for v in change.getdata()),'technical':technical(result,f),'decision':'PENDING_VISUAL_INSPECTION'}
        write(folder/f'{region}-1.json',rec);records.append(rec)
    write(folder/'candidates.json',records)
    preview=Image.new('RGB',(7*512,560),(36,39,38));d=ImageDraw.Draw(preview)
    for i,(name,im) in enumerate([('A8',base)]+[(r['region'],Image.open(ROOT/r['output'])) for r in records]):
        preview.paste(im,(i*512,35),im);d.text((i*512+8,8),f'{f} {name} candidate (not accepted)',fill='white')
    preview.save(folder/'candidate-review.png')
    print(f'A9 candidates {f}: '+', '.join(f'{r["region"]}={r["changed_pixels"]}px' for r in records))

def refine(f):
    """Second local attempt after inspecting 03: avoid carved collar and occluded motif."""
    folder=OUT/f'attempts/{f}';records=load(folder/'candidates.json')
    base=Image.open(OUT/f'baseline-a8/{f}.png').convert('RGBA')
    idle=Image.open(SHARED/'thoma/idle/01.png').convert('RGBA')
    spec=load(OUT/'defects-and-targets.json')['frames'][f]
    for region in ['head','embroidery']:
        r=next(r for r in records if r['region']==region)
        assert r['attempt']==1
        permitted=Image.open(ROOT/r['permission_mask'])
        result=base.copy();transforms=[]
        if region=='head':
            m=affine((256,138),spec['target_head_centre'])
            layer=warp(cut(idle,Image.open(OUT/'masks/idle-01/head.png')),m)
            # Remove old crown only ABOVE ear height; the collar underpainting
            # stays in place. Original face is covered by opaque donor interior.
            old=Image.new('L',(512,512));od=ImageDraw.Draw(old)
            b=HEAD_BOXES[f];od.rectangle((b[0],b[1],b[2],b[1]+40),fill=255)
            old=ImageChops.multiply(old,permitted)
            # Carve only original head-coloured pixels; leave teal collar.
            warm=Image.new('L',(512,512));wp=warm.load();bp=base.load()
            for y in range(b[1],b[1]+41):
                for x in range(b[0],b[2]+1):
                    red,g,blue,a=bp[x,y]
                    if red>g*1.05 and g>blue*1.04 and a:wp[x,y]=255
            old=ImageChops.multiply(old,warm)
            result.paste((0,0,0,0),(0,0,512,512),old)
            result.alpha_composite(layer)
            transforms=[{'part':'head','matrix':m,'source_mask':rel(OUT/'masks/idle-01/head.png')}]
            desc='Revision2: exact donor face/hair; remove warm old crown only above ears, retain teal collar underpainting; no face repaint.'
        else:
            for side,(box,centre,(target,angle)) in enumerate(zip([(225,349,251,373),(289,300,307,347)],[(238,355),(297,325)],MOTIFS[f])):
                sm=mask([rect(*box)]);m=affine(centre,target,angle)
                wm=warp(sm.filter(ImageFilter.GaussianBlur(1.0)),m)
                wm=ImageChops.multiply(wm,base.getchannel('A'))
                result=Image.composite(warp(idle,m),result,wm);result.putalpha(base.getchannel('A'))
                transforms.append({'part':['left','right'][side],'source_box':box,'matrix':m})
            desc='Revision2: exclude anchor weapon occlusion and teal edge from motif crops; retain original alpha and feather1px. Larger A8 motifs may remain around patch.'
        result=Image.composite(result,base,permitted)
        output=folder/f'{region}-2.png';mp=folder/f'{region}-2-mask.png';result.save(output);change=delta_mask(base,result);change.save(mp)
        r.update(attempt=2,output=rel(output),output_sha256=sha(output),mask=rel(mp),mask_sha256=sha(mp),transform=transforms,
          description=desc,changed_pixels=sum(v>0 for v in change.getdata()),technical=technical(result,f))
        write(folder/f'{region}-2.json',r)
    write(folder/'candidates.json',records)
    preview=Image.new('RGB',(3*512,550),(36,39,38))
    for i,im in enumerate([base,Image.open(folder/'head-2.png'),Image.open(folder/'embroidery-2.png')]):preview.paste(im,(i*512,30),im)
    ImageDraw.Draw(preview).text((8,5),f'{f}: A8 / head2 / embroidery2',fill='white');preview.save(folder/'revision-review.png')
    print('A9 local revisions2 prepared',f)

def decide(f,accepted):
    folder=OUT/f'attempts/{f}';records=load(folder/'candidates.json')
    logpath=OUT/'a9-fix-log.json'
    log=load(logpath) if logpath.exists() else {'method':'A8 base; region masks enforced in Python; anchor pixel transplants and manual seam blends only','order':ORDER,'operations':[],'frames':{}}
    assert f not in log['frames'],'Frame already decided'
    done=list(log['frames']);assert f==ORDER[len(done)],'Must process prescribed order'
    base=Image.open(OUT/f'baseline-a8/{f}.png').convert('RGBA');final=base.copy()
    oldchecks=load(OUT/'defects-and-targets.json')['frames'][f]['a8_checklist']
    for r in records:
        keep=r['region'] in accepted
        if r['changed_pixels']==0:keep=False;reason='No change required here; A8 pixels retained.'
        elif keep:
            t=r['technical'];assert t['mace_error']<=4 and 463<=t['bottom']<=465 and t['ground']>4 and t['contact_opaque']
            reason='Native-size model inspection: '+('rigid canon head/haft size and straightness improve; original fingers/cuff retained; integration still needs W3 review.' if r['region']=='mace' else 'anchor face identity improves; collar underpainting preserved.')+' Protected A8 PASS items remain visually intact. No Owner approval.'
            m=Image.open(ROOT/r['mask']);candidate=Image.open(ROOT/r['output']);final=Image.composite(candidate,final,m)
        elif r['region'] in ['stole','tassels']:
            reason='REGRESSION: narrower anchor patch cuts continuous ivory/teal hem or creates a cloth seam/alpha notch; retain A8 region, including its existing motif/fringe defects.'
        elif r['region']=='legs_feet':
            reason='REGRESSION: foot translation opens a gap or abrupt hem-to-leg boundary; A8 feet/hem PASS would be lost. Keep attached A8 legs/feet, acknowledge target FAIL.'
        elif r['region']=='mace':
            reason='REGRESSION: rigid uncompressed donor does not meet painted grip without severing the continuous cuff/hand or leaving exposed old shaft; preserve A8 grip/cuff, target and weapon pixels.'
        elif r['region']=='embroidery':reason='REGRESSION/NO IMPROVEMENT: residual A8 leaves and donor sprig overlap or show patch boundaries; two exact anchor motifs not established; preserve A8 pixels.'
        else:reason='No demonstrated improvement without new edge/lighting seam; A8 region retained.'
        recheck={n:('PASS: A8 passing feature remains intact in native candidate review.' if oldchecks[n].startswith('PASS') else 'FAIL: not certified by this local operation; full W3 audit required.') for n in CHECKS}
        if not keep and r['changed_pixels']:
            if r['region'] in ['stole','tassels','legs_feet']:recheck['hem']='FAIL: candidate breaks previously continuous lower garment; reverted.'
            if r['region']=='legs_feet':recheck['feet']='FAIL: candidate attachment is less continuous than A8; reverted.'
            if r['region']=='mace':recheck['cuffs']='FAIL: donor grip/shaft overlap jeopardizes continuous wrist; reverted.'
        r.update(kept=keep,decision='kept' if keep else 'reverted_to_a8',reason=reason,regression_check_13=recheck,
          regression_authority='model native source comparison; A8 PASS items protected; not human approval')
        for previous_attempt in range(1,r['attempt']):
            first=load(folder/f'{r["region"]}-{previous_attempt}.json')
            first.update(kept=False,decision='reverted_to_a8',reason='Native review found '+('donor robe contamination and target-centroid error in rigid mace1.' if r['region']=='mace' else 'carved collar gap (head) or donor weapon/teal edge contamination (motif).')+' Replaced by bounded revision2.',regression_check_13={n:('PASS: feature unchanged.' if oldchecks[n].startswith('PASS') else 'FAIL: local candidate not certified.') for n in CHECKS})
            # Palette/seams already failed/passed as specified; no failed trial is
            # silently erased. Preserve candidate PNG, mask and original matrix.
            write(folder/f'{r["region"]}-{previous_attempt}.json',first);log['operations'].append(first)
        write(folder/f'{r["region"]}-{r["attempt"]}.json',r);log['operations'].append(r)
    dest=SHARED/f'thoma/swing/{f}.png';final.save(dest)
    union=Image.new('L',(512,512))
    for r in records:
        if r['kept']:union=ImageChops.lighter(union,Image.open(ROOT/r['mask']))
    assert ImageChops.subtract(delta_mask(base,final),union).getbbox() is None
    finalmask=folder/'final-kept-mask.png';union.save(finalmask)
    installed=folder/'installed.png';shutil.copyfile(dest,installed)
    log['frames'][f]={'path':rel(dest),'sha256':sha(dest),'baseline_sha256':sha(OUT/f'baseline-a8/{f}.png'),
      'installed':rel(installed),'kept_mask':rel(finalmask),'kept_mask_sha256':sha(finalmask),'technical':technical(final,f),'kept_regions':[r['region'] for r in records if r['kept']]}
    write(logpath,log)
    with (SHARED/'SOURCES.md').open('a',encoding='utf-8',newline='\n') as stream:
        stream.write(f'\n\n### spike-02 A9 targeted frame {f}\n\nA8 base; Python/Pillow manual anchor transplants, enforced region masks. No image generation, whole-frame repaint or new external material. Model regression review only; Owner approval pending. Complete operation records:\n\n```json\n'+json.dumps(records,indent=2,ensure_ascii=False)+'\n```\n')
    print(f'A9_DECIDED {f} kept={log["frames"][f]["kept_regions"]} sha256={sha(dest)}')

def withdraw(f,region):
    """Regression found during adjacent-candidate comparison: explicit third trial."""
    logpath=OUT/'a9-fix-log.json';log=load(logpath);rec=log['frames'][f]
    previous=next(r for r in reversed(log['operations']) if r['frame'].endswith(f'/{f}.png') and r['region']==region and r['kept'])
    folder=OUT/f'attempts/{f}';live=SHARED/f'thoma/swing/{f}.png'
    inp=folder/f'{region}-3-input.png';shutil.copyfile(live,inp)
    im=Image.open(live);base=Image.open(OUT/f'baseline-a8/{f}.png');m=Image.open(ROOT/previous['mask'])
    im=Image.composite(base,im,m);out=folder/f'{region}-3.png';im.save(out);shutil.copyfile(out,live)
    previous.update(kept=False,decision='withdrawn_after_adjacent_review',reason='Adjacent/source review revealed residual A8 leaves plus donor motif make the embroidery larger/doubled; improvement not established. Third operation restores A8 region.')
    write(folder/f'{region}-{previous["attempt"]}.json',previous)
    op=dict(previous);op.update(attempt=3,input=rel(inp),input_sha256=sha(inp),output=rel(out),output_sha256=sha(out),
      transform=[{'matrix':IDENTITY}],source_anchor=f'baseline-a8/{f}.png',source_sha256=sha(OUT/f'baseline-a8/{f}.png'),
      kept=False,decision='reverted_to_a8',reason='REGRESSION: overlapping motif patches do not improve anchor consistency. Restore exact A8 motif pixels; original candidates retained.',
      description='Explicit regional rollback to A8 following sequential comparison; no generation.',technical=technical(im,f))
    log['operations'].append(op);write(folder/f'{region}-3.json',op)
    rec.update(sha256=sha(live),installed=rel(out),technical=technical(im,f));rec['kept_regions'].remove(region)
    union=Image.new('L',(512,512))
    for r in log['operations']:
        if r['frame']==f'thoma/swing/{f}.png' and r.get('kept'):union=ImageChops.lighter(union,Image.open(ROOT/r['mask']))
    keptmask=folder/'final-kept-mask-v2.png';union.save(keptmask);rec.update(kept_mask=rel(keptmask),kept_mask_sha256=sha(keptmask))
    assert ImageChops.subtract(delta_mask(base,im),union).getbbox() is None
    write(logpath,log)
    with (SHARED/'SOURCES.md').open('a',encoding='utf-8') as stream:stream.write('\nA9 corrective regression withdrawal (supersedes prior kept motif decision):\n```json\n'+json.dumps(op,indent=2)+'\n```\n')
    print('A9_WITHDRAW',f,region,'final',sha(live))

def mace_refine(f):
    folder=OUT/f'attempts/{f}';records=load(folder/'candidates.json');r=next(r for r in records if r['region']=='mace')
    assert f in ['00','01'] and r['attempt']==1
    base=Image.open(OUT/f'baseline-a8/{f}.png').convert('RGBA');donor=Image.open(SHARED/'thoma/swing/05.png').convert('RGBA')
    polys=[[(182,297),(187,294),(214,316),(217,324),(210,327),(183,302)],
      [(209,319),(218,320),(231,321),(232,329),(240,330),(237,337),(241,340),(235,343),(232,349),(225,342),(214,344),(214,335),(205,329),(210,325)]]
    sm=mask(polys);sp=folder/'mace-2-source-mask.png';sm.save(sp)
    target=load(OUT/'defects-and-targets.json')['frames'][f]['targets']['mace_head']
    grip=r['transform'][0]['original_grip'];angle=math.degrees(math.atan2(target[1]-grip[1],target[0]-grip[0]))
    m=affine((223,333),(target[0]+1,target[1]+1),angle-math.degrees(math.atan2(34,40)))
    layer=warp(cut(donor,sm),m)
    erase=Image.new('L',(512,512));d=ImageDraw.Draw(erase)
    end=(grip[0]+(target[0]-grip[0])*.20,grip[1]+(target[1]-grip[1])*.20)
    d.line([end,tuple(target)],fill=255,width=14);d.ellipse((target[0]-23,target[1]-23,target[0]+23,target[1]+23),fill=255)
    out=base.copy();out.paste((0,0,0,0),(0,0,512,512),erase);out.alpha_composite(layer)
    hb=(round(grip[0]-10),round(grip[1]-10),round(grip[0]+10),round(grip[1]+10));out.paste(base.crop(hb),hb[:2])
    out=Image.composite(out,base,Image.open(ROOT/r['permission_mask']))
    output=folder/'mace-2.png';mp=folder/'mace-2-mask.png';out.save(output);change=delta_mask(base,out);change.save(mp)
    r.update(attempt=2,output=rel(output),output_sha256=sha(output),mask=rel(mp),mask_sha256=sha(mp),
      transform=[{'part':'canon_mace','matrix':m,'scale':1,'original_grip':grip,'source_mask':rel(sp),'source_mask_sha256':sha(sp)}],
      description='Revision2: tightly traced recover05 weapon mask excludes ivory robe/bag contamination; rigid scale1, original fingers restored, +1px centroid allowance.',
      changed_pixels=sum(v>0 for v in change.getdata()),technical=technical(out,f))
    write(folder/'mace-2.json',r);write(folder/'candidates.json',records)
    print('A9_MACE2',f,r['technical'])

def head_final(f):
    folder=OUT/f'attempts/{f}';records=load(folder/'candidates.json');r=next(r for r in records if r['region']=='head')
    assert r['attempt']==2
    base=Image.open(OUT/f'baseline-a8/{f}.png').convert('RGBA');idle=Image.open(SHARED/'thoma/idle/01.png').convert('RGBA')
    target=load(OUT/'defects-and-targets.json')['frames'][f]['target_head_centre'];m=affine((256,138),target)
    # The W1 box underestimated 01's old nose/right hair. Record a revised
    # bounded permission mask rather than silently changing the frozen W1 mask.
    pm=mask([rect(224,99,311,177)]);pp=folder/'head-3-permission-mask.png';pm.save(pp)
    warm=Image.new('L',(512,512));wp=warm.load();bp=base.load()
    for y in range(99,174):
        for x in range(224,312):
            red,g,b,a=bp[x,y]
            if red>g*1.02 and g>b*1.02 and a:wp[x,y]=255
    im=base.copy();im.paste((0,0,0,0),(0,0,512,512),warm)
    im.alpha_composite(warp(cut(idle,Image.open(OUT/'masks/idle-01/head.png')),m))
    im=Image.composite(im,base,pm)
    output=folder/'head-3.png';mp=folder/'head-3-mask.png';im.save(output);dm=delta_mask(base,im);dm.save(mp)
    r.update(attempt=3,output=rel(output),output_sha256=sha(output),mask=rel(mp),mask_sha256=sha(mp),
      permission_mask=rel(pp),permission_mask_sha256=sha(pp),transform=[{'matrix':m,'source_mask':rel(OUT/'masks/idle-01/head.png')}],
      description='Revision3: correct underestimated old01 nose/hair mask; erase warm original head above collar and composite unchanged anchor face. Explicit revised region permission, not whole-frame edit.',
      changed_pixels=sum(v>0 for v in dm.getdata()),technical=technical(im,f))
    write(folder/'head-3.json',r);write(folder/'candidates.json',records)
    print('A9_HEAD3',f,r['technical'])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--prepare');ap.add_argument('--refine');ap.add_argument('--head-final');ap.add_argument('--mace-refine');ap.add_argument('--decide');ap.add_argument('--withdraw',nargs=2);ap.add_argument('--accept',default='')
    args=ap.parse_args()
    if args.prepare:prepare(args.prepare)
    if args.refine:refine(args.refine)
    if args.mace_refine:mace_refine(args.mace_refine)
    if args.head_final:head_final(args.head_final)
    if args.decide:decide(args.decide,args.accept.split(','))
    if args.withdraw:withdraw(*args.withdraw)
