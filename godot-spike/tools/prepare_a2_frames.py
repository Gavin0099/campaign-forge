"""A2-only cleanup: original PNGs and all raw attempts remain unchanged."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json

ROOT = Path(__file__).resolve().parents[2] / 'shared-anim'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

ref=Image.open(ROOT/'references/thoma.png').convert('RGBA')
pixels=[p[:3] for p in ref.getdata() if p[3]>200]
strip=Image.new('RGB',(len(pixels),1));strip.putdata(pixels)
pal=strip.quantize(colors=128,method=Image.Quantize.MEDIANCUT)
# Manually observed foot midpoint, ground baseline, head top, intended body height.
registration={
 'thoma/idle/01.png':(665,1219,58,360),
 'thoma/swing/00.png':(685,1218,144,350),
 'thoma/swing/01.png':(665,1220,132,354),
 'thoma/swing/02.png':(575,1205,133,350),
 'thoma/swing/03.png':(545,1190,81,350),
 'thoma/swing/04.png':(607,1167,110,342),
 'thoma/swing/05.png':(673,1217,85,360),
}
entries=read('a2-generation-prompts.json')+read('a2-swing-prompts.json')+[read('a2-retry-prompt.json')]
entries[3]['accepted']=False
entries[3]['rejection']='Weapon already below waist before chest-high contact; discontinuous arc.'
entries[3]['rejected_copy']='rejected/thoma-mace-swing-02-attempt1.png'
entries[3]['raw']=entries[3]['rejected_copy']
active={e['frame']:e for e in entries if e.get('accepted',True)}
audit=[r for r in read('frame-audit.json') if not r['path'].startswith('thoma/')]
for path,e in active.items():
 im=Image.open(ROOT/e['raw']).convert('RGBA');a=im.getchannel('A').point(lambda v:0 if v<24 else v);im.putalpha(a)
 x,y,head,h=registration[path];s=h/(y-head)
 im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(512,512));out.alpha_composite(im,(round(256-x*s),round(464-y*s)))
 a=out.getchannel('A');out=out.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(a)
 out.save(ROOT/path,optimize=True)
 e['runtime_sha256']=sha(ROOT/path)
 status='PASS' if '/idle/' in path or path.endswith('05.png') else 'PLACEHOLDER'
 reason='Identity and near-idle silhouette retained at review scale; not Owner art approval.' if status=='PASS' else 'Stole embroidery, cuff folds and hem contour drift from original; motion candidate only.'
 audit.append(dict(path=path,sha256=e['runtime_sha256'],source=e['raw'],raw_sha256=sha(ROOT/e['raw']),registration=registration[path],status=status,weapon_status='PROPOSED',reason=reason,style_review={'face':'PASS: recognizable aged face and grey beard','costume':status+': '+reason,'proportions':'PASS: fixed body-height registration, natural joint poses','palette':'PASS: mapped to original 128-color palette','light':'PASS: top-left highlight direction','stroke':'PASS at runtime scale; detailed painted contours vary'}))
for e in entries:
 e['raw_sha256']=sha(ROOT/e['raw'])
 e['reference_sha256']={p:sha(ROOT/p) for p in e['references']}
 e['weapon_status']='PROPOSED; Owner confirmation pending'
 e['cleanup']='alpha <24 cleared; uniform Lanczos resize; manual feet to [256,464]; original Thoma 128-color palette, no dithering'
 e['output']=e['raw']
historical=[e for e in read('generation-prompts.json') if e.get('segment')!='spike-02 A2']
for e in entries:e['segment']='spike-02 A2'
write('generation-prompts.json',historical+entries)
write('frame-audit.json',audit)
m=read('manifest.json');m['sequences']['thoma.idle']['frames'][0]['path']='thoma/idle/01.png'
for f,d in zip(m['sequences']['thoma.swing']['frames'],[180,70,40,80,100,150]):f['duration_ms']=d
# The generated contact head center (1175,340) transformed by its registration.
for e in m['sequences']['thoma.swing']['events']:e['anchor']=[455,196]
write('manifest.json',m)

items=[('ORIGINAL (empty hands)',Image.open(ROOT/'thoma/idle/00.png'))]+[(p,Image.open(ROOT/p)) for p in sorted(active)]
sheet=Image.new('RGB',(2048,420),(34,40,38));d=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(items):
 d.text((i*256+6,8),label,fill='#eee7d6');large=im.resize((256,256),Image.Resampling.LANCZOS);sheet.paste(large,(i*256,34),large)
 small=im.resize((68,68),Image.Resampling.LANCZOS);sheet.paste(small,(i*256+94,322),small)
d.text((8,302),'720p native scale: 47.9px body; asset sheet, NOT a runtime screenshot.',fill='#eee7d6')
sheet.save(ROOT/'thoma-weapon-style-check.png',optimize=True)
contact=Image.new('RGB',(2048,900),(34,40,38));d=ImageDraw.Draw(contact)
for row,c in enumerate(m['characters']):
 paths=[f['path'] for seq in m['sequences'].values() if seq['character']==c for f in seq['frames']]
 for col,p in enumerate(paths):
  im=Image.open(ROOT/p).resize((256,256),Image.Resampling.LANCZOS);contact.paste(im,(col*256,row*300+30),im);d.text((col*256+5,row*300+8),p,fill='#eee7d6')
contact.save(ROOT/'contact-sheet.png',optimize=True)

source=(ROOT/'SOURCES.md').read_text(encoding='utf-8').split('\n## spike-02 A2')[0]
lines=['','## spike-02 A2','', '**Weapon PROPOSED — Owner confirmation pending:** short one-handed flanged mace, dark iron head, worn oak haft and brass collar. Canon names no weapon. It fits a medical friar silhouette, provides blunt impact and is too short to read as a staff. Historical Phase A sword records above are superseded, not runtime provenance for A2. Original PNGs are untouched; original empty-handed idle remains reference-only.','', 'Evidence: character-prompt.txt:1 (empty hands, no staff/book/glow); ART-DIRECTION.md:9 (medical satchel/teal); l03Scene.ts:51–54 (medical/support); DEMO-CONTRACT.md:17 (melee 3, heal 3); narrative branch STORY.md:56 and COMPANION-ARCS.md:28,34 (friar, holy medallion), ch01.ink:306 / ch02.ink:250 and CREATIVE-BIBLE.md:74; DECISIONS U003 (class frame). These are brief-cited source facts, not a new canon claim.','', 'Tool: built-in image_gen; 1 attempt each except swing 02 (2). Rejected 02 attempt 1 is archived under rejected/ because it passes below the waist before chest-high contact. No rejected output is a runtime frame. Full reproducible cleanup: godot-spike/tools/prepare_a2_frames.py. No other character, prop or battlefield generation.','']
for e in entries:
 lines += [f"### {e['frame']} attempt {e['attempt']}",f"Raw: {e['raw']} SHA-256 `{e['raw_sha256']}`",'References: '+json.dumps(e['reference_sha256']),e['prompt'],'Cleanup: '+e['cleanup'],'Runtime SHA-256: '+e.get('runtime_sha256','REJECTED (no runtime output)'), '']
lines+=['| Frame | Style verdict | SHA-256 |','| --- | --- | --- |']
for r in audit:
 if r['path'].startswith('thoma/'):lines.append(f"| {r['path']} | {r['status']}: {r['reason']} | `{r['sha256']}` |")
lines+=['','Weapon identity stays PROPOSED regardless of style PASS. Detailed frame review: frame-audit.json. Style sheet SHA-256 `'+sha(ROOT/'thoma-weapon-style-check.png')+'`. Contact sheet SHA-256 `'+sha(ROOT/'contact-sheet.png')+'`.']
(ROOT/'SOURCES.md').write_text(source+'\n'.join(lines)+'\n',encoding='utf-8')
print('A2_FRAMES 7 weapon=PROPOSED original_PNGs_unchanged=true')
