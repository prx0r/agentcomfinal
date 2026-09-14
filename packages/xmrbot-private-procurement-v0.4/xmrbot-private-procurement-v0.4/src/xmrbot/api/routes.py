from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel
from xmrcomputer.models.domain import MachineProfile
from xmrbot.agent.plans import node_plan, wallet_plan
from xmrbot.core.economics import mine_or_buy, profitability
from xmrbot.core.methodology import METHODOLOGIES
from xmrbot.core.types import MineOrBuyRequest, ProfitabilityRequest
from xmrbot.content.blog import BlogPostInput
from xmrbot.content.events import detect_events
from xmrbot.content.workflows import workflow_for_event
from xmrbot.content.recipes import get_recipe, list_recipes, package_from_blog
from xmrbot.hardware.catalog import catalog
from xmrbot.integrations.xmrcomputer import opportunities
from xmrbot.knowledge.engine import engine
from xmrbot.config import settings
from xmrbot.site import site_map

router = APIRouter(prefix="/v1")

class MetricQuery(BaseModel):
    metric: str
    limit: int = 100

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class ResourceRequest(BaseModel):
    task: str

class NodePlanRequest(BaseModel):
    tor: bool = True
    prune: bool = False
    public_rpc: bool = False

class WalletPlanRequest(BaseModel):
    hardware_wallet: bool = False

class ComputerRequest(BaseModel):
    machine: MachineProfile
    include_mock: bool = False

class ProviderProposalRequest(BaseModel):
    action: str
    payload: dict = {}

class ProcurementRouteRequest(BaseModel):
    objective: str
    category: str | None = None
    max_xmr: float | None = None
    max_usd: float | None = None
    privacy_weight: float = 0.8
    escrow_required: bool = False
    max_kyc_level: int | None = None
    preferred_providers: list[str] = []

class GrantRequest(BaseModel):
    provider_id: str
    action: str
    payload: dict = {}
    max_xmr: float | None = None
    max_usd: float | None = None
    ttl_minutes: int = 30

class GateRequest(BaseModel):
    action: dict
    grant: dict | None = None
    amount_atomic_xmr: int | None = None
    amount_usd: float | None = None


def _require_editor(request: Request) -> None:
    if not settings.editor_token:
        raise HTTPException(503, "HTTP content writes are disabled. Set XMRBOT_EDITOR_TOKEN or use trusted local stdio MCP.")
    auth = request.headers.get("authorization", "")
    if auth != f"Bearer {settings.editor_token}":
        raise HTTPException(401, "invalid editor token")


def install_routes(services):
    @router.get("/site/map")
    def machine_site_map(): return site_map()

    @router.get("/network")
    def network():
        n = services.current_network()
        return n.model_dump(mode="json") | services.network_derived()

    @router.post("/network/refresh")
    async def refresh(): return await services.refresh_network()

    @router.get("/network/history")
    def history(limit: int = Query(default=100, ge=1, le=5000)):
        return [n.model_dump(mode="json") | {
            "hashprice_xmr_per_khs_day": n.hashprice_xmr_per_khs_day,
            "hashprice_usd_per_khs_day": n.hashprice_usd_per_khs_day,
        } for n in services.repo.network_history(limit)]

    @router.get("/mining/hashprice")
    def hashprice():
        n = services.current_network()
        return {"xmr_per_khs_day": n.hashprice_xmr_per_khs_day, "usd_per_khs_day": n.hashprice_usd_per_khs_day,
                "network_hashrate_hs": n.estimated_hashrate_hs, "methodology": "xmr-hashprice-v1", "source": n.source}

    @router.post("/mining/profitability")
    def mining_profitability(req: ProfitabilityRequest):
        return profitability(req, services.current_network())

    @router.post("/mining/mine-or-buy")
    def mining_mine_or_buy(req: MineOrBuyRequest):
        return mine_or_buy(req, services.current_network())

    @router.get("/hardware/cpus")
    def cpus(q: str | None = None):
        rows = catalog.search(q) if q else catalog.all()
        return [x.model_dump() for x in rows]

    @router.get("/hardware/cpus/{slug}")
    def cpu(slug: str):
        row = catalog.get(slug)
        if not row: raise HTTPException(404, "CPU not found")
        return row.model_dump()

    @router.get("/hardware/rankings")
    def rankings(electricity_usd_kwh: float = Query(default=0.10, ge=0)):
        return catalog.rankings(services.current_network(), electricity_usd_kwh)

    @router.post("/query")
    def metric_query(req: MetricQuery):
        allowed = {
            "hashprice_usd": "hashprice_usd_per_khs_day",
            "hashprice_xmr": "hashprice_xmr_per_khs_day",
            "difficulty": "difficulty",
            "hashrate": "estimated_hashrate_hs",
            "price": "xmr_usd",
        }
        if req.metric not in allowed:
            raise HTTPException(400, "unsupported metric")
        rows = services.repo.network_history(max(1, min(req.limit, 5000)))
        key = allowed[req.metric]
        data=[]
        for n in rows:
            value = getattr(n, key) if hasattr(n, key) else None
            data.append({"timestamp": n.timestamp, "value": value, "source": n.source})
        return {"metric": req.metric, "series": data}

    @router.get("/privacy/profile")
    def privacy_profile():
        return {"network":"tor-preferred","node":"local","wallet":"local-only","telemetry":"disabled-by-default","external_compute":"disabled-by-default","guarantee":"configuration profile, not an anonymity guarantee"}

    @router.post("/search")
    def search(req: SearchRequest): return {"results": engine.search(req.query, req.limit)}

    @router.post("/resource/find")
    def resource_find(req: ResourceRequest): return engine.resource_find(req.task)

    @router.post("/node/plan")
    def plan_node(req: NodePlanRequest): return node_plan(**req.model_dump())

    @router.post("/wallet/plan")
    def plan_wallet(req: WalletPlanRequest): return wallet_plan(**req.model_dump())

    @router.post("/computer/opportunities")
    async def computer_opportunities(req: ComputerRequest):
        return await opportunities(req.machine, services.current_network(), include_mock=req.include_mock)


    @router.get("/providers")
    def providers(q: str = ""):
        return {"providers": services.procurement.providers(q)}

    @router.get("/providers/{provider_id}")
    def provider(provider_id: str):
        try: return services.procurement.provider(provider_id)
        except KeyError: raise HTTPException(404, "provider not found")

    @router.post("/procurement/route")
    def procurement_route(req: ProcurementRouteRequest):
        return services.procurement.route(**req.model_dump())

    @router.post("/providers/{provider_id}/propose")
    def provider_propose(provider_id: str, req: ProviderProposalRequest):
        try: return services.procurement.propose(provider_id, req.action, req.payload)
        except KeyError as exc: raise HTTPException(400, str(exc))

    @router.post("/providers/{provider_id}/read")
    async def provider_read(provider_id: str, req: ProviderProposalRequest):
        try: return await services.procurement.invoke_read(provider_id, req.action, req.payload)
        except KeyError as exc: raise HTTPException(400, str(exc))
        except RuntimeError as exc: raise HTTPException(503, str(exc))

    @router.post("/qp/grant-request")
    def qp_grant_request(req: GrantRequest):
        return services.procurement.grant_request(**req.model_dump())

    @router.post("/qp/gate")
    def qp_gate(req: GateRequest):
        return services.procurement.gate(req.action, req.grant, req.amount_atomic_xmr, req.amount_usd)

    @router.get("/methodologies")
    def methodologies(): return METHODOLOGIES

    @router.get("/blocks/latest")
    def latest_block():
        n = services.current_network()
        return {"height": n.height, "timestamp": n.timestamp, "reward_xmr": n.reward_xmr, "source": n.source}

    @router.get("/fees")
    def fees():
        n = services.current_network()
        return {"fee_per_byte_atomic": n.fee_per_byte_atomic, "source": n.source}

    @router.get("/content/events")
    def content_events():
        history = services.repo.network_history(2)
        events = detect_events(history[-2] if len(history) > 1 else None, history[-1]) if history else []
        return [{**event, "workflow": workflow_for_event(event)} for event in events]

    @router.get("/content/recipes")
    def content_recipes(): return {"recipes": list_recipes()}

    @router.get("/content/recipes/{recipe_id}")
    def content_recipe(recipe_id: str):
        recipe = get_recipe(recipe_id)
        if not recipe: raise HTTPException(404, "recipe not found")
        return recipe

    @router.get("/content/from-blog/{slug}")
    def content_from_blog(slug: str):
        post = services.repo.get_blog(slug)
        if not post: raise HTTPException(404, "published blog post not found")
        return package_from_blog(post, settings.canonical_url)

    @router.get("/blog")
    def blog_index(limit: int = Query(default=50, ge=1, le=100)):
        return {"posts": [p.model_dump(mode="json") for p in services.repo.list_blog(limit, False)]}

    @router.get("/blog/{slug}")
    def blog_post(slug: str):
        post = services.repo.get_blog(slug, False)
        if not post: raise HTTPException(404, "blog post not found")
        return post.model_dump(mode="json")

    @router.get("/blog/{slug}/raw")
    def blog_raw(slug: str):
        post = services.repo.get_blog(slug, False)
        if not post: raise HTTPException(404, "blog post not found")
        return {"slug": post.slug, "title": post.title, "body_md": post.body_md, "source_refs": post.source_refs}

    @router.post("/blog/draft")
    def blog_draft(req: BlogPostInput, request: Request):
        _require_editor(request)
        return services.repo.upsert_blog_draft(req).model_dump(mode="json")

    @router.post("/blog/{slug}/publish")
    def blog_publish(slug: str, request: Request):
        _require_editor(request)
        try:
            return services.repo.publish_blog(slug).model_dump(mode="json")
        except KeyError:
            raise HTTPException(404, "blog draft not found")

    return router
