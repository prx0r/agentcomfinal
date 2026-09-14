from __future__ import annotations
from html import escape
from importlib.resources import files
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from xmrbot import __version__
from xmrbot.agent.tools import ToolRegistry
from xmrbot.api.routes import install_routes
from xmrbot.config import settings
from xmrbot.core.risk import TOOL_RISK
from xmrbot.mcp.server import MCPServer
from xmrbot.services import Services
from xmrbot.site import llms_text, site_map

services = Services()
registry = ToolRegistry(services)
mcp = MCPServer(registry)
app = FastAPI(
    title="XMRBot",
    version=__version__,
    description="Monero intelligence, mining economics, source-linked publishing and agent/MCP interface",
)
app.include_router(install_routes(services))

static_dir = files("xmrbot.web").joinpath("static")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def _require_http_mcp_write_auth(request: Request, body: dict) -> None:
    if body.get("method") != "tools/call":
        return
    name = body.get("params", {}).get("name", "")
    risk = TOOL_RISK.get(name)
    if not risk or risk.value.startswith("R0"):
        return
    if not settings.editor_token:
        raise HTTPException(503, "State-changing MCP calls over HTTP are disabled. Use local stdio MCP or configure XMRBOT_EDITOR_TOKEN.")
    if request.headers.get("authorization", "") != f"Bearer {settings.editor_token}":
        raise HTTPException(401, "invalid editor token")


@app.get("/health")
def health(): return {"ok": True, "version": __version__, "network_source": services.current_network().source}

@app.get("/v1/tools")
def tools(): return [t.model_dump(mode="json") for t in registry.metadata()]

@app.post("/mcp")
async def mcp_http(request: Request):
    body = await request.json()
    _require_http_mcp_write_auth(request, body)
    response = await mcp.handle(body)
    return response or {"ok": True}

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"User-agent: *\nAllow: /\nSitemap: {settings.canonical_url}/sitemap.xml\n\n# Agent/LLM discovery\n# {settings.canonical_url}/llms.txt\n# {settings.canonical_url}/v1/site/map\n"

@app.get("/llms.txt", response_class=PlainTextResponse)
@app.get("/.well-known/llms.txt", response_class=PlainTextResponse)
def llms(): return llms_text()

@app.get("/.well-known/xmrbot.json")
def well_known(): return site_map()

@app.get("/sitemap.xml")
def sitemap():
    base = settings.canonical_url
    paths = ["/", "/terminal", "/mine", "/ask", "/blog", "/providers", "/recipes", "/docs", "/llms.txt"]
    paths += [f"/cpu/{c.slug}" for c in __import__("xmrbot.hardware.catalog", fromlist=["catalog"]).catalog.all()]
    paths += [f"/blog/{p.slug}" for p in services.repo.list_blog(500, False)]
    urls = "".join(f"<url><loc>{escape(base + p)}</loc></url>" for p in paths)
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', media_type="application/xml")

@app.get("/blog/feed.xml")
def blog_feed():
    base = settings.canonical_url
    items=[]
    for p in services.repo.list_blog(50, False):
        link=f"{base}/blog/{p.slug}"
        items.append(
            f"<item><title>{escape(p.title)}</title><link>{escape(link)}</link><guid>{escape(link)}</guid>"
            f"<description>{escape(p.dek)}</description><pubDate>{escape((p.published_at or p.updated_at).strftime('%a, %d %b %Y %H:%M:%S +0000'))}</pubDate></item>"
        )
    xml=(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>XMRBot</title>'
         f'<link>{escape(base + "/blog")}</link><description>Monero research and operating notes.</description>{"".join(items)}</channel></rss>')
    return Response(xml, media_type="application/rss+xml")

@app.get("/")
def home(): return FileResponse(str(static_dir.joinpath("index.html")))
@app.get("/terminal")
def terminal(): return FileResponse(str(static_dir.joinpath("terminal.html")))
@app.get("/mine")
def mine(): return FileResponse(str(static_dir.joinpath("mine.html")))
@app.get("/ask")
def ask(): return FileResponse(str(static_dir.joinpath("ask.html")))
@app.get("/blog")
def blog(): return FileResponse(str(static_dir.joinpath("blog.html")))
@app.get("/blog/{slug}")
def blog_post(slug: str): return FileResponse(str(static_dir.joinpath("blog-post.html")))
@app.get("/providers")
def providers(): return FileResponse(str(static_dir.joinpath("providers.html")))
@app.get("/recipes")
def recipes(): return FileResponse(str(static_dir.joinpath("recipes.html")))
@app.get("/cpu/{slug}")
def cpu_page(slug: str): return FileResponse(str(static_dir.joinpath("cpu.html")))
