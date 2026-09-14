# XMRBot Solid Style v0.3

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `xmrbot-solid-v0.3`
- **source zip:** `docs/xmrbot-solid-style-v0.3.zip` (103808 bytes)
- **unpacked:** 107 files, 189305 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `xmrbot-solid`
- **original README(s):** `xmrbot-solid/README.md`

## What this is

Solid-style XMRBot app: web static UI, agent tools/plans, hardware catalog, knowledge engine, content/blog, core economics/risk, MCP. No tests dir (cf procurement).

## Layout (top 2 levels)

```
  xmrbot-solid/.env.example (400b)
  xmrbot-solid/Dockerfile (253b)
  xmrbot-solid/Makefile (325b)
  xmrbot-solid/README.md (4260b)
  xmrbot-solid/docker-compose.yml (369b)
  xmrbot-solid/docs/ARCHITECTURE.md (1374b)
  xmrbot-solid/docs/COMPATIBILITY.md (468b)
  xmrbot-solid/docs/CONTENT_AUTOMATION.md (1544b)
  xmrbot-solid/docs/DATA.md (854b)
  xmrbot-solid/docs/EXTENSION_GUIDE.md (1093b)
  xmrbot-solid/docs/FEATURE_MATRIX.md (3317b)
  xmrbot-solid/docs/MCP.md (851b)
  xmrbot-solid/docs/ROADMAP.md (814b)
  xmrbot-solid/docs/SECURITY.md (881b)
  xmrbot-solid/docs/STYLE_SYSTEM.md (1052b)
  xmrbot-solid/migrations/001_init.sql (677b)
  xmrbot-solid/migrations/002_blog.sql (642b)
  xmrbot-solid/pyproject.toml (795b)
  xmrbot-solid/scripts/validate.sh (3118b)
  xmrbot-solid/tests/conftest.py (132b)
  xmrbot-solid/tests/test_api.py (1946b)
  xmrbot-solid/tests/test_blog.py (2163b)
  xmrbot-solid/tests/test_compatibility.py (693b)
  xmrbot-solid/tests/test_content.py (553b)
  xmrbot-solid/tests/test_economics.py (1444b)
  xmrbot-solid/tests/test_hardware.py (538b)
  xmrbot-solid/tests/test_knowledge.py (510b)
  xmrbot-solid/tests/test_machine_discovery.py (1201b)
  xmrbot-solid/tests/test_mcp.py (2331b)
  xmrbot-solid/tests/test_rpc.py (1282b)
  xmrbot-solid/tests/test_security.py (773b)
  xmrbot-solid/tests/test_style.py (567b)
  xmrbot-solid/tests/test_xmrcomputer_bridge.py (597b)
  xmrbot-solid/validation/RESULTS.md (501b)
  xmrbot-solid/validation/SHA256SUMS.txt (10026b)
  xmrbot-solid/validation/TEST_MANIFEST.md (373b)
  xmrbot-solid/validation/summary.json (59b)
  xmrbot-solid/validation/tests_collected.txt (342b)
  xmrbot-solid/validation/validation.log (1614b)
```

## Original README excerpt

_Source: `xmrbot-solid/README.md`_

```markdown
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

... (+81 more lines in xmrbot-solid/README.md)
```

## How to use

- Raw zip stays in `docs/xmrbot-solid-style-v0.3.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/xmrbot-solid-v0.3 -q` (adjust to inner dir, e.g. `packages/xmrbot-solid-v0.3/xmrbot-solid`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
