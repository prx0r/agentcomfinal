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
        |
        +------------- feedback / observed outcomes --------+
```

## Seesaw invariant

```text
Interfaces become cheap.
Cognition becomes cheap.
Implementation becomes cheap.

Consequential external state does not automatically become cheap.
```

Therefore Seesaw rewards projects/features attached to:

- exclusive or hard-to-reproduce state;
- live data-generating processes;
- authority / permission to act;
- real economic supply;
- proprietary state-action-outcome trajectories;
- trust / liability / reputation;
- network liquidity;
- regulated access;
- physical-world execution;
- scarce energy / compute / land / equipment;
- authenticated identity and durable relationships.

It penalizes:

- wrappers;
- generic UI;
- commodity code;
- static public-data transformations;
- generic prompts;
- routing/metadata tricks that a platform can absorb;
- features a stronger model can simply internalize;
- software whose only moat is "we built it first."

---

## Feature decision vocabulary

Every feature gets one of seven actions:

### `OWN`
Build/accumulate this as proprietary state. It is or can become the moat.

### `BUILD`
Build because the capability is strategically necessary and not cheaply reusable.

### `REUSE`
Use open source/API/platform capability. Do not spend personal capital rebuilding it.

### `BUY`
Procure a commodity service because ownership has weak strategic value.

### `VALIDATE`
Run the cheapest experiment because the economic claim is uncertain.

### `WATCH`
Potential future bottleneck; preserve optionality but do not invest heavily yet.

### `DROP`
Likely to commoditize or does not create durable external state.

---

## CLI

Score the included portfolio:

```bash
python -m seesaw.cli portfolio data/projects.json
```

Score one project:

```bash
python -m seesaw.cli project data/projects.json --id cmail
```

Evaluate features:

```bash
python -m seesaw.cli features data/projects.json --id breadup
```

Evaluate a disruptive event against the portfolio:

```bash
python -m seesaw.cli event examples/plugin_compiler_free.json data/projects.json
```

Generate reports:

```bash
python -m seesaw.cli report data/projects.json --out reports/portfolio.md
```

---

## Repository map

```text
docs/
  00_thesis.md
  01_formal_model.md
  02_agent_workflow.md
  03_project_shaping_rules.md
  04_feature_priority_rules.md
  05_plugin_agent_target_zone.md
  06_falsifiers.md

data/
  projects.json
  scarcity_classes.json

schemas/
  disruptive_event.schema.json
  project.schema.json
  feature.schema.json

src/seesaw/
  scoring.py
  engine.py
  event.py
  report.py
  cli.py

examples/
  plugin_compiler_free.json
  routing_solved.json
  world_model_jump.json

integrations/plugin_factory/
  README.md

tests/
  test_engine.py
```

---

## Strategic rule

The most useful Seesaw question for an agent-native project is:

> **Can a frontier lab destroy the differentiated value of this feature merely by writing better software?**

If yes: `REUSE`, `BUY`, `WATCH`, or `DROP`.

If no: identify the reason. The reason is probably the asset you should own.

