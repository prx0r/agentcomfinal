"""Actuality compiler (E2): campaign -> frozen WHAT-must-be-true.

ContractRoot covers claim + leaf {id, judge, evidence_class} only — never
probes, freshness, or runners. Swapping HOW (probe implementation) changes
PlanRoot and leaves ContractRoot untouched (tested). A hard leaf without a
judge is UNPROVABLE and fails compilation: no silent gaps in the contract.
"""
from core import ids

LEAF_FIELDS = ("id", "probe", "evidence_schema", "judge", "freshness_s",
               "evidence_class", "authority")


def check_leaf(leaf):
    """Hard leaves need everything; returns (ok, reasons)."""
    reasons = []
    if not isinstance(leaf, dict):
        return False, ["bad-leaf"]
    for f in LEAF_FIELDS:
        if leaf.get(f) is None:
            reasons.append("%s: missing %s" % (leaf.get("id", "?"), f))
    judge = leaf.get("judge") or {}
    if judge.get("engine") not in ("schema", "cel", "rego", "wasm"):
        reasons.append("%s: no durable judge engine" % leaf.get("id", "?"))
    return (not reasons), reasons


def compile_contract(claim, leaves, plan_ref=""):
    """Returns {contract_root, plan_root, claim, leaves, unprovable}. Two
    roots from one compile: WHAT (stable) and HOW (route-specific)."""
    leaves = list(leaves or [])
    unprovable = [l.get("id", "?") for l in leaves
                  if not check_leaf(l)[0]]
    what = {"claim": claim,
            "leaves": [{k: l.get(k) for k in ("id", "judge", "evidence_class")}
                       for l in leaves]}
    how = {"claim": claim, "leaves": leaves, "plan_ref": plan_ref}
    return {"contract_root": ids.obj_id("contract", what),
            "plan_root": ids.obj_id("plan", how),
            "claim": claim, "leaves": leaves, "unprovable": unprovable}


def check_compilable(compiled):
    if compiled.get("unprovable"):
        return False, ["unprovable:%s" % ",".join(compiled["unprovable"])]
    if not compiled.get("leaves"):
        return False, ["no-leaves"]
    return True, []


UK_LEAVES = [
    {"id": "business-identity-verified", "probe": "company.lookup",
     "evidence_schema": {"type": "object", "required": ["business_id"]},
     "judge": {"engine": "cel", "expression": "e.business_id != ''"},
     "freshness_s": 86400, "evidence_class": "direct", "authority": "none"},
    {"id": "delegated-authority-exists", "probe": "grant.describe",
     "evidence_schema": {"type": "object", "required": ["grant_id"]},
     "judge": {"engine": "cel", "expression": "e.grant_valid == true"},
     "freshness_s": 3600, "evidence_class": "direct", "authority": "grant"},
    {"id": "incoming-lead-observed", "probe": "cmail.read",
     "evidence_schema": {"type": "object", "required": ["lead_id"]},
     "judge": {"engine": "cel", "expression": "e.lead_id != ''"},
     "freshness_s": 600, "evidence_class": "direct", "authority": "none"},
    {"id": "response-constructed", "probe": "artifact.exists",
     "evidence_schema": {"type": "object", "required": ["artifact"]},
     "judge": {"engine": "cel", "expression": "e.complete == true"},
     "freshness_s": 3600, "evidence_class": "direct", "authority": "none"},
    {"id": "outbound-sent", "probe": "company.send_email",
     "evidence_schema": {"type": "object", "required": ["status"]},
     "judge": {"engine": "cel", "expression": "e.status == 202"},
     "freshness_s": 600, "evidence_class": "direct", "authority": "grant"},
    {"id": "readback-agrees", "probe": "provider.readback",
     "evidence_schema": {"type": "object",
                         "required": ["created_id", "found_id"]},
     "judge": {"engine": "cel",
               "expression": "e.found_id == e.created_id"},
     "freshness_s": 300, "evidence_class": "external_readback",
     "authority": "none"},
    {"id": "outcome-observed", "probe": "provider.outcome",
     "evidence_schema": {"type": "object", "required": ["outcome"]},
     "judge": {"engine": "cel", "expression": "e.outcome != ''"},
     "freshness_s": 86400, "evidence_class": "external_readback",
     "authority": "none"},
]

UK_CLAIM = "one real inbound lead receives one bounded booking reply"


def compile_uk(plan_ref="lead-reply-sim0"):
    """E2: the one campaign, compiled. No leaf may be 'agent judges quality'."""
    import copy
    return compile_contract(UK_CLAIM, copy.deepcopy(UK_LEAVES), plan_ref)
