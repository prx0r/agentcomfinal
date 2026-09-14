from .tristate import TRUE, FALSE, UNKNOWN, tri_and, tri_or

def _get(obj,dotted):
    cur=obj
    for part in dotted.split("."):
        if not isinstance(cur,dict) or part not in cur: return None,False
        cur=cur[part]
    return cur,True

def evaluate(validator,evidence):
    kind=validator.get("kind"); params=validator.get("params",{})
    if evidence is None: return {"state":UNKNOWN,"proof":"required evidence unavailable"}
    if kind in {"eq","gte","gt","lte"}:
        value,ok=_get(evidence,params["path"])
        if not ok or value is None: return {"state":UNKNOWN,"proof":f"missing path {params['path']}"}
        exp=params["value"]
        passed={"eq":value==exp,"gte":value>=exp,"gt":value>exp,"lte":value<=exp}[kind]
        return {"state":TRUE if passed else FALSE,"proof":f"{params['path']}={value!r}; {kind} {exp!r}"}
    if kind=="exists":
        _,ok=_get(evidence,params["path"]); return {"state":TRUE if ok else FALSE,"proof":f"path exists={ok}: {params['path']}"}
    if kind=="exit_code":
        code=evidence.get("exit_code") if isinstance(evidence,dict) else None
        if code is None: return {"state":UNKNOWN,"proof":"exit_code absent"}
        exp=int(params.get("value",0)); return {"state":TRUE if int(code)==exp else FALSE,"proof":f"exit_code={code}; expected={exp}"}
    if kind in {"all","any"}:
        child=[evaluate(v,evidence) for v in params.get("validators",[])]
        state=tri_and(c["state"] for c in child) if kind=="all" else tri_or(c["state"] for c in child)
        return {"state":state,"proof":child}
    return {"state":FALSE,"proof":f"unknown validator kind: {kind}"}
