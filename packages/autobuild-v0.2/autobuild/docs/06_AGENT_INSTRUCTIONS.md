# Instructions for an autobuild coding agent

## Mission
Make fuzzy approved plans executable without letting autonomous workers redefine success.

## Order

```text
READ StrategicSpec
-> READ PlanSpec
-> UNDERENGINEER
-> COMPILE TargetSpec
-> VALIDATE spec
-> PREBUILD via GitGoblin
-> APPLY reuse plan
-> VALIDATE again
-> EMIT QP/A-Task bridges
-> execute outside autobuild
-> ACCRUE all run contributions
```

## Rules
- Do not rewrite `/qp`, `/atask`, or `/gitgoblin`.
- Use explicit bridge artifacts/adapters.
- Do not create another cryptographic runtime, task queue, or GitHub search engine.
- Do not build commodity components before prebuild.
- Do not collapse technical and economic gates.
- Do not delete failed attempts.
- Preserve raw structured observations and normalized derived facts.
- Every score/formula must be inspectable.
- Every artifact change must be attributable to transformation + reason.
- If evidence is missing, output UNKNOWN.
