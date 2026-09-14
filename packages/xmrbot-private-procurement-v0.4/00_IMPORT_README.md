# XMRBot Private Procurement v0.4

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `xmrbot-private-procurement-v0.4`
- **source zip:** `docs/xmrbot-private-procurement-v0.4.zip` (155730 bytes)
- **unpacked:** 150 files, 280819 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `xmrbot-private-procurement-v0.4`
- **original README(s):** `xmrbot-private-procurement-v0.4/README.md`

## What this is

Full private-procurement stack: 20+ provider docs (Njalla, BTCPay, Haveno, etc), MCP server, QP procurement protocol, API/routes, 15+ tests + validation logs. Most complete XMRBot.

## Layout (top 2 levels)

```
  xmrbot-private-procurement-v0.4/.env.example (809b)
  xmrbot-private-procurement-v0.4/Dockerfile (253b)
  xmrbot-private-procurement-v0.4/Makefile (325b)
  xmrbot-private-procurement-v0.4/README.md (4055b)
  xmrbot-private-procurement-v0.4/docker-compose.yml (369b)
  xmrbot-private-procurement-v0.4/docs/ADDING_PROVIDER.md (1022b)
  xmrbot-private-procurement-v0.4/docs/ARCHITECTURE.md (1374b)
  xmrbot-private-procurement-v0.4/docs/COMPATIBILITY.md (468b)
  xmrbot-private-procurement-v0.4/docs/CONTENT_AUTOMATION.md (1544b)
  xmrbot-private-procurement-v0.4/docs/DATA.md (854b)
  xmrbot-private-procurement-v0.4/docs/EXTENSION_GUIDE.md (1093b)
  xmrbot-private-procurement-v0.4/docs/FEATURE_MATRIX.md (4875b)
  xmrbot-private-procurement-v0.4/docs/MCP.md (851b)
  xmrbot-private-procurement-v0.4/docs/MCP_PRIVATE_ECONOMY.md (633b)
  xmrbot-private-procurement-v0.4/docs/PRIVATE_PROCUREMENT.md (1377b)
  xmrbot-private-procurement-v0.4/docs/PROVIDER_MATRIX.md (3412b)
  xmrbot-private-procurement-v0.4/docs/PROVIDER_RESEARCH.md (3834b)
  xmrbot-private-procurement-v0.4/docs/QP_PROVIDER_PROTOCOL.md (1110b)
  xmrbot-private-procurement-v0.4/docs/ROADMAP.md (814b)
  xmrbot-private-procurement-v0.4/docs/SECURITY.md (881b)
  xmrbot-private-procurement-v0.4/docs/STYLE_SYSTEM.md (1052b)
  xmrbot-private-procurement-v0.4/migrations/001_init.sql (677b)
  xmrbot-private-procurement-v0.4/migrations/002_blog.sql (642b)
  xmrbot-private-procurement-v0.4/pyproject.toml (809b)
  xmrbot-private-procurement-v0.4/scripts/validate.sh (5388b)
  xmrbot-private-procurement-v0.4/tests/conftest.py (132b)
  xmrbot-private-procurement-v0.4/tests/test_api.py (1946b)
  xmrbot-private-procurement-v0.4/tests/test_blog.py (2163b)
  xmrbot-private-procurement-v0.4/tests/test_compatibility.py (693b)
  xmrbot-private-procurement-v0.4/tests/test_content.py (553b)
  xmrbot-private-procurement-v0.4/tests/test_economics.py (1444b)
  xmrbot-private-procurement-v0.4/tests/test_hardware.py (538b)
  xmrbot-private-procurement-v0.4/tests/test_knowledge.py (510b)
  xmrbot-private-procurement-v0.4/tests/test_machine_discovery.py (1201b)
  xmrbot-private-procurement-v0.4/tests/test_mcp.py (2331b)
  xmrbot-private-procurement-v0.4/tests/test_procurement_api_mcp.py (1556b)
  xmrbot-private-procurement-v0.4/tests/test_procurement_registry.py (1309b)
  xmrbot-private-procurement-v0.4/tests/test_provider_http_adapters.py (5091b)
  xmrbot-private-procurement-v0.4/tests/test_qp_procurement.py (2174b)
  xmrbot-private-procurement-v0.4/tests/test_rpc.py (1282b)
  xmrbot-private-procurement-v0.4/tests/test_security.py (773b)
  xmrbot-private-procurement-v0.4/tests/test_style.py (567b)
  xmrbot-private-procurement-v0.4/tests/test_xmrcomputer_bridge.py (597b)
  xmrbot-private-procurement-v0.4/validation/RESULTS.md (766b)
  xmrbot-private-procurement-v0.4/validation/SHA256SUMS.txt (13987b)
  xmrbot-private-procurement-v0.4/validation/TEST_MANIFEST.md (520b)
  xmrbot-private-procurement-v0.4/validation/summary.json (92b)
  xmrbot-private-procurement-v0.4/validation/tests_collected.txt (489b)
  xmrbot-private-procurement-v0.4/validation/validation.log (2581b)
```

## Original README excerpt

_Source: `xmrbot-private-procurement-v0.4/README.md`_

```markdown
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


... (+48 more lines in xmrbot-private-procurement-v0.4/README.md)
```

## How to use

- Raw zip stays in `docs/xmrbot-private-procurement-v0.4.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/xmrbot-private-procurement-v0.4 -q` (adjust to inner dir, e.g. `packages/xmrbot-private-procurement-v0.4/xmrbot-private-procurement-v0.4`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
