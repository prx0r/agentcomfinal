
# Deterministic validation design

A good checkpoint asks: **what evidence would be hard to produce unless the user-visible behavior actually worked?**

Prefer, in descending strength:
1. External active probe against a deployed endpoint or provider object.
2. Provider-returned immutable ID plus follow-up read-back.
3. Browser/runtime event tied to an exact state cursor and artifact hash.
4. Local integration test against real dependencies.
5. Unit test / file presence (implementation evidence only).

Every validator states exactly what passing implies and, equally important, what it does *not* imply. A listing-created receipt proves marketplace acceptance of that listing; it does not prove conversion. A browser AR load proves rendering on the tested device; it does not prove every device works.

The validator IR should remain small: `event_match`, `artifact_exists`, `json_predicate`, `http_probe`, `provider_readback`, `all_of`, `any_of`, `threshold`. WASM compilation is an implementation detail; semantics must be identical to the reference runtime.
