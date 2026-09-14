"""Reusable LEGO primitives and deterministic composition metadata."""
from .canonical import content_id,digest,canonical_clone

REQUIRED={"name","requires","provides","transform","validator"}

def make_primitive(name,requires,provides,transform,validator,**meta):
    core={"name":name,"requires":sorted(set(requires)),"provides":sorted(set(provides)),"transform":transform,"validator":validator}
    pid=content_id("primitive",core)
    out={"kind":"PRIMITIVE","version":"1.0","id":pid,**core,"meta":meta}
    out["semantic_root"]=digest(core)
    return out

def validate_primitive(p):
    missing=sorted(REQUIRED-set(p))
    if missing:return {"result":"FAIL","failures":[f"missing {x}" for x in missing]}
    if not p.get("provides"):return {"result":"FAIL","failures":["provides empty"]}
    return {"result":"PASS","failures":[]}

def compose(primitives,initial_capabilities,target_capabilities):
    """Deterministic greedy closure. Records each exact newly enabled brick."""
    available=set(initial_capabilities); remaining={p["id"]:p for p in primitives}; steps=[]
    while not set(target_capabilities) <= available:
        candidates=[]
        for p in remaining.values():
            if set(p.get("requires",[])) <= available:
                gain=set(p.get("provides",[]))-available
                if gain:candidates.append((len(gain),p["id"],p,gain))
        if not candidates:break
        # max gain, then stable id
        _,_,p,gain=sorted(candidates,key=lambda x:(-x[0],x[1]))[0]
        before=sorted(available); available |= gain
        steps.append({"primitive_id":p["id"],"before":before,"added":sorted(gain),"after":sorted(available)})
        remaining.pop(p["id"])
    missing=sorted(set(target_capabilities)-available)
    return {"result":"PASS" if not missing else "INCOMPLETE","initial":sorted(set(initial_capabilities)),"target":sorted(set(target_capabilities)),"steps":steps,"available":sorted(available),"missing":missing}

def promote_candidate(pattern_id,uses,minimum_uses=3):
    """Deprecated count-only signal. Never authorizes promotion."""
    unique=sorted(set(uses))
    return {"pattern_id":pattern_id,"unique_project_uses":unique,"count":len(unique),"minimum_uses":minimum_uses,"decision":"EVAL_REQUIRED","note":"Use promotion.assess_promotion with held-out replay/regression evidence."}
