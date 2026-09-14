from copy import deepcopy
from .canonical import digest,content_id
from .underengineer import select_minimum
from .specgate import validate_target
from .circuit import all_of
from .admission import validate_strategic
from .plangate import validate_plan

def _norm_req(feature,r):
    rr=deepcopy(r); rr.setdefault("feature_id",feature["id"]); rr.setdefault("criticality","HARD"); rr.setdefault("depends_on",[]); rr.setdefault("authority",{"required":False})
    if "id" not in rr: rr["id"]=content_id("req",{"feature":feature["id"],"statement":rr.get("statement","")})
    return rr

def compile_plan(plan,threshold=0.70):
    plan_gate=validate_plan(plan)
    if plan_gate["result"] != "PASS":
        raise ValueError("plan gate failed: " + "; ".join(plan_gate["failures"]))
    strategic=plan.get("strategic_spec",{})
    admission=validate_strategic(strategic)
    if admission["result"]!="PASS": raise ValueError("strategic admission failed: "+"; ".join(admission["failures"]))
    decision=strategic.get("decision")
    if decision not in {"BUILD","VALIDATE"}: raise ValueError(f"strategic decision {decision!r} not executable")
    source_features=deepcopy(plan.get("features",[])); under=select_minimum(source_features,threshold); selected=set(under["selected_ids"])
    reqs=[]
    features=[]
    # First normalize all selected requirements, then project feature DAG edges
    # into requirement dependencies. A downstream feature cannot become READY
    # before every HARD requirement of its selected immediate dependencies.
    selected_feature_reqs={}
    for f in source_features:
        if f["id"] in selected:
            normalized=[_norm_req(f,r) for r in f.get("requirements",[])]
            reqs.extend(normalized)
            selected_feature_reqs[f["id"]]=[r["id"] for r in normalized if r.get("criticality")=="HARD"]
        # TargetSpec has one canonical requirement table. Do not duplicate
        # requirement semantics inside feature records.
        fm={k:deepcopy(v) for k,v in f.items() if k!="requirements"}
        fm["selected"]=f["id"] in selected
        features.append(fm)

    feature_by_id={f["id"]:f for f in source_features}
    for r in reqs:
        f=feature_by_id[r["feature_id"]]
        inherited=[]
        for dep_feature in f.get("depends_on",[]):
            if dep_feature in selected_feature_reqs:
                inherited.extend(selected_feature_reqs[dep_feature])
        r["depends_on"]=sorted(set(r.get("depends_on",[])) | set(inherited))
    hard=[r["id"] for r in reqs if r.get("criticality")=="HARD"]
    target={"kind":"TARGET_SPEC","version":"1.0","id":plan["id"],"strategic_parent":{"id":plan.get("strategic_spec",{}).get("id"),"root":digest(plan.get("strategic_spec",{})),"decision":decision,"durable_scarcity":plan.get("strategic_spec",{}).get("durable_scarcity")},"objective":plan["objective"],"features":features,"requirements":reqs,"completion":{"mode":"ALL_HARD","requirement_ids":hard,"circuit":all_of(hard)},"economic_validation":deepcopy(plan.get("economic_validation",{"claimed":False,"metrics":[]})),"reuse":{"status":"UNSCANNED","coverage":None,"components":[],"missing_requirement_ids":[]},"metadata":{"compiler":"autobuild-compile-v2","underengineer":under}}
    return {"target_spec":target,"gate":validate_target(target)}
