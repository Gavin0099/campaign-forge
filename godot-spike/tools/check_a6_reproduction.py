"""Reproduce all adopted output PNGs/masks from committed raw files and settings."""
from prepare_a6_frames import *

def main():
    target=REPO/'godot-spike/.godot/a6-reproduction';target.mkdir(parents=True,exist_ok=True)
    checked=[]
    for row in load(SHARED/'a6-swing-prompts.json'):
        assert sha(REPO/row['raw'])==row['raw_sha256']
        for ref in row['references']:assert sha(REPO/ref['path'])==ref['sha256']
        if not row['adopted']:continue
        record=row['normalization'];dest=target/row['frame'].split('/')[-1]
        result=normalize(REPO/row['raw'],record['settings'],dest)
        assert result['normalized_sha256']==row['runtime_sha256']==sha(SHARED/row['frame'])
        assert result['cleanup_mask_sha256']==record['cleanup_mask_sha256']
        assert result['palette_distance']==record['palette_distance']
        checked.append(row['frame'])
    assert len(checked)==5
    assert sha(SHARED/'thoma/idle/01.png')=='c109ac1680fbe9b93e8282cf9d2962b4dd0fb9c1e3251b6ef2c7517cc9b3a808'
    assert sha(SHARED/'thoma/swing/05.png')=='f0187ad4e82b45ac9c3495ca0c374f0aad868bc3d41be6ecfc4ebb6c13addebf'
    assert load(SHARED/'manifest.json')==load(BASE/'manifest.json')
    parity=0
    for source in SHARED.rglob('*'):
        if not source.is_file() or source.suffix in ['.import','.uid'] or any(part in ['tools','rejected','__pycache__'] for part in source.parts):continue
        assert sha(source)==sha(REPO/'godot-spike/art/anim-shared'/source.relative_to(SHARED))
        parity+=1
    write(OUT/'reproduction.json',{'reproduced_png_and_mask_count':len(checked),'shared_files_byte_equal':parity,'pass':True})
    print(f'A6_REPRODUCTION pass=true full_pngs=5 cleanup_masks=5 references_fixed=true manifest_unchanged=true parity={parity}')

if __name__=='__main__':main()
