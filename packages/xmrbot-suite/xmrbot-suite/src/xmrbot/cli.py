from __future__ import annotations
import asyncio
import json
import typer
from xmrbot.services import Services
from xmrbot.hardware.catalog import catalog
from xmrbot.core.economics import profitability
from xmrbot.core.types import ProfitabilityRequest

app = typer.Typer(help="XMRBot CLI")

@app.command()
def network():
    s = Services(); print(json.dumps(s.current_network().model_dump(mode="json") | s.network_derived(), indent=2))

@app.command()
def cpus(query: str = ""):
    rows = catalog.search(query) if query else catalog.all()
    print(json.dumps([x.model_dump() for x in rows], indent=2))

@app.command()
def profit(hashrate: float, watts: float, electricity: float = 0.10, hardware: float = 0, months: float = 0):
    s = Services(); req = ProfitabilityRequest(hashrate_hs=hashrate, watts=watts, electricity_usd_kwh=electricity, hardware_cost_usd=hardware, amortization_months=months)
    print(json.dumps(profitability(req, s.current_network()).model_dump(), indent=2))

if __name__ == "__main__": app()
