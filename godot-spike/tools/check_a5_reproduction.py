"""Read-only reconstruction, protection, baseline and seam paint support checks."""
from prepare_a5_frames import *

def main():
    records=json.loads((SHARED/'a5-swing-prompts.json').read_text())
    ground=[]
    for r in records:
        index=r['frame'][-6:-4]
        old=Image.open(BASE/f'{index}.png').convert('RGBA')
        rebuilt,protected=build(index,old)
        buffer=BytesIO();rebuilt.save(buffer,format='PNG',optimize=True)
        assert hashlib.sha256(buffer.getvalue()).hexdigest()==sha(SHARED/r['frame'])==r['runtime_sha256']
        assert protected.tobytes()==Image.open(OUT/f'protected-masks/{index}.png').tobytes()
        seam,joins=bands(index)
        assert seam.tobytes()==Image.open(OUT/f'seam-masks/{index}.png').tobytes()
        # Detect baseline shadow / raster overshoot honestly, rather than
        # equating an unchanged pivot with a new ground-contact quality PASS.
        def below(im):
            return sum(im.getpixel((x,y))[3]>127 for y in range(465,512) for x in range(512))
        ground.append({'frame':index,'a4_opaque_pixels_below_pivot_y464':below(old),
            'a5_opaque_pixels_below_pivot_y464':below(rebuilt),
            'interpretation':'fixed A4 sole pixels retained; any inherited raster overshoot is a feet FAIL, not excused by pivot equality'})
        for path in a4.REFS.values():assert r['references'][path]==sha(SHARED/path)
    # Do not mutate proof output: W1 is an earlier draft retained in history.
    print('A5_REPRODUCTION frames=5 identical_png_bytes=true protected_masks=true seam_masks=true references=true')
    print(json.dumps({'ground_contact_observations':ground},indent=2))

if __name__=='__main__':main()
