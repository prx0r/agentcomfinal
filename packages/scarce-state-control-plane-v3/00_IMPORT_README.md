# Scarce-State Control Plane v3 / Autonomous Economic Discovery (2026-09-14)

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `scarce-state-control-plane-v3`
- **source zip:** `docs/autonomous-economic-discovery-control-plane-v3-2026-09-14.zip` (225822 bytes)
- **unpacked:** 112 files, 596769 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 3 entries cleaned)
- **top-level inside:** `scarce-state-control-plane`
- **original README(s):** `scarce-state-control-plane/README.md`

## What this is

V3 discovery control plane. Portfolio of 13 projects, experiment worlds, fixtures per project, scarce-asset ledger, human tasks. Largest dataset in dump.

## Layout (top 2 levels)

```
  scarce-state-control-plane/.gitignore (34b)
  scarce-state-control-plane/ARCHITECTURE.md (2623b)
  scarce-state-control-plane/FREEZE.md (1097b)
  scarce-state-control-plane/MANIFEST.sha256.json (13727b)
  scarce-state-control-plane/Makefile (100b)
  scarce-state-control-plane/README.md (3952b)
  scarce-state-control-plane/TEST_REPORT.md (1398b)
  scarce-state-control-plane/V2_CHANGES.md (1694b)
  scarce-state-control-plane/V3_CHANGES.md (3312b)
  scarce-state-control-plane/cli.py (4952b)
  scarce-state-control-plane/data/breadup_self_lab.json (1272b)
  scarce-state-control-plane/data/experiment_runs.jsonl (0b)
  scarce-state-control-plane/data/experiment_worlds.json (6115b)
  scarce-state-control-plane/data/human_task_templates.json (1285b)
  scarce-state-control-plane/data/human_tasks.json (57b)
  scarce-state-control-plane/data/mcp_miner_example.json (687b)
  scarce-state-control-plane/data/meta_bottlenecks.json (5233b)
  scarce-state-control-plane/data/portfolio.json (18192b)
  scarce-state-control-plane/data/repo_snapshots.json (112b)
  scarce-state-control-plane/data/resource_classes.json (1576b)
  scarce-state-control-plane/data/resource_constraints.json (3015b)
  scarce-state-control-plane/data/scarce_asset_ledger.json (186b)
  scarce-state-control-plane/data/shared_components.json (3742b)
  scarce-state-control-plane/data/strategy_families.json (1401b)
  scarce-state-control-plane/data/target_profiles.json (1960b)
  scarce-state-control-plane/data/underengineer_state.json (1095b)
  scarce-state-control-plane/docs/AUTONOMY.md (840b)
  scarce-state-control-plane/docs/BREADUP_DOGFOOD.md (1247b)
  scarce-state-control-plane/docs/EXPERIMENT_WORLDS.md (1802b)
  scarce-state-control-plane/docs/GITHUB_SYNC.md (618b)
  scarce-state-control-plane/docs/HUMAN_DESK.md (1406b)
  scarce-state-control-plane/docs/MCP_SCARCITY_MINER.md (677b)
  scarce-state-control-plane/docs/PORTFOLIO_SCHEDULER.md (1381b)
  scarce-state-control-plane/docs/PROJECT_THESIS_SCHEMA.md (1139b)
  scarce-state-control-plane/docs/QP_INTEGRATION.md (619b)
  scarce-state-control-plane/docs/SCARCE_STATE.md (1406b)
  scarce-state-control-plane/docs/SEESAW_MARKET_LAB.md (997b)
  scarce-state-control-plane/docs/SMB_CHATGPT_MIGRATION.md (1275b)
  scarce-state-control-plane/docs/UNDERENGINEER.md (1945b)
  scarce-state-control-plane/docs/VALIDATION.md (1067b)
  scarce-state-control-plane/docs/VALIDATION_V2.md (924b)
  scarce-state-control-plane/runtime/__init__.py (0b)
  scarce-state-control-plane/runtime/attestation.py (1565b)
  scarce-state-control-plane/runtime/drift.py (572b)
  scarce-state-control-plane/runtime/eventlog.py (524b)
  scarce-state-control-plane/runtime/experiments.py (1694b)
  scarce-state-control-plane/runtime/graph.py (867b)
  scarce-state-control-plane/runtime/hdesk.py (2186b)
  scarce-state-control-plane/runtime/model.py (602b)
  scarce-state-control-plane/runtime/performance.py (2822b)
  scarce-state-control-plane/runtime/poll_github.py (1999b)
  scarce-state-control-plane/runtime/qp_adapter.py (727b)
  scarce-state-control-plane/runtime/resources.py (335b)
  scarce-state-control-plane/runtime/reward.py (1292b)
  scarce-state-control-plane/runtime/scarcity.py (1187b)
  scarce-state-control-plane/runtime/scheduler.py (3655b)
  scarce-state-control-plane/runtime/selflab.py (112b)
  scarce-state-control-plane/runtime/simulation.py (810b)
  scarce-state-control-plane/runtime/underengineer.py (3843b)
  scarce-state-control-plane/runtime/validators.py (4514b)
  ... +25 more
```

## Original README excerpt

_Source: `scarce-state-control-plane/README.md`_

```markdown
# Autonomous Economic Discovery Control Plane — v3 frozen 2026-09-14

v3 turns the Scarce State Control Plane into a **multi-market experimental operating system**.

> **Seesaw discovers migrating scarcity → WORLD_SELECT finds the cheapest real feedback environment → UNDERENGINEER builds only what that experiment requires → agents iterate until deterministic/external gates pass → QP controls consequential action → outcome/scarce-state receipts update the portfolio → the scheduler reallocates resources.**

The human endgame is intentionally narrow: answer bounded strategic questions, do physical/platform/identity tasks agents cannot access, handle trust/relationship work, and approve consequential authority. Agents own implementation, simulation, tests, monitoring and iteration.

## New in v3

### Four feedback worlds

- **A_TRUTH** — paper trading / frozen forecasts.
- **B_DEMAND** — ChatGPT apps and free tools.
- **C_ECONOMIC** — Etsy/marketplace/paid outcomes.
- **D_SCARCE_STATE** — permissions, proprietary transactions, physical observations and network participants.

### ChatGPT apps stay — but as probes

ChatGPT surfaces are cheap places to measure real task intent and repeat use. They are not assumed to be durable moats. Winning probes should graduate toward external economic/scarce-state loops.

### Seesaw Market Lab

`seesaw-market-lab` is a 13th campaign/lab. It preregisters causal claims and paper positions, resolves them from external data and builds a longitudinal calibration corpus. Paper success does **not** claim live execution alpha.

### Explicit resource bottlenecks

`data/resource_constraints.json` models stores, accounts, human attention, permissions and physical capacity. Current planning assumptions include one primary Etsy store and one primary ChatGPT app account. The Etsy £14 value is stored as a user-supplied planning assumption and is editable.

### Strategic H-task desk

Only six classes may reach the human: direction, physical access, identity/KYC, spend approval, relationships/trust, and genuine taste/value judgement. Debugging is not an H-task class.

### BreadUp self-lab

The portfolio now dogfoods BreadUp's architecture: signal → hypothesis → simulation/backtest → live offer/action → real outcome → normalized dataset → strategy replication/kill.

## Run

```bash

... (+45 more lines in scarce-state-control-plane/README.md)
```

## How to use

- Raw zip stays in `docs/autonomous-economic-discovery-control-plane-v3-2026-09-14.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/scarce-state-control-plane-v3 -q` (adjust to inner dir, e.g. `packages/scarce-state-control-plane-v3/scarce-state-control-plane`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
