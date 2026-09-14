# autobuild2 — signed receipts + grant-gated spend (stdlib Python)

Hypothesis: ab1's pipeline plus real authority — every consequential action
needs a valid in-scope grant, every receipt is Ed25519-signed (vendored
from qp, zero new deps). Fail-closed like qp: unknown constraint = deny,
unsigned = deny.

Result: PASS — 13/13 tests, demo signed BUILD receipt verifies. See VALIDATION.json. Review: PASS WITH DEBT (live QP adapter deferred to ab3).

## Run

```bash
cd /agentcomfinal/agentcombuild/autobuild2
PYTHONPATH=../autobuild1/src:src python3 -m ab2.cli demo
python3 -m pytest tests/ -q   # needs ../autobuild1/src on path: see GO.sh
```

## Layout

- `SPEC.md` — delta over ab1. `VALIDATION.md`, `VALIDATION.json`.
- `src/ab2/` — `_vendored_ed25519.py` (provenance noted), `crypto.py`,
  `grants.py`, `gates2.py` (L1 gates), `build.py`, `cli.py`.
- `examples/` — lead plan (one consequential action) + evidence + demo seed.
- `review/` — criteria check vs scope G1/G2/G5/T1-sim + ab1 no-regression.
