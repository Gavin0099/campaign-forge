"""Actual native720p movie RGB under W1 region masks; source IoU labelled."""
from a9_style_check import *
from package_a3_evidence import chunks
from PIL import ImageStat, ImageChops
from io import BytesIO

def main():
    avi=ROOT/'godot-spike/.godot/spike02-a9-movie/attack.avi';data=avi.read_bytes()
    frames=[Image.open(BytesIO(v)).convert('RGB') for k,v in chunks(data,12,len(data)) if k in [b'00dc',b'00db']]
    trace=load(OUT/'render-trace.json');assert [r['process_frame'] for r in trace]==list(range(len(trace)))
    assert len(frames)-len(trace) in [0,1] and frames[-1].tobytes()==frames[-2].tobytes()
    assert all(im.size==(1280,720) for im in frames)
    selected=[];samples={};means={};defs=load(OUT/'defects-and-targets.json')
    dest=OUT/'sequence-runtime';dest.mkdir(exist_ok=True)
    for path in PATHS:
        indices=[i for i,r in enumerate(trace) if r['path']==path];assert indices,path
        i=indices[len(indices)//2];tr=trace[i];im=frames[i]
        name='idle.png' if '/idle/' in path else Path(path).name;im.save(dest/name,optimize=True)
        samples[path]=(im,tr);means[path]={}
        source=Image.open(SHARED/path).convert('RGBA')
        group=defs['anchors']['idle-01' if '/idle/' in path else 'swing-05']['regions'] if path in [PATHS[0],PATHS[-1]] else defs['frames'][Path(path).stem]['masks']
        sx,sy,tx,ty=tr['body_transform'];inverse=(1/sx,0,-tx/sx,0,1/sy,-ty/sy)
        mask_records={}
        for region in REGIONS:
            mp=ROOT/group[region]['path'];mask=ImageChops.multiply(Image.open(mp).convert('L'),source.getchannel('A'))
            screen=mask.transform(im.size,Image.Transform.AFFINE,inverse,Image.Resampling.NEAREST)
            assert screen.getbbox(),(path,region)
            means[path][region]=ImageStat.Stat(im,screen).mean
            mask_records[region]={'source_mask':rel(mp),'source_mask_sha256':sha(mp),'viewport_bbox':screen.getbbox(),'mean_rendered_rgb':means[path][region]}
        selected.append({'path':path,'movie_frame':i,'file':'sequence-runtime/'+name,'decoded_rgb_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'trace':tr,'region_masks':mask_records})
    film=Image.new('RGB',(3200,350*math.ceil(len(frames)/10)),(34,40,38));draw=ImageDraw.Draw(film)
    for i,im in enumerate(frames):
        x=i%10*320;y=i//10*350;film.paste(im.crop((260,160,580,480)),(x,y+25))
        draw.text((x+4,y+4),str(i)+' '+(trace[i]['path'] if i<len(trace) else 'identical terminal'),fill='white')
    film.save(OUT/'playback-every-frame.png',optimize=True)
    key=Image.new('RGB',(2240,390),(34,40,38));draw=ImageDraw.Draw(key)
    for i,r in enumerate(selected):
        key.paste(frames[r['movie_frame']].crop((260,160,580,480)),(i*320,35));draw.text((i*320+4,8),r['path'],fill='white')
    draw.text((8,365),'A9 real native720p crops; source defects remain; MODEL review, HUMAN_PENDING.',fill='white');key.save(OUT/'playback-keyframes.png',optimize=True)
    measured=load(OUT/'landmark-deltas.json')['measured'];pairs=[]
    for a,b in zip(PATHS,PATHS[1:]):
        masks=[Image.open(SHARED/p).getchannel('A').crop((100,275,420,440)).point(lambda x:255 if x>127 else 0) for p in [a,b]]
        inter=sum(v>0 for v in ImageChops.darker(*masks).getdata());union=sum(v>0 for v in ImageChops.lighter(*masks).getdata())
        pairs.append({'from':a,'to':b,'region_mean_rgb_delta':{r:round(math.dist(means[a][r],means[b][r]),5) for r in REGIONS},
          'garment_silhouette_iou':round(inter/union,6),'iou_source':'registered SOURCE alpha garment ROI (100,275)-(420,440), not segmentation of actual rendered RGB',
          'character_height_delta_px':measured[b]['character_height_px']-measured[a]['character_height_px'],
          'result':'FAIL','reason':'Mixed head01 identity, broad retained cloth and A8 stance/feet jumps; proxy values do not establish no flicker.'})
    write(OUT/'sequence-check.json',{'pairs':pairs,'authority':'RGB differences measured from actual Godot movie pixels under transformed W1 masks; source silhouette separately labelled'})
    write(OUT/'playback-check.json',{'capture_complete':load(OUT/'movie-timing.json')['complete'],'source_movie_sha256':sha(avi),'fps':60,'frames':len(frames),'traced_frames':len(trace),
      'untraced_terminal_frames':len(frames)-len(trace),'terminal_pixels_equal_previous_ready':True,'selected':selected,'pairs':pairs,'result':'FAIL',
      'observations':{'face_hair':'Improved source identity on4 poses;01 retains A8, full transition FAIL.','cloth':'Stole/motifs/fringe unchanged; broad endpoints still jump.','mace':'00/01 uncompressed donor shape improves but grip/lighting seam visible at512px.','feet':'Connected/grounded;03 stance and04 placement remain A8 defects.'},
      'authority':'Model inspection of actual consecutive rendered frames; HUMAN_PENDING; not Owner art approval',
      'limits':'Region mask can include antialiasing/background, transient flash and camera interpolation; source IoU is not rendered segmentation; source heights are anatomical estimates. RGB proxies cannot prove absence of flicker.'})
    print(f'A9_PLAYBACK frames={len(frames)} keyposes={len(selected)} adjacent_pairs={len(pairs)} result=FAIL')

if __name__=='__main__':main()
