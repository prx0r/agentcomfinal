# 6. Research Program

Personal Seesaw should be falsifiable.

## A. Historical backtest

### H1
Activities with high predicted chain closure and low human-source premium suffer larger declines in economic skill rents.

Method:
1. choose 50 historical technologies,
2. define cutoff before mass adoption,
3. score only information available by cutoff,
4. estimate chain closure, cost slope, deployment friction, source premium, demand elasticity,
5. measure later wage/employment/output-price changes.

Baselines:
- occupation automation exposure,
- mean task share automated,
- expert narrative forecast.

Success:
Personal Seesaw improves prediction of:
- wage compression,
- task reorganization,
- premium-craft survival,
- migration to complementary roles.

## B. Human-source premium experiment

### H2
Matched artifacts receive different value when credible provenance changes.

Randomize identical works across labels:
- human-created,
- AI-created,
- human + AI,
- unknown.

Measure:
- liking,
- willingness to pay,
- depth,
- emotional involvement,
- memorability,
- desire to follow creator.

Reveal process evidence and retest.

Falsifier:
If provenance effects reliably converge to zero across domains/cohorts, reduce the human-premium weight.

## C. Lived-experience detection

### H3
People may fail to detect lived experience from content alone, while verified lived provenance still changes value.

Conditions:
- genuine autobiographical passages,
- human fictional passages,
- AI imitations,
- AI transformations of autobiographical material.

Blind origin, measure classification, then reveal provenance.

This separates:
1. content detectability,
2. provenance utility.

## D. Creativity-training RCT

### H4
Explicit prediction + divergence journaling improves calibrated creative novelty more than generic brainstorming.

Groups:
- A: ordinary creative practice,
- B: divergent-thinking prompts,
- C: predict → observe → divergence → update → analogy → artifact → decode-test.

Run 8–12 weeks.

Measure:
- novelty,
- usefulness/coherence,
- cross-domain analogy,
- calibration,
- audience reconstruction accuracy,
- longitudinal distinctiveness.

## E. World-model delta metric

Embed:
- prior statement,
- observation,
- update,
- artifact.

Test whether artifact representations predict the creator's stated model update.

Candidate:

\[
TransmissionFidelity=
sim(Decode(artifact),\Delta WorldModel).
\]

This is a potential proxy for "the work carries the update."

## F. Personal skill half-life dataset

Build:

```text
technology
date
affected_task
performance_curve
cost_curve
chain_closure_date
wage_before
wage_after
employment_before
employment_after
premium_craft_survival
human_practice_survival
complement_skill
```

Fit hazard/survival models for economic skill rents.

## G. New-signal dual forecast test

Every month, ingest frontier innovations and freeze two forecasts:

```text
INDUSTRY
- constraints tightened/loosened
- shadow prices
- winners/losers
- timing
- falsifiers

PERSON
- skills commoditized
- skills complemented
- source premiums
- practices unaffected
- acquisition half-lives
- stop/start/own/practice
- falsifiers
```

Timestamp them and score at 6/12/24 months.

This lets the framework learn rather than become an unfalsifiable worldview.

## H. Creativity tutor MVP

Do **not** start by generating art.

Build:
1. prediction logger,
2. observation logger,
3. divergence scorer,
4. longitudinal memory,
5. recurring-pattern graph,
6. analogy retriever,
7. audience decode collector.

The AI should ask:

> What changed in your model?

before:

> Want me to write it for you?

That preserves the scarce human input.

## I. Core metrics

Economic:
- wage delta,
- employment delta,
- price delta,
- machine share,
- task share,
- complementary occupation growth.

Human residual:
- participation despite superior machine output,
- willingness to pay for human provenance,
- live-event premium,
- hobby participation,
- community persistence.

Creativity:
- novelty,
- coherence,
- calibration,
- update magnitude,
- transmission fidelity,
- recurrence depth,
- analogical distance,
- human-source premium.

## J. Whole-theory falsifiers

Personal Seesaw is weakened if:

1. Machine improvements do not systematically change relative task scarcity.
2. Chain closure adds little beyond average task exposure.
3. Human provenance premiums disappear rapidly and broadly.
4. Intrinsic human practice collapses whenever machines exceed human performance.
5. Positive-AI-beta assets are also cheaply synthesized/controlled by machines.
6. Framework forecasts do not beat naive extrapolation.
7. Divergence-based creativity training does no better than generic practice.

A theory that cannot lose is not useful.
