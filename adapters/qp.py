"""QP adapter (devplan §13/§25): AgentCom asks QP; QP constructs/verifies.

No local clone of semantics: CLAIM/TASK/GATE/GRANT ids are minted by real
`~/qp` constructors (imported, version-pinned below). AgentCom stores the
references. Receipt settlement/verification stays inside QP
(`acom/receipts.py`); this adapter never settles.
"""
import importlib.util
import os
import subprocess
import sys

QP_ROOT = "/home/ubuntu/qp"
PKG = "qp_acom"


def _pkg():
    if PKG in sys.modules:
        return sys.modules[PKG]
    spec = importlib.util.spec_from_file_location(
        PKG, os.path.join(QP_ROOT, "acom", "__init__.py"),
        submodule_search_locations=[os.path.join(QP_ROOT, "acom")])
    pkg = importlib.util.module_from_spec(spec)
    sys.modules[PKG] = pkg
    spec.loader.exec_module(pkg)
    return pkg


def _mod(name):
    _pkg()
    full = PKG + "." + name
    if full in sys.modules:
        return sys.modules[full]
    spec = importlib.util.spec_from_file_location(
        full, os.path.join(QP_ROOT, "acom", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[full] = mod
    spec.loader.exec_module(mod)
    return mod


def version():
    try:
        rev = subprocess.run(["git", "-C", QP_ROOT, "rev-parse", "HEAD"],
                             capture_output=True, text=True,
                             timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        rev = "unknown"
    return {"repo": QP_ROOT, "rev": rev, "protocol": "acom/0.1",
            "schema": "https://pog.town/schemas/acom-0.1.json"}


def make_claim(statement, domain):
    return _mod("objects").make_claim(statement, domain)


def make_task(kind, target, acceptance):
    return _mod("objects").make_task(kind, target, acceptance)


def make_gate(gate_id, runtime, program_hash):
    return _mod("objects").make_gate(gate_id, runtime, program_hash)


def make_grant(subject, capability, constraints, predicates, expiry):
    return _mod("objects").make_grant(subject, capability, constraints,
                                      predicates, expiry)


def make_evidence(metric, value, unit, as_of, source):
    return _mod("objects").make_evidence(metric, value, unit, as_of, source)


def bind_requirement(contract_root, requirement_id, claim, task, gate,
                     minimum_proof_level=9):
    """Reference bundle AgentCom files (never fabricates). Mirrors the
    adapter shape in agentcomidea §8."""
    return {"contract_root": contract_root, "requirement_id": requirement_id,
            "qp_claim_id": claim["id"], "qp_task_id": task["id"],
            "qp_gate_id": gate["id"],
            "minimum_proof_level": minimum_proof_level}
