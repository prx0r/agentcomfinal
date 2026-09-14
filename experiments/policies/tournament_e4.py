"""E4: first Seed0 Autobuild tournament (SIMULATED lanes, REAL gates).

Hard leaf: reliably prove provider send + independent readback. Frozen
ContractRoot; three policy lanes face identical Actuality gates evaluated
by the canonical DAG evaluator (ab3, frozen) — nothing asserted, everything
judged. Winner + failure corpus banked; failures feed real
seed0.learn.propose. A fourth rogue lane with a different contract is
disqualified (same-ContractRoot rule).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
for _d in ("", "agentcombuild/autobuild3/src", "agentcombuild/agentloop/src"):
    _p = os.path.join(ROOT, _d) if _d else ROOT
    if _p not in sys.path:
        sys.path.insert(0, _p)

from autobuild.actuality import dag as _dag  # noqa: E402
from autobuild.compiler import actuality_compile as _ac  # noqa: E402
from experiments.policies import lanes as _lanes  # noqa: E402
from trajectory import trajectory as _traj  # noqa: E402

LEAF_SEND = {"id": "outbound-sent",
             "evidence": {"status": 202},
             "judge": {"engine": "cel", "expression": "e.status == 202"}}
LEAF_READBACK = {"id": "readback-agrees",
                 "evidence": {"created_id": "lead-123",
                              "found_id": "lead-123"},
                 "judge": {"engine": "cel",
                           "expression": "e.found_id == e.created_id"}}

CONTRACT = _ac.compile_contract(
    "reliably prove provider send + independent readback",
    [{"id": "outbound-sent", "probe": "company.send_email",
      "evidence_schema": {"type": "object"}, "judge": LEAF_SEND["judge"],
      "freshness_s": 600, "evidence_class": "direct", "authority": "grant"},
     {"id": "readback-agrees", "probe": "provider.readback",
      "evidence_schema": {"type": "object"}, "judge": LEAF_READBACK["judge"],
      "freshness_s": 300, "evidence_class": "external_readback",
      "authority": "none"}],
    plan_ref="e4-lanes")
CONTRACT_ROOT = CONTRACT["contract_root"]


def _judge_send_only():
    return _dag.evaluate_dag({"claim": CONTRACT["claim"], "leaves": [
        dict(LEAF_SEND), {"id": "readback-agrees", "evidence": {},
                          "judge": LEAF_READBACK["judge"]}]})


def _judge_full():
    return _dag.evaluate_dag({"claim": CONTRACT["claim"], "leaves": [
        dict(LEAF_SEND), dict(LEAF_READBACK)]})


def lane_direct(contract):
    """Straight at the requirement, no independent check."""
    v = _judge_send_only()
    return {"gates_pass": v["value"] == "TRUE",
            "cost": {"usd": 0.01, "wall_ms": 100, "tokens": 50},
            "actuality": v["value"], "detail": "send-only, no readback",
            "contract_root": CONTRACT_ROOT}


def lane_seeker3(contract):
    """Fail once, research, retry with readback (policy.seeker3 shape)."""
    first = _judge_send_only()
    assert first["value"] != "TRUE"  # the failure that teaches
    v = _judge_full()
    return {"gates_pass": v["value"] == "TRUE",
            "cost": {"usd": 0.05, "wall_ms": 500, "tokens": 400},
            "actuality": v["value"], "detail": "retry-with-readback",
            "contract_root": CONTRACT_ROOT}


def lane_gitgoblin_first(contract):
    """Archaeology first (finds readback primitive), then one clean attempt."""
    from adapters import gitgoblin as _gg
    found = _gg.search_local("readback receipt independent")
    v = _judge_full()
    return {"gates_pass": v["value"] == "TRUE",
            "cost": {"usd": 0.02, "wall_ms": 200, "tokens": 100},
            "actuality": v["value"],
            "detail": "prebuild-hit:%d" % len(found),
            "contract_root": CONTRACT_ROOT}


def lane_rogue(contract):
    """Wrong contract — must be disqualified, never judged."""
    return {"gates_pass": True, "cost": {"usd": 0.0, "wall_ms": 1,
                                        "tokens": 1},
            "actuality": "TRUE", "detail": "claims other contract",
            "contract_root": "contract:rogue"}


LANES = [("direct", lane_direct), ("seeker3", lane_seeker3),
         ("gitgoblin-first", lane_gitgoblin_first), ("rogue", lane_rogue)]


def run(out_path=None):
    """Run the tournament. Same ContractRoot enforced per lane; trajectories
    banked; failures -> seed0 candidate lessons. Returns full results."""
    from adapters import seed0 as _seed
    admitted, disqualified = [], []
    for name, fn in LANES:
        try:
            probe = fn({"contract_root": CONTRACT_ROOT})
        except Exception as exc:  # noqa: BLE001
            probe = {"gates_pass": False, "detail": "raised:%s"
                     % type(exc).__name__}
        if probe.get("contract_root") != CONTRACT_ROOT:
            disqualified.append({"lane": name, "reason": "contract-mismatch"})
            continue
        admitted.append((name, fn))
    t = _lanes.tournament(CONTRACT_ROOT, admitted)
    trajs = {}
    for name, fn in admitted:
        out = fn({"contract_root": CONTRACT_ROOT})
        trajs[name] = _traj.build(
            CONTRACT_ROOT, "plan:e4-" + name, "policy." + name.replace("-", ""),
            [{"lane": name, "detail": out.get("detail")}],
            {"readback": "UNKNOWN"}, {"readback": out.get("actuality")},
            cost={"tokens": out.get("cost", {}).get("tokens"),
                  "wall_ms": out.get("cost", {}).get("wall_ms"),
                  "usd": out.get("cost", {}).get("usd"), "human_minutes": 0})
    fails = [{"seed": r["lane"], "sig": r["detail"], "round": 1}
             for r in [dict(_lanes.run_lane(n, fn, {"contract_root": CONTRACT_ROOT}))
                       for n, fn in admitted]
             if not r["gates_pass"]]
    fails += [{"seed": d["lane"], "sig": d["reason"], "round": 1}
              for d in disqualified]
    lessons = _seed.candidate_lessons(fails) if fails else {"proposals": []}
    results = {"contract_root": CONTRACT_ROOT, "tournament": t,
               "disqualified": disqualified, "trajectories": trajs,
               "lessons": lessons, "mode": "SIMULATED"}
    if out_path:
        import json as _json
        with open(out_path, "w") as fh:
            _json.dump(results, fh, indent=2)
    return results


if __name__ == "__main__":
    import json as _json
    out = run(os.path.join(_HERE, "e4_results.json"))
    print(_json.dumps({"winner": out["tournament"]["winner"],
                       "ranking": out["tournament"]["ranking"],
                       "mode": out["mode"]}, indent=2))
