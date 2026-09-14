
import json, hashlib
from pathlib import Path

def read_jsonl(path):
    out=[]
    p=Path(path)
    if not p.exists(): return out
    for i,line in enumerate(p.read_text().splitlines(),1):
        if not line.strip(): continue
        obj=json.loads(line); obj['_line']=i; out.append(obj)
    return out

def evidence_root(events):
    canon='\n'.join(json.dumps({k:v for k,v in e.items() if k!='_line'},sort_keys=True,separators=(',',':')) for e in events)
    return 'sha256:'+hashlib.sha256(canon.encode()).hexdigest()
