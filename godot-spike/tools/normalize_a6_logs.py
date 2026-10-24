"""Normalize encoding/ANSI/trailing progress whitespace without dropping lines."""
from prepare_a6_frames import OUT
import re
for path in OUT.glob('*.log'):
    if path.name=='package-run.log':continue  # may be redirected by caller
    raw=path.read_bytes();text=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
    text=re.sub(r'\x1b\[[0-9;]*m','',text)
    path.write_text('\n'.join(line.rstrip() for line in text.replace('\r\n','\n').replace('\r','').splitlines())+'\n',encoding='utf-8',newline='\n')
