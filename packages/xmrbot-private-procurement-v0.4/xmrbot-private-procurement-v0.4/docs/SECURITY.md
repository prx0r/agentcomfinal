# Security model

## Non-custodial invariant

Cloud code has no seed/private-key fields and no export methods. This is tested.

## Risk classes

- R0: read-only
- R1: local machine mutation
- R2: sensitive/financial; future implementation must require exact-parameter approval
- disabled: seed/private-key export

## xmrbotd

The local service binds only to loopback by default and rejects arbitrary external bind addresses. It exposes machine inspection, a benchmark estimate and privacy status only in this release.

## Third-party compute

No untrusted workload execution is implemented. Future adapters must enforce sandboxing, resource limits, disposable identities and explicit policy/terms checks.

## Tor

The current build models Tor in privacy/node plans and detects local Tor installation. It does not claim Tor use unless an adapter is explicitly configured to use it.
