# XMRBot Suite

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `xmrbot-suite`
- **source zip:** `docs/xmrbot-suite.zip` (79113 bytes)
- **unpacked:** 93 files, 130351 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `xmrbot-suite`
- **original README(s):** `xmrbot-suite/README.md`

## What this is

Suite variant of XMRBot: slimmer web UI, monerod + xmrcomputer integrations, core/api/mcp. Sibling of solid-v0.3, predecessor to procurement-v0.4.

## Layout (top 2 levels)

```
  xmrbot-suite/.env.example (211b)
  xmrbot-suite/Dockerfile (253b)
  xmrbot-suite/Makefile (325b)
  xmrbot-suite/README.md (5572b)
  xmrbot-suite/docker-compose.yml (369b)
  xmrbot-suite/docs/ARCHITECTURE.md (1374b)
  xmrbot-suite/docs/COMPATIBILITY.md (468b)
  xmrbot-suite/docs/DATA.md (854b)
  xmrbot-suite/docs/EXTENSION_GUIDE.md (1093b)
  xmrbot-suite/docs/FEATURE_MATRIX.md (2572b)
  xmrbot-suite/docs/MCP.md (674b)
  xmrbot-suite/docs/ROADMAP.md (814b)
  xmrbot-suite/docs/SECURITY.md (881b)
  xmrbot-suite/migrations/001_init.sql (677b)
  xmrbot-suite/pyproject.toml (795b)
  xmrbot-suite/scripts/validate.sh (1848b)
  xmrbot-suite/tests/conftest.py (132b)
  xmrbot-suite/tests/test_api.py (1924b)
  xmrbot-suite/tests/test_compatibility.py (693b)
  xmrbot-suite/tests/test_content.py (553b)
  xmrbot-suite/tests/test_economics.py (1444b)
  xmrbot-suite/tests/test_hardware.py (538b)
  xmrbot-suite/tests/test_knowledge.py (510b)
  xmrbot-suite/tests/test_mcp.py (1789b)
  xmrbot-suite/tests/test_rpc.py (1282b)
  xmrbot-suite/tests/test_security.py (773b)
  xmrbot-suite/tests/test_xmrcomputer_bridge.py (597b)
  xmrbot-suite/validation/RESULTS.md (388b)
  xmrbot-suite/validation/SHA256SUMS.txt (8687b)
  xmrbot-suite/validation/TEST_MANIFEST.md (293b)
  xmrbot-suite/validation/summary.json (58b)
  xmrbot-suite/validation/tests_collected.txt (262b)
  xmrbot-suite/validation/validation.log (1970b)
```

## Original README excerpt

_Source: `xmrbot-suite/README.md`_

```markdown
# XMRBot Suite

**Monero for humans, agents and computers.**

This repository is the working implementation of the XMRBot architecture and includes the earlier `xmr.computer` compute-router package under the same Python source tree for direct compatibility.

## What ships

- responsive XMRBot website: home, terminal, mine-vs-buy, canonical search/resource router, CPU pages
- Monero network data model with SQLite history and a production Timescale/Postgres migration
- optional live `monerod` JSON-RPC ingestion; explicit offline seed mode when live RPC is disabled
- XMR hashprice and RandomX profitability engine with methodology IDs
- mine-vs-buy scenario engine with difficulty growth and hardware residual value
- RandomX hardware catalog/rankings and per-CPU programmatic pages
- provenance-oriented knowledge search and Monero primitive/resource routing
- safe node/wallet setup plans
- HTTP MCP endpoint (`POST /mcp`) and stdio MCP server (`xmrbot-mcp`)
- typed tools for network status, mining economics, CPU lookup, mine-vs-buy, node/wallet plans, local machine inspection and xmr.computer opportunity ranking
- `xmrbotd` local companion with localhost-only serve policy
- content event detector + cross-channel workflow object generator
- the original xmr.computer scheduler/economics package and adapters, imported directly rather than duplicated
- regression, API, MCP, RPC, security, web and compatibility tests
- reproducible validation script and captured validation results

## Trust boundaries

This project is deliberately **non-custodial**. It does not accept or export wallet seeds/private spend keys. Wallet execution is not implemented in this release; only a local-first plan surface is present. `xmrbotd` refuses non-loopback bind addresses by default. External compute execution is also not enabled by default.

Hardware benchmarks bundled in `cpus.json` are discovery seeds and explicitly carry `verified=false` unless independently validated. Do not use seed prices/benchmarks as purchase advice without measurement.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env   # export values or use your preferred env loader
xmrbot network
uvicorn xmrbot.app:app --host 127.0.0.1 --port 8000
```

... (+109 more lines in xmrbot-suite/README.md)
```

## How to use

- Raw zip stays in `docs/xmrbot-suite.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/xmrbot-suite -q` (adjust to inner dir, e.g. `packages/xmrbot-suite/xmrbot-suite`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
