"""Tournament lanes (Seed0 method, local runner): freeze the ContractRoot,
run N candidate execution policies as isolated lanes against the same
gates, rank gates-first then cost. Winner + failure corpus banked; lessons
stay proposals (learn.propose), never auto-applied.

Policy registry: policy.direct, policy.seeker3 (= agentloop seeker),
policy.gitgoblin_first, policy.test_first, policy.redteam_first,
policy.repair_first, policy.replace_component. Lanes receive callables so
real policies and test fakes share one runner.
"""
from core import ids


def run_lane(name, fn, contract):
    """fn(contract) -> {gates_pass: bool, cost: {usd, wall_ms, tokens},
    actuality: TRUE|FALSE|UNKNOWN, detail}. Never raises (lane errors are
    results: gates_pass False)."""
    try:
        out = fn(contract) or {}
    except Exception as exc:  # noqa: BLE001
        return {"lane": name, "gates_pass": False, "cost": {},
                "actuality": "UNKNOWN", "detail": "raised:%s"
                % type(exc).__name__}
    return {"lane": name, "gates_pass": bool(out.get("gates_pass")),
            "cost": out.get("cost", {}),
            "actuality": out.get("actuality", "UNKNOWN"),
            "detail": out.get("detail", "")}


def tournament(contract_root, lanes):
    """lanes: [(name, fn)]. Returns {contract_root, ranking, winner,
    failures}. Correctness lexicographic before cost (devplan §9)."""
    ran = [run_lane(n, fn, {"contract_root": contract_root}) for n, fn in lanes]
    ok = [r for r in ran if r["gates_pass"] and r["actuality"] == "TRUE"]
    def cost_key(r):
        c = r.get("cost", {})
        return (c.get("usd", 0) or 0, c.get("wall_ms", 0) or 0,
                c.get("tokens", 0) or 0, r["lane"])
    ranking = sorted(ok, key=cost_key) + sorted(
        [r for r in ran if r not in ok],
        key=lambda r: (r["lane"]))
    out = {"contract_root": contract_root,
           "ranking": [(r["lane"], r["gates_pass"]) for r in ranking],
           "winner": ranking[0]["lane"] if ranking and ranking[0]["gates_pass"]
           else None,
           "failures": [{"lane": r["lane"], "detail": r["detail"]}
                        for r in ranking if not r["gates_pass"]]}
    out["tournament_id"] = ids.obj_id("tournament", {
        "contract_root": contract_root,
        "lanes": sorted(n for n, _ in lanes)})
    return out
