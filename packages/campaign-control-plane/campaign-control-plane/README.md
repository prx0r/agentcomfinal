
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
python3 -m unittest discover tests -v
python3 cli.py check
python3 server.py
# open http://127.0.0.1:8787
```

Optional GitHub implementation snapshot:

```bash
GITHUB_TOKEN=... python3 cli.py poll-github
# or continuously (15 minute default)
GITHUB_TOKEN=... python3 -m runtime.poll_github --watch --interval 900
```

The token is optional for public repos. The poller stores commit/tree/file metadata only. **A repo snapshot can move a checkpoint to CODE_PRESENT/EVIDENCED but never PROVEN.**

## What is included

- 11 frozen project theses.
- 132 deterministic behavioral checkpoints (12/project).
- Explicit dependency order, M/H/A authority class, proof level, expected event/data contract, reward and implication for every checkpoint.
- Shared-component registry showing why Cmail/security/QP/ATask/Seed0/demand/plugin infrastructure compounds across projects.
- Meta-bottleneck registry for the human to solve structurally.
- Stdlib dashboard/API.
- Deterministic reference validator runtime.
- Fixture evidence for validator self-tests; fixtures are deliberately prohibited from producing `PROVEN`.
- GitHub poller that snapshots implementation state without confusing code with behavior.
- WASM validator ABI sketch; Python is the executable reference semantics in this prototype.

## Critical invariant

`PASS(fixture)` means **the validator works on a known fixture**.

`PASS(live)` means **the checkpoint behavior was observed in a real run**.

Only the latter may become `PROVEN`.
