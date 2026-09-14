"""Actuality DAG: promoted from ab3 (frozen). AND over TRUE/FALSE/UNKNOWN;
UNKNOWN blocks. See agentcombuild/autobuild3/src/ab3/actuality.py."""
from ab3 import actuality as _a


def evaluate_leaf(leaf):
    return _a.evaluate_leaf(leaf)


def evaluate_dag(dag):
    return _a.evaluate_dag(dag)


def actuality_record(claim, value, contract_root, evidence_root,
                     validator_root, environment, observed_at, proof_class):
    return _a.actuality_record(claim, value, contract_root, evidence_root,
                               validator_root, environment, observed_at,
                               proof_class)
