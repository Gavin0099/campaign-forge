"""Second local 04 attempt; retain failed first attempt including duplicate mace."""
from prepare_a7_frames import *

folder=OUT/'attempts/04'
first=load(folder/'attempt-1.json')
assert not (folder/'attempt-2.png').exists(), 'Do not overwrite an attempt'
before_path=folder/'touchup-03-output.png'
before=Image.open(before_path).convert('RGBA')
mask=Image.new('L',(512,512))
poly=[(324,280),(358,291),(461,335),(466,404),(391,405),(345,350),(326,331)]
ImageDraw.Draw(mask).polygon(poly,fill=255)
patch=before.copy();patch.putalpha(ImageChops.multiply(before.getchannel('A'),mask))
result=before.copy();result.putalpha(ImageChops.subtract(before.getchannel('A'),patch.getchannel('A')))
result.alpha_composite(patch,(0,19))
# A source-cloth-only inward bridge, not the old hand/haft. This avoids the
# first attempt's erroneous overlay of original weapon pixels at the join.
cloth=Image.new('RGBA',(512,512));cloth.alpha_composite(before,(14,24))
join=Image.new('L',(512,512));join_poly=[(318,282),(331,285),(342,300),(333,311),(318,298)]
ImageDraw.Draw(join).polygon(join_poly,fill=255);join=join.filter(ImageFilter.GaussianBlur(1.5))
result=Image.composite(cloth,result,join)
dest=folder/'attempt-2.png';result.save(dest,optimize=True)
mask_path=folder/'attempt-2-weapon-mask.png';mask.save(mask_path,optimize=True)
join_path=folder/'attempt-2-join-mask.png';join.save(join_path,optimize=True)
shutil.copyfile(dest,SHARED/'thoma/swing/04.png')
first.update(adopted=False,placeholder=True,reason='REJECTED local result: first extraction mask omitted part of original head/haft, causing a duplicate mace. Preserved, superseded by local attempt2.')
write(folder/'attempt-1.json',first)
row={**first,'attempt':2,'tool':'Pillow authorized targeted touch-up','mode':'local correction of attempted weapon extraction, no new generation',
  'prompt':'Correct failed 04 attempt1 duplicate weapon: start from saved pre-weapon touchup03, extract ALL connected hand/weapon pixels using larger polygon, translate exactly [0,19], bridge cuff with cloth-only A6 patch. No weapon scale/rotation or new paint design.',
  'settings':{'seed':'not applicable; deterministic','model':'not applicable','transparent_background':True,'canvas':[512,512]},
  'references':first['references']+[{'path':before_path.relative_to(ROOT).as_posix(),'sha256':sha(before_path),'role':'pre-weapon A7 touchup source'}],
  'raw':dest.relative_to(ROOT).as_posix(),'raw_sha256':sha(dest),'runtime':dest.relative_to(ROOT).as_posix(),'runtime_sha256':sha(dest),
  'adopted':True,'generated_pixels_adopted':False,'origin_imagegen_raw':first['raw'],'origin_imagegen_raw_sha256':first['raw_sha256'],
  'reason':'Single mace restored and 04 head lowered19px. Cloth bridge/face/stole continuity remains unproven: PLACEHOLDER.',
  'touchups':first['touchups'][:3]+[{'name':'corrected complete connected weapon translation','input':before_path.relative_to(ROOT).as_posix(),'input_sha256':sha(before_path),
    'output':dest.relative_to(ROOT).as_posix(),'output_sha256':sha(dest),'mask':mask_path.relative_to(ROOT).as_posix(),'mask_sha256':sha(mask_path),
    'join_mask':join_path.relative_to(ROOT).as_posix(),'join_mask_sha256':sha(join_path),'details':{'source_polygon':poly,'translate':[0,19],'scale':1,'cuff_cloth_translate':[14,24],'cuff_polygon':join_poly,'feather_px':1.5}}]}
write(folder/'attempt-2.json',row)
rows=load(SHARED/'a7-swing-prompts.json')
rows=[first if r['frame']==first['frame'] and r['attempt']==1 else r for r in rows];rows.append(row)
write(SHARED/'a7-swing-prompts.json',rows)
with (SHARED/'SOURCES.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n\n### A7 swing/04 attempt2 — local duplicate-weapon correction\n\nAttempt1 runtime is REJECTED, not live. Historical record above is superseded by this attempt and a7-swing-prompts.json.\n\n'+json.dumps(row,ensure_ascii=False,indent=2)+'\n')
print('A7_04_ATTEMPT2 runtime',sha(dest),'mace_translate=[0,19] no_rescale=true PLACEHOLDER')
