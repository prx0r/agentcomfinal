"""Transition receipts. Unsigned V0 in attempt 1 (signing = attempt 2)."""
from . import gates
from .canonical import canonical, sha12

PROTOCOL = "ab1/0.1"


def transition(t, subject, state_before, proposal, evidence, calls, now):
    """calls: [(gate_id, inputs)]. Executes gates, settles, ids by content."""
    results = [gates.execute(gid, inp) for gid, inp in calls]
    passed = bool(results) and all(r["verdict"] == "PASS" for r in results)
    body = {"protocol": PROTOCOL, "transition": t, "subject": subject,
            "state_before": state_before, "proposal": proposal,
            "evidence": evidence, "gates": results, "now": now,
            "passed": passed, "proof_level": "V0-unsigned",
            "state_after": proposal if passed else state_before}
    rid = "receipt:" + sha12(canonical(body))
    return dict([("id", rid)] + list(body.items()))


def verify(receipt):
    """Recompute id from bytes, then re-execute every gate from stored inputs."""
    if not isinstance(receipt, dict) or "id" not in receipt:
        return False
    body = {k: v for k, v in receipt.items() if k != "id"}
    if receipt["id"] != "receipt:" + sha12(canonical(body)):
        return False
    for g in body.get("gates", []):
        fresh = gates.execute(g.get("id"), g.get("inputs"))
        if fresh["verdict"] != g.get("verdict"):
            return False
    return True
