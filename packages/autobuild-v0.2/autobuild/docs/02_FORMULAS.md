# Formulas

All formulas are versioned heuristics and remain inspectable.

## Underengineer priority

For feature `f`:

```text
MMP_f = (M * A * D * V) / (1 + C + L)
```

where `M`=moat contribution, `A`=asset accumulation, `D`=dependency centrality, `V`=early validation value, `C`=implementation cost, `L`=lab-attack risk. Inputs normalized 0..1.

`underengineer-v1` greedily selects the smallest dependency-closed set whose cumulative moat contribution reaches threshold 0.70, plus any feature explicitly marked `starts_moat_accumulation=true`.

## Existing Capability Coverage

```text
ECC = sum(weight_i * reuse_fitness_i) / sum(weight_i)
```

## Missing Delta

```text
MissingDelta_i = Requirement_i AND reuse_fitness_i < 0.80
```

## Useful run yield

```text
Y = 1.0F + 1.0N + 0.8E + 0.7X + 0.7C + 0.5O - 0.8D - 1.0U
```

`F` positive facts, `N` negative facts, `E` validated edges, `X` fixtures, `C` component evaluations, `O` real outcomes, `D` duplicates, `U` unsupported claims.

Raw contributions are retained regardless of score.

## Accretion efficiency

```text
AE = UsefulYield / (1 + CostUSD + lambda*TimeHours + mu*Tokens/1e6)
```

## Build utility

```text
BU = StrategicValue + InformationGain + AssetAccretion
     - ImplementationCost - MaintenanceSurface - PlatformCapture
```

Used only for ranking work, never for proving completion.

## Exact transformation

For every changed path:

```text
Delta_p = (old, new, op, reason, evidence)
```

Then `ChangeSetRoot = H(Canonical(sorted deltas))`.
