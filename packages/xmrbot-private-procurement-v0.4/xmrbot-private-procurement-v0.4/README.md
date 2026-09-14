# XMRBot Suite 0.4 — Private Procurement Fabric

**Monero, understood — and usable by agents.** This repository is a cohesive extension of the 0.3 XMRBot + `xmr.computer` suite. It adds a typed private-economy provider fabric and a QP-compatible authority model without turning the MCP into an unrestricted spending wallet.

## New in 0.4

- 20 provider adapters/descriptors across marketplaces, labor, swaps, EVM gas, VPS/domains, eSIM, shipping, gift cards, concierge, fundraising and merchant checkout.
- Stable provider contract: `discover → quote/read → propose → grant-request → gate → execute (local/credentialed adapter only) → receipt`.
- Explicit integration modes: `native_api`, `local_api`, `read_only_web`, `manual_bridge`, `upcoming_api`.
- QP grant objects bind provider + action + exact payload hash + budget + expiry.
- Deterministic gate evaluation and hash receipts with tamper verification.
- MCP tools and `xmrbot://providers` resources for agent discovery.
- `/providers` human surface plus REST APIs under `/v1/providers`, `/v1/procurement` and `/v1/qp`.
- Native contracts for KYCnot, OrbitSwap, 1gwei, Trocador AnonPay, XMR Checkout, `monero-wallet-rpc`, BasicSwap and a local Haveno bridge.
- Honest adapter seams for XMRBazaar, Monero.Jobs, Kuno, Njalla, 1984 Hosting, Servers Guru, Silent Link, AnonymousLabels, XMR.CARDS, CoinsBee, ShopinBit and BTCPay where a stable public transactional API was not verified.

## Authority model

```text
user / agent intent
       ↓
xmr_procurement_route
       ↓
xmr_provider_propose          # no external state change
       ↓
qp_grant_request              # approved=false; exact payload hash
       ↓
external/user policy approval
       ↓
qp_gate_evaluate
       ↓
credentialed/local provider adapter
       ↓
ActionReceipt                 # action hash + response hash
```

Public MCP intentionally exposes proposal and verification primitives rather than a generic spend-anywhere tool. The local `monero-wallet-rpc` transfer adapter exists behind the provider layer, but seed/private-key export is absent and state-changing execution requires a matching grant.

## Provider registry

See `docs/PROVIDER_MATRIX.md` for the researched capability/mode table and `docs/providers/` for generated machine-oriented provider sheets. Source URLs are stored on every provider descriptor and exposed through API/MCP.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn xmrbot.app:app --host 127.0.0.1 --port 8000
```

Open `/providers` for the human router, `/docs` for OpenAPI, or use `xmrbot-mcp` over stdio.

## MCP examples

List the provider fabric:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"xmr_provider_list","arguments":{}}}
```

Route a procurement objective without spending:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xmr_procurement_route","arguments":{"objective":"hire a designer","max_xmr":0.2,"escrow_required":true}}}
```

Create an exact action proposal and grant request:

```text
xmr_provider_propose → qp_grant_request → policy approval → qp_gate_evaluate
```

## Existing XMRBot functionality preserved

The 0.3 site, mining terminal, CPU economics, blog/content automation, `llms.txt`, MCP resources, Monero knowledge layer and `xmr.computer` compute router remain intact.

## Test truthfulness

The test suite distinguishes **contract tests** from **live external end-to-end tests**. Contract tests use `httpx.MockTransport` to assert exact methods, paths, auth headers and payload semantics for native/local adapters. We do not claim that a real purchase/trade occurred. Live financial transactions are deliberately not run in CI because they require credentials, local daemons and real funds.

Run the full auditable validation pipeline:

```bash
bash scripts/validate.sh
```

The packaged archive contains the exact command log, pytest collection manifest, provider matrix, source checksum manifest and ZIP integrity report.
