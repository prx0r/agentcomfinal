from .canonical import digest, canonical_clone

_MISSING = object()

def _paths(a, b, path="$"):
    if isinstance(a, dict) and isinstance(b, dict):
        out=[]
        for k in sorted(set(a) | set(b)):
            av=a.get(k,_MISSING); bv=b.get(k,_MISSING); child=f"{path}.{k}"
            if av is _MISSING: out.append({"path":child,"op":"ADD","old":None,"new":bv})
            elif bv is _MISSING: out.append({"path":child,"op":"REMOVE","old":av,"new":None})
            else: out.extend(_paths(av,bv,child))
        return out
    if isinstance(a, list) and isinstance(b, list):
        return [] if a == b else [{"path":path,"op":"REPLACE","old":a,"new":b}]
    return [] if a == b else [{"path":path,"op":"REPLACE","old":a,"new":b}]

def changeset(before, after, transform_id="diff-v1", reasons=None, evidence_ids=None):
    changes=[]
    for c in _paths(before,after):
        c=canonical_clone(c)
        c["old_hash"]=digest(c["old"]); c["new_hash"]=digest(c["new"])
        changes.append(c)
    obj={"kind":"CHANGESET","version":"1.0","transform_id":transform_id,"before_root":digest(before),"after_root":digest(after),"reasons":sorted(reasons or []),"evidence_ids":sorted(evidence_ids or []),"changes":changes}
    obj["changes_root"]=digest(changes)
    return obj
