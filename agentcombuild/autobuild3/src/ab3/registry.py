"""Validator registry: LEGO primitives (manifests, not code).

Each primitive declares REQUIRES/PROVIDES/PROBE/JUDGE/COST/FAILURE/VERSION.
The agent cannot redefine them; Autobuild composes them. Adapters for
Playwright/Schemathesis/k6/etc. arrive as later primitives with the same
shape (probe.runner names the engine, judge stays structured).
"""
import json
import os

from . import judges

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.normpath(os.path.join(HERE, "..", "..", "validators",
                                         "registry.json"))


def load(path=None):
    with open(path or REGISTRY, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("primitives", [])


def find(provides=None, claim_class=None, path=None):
    out = []
    for p in load(path):
        if provides is not None and provides not in p.get("provides", []):
            continue
        if claim_class is not None and p.get("claim_class") != claim_class:
            continue
        out.append(p)
    return out


def judge_with(primitive, evidence):
    """Evaluate evidence with the primitive's frozen judge spec."""
    return judges.judge_evidence(evidence, primitive.get("judge", {}))


def compose(provides_list, path=None):
    """Map each needed claim to primitives that provide it. Raises nothing:
    returns (plan, missing) where missing lists unmet claims."""
    plan, missing = {}, []
    for claim in provides_list:
        found = find(provides=claim, path=path)
        if found:
            plan[claim] = [p["id"] for p in found]
        else:
            missing.append(claim)
    return plan, missing
