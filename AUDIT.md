# AUDIT — agentcomfinal R2 import (2026-09-14)

Source: Cloudflare R2 bucket `agentcom` via S3-compatible endpoint.
Import date: 2026-09-14. Destination: `/agentcomfinal`.

## 1. What was in the bucket

- `list_objects_v2` on `agentcom`: **60 objects, 2,530,016 bytes (~2.4 MiB)**.
- De-duplicated by stripping leading `agentcom/` prefix: **30 unique files**.
  - The bucket stores everything twice: once at top-level (`breadupp`) and once under `agentcom/` (`agentcom/breadupp`). Same sizes, same content (spot-checked).
  - 2 exact duplicate pairs beyond that prefix duplication:
    - `campaign-control-plane-2026-09-14.zip` == `campaign-control-plane-2026-09-14(1).zip` (81,309 b each)
    - `goated thesis` == `insane theis` (53,643 b each, sha12 `d7723ad9dca2`)
- Split: **13 zip files (12 unique)** + **17 raw text docs (16 unique)**.

Raw dump preserved untouched in `docs/` + `docs/_manifest.json`
(30 unique files, with `source_keys`, sizes, sha12).

## 2. Repo layout (after organise)

```
agentcomfinal/
  README.md            — front door
  AUDIT.md             — this file
  .gitignore
  docs/                — raw R2 dump (immutable, 30 files + _manifest.json)
  notes/               — 16 curated text notes, sanitized filenames + frontmatter
  packages/            — 12 unpacked zips, each with 00_IMPORT_README.md
    agent-plugin-factory/
    agentcom-plugin-canonical/
    autobuild-v0.2/
    scarce-state-control-plane-v3/   (from autonomous-economic-discovery-...v3.zip)
    campaign-control-plane/
    personal-seesaw/
    scarce-state-control-plane-v2/
    seesaw-agent-module/
    thesisdesk/
    xmrbot-private-procurement-v0.4/
    xmrbot-solid-v0.3/
    xmrbot-suite/
```

Unpack hygiene: removed regenerable `__pycache__/`, `.pytest_cache/`, `*.pyc`
(counts per package in each `00_IMPORT_README.md`). Zips kept in `docs/`
as source of truth.

## 3. Packages — what each is

| slug | source zip | files / bytes (cleaned) | one-line |
|---|---|---|---|
| agent-plugin-factory | agent-plugin-factory-v0.1.zip (19,679) | 17 / 22k | Packet→plugin factory: scoring/registry/evals/CLI, domain-checker example |
| agentcom-plugin-canonical | agentcom-plugin-canonical-2026-09-13.zip (50,003) | 28 / 119k | Canonical plugin spec + router standard + lint checks + BUILD/REVIEW/ROUTING prompts + schemas/templates |
| autobuild-v0.2 | autobuild-v0.2-hardened.zip (59,884) | 54 / 150k | Hardened plan compiler: specgate/plangate/accretion/bridges/ledger + peerreview + tests |
| scarce-state-control-plane-v3 | autonomous-economic-discovery-control-plane-v3-2026-09-14.zip (225,822) | 112 / 597k | V3 discovery control plane, 13 projects, experiment worlds, fixtures, largest dataset |
| campaign-control-plane | campaign-control-plane-2026-09-14.zip (81,309) | 62 / 335k | Campaign-graph runtime: eventlog/drift/validators/GitHub poll/qp_adapter, 11 project theses, server+CLI |
| personal-seesaw | personal-seesaw-v0.1.zip (32,162) | 15 / 66k | Personal-Seesaw research repo: theory/formal model/backtests/divergence/extremes + py src |
| scarce-state-control-plane-v2 | scarce-state-control-plane-v2-2026-09-14.zip (119,778) | 83 / 499k | V2 control plane + web UI (index/app.js/style) + TEST_REPORT, 12 projects |
| seesaw-agent-module | seesaw-agent-module-v0.1.zip (39,854) | 28 / 66k | Working Seesaw strategy agent: OWN/BUILD/REUSE/BUY/VALIDATE/WATCH/DROP, engine/scoring/CLI, docs 00–06 |
| thesisdesk | thesisdesk.zip (9,946) | 6 / 26k | Tiny desk prototype UI + trades.json + RESEARCH.md |
| xmrbot-private-procurement-v0.4 | xmrbot-private-procurement-v0.4.zip (155,730) | 150 / 281k | Full private-procurement stack: 20+ provider docs, MCP, QP protocol, API, 15+ tests + validation logs |
| xmrbot-solid-v0.3 | xmrbot-solid-style-v0.3.zip (103,808) | 107 / 189k | Solid-style XMRBot app: web UI, agent tools/plans, hardware catalog, knowledge, content/blog, no tests |
| xmrbot-suite | xmrbot-suite.zip (79,113) | 93 / 130k | Suite variant: slimmer UI + monerod/xmrcomputer integrations, sibling of solid-v0.3 |

Unpacked total: ~755 files, ~5.0 MiB (cleaned).

Maturity signals:
- Tests present: autobuild, campaign, scarce-v2, scarce-v3, seesaw-agent-module, xmrbot-private-procurement. Missing in: agent-plugin-factory (has evals but no pytest), agentcom-plugin-canonical (has checks/ not pytest), personal-seesaw (no tests), thesisdesk (none), xmrbot-solid/suite (none).
- `VALIDATION.json`: agent-plugin-factory, autobuild, seesaw-agent-module.
- `MANIFEST.sha256.json`: campaign, scarce-v2 (v3 has partial? check inner).
- Web UI: scarce-v2, thesisdesk, xmrbot-solid/suite, xmrbot-procurement (partial).
- Each package has an original `README.md` (preserved); import notes in `00_IMPORT_README.md`.

## 4. Notes — what each is

| file | src bytes | theme |
|---|---|---|
| scarcity-thesis-moving-scarcity-surface.md | 53,643 | Canonical thesis: abundance→moving scarcity surface, catalytic edges, NBER 2026 backing |
| xmrbot-qp-procurement-thesis.md | 39,245 | qp + XMRBazaar + Monero as autonomous procurement protocol, order→CLAIM/RUN/RECEIPT mapping |
| the-plan-now-agentic-business-stack.md | 15,721 | 2026-09-13 stack snap: BreadUp headless, hourly scans, ChatGPT owns convo / BreadUp owns execution |
| breadup-shopify-chatgpt-os.md | 11,350 | BreadUp opening: entrepreneurial control loop on top of Shopify-for-ChatGPT primitives |
| breadup-marketplace-executable-businesses.md | 6,961 | BreadScan/Uplist/Upload/Worlds/Actors/Store/Packs; marketing intel + validation + execution loop |
| seesaw-invariant-moat-test.md | 4,470 | Invariant: “Can OpenAI destroy this by writing software?” + MCP-behind-endpoint moat ladder + M_i formula |
| freeze-campaign-graph-plan.md | 4,073 | FREEZE: campaign-graph PM website, GitHub polling, wasm validators, autonomy vs augmented optimum |
| seesaw-agent-module-summary.md | 4,046 | Seesaw module announcement: loop, OWN/... taxonomy, scarce-state→capability-kernel arch |
| personal-seesaw-two-seesaws.md | 6,967 | Two Seesaws (industry constraints / personal returns) + Future-Adjusted Personal Value + AI-beta |
| seesaw-bark-weighting-layer.md | 1,722 | Bark: performance-weighting layer over Seesaw (thesis→build→advertise→P&L→score) |
| chatgpt-is-distribution-agentugly-router.md | 2,020 | AgentUgly: ChatGPT as middle-man router (tradies via Checkatrade + scheduler), lead-gen |
| tom-plan-0910-bottlenecks.md | 1,266 | Bottlenecks → post-AGI money → tradie/EV/solar acquisition via free leads → admin/finance wedge |
| pogtown-band-music-agents.md | 1,000 | Pogtown music agents, instruments, POGCASTS, dance-sync question |
| it-helpdesk-agent-idea.md | 243 | Qwen-omni IT helpdesk agent |
| the-actual-plan.md | 140 | “Infinite money, retire bloodline, give to poorest daily” |
| pinterest-token.md | 101 orig / redacted | Live-pattern `pina_...` token — REDACTED before push, rotate if live |

`insane theis` intentionally not duplicated in `notes/` (identical to `goated thesis`).

## 5. Themes (what we actually have)

1. **Scarcity / Seesaw is the thesis.** 1 canonical essay + module + personal variant + 3 short notes + formal models in code. Invariant is crisp: own external state, authority, trajectories, liquidity, trust — not OSS-computable layers.
2. **Control planes are the OS.** campaign-control-plane, scarce-v2, scarce-v3/autonomous-discovery share the same DNA: `data/projects/*.json` (11–13 project theses), `data/fixtures/events/*.jsonl`, `portfolio.json`, `meta_bottlenecks.json`, drift/validators, GitHub polling, qp adapters. V3 is superset in data; v2 has the only web UI; campaign is the cleanest runtime.
3. **Plugin pipeline is the gate.** agent-plugin-factory (packet→candidate) → agentcom-plugin-canonical (spec/router/lint/prompts) → autobuild (compiler/gates/accretion). These three should be one pipeline but currently live as separate zips with overlapping schemas.
4. **XMRBot is the first external economy.** procurement-v0.4 is the keeper (tests + validation + provider matrix + MCP + QP). solid-v0.3/suite are UI-rich predecessors; raw `xmrbot` note is the thesis that justifies them.
5. **BreadUp is the commerce OS.** 2 BreadUp notes + the-plan-now + campaign/scarce project `breadup.json` all point the same way: headless scanners/watchers/repricers + economics + execution policy, ChatGPT as conversation layer.
6. **ChatGPT-as-distribution.** AgentUgly router note + tradie scheduler + EV/solar/tom-plan acquisition loop. No code yet — thesis only.

## 6. Problems / redundancies

- **Triple control-plane fork.** campaign vs scarce-v2 vs scarce-v3 share ~80% of `data/` filenames with divergent counts (11 vs 12 vs 13 projects) and different runtimes (`runtime/` vs `server.py` vs `web/`). No canonical version declared. Pick one.
- **Triple XMRBot fork.** suite vs solid-v0.3 vs procurement-v0.4 overlap heavily in `src/xmrbot/*` and `docs/` but differ in tests/coverage. Procurement-v0.4 wins on completeness; others should become history or UI-only.
- **Spec drift.** `plugin_spec`, `project`, `thesis`, `checkpoint`, `event`, `receipt` schemas exist in 3+ places with similar-but-not-identical fields. Canonical (`agentcom-plugin-canonical/schemas/`) should win, others should import it.
- **Raw filenames with spaces** (`chatgpt is distribution`, `pogtown band`, `the actual plan`, `goated thesis`) preserved in `docs/` for fidelity; sanitized copies in `notes/`. Do not add new space-named files.
- **No top-level runner.** No Makefile/CI that runs all checks/tests across packages. Each package has its own (or none).
- **Missing:** LICENSE, requirements/pyproject at root, provider secrets handling (only `.env.example` — good). The R2 `pinterest` object was a live-pattern Pinterest token — REDACTED from `docs/pinterest` + `notes/pinterest-token.md` before push (GitHub push protection). Rotate it if ever live.
- **No credentials in repo.** R2 keys used for import are NOT stored here (env-only during import, since removed). Do not commit them.

## 7. Recommended next steps

1. **Declare canonicals:** scarce-v3 = control-plane canonical (merge v2 web UI + campaign server polish into it); procurement-v0.4 = XMRBot canonical; agentcom-plugin-canonical = spec canonical; autobuild = compiler canonical.
2. **Unify schemas:** single `schemas/` at root re-exporting canonical plugin/project/thesis/event/receipt; packages import, not copy.
3. **Root test runner:** `make test` → pytest per package that has tests + `checks/run_all.py` for canonical + `scripts/peerreview.py` for autobuild. Record in `VALIDATION.json` at root.
4. **Fold notes into theses/:** `notes/scarcity-thesis-*.md` becomes `THESIS.md`; BreadUp notes → `packages/breadup/` (new, code to come); tradie/router note → AgentUgly stub.
5. **Decide BreadUp home:** currently thesis-only + `breadup.json` project files. Needs a real `packages/breadup/` service (scanners/watchers/economics) or explicitly mark as spec-only.
6. **Rotate the redacted pinterest token** if it was ever live; keep all future tokens in env, never in `notes/`.

## 8. Provenance

- Bucket `agentcom`, 60 objects listed, 30 unique downloaded to `docs/`, deduped to 12 zips + 16 notes, unpacked to `packages/` (755 files).
- Import scripts (not committed, in `/tmp/opencode/`): `list_r2.py`, `list_agentcom.py`, `import_agentcom.py`, `inventory.py`, `unpack.py`, `organise_notes.py`, `gen_pkg_readmes.py`.
- `docs/_manifest.json` is the machine-readable manifest (bucket, counts, sizes, sha12, source_keys).
