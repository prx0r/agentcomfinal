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
- compound,
- are difficult for machines to acquire cheaply,
- become complements to stronger AI,
- or carry a genuine human-source premium.

## Repository map

- `01_personal_seesaw_theory.md` — complete theory.
- `02_formal_model.md` — equations, variables, decision rules and falsifiers.
- `03_historical_backtests.md` — historical analogue tests.
- `04_creativity_as_world_model_divergence.md` — creativity, art, authenticity and teachability.
- `05_future_extremes.md` — logical extremes under very capable AI.
- `06_research_program.md` — experiments that could falsify or strengthen the framework.
- `data/historical_cases.csv` — scored historical cases.
- `data/motive_ontology.csv` — why humans do activities.
- `templates/disruption_event.json` — Seesaw-compatible dual industry/person event.
- `templates/divergence_log.csv` — creativity training log.
- `examples/ai_2026_events.json` — worked examples.
- `src/personal_seesaw.py` — lightweight scoring CLI.
- `SOURCES.md` — research basis.

## Five principles

### 1. Output substitution ≠ activity substitution
Machines can eliminate the economic scarcity of an output without eliminating mastery, play, identity, communication or ritual.

### 2. Evaluate chains, not isolated tasks
If AI can do 8 of 10 steps but cannot close the economically necessary chain, the workflow may remain human-bound. Conversely, closing the last blocking step can cause a discontinuous shock.

### 3. Source can be part of the product
For art, testimony, handmade craft, live performance, advice or care, consumers may value not only sensory output but *who made it, why, and through what experience*.

### 4. Prefer positive-AI-beta personal capital
The strongest assets are those whose value rises as machine intelligence rises:

\[
\frac{\partial V(asset)}{\partial AI} > 0.
\]

### 5. Live in probability-weighted futures, not one prophecy
A vivid future is not a forecast. Long causal chains compound uncertainty. Personal capital should be robust across several plausible capability timelines.

## One-line summary

**Own or become the bottleneck created by the thing that is making your old bottleneck cheap.**
