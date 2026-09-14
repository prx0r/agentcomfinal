# ab2 SPEC (ab2/0.1) — delta over ab1/0.1

ab1 pipeline unchanged (specgate → seesaw → L0 gates → receipt). ab2 adds:

## Grants

`{subject (64-hex pubkey), capability, constraints{}, predicates[],
expiry (ISO Z), id, signature}`. `id = "grant:"+sha12(canonical(body minus
id/signature))`; signature = Ed25519(canonical(body minus id/signature)).

`verify_grant(grant, action, facts, now_iso)` denies (FAIL-closed) on: bad
shape, id mismatch, bad signature, expired (`expiry < now`, lexicographic
ISO Z), capability mismatch, **unknown constraint key** (allowed:
`max_risk_usd`, `max_calls`, `asset`), `facts.amount_usd > max_risk_usd`,
`facts.calls_made+1 > max_calls`, `facts.asset != asset`, any predicate
false. Predicates: `{key: "facts.<dotted>", op: ==|!=|>|>=|<|<=, lit}`.
Unsigned grant = deny. Keys never persisted by the lib (caller holds them).

## Consequential actions

Plan features may carry `consequential: true` + `capability`. BUILD collects
required capabilities; gate `consequential-requires-grant-v1` passes iff
every one has a valid in-scope grant. Non-consequential plans skip L1.

## Signed receipts

After ab1 settles, `sign(sk, receipt)`: `signature = Ed25519(receipt.id)`,
adds `signer` (pubkey hex) + `proof_level: V1-signed`. `verify_signed`
recomputes id (ab1.verify) AND signature. Tamper either → FAIL.

Demo uses a fixed DEMO-ONLY seed (`examples/demo_seed.hex`, no value) so
`demo` output is byte-deterministic. Real keys live in env/caller memory.
