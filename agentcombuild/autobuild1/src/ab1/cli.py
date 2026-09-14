"""ab1 CLI. JSON to stdout; exit code = verdict (0 pass, 2 fail)."""
import argparse
import json
import os
import sys

try:
    from ab1 import gates, receipts, seesaw, specgate
    from ab1.canonical import canonical
except ImportError:  # direct script run: bootstrap src/ onto path
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    from ab1 import gates, receipts, seesaw, specgate  # noqa: E402
    from ab1.canonical import canonical  # noqa: E402

DEFAULT_NOW = "2026-09-14T00:00:00Z"
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def cmd_score(args):
    plan = load(args.plan)
    print(canonical(seesaw.score_project(plan.get("features", []))).decode())


def cmd_gate(args):
    plan = load(args.plan)
    ev = load(args.evidence)
    verdict = specgate.check_plan(plan)
    calls = [("specgate-v1", {"spec_verdict": verdict}),
             ("evidence-declared-v1", {"features": plan.get("features", [])}),
             ("two-sources-v1", {"sources": ev.get("sources", [])}),
             ("no-duplicate-v1", {"items": [f.get("id") for f in
                                            plan.get("features", [])]})]
    results = [gates.execute(gid, inp) for gid, inp in calls]
    print(canonical({"verdict": verdict, "gates": results}).decode())
    return 0 if verdict["ok"] and all(
        r["verdict"] == "PASS" for r in results) else 2


def cmd_build(args):
    plan = load(args.plan)
    ev = load(args.evidence)
    verdict = specgate.check_plan(plan)
    proj = seesaw.score_project(plan.get("features", []))
    state_before = {"cursor": 0, "projects": {}}
    proposal = {"cursor": 1, "projects": {
        plan.get("id", "plan"): {"status": "SCORED",
                                 "value": proj["value"],
                                 "binding": proj["binding"],
                                 "actions": {s["id"]: s["action"]
                                             for s in proj["scores"]}}}}
    calls = [("specgate-v1", {"spec_verdict": verdict}),
             ("evidence-declared-v1", {"features": plan.get("features", [])}),
             ("two-sources-v1", {"sources": ev.get("sources", [])}),
             ("score-threshold-v1", {"value": proj["value"],
                                     "min": args.min}),
             ("no-duplicate-v1", {"items": [f.get("id") for f in
                                            plan.get("features", [])]})]
    r = receipts.transition("BUILD", plan.get("id", "plan"), state_before,
                            proposal, {"plan": plan.get("id"),
                                       "sources": ev.get("sources", [])},
                            calls, args.now)
    view = {"receipt": r, "scores": proj, "spec": verdict}
    print(canonical(view).decode())
    return 0 if r["passed"] else 2


def cmd_verify(args):
    print("true" if receipts.verify(load(args.receipt)) else "false")
    return 0 if receipts.verify(load(args.receipt)) else 2


def cmd_demo(_args):
    base = os.path.dirname(HERE)
    plan = os.path.join(base, "..", "examples", "breadup_plan.json")
    ev = os.path.join(base, "..", "examples", "breadup_evidence.json")
    if not os.path.exists(plan):  # installed-layout fallback
        plan = os.path.join(os.getcwd(), "examples", "breadup_plan.json")
        ev = os.path.join(os.getcwd(), "examples", "breadup_evidence.json")
    ns = argparse.Namespace(plan=plan, evidence=ev, min=100.0,
                            now=DEFAULT_NOW)
    return cmd_build(ns)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ab1")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("score"); p.add_argument("plan")
    p.set_defaults(fn=cmd_score)
    p = sub.add_parser("gate"); p.add_argument("plan"); p.add_argument("evidence")
    p.set_defaults(fn=cmd_gate)
    p = sub.add_parser("build"); p.add_argument("plan"); p.add_argument("evidence")
    p.add_argument("--min", type=float, default=100.0); p.add_argument("--now", default=DEFAULT_NOW)
    p.set_defaults(fn=cmd_build)
    p = sub.add_parser("verify"); p.add_argument("receipt")
    p.set_defaults(fn=cmd_verify)
    p = sub.add_parser("demo"); p.set_defaults(fn=cmd_demo)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
