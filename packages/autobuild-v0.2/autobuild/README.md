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
            |
            v
 evidence / failures / outcomes
            |
      +-----+------+
      |            |
      v            v
     QP          SEESAW
    proof       economic update
```

## Core idea

A worker may be arbitrarily creative about **how** to achieve a target.

It may not redefine **what counts as success**.

`autobuild` turns an approved intent into frozen structured data:

- capabilities;
- requirements;
- dependencies;
- evidence contracts;
- deterministic validators;
- completion circuits;
- authority requirements;
- reuse candidates;
- missing delta;
- economic outcome gates;
- falsifiers.

Every transformation is canonicalized, hashed, and emitted as an append-only receipt.

## The additive-run invariant

> **A run that consumes resources but leaves no new structured reusable state is a failed system run, even when the worker's immediate task failed correctly.**

A failed attempt may still add a rejected repository, incompatibility, measured cost/latency, API constraint, edge case, validator fixture, source observation, dependency relationship, or explicit `UNKNOWN`.

Canonical yield:

```text
UsefulYield(run) =
  NewFacts
+ NewNegativeFacts
+ NewValidatedEdges
+ NewFixtures
+ NewReusableComponents
+ NewOutcomeRows
- Duplicates
- UnsupportedClaims
```

A run may close with task `FAIL` and still have positive `UsefulYield`.

## State model

Nothing is silently mutated.

```text
Artifact A
   |
Transformation
   |
ChangeSet
   |
Artifact B
   |
ValidationReceipt
```

Each `ChangeSet` records exact path, old/new hashes, transformation id, reasons and evidence ids. Old artifacts remain addressable forever.

## Core commands

```bash
python -m autobuild.cli compile examples/breadup_minimum_moat/plan.json --out build/breadup
python -m autobuild.cli validate build/breadup/target_spec.json
python -m autobuild.cli underengineer examples/breadup_minimum_moat/plan.json
python -m autobuild.cli prebuild build/breadup/target_spec.json --out build/breadup/prebuild_request.json
python -m autobuild.cli apply-prebuild build/breadup/target_spec.json fixtures/prebuild_response.json --out build/breadup/target_spec.prebuilt.json
python -m autobuild.cli bridges build/breadup/target_spec.prebuilt.json --out build/breadup/bridges
python -m autobuild.cli diff build/breadup/target_spec.json build/breadup/target_spec.prebuilt.json
python -m autobuild.cli accrue fixtures/run_contribution.json --ledger build/accretion.jsonl
```

## Hard boundaries

- **Seesaw:** Is this worth doing? What is scarce? What is the kill condition?
- **autobuild:** What exact observable reality would make the approved plan true?
- **GitGoblin:** What already exists, under what rights/quality, and what remains missing?
- **QP / A-COM:** Did the claimed transition pass frozen gates under valid evidence/grants?
- **A-Task:** Which bounded work is ready, and did rerunnable proof turn green?

## Design doctrine

1. JSON first.
2. Canonical bytes before prose.
3. Append; never rewrite history.
4. `UNKNOWN` is valid; it never passes a hard gate.
5. Failure is data.
6. Evidence must be rerunnable or externally observable.
7. Exact formulas are versioned.
8. Every transformation emits an auditable `ChangeSet`.
9. Every reusable primitive gets a stable content-derived key.
10. Commodity implementation is searched before built.
11. Only the missing delta becomes work.
12. Economic success and technical completion are separate circuits.
