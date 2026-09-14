"""Canonical archive isolation (gitbuild1 §C): AST-based, not grep.

FAILs if canonical/openai-native production code OR its tests import the
frozen historical trees (agentcombuild/autobuild1|2|3, ab1|ab2|ab3) or put
them back on sys.path. Historical tests under agentcombuild/ are exempt
(they test the frozen code itself). New code references canonical paths
(autobuild/, core/, adapters/) or real externals (~/qp) instead.
"""
import ast
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))
CANONICAL = ("autobuild", "core", "adapters", "experiments", "trajectory",
             "contracts")
FORBIDDEN_MODS = ("ab1", "ab2", "ab3")
FORBIDDEN_PREFIX = "agentcombuild.autobuild"


def _violations(path):
    with open(path, encoding="utf-8") as fh:
        try:
            tree = ast.parse(fh.read())
        except SyntaxError as exc:
            return ["syntax-error:%s" % exc]
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in FORBIDDEN_MODS or \
                    node.module.startswith(FORBIDDEN_PREFIX):
                hits.append("import-from:%s" % node.module)
        elif isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                if root in FORBIDDEN_MODS or \
                        a.name.startswith(FORBIDDEN_PREFIX):
                    hits.append("import:%s" % a.name)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("insert", "append"):
            func = node.func
            if isinstance(func.value, ast.Name) and func.value.id == "sys":
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str) \
                            and ("autobuild1" in arg.value
                                 or "autobuild2" in arg.value
                                 or "autobuild3" in arg.value):
                        hits.append("sys.path:%s" % arg.value)
    return hits


def test_canonical_archive_isolation():
    bad = {}
    for top in CANONICAL:
        base = os.path.join(ROOT, top)
        if not os.path.isdir(base):
            continue
        for dirpath, _, files in os.walk(base):
            for fn in sorted(files):
                if not fn.endswith(".py"):
                    continue
                full = os.path.join(dirpath, fn)
                hits = _violations(full)
                if hits:
                    bad[os.path.relpath(full, ROOT)] = hits
    assert not bad, "canonical imports frozen history: %s" % bad
