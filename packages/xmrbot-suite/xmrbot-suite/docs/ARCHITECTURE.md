# Architecture

## Layers

1. **Acquisition/UI** — static HTML/CSS/JS served by FastAPI. No npm build step is required.
2. **HTTP API** — typed FastAPI routes under `/v1`.
3. **Agent/MCP** — `ToolRegistry` is the canonical tool ontology. HTTP and stdio MCP transports both call it.
4. **Domain core** — profitability, mine-vs-buy, methodologies, provenance/risk types.
5. **Data** — SQLite in development; a Timescale/Postgres migration is provided for production.
6. **Integrations** — local monerod RPC and the original xmr.computer scheduler.
7. **Local execution** — xmrbotd inspection/planning surface. Secrets remain local.

## Dependency direction

`web -> API -> domain/services -> repository/integrations`

`MCP -> ToolRegistry -> same domain/services`

`xmrbot -> xmrcomputer`, never the reverse. The earlier compute router therefore remains usable standalone.

## Reserve bid

xmr.computer normalizes CPU opportunities to net XMR/hour. Direct RandomX is the reserve bid. Qubic or another market should enter only through a `MarketAdapter`; no venue owns the scheduler.

## Canonical data versus explanation

Values such as network hashrate and hashprice are typed and derived deterministically. The knowledge engine returns source/provenance fields. Future LLM explanation should sit above these objects and must not replace them as data authority.
