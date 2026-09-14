"""Seesaw scorer: where is the binding constraint, what to do per feature.

S = (E * X * F * N * T * beta) / cost. Missing moat keys default 1 (neutral),
cost defaults 1. Magnitudes illustrative; ORDERINGS asserted (qp rule).
Invariant: software-substitutable with hard-moat <= 1 is never OWN.
"""

ACTIONS = ("OWN", "BUILD", "BUY", "REUSE", "VALIDATE", "WATCH", "DROP")
MOAT_KEYS = ("exclusivity", "externality", "feedback", "network", "trust",
             "ai_beta")


def score_feature(f):
    moat = f.get("moat", {}) if isinstance(f.get("moat", {}), dict) else {}
    vals = [float(moat.get(k, 1)) for k in MOAT_KEYS]
    cost = f.get("cost", 1)
    try:
        cost = float(cost) or 1.0
    except (TypeError, ValueError):
        cost = 1.0
    s = vals[0] * vals[1] * vals[2] * vals[3] * vals[4] * vals[5] / cost
    hard = max(vals[0], vals[1], vals[3], vals[4])
    subst = bool(f.get("software_substitutable", True))
    if subst and hard <= 1:
        action = "REUSE" if s >= 1 else "DROP"
    elif s >= 200 and hard >= 3:
        action = "OWN"
    elif s >= 60:
        action = "BUILD"
    elif s >= 20:
        action = "BUY"
    elif s >= 6:
        action = "VALIDATE"
    elif s >= 2:
        action = "WATCH"
    else:
        action = "DROP"
    return {"id": f.get("id"), "S": round(s, 4), "action": action}


def score_project(features):
    scored = [score_feature(f) for f in features]
    ranking = sorted([s["id"] for s in scored],
                     key=lambda i: next(x["S"] for x in scored
                                        if x["id"] == i),
                     reverse=True)
    value = round(sum(s["S"] for s in scored), 4)
    return {"scores": scored, "value": value,
            "binding": ranking[0] if ranking else None, "ranking": ranking}


def ai_exposure(demand_effect, destruction_effect):
    """Which way does AI move the constraint? qp seesaw/graph.py shape."""
    d = float(demand_effect) - float(destruction_effect)
    if d > 0:
        return "TIGHTENS"
    if d < 0:
        return "RELAXES"
    return "NEUTRAL"
