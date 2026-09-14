"""Core proof suite: E0 canonicalization invariants. Stdlib only (adapters
may shell to real CLIs in sandboxes; no network, no spend)."""
import json
import os
import sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "autobuild1", "src"))
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "autobuild3", "src"))
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "agentloop", "src"))

from adapters import atask as A_atask  # noqa: E402
from adapters import gitgoblin as A_gg  # noqa: E402
from adapters import qp as A_qp  # noqa: E402
from adapters import seed0 as A_seed  # noqa: E402
from adapters import seesaw as A_seesaw  # noqa: E402
from autobuild.actuality import dag as ADag  # noqa: E402
from autobuild.actuality import envelope as AEnv  # noqa: E402
from autobuild.actuality import judges as AJ  # noqa: E402
from autobuild.compiler import priority as CPrio  # noqa: E402
from autobuild.compiler import proposals as CProp  # noqa: E402
from autobuild.compiler import seesaw as CSee  # noqa: E402
from autobuild.compiler import specgate as CSpec  # noqa: E402
from autobuild.registry import registry as CReg  # noqa: E402
from core import ids, lineage, portfolio, scheduler  # noqa: E402
from experiments.policies import lanes as Lanes  # noqa: E402
from trajectory import trajectory as Traj  # noqa: E402


def test_ids_full_sha256():
    a = ids.obj_id("x", {"b": 1, "a": [1, 2]})
    assert a.startswith("x:") and len(a) == 66  # prefix + 64 hex, never 16
    assert ids.obj_id("x", {"a": [1, 2], "b": 1}) == a
    assert ids.merkle_root([]) == ids.sha256_hex(b"")


def test_lineage_roundtrip_and_tamper():
    parts = {k: {"v": k} for k in ("strategic", "campaign", "contract", "plan",
                                   "run", "evidence", "outcome")}
    chain = lineage.build_chain(qp_receipt_id="qp:receipt:abc", **parts)
    assert len(chain) == 8
    ok, fails = lineage.verify_chain(chain, parts)
    assert ok, fails
    bad = dict(parts)
    bad["plan"] = {"v": "evil"}
    ok, fails = lineage.verify_chain(chain, bad)
    assert not ok and fails == ["mismatch:plan"]


def test_contract_invariant():
    old = {"contract": "c", "plan": "p1"}
    ok, _ = lineage.contract_invariant(old, {"contract": "c", "plan": "p2"})
    assert ok
    ok, reason = lineage.contract_invariant(old, {"contract": "c2", "plan": "p2"})
    assert not ok and reason == "contract-changed"


def test_scheduler_infra_cannot_outbid():
    camps = [{"id": "infra-cdn", "kind": "infra", "value": 999, "needs_slot": True},
             {"id": "breadup", "kind": "asset", "value": 1, "needs_slot": True}]
    alloc = scheduler.select(camps, ["store-1"])
    assert alloc["allocation"] == {"store-1": "breadup"}
    assert alloc["unallocated"] == ["infra-cdn"]
    alloc2 = scheduler.select(camps, ["store-1", "store-2"])
    assert alloc2["allocation"]["store-2"] == "infra-cdn:support"


def test_portfolio_select_needs_decision():
    camps = {}
    camps = portfolio.register(camps, {"id": "breadup", "kind": "asset"})
    with pytest.raises(portfolio.BadCampaign):
        portfolio.select_next(camps, ["s"], "")
    out = portfolio.select_next(camps, ["s"], "strategic:abc")
    assert out["strategic_ref"] == "strategic:abc" and "selection_id" in out


def good_plan():
    return {"id": "p", "goal": {"statement": "s", "acceptance": ["a", "b"]},
            "features": [{"id": "f1", "description": "d",
                          "acceptance": ["x"],
                          "evidence": [{"kind": "doc", "ref": "r"}],
                          "covers": [0]}]}


def test_specgate_combined():
    assert CSpec.check_plan(good_plan())["ok"]
    bad = good_plan()
    bad["features"][0]["evidence"] = []
    assert not CSpec.check_plan(bad)["ok"]  # trust-only refused
    bad2 = good_plan()
    del bad2["features"][0]["covers"]
    assert not CSpec.check_plan(bad2)["ok"]  # unmapped refused


def test_seesaw_demoted_to_proposal():
    feats = [{"id": "a", "moat": {"exclusivity": 3}, "cost": 1},
             {"id": "b", "cost": 100, "software_substitutable": True}]
    prop = CSee.propose("proj", feats)
    assert prop["status"] == "PROPOSED" and "verdict" not in prop
    assert prop["ranking"][0] == "a"  # ordering kept, proof removed


def test_priority_impact_is_weak():
    full = {"task": "probe", "justification": "j", "expected_progress": 0.8,
            "bottleneck_centrality": 0.8, "information_value": 0.8,
            "strategic_value": 0.8, "cost": 0.2, "human_needed": False,
            "reversibility": 0.9}
    bare = {"task": "hype", "justification": "trust", "impact": 5}
    s_full, _ = CPrio.priority(full)
    s_bare, inputs = CPrio.priority(bare)
    assert inputs["impact_weight"] == 0.2 and s_bare == round(1.0 * 0.2, 6)
    assert s_full > s_bare  # evidence-backed math beats loud enthusiasm
    ranked = CPrio.rank([bare, full])
    assert ranked[0]["task"] == "probe"


def test_proposal_channel():
    p = CProp.propose("do X", "why")
    assert p["binding"] is None and not CProp.is_work_order(p)
    assert CProp.bind(p, "", "sched:1") is None  # no requirement, no bind
    b = CProp.bind(p, "req-1", "sched:1")
    assert b["channel"] == "bound" and CProp.bind(b, "r", "s") is None
    assert CProp.is_work_order({"task_id": "t", "status": "READY"})


def test_envelope_binds_and_drifts(tmp_path):
    env = AEnv.bind_envelope(["echo", "hi"], cwd=str(tmp_path))
    assert env["envelope_id"].startswith("env:")
    assert len(env["envelope_id"]) == 68
    ok, _ = AEnv.verify_envelope(env)
    assert ok
    ok, reason = AEnv.verify_envelope(env, cwd="/")
    assert not ok and reason == "envelope-drift:cwd"
    rc, out = AEnv.run_envelope(env)
    assert rc == 0 and "hi" in out
    with pytest.raises(ValueError):
        AEnv.bind_envelope(["no-such-exe-zzz"])


def test_registry_promoted():
    assert CReg.find(provides="command-ran")
    plan, missing = CReg.compose(["command-ran", "teleport-x"])
    assert "teleport-x" in missing


def test_qp_adapter_real_ids():
    v = A_qp.version()
    assert v["protocol"] == "acom/0.1"
    c = A_qp.make_claim("s?", "d")
    t = A_qp.make_task("build", "x", {"ok": True})
    g = A_qp.make_gate("g1", "wasm", "h" * 64)
    assert c["id"].startswith("claim:") and t["id"].startswith("task:")
    assert g["id"] == "g1"  # qp law: gate ids verbatim
    bound = A_qp.bind_requirement("cr:1", "r1", c, t, g)
    assert bound["qp_claim_id"] == c["id"]


def test_atask_adapter_sandbox(tmp_path):
    sb = str(tmp_path / "work")
    rc, _ = A_atask.init_sandbox(sb)
    assert rc == 0
    rc, _ = A_atask.add_task(sb, "t1", "demo", ["done works"],
                             ["command:echo hi"])
    assert rc == 0
    out = A_atask.run_cycle(sb, "t1", input_tokens=10, output_tokens=5,
                            cost=0.001)
    assert out["run_id"] and out["finish"][0] == 0


def test_seed0_adapter():
    v = A_seed.version()
    assert "policy.seeker3" in v["policies"]
    lessons = A_seed.candidate_lessons(
        [{"seed": "a", "sig": "s1", "round": 1},
         {"seed": "b", "sig": "s1", "round": 1}])
    assert "proposals" in lessons  # real learn.propose, stops at proposed


def test_gitgoblin_adapter_honest_limits(tmp_path):
    v = A_gg.version()
    assert "search_entities" in v["remote_search"]  # entity search only
    cands = A_gg.search_local("lineage scheduler")
    assert cands and cands[0]["path"]
    empty = A_gg.reuse_plan("r", "zzz-no-such-capability-qqq",
                            roots=[str(tmp_path)])
    assert empty["candidates"] == [] and empty["verdict"] == "BUILD"
    assert A_gg.reuse_plan("r", "q", exemption="spike")["verdict"] == "EXEMPT"


def test_seesaw_adapter_decision():
    prop = A_seesaw.propose("proj", [{"id": "a", "cost": 1}])
    dec = A_seesaw.accept(prop)
    assert dec["status"] == "ACCEPTED" and dec["strategic_root"].startswith(
        "strategic:")


def test_lanes_gates_first():
    cheap_fail = lambda c: {"gates_pass": False, "cost": {"usd": 0.01},
                            "actuality": "FALSE"}
    pricey_pass = lambda c: {"gates_pass": True, "cost": {"usd": 9},
                             "actuality": "TRUE"}
    cheap_pass = lambda c: {"gates_pass": True, "cost": {"usd": 0.02},
                            "actuality": "TRUE"}
    out = Lanes.tournament("cr:1", [("pricey", pricey_pass),
                                    ("cheap-fail", cheap_fail),
                                    ("cheap", cheap_pass)])
    assert out["winner"] == "cheap"
    assert len(out["failures"]) == 1
    out2 = Lanes.tournament("cr:1", [("a", cheap_fail)])
    assert out2["winner"] is None


def test_trajectory_ladder():
    t = Traj.build("cr", "pr", "policy.seeker3", [], {}, {},
                   cost={"tokens": 1, "wall_ms": 2, "usd": 0.01,
                         "human_minutes": 0})
    assert t["level"] == "L0-observation" and len(t["trajectory_id"]) > 20
    _, ok, reason = Traj.advance(t)
    assert not ok and reason == "needs:qp_receipt"
    t1, ok, _ = Traj.advance(t, {"qp_receipt": "qp:r:1"})
    t2, ok2, reason2 = Traj.advance(t1, {"runs": ["a"]})
    assert not ok2 and reason2 == "needs-2-runs"
    assert t2 is t1  # refused advance returns same object
    t2b, ok, _ = Traj.advance(t1, {"runs": ["a", "b"]})
    assert ok and t2b["level"] == "L2-pattern"


# ---- boundary red-team (R13-R15) ----

def test_r13_adapter_mints_no_truth():
    """R13: the qp adapter exposes constructors (ids) but NO settlement.
    A fabricated receipt id in a chain is structural only — truth lives in
    QP's settle path, which this adapter must not contain."""
    import adapters.qp as A
    for forbidden in ("settle", "transition", "verify_receipt",
                      "execute_gate"):
        assert not hasattr(A, forbidden), forbidden
    parts = {k: {"v": k} for k in ("strategic", "campaign", "contract",
                                   "plan", "run", "evidence", "outcome")}
    chain = lineage.build_chain(qp_receipt_id="qp:receipt:fabricated",
                                **parts)
    ok, _ = lineage.verify_chain(chain, parts)
    assert ok  # structural only — documented boundary, not a hole:
    # nothing here claims the receipt is real. Only QP settles.


def test_r14_infra_never_bare_slot():
    """R14: bribe the scheduler — infra value 10^9 vs asset value 1."""
    camps = [{"id": "infra-x", "kind": "infra", "value": 10 ** 9,
              "needs_slot": True},
             {"id": "asset-y", "kind": "asset", "value": 1,
              "needs_slot": True}]
    alloc = scheduler.select(camps, ["slot-1", "slot-2"])
    bare = [v for v in alloc["allocation"].values() if ":" not in v]
    assert bare == ["asset-y"]
    assert alloc["allocation"]["slot-2"] == "infra-x:support"


def test_r15_proposal_is_not_work():
    """R15: smuggle a bound proposal into execution — still not a work
    order until A-Task mints it. Binding authorizes scheduling, not work."""
    p = CProp.propose("ship X", "why", expected_delta=3)
    b = CProp.bind(p, "req-9", "sched:1")
    assert not CProp.is_work_order(p) and not CProp.is_work_order(b)
    assert b["binding"]["scheduler_ref"] == "sched:1"


def test_cg_adapter_live():
    from adapters import cg as A_cg
    v = A_cg.version()
    assert v["kernel"] == "cogymkernel" and len(v["rev"]) == 40
    s = A_cg.smoke()
    assert s["status"] == "ok" and s["request_hash"].startswith("req_")
    m = A_cg.lane_to_worldpack("cr:1", "abc123", "policy.seeker3")
    assert m["scenario"]["contract_root"] == "cr:1"
