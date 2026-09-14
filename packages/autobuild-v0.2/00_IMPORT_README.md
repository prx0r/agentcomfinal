# Autobuild v0.2 hardened

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `autobuild-v0.2`
- **source zip:** `docs/autobuild-v0.2-hardened.zip` (59884 bytes)
- **unpacked:** 54 files, 150326 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `autobuild`
- **original README(s):** `autobuild/README.md, autobuild/adapters/README.md`

## What this is

Hardened plan-compiler pipeline: prebuild -> specgate -> plangate -> accretion/promotion with bridges, circuits, ledger, receipts. Includes peer-review script + tests.

## Layout (top 2 levels)

```
  autobuild/AGENTS.md (961b)
  autobuild/HANDOFF.md (1138b)
  autobuild/KNOWN_LIMITATIONS.md (1236b)
  autobuild/Makefile (597b)
  autobuild/README.md (4255b)
  autobuild/VALIDATION.json (2221b)
  autobuild/adapters/README.md (900b)
  autobuild/autobuild/__init__.py (22b)
  autobuild/autobuild/accretion.py (4513b)
  autobuild/autobuild/admission.py (687b)
  autobuild/autobuild/bridges.py (5111b)
  autobuild/autobuild/canonical.py (560b)
  autobuild/autobuild/circuit.py (1292b)
  autobuild/autobuild/cli.py (3339b)
  autobuild/autobuild/compiler.py (3306b)
  autobuild/autobuild/delta.py (1282b)
  autobuild/autobuild/facts.py (1145b)
  autobuild/autobuild/ledger.py (1333b)
  autobuild/autobuild/plangate.py (2602b)
  autobuild/autobuild/prebuild.py (4755b)
  autobuild/autobuild/primitives.py (2339b)
  autobuild/autobuild/promotion.py (1075b)
  autobuild/autobuild/qp_circuit_spec.py (3073b)
  autobuild/autobuild/receipt.py (566b)
  autobuild/autobuild/report.py (862b)
  autobuild/autobuild/roots.py (3066b)
  autobuild/autobuild/specgate.py (8331b)
  autobuild/autobuild/tristate.py (444b)
  autobuild/autobuild/underengineer.py (3039b)
  autobuild/autobuild/validator_codegen.py (2613b)
  autobuild/autobuild/validators.py (1636b)
  autobuild/autobuild/verified_import.py (1284b)
  autobuild/docs/00_ARCHITECTURE.md (2356b)
  autobuild/docs/01_OBJECTS.md (1677b)
  autobuild/docs/02_FORMULAS.md (1519b)
  autobuild/docs/03_PIPELINE.md (1549b)
  autobuild/docs/04_INVARIANTS.md (1103b)
  autobuild/docs/05_AUTOBUILD_PRIMITIVES.md (1138b)
  autobuild/docs/06_AGENT_INSTRUCTIONS.md (961b)
  autobuild/docs/07_LEGO_MODEL.md (1312b)
  autobuild/docs/08_FRONTIER_PEER_REVIEW.md (12435b)
  autobuild/fixtures/prebuild_response.json (1539b)
  autobuild/fixtures/run_contribution.json (1102b)
  autobuild/pyproject.toml (287b)
  autobuild/schemas/plan_spec.schema.json (6315b)
  autobuild/schemas/run_contribution.schema.json (931b)
  autobuild/schemas/target_spec.schema.json (9390b)
  autobuild/scripts/peerreview.py (4729b)
  autobuild/tests/test_autobuild.py (4172b)
  autobuild/tests/test_end_to_end.py (2057b)
  autobuild/tests/test_peerreview.py (9466b)
```

## Original README excerpt

_Source: `autobuild/README.md`_

```markdown
# autobuild

**Canonical compiler from strategy to provable autonomous work.**

`autobuild` sits between strategic judgment and execution.

It does not replace `qp`, `atask`, or `gitgoblin`.

```text
idea / campaign / business plan
            |
            v
        SEESAW
   should this exist?
            |
            v
      StrategicSpec
            |
            v
     UNDERENGINEER
 minimum moat-producing path
            |
            v
        AUTOBUILD
 intent -> exact TargetSpec
            |
       +----+-----+
       |          |
       v          v
   GITGOBLIN      QP
   prebuild       truth/authority
   reuse plan     runtime
       |          |
       +----+-----+
            v
          A-TASK
       executable work
            |
            v
          workers

... (+108 more lines in autobuild/README.md)
```

## How to use

- Raw zip stays in `docs/autobuild-v0.2-hardened.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/autobuild-v0.2 -q` (adjust to inner dir, e.g. `packages/autobuild-v0.2/autobuild`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
