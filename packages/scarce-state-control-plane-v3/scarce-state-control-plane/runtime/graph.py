
from .model import projects

def checkpoint_index():
    idx={}
    for p in projects():
        for cp in p['checkpoints']:
            idx[cp['id']]={'project_id':p['id'],**cp}
    return idx

def assert_acyclic():
    idx=checkpoint_index(); visiting=set(); done=set()
    def dfs(n):
        if n in visiting: raise ValueError(f'cycle at {n}')
        if n in done: return
        visiting.add(n)
        for d in idx[n].get('depends_on',[]):
            if d not in idx: raise ValueError(f'missing dependency {d} for {n}')
            dfs(d)
        visiting.remove(n); done.add(n)
    for n in idx: dfs(n)
    return True

def ready(project, proven_ids):
    proven=set(proven_ids); out=[]
    for cp in project['checkpoints']:
        if cp['id'] in proven: continue
        if all(d in proven for d in cp.get('depends_on',[])): out.append(cp)
    return out
