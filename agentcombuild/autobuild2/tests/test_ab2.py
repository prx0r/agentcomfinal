"""ab2 proof suite: G1/G2/G5 + fail-closed matrix + ab1 no-regression."""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "autobuild1", "src")))

from ab1 import gates as ab1gates  # noqa: E402
from ab2 import build as ab2build  # noqa: E402
from ab2 import crypto, grants  # noqa: E402

NOW = "2026-09-14T00:00:00Z"
FUTURE = "2026-12-31T00:00:00Z"
EX = os.path.join(HERE, "..", "examples")
SEED = open(os.path.join(EX, "demo_seed.hex")).read().strip().split()[-1]
SECRET, PUB = crypto.keypair_from_seed_hex(SEED)
FACTS = {"amount_usd": 5, "calls_made": 0, "asset": "lead-123"}


def good_grant(**kw):
    args = {"capability": "email.send",
            "constraints": {"max_risk_usd": 50, "asset": "lead-123"},
            "predicates": [{"key": "facts.amount_usd", "op": "<=",
                            "lit": 50}],
            "expiry": FUTURE}
    args.update(kw)
    return grants.issue(PUB, args["capability"], args["constraints"],
                        args["predicates"], args["expiry"], SECRET)


def plan():
    with open(os.path.join(EX, "lead_plan.json")) as fh:
        return json.load(fh)


def ev():
    with open(os.path.join(EX, "lead_evidence.json")) as fh:
        return json.load(fh)


def test_roundtrip():
    assert crypto.verify_hex(PUB, b"hello", crypto.sign_hex(SECRET, b"hello"))
    assert not crypto.verify_hex(PUB, b"hello!",
                                 crypto.sign_hex(SECRET, b"hello"))


def test_grant_valid():
    ok, reason = grants.verify_grant(good_grant(), "email.send", FACTS, NOW)
    assert ok, reason


def test_grant_expired():
    g = good_grant(expiry="2026-01-01T00:00:00Z")
    ok, reason = grants.verify_grant(g, "email.send", FACTS, NOW)
    assert not ok and reason == "expired"


def test_grant_wrong_capability():
    ok, reason = grants.verify_grant(good_grant(), "marketplace.purchase",
                                     FACTS, NOW)
    assert not ok and reason == "capability-mismatch"


def test_grant_unknown_constraint():
    g = good_grant(constraints={"teleport": 1})
    ok, reason = grants.verify_grant(g, "email.send", FACTS, NOW)
    assert not ok and reason.startswith("unknown-constraint")


def test_grant_over_limit():
    big = dict(FACTS, amount_usd=500)
    ok, reason = grants.verify_grant(good_grant(), "email.send", big, NOW)
    assert not ok and reason == "over-risk-limit"


def test_grant_predicate_false():
    big = dict(FACTS, amount_usd=51)
    ok, reason = grants.verify_grant(good_grant(), "email.send", big, NOW)
    assert not ok and reason in ("over-risk-limit", "predicate-false")


def test_grant_unsigned():
    g = good_grant()
    del g["signature"]
    ok, _ = grants.verify_grant(g, "email.send", FACTS, NOW)
    assert not ok


def test_consequential_without_grant_refused():
    view = ab2build.build(plan(), ev(), {}, None, PUB, NOW)
    assert not view["receipt"]["passed"]
    proofs = " ".join(g["proof"] for g in view["receipt"]["gates"])
    assert "REFUSED" in proofs


def test_wrong_scope_refused():
    g = good_grant(capability="email.send")
    view = ab2build.build(plan(), ev(),
                          {"marketplace.purchase": {"grant": g, "facts": FACTS}},
                          SECRET, PUB, NOW)
    assert not view["receipt"]["passed"]


def test_signed_build_verifies():
    g = good_grant()
    view = ab2build.build(plan(), ev(),
                          {"email.send": {"grant": g, "facts": FACTS}},
                          SECRET, PUB, NOW)
    r = view["receipt"]
    assert r["passed"] and r["proof_level"] == "V1-signed"
    assert ab2build.verify_signed(r, PUB)


def test_tamper_sig_fails():
    g = good_grant()
    view = ab2build.build(plan(), ev(),
                          {"email.send": {"grant": g, "facts": FACTS}},
                          SECRET, PUB, NOW)
    r = dict(view["receipt"])
    r["signature"] = "00" * 64
    assert not ab2build.verify_signed(r, PUB)


def test_ab1_still_green():
    sys.path.insert(0, os.path.normpath(os.path.join(
        HERE, "..", "..", "autobuild1", "src")))
    from ab1 import receipts, seesaw, specgate  # noqa: E402
    import json as _j
    base = os.path.normpath(os.path.join(HERE, "..", "..", "autobuild1",
                                         "examples"))
    p = _j.load(open(os.path.join(base, "breadup_plan.json")))
    assert specgate.check_plan(p)["ok"]
    assert seesaw.score_project(p["features"])["binding"] == \
        "photo-valuation-crosslist"
