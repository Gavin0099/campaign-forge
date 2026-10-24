from prepare_a6_frames import *
import sys
sheet=Image.new('RGB',(1536,1100),(34,40,38));d=ImageDraw.Draw(sheet)
for i,index in enumerate(['00','01','02']):
    for row,folder in enumerate([BASE,SHARED/'thoma/swing']):
        im=Image.open(folder/f'{index}.png').convert('RGBA')
        sheet.paste(im,(i*512,row*550+30),im)
        d.text((i*512+8,row*550+8),('A5 baseline ' if row==0 else 'A6 neighbours / retained01 ')+index,fill='white')
sheet.save(OUT/('01-neighbours-after.png' if '--after' in sys.argv else '01-neighbours-before.png'),optimize=True)
