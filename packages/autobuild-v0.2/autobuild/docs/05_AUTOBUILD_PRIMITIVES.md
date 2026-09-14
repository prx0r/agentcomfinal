# Autobuild primitives

## COMPILE_PLAN
`PlanSpec -> TargetSpec` using deterministic compilation over already-structured input.

## UNDERENGINEER
Features -> minimum moat-producing dependency-closed feature set.

## PREBUILD_DISCOVER
`TargetSpec -> PrebuildRequest`; GitGoblin owns external search.

## APPLY_REUSE_PLAN
`TargetSpec + ReusePlan -> TargetSpec'` with exact ChangeSet and receipt.

## EMIT_QP_BRIDGE
`TargetSpec -> QP bridge input`. Autobuild does not import or duplicate QP.

## EMIT_ATASK_BRIDGE
`TargetSpec -> A-Task plan` with indexed acceptance, rerunnable evidence, and validator specs.

## ACCRUE_RUN
`RunContribution -> append-only ledger`; exact facts dedupe without erasing run history.

## DIFF
Artifact A + Artifact B -> exact structured `ChangeSet`.

## SUPERSEDE
Corrections append a new record pointing from old fact to new fact with reason + evidence. Historical facts are never edited.

## PROMOTE_PRIMITIVE
Repeated project-local pattern -> reusable primitive candidate. Promotion should eventually be QP-governed and require repeated use, deterministic schema, validator, and no project-local identifiers.
