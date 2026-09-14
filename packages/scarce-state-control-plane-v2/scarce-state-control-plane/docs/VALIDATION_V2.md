# Validation v2 — claims are not proof

V1 incorrectly allowed a self-reported event with `source=live` and `ok=true` to reach `PROVEN`.

V2 separates claims from independently attested evidence.

Evidence classes, weakest to strongest:

```text
fixture
replay
artifact_hash
local_active_probe
external_sandbox_probe
external_readback
signed_third_party_receipt
real_economic_outcome
```

A live checkpoint declares `minimum_evidence_class`. `attested_event` requires an attestation produced outside the worker trust boundary. The stdlib prototype verifies HMAC-SHA256 using `CCP_ATTESTATION_KEY`; production should prefer QP public-key TransitionReceipts and keep signing authority inaccessible to workers.

A raw event such as:

```json
{"source":"live","ok":true}
```

is only an untrusted claim.

Fixtures can still return PASS to test validator semantics, but their proof state remains `VALIDATOR_PASS_FIXTURE_ONLY`.
