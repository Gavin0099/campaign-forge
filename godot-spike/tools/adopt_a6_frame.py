"""Record a generated attempt and optionally adopt a normalized full frame."""
from prepare_a6_frames import *
import sys

frame,attempt=sys.argv[1],int(sys.argv[2])
raw=OUT/f'candidates/{frame}/attempt-{attempt}.png'
rows=load(SHARED/'a6-swing-prompts.json')
row=next((r for r in rows if r['frame']==f'thoma/swing/{frame}.png' and r['attempt']==attempt),None)
if row is None:
    row={'frame':f'thoma/swing/{frame}.png','attempt':attempt,'tool':'image_gen (built-in)',
         'prompt':raw.with_suffix('.prompt.txt').read_text(encoding='utf-8'),
         'references':[{'path':p,'role':role} for p,role in [
             ('shared-anim/thoma/idle/01.png','costume/face/hair/palette/painting/mace'),
             ('shared-anim/thoma/swing/05.png','costume/face/hair/palette/painting/mace'),
             ((BASE/f'{frame}.png').relative_to(REPO).as_posix(),'A5 pose/silhouette ONLY')]],
         'settings':{'transparent_background':True,'seed':'not exposed','model':'not exposed','quality':'not exposed',
                     'requested_size':'512x512 via prompt','returned_size':list(Image.open(raw).size)},
         'raw':raw.relative_to(REPO).as_posix(),'pick':False,'adopted':False,'runtime_sha256':None}
    rows.append(row)
adopt='--adopt' in sys.argv
row['pick']=adopt;row['adopted']=adopt
row['reason']=sys.argv[sys.argv.index('--reason')+1]
if adopt:
    normalized=OUT/f'normalized/{frame}-attempt-{attempt}.png'
    shutil.copyfile(normalized,SHARED/row['frame'])
write(SHARED/'a6-swing-prompts.json',rows)
from record_a6_provenance import main
main()
