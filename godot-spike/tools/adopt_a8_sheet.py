"""A8 W2 sheet attempt records and pose-only input variants; no rig or body warp."""
from prepare_a8_sheet import ROOT, SHARED, OUT, sha, write
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import json
import argparse
import math
import shutil
from collections import deque
from pathlib import Path

def prepare(number):
    folder=OUT/'sheet-attempts'
    inputs=OUT/'inputs'
    prompt=(inputs/'sheet-prompt.txt').read_text(encoding='utf-8')
    paths=[inputs/n for n in ['sheet-canvas.png','sheet-mask.png','anchors-2x.png','spec-crops.png']]
    if number==2:
        canvas=Image.open(paths[0]).convert('RGBA')
        layout=json.loads((inputs/'sheet-layout.json').read_text())
        for panel in layout['panels']:
            if panel['fixed']:continue
            name=panel['frame'].split('/')[-1]
            base=Image.open(OUT/f'baseline-a7/{name}.png').convert('RGBA')
            silhouette=Image.new('RGBA',base.size)
            silhouette.paste((90,99,97,255),(0,0,512,512),base.getchannel('A').point(lambda a:round(a*.22)))
            x,y=panel['rect'][:2]
            guide=canvas.crop(tuple(panel['rect']))
            silhouette.alpha_composite(guide)
            canvas.paste(silhouette,(x,y))
        target=folder/'attempt-2-canvas.png'
        canvas.save(target)
        paths[0]=target
        prompt+='\nAttempt2 correction: same design and painting across ALL five frames remains first priority. The middle cells now contain FAINT FLAT SILHOUETTES ONLY, no face or costume texture. Follow their exact arm/leg placement and the joint guide; use the two fixed ANCHOR figures for every surface detail. Do not reframe, enlarge the figures or fill the cell. Keep head top at103 and foot line464 in each512px cell. In panel4 (02) the mace is ABOVE and RIGHT at449,110, not horizontally in front of the chest. In panel6 (04) mace is DOWN at421,376, not at waist level. Do not make the mace bigger than the anchor. Keep the two fixed panel figures their original360px height and keep all seven heads the same size. Return the original2048x1024 grid including empty margins.\n'
    if number==3:
        paths[0]=folder/'attempt-2-canvas.png'
        prompt+='\nAttempt3 emphasis: Use the flat silhouette scaffold for pose ONLY. Copy the character rendering density, angular squared beard, very short grey hair, narrow ivory stole widths and TINY embroidery from the two immutable anchors. In earlier outputs the stole got too wide, embroidered plants too large, and long regular tassels replaced the short uneven fringe. Correct this throughout ALL FIVE cells together. Preserve anchor1 and7 exactly. The visible two stole ends should differ in length as in the anchors, not symmetrical matching strips. Do not smooth or simplify the anchor mottled surface. Keep all faces the same with an exposed ear and short squared beard. Output ONE sheet with original4+3 grid and empty eighth cell, same pose locations, each figure360px tall in its512px cell, opaque contact mace at455,196. No ground shadow or ground line.\n'
    pp=folder/f'attempt-{number}.prompt.txt'
    pp.write_text(prompt,encoding='utf-8')
    rec={'attempt':number,'tool':'image_gen (built-in)','mode':'edit one shared seven-panel sheet',
         'prompt':prompt,'prompt_path':pp.relative_to(ROOT).as_posix(),'prompt_sha256':sha(pp),
         'inputs':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in paths],
         'settings':{'transparent_background':True,'seed':'not exposed','model':'not exposed',
                     'quality':'not exposed','mask_parameter':'not exposed; supplied as supporting image + prompt only'},
         'adjustment':{1:'Initial brief scaffold',2:'22% flat A7 alpha silhouette for pose only; prompt corrects reframe and02/04 arc',3:'Same pose scaffold; prompt prioritizes anchor-scale narrow stole, tiny sprigs, uneven short fringe and hair/beard'}[number],
         'fallback':False}
    raw=folder/f'attempt-{number}.png'
    if raw.exists():
        rec.update(raw=raw.relative_to(ROOT).as_posix(),raw_sha256=sha(raw),returned_size=list(Image.open(raw).size))
    write(folder/f'attempt-{number}.json',rec)
    print(pp.read_text(encoding='utf-8'))

def slice_preview(number):
    folder=OUT/'sheet-attempts'
    raw=Image.open(folder/f'attempt-{number}.png').convert('RGBA')
    assert abs(raw.width/raw.height-2)<.002
    sheet=raw.resize((2048,1024),Image.Resampling.LANCZOS)
    layout=json.loads((OUT/'inputs/sheet-layout.json').read_text())
    dest=OUT/f'normalized/attempt-{number}'
    dest.mkdir(parents=True,exist_ok=True)
    preview=Image.new('RGB',(2560,512),(35,40,38))
    for i,panel in enumerate(layout['panels'][1:6]):
        im=sheet.crop(tuple(panel['rect']))
        im.save(dest/f'{i:02}-slice.png')
        preview.paste(im,(i*512,0),im)
    d=ImageDraw.Draw(preview)
    for x in range(0,2560,32):d.line((x,0,x,512),fill=(65,70,68));d.text((x+1,1),str(x%512),fill='white')
    for y in range(32,512,32):d.line((0,y,2560,y),fill=(65,70,68));d.text((1,y+1),str(y),fill='white')
    preview.save(dest/'coordinate-preview.png')
    print(raw.size,'slice pixels in',dest)

def clean(im):
    """Keep generated alpha; remove low-alpha debris and small detached islands."""
    alpha=im.getchannel('A').point(lambda a:0 if a<24 else a)
    bits=bytearray(alpha.point(lambda a:1 if a else 0).tobytes())
    pix=bytearray(alpha.tobytes())
    for start in range(len(bits)):
        if not bits[start]:continue
        todo=deque([start]);bits[start]=0;component=[]
        while todo:
            q=todo.popleft();component.append(q);x=q%512;y=q//512
            for n in ([q-1] if x else [])+([q+1] if x<511 else [])+([q-512] if y else [])+([q+512] if y<511 else []):
                if bits[n]:bits[n]=0;todo.append(n)
        if len(component)<80:
            for q in component:pix[q]=0
    alpha=Image.frombytes('L',(512,512),bytes(pix))
    im.putalpha(alpha)
    # Straight colour is retained at nonzero alpha, not multiplied by alpha.
    im.paste((0,0,0,0),(0,0,512,512),alpha.point(lambda a:255 if a==0 else 0))
    return im

def adopt(number):
    assert number==3,'Selection frozen after visual comparison'
    folder=OUT/f'normalized/attempt-{number}'
    targets=[[192,85],[259,87],[449,110],[455,196],[421,376]]
    # Manual1x picks on whole sheet after its UNIFORM2048/1774 resize.
    head_tops=[83,85,103,70,74]
    head_x=[264,268,313,293,324]
    target_x=[260,260,282,264,310]
    grips=[(136,91),(219,49),(418,175),(403,157),(393,296)]
    old_heads=[(217,48),(321,32),(469,103),(489,151),(479,357)]
    polygons=[[(148,79),(191,50),(198,20),(226,15),(249,43),(232,75),(196,74),(152,103)],
      [(238,34),(288,23),(299,10),(327,9),(342,28),(338,48),(312,58),(291,44),(239,56)],
      [(425,156),(445,119),(443,94),(466,78),(493,87),(498,115),(478,132),(441,174)],
      [(420,145),(463,140),(475,124),(506,122),(512,140),(512,175),(479,177),(460,163),(421,169)],
      [(407,302),(458,333),(470,332),(501,341),(507,368),(489,386),(462,377),(453,357),(400,321)]]
    anchor=Image.open(SHARED/'thoma/idle/01.png').convert('RGBA')
    headmask=Image.new('L',(512,512))
    ImageDraw.Draw(headmask).polygon([(212,319),(218,318),(219,311),(228,317),(236,316),(237,325),(247,330),(239,336),(239,344),(230,338),(222,344),(220,334),(212,331),(216,325)],fill=255)
    donor=anchor.copy();donor.putalpha(ImageChops.multiply(anchor.getchannel('A'),headmask));donor=donor.crop((210,309,249,346))
    donor.save(folder/'mace-head-donor.png')
    records=[]
    sheet_rec=json.loads((OUT/f'sheet-attempts/attempt-{number}.json').read_text())
    for i in range(5):
        im=clean(Image.open(folder/f'{i:02}-slice.png').convert('RGBA'))
        a=im.getchannel('A').point(lambda v:255 if v>127 else 0)
        bottom=a.getbbox()[3]-1
        s=361/(bottom-head_tops[i]);tx=target_x[i]-head_x[i]*s;ty=464-bottom*s
        matrix=(1/s,0,-tx/s,0,1/s,-ty/s)
        norm=im.transform((512,512),Image.Transform.AFFINE,matrix,Image.Resampling.BICUBIC)
        norm=clean(norm)
        before=folder/f'{i:02}-normalized.png';norm.save(before)
        old=Image.new('L',(512,512));ImageDraw.Draw(old).polygon(polygons[i],fill=255)
        old=old.transform((512,512),Image.Transform.AFFINE,matrix,Image.Resampling.NEAREST)
        # Existing opaque hand/forearm retained. Only old exposed weapon is erased.
        result=norm.copy();result.putalpha(ImageChops.subtract(norm.getchannel('A'),old))
        grip=(grips[i][0]*s+tx,grips[i][1]*s+ty)
        target=targets[i]
        angle=math.degrees(math.atan2(target[1]-grip[1],target[0]-grip[0]))
        layer=Image.new('RGBA',(512,512));d=ImageDraw.Draw(layer)
        # Local weapon redraw: thin textured worn-oak haft, rounded pommel,
        # bronze collar; original anchor-head pixels rotate as one rigid patch.
        d.line([grip,tuple(target)],fill=(39,25,17,255),width=8)
        d.line([(grip[0],grip[1]-1),(target[0],target[1]-1)],fill=(105,76,48,255),width=4)
        d.line([(grip[0],grip[1]-2),(target[0],target[1]-2)],fill=(145,110,73,255),width=1)
        vx,vy=target[0]-grip[0],target[1]-grip[1];dist=math.hypot(vx,vy);ux,uy=vx/dist,vy/dist
        collar=(target[0]-ux*18,target[1]-uy*18)
        d.line([(collar[0]-uy*4,collar[1]+ux*4),(collar[0]+uy*4,collar[1]-ux*4)],fill=(151,114,69,255),width=5)
        rotated=donor.rotate(35-angle,Image.Resampling.BICUBIC,expand=True)
        alpha=rotated.getchannel('A');pts=[(x,y,alpha.getpixel((x,y))) for y in range(rotated.height) for x in range(rotated.width) if alpha.getpixel((x,y))>127]
        cx=sum(x for x,y,a in pts)/len(pts);cy=sum(y for x,y,a in pts)/len(pts)
        pos=(round(target[0]-cx),round(target[1]-cy))
        layer.alpha_composite(rotated,pos)
        # Put the untouched painted gripping fingers over the new haft.
        hand=norm.crop((round(grip[0]-8),round(grip[1]-8),round(grip[0]+8),round(grip[1]+8)))
        result.alpha_composite(layer)
        result.alpha_composite(hand,(round(grip[0]-8),round(grip[1]-8)))
        result=clean(result)
        final=folder/f'{i:02}-runtime.png';result.save(final)
        mask=ImageChops.lighter(old,layer.getchannel('A'));mp=folder/f'{i:02}-weapon-fix-mask.png';mask.save(mp)
        measured=[round(pos[0]+cx,3),round(pos[1]+cy,3)]
        shutil.copyfile(final,SHARED/f'thoma/swing/{i:02}.png')
        records.append({'frame':f'thoma/swing/{i:02}.png','adopted':True,'sheet_attempt':number,'fallback':False,
          'tool':sheet_rec['tool'],'prompt':sheet_rec['prompt'],'inputs':sheet_rec['inputs'],'settings':sheet_rec['settings'],
          'raw':sheet_rec['raw'],'raw_sha256':sheet_rec['raw_sha256'],'runtime':final.relative_to(ROOT).as_posix(),'runtime_sha256':sha(final),
          'slice':{'layout':'godot-spike/docs/evidence/spike02-a8/inputs/sheet-layout.json','uniform_sheet_scale':2048/1774,'panel':i+2},
          'normalization':{'scale':s,'translate':[tx,ty],'head_top_before':head_tops[i],'lowest_opaque_before':bottom,'method':'uniform scale and translation ONLY; alpha cleanup, no body warping'},
          'local_fixes':[{'scope':'exposed mace only; hand/forearm/body kept','input':before.relative_to(ROOT).as_posix(),'input_sha256':sha(before),
             'output':final.relative_to(ROOT).as_posix(),'output_sha256':sha(final),'mask':mp.relative_to(ROOT).as_posix(),'mask_sha256':sha(mp),
             'donor':(folder/'mace-head-donor.png').relative_to(ROOT).as_posix(),'donor_sha256':sha(folder/'mace-head-donor.png'),
             'source':'shared-anim/thoma/idle/01.png','source_sha256':sha(SHARED/'thoma/idle/01.png'),
             'before_mace_head':[old_heads[i][0]*s+tx,old_heads[i][1]*s+ty],'target':target,'measured_head_alpha_centroid':measured,
             'description':'Remove old exposed weapon via polygon mask; redraw oak haft/collar between original grip and target; rigidly rotate anchor iron head; no forearm/body deformation. Painted-hand pixels composited over haft. Seam/design review separate.',
             'head_output_position':list(pos),'head_rotation_degrees':35-angle,'grip':list(grip)}],
          'alpha_policy':'Generated alpha preserved above24; disconnected components<80px removed; RGB retained straight, zero RGB where alpha0',
          'placeholder':True})
    attempts=[json.loads(p.read_text()) for p in sorted((OUT/'sheet-attempts').glob('attempt-?.json'))]
    write(SHARED/'a8-swing-prompts.json',{'method':'single shared sheet edit','selected_attempt':number,'sheet_attempts':attempts,'fallback_edits':[], 'frames':records})
    with (SHARED/'SOURCES.md').open('a',encoding='utf-8',newline='\n') as f:
        f.write('\n\n## spike-02 A8 — brief-driven shared sheet\n\nBuilt-in image_gen EDIT, three whole-sheet attempts; attempt3 adopted for all five frames. No per-frame generation/fallback. Full prompts, input/reference/mask SHA-256, raw/runtime hashes, tool settings (seed/model not exposed), slice transforms and local weapon fix input/output/mask/donor hashes: `a8-swing-prompts.json`. Raw sheets are immutable under `godot-spike/docs/evidence/spike02-a8/sheet-attempts/`. The tool has no explicit mask argument; supporting mask + prompt requested fixed endpoints, but it repainted them. Runtime endpoints remain original byte-identical files. All five remain PLACEHOLDER pending the full13-item audit.\n')
        f.write(json.dumps({'sheet_attempts':attempts,'frames':records},ensure_ascii=False,indent=2)+'\n')
    print('A8_ADOPTED single_sheet=3 frames=5 fallback=false local_weapon_fixes=5')

def cleanup_residuals():
    provenance=json.loads((SHARED/'a8-swing-prompts.json').read_text())
    polygons={'01':[(275,64),(308,64),(308,86),(281,88)],
              '04':[(399,313),(447,343),(444,349),(398,322)]}
    for rec in provenance['frames']:
        name=Path(rec['frame']).stem
        if name not in polygons:continue
        src=ROOT/rec['runtime'];im=Image.open(src).convert('RGBA')
        mask=Image.new('L',(512,512));ImageDraw.Draw(mask).polygon(polygons[name],fill=255)
        im.putalpha(ImageChops.subtract(im.getchannel('A'),mask))
        im=clean(im)
        dest=src.with_name(name+'-runtime-2.png');im.save(dest)
        mp=src.with_name(name+'-residual-cleanup-mask.png');mask.save(mp)
        rec['local_fixes'].append({'scope':'old exposed mace shaft residual ONLY','input':src.relative_to(ROOT).as_posix(),'input_sha256':sha(src),
          'output':dest.relative_to(ROOT).as_posix(),'output_sha256':sha(dest),'mask':mp.relative_to(ROOT).as_posix(),'mask_sha256':sha(mp),
          'description':'1x inspection found small remnant of superseded shaft outside first mask; erase exact residual polygon without changing body/head/hand/new mace.'})
        rec.update(runtime=dest.relative_to(ROOT).as_posix(),runtime_sha256=sha(dest))
        shutil.copyfile(dest,SHARED/rec['frame'])
    write(SHARED/'a8-swing-prompts.json',provenance)
    with (SHARED/'SOURCES.md').open('a',encoding='utf-8',newline='\n') as f:
        f.write('\n### A8 W2 final local cleanup revision\n\nFirst local normalization retained old shaft slivers on01 and04. Original runtime and masks preserved. Final local erasure masks and input/output hashes follow; no further imagegen or body changes. The live final hashes in a8-swing-prompts.json supersede the first W2 runtime entries above.\n')
        f.write(json.dumps(provenance['frames'],indent=2)+'\n')
    print('A8_LOCAL_RESIDUAL_CLEANUP frames=01,04')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',type=int);p.add_argument('--slice',type=int);p.add_argument('--adopt',type=int);p.add_argument('--cleanup-residuals',action='store_true');args=p.parse_args()
    if args.prepare:prepare(args.prepare)
    if args.slice:slice_preview(args.slice)
    if args.adopt:adopt(args.adopt)
    if args.cleanup_residuals:cleanup_residuals()
