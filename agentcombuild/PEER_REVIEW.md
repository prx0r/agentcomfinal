# PEER_REVIEW.md — adversarial self-review of ab1/ab2 (2026-09-14)

Method: re-read every module critically, ran full suites, attacked the chain
(see REDTEAM.md). Findings below with dispositions. Nothing promotes with an
open FAIL.

## Findings fixed

- **P1 (grant fail-open: amount-unknown).** `verify_grant` treated missing
  `facts.amount_usd` as 0, so a spend cap could pass with unknown spend.
  Fix: `max_risk_usd` set + amount absent → deny `amount-unknown`.
  Regression test: `test_grant_amount_unknown_denied`. (ab2, 15/15)
- **P2 (unscoped consequential bypass).** `consequential: true` without a
  `capability` silently skipped the grant gate — authority assumed instead
  of refused. Fix: such features surface as `UNSCOPED:<id>` actions that can
  never hold a grant → REFUSED. Regression test: `test_unscoped_consequential_refused`.
- **P3 (signature broke receipt id).** First ab2 cut signed the receipt id,
  then mutated the body — verification could never pass. Fix per qp law:
  signer/signature ride OUTSIDE the hashed body (`OUTSIDE_BODY` in ab1
  receipts, no-op for V0). ab1 suite still 17/17.
- **P4 (review false positive).** `no-qp-fabrication` grep matched the word
  "qp" in the vendored file's provenance header. Fix: reviewkit skips
  `*vendored*` files (vendoring with provenance is policy, not violation).

## Accepted design (not bugs)

- **A1.** `secret=None` skips signing. Caller-as-authority pattern from qp
  (kernel never signs); GO/demo always sign. Documented in SPEC.
- **A2.** `now` is caller-supplied. Kernel has no clock by law; backdating
  resurrects expired grants (REDTEAM R5). Mitigation: authority clock /
  anchoring, ab5+. Recorded, not hidden.
- **A3.** Grants bind capability+constraints, not asset→owner identity. No
  authority registry exists yet; caller's job (ab5+). An attacker with their
  own valid grant authorizes their own scope — correct behavior.
- **A4.** Chain verifies linkage, not receipt truth; receipts verify
  separately. Matches qp (Store.verify_chain vs settle). Callers run both.
- **A5.** Seesaw magnitudes illustrative, orderings asserted. Scores rank;
  they don't prove. Documented in SPEC.

## Debt carried (→ NEXT files)

C2 full 7-root lineage (ab4) · W5 outcome/readback (ab5) · H2 knowledge
contribution (ab5) · T1 live QP adapter (ab3) · coverage indices (ab3).

## Full suite results (this review)

| suite | result |
|---|---|
| agentcombuild GO.sh (ab1+ab2 suites+reviews+demos) | 6/6 green |
| packages autobuild-v0.2 pytest | 34 passed |
| packages scarce-state-control-plane-v3 unittest | 32 passed OK |
| packages seesaw-agent-module pytest | 3 passed |
| redteam_ab12.py | 9 held, 0 open |
