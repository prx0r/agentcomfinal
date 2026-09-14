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
python3 -m unittest discover tests -v
python3 cli.py check
python3 cli.py schedule
python3 cli.py worlds
python3 cli.py profiles
python3 cli.py simulate breadup
python3 cli.py hdesk
python3 cli.py performance
python3 cli.py selflab
python3 server.py
# http://127.0.0.1:8787
```

Add a valid human task:

```bash
python3 cli.py htask-add strategic_direction \
  "Which of these two customer segments should receive the next real probe?" \
  --project breadup --option casual-sellers --option power-resellers \
  --recommendation casual-sellers --why-human "This is an owner portfolio tradeoff after equal evidence." \
  --blocking-value 8 --minutes 2
```

Answer it:

```bash
python3 cli.py htask-answer H-... casual-sellers
```

The answer records a bounded decision only. QP still governs external consequences.

## Important files

- `data/experiment_worlds.json` — A/B/C/D worlds and evidence ceilings.
- `data/target_profiles.json` — markets Seesaw can route hypotheses into.
- `data/resource_constraints.json` — account/store/human/permission capacity.
- `data/strategy_families.json` + `experiment_runs.jsonl` — empirical replication loop.
- `data/breadup_self_lab.json` — self-dogfood commerce-data architecture.
- `runtime/scheduler.py` — resource-aware live portfolio queue.
- `runtime/experiments.py` — WORLD_SELECT.
- `runtime/hdesk.py` — strategic human queue.
- `runtime/simulation.py` — non-canonical preflight sensitivity.
- `runtime/performance.py` — real-outcome-only family learning.

See `V3_CHANGES.md` and `docs/` for the full contracts.
