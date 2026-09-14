"""CG adapter: cogymkernel as canonical experiment executor (reference).

CG owns: deterministic runs, content-addressed RunReceipts, hard gates,
evolution recipes, experience. We own: contracts, truth, scheduling.
Adapter surface: version pin, executor smoke (proves the import path live),
lane->worldpack manifest translation. Full AsyncRunner episodes stay in
/cg (run there, bank receipts here) — never reimplemented.
"""
import os
import subprocess
import sys

CG_ROOT = "/home/ubuntu/cg"


def version():
    try:
        rev = subprocess.run(["git", "-C", CG_ROOT, "rev-parse", "HEAD"],
                             capture_output=True, text=True,
                             timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        rev = "unknown"
    return {"repo": CG_ROOT, "rev": rev, "kernel": "cogymkernel",
            "receipt": "content-addressed RunReceipt"}


def _import():
    if CG_ROOT not in sys.path:
        sys.path.insert(0, CG_ROOT)
    import cogym_kernel  # noqa: E402
    return cogym_kernel


def smoke():
    """Prove the import + executor path live: one deterministic action."""
    _import()
    from cogym_kernel import executors
    from cogym_kernel.kernel import contracts as _c
    action = _c.ActionSpec(kind="smoke", payload={"echo": "hi"},
                           estimated_cost=0.0)
    result = executors.DeterministicExecutor().execute(action)
    return {"executor": "det-v1", "status": result.status,
            "request_hash": result.request_hash,
            "response_hash": result.response_hash}


def lane_to_worldpack(contract_root, candidate_sha, policy_id, seed=7):
    """Translate a Seed0 lane into a cg worldpack-ish manifest (reference
    shape for running inside /cg; executed there, not here)."""
    return {"worldpack": "agentcom-lane",
            "scenario": {"contract_root": contract_root,
                         "candidate_sha": candidate_sha,
                         "policy_id": policy_id, "seed": seed},
            "candidate": {"sha": candidate_sha, "policy": policy_id}}
