"""Actuality DAG (PROMOTED to canonical 2026-09-14, gitbuild1 experiment 1).

Provenance: semantics promoted from agentcombuild/autobuild3/src/ab3
(frozen). ONE deliberate change: all roots are FULL SHA-256 via core.ids
(devplan §11 — no truncated identity on evidence paths).
AND over TRUE/FALSE/UNKNOWN; UNKNOWN blocks progress.
"""
from core import ids

from . import judges
from .judges import FALSE, TRUE, UNKNOWN


def leaf_id(leaf):
    return "leaf:" + ids.sha256_hex(ids.canonical(
        {"evidence": leaf.get("evidence"), "judge": leaf.get("judge")}))


def evaluate_leaf(leaf):
    if not isinstance(leaf, dict):
        return {"id": "?", "value": UNKNOWN, "detail": "bad-leaf"}
    value, detail = judges.judge_evidence(leaf.get("evidence"),
                                          leaf.get("judge", {}))
    return {"id": leaf.get("id", "?"), "value": value, "detail": detail}


def evidence_root(leaves):
    hashes = sorted(leaf_id({"evidence": l.get("evidence"), "judge": {}})
                    for l in leaves)
    return "eroot:" + ids.sha256_hex(ids.canonical(hashes))


def validator_root(leaves):
    hashes = sorted(leaf_id({"evidence": {}, "judge": l.get("judge")})
                    for l in leaves)
    return "vroot:" + ids.sha256_hex(ids.canonical(hashes))


def evaluate_dag(dag):
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
    return {"claim": claim, "actuality": value, "contract_root": contract_root,
            "evidence_root": evidence_root, "validator_root": validator_root,
            "environment": environment, "observed_at": observed_at,
            "proof_class": proof_class}
