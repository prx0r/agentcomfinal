# Scarce-State Control Plane v2 (2026-09-14)

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `scarce-state-control-plane-v2`
- **source zip:** `docs/scarce-state-control-plane-v2-2026-09-14.zip` (119778 bytes)
- **unpacked:** 83 files, 498785 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `scarce-state-control-plane`
- **original README(s):** `scarce-state-control-plane/README.md`

## What this is

V2 with web UI (index/app.js/style), TEST_REPORT, runtime (underengineer, attestation, validators), 12 project JSONs. Predecessor to v3.

## Layout (top 2 levels)

```
  scarce-state-control-plane/.gitignore (34b)
  scarce-state-control-plane/ARCHITECTURE.md (1733b)
  scarce-state-control-plane/FREEZE.md (1413b)
  scarce-state-control-plane/MANIFEST.sha256.json (13161b)
  scarce-state-control-plane/Makefile (100b)
  scarce-state-control-plane/README.md (4259b)
  scarce-state-control-plane/TEST_REPORT.md (976b)
  scarce-state-control-plane/V2_CHANGES.md (1694b)
  scarce-state-control-plane/cli.py (2525b)
  scarce-state-control-plane/data/mcp_miner_example.json (687b)
  scarce-state-control-plane/data/meta_bottlenecks.json (4077b)
  scarce-state-control-plane/data/portfolio.json (14495b)
  scarce-state-control-plane/data/repo_snapshots.json (112b)
  scarce-state-control-plane/data/resource_classes.json (1576b)
  scarce-state-control-plane/data/scarce_asset_ledger.json (186b)
  scarce-state-control-plane/data/shared_components.json (2531b)
  scarce-state-control-plane/data/underengineer_state.json (1095b)
  scarce-state-control-plane/docs/AUTONOMY.md (840b)
  scarce-state-control-plane/docs/GITHUB_SYNC.md (618b)
  scarce-state-control-plane/docs/MCP_SCARCITY_MINER.md (677b)
  scarce-state-control-plane/docs/PROJECT_THESIS_SCHEMA.md (1139b)
  scarce-state-control-plane/docs/QP_INTEGRATION.md (619b)
  scarce-state-control-plane/docs/SCARCE_STATE.md (1406b)
  scarce-state-control-plane/docs/UNDERENGINEER.md (1945b)
  scarce-state-control-plane/docs/VALIDATION.md (1067b)
  scarce-state-control-plane/docs/VALIDATION_V2.md (924b)
  scarce-state-control-plane/runtime/__init__.py (0b)
  scarce-state-control-plane/runtime/attestation.py (1565b)
  scarce-state-control-plane/runtime/drift.py (572b)
  scarce-state-control-plane/runtime/eventlog.py (524b)
  scarce-state-control-plane/runtime/graph.py (867b)
  scarce-state-control-plane/runtime/model.py (575b)
  scarce-state-control-plane/runtime/poll_github.py (1999b)
  scarce-state-control-plane/runtime/qp_adapter.py (727b)
  scarce-state-control-plane/runtime/reward.py (1292b)
  scarce-state-control-plane/runtime/scarcity.py (1187b)
  scarce-state-control-plane/runtime/underengineer.py (3921b)
  scarce-state-control-plane/runtime/validators.py (4514b)
  scarce-state-control-plane/schemas/attested_event.schema.json (553b)
  scarce-state-control-plane/schemas/checkpoint.schema.json (702b)
  scarce-state-control-plane/schemas/event.schema.json (354b)
  scarce-state-control-plane/schemas/htask.schema.json (301b)
  scarce-state-control-plane/schemas/receipt.schema.json (423b)
  scarce-state-control-plane/schemas/scarce_asset.schema.json (862b)
  scarce-state-control-plane/schemas/thesis.schema.json (456b)
  scarce-state-control-plane/schemas/underengineer.schema.json (654b)
  scarce-state-control-plane/server.py (2518b)
  scarce-state-control-plane/tests/test_drift.py (294b)
  scarce-state-control-plane/tests/test_graph.py (432b)
  scarce-state-control-plane/tests/test_portfolio.py (982b)
  scarce-state-control-plane/tests/test_scarcity.py (573b)
  scarce-state-control-plane/tests/test_server.py (270b)
  scarce-state-control-plane/tests/test_underengineer.py (1257b)
  scarce-state-control-plane/tests/test_underengineer.py.tmp (0b)
  scarce-state-control-plane/tests/test_validators.py (2255b)
  scarce-state-control-plane/web/app.js (7395b)
  scarce-state-control-plane/web/index.html (1814b)
  scarce-state-control-plane/web/style.css (5781b)
```

## Original README excerpt

_Source: `scarce-state-control-plane/README.md`_

```markdown
# Scarce State Control Plane — v2 frozen 2026-09-14

This repository is the executable portfolio/control-plane prototype for the revised thesis:

> **Acquire or produce scarce consequential state → expose it through whatever agent protocol wins.**

The strategic kill test is simple:

> **Can OpenAI/platform vendors destroy this merely by writing more software?**

If yes, the software is normally internal infrastructure. If no, the project must name the scarce external state it expects to control and the verified event that increases it.

## UNDERENGINEER

`UNDERENGINEER/1.0` is the high-level project manager. It finds the **earliest real moat-producing event**, builds only its prerequisites plus safety/verification, then pauses feature expansion to observe the result.

This deliberately separates the **full capability library** from the **current build order**.

```text
scarce asset thesis
   ↓
UNDERENGINEER
   ↓
first real moat event
   ↓
minimum steps
   ↓
ATask / competing agents
   ↓
independent evidence
   ↓
QP-granted consequence
   ↓
scarce-state ledger delta
   ↓
observe before adding features
```

## Current portfolio


... (+75 more lines in scarce-state-control-plane/README.md)
```

## How to use

- Raw zip stays in `docs/scarce-state-control-plane-v2-2026-09-14.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/scarce-state-control-plane-v2 -q` (adjust to inner dir, e.g. `packages/scarce-state-control-plane-v2/scarce-state-control-plane`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
