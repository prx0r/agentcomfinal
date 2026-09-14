"""Acceptance chain (brief acceptance, SIMULATED): one session -> one MCP
action -> one QP-authorized transition -> one independent readback -> one
full trajectory. Every step labeled simulation; no network, no key, no
spend. Live operation swaps the sim doubles for real services without
changing the chain shape.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", "..", ".."))
for _d in ("agentcombuild/autobuild1/src", "agentcombuild/autobuild2/src",
           "agentcombuild/autobuild3/src", "experiments/openai_native/src"):
    _p = os.path.join(ROOT, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ab2 import crypto, grants  # noqa: E402
from ab3 import readback as _rb  # noqa: E402
from opennative import approvals, mcp_servers, session  # noqa: E402
from trajectory import trajectory as _traj  # noqa: E402

NOW = "2026-09-14T00:00:00Z"
DEMO_SEED = "9d61b19deffd5a60ba844af492ec2af44449c5697b326919703bac031cae58d1"


def run_chain(spec, readback_ok=True):
    """Run the full acceptance chain in simulation. Returns
    {ok, steps[{name, ok, detail}], trajectory}."""
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

    # 3+4. grant + both belts for the consequential send
    secret, pub = crypto.keypair_from_seed_hex(DEMO_SEED)
    grant = grants.issue(pub, "email.send", {"max_risk_usd": 50},
                         [{"key": "facts.amount_usd", "op": "<=", "lit": 50}],
                         "2026-12-31T00:00:00Z", secret)
    facts = {"amount_usd": 5, "calls_made": 0}
    dec = approvals.decide({"capability": "email.send", "consequential": True},
                           grant, facts, NOW)
    step("qp-authorize", dec["decision"] == "PROCEED", dec.get("reason", ""))
    enforced = approvals.enforce("company.send_email",
                                 {"grant": grant, "facts": facts, "now": NOW})
    step("mcp-enforce", bool(enforced.get("authorized")), "gateway enforced")

    # 5. independent readback (simulated provider channel)
    action_ev = {"created_id": "lead-123", "source": "mcp-send"}
    readback_ev = {"created_id": "lead-123" if readback_ok else "lead-999",
                   "source": "provider-api"}
    val, detail = _rb.check_readback(action_ev, readback_ev)
    step("readback", val == "TRUE", detail)

    # 6. trajectory
    traj = _traj.build(spec["contract_root"], spec.get("plan_root", ""),
                       spec.get("policy_id", "autobuild-worker-v1"),
                       [{"step": s["name"], "ok": s["ok"]} for s in steps],
                       {"reply": "UNKNOWN"}, {"reply": "TRUE" if val == "TRUE"
                                                       else "UNKNOWN"},
                       qp_receipts=[],
                       cost={"tokens": None, "wall_ms": None, "usd": 0,
                             "human_minutes": 0})
    ok = all(s["ok"] for s in steps)
    return {"ok": ok, "steps": steps, "trajectory": traj,
            "mode": "SIMULATED"}
