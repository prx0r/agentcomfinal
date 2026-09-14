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
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "autobuild1", "src"))
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "autobuild2", "src"))
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "autobuild3", "src"))

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


def test_mcp_authorize_roundtrip():
    from ab2 import crypto, grants
    secret, pub = crypto.keypair_from_seed_hex("ab" * 32)
    g = grants.issue(pub, "email.send", {}, [], "2026-12-31T00:00:00Z", secret)
    r = mcp_servers.call("qp.authorize",
                         {"action": "email.send", "grant": g,
                          "facts": {}, "now": "2026-09-14T00:00:00Z"})
    assert r == {"authorized": True, "reason": "ok"}
    r = mcp_servers.call("qp.authorize",
                         {"action": "email.send", "grant": {},
                          "facts": {}, "now": "2026-09-14T00:00:00Z"})
    assert r["authorized"] is False


def test_mcp_stdio_roundtrip():
    reqs = ('{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n'
            '{"jsonrpc":"2.0","id":2,"method":"tools/call",'
            '"params":{"name":"gg.search","arguments":{"query":"seesaw"}}}\n')
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [os.path.join(HERE, "..", "src"), ROOT,
         os.path.join(ROOT, "agentcombuild", "autobuild1", "src"),
         os.path.join(ROOT, "agentcombuild", "autobuild2", "src")]))
    p = subprocess.run([sys.executable, "-m", "opennative.mcp_servers"],
                       input=reqs, capture_output=True, text=True, timeout=60,
                       cwd=os.path.join(HERE, "..", "src"), env=env)
    lines = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
    assert len(lines) == 2 and "result" in lines[0] and "result" in lines[1]
    assert isinstance(lines[1]["result"]["candidates"], list)


# ---- vault + approvals ----

def test_vault_split():
    assert vault.classify("maps", {"kind": "read"})[0] == "VAULT"
    assert vault.classify("send", {"kind": "write"})[0] == "QP_GATEWAY"
    assert vault.classify("pay", {"kind": "write", "moves_value": True})[0] \
        == "QP_GATEWAY"
    for name, (got, _) in vault.check_examples().items():
        assert got in ("VAULT", "QP_GATEWAY"), name


def test_both_belts_and_bypass_proof():
    from ab2 import crypto, grants
    secret, pub = crypto.keypair_from_seed_hex("cd" * 32)
    g = grants.issue(pub, "email.send", {}, [], "2026-12-31T00:00:00Z", secret)
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
    assert out["mode"] == "SIMULATED"
    assert out["ok"] is True
    assert [s["name"] for s in out["steps"]] == [
        "session-bind", "mcp-read", "qp-authorize", "mcp-enforce",
        "readback", ]
    assert out["trajectory"]["level"] == "L0-observation"


def test_chain_readback_disagreement_stops():
    out = chain.run_chain(spec(), readback_ok=False)
    assert out["ok"] is False
    by_name = {s["name"]: s for s in out["steps"]}
    assert by_name["readback"]["ok"] is False
    assert by_name["qp-authorize"]["ok"] is True  # auth passed; reality didn't
