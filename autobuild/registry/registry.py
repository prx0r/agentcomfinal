"""Validator registry: promoted from ab3 (frozen manifests + loader)."""
import os

from ab3 import registry as _r

_DEFAULT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "agentcombuild",
    "autobuild3", "validators", "registry.json"))


def load(path=None):
    return _r.load(path or _DEFAULT)


def find(provides=None, claim_class=None, path=None):
    return _r.find(provides=provides, claim_class=claim_class,
                   path=path or _DEFAULT)


def judge_with(primitive, evidence):
    return _r.judge_with(primitive, evidence)


def compose(provides_list, path=None):
    return _r.compose(provides_list, path=path or _DEFAULT)
