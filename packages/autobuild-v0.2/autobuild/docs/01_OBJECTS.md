# Canonical objects

## StrategicSpec
Produced by Seesaw. Autobuild hashes and references it but does not decide strategic truth.

## PlanSpec
Structured pre-compilation plan: objective, features, constraints, interfaces, budgets, risks.

## Capability
A user-visible or system-visible ability composed from requirements.

## Requirement
Atomic proposition that can be independently proven. Fields: id, statement, feature, dependencies, evidence contract, validator, criticality, optional authority.

## EvidenceContract
Declares accepted evidence forms such as command exit code, JSON file, HTTP response, DNS observation, transaction record, webhook observation, or metric threshold.

## Validator
Versioned deterministic rule returning `PASS` or `FAIL`. Missing required evidence yields requirement state `UNKNOWN` before validation.

## CompletionCircuit
Boolean expression over requirement states. `UNKNOWN` never passes a hard circuit.

## TargetSpec
Canonical compilation product. Defines what `done` means.

## PrebuildRequest
Requirements transformed into reusable-component search jobs for GitGoblin.

## ReusePlan
Maps requirements to `REUSE | BUY | BUILD | BLOCK` with fitness/provenance/rights.

## WorkSpec
Only missing implementation delta becomes work.

## ChangeSet
Exact deterministic difference between canonical artifacts.

## TransformationReceipt
Binds input root, transformation id, output root, changeset root, reasons, evidence ids.

## RunContribution
Structured information produced by a run independent of operational success.

## AccretionLedger
Append-only JSONL. Historical records are never edited; corrections supersede old records explicitly.
