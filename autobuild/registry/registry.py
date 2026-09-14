"""Validator registry (PROMOTED to canonical 2026-09-14).

Provenance: loader semantics promoted from ab3 registry (frozen); manifests
live here now (registry.json — no cross-tree data dependency). Primitives
declare REQUIRES/PROVIDES/PROBE/JUDGE/COST/FAILURE/VERSION. Agents compose;
they never redefine.
"""
import json
import os

from autobuild.actuality import judges

_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "registry.json")


def load(path=None):
    with open(path or _DEFAULT, encoding="utf-8") as fh:
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
    return judges.judge_evidence(evidence, primitive.get("judge", {}))


def compose(provides_list, path=None):
    plan, missing = {}, []
    for claim in provides_list:
        found = find(provides=claim, path=path)
        if found:
            plan[claim] = [p["id"] for p in found]
        else:
            missing.append(claim)
    return plan, missing
