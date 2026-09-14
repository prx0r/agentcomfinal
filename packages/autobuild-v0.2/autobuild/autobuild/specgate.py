from collections import defaultdict, deque
from .canonical import digest
from .circuit import refs
from .underengineer import validate_feature_graph
from .qp_circuit_spec import validate as validate_qp_circuit

VALIDATOR_KINDS={"eq","gte","gt","lte","exists","exit_code","all","any"}


def _require_nonempty_string(obj,key,failures,label):
    v=obj.get(key)
    if not isinstance(v,str) or not v.strip(): failures.append(f"{label} missing non-empty {key}")


def _validate_validator(v,path,failures):
    if not isinstance(v,dict):
        failures.append(f"{path} validator must be object"); return
    kind=v.get("kind")
    if kind not in VALIDATOR_KINDS:
        failures.append(f"{path} unknown validator kind {kind!r}"); return
    params=v.get("params")
    if not isinstance(params,dict):
        failures.append(f"{path} validator params must be object"); return
    if kind in {"eq","gte","gt","lte"}:
        if not isinstance(params.get("path"),str) or not params.get("path"):
            failures.append(f"{path} validator {kind} missing path")
        if "value" not in params: failures.append(f"{path} validator {kind} missing value")
    elif kind=="exists":
        if not isinstance(params.get("path"),str) or not params.get("path"):
            failures.append(f"{path} validator exists missing path")
    elif kind=="exit_code":
        if "value" in params and not isinstance(params["value"],int):
            failures.append(f"{path} exit_code value must be integer")
    elif kind in {"all","any"}:
        children=params.get("validators")
        if not isinstance(children,list) or not children:
            failures.append(f"{path} validator {kind} requires non-empty validators")
        else:
            for i,c in enumerate(children): _validate_validator(c,f"{path}.{kind}[{i}]",failures)


def _validate_evidence_contract(ev,path,failures):
    if not isinstance(ev,dict) or not ev:
        failures.append(f"{path} evidence_contract must be non-empty object"); return
    declared=[k for k in ("command","file","http","metric","dns","event") if k in ev]
    if not declared:
        failures.append(f"{path} evidence_contract has no recognized source selector")
    if "command" in ev and (not isinstance(ev["command"],str) or not ev["command"].strip()):
        failures.append(f"{path} command evidence must be non-empty string")
    if "file" in ev and (not isinstance(ev["file"],str) or not ev["file"].strip()):
        failures.append(f"{path} file evidence must be non-empty string")


def _cycle(requirements):
    ids={r["id"] for r in requirements}; indeg={i:0 for i in ids}; edges=defaultdict(list)
    for r in requirements:
        for dep in r.get("depends_on",[]):
            if dep in ids: edges[dep].append(r["id"]); indeg[r["id"]]+=1
    q=deque(sorted(i for i,d in indeg.items() if d==0)); seen=0
    while q:
        x=q.popleft(); seen+=1
        for y in edges[x]:
            indeg[y]-=1
            if indeg[y]==0:q.append(y)
    return seen != len(ids)


def _safe_root(spec, failures):
    try:
        return digest(spec)
    except Exception as e:
        failures.append(f"target is not canonically serializable: {e}")
        return None


def validate_target(spec):
    failures=[]
    if not isinstance(spec,dict):
        root=_safe_root(spec, failures)
        failures.append("target spec must be object")
        return {"kind":"SPEC_GATE_RESULT","gate_id":"autobuild-spec-ready-v2","result":"FAIL","plan_root":root,"failures":failures}
    if spec.get("kind")!="TARGET_SPEC": failures.append("kind must be TARGET_SPEC")
    if spec.get("version")!="1.0": failures.append("version must be 1.0")
    _require_nonempty_string(spec,"id",failures,"target")
    _require_nonempty_string(spec,"objective",failures,"target")
    features=spec.get("features",[]); reqs=spec.get("requirements",[])
    if not isinstance(features,list): failures.append("features must be array"); features=[]
    if not isinstance(reqs,list): failures.append("requirements must be array"); reqs=[]
    try: validate_feature_graph(features)
    except Exception as e: failures.append(str(e))
    fids=[f.get("id") for f in features if isinstance(f,dict)]
    known_f={x for x in fids if isinstance(x,str) and x}
    rids=[]
    for i,r in enumerate(reqs):
        if not isinstance(r,dict): failures.append(f"requirement[{i}] must be object"); continue
        rid=r.get("id")
        if not isinstance(rid,str) or not rid.strip(): failures.append(f"requirement[{i}] missing non-empty id")
        else: rids.append(rid)
    if len(rids)!=len(set(rids)): failures.append("duplicate requirement ids")
    known_r=set(rids)
    for i,r in enumerate(reqs):
        if not isinstance(r,dict): continue
        rid=r.get("id",f"requirement[{i}]")
        _require_nonempty_string(r,"statement",failures,rid)
        if r.get("feature_id") not in known_f: failures.append(f"requirement {rid} unknown feature {r.get('feature_id')}")
        crit=r.get("criticality")
        if crit not in {"HARD","SOFT"}: failures.append(f"requirement {rid} invalid criticality {crit!r}")
        deps=r.get("depends_on",[])
        if not isinstance(deps,list): failures.append(f"requirement {rid} depends_on must be array"); deps=[]
        for dep in deps:
            if dep not in known_r: failures.append(f"requirement {rid} unknown dependency {dep}")
        if crit=="HARD":
            _validate_evidence_contract(r.get("evidence_contract"),rid,failures)
            _validate_validator(r.get("validator"),rid,failures)
        auth=r.get("authority",{})
        if isinstance(auth,dict) and auth.get("required"):
            if not isinstance(auth.get("capability"),str) or not auth.get("capability"):
                failures.append(f"requirement {rid} authority required but capability missing")
    if all(isinstance(r,dict) and isinstance(r.get("id"),str) and r.get("id") for r in reqs):
        if _cycle(reqs): failures.append("requirement dependency cycle")
    completion=spec.get("completion",{})
    if not isinstance(completion,dict): failures.append("completion must be object"); completion={}
    declared=completion.get("requirement_ids",[])
    if not isinstance(declared,list): failures.append("completion requirement_ids must be array"); declared=[]
    declared=set(declared); unknown=declared-known_r
    if unknown: failures.append(f"completion references unknown requirements: {sorted(unknown)}")
    hard={r.get("id") for r in reqs if isinstance(r,dict) and r.get("criticality")=="HARD" and r.get("id")}
    if completion.get("mode")=="ALL_HARD" and declared!=hard:
        failures.append(f"ALL_HARD completion must exactly cover hard requirements; missing={sorted(hard-declared)} extra={sorted(declared-hard)}")
    try:
        circuit_refs=refs(completion.get("circuit", {"op":"AND","args":[]})); bad=circuit_refs-known_r
        if bad: failures.append(f"completion circuit references unknown requirements: {sorted(bad)}")
        if completion.get("mode")=="ALL_HARD" and circuit_refs!=hard:
            failures.append(f"completion circuit must exactly reference hard requirements; missing={sorted(hard-circuit_refs)} extra={sorted(circuit_refs-hard)}")
    except Exception as e: failures.append(f"invalid completion circuit: {e}")
    econ=spec.get("economic_validation",{})
    if not isinstance(econ,dict): failures.append("economic_validation must be object"); econ={}
    metrics=econ.get("metrics",[])
    if econ.get("claimed",False) and not metrics: failures.append("economic validation claimed but no metrics declared")
    if econ.get("claimed",False):
        circuit=econ.get("qp_circuit")
        if not circuit: failures.append("economic validation claimed but qp_circuit missing")
        else: failures.extend("economic "+x for x in validate_qp_circuit(circuit))
    for i,m in enumerate(metrics or []):
        if not isinstance(m,dict): failures.append(f"economic metric[{i}] must be object"); continue
        for k in ("id","formula","source"):
            if not isinstance(m.get(k),str) or not m.get(k): failures.append(f"economic metric[{i}] missing {k}")
    root=_safe_root(spec, failures)
    return {"kind":"SPEC_GATE_RESULT","gate_id":"autobuild-spec-ready-v2","result":"PASS" if not failures else "FAIL","plan_root":root,"failures":failures}
