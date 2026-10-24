"""Regenerate manifest contact sheet; explicitly an asset sheet."""
from prepare_a5_frames import SHARED
from PIL import Image, ImageDraw
import json

manifest=json.loads((SHARED/'manifest.json').read_text())
sheet=Image.new('RGB',(1536, len(manifest['sequences'])*290),(34,40,38));d=ImageDraw.Draw(sheet)
for row,(name,seq) in enumerate(manifest['sequences'].items()):
    d.text((8,row*290+5),'A5 ASSET SHEET | '+name,fill='white')
    for col,f in enumerate(seq['frames']):
        im=Image.open(SHARED/f['path']).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
        sheet.paste(im,(col*256,row*290+22),im)
        d.text((col*256+5,row*290+276),f['path'],fill='white')
sheet.save(SHARED/'contact-sheet.png',optimize=True)
print('A5_CONTACT_SHEET regenerated_from_live_manifest=true')
