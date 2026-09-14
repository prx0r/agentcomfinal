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

Open:

- `http://127.0.0.1:8000/`
- `/terminal`
- `/mine`
- `/ask`
- `/docs`

## Enable live monerod data

Run a local Monero node with RPC accessible only where intended, then set:

```bash
export XMRBOT_MONEROD_ENABLED=1
export XMRBOT_MONEROD_URL=http://127.0.0.1:18081
export XMRBOT_XMR_USD=500  # price adapter is deliberately separate from chain truth
curl -X POST http://127.0.0.1:8000/v1/network/refresh
```

When disabled, the app labels data source `offline-seed-config` with low confidence rather than pretending the values are live.

## API examples

```bash
curl http://127.0.0.1:8000/v1/network

curl -X POST http://127.0.0.1:8000/v1/mining/profitability \
  -H 'content-type: application/json' \
  -d '{"hashrate_hs":26900,"watts":160,"electricity_usd_kwh":0.10,"hardware_cost_usd":480,"amortization_months":36}'

curl -X POST http://127.0.0.1:8000/v1/mining/mine-or-buy \
  -H 'content-type: application/json' \
  -d '{"budget_usd":800,"hardware_cost_usd":480,"hashrate_hs":26900,"watts":160,"electricity_usd_kwh":0.10,"months":24,"monthly_difficulty_growth_pct":1,"residual_value_pct":30}'
```

## MCP

HTTP MCP-compatible JSON-RPC:

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Stdio:

```bash
xmrbot-mcp
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

The stdio transport is newline-delimited JSON-RPC, which makes it easy for coding agents to embed and test. The core MCP server is transport-independent.

## Local daemon

```bash
xmrbotd inspect
xmrbotd benchmark
xmrbotd node-plan
xmrbotd wallet-plan
xmrbotd serve                 # 127.0.0.1:47831
```

`xmrbotd serve --host 0.0.0.0` is rejected.

## xmr.computer compatibility

The previous package's classes remain available unchanged:

```python
from xmrcomputer.models.domain import MachineProfile
from xmrcomputer.core.economics import RandomXNetwork
from xmrcomputer.core.scheduler import Scheduler
```

XMRBot's `/v1/computer/opportunities` and MCP `xmr_computer_opportunities` tool call these same classes. See `docs/COMPATIBILITY.md`.

## Validation

Run exactly:

```bash
bash scripts/validate.sh
```

The script records commands and outputs under `validation/`. The packaged archive includes the results from the build that produced it.

## Structure

```text
src/xmrbot/
  agent/          typed agent/MCP tools and safe plans
  api/            HTTP API
  content/        event detection + media workflow objects
  core/           economics, types, methodology, risk
  data/           SQLite repository
  hardware/       CPU catalog/rankings
  integrations/   monerod + xmr.computer bridge
  knowledge/      canonical resource/search layer
  local/          xmrbotd companion
  mcp/            transport-independent JSON-RPC MCP server + stdio
  web/static/     self-contained frontend
src/xmrcomputer/  prior xmr.computer implementation, retained compatibly
```

The code intentionally favors small typed modules and pure functions so a coding agent can replace each adapter independently (price, hardware market, Qubic, real XMRig benchmark, wallet RPC, TimescaleDB, content generation) without rewriting the system.
