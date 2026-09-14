"""agentcom CLI: one command that builds one thing. Exit 0 PASS, 2 FAIL."""
import argparse
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

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
    else:
        print("winner: %s" % report.get("winner"))
        print("dir: %s" % report.get("dir"))
    print("ok: %s" % report.get("ok"))
    return 0 if report.get("ok") else 2


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agentcom")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("spec")
    p.add_argument("--out", default=None)
    p.set_defaults(fn=cmd_build)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
