import pytest
from xmrbot.agent.tools import ToolRegistry
from xmrbot.mcp.server import MCPServer, PROTOCOL_VERSION
from xmrbot.services import Services

@pytest.mark.asyncio
async def test_initialize():
    s=MCPServer(ToolRegistry(Services(":memory:")))
    r=await s.handle({"jsonrpc":"2.0","id":1,"method":"initialize","params":{}})
    assert r["result"]["protocolVersion"]==PROTOCOL_VERSION

@pytest.mark.asyncio
async def test_tools_list_contains_core_tools():
    s=MCPServer(ToolRegistry(Services(":memory:")))
    r=await s.handle({"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}})
    names={t["name"] for t in r["result"]["tools"]}
    assert {"xmr_network_status","xmr_mining_profitability","xmr_mine_or_buy","xmr_computer_opportunities"} <= names

@pytest.mark.asyncio
async def test_tool_call_structured_result():
    s=MCPServer(ToolRegistry(Services(":memory:")))
    r=await s.handle({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"xmr_cpu_lookup","arguments":{"query":"7950X"}}})
    assert r["result"]["structuredContent"]["results"][0]["model"]=="Ryzen 9 7950X"
    assert r["result"]["isError"] is False

@pytest.mark.asyncio
async def test_unknown_tool_is_error():
    s=MCPServer(ToolRegistry(Services(":memory:")))
    r=await s.handle({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"wallet.export_seed","arguments":{}}})
    assert "error" in r

@pytest.mark.asyncio
async def test_tool_discovery_filters():
    s=MCPServer(ToolRegistry(Services(":memory:")))
    r=await s.handle({"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"xmr_tools","arguments":{"category":"mining"}}})
    assert any("mining" in t["name"] or "mining" in t["description"].lower() for t in r["result"]["structuredContent"]["tools"])
