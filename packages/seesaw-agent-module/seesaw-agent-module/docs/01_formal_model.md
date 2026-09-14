# 1. Formal Model

## 1.1 Scarcity vector

Each project/feature is scored on a scarcity vector \(s\):

\[
s =
[E, A, T, N, P, R, L, C, V, X]
\]

where:

- \(E\): exclusive/live state
- \(A\): authority / permission to act
- \(T\): proprietary trajectories (state → action → outcome)
- \(N\): network/liquidity
- \(P\): physical scarcity/supply
- \(R\): trust/reputation/regulatory standing
- \(L\): lock-in from accumulated longitudinal state
- \(C\): AI complementarity
- \(V\): verifiability / measurable outcomes
- \(X\): externality — cannot be synthesized by pure reasoning

Each normalized to 0–5.

## 1.2 Fragility vector

\[
q =
[W, U, D, S, F, H]
\]

where:

- \(W\): wrapper risk
- \(U\): public replicability
- \(D\): dependency/platform capture risk
- \(S\): synthetic substitutability
- \(F\): feature internalization risk
- \(H\): human distribution/sales burden

Higher is worse.

## 1.3 Moat score

\[
Moat =
\frac{
\sum_i \alpha_i s_i
}{
\sum_i \alpha_i
}
-
\lambda
\frac{
\sum_j \beta_j q_j
}{
\sum_j \beta_j
}
\]

Rescale to 0–100.

The default weights intentionally overweight:
- external state;
- authority;
- trajectories;
- physical supply;
- AI complementarity;
- externality.

## 1.4 Ownership score

A strong opportunity can still be poor if **someone else owns the scarce variable**.

Define:

\[
Ownership =
\frac{
OwnedState
+ OwnedAuthority
+ OwnedTrajectories
+ OwnedNetwork
+ OwnedSupply
}{
5}
\]

Each term 0–5.

Then:

\[
StrategicValue = Moat \times (0.45 + 0.55 \cdot Ownership/5)
\]

Thus a project depending on Shopify's data may be useful but scores lower unless it accumulates something proprietary.

## 1.5 Lab Attack Resistance

For feature \(f\):

\[
LAR_f =
P(
\text{frontier platform can absorb core user value through software alone}
)
\]

Practical 0–5 proxy:

- 0: impossible without our scarce state/rights/supply.
- 1: model improvement helps us.
- 2: some UI/orchestration commoditizes, core remains.
- 3: substantial overlap.
- 4: platform could reproduce most differentiated value.
- 5: one platform release makes feature irrelevant.

## 1.6 Reuse decision

Let:

- \(M_f\): moat contribution;
- \(I_f\): integration/strategic necessity;
- \(O_f\): ownability;
- \(R_f\): reusable implementation availability;
- \(C_f\): cost.

Then:

\[
BuildPriority_f =
M_f \cdot O_f \cdot I_f - R_f - C_f
\]

Operationally:

```text
High moat + high ownability    -> OWN
High necessity, low OSS reuse  -> BUILD
High reuse + low moat          -> REUSE
Commodity external service     -> BUY
Uncertain economics            -> VALIDATE
Potential future bottleneck    -> WATCH
High fragility + low ownership -> DROP
```

## 1.7 Feature marginal value

Do not score features in isolation.

For feature \(f\) added to project \(p\):

\[
\Delta SV(f|p)=SV(p+f)-SV(p)
\]

Prioritize features that increase:
- proprietary state;
- authority;
- trajectory generation;
- trust;
- physical execution;
- network state.

Deprioritize features that only increase:
- UI polish;
- generic intelligence;
- generic retrieval;
- generic workflow orchestration;
- generic code.

## 1.8 Event update

A disruptive event \(e\) changes project scores:

\[
s' = s + \Delta s(e)
\]

\[
q' = q + \Delta q(e)
\]

Examples:

### Prompt → plugin becomes free
- wrapper risk +2
- public replicability +1
- platform dependency +1
- software-interface moat -2
- external-state relative value +1

### Tool routing becomes solved
- metadata/routing feature moat → 0
- proprietary capability value unchanged
- distribution ambiguity decreases

### Strong robotics breakthrough
- physical action substitutability rises
- proprietary trajectory and hardware integration value rises
- pure teleoperation value falls

## 1.9 Seesaw invariant checks

Before allocating engineering hours, require answers:

1. **What exact scarcity does this feature own?**
2. **Why can a better model not synthesize it?**
3. **Does usage generate proprietary state/action/outcome data?**
4. **Does the feature become more useful when models improve?**
5. **Can we replace most implementation with open source/API?**
6. **What would make this feature obsolete?**
7. **What observable evidence would falsify the moat thesis?**

If #1 has no good answer, default to `REUSE` or `DROP`.

