"""Actuality judges L0/L1: promoted from ab3 (frozen). Pure, total,
three-valued. See agentcombuild/autobuild3/src/ab3/judges.py (canonical)."""
from ab3 import judges as _j

TRUE, FALSE, UNKNOWN = _j.TRUE, _j.FALSE, _j.UNKNOWN


def check_shape(evidence, schema):
    return _j.check_shape(evidence, schema)


def eval_cel(expression, evidence):
    return _j.eval_cel(expression, evidence)


def judge_evidence(evidence, spec):
    return _j.judge_evidence(evidence, spec)
