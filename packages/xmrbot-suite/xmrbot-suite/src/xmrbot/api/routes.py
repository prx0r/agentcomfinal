from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from xmrcomputer.models.domain import MachineProfile
from xmrbot.agent.plans import node_plan, wallet_plan
from xmrbot.core.economics import mine_or_buy, profitability
from xmrbot.core.methodology import METHODOLOGIES
from xmrbot.core.types import MineOrBuyRequest, ProfitabilityRequest
from xmrbot.content.events import detect_events
from xmrbot.content.workflows import workflow_for_event
from xmrbot.hardware.catalog import catalog
from xmrbot.integrations.xmrcomputer import opportunities
from xmrbot.knowledge.engine import engine

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


def install_routes(services):
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

    return router
