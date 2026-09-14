"""openai-native-0 proof suite: bundle/skill/session/MCP/vault/approvals/chain."""
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "agentloop", "src"))

from opennative import approvals, bundle, chain, mcp_servers  # noqa: E402
from opennative import session, skill, vault  # noqa: E402

EX = os.path.join(HERE, "..", "examples")


def spec():
    with open(os.path.join(EX, "lead_business.json")) as fh:
        return json.load(fh)


# ---- bundle ----

def test_bundle_layout_complete():
    tree = bundle.build(spec())
    for path in bundle.LAYOUT:
        assert path in tree, path
    assert "business-operator" in tree["skills"]
    assert tree["agent/agent.json"]["policy"] == "autobuild-worker-v1"
    assert tree["security/tool-policy.json"]["authority"] == "qp-only"


def test_bundle_refuses_missing_lineage():
    bad = spec()
    del bad["contract_root"]
    with pytest.raises(ValueError):
        bundle.build(bad)


def test_bundle_writes(tmp_path):
    paths = bundle.write(bundle.build(spec()), str(tmp_path))
    assert len(paths) >= len(bundle.LAYOUT)
    assert os.path.exists(os.path.join(str(tmp_path), "agent", "agent.json"))


# ---- skill ----

def test_skill_from_policy():
    sk = skill.build_skill()
    assert "cannot declare completion" in sk["SKILL.md"].lower() or \
        "cannot declare completion" in sk["SKILL.md"]
    assert sk["policy.json"]["policy_id"] == "autobuild-worker-v1"
    assert "escalation" in sk["resources.json"]


# ---- session ----

def test_session_payload_keys():
    payload, warnings = session.session_payload(
        "gpt-6-astra", ["company.lookup"],
        {"project": "p", "campaign": "c", "contract": "cr",
         "plan": "pr", "policy": "pol", "extra-stays-local": "x"})
    assert set(payload["metadata"]) == {"project", "campaign", "contract",
                                        "plan", "policy"}
    assert warnings == []
    with pytest.raises(ValueError):
        session.session_payload("m", [], {"project": "p"})


def test_event_normalize_unknown_passthrough():
    rec = session.normalize_event({"type": "weird.future", "id": "e1"},
                                  {"contract": "cr"})
    assert rec["source"] == "openai.agents" and rec["contract_root"] == "cr"
    assert rec["qp_receipt"] is None and rec["raw_type"] == "weird.future"


def test_events_to_trajectory():
    evs = [{"id": "e1", "type": "tool.call", "tool": "cmail.send",
            "session_id": "s"},
           {"id": "e2", "type": "turn.end", "session_id": "s"}]
    t = session.events_to_trajectory(evs, {"contract": "cr"})
    assert t["tools_seen"] == ["cmail.send"] and t["event_count"] == 2


# ---- MCP ----

def test_mcp_tools_list_and_unknown():
    r = mcp_servers.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    names = [t["name"] for t in r["result"]["tools"]]
    assert {"qp.authorize", "qp.verify", "gg.search"} <= set(names)
    r = mcp_servers.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                            "params": {"name": "nope", "arguments": {}}})
    assert "error" in r


def _signed_grant(seed_hex="ab" * 32, cap="email.send", constraints=None,
                  predicates=None, expiry="2026-12-31T00:00:00Z"):
    from adapters import qp as _qp
    secret, pub = _qp.keypair(bytes.fromhex(seed_hex))
    g = _qp.make_grant(pub.hex(), cap, constraints or {}, predicates or [],
                       expiry)
    body = {k: v for k, v in g.items() if k not in ("id", "signature")}
    return dict(g, signature=_qp.sign_grant(secret, body))


def test_mcp_authorize_roundtrip():
    g = _signed_grant()
    r = mcp_servers.call("qp.authorize",
                         {"action": {"capability": "email.send"},
                          "grant": g, "facts": {},
                          "now": "2026-09-14T00:00:00Z"})
    assert r == {"authorized": True, "reason": "grant authorizes action"}
    r = mcp_servers.call("qp.authorize",
                         {"action": {"capability": "email.send"},
                          "grant": {}, "facts": {},
                          "now": "2026-09-14T00:00:00Z"})
    assert r["authorized"] is False


def test_mcp_verify_roundtrip():
    from adapters import qp as _qp
    claim = _qp.make_claim("s?", "d")
    claim = dict(claim, result="TRUE")
    task = _qp.make_task("t", "x", {})
    run = _qp.make_run(task["id"], "w", "m")
    ev = [_qp.make_evidence("m", 1, "u", "2026-09-14T00:00:00Z", {"class": "a"}),
          _qp.make_evidence("m", 2, "u", "2026-09-14T00:00:00Z", {"class": "b"})]
    receipt = _qp.settle_transition({"cursor": 0}, {"id": "t", "claim": claim},
                                    ev, ["two-sources-v1"], run)
    r = mcp_servers.call("qp.verify", {"receipt": receipt, "evidence": ev})
    assert r["valid"] is True
    bad = dict(receipt, id="receipt:0" * 2)
    r = mcp_servers.call("qp.verify", {"receipt": bad, "evidence": ev})
    assert r["valid"] is False


def test_mcp_stdio_roundtrip():
    reqs = ('{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n'
            '{"jsonrpc":"2.0","id":2,"method":"tools/call",'
            '"params":{"name":"gg.search","arguments":{"query":"seesaw"}}}\n')
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [os.path.join(HERE, "..", "src"), ROOT]))
    p = subprocess.run([sys.executable, "-m", "opennative.mcp_servers"],
                       input=reqs, capture_output=True, text=True, timeout=60,
                       cwd=os.path.join(HERE, "..", "src"), env=env)
    lines = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
    assert len(lines) == 2 and "result" in lines[0] and "result" in lines[1]
    body = json.loads(lines[1]["result"]["content"][0]["text"])
    assert isinstance(body["candidates"], list)


# ---- vault + approvals ----

def test_vault_split():
    assert vault.classify("maps", {"kind": "read"})[0] == "VAULT"
    assert vault.classify("send", {"kind": "write"})[0] == "QP_GATEWAY"
    assert vault.classify("pay", {"kind": "write", "moves_value": True})[0] \
        == "QP_GATEWAY"
    for name, (got, _) in vault.check_examples().items():
        assert got in ("VAULT", "QP_GATEWAY"), name


def test_both_belts_and_bypass_proof():
    g = _signed_grant("cd" * 32)
    act = {"capability": "email.send", "consequential": True}
    now = "2026-09-14T00:00:00Z"
    ok = approvals.decide(act, g, {}, now)
    assert ok["decision"] == "PROCEED"
    denied = approvals.decide(act, g, {}, now, approval="denied")
    assert denied["decision"] == "REFUSE"
    # bypass: approval says granted, but gateway sees no grant -> still refused
    forged = approvals.enforce("company.send_email",
                               {"grant": {}, "facts": {}, "now": now})
    assert forged["authorized"] is False
    assert approvals.request_approval({"consequential": False},
                                      "consequential-only")["needed"] is False


# ---- acceptance chain ----

def test_chain_acceptance():
    out = chain.run_chain(spec())
    assert out["mode"] == "SIMULATED-SERVICES-REAL-QP"
    assert out["ok"] is True
    assert [s["name"] for s in out["steps"]] == [
        "session-bind", "mcp-read", "qp-authorize", "mcp-enforce",
        "action", "readback", "qp-settle", "qp-verify", "trajectory-L1"]
    assert out["trajectory"]["level"] == "L1-fact"
    assert len(out["trajectory"]["qp_receipts"]) == 1
    assert out["receipt"]["id"] == out["trajectory"]["qp_receipts"][0]


def test_readback_false_mints_no_receipt():
    """Constitutional: reality precedes settlement. Readback FALSE means
    settlement is structurally unreachable — no receipt, no fact, L0."""
    out = chain.run_chain(spec(), readback_ok=False)
    assert out["ok"] is False
    assert out["receipt"] is None
    assert out["trajectory"]["qp_receipts"] == []
    assert out["trajectory"]["level"] == "L0-observation"
    assert out["trajectory"]["actuality_after"] != {"reply": "TRUE"}
    assert "qp-settle" not in [s["name"] for s in out["steps"]]


def test_settle_unreachable_on_false_readback(monkeypatch):
    """Even if settlement were attempted on the refusal path, it must not
    be reachable: monkeypatched settle raising still completes the run."""
    import opennative.chain as _chainmod
    from adapters import qp as _qp

    def boom(*a, **k):
        raise AssertionError("settlement attempted without TRUE readback")

    monkeypatch.setattr(_qp, "settle_transition", boom)
    out = _chainmod.run_chain(spec(), readback_ok=False)
    assert out["ok"] is False and out["receipt"] is None


def test_chain_readback_disagreement_stops():
    out = chain.run_chain(spec(), readback_ok=False)
    assert out["ok"] is False
    by_name = {s["name"]: s for s in out["steps"]}
    assert by_name["readback"]["ok"] is False
    assert by_name["qp-authorize"]["ok"] is True  # auth passed; reality didn't


def test_live_mode_refuses_without_key():
    from opennative import executor
    import os as _os
    if _os.environ.get("OPENAI_API_KEY"):
        pytest.skip("key present: live path is manual-only")
    ok, reason = executor.live_available()
    assert ok is False and reason in ("no-openai-package", "no-api-key",
                                      "no-sessions-create")
    with pytest.raises(executor.NotConfigured):
        executor.run_live("hi", lineage={"project": "p"})


def test_scripted_executor_offline():
    from opennative import executor
    out = executor.run_scripted(
        [{"tool": "gg.search", "args": {"query": "seesaw"}},
         {"tool": "evil.tool", "args": {}}],
        lineage={"contract": "cr:1"}, session_id="sess-t")
    assert out["mode"] == "SCRIPTED-OFFLINE"
    assert out["trajectory"]["tools_seen"] == ["gg.search"]
    assert out["errors"] == ["evil.tool"]  # unknown fails closed via gateway
    assert out["trajectory"]["event_count"] == 2


# ---- P0 fail-closed ----

def test_unknown_approval_policy_refuses():
    r = approvals.request_approval({}, "foobar")
    assert r == {"needed": True, "belt": "unknown-policy-refuse"}
    r = approvals.request_approval({}, None)
    assert r["needed"] is True
    r = approvals.request_approval({}, "never")
    assert r == {"needed": False, "belt": "none"}


def test_ungranted_approval_refuses():
    g = _signed_grant("ee" * 32)
    act = {"capability": "email.send", "consequential": True}
    now = "2026-09-14T00:00:00Z"
    for bad in ("skipped", None, "", "maybe"):
        d = approvals.decide(act, g, {}, now, approval=bad)
        assert d["decision"] == "REFUSE", bad


def test_unknown_tool_refuses():
    r = approvals.enforce("evil.deploy", {"now": "2026-09-14T00:00:00Z"})
    assert r == {"authorized": False, "reason": "unknown-tool:REFUSE"}
    r = approvals.enforce("company.lookup", {})
    assert r == {"authorized": True, "reason": "non-consequential"}


def test_unknown_credential_unclassified():
    assert vault.classify("x", {})[0] == "UNCLASSIFIED"
    assert vault.classify("x", None)[0] == "UNCLASSIFIED"
    assert vault.classify("x", {"kind": "unknown"})[0] == "UNCLASSIFIED"
    assert vault.classify("x", {"kind": "read"})[0] == "VAULT"
