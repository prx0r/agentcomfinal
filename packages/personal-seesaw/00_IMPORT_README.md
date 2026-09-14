# Personal Seesaw v0.1

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `personal-seesaw`
- **source zip:** `docs/personal-seesaw-v0.1.zip` (32162 bytes)
- **unpacked:** 15 files, 66385 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `personal-seesaw`
- **original README(s):** `personal-seesaw/README.md`

## What this is

Research repo for personal Seesaw: theory, formal Future-Adjusted Personal Value model, 10 historical backtests, creativity-as-divergence, future extremes, research program + minimal py src.

## Layout (top 2 levels)

```
  personal-seesaw/01_personal_seesaw_theory.md (8919b)
  personal-seesaw/02_formal_model.md (5145b)
  personal-seesaw/03_historical_backtests.md (9749b)
  personal-seesaw/04_creativity_as_world_model_divergence.md (12495b)
  personal-seesaw/05_future_extremes.md (5290b)
  personal-seesaw/06_research_program.md (4777b)
  personal-seesaw/README.md (4026b)
  personal-seesaw/SOURCES.md (6441b)
  personal-seesaw/data/historical_cases.csv (1556b)
  personal-seesaw/data/motive_ontology.csv (1327b)
  personal-seesaw/examples/ai_2026_events.json (3214b)
  personal-seesaw/examples/generic_copywriting_score.json (291b)
  personal-seesaw/src/personal_seesaw.py (1786b)
  personal-seesaw/templates/disruption_event.json (1144b)
  personal-seesaw/templates/divergence_log.csv (225b)
```

## Original README excerpt

_Source: `personal-seesaw/README.md`_

```markdown
# Personal Seesaw

**A framework for allocating a finite human life under accelerating technological change.**

Version 0.1 — 2026-09-14

## Thesis

Seesaw asks what a technological innovation does to economic constraints:

> Innovation → ΔConstraint → ΔShadow Price → Capital Allocation → Supply Response → Constraint Relaxation.

**Personal Seesaw** applies the same logic to a person's finite stock of time:

> Innovation → ΔMachine Capability → ΔTask Feasibility → ΔHuman Scarcity → ΔReturn to Skill / ΔHuman Premium / ΔPractice Utility → Time Allocation → Personal Capital.

The crucial correction is that **economic obsolescence is not human obsolescence**.

A machine can make an output effectively free while humans continue to perform and value the activity because they were never optimizing only for output. Humans also act for mastery, play, identity, status, belonging, communication, witness, ritual, embodiment, autonomy, care, curiosity and transcendence.

Chess after superhuman engines is not irrational. Running after cars is not irrational. Painting after photography is not irrational. Playing music after generative music is not irrational. One purpose became cheap while others remained scarce.

This repository therefore uses **three ledgers**:

1. **Market ledger** — what will still earn rents?
2. **Human ledger** — what remains worth doing even if the output is free?
3. **Option ledger** — what practice builds capabilities/assets that become more valuable as technology advances?

## Core rule

Do not ask only:

> Will this job still exist?

Ask:

> Which component of this activity is becoming abundant, which component remains scarce, and why does a human do it?

Prefer activities whose scarce components:
- survive across several plausible technological futures,

... (+45 more lines in personal-seesaw/README.md)
```

## How to use

- Raw zip stays in `docs/personal-seesaw-v0.1.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/personal-seesaw -q` (adjust to inner dir, e.g. `packages/personal-seesaw/personal-seesaw`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
