"""Contracts are law: all 5 schemas enforced, real objects validated."""
import os
import sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
sys.path.insert(0, ROOT)

from contracts.check import check  # noqa: E402


def test_all_schemas_reject_garbage():
    for kind in ("strategic", "campaign", "actuality", "trajectory",
                 "promotion"):
        ok, _ = check(kind, {"nope": True})
        assert not ok, kind
        ok, _ = check(kind, "not-an-object")
        assert not ok, kind
    ok, _ = check("nonexistent", {})
    assert not ok


def test_strategic_and_campaign():
    ok, r = check("strategic", {"decision_id": "d", "project": "p",
                                "thesis": "t", "first_moat_event": "m"})
    assert ok, r
    ok, _ = check("campaign", {"campaign_id": "c", "project": "p",
                               "scarce_asset": "s", "objective": "o",
                               "world": "BOGUS"})
    assert not ok  # enum enforced
    ok, r = check("campaign", {"campaign_id": "c", "project": "p",
                               "scarce_asset": "s", "objective": "o",
                               "world": "C_ECONOMIC"})
    assert ok, r


def test_actuality_contract_shape():
    good = {"contract_id": "c", "claim": "x",
            "leaves": [{"id": "l", "probe": {}, "evidence_schema": {},
                        "judge": {"engine": "cel"}}]}
    ok, r = check("actuality", good)
    assert ok, r
    bad = {"contract_id": "c", "claim": "x",
           "leaves": [{"id": "l", "probe": {}}]}
    ok, _ = check("actuality", bad)
    assert not ok


def test_real_trajectory_validates():
    from trajectory import trajectory as _t
    t = _t.build("cr", "pr", "policy.seeker3", [{"a": 1}], {"x": "U"},
                 {"x": "T"}, cost={"tokens": 1, "wall_ms": 2, "usd": 0.01,
                                   "human_minutes": 0})
    ok, r = check("trajectory", t)
    assert ok, r


def test_promotion_contract():
    ok, _ = check("promotion", {"subject": "s", "kind": "nope",
                                "evidence": [], "replay": {},
                                "approver": "h"})
    assert not ok  # kind enum enforced
    ok, r = check("promotion", {"subject": "s", "kind": "policy",
                                "evidence": [], "replay": {},
                                "approver": "h"})
    assert ok, r
