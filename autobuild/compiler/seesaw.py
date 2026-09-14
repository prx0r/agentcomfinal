"""Seesaw strategy: ranking → proposal → accepted StrategicDecision.

Promoted from ab1.seesaw scoring. DEMOTION (devplan §3): scores are
priorities, not truth. This module never emits PASS/FAIL over a score;
it emits a ranked proposal citing components. Acceptance (by scheduler /
human) mints the StrategicDecision. score-threshold-v1 is retired.
"""
from ab1 import seesaw as _ab1


def rank(features):
    """Returns {scores, value, binding, ranking} — advisory ordering."""
    return _ab1.score_project(features)


def propose(project, features, scores=None):
    """Strategic proposal (not proof): cites score components + moat event."""
    scores = scores or rank(features)
    by_id = {s["id"]: s for s in scores["scores"]}
    binding = scores["binding"]
    moat_event = ("first-moat:%s" % binding) if binding else "no-moat"
    return {"project": project, "ranking": scores["ranking"],
            "binding": binding, "value": scores["value"],
            "first_moat_event": moat_event,
            "cites": {i: {"S": s["S"], "action": s["action"]}
                      for i, s in by_id.items()},
            "status": "PROPOSED"}


def ai_exposure(demand_effect, destruction_effect):
    return _ab1.ai_exposure(demand_effect, destruction_effect)
