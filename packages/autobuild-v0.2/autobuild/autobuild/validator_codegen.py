"""Generate stdlib-only A-Task validators from autobuild validator specs.
The script judges recorded evidence. It never calls an LLM."""
import json
from pathlib import Path

_RUNTIME = r'''import json,sys
from pathlib import Path

def get(obj,path):
    cur=obj
    for part in path.split('.'):
        if not isinstance(cur,dict) or part not in cur:return None,False
        cur=cur[part]
    return cur,True

def ev(v,e):
    k=v.get('kind'); p=v.get('params',{})
    if k=='eq':
        x,ok=get(e,p['path']); return ok and x==p['value'], f"{p['path']}={x!r} expected={p['value']!r}"
    if k=='gte':
        x,ok=get(e,p['path']); return ok and x>=p['value'], f"{p['path']}={x!r} threshold>={p['value']!r}"
    if k=='gt':
        x,ok=get(e,p['path']); return ok and x>p['value'], f"{p['path']}={x!r} threshold>{p['value']!r}"
    if k=='lte':
        x,ok=get(e,p['path']); return ok and x<=p['value'], f"{p['path']}={x!r} threshold<={p['value']!r}"
    if k=='exists':
        _,ok=get(e,p['path']); return ok, f"exists {p['path']}={ok}"
    if k=='all':
        rs=[ev(c,e) for c in p['validators']]; return all(x[0] for x in rs), str(rs)
    if k=='any':
        rs=[ev(c,e) for c in p['validators']]; return any(x[0] for x in rs), str(rs)
    return False, f"unsupported generated validator kind {k}"

_,tid,queue_path,alog_path=sys.argv
SPEC=__SPEC__
EVIDENCE_PATH=__EVIDENCE_PATH__
reasons=[]
try:
    evidence=json.loads(Path(EVIDENCE_PATH).read_text())
except Exception as ex:
    evidence=None; reasons.append(f"evidence unreadable: {ex}")
if evidence is not None:
    ok,proof=ev(SPEC,evidence)
    if not ok:reasons.append(proof)
print(json.dumps({'pass':not reasons,'reasons':reasons},sort_keys=True))
'''

def generate_validator(validator_spec,evidence_contract):
    path=evidence_contract.get("file")
    if not path:
        # command evidence is rerun by A-Task itself; generated validator should not duplicate shell execution.
        return None
    return _RUNTIME.replace("__SPEC__",repr(validator_spec)).replace("__EVIDENCE_PATH__",repr(path))

def materialize(atask_bridge,out_dir):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); written=[]
    for task in atask_bridge.get("tasks",[]):
        declared=task.get("declared_evidence",[])
        file_ev=next((x.split(":",1)[1] for x in declared if x.startswith("file:")),None)
        if not file_ev: continue
        script=generate_validator(task["validator_spec"],{"file":file_ev})
        p=out/Path(task["validator_filename"]).name; p.write_text(script); p.chmod(0o755); written.append(str(p))
    return written
