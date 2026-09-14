from collections import defaultdict, deque

FORMULA_ID="underengineer-v2"

REQUIRED_SCORE_KEYS=("moat","asset_accumulation","dependency_centrality","validation_value","implementation_cost","lab_attack_risk")


def _finite_unit(value,key,fid):
    x=float(value)
    if x != x or x < 0.0 or x > 1.0:
        raise ValueError(f"feature {fid} score {key} must be finite in [0,1]")
    return x


def validate_feature_graph(features):
    ids=[]
    for f in features:
        fid=f.get("id")
        if not isinstance(fid,str) or not fid.strip():
            raise ValueError("every feature requires non-empty string id")
        ids.append(fid)
    if len(ids)!=len(set(ids)):
        raise ValueError("duplicate feature ids")
    known=set(ids)
    indeg={i:0 for i in ids}; edges=defaultdict(list)
    for f in features:
        fid=f["id"]
        for dep in f.get("depends_on",[]):
            if dep not in known:
                raise ValueError(f"feature {fid} unknown dependency {dep}")
            edges[dep].append(fid); indeg[fid]+=1
    q=deque(sorted(i for i,d in indeg.items() if d==0)); seen=[]
    while q:
        x=q.popleft(); seen.append(x)
        for y in sorted(edges[x]):
            indeg[y]-=1
            if indeg[y]==0:q.append(y)
    if len(seen)!=len(ids):
        cyclic=sorted(i for i,d in indeg.items() if d>0)
        raise ValueError(f"feature dependency cycle: {cyclic}")
    return seen


def feature_score(feature):
    fid=feature.get("id","?"); s=feature.get("scores",{})
    vals={k:_finite_unit(s.get(k,0),k,fid) for k in REQUIRED_SCORE_KEYS}
    return (vals["moat"]*vals["asset_accumulation"]*vals["dependency_centrality"]*vals["validation_value"])/(1.0+vals["implementation_cost"]+vals["lab_attack_risk"])


def select_minimum(features,threshold=0.70):
    if not 0.0 <= float(threshold) <= 1.0:
        raise ValueError("threshold must be in [0,1]")
    validate_feature_graph(features)
    byid={f["id"]:f for f in features}
    rows=sorted(((feature_score(f),f) for f in features),key=lambda x:(-x[0],x[1]["id"]))
    total=sum(max(0,float(f.get("scores",{}).get("moat",0))) for f in features) or 1.0
    selected=set(); why={}; accum=0.0
    def add(fid,reason):
        nonlocal accum
        if fid in selected:return
        for dep in sorted(byid[fid].get("depends_on",[])):
            add(dep,f"dependency of {fid}")
        selected.add(fid); accum+=max(0,float(byid[fid].get("scores",{}).get("moat",0))); why.setdefault(fid,[]).append(reason)
    for score,f in rows:
        if accum/total>=threshold:break
        if score>0:add(f["id"],f"ranked MMP={score:.6f}")
    for f in features:
        if f.get("starts_moat_accumulation"):add(f["id"],"starts_moat_accumulation=true")
    return {"formula_id":FORMULA_ID,"threshold":threshold,"selected_ids":sorted(selected),"deferred_ids":sorted(set(byid)-selected),"scored":[{"id":f["id"],"score":round(feature_score(f),8),"selected":f["id"] in selected,"reasons":why.get(f["id"],["deferred: below minimum moat path"])} for _,f in rows]}
