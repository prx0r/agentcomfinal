# Seesaw Agent Module v0.1

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `seesaw-agent-module`
- **source zip:** `docs/seesaw-agent-module-v0.1.zip` (39854 bytes)
- **unpacked:** 28 files, 66444 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 3 entries cleaned)
- **top-level inside:** `seesaw-agent-module`
- **original README(s):** `seesaw-agent-module/README.md, seesaw-agent-module/integrations/plugin_factory/README.md`

## What this is

Working Seesaw strategy agent: NewInfo -> dCapability -> dConstraint -> dScarcity -> dValue -> dPriority. OWN/BUILD/REUSE/BUY/VALIDATE/WATCH/DROP. Engine + scoring + report + CLI + docs 00-06.

## Layout (top 2 levels)

```
  seesaw-agent-module/AGENTS.md (1611b)
  seesaw-agent-module/README.md (4343b)
  seesaw-agent-module/VALIDATION.json (4529b)
  seesaw-agent-module/data/projects.json (19157b)
  seesaw-agent-module/data/scarcity_classes.json (1843b)
  seesaw-agent-module/docs/00_thesis.md (3251b)
  seesaw-agent-module/docs/01_formal_model.md (4282b)
  seesaw-agent-module/docs/02_agent_workflow.md (3025b)
  seesaw-agent-module/docs/03_project_shaping_rules.md (2596b)
  seesaw-agent-module/docs/04_feature_priority_rules.md (2510b)
  seesaw-agent-module/docs/05_plugin_agent_target_zone.md (1728b)
  seesaw-agent-module/docs/06_falsifiers.md (1830b)
  seesaw-agent-module/examples/plugin_compiler_free.json (580b)
  seesaw-agent-module/examples/routing_solved.json (494b)
  seesaw-agent-module/examples/world_model_jump.json (546b)
  seesaw-agent-module/pyproject.toml (277b)
  seesaw-agent-module/reports/portfolio.md (2570b)
  seesaw-agent-module/schemas/disruptive_event.schema.json (591b)
  seesaw-agent-module/schemas/feature.schema.json (269b)
  seesaw-agent-module/schemas/project.schema.json (564b)
  seesaw-agent-module/tests/test_engine.py (876b)
```

## Original README excerpt

_Source: `seesaw-agent-module/README.md`_

```markdown
# Seesaw Agent Module

**Autonomous strategic allocation under accelerating AI capability.**

Seesaw is a control-plane module for deciding what to build, own, reuse, buy, drop, or merely watch as new technological information changes the scarcity structure around a project.

The core question is:

> **If frontier models, agent platforms, and open-source software absorb everything that can be absorbed by better software, what scarce state is left behind — and do we own it?**

This repository turns that question into a repeatable workflow.

---

## Core loop

```text
NEW DISRUPTIVE INFORMATION
        |
        v
CAPABILITY DELTA
What just became cheaper / easier / possible?
        |
        v
CONSTRAINT GRAPH
Which bottlenecks loosened? Which tightened?
        |
        v
SHADOW-PRICE UPDATE
What became less/more scarce?
        |
        +---------------------------+
        |                           |
        v                           v
INDUSTRY SEESAW                PROJECT SEESAW
markets/assets                 projects/features
        |                           |
        v                           v
capital allocation            OWN / BUILD / REUSE /
                              DROP / WATCH / VALIDATE

... (+154 more lines in seesaw-agent-module/README.md)
```

## How to use

- Raw zip stays in `docs/seesaw-agent-module-v0.1.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/seesaw-agent-module -q` (adjust to inner dir, e.g. `packages/seesaw-agent-module/seesaw-agent-module`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
