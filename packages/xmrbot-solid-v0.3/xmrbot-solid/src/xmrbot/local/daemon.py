from __future__ import annotations
import typer
import uvicorn
from fastapi import FastAPI
from xmrbot.local.inspect import benchmark_estimate, inspect_machine
from xmrbot.agent.plans import node_plan, wallet_plan

app = typer.Typer(help="Local-first XMRBot companion. It never exports wallet seeds/private keys.")
local_api = FastAPI(title="xmrbotd", version="0.2.0")

@local_api.get("/health")
def health(): return {"ok": True, "bind_policy": "localhost-only"}

@local_api.get("/v1/machine")
def machine(): return inspect_machine()

@local_api.get("/v1/benchmark")
def benchmark(): return benchmark_estimate()

@local_api.get("/v1/privacy")
def privacy():
    return {"network":"tor-preferred","node":"local","wallet":"local-only","telemetry":"disabled-by-default","external_compute":"disabled-by-default"}

@app.command("inspect")
def cmd_inspect():
    import json; print(json.dumps(inspect_machine(), indent=2))

@app.command("benchmark")
def cmd_benchmark():
    import json; print(json.dumps(benchmark_estimate(), indent=2))

@app.command("node-plan")
def cmd_node_plan(tor: bool = True, prune: bool = False):
    import json; print(json.dumps(node_plan(tor=tor, prune=prune), indent=2))

@app.command("wallet-plan")
def cmd_wallet_plan(hardware_wallet: bool = False):
    import json; print(json.dumps(wallet_plan(hardware_wallet=hardware_wallet), indent=2))

@app.command("serve")
def serve(host: str = "127.0.0.1", port: int = 47831):
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise typer.BadParameter("xmrbotd binds to localhost only by default")
    uvicorn.run(local_api, host=host, port=port)

if __name__ == "__main__":
    app()
