# Campaign Control Plane (2026-09-14)

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `campaign-control-plane`
- **source zip:** `docs/campaign-control-plane-2026-09-14.zip` (81309 bytes)
- **unpacked:** 62 files, 334919 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 2 entries cleaned)
- **top-level inside:** `campaign-control-plane`
- **original README(s):** `campaign-control-plane/README.md`

## What this is

Campaign-graph runtime: event log, drift detection, validators, GitHub poller, qp adapter, checkpoint/event/receipt schemas, 11 project theses. Server + CLI.

## Layout (top 2 levels)

```
  campaign-control-plane/.gitignore (34b)
  campaign-control-plane/ARCHITECTURE.md (2054b)
  campaign-control-plane/FREEZE.md (1309b)
  campaign-control-plane/MANIFEST.sha256.json (7307b)
  campaign-control-plane/Makefile (100b)
  campaign-control-plane/README.md (2581b)
  campaign-control-plane/cli.py (1541b)
  campaign-control-plane/data/meta_bottlenecks.json (2514b)
  campaign-control-plane/data/portfolio.json (7903b)
  campaign-control-plane/data/repo_snapshots.json (112b)
  campaign-control-plane/data/shared_components.json (2131b)
  campaign-control-plane/docs/AUTONOMY.md (786b)
  campaign-control-plane/docs/GITHUB_SYNC.md (618b)
  campaign-control-plane/docs/PROJECT_THESIS_SCHEMA.md (567b)
  campaign-control-plane/docs/QP_INTEGRATION.md (619b)
  campaign-control-plane/docs/VALIDATION.md (1067b)
  campaign-control-plane/runtime/__init__.py (0b)
  campaign-control-plane/runtime/drift.py (572b)
  campaign-control-plane/runtime/eventlog.py (524b)
  campaign-control-plane/runtime/graph.py (867b)
  campaign-control-plane/runtime/model.py (575b)
  campaign-control-plane/runtime/poll_github.py (1999b)
  campaign-control-plane/runtime/qp_adapter.py (727b)
  campaign-control-plane/runtime/reward.py (384b)
  campaign-control-plane/runtime/validators.py (2600b)
  campaign-control-plane/schemas/checkpoint.schema.json (702b)
  campaign-control-plane/schemas/event.schema.json (354b)
  campaign-control-plane/schemas/htask.schema.json (301b)
  campaign-control-plane/schemas/receipt.schema.json (423b)
  campaign-control-plane/schemas/thesis.schema.json (456b)
  campaign-control-plane/server.py (1862b)
  campaign-control-plane/tests/test_drift.py (294b)
  campaign-control-plane/tests/test_graph.py (432b)
  campaign-control-plane/tests/test_portfolio.py (678b)
  campaign-control-plane/tests/test_server.py (254b)
  campaign-control-plane/tests/test_validators.py (1203b)
  campaign-control-plane/web/app.js (3126b)
  campaign-control-plane/web/index.html (1040b)
  campaign-control-plane/web/style.css (3152b)
```

## Original README excerpt

_Source: `campaign-control-plane/README.md`_

```markdown

# Campaign Control Plane — frozen 2026-09-14

This repository freezes the current portfolio into an executable project-management/control-plane prototype.
It is intentionally **not another agent framework**. It sits above existing kernels:

- **ATask** = factual task/run/proof/human boundary.
- **Seed0** = project-shape, tournaments, comparative trajectories and learning candidates.
- **QP / A-COM** = deterministic truth/authority, grants, proof levels and receipts.
- **Campaign Control Plane** = product theses → behavioral checkpoint DAGs → evidence contracts → next work / H-tasks / cross-project bottlenecks.

## North star

```text
THESIS
  ↓
CAMPAIGN GRAPH
  ↓
BEHAVIORAL CHECKPOINT
  ↓
AGENT BUILD VARIANTS
  ↓
APPEND-ONLY EVIDENCE
  ↓
DETERMINISTIC VALIDATOR
  ↓
QP-GATED TRANSITION / H-TASK
  ↓
RECEIPT
  ↓
TOURNAMENT + LEARNING
  ↓
NEXT CHECKPOINT
```

The businesses are useful products, but they are also worlds for solving the harder problem: **reliable autonomous creation from spec to externally verified functionality.**

## Run

```bash

... (+36 more lines in campaign-control-plane/README.md)
```

## How to use

- Raw zip stays in `docs/campaign-control-plane-2026-09-14.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/campaign-control-plane -q` (adjust to inner dir, e.g. `packages/campaign-control-plane/campaign-control-plane`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
