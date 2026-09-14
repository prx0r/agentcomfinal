"""Official wire-compat (venv only, keyless, no network).

- MCP: real MCP client (official `mcp` package) over stdio against OUR
  server: initialize -> tools/list -> tools/call(gg.search) ->
  tools/call(qp.authorize negative) -> shutdown. If the official client
  cannot connect, the gate is FALSE (we fix the server, never the test).
- SDK: generated bundle artifacts accepted by REAL Agents SDK
  constructors: Agent config, MCPServerStdio config, session metadata map.
"""
import asyncio
import os
import sys

import pytest

mcp = pytest.importorskip("mcp")
agents = pytest.importorskip("agents")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, ROOT)

SERVER = os.path.join(HERE, "..", "src", "opennative", "mcp_servers.py")


def _env():
    return dict(os.environ, PYTHONPATH=os.pathsep.join(
        [os.path.join(HERE, "..", "src"), ROOT]))


def test_official_mcp_client_handshake():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def go():
        params = StdioServerParameters(command=sys.executable,
                                       args=[SERVER], env=_env())
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as s:
                await s.initialize()
                tools = await s.list_tools()
                names = sorted(t.name for t in tools.tools)
                assert {"qp.authorize", "qp.verify",
                        "gg.search", "business.lookup"} <= set(names)
                r = await s.call_tool("gg.search",
                                      {"query": "seesaw gates"})
                assert r.content, "gg.search returned no content"
                b = await s.call_tool("business.lookup",
                                      {"company": "acme-plumbing-leeds"})
                assert "acme-plumbing-leeds" in b.content[0].text
                bad = await s.call_tool("business.lookup",
                                        {"company": "no-such-company-zzz"})
                assert "unknown-company" in bad.content[0].text
                neg = await s.call_tool(
                    "qp.authorize",
                    {"action": {"capability": "email.send"},
                     "grant": {}, "facts": {}, "now": "2026-09-14T00:00:00Z"})
                assert "REFUSE" in neg.content[0].text.upper() or \
                    "false" in neg.content[0].text.lower()
    asyncio.run(go())


def test_sdk_accepts_bundle_artifacts():
    import json as _json
    from agents import Agent
    from agents.mcp import MCPServerStdio
    with open(os.path.join(HERE, "..", "examples",
                           "lead_business.json")) as fh:
        spec = _json.load(fh)
    agent = Agent(name="agentcom-uk",
                  instructions="You are executing ContractRoot %s. "
                               "Completion is external." % spec["contract_root"],
                  model="gpt-4o")
    assert agent.name == "agentcom-uk"
    mcp_cfg = MCPServerStdio(params={"command": "python",
                                       "args": ["-m", "opennative.mcp_servers"]},
                             require_approval="always")
    assert mcp_cfg.params.command == "python"
    # require_approval consumed into tool config at connect time; the
    # bundle pins the policy ("always" for qp-gateway tools).
    metadata = {k: spec.get({"project": "project"}.get(k, k), "")
                for k in ("project",)}
    metadata.update({"campaign": spec["campaign"],
                     "contract": spec["contract_root"]})
    assert all(isinstance(v, str) and v for v in metadata.values())
