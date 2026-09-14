"""agentcom CLI: one command that builds one thing. Exit 0 PASS, 2 FAIL."""
import argparse
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agentcom import actuality as _actuality
from agentcom import build as _build


def cmd_build(args):
    try:
        report = _build.build(args.spec, args.out)
    except (ValueError, OSError) as exc:
        print("agentcom build REFUSED: %s" % exc)
        return 2
    print("product: %s" % report.get("product", report.get("id", "?")))
    if report.get("kind") == "product":
        dag = report.get("dag", {})
        print("Actuality: %d TRUE / %d UNKNOWN / %d FALSE" % (
            dag.get("true", 0), dag.get("unknown", 0), dag.get("false", 0)))
        print("QP receipts: %s" % report.get("qp_receipts", "n/a (read-only)"))
        print("Artifact: %s" % report.get("dist", "?"))
        print("latency_ms: %s" % report.get("latency_ms", "?"))
        print("status: %s" % report.get("status", "?"))
    else:
        print("winner: %s" % report.get("winner"))
        print("dir: %s" % report.get("dir"))
    print("ok: %s" % report.get("ok"))
    # P7: default succeeds only on full proof. LOCAL_PASS (UNKNOWNs remain)
    # exits 3 (incomplete) unless --stage local explicitly accepts it.
    if report.get("kind") == "product":
        if report.get("status") == "PRODUCT_PROVEN":
            return 0
        if report.get("ok") and args.stage == "local":
            return 0
        return 3 if report.get("ok") else 2
    return 0 if report.get("ok") else 2


def cmd_actuality(args):
    proj = _actuality.evaluate(args.repo or None)
    print("contract: %s  subject: %s" % (
        proj["contract"], (proj["subject_sha"] or "")[:12]))
    for lid in ["exact-candidate", "validator-frozen",
                "baseline-fails-candidate-passes", "cg-real-run",
                "openai-real-session", "mcp-roundtrip-same-session",
                "github-ci-exact-sha", "no-promotion-on-failure",
                "fixture-boundary", "host-leaves-unknown"]:
        r = proj["results"].get(lid, {})
        print("  %-32s %-7s %s" % (lid, r.get("value", "?"),
                                   r.get("detail", "")[:70]))
    a = proj["actuality"]
    print("actuality: %d TRUE / %d FALSE / %d UNKNOWN" % (
        a["TRUE"], a["FALSE"], a["UNKNOWN"]))
    print("blocking: %s" % ", ".join(proj["blocking"]))
    print("next blocker: %s" % proj["next_blocker"])
    print("receipts: %d  state: %s" % (len(proj["receipts"]), proj["state"]))
    if args.json:
        print(json.dumps(proj, indent=2, sort_keys=True))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agentcom")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("spec")
    p.add_argument("--out", default=None)
    p.add_argument("--stage", default="auto", choices=("auto", "local"),
                   help="auto: exit 0 only on full proof (default); "
                        "local: accept LOCAL_PASS with exit 0")
    p.set_defaults(fn=cmd_build)
    p = sub.add_parser("actuality")
    p.add_argument("--repo", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_actuality)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
