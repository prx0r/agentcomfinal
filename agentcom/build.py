"""agentcom build orchestrator (brief P3): boring wiring, no strategy.

Dispatches spec kind: product -> build_product, selfhost -> frozen-contract
validation run banked as experiment artifacts. Strategic intelligence lives
in Seesaw/scheduler, never here. Exit contract: returns report dict with
ok bool; CLI maps to exit codes.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def load_spec(path):
    with open(path) as fh:
        spec = json.load(fh)
    if not isinstance(spec, dict) or not spec.get("kind"):
        raise ValueError("spec needs kind")
    return spec


def build_selfhost(spec, out_root):
    """Run the frozen contract nodes; bank candidates/receipts/tournament/
    promoted under experiments/selfhost/<id>/. Single direct lane this
    cycle; multi-policy tournaments use the same artifact shape next."""
    import shutil
    spec_id = spec.get("id", "selfhost")
    dest = os.path.join(ROOT, spec.get("out", "experiments/selfhost/" + spec_id))
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    t0 = time.monotonic()
    env = dict(os.environ, PYTHONPATH=":".join([
        os.path.join(ROOT, "experiments", "openai_native", "src"),
        os.path.join(ROOT, "agentcombuild", "agentloop", "src"), ROOT]))
    results = []
    ok_all = True
    for node in spec.get("test_nodes", []):
        p = subprocess.run([sys.executable, "-m", "pytest", node, "-q"],
                           capture_output=True, text=True, timeout=300,
                           cwd=ROOT, env=env)
        passed = p.returncode == 0
        ok_all = ok_all and passed
        results.append({"node": node, "passed": passed,
                        "tail": (p.stdout + p.stderr)[-300:]})
    wall_ms = int((time.monotonic() - t0) * 1000)
    candidate = {"policy": spec.get("policy_id", "direct"),
                 "rev": _head_sha(), "contract": spec.get("contract", "")}
    receipt = {"candidate": candidate, "results": results,
               "passed": ok_all, "wall_ms": wall_ms}
    tournament = {"lanes": [candidate["policy"]], "winner": candidate["policy"]
                  if ok_all else None, "failures": [] if ok_all else results}
    promoted = {"state": "PROMOTED" if ok_all else "REFUSED",
                "candidate": candidate,
                "note": "single-lane direct repair; multi-policy next cycle"}
    for name, obj in (("contract.json", spec), ("candidates.json", [candidate]),
                      ("receipts.json", [receipt]),
                      ("tournament.json", tournament),
                      ("promoted.json", promoted)):
        json.dump(obj, open(os.path.join(dest, name), "w"), indent=2)
    return {"kind": "selfhost", "id": spec_id, "ok": ok_all,
            "dir": dest, "winner": tournament["winner"]}


def _head_sha():
    try:
        p = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        return p.stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def build(spec_path, out_root=None):
    """Kind-dispatched build. Returns a JSON-serializable report."""
    spec = load_spec(spec_path)
    kind = spec["kind"]
    if kind == "product":
        from agentcom import build_product
        return dict(build_product.build(
            spec_path, out_root or os.path.join(ROOT, "dist")),
            kind="product")
    if kind == "selfhost":
        return dict(build_selfhost(spec, out_root or ROOT), kind="selfhost")
    raise ValueError("unknown spec kind:%s" % (kind,))
