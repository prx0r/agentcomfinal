"""Separate normative success identity from replaceable execution planning.

ContractRoot = WHAT counts as success.
PlanRoot     = HOW the current Autobuild artifact plans to achieve it.
LineageRoot  = WHY/WHERE the contract came from (strategy/compiler ancestry).

The normative projection canonicalizes semantically unordered structures so
provider-specific list order does not change ContractRoot.
"""
from copy import deepcopy
from .canonical import digest, canonical_bytes


def _norm_bool_circuit(node):
    if not isinstance(node,dict): return deepcopy(node)
    out=deepcopy(node); op=out.get("op")
    if isinstance(out.get("args"),list):
        args=[_norm_bool_circuit(x) for x in out["args"]]
        if op in {"AND","OR"}:
            args=sorted(args,key=canonical_bytes)
        out["args"]=args
    if isinstance(out.get("arg"),dict): out["arg"]=_norm_bool_circuit(out["arg"])
    return out


def contract_projection(target):
    if not isinstance(target,dict) or target.get("kind")!="TARGET_SPEC":
        raise ValueError("contract_projection requires TARGET_SPEC")
    requirements=[]
    for source in target.get("requirements",[]):
        r=deepcopy(source)
        if isinstance(r.get("depends_on"),list): r["depends_on"]=sorted(set(r["depends_on"]))
        requirements.append(r)
    requirements=sorted(requirements,key=lambda r:r.get("id",""))

    completion=deepcopy(target.get("completion",{}))
    if isinstance(completion.get("requirement_ids"),list):
        completion["requirement_ids"]=sorted(set(completion["requirement_ids"]))
    if isinstance(completion.get("circuit"),dict):
        completion["circuit"]=_norm_bool_circuit(completion["circuit"])

    econ=deepcopy(target.get("economic_validation",{}))
    if isinstance(econ.get("metrics"),list):
        econ["metrics"]=sorted(econ["metrics"],key=lambda m:canonical_bytes(m))
    if isinstance(econ.get("qp_circuit"),dict):
        econ["qp_circuit"]=_norm_bool_circuit(econ["qp_circuit"])

    # Deliberately exclude feature scores, underengineer diagnostics, reuse plan,
    # compiler metadata, and strategic rationale. Requirements/authority and
    # completion/economic circuits are normative success semantics.
    return {
        "kind":"AUTOBUILD_CONTRACT",
        "version":"1.0",
        "target_id":target.get("id"),
        "objective":target.get("objective"),
        "requirements":requirements,
        "completion":completion,
        "economic_validation":econ,
    }


def contract_root(target):
    return digest(contract_projection(target))


def plan_root(target):
    return digest(target)


def lineage_projection(target):
    return {
        "kind":"AUTOBUILD_LINEAGE",
        "version":"1.0",
        "target_id":target.get("id"),
        "strategic_parent":deepcopy(target.get("strategic_parent",{})),
        "compiler":deepcopy(target.get("metadata",{}).get("compiler")),
        "underengineer":deepcopy(target.get("metadata",{}).get("underengineer",{})),
    }


def lineage_root(target):
    return digest(lineage_projection(target))
