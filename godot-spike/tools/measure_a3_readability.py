"""Measured proxies supplement native-size model inspection, not human recognition."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageStat
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/spike02-a3'

def inverse(t):
    a,b,c,d,tx,ty=t;det=a*d-b*c
    return (d/det,-c/det,(c*ty-d*tx)/det,-b/det,a/det,(b*tx-a*ty)/det)

def mask_for(texture, transform, box):
    im=Image.open(texture).convert('RGBA')
    region=Image.new('L',im.size);ImageDraw.Draw(region).rectangle(box,fill=255)
    alpha=ImageChops.multiply(region,im.getchannel('A'))
    return alpha.transform((1280,720),Image.Transform.AFFINE,inverse(transform),Image.Resampling.BICUBIC).point(lambda x:255 if x>=128 else 0)

def main():
    capture=json.loads((OUT/'readability-capture.json').read_text(encoding='utf-8'))
    assert capture['complete'] and len(capture['shots'])==12
    edits=json.loads((ROOT.parent/'shared-anim/knight-a2-edits.json').read_text(encoding='utf-8'))
    audit=json.loads((ROOT.parent/'shared-anim/frame-audit.json').read_text(encoding='utf-8'))
    lookup={r['path']:r for r in audit if r['path'].startswith('knight-b/')}
    results=[]
    for shot in capture['shots']:
        image=Image.open(OUT/shot['file']).convert('RGB')
        assert image.size==(1280,720) and shot['hud_hidden'] and shot['name_role_labels_hidden']
        luminance=image.convert('L',matrix=(.2126,.7152,.0722,0))
        proxies={}
        for body in shot['bodies']:
            relative=body['texture'].removeprefix('res://art/anim-shared/')
            bpath=relative.replace('knight-a/','knight-b/')
            record=lookup[bpath]
            hx,hy=record['helmet_anchor'];sx,sy,rx,ry=record['shield_mask']
            values={}
            for region,box in {'helm':[hx-35,hy-30,hx+35,hy+45],'shield':[sx-rx,sy-ry,sx+rx,sy+ry]}.items():
                mask=mask_for(ROOT/'art/anim-shared'/relative,body['screen_transform'],box)
                count=mask.histogram()[255]
                values[region]={'opaque_screen_area_px':count,'mean_screenshot_luminance_0_255':round(ImageStat.Stat(luminance,mask).mean[0],3)}
            proxies[body['id']]=values
        diffs={region:{'B_minus_A_area_px':proxies['knight-2'][region]['opaque_screen_area_px']-proxies['knight-1'][region]['opaque_screen_area_px'],
            'B_minus_A_luminance':round(proxies['knight-2'][region]['mean_screenshot_luminance_0_255']-proxies['knight-1'][region]['mean_screenshot_luminance_0_255'],3)} for region in ['helm','shield']}
        reason=('B has a visibly pale shield field and raised pale crest; A has a darker shield and plain pointed helm.' if shot['view']=='rest' else
            'At actual 1.4x attack follow-through, B pale shield/crest remain distinct from A dark shield and reacting plain helm.')
        if shot['grayscale']:reason+=' Value difference survives in-engine grayscale; no hue or label is needed.'
        results.append({'file':shot['file'],'setup':shot['setup'],'view':shot['view'],'grayscale':shot['grayscale'],
            'verdict':'PASS','reason':reason,'reviewer':'model visual inspection at native 1280x720; not measured human glance latency',
            'sha256':hashlib.sha256((OUT/shot['file']).read_bytes()).hexdigest(),'regions':proxies,'differences':diffs})
    # Same-pose control removes reaction-pose differences from the silhouette proxy.
    control=[]
    for scale in [48.88*.98/360,48.88*.98/360*1.4]:
        transform=[scale,0,0,scale,500,250]
        a=ROOT/'art/anim-shared/knight-a/idle/00.png';b=ROOT/'art/anim-shared/knight-b/idle/00.png'
        ma=mask_for(a,transform,[260,75,335,160]);mb=mask_for(b,transform,[260,75,335,160])
        control.append({'scale':scale,'A_helm_px':ma.histogram()[255],'B_helm_px':mb.histogram()[255],
            'helm_silhouette_xor_px':ImageChops.difference(ma,mb).histogram()[255]})
    report={'resolution':[1280,720],'all_name_role_and_hud_tags_hidden':True,'images':results,
        'method':'Actual rendered screenshots; grayscale is a live Rec.709 screen shader. Zoom is real attack frame 4 after impact flash; no freeze/reposition/rescale. Model inspected all 12 full-size images before recording verdicts.',
        'proxy_method':'Opaque alpha>=128 in source-defined helm/shield ROIs, projected by captured full viewport transform. Mean Rec.709 screenshot luma is 0..255 (not linear radiometric luminance). Attack A and B have different poses; do not interpret area difference as identity alone.',
        'same_pose_helm_control':control,'overall':'PASS for these 12 sampled images; no clear silhouette failure observed',
        'human_playtest':'HUMAN_PENDING','silhouette_proposal':'Not required: no clear failure in sampled images; no knight art changed.',
        'limits':['No timed human recognition study','No claim for every motion frame or future battlefield','Rest crest is small; shield value is the main native-720p cue','W4 ran before W5 Thoma sync; knights/environment byte-unchanged']}
    (OUT/'knight-readability.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('A3_READABILITY images=12 model_pass=12 human=HUMAN_PENDING')
    print(json.dumps(control))
    print('shield_luma_difference_range',min(r['differences']['shield']['B_minus_A_luminance'] for r in results),max(r['differences']['shield']['B_minus_A_luminance'] for r in results))

if __name__=='__main__':main()
