"""Compiler spec gate: ab1 plan validation + ab3 covers mapping.

Promoted from ab1.specgate (plan/acceptance/declared-evidence) and
ab3.alog.check_covers (feature→goal index map). One entry point for
'approved intent may enter compilation'. Seesaw scoring is separate and
advisory only (devplan §3: scores are priorities, never proof — the old
score-threshold-v1 hard gate is deliberately NOT promoted).
"""
from ab1 import specgate as _ab1
from ab3 import alog as _alog


def check_plan(plan):
    v = _ab1.check_plan(plan)
    c = _alog.check_covers(plan)
    errors = list(v.get("errors", [])) + list(c.get("errors", []))
    return {"ok": not errors, "errors": errors}


def check_plugin(spec):
    return _ab1.check_plugin(spec)
