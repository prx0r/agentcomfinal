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


def run_lane(contract_root, candidate_sha, policy_id, work_fn, seed=7,
             base_sha=""):
    """Minimal lane execution through CG primitives: run the lane function
    (AgentCom-side work), then wrap the outcome as a CG-style RunReceipt
    reference {run_id (content-addressed), contract, candidate, policy,
    seed, events_root, metrics}. CG = experiment record; QP (elsewhere)
    remains truth. work_fn() -> {events[{kind, hash}], metrics{...}}."""
    _import()
    from cogym_kernel.kernel import ids as _ids
    out = work_fn() or {}
    events = out.get("events", [])
    event_hashes = [e if isinstance(e, str) else _ids.content_id(
        "event", {"kind": e.get("kind", "?"),
                  "hash": e.get("hash", "?")}) for e in events]
    events_root = _ids.events_root(event_hashes) if hasattr(_ids, "events_root") \
        else _ids.content_id("events", event_hashes)
    receipt = {"worldpack": "agentcom-lane",
               "scenario": {"contract_root": contract_root,
                            "candidate_sha": candidate_sha,
                            "policy_id": policy_id, "seed": seed,
                            "base_sha": base_sha},
               "candidate": {"sha": candidate_sha, "policy": policy_id},
               "events_root": events_root,
               "metrics": out.get("metrics", {})}
    receipt["run_id"] = _ids.content_id("run", {
        "worldpack": receipt["worldpack"], "scenario": receipt["scenario"],
        "candidate": candidate_sha, "seed": seed,
        "events_root": events_root})
    return receipt
