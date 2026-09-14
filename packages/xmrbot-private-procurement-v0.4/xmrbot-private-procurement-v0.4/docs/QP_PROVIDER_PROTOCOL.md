# QP provider protocol

The provider layer is designed to slot beneath `qp`/A-COM's typed state, evidence, gates, grants and receipts.

## Canonical objects

- `ProviderDescriptor`: asserted capabilities and source evidence.
- `ProviderAction`: exact provider/action/payload; canonical SHA-256 hash.
- `ActionProposal`: non-executing intent object.
- `QPGrant`: approved flag, budget, allowed provider/actions, exact payload hash and expiry.
- `GateResult`: deterministic check ledger.
- `ActionReceipt`: integrity receipt binding action hash to normalized provider response hash.

An `ActionReceipt` is **not** a ZK proof and is not represented as one. Future `proof_type` adapters can attach TEE attestations, zkVM proofs or external signatures while preserving the receipt envelope.

## Capability classes

`discover`, `quote`, `propose`, `execute`, `status`, `verify`.

## Integration modes

`native_api`, `local_api`, `read_only_web`, `manual_bridge`, `upcoming_api`.

An adapter may only claim the mode supported by current provider documentation. This is intentionally stricter than browser automation.
