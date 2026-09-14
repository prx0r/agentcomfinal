# autobuild1 — oneshot full system (stdlib Python)

Hypothesis: the whole loop — PLAN → specgate → seesaw → gates → RECEIPT →
report — fits in one small deterministic package with no new ideas, only
composition of qp + atask + canonical + autobuild-v0.2 + seesaw-module.

Result: PASS — 17/17 tests, demo BUILD receipt `passed=true`, value 217.01, binding photo-valuation-crosslist. See VALIDATION.json.

## Run

```bash
cd /agentcomfinal/autobuild1
PYTHONPATH=src python3 -m ab1.cli demo
PYTHONPATH=src python3 -m ab1.cli build examples/breadup_plan.json examples/breadup_evidence.json --now 2026-09-14T00:00:00Z
python3 -m pytest tests/ -q
```

## Layout

- `SPEC.md` — protocol. `VALIDATION.md` — criteria. `VALIDATION.json` — results.
- `src/ab1/` — canonical, specgate, seesaw, gates, receipts, store, cli.
- `examples/` — breadup mini-plan + evidence. `tests/` — the proof.
