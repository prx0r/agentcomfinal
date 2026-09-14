"""ab2 build: ab1 pipeline + L1 grant gates + V1 signing."""
from ab1 import gates, receipts, seesaw, specgate
from ab1.canonical import canonical

from . import crypto
from . import gates2  # noqa: F401 - registers L1 gates  # pylint: disable=unused-import


def consequential_actions(plan):
    out = []
    for f in plan.get("features", []):
        if isinstance(f, dict) and f.get("consequential") and f.get("capability"):
            out.append(f["capability"])
    return sorted(set(out))


def sign_receipt(secret, pub_hex, receipt):
    from ab1.canonical import sha12, canonical
    body = {k: v for k, v in receipt.items()
            if k not in ("id", "signer", "signature")}
    body["proof_level"] = "V1-signed"
    rid = "receipt:" + sha12(canonical(body))
    sig = crypto.sign_hex(secret, rid.encode("utf-8"))
    return dict([("id", rid)] + list(body.items()) +
                [("signer", pub_hex), ("signature", sig)])


def verify_signed(receipt, pub_hex):
    r = gates.execute("receipt-signed-v1",
                      {"receipt": receipt, "pubkey": pub_hex})
    return r["verdict"] == "PASS"


def build(plan, evidence, grants_map, secret, pub_hex, now, min_score=0.0):
    """grants_map: {capability: {"grant":..., "facts":...}}. secret None skips signing."""
    verdict = specgate.check_plan(plan)
    proj = seesaw.score_project(plan.get("features", []))
    needed = consequential_actions(plan)
    state_before = {"cursor": 0, "projects": {}}
    proposal = {"cursor": 1, "projects": {
        plan.get("id", "plan"): {"status": "SCORED", "value": proj["value"],
                                 "binding": proj["binding"],
                                 "actions": {s["id"]: s["action"]
                                             for s in proj["scores"]}}}}
    calls = [("specgate-v1", {"spec_verdict": verdict}),
             ("evidence-declared-v1", {"features": plan.get("features", [])}),
             ("two-sources-v1", {"sources": evidence.get("sources", [])}),
             ("score-threshold-v1", {"value": proj["value"], "min": min_score}),
             ("no-duplicate-v1", {"items": [f.get("id") for f in
                                            plan.get("features", [])]})]
    if needed:
        calls.append(("consequential-requires-grant-v1",
                      {"actions": needed, "grants": grants_map, "now": now}))
    r = receipts.transition("BUILD", plan.get("id", "plan"), state_before,
                            proposal,
                            {"plan": plan.get("id"),
                             "sources": evidence.get("sources", [])},
                            calls, now)
    if r["passed"] and secret is not None:
        r = sign_receipt(secret, pub_hex, r)
    view = {"receipt": r, "scores": proj, "spec": verdict,
            "consequential": needed}
    return view
