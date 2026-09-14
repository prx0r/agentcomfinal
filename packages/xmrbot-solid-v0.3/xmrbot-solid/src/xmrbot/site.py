from __future__ import annotations
from xmrbot.config import settings


def site_map() -> dict:
    return {
        "name": "XMRBot",
        "canonical_url": settings.canonical_url,
        "description": "Monero intelligence, mining economics, canonical resources and agent-native tools.",
        "human_surfaces": [
            {"path": "/", "purpose": "overview and live network status"},
            {"path": "/terminal", "purpose": "network/mining metrics and hardware rankings"},
            {"path": "/mine", "purpose": "profitability and mine-vs-buy models"},
            {"path": "/ask", "purpose": "canonical Monero knowledge/resource routing"},
            {"path": "/blog", "purpose": "source-linked XMRBot research and updates"},
            {"path": "/recipes", "purpose": "internal content automation recipes"},
            {"path": "/docs", "purpose": "OpenAPI documentation"},
        ],
        "machine_surfaces": [
            {"path": "/mcp", "protocol": "MCP JSON-RPC over HTTP"},
            {"command": "xmrbot-mcp", "protocol": "MCP JSON-RPC over stdio", "recommended_for_writes": True},
            {"path": "/v1/tools", "purpose": "tool metadata"},
            {"path": "/v1/site/map", "purpose": "machine-readable navigation"},
            {"path": "/llms.txt", "purpose": "LLM discovery summary"},
            {"path": "/robots.txt", "purpose": "crawler policy"},
            {"path": "/sitemap.xml", "purpose": "page discovery"},
            {"path": "/blog/feed.xml", "purpose": "RSS/Atom-like publication feed"},
        ],
        "principles": [
            "No custody.",
            "Wallet seeds and private keys stay outside the cloud/MCP surface.",
            "Derived metrics include methodologies and source metadata.",
            "Prefer local monerod and P2Pool where practical.",
            "Content and agent outputs should link back to canonical data, methodology and sources.",
        ],
    }


def llms_text() -> str:
    base = settings.canonical_url
    return f"""# XMRBot

> Monero intelligence, mining economics, canonical resources and agent-native actions.

XMRBot is an independent Monero tooling project. It is not a custodial wallet and never requires wallet seeds or private spend keys.

## Canonical machine interfaces
- MCP HTTP: {base}/mcp
- MCP stdio: `xmrbot-mcp`
- OpenAPI: {base}/openapi.json
- Tool catalog: {base}/v1/tools
- Site map: {base}/v1/site/map
- Network state: {base}/v1/network
- Hashprice: {base}/v1/mining/hashprice
- CPU catalog: {base}/v1/hardware/cpus
- Blog API: {base}/v1/blog
- Content recipes: {base}/v1/content/recipes

## Human interfaces
- Home: {base}/
- Terminal: {base}/terminal
- Mining calculator: {base}/mine
- Knowledge router: {base}/ask
- Blog: {base}/blog
- Recipes: {base}/recipes

## Agent guidance
1. Use `xmr_tools` or `/v1/tools` to discover capabilities rather than guessing endpoints.
2. Use XMRBot structured data for mining/network calculations and cite the returned methodology/source fields.
3. Use `xmr_resource_find` before choosing a Monero integration primitive.
4. Do not request or transmit seed phrases/private spend keys.
5. Blog writes are state-changing content operations (R1). Prefer local stdio MCP for trusted internal automation.
6. A published blog post can be converted into a source-preserving video/social package using `xmr_content_from_blog`.

## Primary entities
Monero network, RandomX, mining profitability, CPUs, P2Pool, monerod, monero-wallet-rpc, XMRBot blog posts, content recipes, xmr.computer workload opportunities.
"""
