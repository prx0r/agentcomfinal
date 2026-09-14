# autobuild3 — a-log telemetry + stoplight (atask-native)

Hypothesis: the atask loop ports cleanly — agent appends hash-chained
telemetry lines tagging acceptance indices with re-runnable evidence, and an
independent stoplight re-executes every claim. The agent never judges: no
status field exists for it to set, verdict files are recomputed not read,
and false telemetry fails the task.

Result: PASS — 29/29 tests, demo GO, review PASS WITH DEBT. See VALIDATION.json. Axiom `../actuality.md` implemented: probe/judge split, CEL-subset judges, Actuality DAG, independent readback, registry v0.

## Run

```bash
cd /agentcomfinal/agentcombuild/autobuild3
PYTHONPATH=../autobuild1/src:src python3 -m ab3.cli demo
python3 -m pytest tests/ -q   # same PYTHONPATH as above
```

## Layout

- `SPEC.md` — a-log/stoplight protocol. `VALIDATION.md`, `VALIDATION.json`.
- `src/ab3/` — `alog.py` (chained telemetry, refusals), `stoplight.py`
  (re-execution judge + validator contract + acheck), `gates3.py`,
  `cli.py` (log/judge/acheck/demo).
- `validators/lead-reply.py` — example mechanical validator.
- `examples/lead3_plan.json` — goal + features with `covers` index maps.
- `review/` — criteria check vs scope A1–A6 + chain no-regression.
