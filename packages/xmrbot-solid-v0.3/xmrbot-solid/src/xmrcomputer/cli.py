import asyncio
import json
import typer
from xmrcomputer.core.economics import RandomXNetwork
from xmrcomputer.core.scheduler import Scheduler
from xmrcomputer.markets.randomx import RandomXAdapter
from xmrcomputer.markets.mock_compute import MockComputeAdapter
from xmrcomputer.models.domain import MachineProfile
from xmrcomputer.models.settings import Policy

app = typer.Typer(help="xmr.computer CPU opportunity router")

@app.command()
def decide(
    hashrate: float = typer.Option(..., help="RandomX hashrate in H/s"),
    watts: float = typer.Option(...),
    electricity: float = typer.Option(..., help="USD/kWh"),
    xmr_price: float = typer.Option(..., help="USD/XMR"),
    network_hashrate: float = typer.Option(5.9e9, help="Network H/s"),
):
    machine = MachineProfile(hashrate_hs=hashrate, watts_at_load=watts, electricity_usd_kwh=electricity)
    scheduler = Scheduler(
        [RandomXAdapter(RandomXNetwork(network_hashrate_hs=network_hashrate)), MockComputeAdapter()],
        Policy(),
    )
    result = asyncio.run(scheduler.decide(machine, xmr_usd=xmr_price))
    typer.echo(json.dumps(result.model_dump(), indent=2, default=str))
