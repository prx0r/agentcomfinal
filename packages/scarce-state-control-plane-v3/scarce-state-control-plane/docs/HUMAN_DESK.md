# Strategic H-task Desk

The desired end state is not "human supervises every agent". It is:

```text
agents search / build / test / monitor / iterate continuously
                         ↓
only irreducible bottlenecks become H-tasks
                         ↓
human desk answers bounded strategic questions or performs inaccessible actions
```

## Allowed H-task classes

- `strategic_direction` — competing objectives/tradeoffs remain after evidence/ranking.
- `physical_access` — hands/device/presence/postage/photography/etc.
- `identity_kyc` — OTP, account owner, KYC, legal identity.
- `spend_approval` — QP policy requires authorization for consequential spend.
- `relationship_trust` — customer/partner negotiation or trust-building.
- `taste_value_judgement` — a genuine owner preference that cannot be discovered by testing.

## Forbidden escalation pattern

Do not ask the human:
- to debug code the agent can execute;
- to inspect logs available to tools;
- broad unbounded "what should I do?" questions;
- questions caused only by low model confidence when a test can resolve them.

## Queue ordering

The local prototype uses:

```text
attention_value_per_minute = blocking_value / estimated_minutes
```

This is a coarse ordering heuristic only.

An H-task answer records a bounded decision. It does not itself execute an external action; QP remains the authority boundary.
