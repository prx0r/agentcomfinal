"""Fail-closed validation of PlanSpec before compilation."""
from .admission import validate_strategic
from .underengineer import validate_feature_graph, feature_score
from .canonical import digest


def _safe_root(plan, failures):
    try:
        return digest(plan)
    except Exception as e:
        failures.append(f"plan is not canonically serializable: {e}")
        return None


def validate_plan(plan):
    failures=[]
    if not isinstance(plan,dict):
        root=_safe_root(plan,failures)
        failures.append("plan must be object")
        return {"kind":"PLAN_GATE_RESULT","gate_id":"autobuild-plan-ready-v1","result":"FAIL","plan_root":root,"failures":failures}
    if plan.get("kind")!="PLAN_SPEC": failures.append("kind must be PLAN_SPEC")
    for k in ("id","objective"):
        if not isinstance(plan.get(k),str) or not plan.get(k).strip(): failures.append(f"missing non-empty {k}")
    strategic=plan.get("strategic_spec")
    if not isinstance(strategic,dict): failures.append("strategic_spec must be object")
    else:
        sr=validate_strategic(strategic)
        failures.extend("strategic: "+x for x in sr["failures"])
        kc=strategic.get("kill_conditions")
        if strategic.get("decision") in {"BUILD","VALIDATE"} and (not isinstance(kc,list) or not kc or not all(isinstance(x,str) and x.strip() for x in kc)):
            failures.append("strategic: kill_conditions must be non-empty string array")
    features=plan.get("features")
    if not isinstance(features,list) or not features:
        failures.append("features must be non-empty array")
        features=[]
    try:
        validate_feature_graph(features)
    except Exception as e:
        failures.append(str(e))
    for i,f in enumerate(features):
        if not isinstance(f,dict):
            failures.append(f"feature[{i}] must be object"); continue
        try: feature_score(f)
        except Exception as e: failures.append(str(e))
        reqs=f.get("requirements")
        if not isinstance(reqs,list): failures.append(f"feature {f.get('id',i)} requirements must be array"); continue
        for j,r in enumerate(reqs):
            if not isinstance(r,dict): failures.append(f"feature {f.get('id',i)} requirement[{j}] must be object")
    econ=plan.get("economic_validation",{"claimed":False,"metrics":[]})
    if not isinstance(econ,dict): failures.append("economic_validation must be object")
    root=_safe_root(plan,failures)
    return {"kind":"PLAN_GATE_RESULT","gate_id":"autobuild-plan-ready-v1","result":"PASS" if not failures else "FAIL","plan_root":root,"failures":failures}
