from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field
from xmrcomputer.models.domain import MachineProfile
from xmrbot.core.economics import mine_or_buy, profitability
from xmrbot.core.risk import TOOL_RISK
from xmrbot.core.types import MineOrBuyRequest, ProfitabilityRequest, ToolMeta
from xmrbot.hardware.catalog import catalog
from xmrbot.knowledge.engine import engine
from xmrbot.agent.plans import node_plan, wallet_plan
from xmrbot.local.inspect import benchmark_estimate, inspect_machine
from xmrbot.integrations.xmrcomputer import opportunities


class ToolDiscoveryInput(BaseModel):
    category: str = ""

class SearchInput(BaseModel):
    query: str
    limit: int = Field(default=5, ge=1, le=20)

class CPUInput(BaseModel):
    query: str

class ResourceInput(BaseModel):
    task: str

class NodePlanInput(BaseModel):
    tor: bool = True
    prune: bool = False
    public_rpc: bool = False

class WalletPlanInput(BaseModel):
    hardware_wallet: bool = False

class ComputerInput(BaseModel):
    machine: MachineProfile
    include_mock: bool = False


class ToolRegistry:
    def __init__(self, services):
        self.services = services
        self.specs: dict[str, tuple[type[BaseModel], str, Any]] = {
            "xmr_tools": (ToolDiscoveryInput, "Discover XMRBot tools by category or keyword.", self._tools),
            "xmr_search": (SearchInput, "Search canonical Monero/XMRBot knowledge with provenance.", self._search),
            "xmr_network_status": (BaseModel, "Return current network, hashprice and source metadata.", self._network),
            "xmr_mining_profitability": (ProfitabilityRequest, "Calculate RandomX mining economics using current network state.", self._profit),
            "xmr_cpu_lookup": (CPUInput, "Find CPU RandomX benchmark records.", self._cpu),
            "xmr_mine_or_buy": (MineOrBuyRequest, "Compare buying XMR with mining over a scenario horizon.", self._mine_or_buy),
            "xmr_resource_find": (ResourceInput, "Route an agent task to the appropriate Monero primitive.", self._resource),
            "xmr_node_plan": (NodePlanInput, "Generate a safe local monerod deployment plan.", self._node_plan),
            "xmr_wallet_plan": (WalletPlanInput, "Generate a local-first wallet creation plan; never exports seed material.", self._wallet_plan),
            "xmr_machine_inspect": (BaseModel, "Inspect the local machine without changing state.", self._inspect),
            "xmr_machine_benchmark": (BaseModel, "Estimate RandomX benchmark from the hardware catalog; real execution is opt-in/future adapter.", self._benchmark),
            "xmr_computer_opportunities": (ComputerInput, "Rank xmr.computer workload opportunities in XMR terms.", self._opportunities),
        }

    def metadata(self) -> list[ToolMeta]:
        out = []
        for name, (model, desc, _) in self.specs.items():
            risk = TOOL_RISK[name]
            out.append(ToolMeta(
                name=name, description=desc, risk_class=risk,
                requires_user_approval=risk.value.startswith("R1") or risk.value.startswith("R2"),
                touches_private_keys=False, moves_funds=False,
                network_access=name in {"xmr_network_status", "xmr_computer_opportunities"},
                input_schema=model.model_json_schema() if model is not BaseModel else {"type": "object", "properties": {}},
            ))
        return out

    async def call(self, name: str, arguments: dict | None = None):
        if name not in self.specs:
            raise KeyError(f"unknown tool: {name}")
        model, _, fn = self.specs[name]
        args = {} if model is BaseModel else model.model_validate(arguments or {}).model_dump()
        result = fn(**args)
        if hasattr(result, "__await__"):
            result = await result
        return result

    def _tools(self, category: str = ""):
        q = category.lower().strip()
        rows = [x.model_dump(mode="json") for x in self.metadata() if x.name != "xmr_tools"]
        if q:
            rows = [x for x in rows if q in (x["name"] + " " + x["description"]).lower()]
        return {"tools": rows}
    def _search(self, query: str, limit: int = 5): return {"results": engine.search(query, limit)}
    def _network(self): return self.services.current_network().model_dump(mode="json") | self.services.network_derived()
    def _profit(self, **kwargs): return profitability(ProfitabilityRequest(**kwargs), self.services.current_network()).model_dump()
    def _cpu(self, query: str): return {"results": [x.model_dump() for x in catalog.search(query)]}
    def _mine_or_buy(self, **kwargs): return mine_or_buy(MineOrBuyRequest(**kwargs), self.services.current_network())
    def _resource(self, task: str): return engine.resource_find(task)
    def _node_plan(self, **kwargs): return node_plan(**kwargs)
    def _wallet_plan(self, **kwargs): return wallet_plan(**kwargs)
    def _inspect(self): return inspect_machine()
    def _benchmark(self): return benchmark_estimate()
    async def _opportunities(self, machine, include_mock=False):
        if isinstance(machine, dict): machine = MachineProfile.model_validate(machine)
        return await opportunities(machine, self.services.current_network(), include_mock=include_mock)
