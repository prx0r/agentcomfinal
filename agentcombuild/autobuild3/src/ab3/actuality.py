"""Actuality DAG: WebsiteWorks = AND of leaves, each in {TRUE,FALSE,UNKNOWN}.

Progress_i = 1 iff Leaf_i = TRUE. UNKNOWN blocks (never passes, never
scores). FALSE is decided-negative. Judges never raise: anything the judge
cannot decide is UNKNOWN.
"""
from ab1.canonical import canonical, sha12

from . import judges
from .judges import FALSE, TRUE, UNKNOWN


def leaf_root(leaf):
    return "leaf:" + sha12(canonical({"evidence": leaf.get("evidence"),
                                      "judge": leaf.get("judge")}))[:16]


def evaluate_leaf(leaf):
    """leaf: {id, evidence, judge:{engine,...}}. Returns {id, value, detail}."""
    if not isinstance(leaf, dict):
        return {"id": "?", "value": UNKNOWN, "detail": "bad-leaf"}
    value, detail = judges.judge_evidence(leaf.get("evidence"),
                                          leaf.get("judge", {}))
    return {"id": leaf.get("id", "?"), "value": value, "detail": detail}


def evidence_root(leaves):
    hashes = sorted(leaf_root({"evidence": l.get("evidence"), "judge": {}})
                    for l in leaves)
    return "eroot:" + sha12(canonical(hashes))[:16]


def validator_root(leaves):
    hashes = sorted(leaf_root({"evidence": {}, "judge": l.get("judge")})
                    for l in leaves)
    return "vroot:" + sha12(canonical(hashes))[:16]


def evaluate_dag(dag):
    """dag: {claim, contract_root?, leaves[]}. AND-semantics with UNKNOWN."""
    leaves = dag.get("leaves", []) if isinstance(dag, dict) else []
    scored = [evaluate_leaf(l) for l in leaves]
    values = [s["value"] for s in scored]
    if any(v == FALSE for v in values) or not scored:
        value = FALSE if scored else UNKNOWN
    elif any(v == UNKNOWN for v in values):
        value = UNKNOWN
    else:
        value = TRUE
    return {"claim": dag.get("claim", "?"), "value": value,
            "progress": 1 if value == TRUE else 0, "leaves": scored,
            "evidence_root": evidence_root(leaves),
            "validator_root": validator_root(leaves)}


def actuality_record(claim, value, contract_root, evidence_root,
                     validator_root, environment, observed_at, proof_class):
    """A(C,E)=1 means: all frozen acceptance predicates for C passed against
    admissible, sufficiently fresh E. Contractual actuality, not omniscience."""
    return {"claim": claim, "actuality": value, "contract_root": contract_root,
            "evidence_root": evidence_root, "validator_root": validator_root,
            "environment": environment, "observed_at": observed_at,
            "proof_class": proof_class}
