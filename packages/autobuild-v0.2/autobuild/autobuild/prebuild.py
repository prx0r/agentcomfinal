from copy import deepcopy
from .canonical import digest
from .receipt import transformation_receipt
from .roots import contract_root, plan_root

ALLOWED_RIGHTS={"OWNED","AUTHORIZED","PERMISSIVE","API_TERMS_OK"}
ALLOWED_LICENSE={"PERMISSIVE","COMMERCIAL_OK","API_TERMS_OK","PROPRIETARY_OWNED"}
ALLOWED_ACTIONS={"REUSE","BUY","BUILD","BLOCK"}


def make_request(target):
    reqs=[]
    for r in target.get("requirements",[]):
        reqs.append({
          "requirement_id":r["id"],"feature_id":r["feature_id"],"job":r["statement"],
          "criticality":r.get("criticality","HARD"),"desired_interfaces":r.get("desired_interfaces",[]),
          "constraints":r.get("reuse_constraints",{})})
    out={"kind":"PREBUILD_REQUEST","version":"2.1","contract_root":contract_root(target),"input_plan_root":plan_root(target),"requirements":reqs,
         "search_order":["existing finished product/API","official SDK","finished MCP","maintained package/library","reference implementation","paper implementation"],
         "required_evaluation":["license_status","rights_status","maintenance","tests","security","fit","integration_cost","provenance"]}
    out["request_root"]=digest(out); return out


def _normalize_entry(rid,e):
    e=deepcopy(e or {})
    e.setdefault("requirement_id",rid)
    action=e.get("action","BUILD")
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"prebuild entry {rid} invalid action {action!r}")
    fit=float(e.get("reuse_fitness",0))
    if fit != fit or fit < 0.0 or fit > 1.0:
        raise ValueError(f"prebuild entry {rid} reuse_fitness must be finite in [0,1]")
    if action in {"REUSE","BUY"}:
        cand=e.get("candidate")
        if not isinstance(cand,dict) or not cand.get("name") or not cand.get("kind"):
            raise ValueError(f"prebuild entry {rid} {action} requires named candidate with kind")
        if not isinstance(e.get("reason"),str) or not e.get("reason").strip():
            raise ValueError(f"prebuild entry {rid} {action} requires reason")
    candidate=e.get("candidate") or {}
    rights=e.get("rights_status") or candidate.get("rights_status") or candidate.get("rights") or "UNKNOWN"
    lic=e.get("license_status") or candidate.get("license_status") or candidate.get("license") or "UNKNOWN"
    rights=str(rights).upper(); lic=str(lic).upper()
    e["rights_status"]=rights; e["license_status"]=lic
    e["declared_reuse_fitness"]=fit
    legal_ok=rights in ALLOWED_RIGHTS and lic in ALLOWED_LICENSE
    if action in {"REUSE","BUY"} and not legal_ok:
        e["original_action"]=action
        e["action"]="BLOCK"
        e["reuse_fitness"]=0.0
        e["gate_failure"]="rights/license not explicitly allowed"
    else:
        e["reuse_fitness"]=fit
    return e


def apply_reuse_plan(target,plan,reuse_threshold=0.80):
    before=deepcopy(target); t=deepcopy(target)
    if plan.get("kind")!="REUSE_PLAN": raise ValueError("prebuild plan kind must be REUSE_PLAN")
    expected_contract=contract_root(target)
    expected_plan=plan_root(target)
    if plan.get("contract_root") != expected_contract:
        raise ValueError(f"prebuild contract_root mismatch: expected {expected_contract}, got {plan.get('contract_root')}")
    if plan.get("input_plan_root") != expected_plan:
        raise ValueError(f"prebuild input_plan_root mismatch: expected {expected_plan}, got {plan.get('input_plan_root')}")
    raw=plan.get("entries",[])
    ids=[e.get("requirement_id") for e in raw if isinstance(e,dict)]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate prebuild requirement_id")
    known={r["id"] for r in t.get("requirements",[])}
    unknown={x for x in ids if x not in known}
    if unknown: raise ValueError(f"prebuild contains unknown requirements: {sorted(unknown)}")
    entries={e["requirement_id"]:e for e in raw}
    components=[]; missing=[]; weights=0.0; reuse_mass=0.0
    for r in t.get("requirements",[]):
        e=_normalize_entry(r["id"],entries.get(r["id"]))
        if r["id"] not in entries:
            e.update({"action":"BUILD","reuse_fitness":0.0,"reason":"no prebuild result"})
        weight=2.0 if r.get("criticality")=="HARD" else 1.0; weights+=weight
        fit=float(e.get("reuse_fitness",0)); reuse_mass+=weight*fit
        components.append(e)
        if fit < reuse_threshold or e.get("action") in ("BUILD","BLOCK"):
            missing.append(r["id"])
    coverage=reuse_mass/weights if weights else 0.0
    t["reuse"]={"status":"SCANNED","coverage":round(coverage,6),"threshold":reuse_threshold,"components":components,"missing_requirement_ids":sorted(missing),"prebuild_root":digest(plan)}
    rr=transformation_receipt(before,t,"apply-reuse-plan-v2",["prebuild-results"],[digest(plan)])
    return {"target_spec":t,**rr}
