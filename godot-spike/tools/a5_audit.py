"""Record explicit model observations after examining the seven-frame strip."""
from a5_style_check import *

DETAIL={
 '00':{'stole':'raised shoulder band still meets the retained sleeve abruptly',
       'cuffs':'raised cuff fold direction still changes at the sleeve edge',
       'hem':'left connection is wider, but far boot remains separated from cloth',
       'seams':'horizontal plain-cloth repair edge under satchel remains visible',
       'feet':'right boot remains detached; left planted sole unchanged'},
 '01':{'stole':'upper shoulder band still exposes a layered cutout join',
       'cuffs':'raised cuff still reads as an inserted reference patch',
       'hem':'underskirt eases toward left ankle but far-leg cloth transition remains abrupt',
       'seams':'waist/body and bag-bottom cloth transition retain brightness steps',
       'feet':'hem-to-boot transition remains narrow and not anatomically continuous'},
 '02':{'stole':'retained upper shoulder still has a squared patch boundary',
       'cuffs':'offhand cuff has a sharp triangular transition and floating edge',
       'hem':'lower sweep is continuous reference cloth but changes width abruptly from raised pose',
       'seams':'shoulder/torso and plain-cloth bag repair edges remain visible',
       'feet':'far boot has an exposed gap above its upper edge; fixed soles alone do not prove attachment'},
 '03':{'stole':'contact shoulder and waist layering still break the fold direction',
       'cuffs':'primary cuff retains a separate edge against extended sleeve',
       'hem':'left ankle now meets cloth, but right upper boot/underskirt join remains disconnected',
       'seams':'plain-cloth patch ends in a horizontal bag-bottom seam; shoulder seam still reads',
       'feet':'left contact improved; right leg-to-boot gap and boot overlap still fail'},
 '04':{'stole':'torso twist still has a hard upper-band/body junction',
       'cuffs':'front cuff fold orientation still differs from retained sleeve',
       'hem':'trailing drape still jumps to the compact unwarped recover silhouette',
       'seams':'twisted sleeve/body and bag-bottom cloth repair remain apparent',
       'feet':'trailing boot/hem overlap and far-leg gap remain; no continuous leg anatomy'},
}

def main():
    audit=json.loads((SHARED/'frame-audit.json').read_text(encoding='utf-8-sig'))
    provenance=json.loads((SHARED/'a5-swing-prompts.json').read_text())
    bypath={r['frame']:r for r in provenance}
    lines=['| Frame | Status | Stole | Embroidery | Cuffs | Hem | Face/hair | Palette | Seams | Bag count | Feet | Sequence | Reason |',
           '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for path in PATHS:
        r=next(r for r in audit if r['path']==path);moving=path in bypath
        if moving:
            detail=DETAIL[path[-6:-4]]
            reviews={k:'FAIL: '+detail[k]+'.' for k in detail}
            reviews.update(embroidery='PASS: same source sprig row; horizontal local scale 1.0, no new motifs.',
                face_hair='PASS: exact A4 reference-derived face/hair pixels protected after seam smoothing.',
                palette='PASS: original muted teal/ivory/brown retained; no remapping or visible colour-family flicker.',
                bag_count='PASS: exactly one reference satchel; no bag pixels used as occlusion fill.',
                sequence='FAIL: sleeve/shoulder folds and hem/boot outline still pop in neighbouring poses.')
            reason='Single bag and unit motif scale fixed; '+detail['seams']+'; '+detail['feet']+'.'
            r.update(source='A4 reference rig refinement; recover body, original pose arms and protected A4 geometry',
                raw_sha256=None,palette_distance=bypath[path]['palette_distance'],cleanup=bypath[path]['cleanup'])
        else:
            reviews={k:'PASS: immutable reference endpoint; byte-identical to A4.' for k in CHECKS}
            reviews['bag_count']='PASS: one original reference satchel.'
            reviews['sequence']='PASS: immutable endpoint retained; adjacent transition FAIL assigned to motion frames.'
            reason='Byte-unchanged reference endpoint; adjacent transition failures are assigned to motion frames; not Owner art approval.'
        r.update(sha256=sha(SHARED/path),status='PLACEHOLDER' if moving else 'PASS',region_review=reviews,
            review_segment='spike-02 A5',review_authority='model inspection only; not Owner art approval or human playtest',
            bag_count=1,bag_count_authority='model count in full-size frame and bag crop',reason=reason)
        r['style_review']={
            'face':reviews['face_hair'],'stole_cape_embroidery':reviews['stole'],'cuffs':reviews['cuffs'],
            'hem_silhouette':reviews['hem'],'palette':reviews['palette'],'proportions':'PASS: fixed canvas/pivot; exact protected mace/hand/feet.',
            'light_direction':'PASS: reference top-left light retained.','stroke':reviews['seams'],
            'satchel_medallion':reviews['bag_count']+' '+reviews['seams']}
        flags=[reviews[k].split(':')[0] for k in CHECKS];flags[7]=str(r['bag_count'])+' '+flags[7]
        lines.append('| `'+path+'` | '+r['status']+' | '+' | '.join(flags)+' | '+reason+' |')
    write(SHARED/'frame-audit.json',audit)
    (OUT/'frame-status-table.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    source=(SHARED/'SOURCES.md').read_text(encoding='utf-8-sig').split('\n## spike-02 A5')[0]
    source+='''
## spike-02 A5 — deterministic seam and foot repair

Tool: offline Pillow 12.2.0, godot-spike/tools/prepare_a5_frames.py. Uses the
unmodified A4 reference cutout helpers/pose controls. Zero AI calls (0/3 per
frame), prompt/raw=null, no rejected AI output. Full source, reference, mask
and runtime SHA-256 records: a5-swing-prompts.json. No original PNGs moved or
edited. Both immutable references match A4 hashes. A4 frames archived as byte
copies in godot-spike/docs/evidence/spike02-a5/baseline-a4/ with hashes.json.

One continuous recover body replaces A4 bag-bearing clone patches. Two plain
cloth source/target quads remove the reference mace occlusion; no bag pixels
or motifs are cloned. Final mask-limited 0.75px smoothing, upper silhouette
retention, unit embroidery scale and below-motif hem mesh are reproducible.
Mace, grip, head/face and feet are protected raw A4 bytes. Palette is unmapped.
Coordinates/width/area/hashes: seam-masks/coordinates.json and rig-controls.json
under the A5 evidence folder. The first W2 inspection found a surviving
reference mace-head fragment; W3 corrected its occlusion support and protected
face pixels. W1 proof remains the original draft, not silently regenerated.

| Frame | Runtime SHA-256 | Mask SHA-256 | Palette distance A4 / A5 |
| --- | --- | --- | --- |
'''
    for r in provenance:
        source+=f"| {r['frame']} | {r['runtime_sha256']} | {r['mask_sha256']} | {r['palette_distance']['before']} / {r['palette_distance']['after']} |\n"
    source+='''
### A5 model verdict

Single-bag count and unit local motif scale pass. Shoulder/waist/cuff folds,
plain-cloth repair boundary and hem-to-boot/sequence continuity still fail.
All five motion frames remain PLACEHOLDER; two unchanged reference endpoints
retain PASS. Per-check reasons in frame-audit.json, same-scale crops in A5
region-check.png and six pair proxies in sequence-check.json. No Owner or
commercial art approval. Human hit-feel remains HUMAN_PENDING.
'''
    (SHARED/'SOURCES.md').write_text(source,encoding='utf-8',newline='\n')
    print('A5_AUDIT motion_placeholder=5 reference_pass=2 bags_per_frame=1 sequence_pairs_fail=6')

if __name__=='__main__':main()
