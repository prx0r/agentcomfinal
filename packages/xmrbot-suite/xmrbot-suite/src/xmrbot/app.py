from __future__ import annotations
from importlib.resources import files
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from xmrbot import __version__
from xmrbot.agent.tools import ToolRegistry
from xmrbot.api.routes import install_routes
from xmrbot.mcp.server import MCPServer
from xmrbot.services import Services

services = Services()
registry = ToolRegistry(services)
mcp = MCPServer(registry)
app = FastAPI(title="XMRBot", version=__version__, description="Monero intelligence, mining economics and agent/MCP interface")
app.include_router(install_routes(services))

static_dir = files("xmrbot.web").joinpath("static")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/health")
def health(): return {"ok": True, "version": __version__, "network_source": services.current_network().source}

@app.get("/v1/tools")
def tools(): return [t.model_dump(mode="json") for t in registry.metadata()]

@app.post("/mcp")
async def mcp_http(request: Request):
    body = await request.json()
    response = await mcp.handle(body)
    return response or {"ok": True}

@app.get("/")
def home(): return FileResponse(str(static_dir.joinpath("index.html")))
@app.get("/terminal")
def terminal(): return FileResponse(str(static_dir.joinpath("terminal.html")))
@app.get("/mine")
def mine(): return FileResponse(str(static_dir.joinpath("mine.html")))
@app.get("/ask")
def ask(): return FileResponse(str(static_dir.joinpath("ask.html")))
@app.get("/cpu/{slug}")
def cpu_page(slug: str): return FileResponse(str(static_dir.joinpath("cpu.html")))
