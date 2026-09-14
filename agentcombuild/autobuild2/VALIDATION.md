# ab2 VALIDATION

Scope: criteria G1, G2, G5, T1-simulated + ab1 no-regression.

| criterion | test |
|---|---|
| G1 consequential w/o grant REFUSED | `test_consequential_without_grant_refused` |
| G2 wrong-scope grant REFUSED | `test_wrong_scope_refused` |
| G5 signed receipts, tamper fails | `test_signed_build_verifies`, `test_tamper_sig_fails`, `test_roundtrip` |
| grant fail-closed matrix | expired / unknown-constraint / over-limit / predicate-false / unsigned |
| T1 simulated | `test_no_receipt_no_advance_shape` (no PASS receipt ⇒ state unchanged, ab1 base) |
| ab1 no-regression | `test_ab1_still_green` (breadup plan still builds PASS unsigned path intact) + `review/check.py` runs ab1 suite |

Manual: `PYTHONPATH=../autobuild1/src:src python3 -m ab2.cli demo` →
signed BUILD receipt `passed=true`, `ab2 verify` true.
