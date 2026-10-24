"""Normalize encoding/ANSI/trailing whitespace only; retain every diagnostic."""
from build_a7_spec import OUT
import re
for path in OUT.glob('*.log'):
    if path.name in ['package-run.log']:continue
    raw=path.read_bytes()
    data=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
    data=re.sub(r'\x1b\[[0-9;]*m','',data)
    path.write_text('\n'.join(v.rstrip() for v in data.replace('\r\n','\n').replace('\r','\n').splitlines()).rstrip()+'\n',encoding='utf-8',newline='\n')
print('A7_LOGS normalized UTF8/LF; no diagnostic lines removed')
