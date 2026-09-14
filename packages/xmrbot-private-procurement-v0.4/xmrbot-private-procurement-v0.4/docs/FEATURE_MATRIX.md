# Feature matrix

This matrix distinguishes executable features from integrations that require external infrastructure/credentials and therefore ship as explicit adapter boundaries rather than fake success responses.

| Area | Status | Implementation |
|---|---|---|
| Solid/legacy responsive visual system | Working | `web/static/styles.css`, all public pages |
| Home / terminal / mining / ask / CPU pages | Working | `src/xmrbot/web/static` |
| Blog index + article UI | Working | `/blog`, `/blog/{slug}` |
| Blog draft/publish persistence | Working | SQLite repo + MCP tools + token-gated HTTP API |
| Blog RSS + raw structured access | Working | `/blog/feed.xml`, `/v1/blog*` |
| Content recipes | Working | `content/recipes.py`, `/recipes`, API + MCP |
| Blog → YouTube/social production package | Working | `xmr_content_from_blog` |
| YouTube account upload | Credential adapter boundary | OAuth/channel credentials required; never faked |
| LLM/agent discovery | Working | `/llms.txt`, robots, sitemap, well-known manifest |
| MCP resources/list + resources/read | Working | site, LLM guide, network, blog, recipes |
| Machine-readable site map | Working | `/v1/site/map`, `xmr_site_map` |
| Network history | Working | SQLite repo + `/v1/network/history` |
| Live monerod ingestion | Working when configured | `integrations/monerod.py`, `/v1/network/refresh` |
| Hashprice / difficulty / emission | Working | deterministic core + methodologies |
| Mining profitability | Working | `/v1/mining/profitability` + MCP |
| Mine vs buy | Working | `/v1/mining/mine-or-buy` + MCP |
| Hardware catalog / rankings | Working with seeded observations | `hardware/` |
| Historical hardware market crawler | Adapter boundary | intentionally not fabricated |
| Constrained analytics query | Working | `/v1/query` |
| Canonical knowledge search | Working | `knowledge/` |
| Resource router | Working | `/v1/resource/find` + MCP |
| Node deployment plan | Working | typed safe plan |
| Automatic node installer/lifecycle | Extension seam | requires signed binary/download policy |
| Wallet creation safety plan | Working | local-first plan |
| Wallet RPC fund movement | Deliberately not exposed | R2 future local approval layer |
| Seed/private-key export | Disabled by design | security invariant/tests |
| xmr.computer reserve-bid bridge | Working | original package imported directly |
| Qubic | Adapter seam retained | prior `QubicAdapter`; no fake live quote |
| External compute markets | Adapter interface | `MarketAdapter` |
| Local machine inspection | Working | `xmrbotd inspect` |
| RandomX benchmark estimate | Working | hardware match; explicitly labelled estimate |
| Real XMRig benchmark execution | Extension seam | needs binary verifier/executor |
| Privacy profile | Working | API + local profile semantics |
| Tor process/routing automation | Extension seam | detected/planned, not falsely claimed active |
| HTTP MCP | Working, write-gated | `POST /mcp` + editor bearer token for R1/R2 |
| stdio MCP | Working | `xmrbot-mcp`; recommended trusted write path |
| Content event detector | Working | `content/events.py` |
| Postgres/Timescale production schema | Shipped | `migrations/001_init.sql`, `002_blog.sql` |
| Test/validation evidence | Working | `tests/`, `scripts/validate.sh`, `validation/` |

## Private procurement fabric (0.4)

| Feature | Status | Notes |
|---|---|---|
| 20-provider typed registry | implemented/tested | source URLs and integration modes exposed over API/MCP |
| Procurement router | implemented/tested | non-executing, ranks compatible providers |
| QP grant request | implemented/tested | exact provider/action/payload hash, budget, expiry; starts unapproved |
| Deterministic gate | implemented/tested | detects mutation, expiry, provider/action mismatch and budget excess |
| Deterministic receipt | implemented/tested | SHA-256 integrity receipt; not represented as ZK proof |
| OrbitSwap | native API contract tested | live financial execution requires API key + approved grant |
| 1gwei | native API contract tested | quote/order/status contract |
| Trocador AnonPay | native API contract tested | indirect transaction/status flow |
| KYCnot | native API contract tested | API key required; attribution requirement documented by provider |
| monero-wallet-rpc | local API contract tested | no seed/private-key export tool; transfer requires grant |
| BasicSwap | local API contract tested | localhost JSON API/auth boundary |
| Haveno | local bridge contract tested | gRPC daemon remains local; bridge is explicit |
| XMR Checkout | local API contract tested | self-hosted API key boundary |
| XMRBazaar | read/manual/upcoming API | JSON automation API announced, not falsely treated as launched |
| Other marketplace/infra/card providers | read/manual bridge | proposal/evidence adapters until stable APIs are verified |
