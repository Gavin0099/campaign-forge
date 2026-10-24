"""Decode actual Godot movie and match every sample to post-draw trace."""
from prepare_a6_frames import *
from package_a3_evidence import chunks
from io import BytesIO
import struct

def main():
    avi=REPO/'godot-spike/.godot/spike02-a6-movie/attack.avi';data=avi.read_bytes()
    payloads=[p for k,p in chunks(data,12,len(data)) if k in [b'00dc',b'00db']]
    frames=[Image.open(BytesIO(p)).convert('RGB') for p in payloads]
    trace=load(OUT/'render-trace.json')
    # finish() quits after the final ready draw is queued. Movie Maker emits
    # one terminal frame after the observer closes, without another callback.
    assert [r['process_frame'] for r in trace]==list(range(len(trace)))
    assert len(frames)-len(trace) in [0,1],(len(frames),len(trace))
    terminal_equal=frames[-1].tobytes()==frames[-2].tobytes()
    if len(frames)>len(trace):assert terminal_equal,'Untraced terminal image must equal preceding actual ready frame'
    dest=OUT/'sequence-runtime';dest.mkdir(exist_ok=True)
    selected=[]
    for path in ['thoma/idle/01.png']+[f'thoma/swing/{i:02}.png' for i in range(6)]:
        options=[i for i,r in enumerate(trace) if r['path']==path]
        assert options,path
        i=options[len(options)//2];name='idle.png' if '/idle/' in path else path[-6:]
        frames[i].save(dest/name,optimize=True)
        selected.append({'path':path,'movie_frame':i,'file':f'sequence-runtime/{name}',
            'decoded_rgb_sha256':hashlib.sha256(frames[i].tobytes()).hexdigest(),'trace':trace[i]})
    sheet=Image.new('RGB',(2240,400),(34,40,38));d=ImageDraw.Draw(sheet)
    for col,r in enumerate(selected):
        crop=frames[r['movie_frame']].crop((260,160,580,480));sheet.paste(crop,(col*320,40))
        d.text((col*320+5,8),r['path']+' movie#'+str(r['movie_frame']),fill='white')
    d.text((8,375),'Native rendered 720p viewport crops, same 320px box, no resampling. Camera moves during attack.',fill='white')
    sheet.save(OUT/'playback-keyframes.png',optimize=True)
    # All 59 consecutive native crops permit inspection beyond just key poses.
    film=Image.new('RGB',(320*10,350*6),(34,40,38));d=ImageDraw.Draw(film)
    for i,im in enumerate(frames):
        x=(i%10)*320;y=(i//10)*350
        film.paste(im.crop((260,160,580,480)),(x,y+25))
        caption=trace[i]['path']+' '+trace[i]['phase'] if i<len(trace) else 'untraced terminal; identical ready pixels'
        d.text((x+5,y+5),f'{i}: '+caption,fill='white')
    film.save(OUT/'playback-every-frame.png',optimize=True)
    # 60fps animated review preview generated solely from real rendered crops.
    crops=[im.crop((260,160,580,480)) for im in frames]
    crops[0].save(OUT/'playback-crop.gif',save_all=True,append_images=crops[1:],duration=1000/60,loop=0,disposal=2)
    write(OUT/'playback-check.json',{'capture_complete':load(OUT/'movie-timing.json')['complete'],
        'source_movie_sha256':sha(avi),'fps':60,'frames':len(frames),'traced_frames':len(trace),
        'untraced_terminal_frames':len(frames)-len(trace),'terminal_pixels_equal_previous_ready':terminal_equal,
        'selected':selected,'authority':'model visual inspection of decoded actual rendered sequence, not human playback acceptance',
        'observations':{'embroidery':'FAIL: fuller generated sprigs/fringe change at fixed idle/recover boundaries.',
            'cuffs':'PASS: no floating cuff fragment in new frames; bend changes follow articulated arm.',
            'hem_outline_shoes':'FAIL: structural gaps repaired, but stance/hem breadth change across poses remains abrupt.',
            'bag_count':'PASS: exactly one bag through all seven sampled poses; no duplicate appears.',
            'colour_flicker':'FAIL: nearest-colour families match but garment shading/grain and occlusion still change at pose swaps.',
            'seam_flicker_01':'PASS: replacement01 has no cutout waist/shoulder boundary flashing; A5 original01 no longer live.'},
        'result':'FAIL','limits':'Model inspects decoded consecutive frames/keyframe strip; GIF is cropped preview with GIF timing quantization, AVI/fixed-fps trace is timing authority. Not human hit-feel or Owner art approval.'})
    print(f'A6_PLAYBACK rendered_frames={len(frames)} keyposes={len(selected)} result=FAIL honest_remaining_style_pops=true')

if __name__=='__main__':main()
