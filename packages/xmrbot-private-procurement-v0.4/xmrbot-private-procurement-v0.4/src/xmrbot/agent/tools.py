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
from xmrbot.content.blog import BlogPostInput
from xmrbot.content.recipes import get_recipe, list_recipes, package_from_blog
from xmrbot.config import settings
from xmrbot.site import llms_text, site_map
from xmrbot.procurement.models import ProcurementIntent


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

class BlogListInput(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    include_drafts: bool = False

class BlogGetInput(BaseModel):
    slug: str
    include_drafts: bool = False

class BlogDraftInput(BlogPostInput):
    pass

class BlogPublishInput(BaseModel):
    slug: str

class RecipeInput(BaseModel):
    recipe_id: str = ""

class BlogPackageInput(BaseModel):
    slug: str

class ProviderSearchInput(BaseModel):
    query: str = ""

class ProviderGetInput(BaseModel):
    provider_id: str

class ProcurementRouteInput(ProcurementIntent):
    pass

class ProviderProposalInput(BaseModel):
    provider_id: str
    action: str
    payload: dict = {}

class ProviderReadInput(ProviderProposalInput):
    pass

class GrantRequestInput(ProviderProposalInput):
    max_xmr: float | None = None
    max_usd: float | None = None
    ttl_minutes: int = Field(default=30, ge=1, le=1440)

class GateEvaluateInput(BaseModel):
    action: dict
    grant: dict | None = None
    amount_atomic_xmr: int | None = None
    amount_usd: float | None = None

class ReceiptVerifyInput(BaseModel):
    receipt: dict
    action: dict
    response: dict


class ToolRegistry:
    def __init__(self, services):
        self.services = services
        self.specs: dict[str, tuple[type[BaseModel], str, Any]] = {
            "xmr_tools": (ToolDiscoveryInput, "Discover XMRBot tools by category or keyword.", self._tools),
            "xmr_site_map": (BaseModel, "Return machine-readable navigation for all XMRBot human/API/MCP surfaces.", self._site_map),
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
            "xmr_blog_list": (BlogListInput, "List XMRBot blog posts. Draft visibility is opt-in.", self._blog_list),
            "xmr_blog_get": (BlogGetInput, "Read a XMRBot blog post and source metadata.", self._blog_get),
            "xmr_blog_draft": (BlogDraftInput, "Create or update a blog draft. State-changing content operation.", self._blog_draft),
            "xmr_blog_publish": (BlogPublishInput, "Publish an existing blog draft. State-changing content operation.", self._blog_publish),
            "xmr_content_recipe": (RecipeInput, "List content automation recipes or inspect one recipe.", self._recipe),
            "xmr_content_from_blog": (BlogPackageInput, "Create a source-preserving YouTube/Shorts/X/Instagram production package from a published blog post.", self._content_from_blog),
            "xmr_provider_list": (ProviderSearchInput, "List/search private-economy provider adapters and their exact integration modes.", self._provider_list),
            "xmr_provider_get": (ProviderGetInput, "Inspect one provider adapter, source evidence, capabilities and caveats.", self._provider_get),
            "xmr_procurement_route": (ProcurementRouteInput, "Route a lawful procurement objective across compatible XMR/private-economy providers without spending.", self._procurement_route),
            "xmr_provider_propose": (ProviderProposalInput, "Create a deterministic provider action proposal; never spends or changes provider state.", self._provider_propose),
            "xmr_provider_read": (ProviderReadInput, "Invoke only a provider read/quote/status capability. State-changing capabilities return proposals instead.", self._provider_read),
            "qp_grant_request": (GrantRequestInput, "Construct a bounded QP grant request bound to exact provider/action/payload; approval remains external.", self._grant_request),
            "qp_gate_evaluate": (GateEvaluateInput, "Deterministically evaluate a provider action against a QP grant.", self._gate_evaluate),
            "qp_receipt_verify": (ReceiptVerifyInput, "Verify deterministic integrity of a provider action receipt.", self._receipt_verify),
        }

    def metadata(self) -> list[ToolMeta]:
        out = []
        for name, (model, desc, _) in self.specs.items():
            risk = TOOL_RISK[name]
            out.append(ToolMeta(
                name=name, description=desc, risk_class=risk,
                requires_user_approval=risk.value.startswith("R1") or risk.value.startswith("R2"),
                touches_private_keys=False, moves_funds=False,
                network_access=name in {"xmr_network_status", "xmr_computer_opportunities", "xmr_provider_read"},
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

    def resources(self) -> list[dict]:
        resources = [
            {"uri": "xmrbot://site", "name": "XMRBot site map", "mimeType": "application/json"},
            {"uri": "xmrbot://llms", "name": "LLM navigation guide", "mimeType": "text/plain"},
            {"uri": "xmrbot://network", "name": "Current Monero network snapshot", "mimeType": "application/json"},
            {"uri": "xmrbot://blog", "name": "Published XMRBot blog index", "mimeType": "application/json"},
            {"uri": "xmrbot://recipes", "name": "Content automation recipes", "mimeType": "application/json"},
            {"uri": "xmrbot://providers", "name": "Private-economy provider registry", "mimeType": "application/json"},
        ]
        for provider in self.services.procurement.providers():
            resources.append({
                "uri": f"xmrbot://provider/{provider['id']}",
                "name": f"Provider: {provider['name']}",
                "mimeType": "application/json",
            })
        return resources

    def read_resource(self, uri: str):
        if uri == "xmrbot://site": return site_map()
        if uri == "xmrbot://llms": return llms_text()
        if uri == "xmrbot://network": return self._network()
        if uri == "xmrbot://blog": return self._blog_list(limit=100, include_drafts=False)
        if uri == "xmrbot://recipes": return {"recipes": list_recipes()}
        if uri == "xmrbot://providers": return {"providers": self.services.procurement.providers()}
        if uri.startswith("xmrbot://provider/"): return self.services.procurement.provider(uri.removeprefix("xmrbot://provider/"))
        if uri.startswith("xmrbot://blog/"):
            return self._blog_get(uri.removeprefix("xmrbot://blog/"), include_drafts=False)
        raise KeyError(f"unknown resource: {uri}")

    def _tools(self, category: str = ""):
        q = category.lower().strip()
        rows = [x.model_dump(mode="json") for x in self.metadata() if x.name != "xmr_tools"]
        if q:
            rows = [x for x in rows if q in (x["name"] + " " + x["description"]).lower()]
        return {"tools": rows}
    def _site_map(self): return site_map()
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
    def _blog_list(self, limit=20, include_drafts=False):
        return {"posts": [p.model_dump(mode="json") for p in self.services.repo.list_blog(limit, include_drafts)]}
    def _blog_get(self, slug: str, include_drafts=False):
        post = self.services.repo.get_blog(slug, include_drafts)
        if not post: raise KeyError(slug)
        return post.model_dump(mode="json")
    def _blog_draft(self, **kwargs):
        post = self.services.repo.upsert_blog_draft(BlogPostInput(**kwargs))
        return post.model_dump(mode="json")
    def _blog_publish(self, slug: str):
        return self.services.repo.publish_blog(slug).model_dump(mode="json")
    def _recipe(self, recipe_id=""):
        if not recipe_id: return {"recipes": list_recipes()}
        recipe = get_recipe(recipe_id)
        if not recipe: raise KeyError(recipe_id)
        return recipe
    def _content_from_blog(self, slug: str):
        post = self.services.repo.get_blog(slug, include_drafts=False)
        if not post: raise KeyError(slug)
        return package_from_blog(post, settings.canonical_url)
    def _provider_list(self, query=""): return {"providers": self.services.procurement.providers(query)}
    def _provider_get(self, provider_id: str): return self.services.procurement.provider(provider_id)
    def _procurement_route(self, **kwargs): return self.services.procurement.route(**kwargs)
    def _provider_propose(self, provider_id: str, action: str, payload: dict): return self.services.procurement.propose(provider_id, action, payload)
    async def _provider_read(self, provider_id: str, action: str, payload: dict): return await self.services.procurement.invoke_read(provider_id, action, payload)
    def _grant_request(self, provider_id: str, action: str, payload: dict, max_xmr=None, max_usd=None, ttl_minutes=30): return self.services.procurement.grant_request(provider_id, action, payload, max_xmr, max_usd, ttl_minutes)
    def _gate_evaluate(self, action: dict, grant: dict | None=None, amount_atomic_xmr=None, amount_usd=None): return self.services.procurement.gate(action, grant, amount_atomic_xmr, amount_usd)
    def _receipt_verify(self, receipt: dict, action: dict, response: dict): return self.services.procurement.verify_receipt(receipt, action, response)
