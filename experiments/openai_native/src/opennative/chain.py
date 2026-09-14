"""Acceptance chain (REAL QP, REAL order): action -> provider response ->
independent readback -> normalized evidence -> judges -> QP settlement.

Constitutional order: REALITY PRECEDES SETTLEMENT. QP evidence is built
ONLY from observations that already exist (action evidence + agreeing
readback). If readback is not TRUE, settlement is structurally unreachable:
no evidence is constructed, settle is never called, no receipt exists,
trajectory stays L0. Tests prove this by making settle raise.

Services (MCP transport, provider channels) are simulated and labeled;
authority and settlement are real ~/qp entrypoints via adapters/qp.
No network, no key, no spend.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", "..", ".."))
for _d in ("experiments/openai_native/src",):
    _p = os.path.join(ROOT, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from adapters import qp as _qp  # noqa: E402 - real QP, never ab2
from autobuild.actuality import readback as _rb  # noqa: E402 - canonical
from opennative import approvals, mcp_servers, session  # noqa: E402
from trajectory import trajectory as _traj  # noqa: E402

NOW = "2026-09-14T00:00:00Z"
DEMO_SEED = bytes.fromhex(
    "9d61b19deffd5a60ba844af492ec2af44449c5697b326919703bac031cae58d1")


def settle_send(grant, evidence):
    """REAL QP settlement. Call ONLY with evidence built from already-
    observed reality (action response + agreeing readback)."""
    claim = _qp.make_claim("lead-123 reply delivered", "email")
    claim = dict(claim, result="TRUE")
    task = _qp.make_task("send", "lead-123", {"delivered": True})
    run = _qp.make_run(task["id"], "chain-sim", "sim")
    proposal = {"id": task["id"], "claim": claim, "grant": grant["id"]}
    receipt = _qp.settle_transition(
        {"cursor": 0}, proposal, evidence,
        ["two-sources-v1", "evidence-fresh-v1", "no-duplicate-v1"], run,
        proof_level=9)
    return receipt, _qp.verify_settlement(receipt, evidence)


def run_chain(spec, readback_ok=True):
    """Run the full acceptance chain. Returns
    {ok, steps[{name, ok, detail}], trajectory, receipt|None}."""
    steps = []

    def step(name, ok, detail=""):
        steps.append({"name": name, "ok": bool(ok), "detail": detail})
        return ok

    # 1. session bind
    payload, _ = session.session_payload(
        spec.get("model", "gpt-6-astra"), ["company.lookup", "company.send_email"],
        {"project": spec["project"], "campaign": spec["campaign"],
         "contract": spec["contract_root"], "plan": spec.get("plan_root", ""),
         "policy": spec.get("policy_id", "autobuild-worker-v1")},
        user_input="Handle one inbound lead.")
    step("session-bind", payload["metadata"]["contract"] == spec["contract_root"],
         "metadata lineage keys bound")

    # 2. non-consequential MCP read (no grant needed)
    read = mcp_servers.call("gg.search", {"query": "lead reply"})
    step("mcp-read", isinstance(read.get("candidates"), list), "simulated read")

    # 3. real QP grant + both belts for the consequential send
    secret, pub = _qp.keypair(DEMO_SEED)
    grant = _qp.make_grant(pub.hex(), "email.send", {"max_risk_usd": 50},
                           ["risk_usd <= 50"], "2026-12-31T00:00:00Z")
    body = {k: v for k, v in grant.items() if k not in ("id", "signature")}
    grant = dict(grant, signature=_qp.sign_grant(secret, body))
    facts = {"risk_usd": 5, "calls_made": 0}
    action = {"capability": "email.send", "risk_usd": 5}
    dec = approvals.decide(dict(action, consequential=True),
                           grant, facts, NOW)
    step("qp-authorize", dec["decision"] == "PROCEED", dec.get("reason", ""))
    enforced = approvals.enforce("company.send_email",
                                 {"grant": grant, "facts": facts, "now": NOW})
    step("mcp-enforce", bool(enforced.get("authorized")), "gateway enforced")

    # 4. MCP action execution (simulated provider response — observation)
    action_ev = {"created_id": "lead-123", "status": 202, "source": "mcp-send"}
    step("action", action_ev["status"] == 202, "provider response observed")

    # 5. independent readback + judge (simulated independent channel)
    readback_ev = {"created_id": "lead-123" if readback_ok else "lead-999",
                   "source": "provider-api"}
    val, detail = _rb.check_readback(action_ev, readback_ev)
    step("readback", val == "TRUE", detail)

    # 6. QP settlement happens ONLY here, ONLY on TRUE, built ONLY from
    # observations already in hand. Otherwise structurally unreachable.
    receipt = None
    if val == "TRUE":
        evidence = [
            _qp.make_evidence("send.status", action_ev["status"], "http", NOW,
                              {"class": "mcp-send"}),
            _qp.make_evidence("readback.found_id",
                              readback_ev["created_id"], "id", NOW,
                              {"class": "provider-api"}),
        ]
        receipt, check = settle_send(grant, evidence)
        step("qp-settle", bool(check.get("ok")), check.get("reason", ""))
        signed = _qp.sign_receipt(secret, receipt)
        recheck = _qp.verify_settlement(signed, evidence)
        step("qp-verify", bool(recheck.get("ok")), "independent re-settlement")
        receipt = signed

    # 7. trajectory: receipt-bearing advances L0 -> L1; anything else stays L0
    traj = _traj.build(spec["contract_root"], spec.get("plan_root", ""),
                       spec.get("policy_id", "autobuild-worker-v1"),
                       [{"step": s["name"], "ok": s["ok"]} for s in steps],
                       {"reply": "UNKNOWN"}, {"reply": "TRUE" if receipt
                                                       else "UNKNOWN"},
                       qp_receipts=[receipt["id"]] if receipt else [],
                       cost={"tokens": None, "wall_ms": None, "usd": 0,
                             "human_minutes": 0})
    if receipt:
        traj, adv_ok, _ = _traj.advance(traj, {"qp_receipt": receipt["id"]})
        step("trajectory-L1", adv_ok, "receipt-bearing trajectory advances")
    ok = all(s["ok"] for s in steps)
    return {"ok": ok, "steps": steps, "trajectory": traj,
            "receipt": receipt, "mode": "SIMULATED-SERVICES-REAL-QP"}
