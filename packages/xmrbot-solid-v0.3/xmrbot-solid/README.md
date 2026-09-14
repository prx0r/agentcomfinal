# XMRBot Suite 0.3

**Monero, understood.** A durable Monero information, mining and agent interface with the earlier `xmr.computer` compute-router preserved as a compatible subsystem.

This build includes the solid/legacy visual system, a source-linked blog CMS for trusted internal agents, LLM/crawler discovery surfaces, MCP resources as well as tools, and content recipes that turn one canonical research object into a YouTube/social production package.

## Product surfaces

Human:

- `/` — system overview and current network ledger
- `/terminal` — Monero/RandomX mining terminal
- `/mine` — profitability and mine-vs-buy models
- `/ask` — canonical Monero knowledge/resource router
- `/cpu/{slug}` — programmatic RandomX hardware records
- `/blog` and `/blog/{slug}` — source-linked research
- `/recipes` — inspectable content automation recipes

Machine/agent:

- `POST /mcp` — MCP JSON-RPC over HTTP
- `xmrbot-mcp` — MCP JSON-RPC over stdio (recommended for trusted internal writes)
- `/v1/tools` — typed tool catalog
- `/v1/site/map` — complete machine-readable navigation
- `/llms.txt` and `/.well-known/llms.txt` — LLM discovery guidance
- `/.well-known/xmrbot.json` — structured project manifest
- `/robots.txt` and `/sitemap.xml`
- `/openapi.json` and `/docs`
- `/blog/feed.xml`

## Blog → video workflow

The blog post plus its `source_refs` is the canonical research object. A trusted internal agent can use:

```text
xmr_blog_draft
      ↓ source/editor review
xmr_blog_publish
      ↓
xmr_content_from_blog
      ↓
video script + YouTube manifest + thumbnail brief
+ Shorts + X + Instagram package
      ↓ render / editor approval
credentialed YouTube publisher adapter
```

The repository deliberately does **not** fake a YouTube upload. Actual publication requires channel OAuth credentials and belongs in a minimal credentialed adapter. See `docs/CONTENT_AUTOMATION.md`.

HTTP content writes are disabled until `XMRBOT_EDITOR_TOKEN` is configured. State-changing MCP tools over HTTP require the same bearer token. Trusted local automation can instead use `xmrbot-mcp` over stdio.

## Visual system

The UI is intentionally the opposite of generic AI/SaaS visual language: no gradients, glass, floating neon cards or marketing animation. It uses a charcoal system shell, warm white/paper information surfaces, explicit borders, dense tables, serif editorial typography, monospace metrics and restrained Monero orange.

See `docs/STYLE_SYSTEM.md`.

## Trust boundaries

XMRBot is non-custodial. It does not accept or export wallet seeds or private spend keys. `xmrbotd` is loopback-only by default. Official Monero wallet binaries are not mirrored by XMRBot; the UI links users to the Monero Project's official download surface.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
uvicorn xmrbot.app:app --host 127.0.0.1 --port 8000
```

For live chain data:

```bash
export XMRBOT_MONEROD_ENABLED=1
export XMRBOT_MONEROD_URL=http://127.0.0.1:18081
export XMRBOT_XMR_USD=500
curl -X POST http://127.0.0.1:8000/v1/network/refresh
```

The price adapter is intentionally separate from chain truth.

## MCP examples

Discover tools:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

Discover structured resources:

```json
{"jsonrpc":"2.0","id":2,"method":"resources/list","params":{}}
```

Read the machine site map:

```json
{"jsonrpc":"2.0","id":3,"method":"resources/read","params":{"uri":"xmrbot://site"}}
```

Trusted local agent blog draft:

```json
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"xmr_blog_draft","arguments":{"title":"Example","body_md":"## Thesis\n\nSource-linked body.","source_refs":[{"name":"Monero docs","url":"https://www.getmonero.org/"}]}}}
```

## xmr.computer compatibility

The prior compute-router remains available unchanged under `src/xmrcomputer/`. XMRBot's opportunity endpoint and MCP tool bridge into those same scheduler/economics models rather than duplicating them.

## Validation

Run:

```bash
bash scripts/validate.sh
```

The packaged archive includes `validation/RESULTS.md`, `validation/validation.log`, the exact collected test manifest and source checksums.
