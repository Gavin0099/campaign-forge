"""Decode real rendered frames and measure alpha-intersected screen regions."""
from a7_style_check import *
from package_a3_evidence import chunks
from io import BytesIO

def screen_proxy(frame, trace, path, box):
    # Sprite is uncentred, transform is native source pixel -> viewport pixel,
    # including reflected x scale. Alpha follows same affine into screen space.
    sx,sy,tx,ty=trace['body_transform']
    source=Image.open(SHARED/path).convert('RGBA')
    source_mask=Image.new('L',(512,512));ImageDraw.Draw(source_mask).rectangle(box,fill=255)
    source_mask=ImageChops.multiply(source_mask,source.getchannel('A'))
    affine=(1/sx,0,-tx/sx,0,1/sy,-ty/sy)
    mask=source_mask.transform(frame.size,Image.Transform.AFFINE,affine,Image.Resampling.NEAREST)
    assert mask.getbbox(),(path,box,trace)
    mean=ImageStat.Stat(frame,mask).mean
    # Registered source-grid screen silhouette is an occupancy proxy. Avoid
    # calling the source mask itself a rendered segmentation measurement.
    bounds=tuple(round(v) for v in (min(tx+sx*box[0],tx+sx*box[2]),ty+sy*box[1],max(tx+sx*box[0],tx+sx*box[2]),ty+sy*box[3]))
    return mean,mask,bounds

def main():
    avi=ROOT/'godot-spike/.godot/spike02-a7-movie/attack.avi'
    data=avi.read_bytes();frames=[Image.open(BytesIO(v)).convert('RGB') for k,v in chunks(data,12,len(data)) if k in [b'00dc',b'00db']]
    trace=load(OUT/'render-trace.json');assert [r['process_frame'] for r in trace]==list(range(len(trace)))
    assert len(frames)-len(trace) in [0,1]
    terminal_equal=frames[-1].tobytes()==frames[-2].tobytes();assert terminal_equal
    dest=OUT/'sequence-runtime';dest.mkdir(exist_ok=True)
    selected=[];samples={}
    for path in PATHS:
      indices=[i for i,r in enumerate(trace) if r['path']==path];assert indices,path
      i=indices[len(indices)//2];name='idle.png' if '/idle/' in path else path[-6:]
      frames[i].save(dest/name,optimize=True)
      samples[path]={'frame':frames[i],'trace':trace[i]}
      selected.append({'path':path,'movie_frame':i,'file':'sequence-runtime/'+name,
        'decoded_rgb_sha256':hashlib.sha256(frames[i].tobytes()).hexdigest(),'trace':trace[i]})
    key=Image.new('RGB',(2240,410),(34,40,38));d=ImageDraw.Draw(key)
    for col,r in enumerate(selected):
      key.paste(frames[r['movie_frame']].crop((260,160,580,480)),(col*320,40));d.text((col*320+4,8),r['path']+' #'+str(r['movie_frame']),fill='white')
    d.text((8,380),'Real native720p crops, no source-sprite compositing; camera moves. Full sequence FAIL, not Owner review.',fill='white');key.save(OUT/'playback-keyframes.png',optimize=True)
    film=Image.new('RGB',(3200,350*math.ceil(len(frames)/10)),(34,40,38));d=ImageDraw.Draw(film)
    for i,im in enumerate(frames):
      x=i%10*320;y=i//10*350;film.paste(im.crop((260,160,580,480)),(x,y+25))
      label=trace[i]['path']+' '+trace[i]['phase'] if i<len(trace) else 'untraced terminal, identical ready pixels'
      d.text((x+4,y+4),str(i)+' '+label,fill='white')
    film.save(OUT/'playback-every-frame.png',optimize=True)
    clips=[im.crop((260,160,580,480)) for im in frames]
    clips[0].save(OUT/'playback-crop.gif',save_all=True,append_images=clips[1:],duration=1000/60,loop=0,disposal=2)
    pairs=[];measure=load(OUT/'landmark-deltas.json')['measured']
    for a,b in zip(PATHS,PATHS[1:]):
      means={};screen_bounds={}
      for name,box in REGIONS.items():
        left,_,lb=screen_proxy(samples[a]['frame'],samples[a]['trace'],a,box)
        right,_,rb=screen_proxy(samples[b]['frame'],samples[b]['trace'],b,box)
        means[name]=round(math.dist(left,right),5);screen_bounds[name]=[lb,rb]
      # Source-grid silhouette IoU removes camera and pose translation. This is
      # a SOURCE occupancy measure; RGB above is measured from ACTUAL readbacks.
      masks=[Image.open(SHARED/p).convert('RGBA').getchannel('A').crop((100,275,420,440)).point(lambda x:255 if x>127 else 0) for p in [a,b]]
      inter=sum(v>0 for v in ImageChops.darker(*masks).getdata());union=sum(v>0 for v in ImageChops.lighter(*masks).getdata())
      pairs.append({'from':a,'to':b,'region_mean_rgb_delta':means,'runtime_mask_bounds':screen_bounds,
        'garment_silhouette_iou':round(inter/union,6),'iou_source':'source alpha in registered512px garment ROI; NOT a segmentation of rendered RGB',
        'character_height_delta_px':round(measure[b]['character_height_px']-measure[a]['character_height_px'],4),
        'visual_result':'FAIL','reason':'Remaining face/stole/hem differences and local texture joins pop between poses; proxy values cannot grant acceptance.'})
    write(OUT/'sequence-check.json',{'pairs':pairs,'authority':'actual rendered-frame RGB measured under transformed source-alpha masks; source silhouette separately labelled',
      'limits':'Masks can include antialiasing/background occlusion, camera interpolation and transient hit flash. They are measurable proxies, not proof of no flicker.'})
    checks={'face_hair':'FAIL: head outer contour and clipped edge change at texture swaps despite shared interior.',
      'embroidery_tassels':'FAIL: residual motif/edge changes persist; 02 right panel misregistration visible in source1x, not resolved by small native screen size.',
      'cuffs':'FAIL: 04 cloth bridge above shifted hand remains visible at source scale; native playback does not prove it clean.',
      'hem_outline_shoes':'FAIL: shoes remain connected, but hem breadth/stance still jumps.',
      'bag_count':'PASS: one unchanged satchel in every pose.',
      'colour_flicker':'FAIL: source palette families stable but changing surface texture/occlusion gives region RGB deltas.',
      'seams':'FAIL: local texture joins remain; source1x failures cannot be waived at720p.'}
    write(OUT/'playback-check.json',{'capture_complete':load(OUT/'movie-timing.json')['complete'],'source_movie_sha256':sha(avi),
       'fps':60,'frames':len(frames),'traced_frames':len(trace),'untraced_terminal_frames':len(frames)-len(trace),
       'terminal_pixels_equal_previous_ready':terminal_equal,'selected':selected,'observations':checks,'result':'FAIL',
       'authority':'model inspection of actual decoded consecutive frames; human hit-feel HUMAN_PENDING; Owner art approval pending',
       'limits':'GIF timing quantizes60FPS; AVI and trace are the timing authority. Small displayed sprites conceal source defects and cannot turn a failed check into PASS.'})
    print(f'A7_PLAYBACK rendered_frames={len(frames)} keyposes={len(selected)} pairs={len(pairs)} result=FAIL')

if __name__=='__main__':main()
