"""A7 W1: source-pixel appearance measurements; pose targets are design targets.

No generated/candidate pixels are used to infer appearance. Half-open crop
boxes, integer manual landmarks +/-2 px; fringe tips +/-1 due to brush grain.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, math

ROOT = Path(__file__).resolve().parents[2]
SHARED = ROOT / 'shared-anim'
OUT = ROOT / 'godot-spike/docs/evidence/spike02-a7'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))

ANCHORS = {'idle/01':'thoma/idle/01.png', 'swing/05':'thoma/swing/05.png'}
BOXES = {
 'face':[(233,118,284,174),(227,108,279,165)],
 'hair':[(227,101,286,150),(221,91,281,140)],
 'robe':[(165,175,325,400),(162,167,325,406)],
 'stole':[(187,151,312,387),(183,143,310,386)],
 'embroidery_left':[(222,337,253,373),(219,337,250,374)],
 'embroidery_right':[(285,300,309,350),(282,292,306,343)],
 'tassels_left':[(220,369,255,386),(217,369,252,386)],
 'tassels_right':[(285,346,313,366),(282,339,310,359)],
 'cuffs':[(154,230,332,284),(151,225,329,282)],
 'hem':[(169,351,325,423),(163,347,326,427)],
 'bag':[(181,246,241,323),(178,241,239,321)],
 'belt':[(198,234,282,270),(193,228,279,263)],
 'shoes':[(181,388,332,465),(179,395,331,465)],
 'mace':[(170,289,252,348),(170,290,246,352)],
 'outline':[(166,339,191,380),(162,339,187,380)]}

# Explicit samples, never a made-up style palette. Names describe sampled use.
SAMPLES = {'skin_light':(265,128),'skin_mid':(251,151),'skin_shadow':(254,134),
 'hair_light':(252,112),'hair_mid':(242,119),'hair_shadow':(233,131),
 'teal_light':(233,210),'teal_mid':(224,224),'teal_shadow':(209,214),
 'ivory_light':(211,185),'ivory_mid':(222,223),'ivory_shadow':(203,178),
 'embroidery':(298,326),'leather':(202,295),'oak':(202,312),
 'iron':(232,328),'brass':(215,318),'outline':(187,379)}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    images = [Image.open(SHARED / p).convert('RGBA') for p in ANCHORS.values()]
    # Select real, opaque pixels within tightly identified material regions.
    # Rank by luminance; retain exact pixel coordinates, never average/invent hex.
    samples = dict(SAMPLES)
    for prefix,box,predicate in [
      ('teal',(167,182,200,228),lambda p:p[1]>p[0] and p[2]>p[0]),
      ('ivory',(210,182,224,228),lambda p:p[0]>p[1]>p[2] and p[0]>130),
      ('hair',(233,107,267,125),lambda p:abs(p[0]-p[1])<35 and p[0]>65)]:
      pixels=[(sum(images[0].getpixel((x,y))[:3]),(x,y)) for y in range(box[1],box[3]) for x in range(box[0],box[2])
              if images[0].getpixel((x,y))[3]>240 and predicate(images[0].getpixel((x,y)))]
      pixels.sort()
      for level,q in [('light',.85),('mid',.5),('shadow',.15)]:samples[prefix+'_'+level]=pixels[int((len(pixels)-1)*q)][1]
    embroidery_pixels=[(sum(images[0].getpixel((x,y))[:3]),(x,y)) for x in range(291,305) for y in range(309,343) if images[0].getpixel((x,y))[3]>240]
    embroidery_pixels.sort();samples['embroidery']=embroidery_pixels[len(embroidery_pixels)//6][1]
    palette = {name:{'hex':'#%02x%02x%02x'%images[0].getpixel(pt)[:3],
                     'sample_xy':list(pt),'source':'idle/01','rgba':list(images[0].getpixel(pt))}
               for name,pt in samples.items()}
    face = {'shape':'Right-facing three-quarter angular long face; heavy brow, deep eye socket, projecting nose, short squared grey beard and moustache.',
      'landmarks_idle':{'eyes':[[263,137],[279,138]],'nose_tip':[281,148],'mouth':[271,158],'chin':[264,170],'ear':[241,145]},
      'eye_brow':'Dark 1-2px eyes beneath 2-3px oblique brows; no bright round cartoon iris.',
      'mouth':'Closed, short dark horizontal mouth under pale moustache; no smile.',
      'skin_hex':{k:palette[k]['hex'] for k in ['skin_light','skin_mid','skin_shadow']}}
    hair = {'silhouette':'Close cropped irregular grey cap, receding at temple, swept right; small textured curls. Exposes ear; ends at nape above teal collar.',
       'bbox_idle':[227,103,285,149],'bbox_recover':[222,93,280,140],
       'parting':'No clean graphic part line resolvable; rightward brushed crown, not invented centre part.',
       'colours':{k:palette[k]['hex'] for k in ['hair_light','hair_mid','hair_shadow']}}
    costume = {
      'robe':{'description':'Desaturated dark teal short outer sleeve and long divided outer skirt over ivory ankle-length underrobe; textured broad shaded folds.', 'outer_hem_idle_y':[370,397],'inner_hem_idle_y':[397,421]},
      'stole':{'description':'Two ivory hanging panels, broad near shoulder, narrow at waist, widening toward embroidered ends; teal cowl crosses above.',
        'idle_left_width_px_at_y':{'185':27,'225':24,'362':30},'idle_right_width_px_at_y':{'185':12,'225':15,'330':22},
        'folds':'Left shoulder diagonal to waist at (235,250), left vertical fall to (237,379); right fall (286,161) to (299,357), narrow dark fold on inner edge.',
        'endpoint_choice':'idle/01 panel shapes and motif spacing; swing/05 confirms construction but right sprig/fringe sits ~7px higher.'},
      'embroidery':{'description':'One muted grey-green botanical sprig on EACH ivory panel (2 total); single central stem, alternating oblique leaf strokes; pale ochre short bottom border. No repeated floral diamonds.',
        'count':2,'left_bbox':[230,340,248,371],'right_bbox':[291,302,306,345],
        'visible_branch_pairs':{'left':4,'right':6},'count_uncertainty':'~1 branch at 512px: left upper stem obscured by mace; do not reconstruct hidden pattern.',
        'vertical_spacing_px':{'left':[4,6],'right':[5,7]},'motif_centre_separation_px':[60,-31],
        'source_rule':'Use anchor crop pixels, not newly invented leaves. Left partial occlusion remains legitimate.', 'colour_sample':palette['embroidery']},
      'tassels':{'description':'Short irregular pale fringe strands at each stole end, plus ONE long knotted waist cord end; fringe is not the waist cord.',
        'left_visible_tips':10,'right_visible_tips':8,'tip_count_uncertainty':1,'left_length_px':[4,9],'right_length_px':[4,9],
        'left_attachment':[222,374,254,380],'right_attachment':[288,347,310,357],
        'waist_cord_bbox':[256,251,270,346],'colour':palette['ivory_mid']['hex'],
        'rule':'Preserve sampled anchor edge, including uneven tips; no uniform extra 20px fringe.'},
      'cuffs':{'description':'Ivory undersleeves flare from short teal sleeves, narrow near wrist; dark interior crease, continuous arm/hand junction.',
        'idle_weapon_side_bbox':[156,232,204,281],'idle_free_side_bbox':[297,214,332,259]},
      'hem':{'description':'Continuous ivory inner bell with several long shaded pleats beneath teal split panels; no detached triangles.',
        'idle_outline_points':[[178,366],[173,391],[178,405],[194,414],[236,422],[269,417],[307,391]],
        'layers':2,'source_disagreement':'recover inner hem bottom ~2px lower and right shoe ~10px lower; retain idle as proportion standard, allow recover endpoint as immutable.'},
      'bag':{'count':1,'idle_bbox':[183,249,243,324],'description':'One brown flap satchel at screen-left hip with a single pale rolled cloth under flap; roll is not a second pouch.'},
      'belt':{'idle_bbox':[198,236,281,266],'description':'Brown belt with pale rope knot screen-right of centre; small bronze round medallion above belt at [265,214].'},
      'shoes':{'description':'Two worn brown rounded ankle boots, dark seams and laces; both visibly join legs under inner robe.',
        'idle_left_ground':[201,462],'idle_right_ground':[312,414],'recover_left_ground':[198,463],'recover_right_ground':[311,425],
        'pivot_note':'[256,464] is the unchanged actor registration origin, NOT the centre of each shoe; two feet cannot both occupy one pivot.'}}
    mace={'canon':'APPROVED short one-handed flanged mace; no canon edit.',
      'idle_head_bbox':[211,310,248,346],'idle_head_centre':[230,328],'idle_grip':[185,297],
      'recover_head_centre':[223,333],'recover_grip':[183,299],
      'idle_grip_to_head_px':round(math.dist([185,297],[230,328]),3),
      'exposed_haft_px':39,'head_size_px':[37,36],'collar_width_px':7,'grip_width_px':17,
      'shape':'Angular dark iron flanged star head with projecting triangular fins, worn oak haft, small brass collar before head; rounded pommel.',
      'projection_limit':'Lengths are anchor projections, not a 3D length. Preserve each A6 pose weapon/grip geometry where projected length differs; no global length invention.',
      'colours':{k:palette[k]['hex'] for k in ['oak','iron','brass']}}
    proportions={'head_height_px':70,'shoulder_width_px':99,'torso_length_px':104,'leg_and_skirt_to_ground_px':204,
      'character_height_from_pivot_px':361,'head_top_y':103,'shoulder_y':156,'hip_y':260,'ground_y':464,
      'measurement_limit':'Manual anatomical estimates +/-2px (shoulders/hips under cloth +/-5px); anchor face/hair crop is exact pixel evidence.',
      'recover_head_top_y':93,'recover_character_height_px':371,'policy':'idle proportions preferred; recover is immutable 10px taller, do not pretend anchors agree.'}
    arc_heads=[[192,85],[259,87],[449,110],[455,196],[421,376]]
    # A single C1 piecewise cubic Hermite stroke through the five target heads.
    tangents=[[67,2],[128.5,12.5],[98,54.5],[-14,133],[-34,180]]
    targets={}
    bodies=[
      [[260,143],[269,141],[281,143],[211,174],[290,172],[140,174],[331,230],[127,117],[358,249],[237,270],[279,269],[201,365],[289,371],[145,464],[342,439],[127,117]],
      [[260,141],[269,139],[281,141],[215,171],[287,174],[174,140],[299,225],[194,109],[295,249],[238,269],[277,268],[214,363],[284,371],[167,464],[326,443],[194,109]],
      [[282,145],[291,143],[302,145],[234,174],[302,173],[306,193],[319,242],[372,160],[350,266],[254,275],[293,274],[213,371],[307,376],[135,464],[372,448],[372,160]],
      [[264,140],[274,138],[284,140],[226,173],[291,172],[294,193],[291,240],[358,196],[305,258],[241,275],[281,272],[197,371],[297,378],[120,464],[354,447],[358,196]],
      [[310,141],[318,139],[329,141],[269,181],[320,178],[320,269],[231,236],[347,324],[213,255],[265,279],[304,282],[230,371],[322,384],[165,455],[334,464],[347,324]]]
    keys=['head_centre','eye_near','eye_far','shoulder_left','shoulder_right','elbow_left','elbow_right','hand_weapon','hand_free','hip_left','hip_right','knee_left','knee_right','foot_left','foot_right','mace_grip']
    for i,row in enumerate(bodies):
      targets[f'{i:02}']={'intent':['anticipation','raise','swing (smear hidden under Reduced Motion)','contact','follow-through'][i],
        'landmarks':dict(zip(keys,row)), 'pivot':[256,464],'landmark_tolerance_px':4,
        'mace_geometry_rule':'A6 projected head/haft/grip lengths retained; pose correction must move connected arm/weapon together.'}
      targets[f'{i:02}']['landmarks']['mace_head']=arc_heads[i]
    arc={'type':'single C1 piecewise cubic Hermite swing arc, not an invented circular shoulder joint',
      'knots':arc_heads,'tangents':tangents,'parameter':'frame key 0..4; actual playback uses unchanged manifest holds',
      'contact':[455,196],'follow_through_a6':[420.72,357.384],'follow_through_target':[421,376],
      'correction_px':[0.28,18.616], 'limits':'Pose intent is design, not appearance measurement; target vs actual must be reported. Final recovery retracts weapon to anchor.'}
    spec={'version':1,'segment':'spike-02 A7','authority':'Anchor pixel observations and model-defined pose targets; NOT Owner art approval.',
      'appearance_sources':[{'path':'shared-anim/'+p,'sha256':sha(SHARED/p)} for p in ANCHORS.values()],
      'measurement_convention':'512x512 source pixels, top-left origin, half-open crop rectangles; manual estimates with stated ambiguity.',
      'anchor_choice':'idle/01 appearance master; recover05 corroborates brush/materials, but 10px taller head and ~7px higher right sprig are documented disagreements.',
      'face':face,'hair':hair,'costume':costume,'mace':mace,'body_proportions':proportions,'palette':palette,
      'outline_brush':{'description':'Thin broken dark brown/teal contour, 1-2px most boundaries and up to 3px under sleeve/bag; mottled hand-painted low-contrast highlights, no black vector edge.', 'outline_sample':palette['outline'], 'normalization':'Uniform scale/translate only. Any anchor-region touch-up separately recorded with masks; no whole-body warp.'},
      'pose_targets':targets,'swing_arc':arc,'canvas':[512,512],'pivot':[256,464]}
    write(SHARED/'thoma-appearance-spec.json',spec)
    crops=[]
    sheet=Image.new('RGB',(1280,120+len(BOXES)*530),(34,40,38));d=ImageDraw.Draw(sheet)
    d.text((12,10),'A7 APPEARANCE SOURCE: idle/01 and swing/05 ONLY. Native 1x + labelled 2x nearest crop.',fill='white')
    for j,(name,boxes) in enumerate(BOXES.items()):
      y=55+j*530;d.text((12,y),name,fill='#dfc28f')
      for i,(label,p) in enumerate(ANCHORS.items()):
        box=boxes[i];crop=images[i].crop(box);x=10+i*640
        sheet.paste(crop,(x,y+30),crop)
        z=crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST)
        sheet.paste(z,(x+190,y+30),z)
        d.text((x,y+515),f'{label} box={box}; left 1x / right 2x',fill='white')
        crops.append({'item':name,'source':'shared-anim/'+p,'sha256':sha(SHARED/p),'box':box,'native_scale':1,'enlargement_scale':2})
    sheet.save(OUT/'spec-crops.png',optimize=True);write(OUT/'spec-crops.json',crops)
    overlay=Image.new('RGB',(5*512,590),(34,40,38));d=ImageDraw.Draw(overlay)
    curve=[]
    for i in range(4):
      for step in range(31):
        t=step/30; h00=2*t**3-3*t*t+1;h10=t**3-2*t*t+t;h01=-2*t**3+3*t*t;h11=t**3-t*t
        curve.append(tuple(sum([h00*arc_heads[i][axis],h10*tangents[i][axis],h01*arc_heads[i+1][axis],h11*tangents[i+1][axis]]) for axis in [0,1]))
    for i,(index,target) in enumerate(targets.items()):
      x=i*512;im=images[0].copy();im.putalpha(im.getchannel('A').point(lambda v:v//3));overlay.paste(im,(x,35),im)
      d.text((x+8,8),f'swing/{index} TARGETS (ghost is immutable idle)',fill='white')
      d.line([(x+a,35+b) for a,b in curve],fill='#dfb16e',width=2)
      lm=target['landmarks']
      for a,b in [('shoulder_left','elbow_left'),('elbow_left','hand_weapon'),('shoulder_right','elbow_right'),('elbow_right','hand_free'),('hip_left','knee_left'),('knee_left','foot_left'),('hip_right','knee_right'),('knee_right','foot_right'),('mace_grip','mace_head')]:
        d.line([(x+lm[a][0],35+lm[a][1]),(x+lm[b][0],35+lm[b][1])],fill='#8cb7b0',width=2)
      for name,(a,b) in lm.items():
        d.ellipse((x+a-3,35+b-3,x+a+3,35+b+3),fill='#f6dfab');d.text((x+a+4,35+b),name,fill='white')
      d.line((x+246,499,x+266,499),fill='#ff8678',width=2);d.line((x+256,489,x+256,509),fill='#ff8678',width=2)
      d.text((x+8,550),'pivot [256,464]; contact03 [455,196]; all positions are targets',fill='white')
    overlay.save(OUT/'pose-targets.png',optimize=True)
    text=['# Thoma unified appearance spec — spike-02 A7','',spec['authority'],'',
      'Only the two immutable PNGs below determine appearance. All numbers refer to source pixels. Manual anatomy ±2px (cloth-hidden joints ±5px); visible fringe/branch counts ±1. Crop pixels take precedence over a verbal count. No hidden design is invented.',
      '',*[f"- `{r['path']}` — SHA-256 `{r['sha256']}`" for r in spec['appearance_sources']], '',
      spec['anchor_choice'],'','[Annotated per-item crops](../godot-spike/docs/evidence/spike02-a7/spec-crops.png) · [crop rectangles](../godot-spike/docs/evidence/spike02-a7/spec-crops.json) · [pose overlay](../godot-spike/docs/evidence/spike02-a7/pose-targets.png)','']
    for title,key in [('Face','face'),('Hair','hair'),('Costume (every element)','costume'),('Mace','mace'),('Body proportions','body_proportions'),('Outline and brush','outline_brush')]:
      text += ['## '+title,'','```json',json.dumps(spec[key],ensure_ascii=False,indent=2),'```','']
    text+=['## Sampled palette','','| Region | Hex | idle/01 pixel |','| --- | --- | --- |']
    text += [f"| {k} | {v['hex']} | {v['sample_xy']} |" for k,v in palette.items()]
    text += ['','These are actual individual pixel samples, not uniform paint fills or a new palette. Pixel grain/shading is part of the anchor appearance.','',
      '## Pose targets and single arc','', 'Pose targets are proposed motion controls, not measured appearance. A6 pose intent is retained. A single C1 cubic Hermite path goes through all five head targets; it is not asserted to be a rigid circular shoulder trajectory. 03 is exactly [455,196]. 04 targets [421,376], down 18.616px from A6 [420.72,357.384]. The per-frame JSON includes eyes, shoulders, elbows, hands, hips, knees, both feet, grip and head.','',
      'The actor pivot stays [256,464]. It is the registration origin; each shoe has its own source-pixel position. At least one foot meets the ground line. Recovery is the immutable endpoint and retracts the weapon. Targets are checked against actual measured results, with failures retained.','',
      '| Frame | Head centre | Weapon hand | Mace head | Feet |','| --- | --- | --- | --- | --- |']
    text += [f"| {k} | {v['landmarks']['head_centre']} | {v['landmarks']['hand_weapon']} | {v['landmarks']['mace_head']} | {v['landmarks']['foot_left']} / {v['landmarks']['foot_right']} |" for k,v in targets.items()]
    (SHARED/'thoma-appearance-spec.md').write_text('\n'.join(text)+'\n',encoding='utf-8',newline='\n')
    print('A7_W1 anchors=2 spec_sections=face,hair,costume,mace,body_proportions,palette,outline_brush pose_targets=5')

if __name__=='__main__': main()
