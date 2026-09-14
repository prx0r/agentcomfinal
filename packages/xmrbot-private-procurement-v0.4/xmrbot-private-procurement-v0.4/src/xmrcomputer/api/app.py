from fastapi import FastAPI
from pydantic import BaseModel, Field
from xmrcomputer.core.economics import RandomXNetwork, randomx_xmr_per_hour
from xmrcomputer.core.scheduler import Scheduler
from xmrcomputer.markets.randomx import RandomXAdapter
from xmrcomputer.markets.mock_compute import MockComputeAdapter
from xmrcomputer.models.domain import MachineProfile
from xmrcomputer.models.settings import Policy

app = FastAPI(title="xmr.computer", version="0.1.0")
DEFAULT_NETWORK = RandomXNetwork(network_hashrate_hs=5.9e9)
DEFAULT_ADAPTERS = [RandomXAdapter(DEFAULT_NETWORK), MockComputeAdapter()]

class DecisionRequest(BaseModel):
    machine: MachineProfile
    xmr_usd: float = Field(gt=0)
    policy: Policy = Field(default_factory=Policy)

class EstimateRequest(BaseModel):
    hashrate_hs: float = Field(gt=0)
    network_hashrate_hs: float = Field(default=5.9e9, gt=0)

@app.get('/health')
def health():
    return {"ok": True}

@app.get('/v1/markets')
def markets():
    return [{"name": a.name} for a in DEFAULT_ADAPTERS]

@app.post('/v1/randomx/estimate')
def estimate(req: EstimateRequest):
    network = RandomXNetwork(network_hashrate_hs=req.network_hashrate_hs)
    hourly = randomx_xmr_per_hour(req.hashrate_hs, network)
    return {"xmr_hour": hourly, "xmr_day": hourly * 24, "xmr_year": hourly * 24 * 365}

@app.post('/v1/decision')
async def decision(req: DecisionRequest):
    scheduler = Scheduler(DEFAULT_ADAPTERS, req.policy)
    return await scheduler.decide(req.machine, xmr_usd=req.xmr_usd)
