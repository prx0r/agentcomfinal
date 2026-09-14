"""ab3 CLI. JSON to stdout; exit 0 GO/pass, 2 NOGO/fail."""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AB1_SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..",
                                         "autobuild1", "src"))
for _p in (os.path.dirname(os.path.dirname(HERE)), AB1_SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ab1.canonical import canonical  # noqa: E402
from ab3 import alog, stoplight  # noqa: E402
from ab3 import gates3  # noqa: E402,E401  (registers ab3 gates)

DEFAULT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "demo3"))


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def ctx(args):
    d = args.dir or DEFAULT_DIR
    qpath = os.path.join(d, "queue.json")
    vdir = os.path.join(d, "validators")
    if os.path.exists(qpath):
        queue = alog.queue_from_plan(load(qpath))
    else:
        queue = {}  # unknown-task refusals, never a traceback
    return d, queue, vdir if os.path.isdir(vdir) else None, qpath


def cmd_log(args):
    d, queue, _, _ = ctx(args)
    try:
        line = alog.append(d, queue, args.task,
                           json.loads(args.idx), args.action,
                           json.loads(args.evidence))
    except alog.Refused as exc:
        print(canonical({"refused": str(exc)}).decode())
        return 2
    print(canonical(line).decode())
    return 0


def cmd_judge(args):
    d, queue, vdir, qpath = ctx(args)
    v = stoplight.judge(args.task, queue, d, vdir, qpath)
    print(canonical(v).decode())
    return 0 if v["verdict"] == "GO" else 2


def cmd_acheck(args):
    d, queue, vdir, qpath = ctx(args)
    out = stoplight.acheck(queue, d, vdir, qpath,
                           stale_hours=args.stale_hours)
    print(canonical(out).decode())
    bad = [t for t, s in out.items() if s["status"] in ("NOGO", "STALE")]
    return 2 if bad else 0


def cmd_demo(_args):
    import shutil
    import tempfile
    from ab3 import demo_worker  # noqa: E402
    d = tempfile.mkdtemp(prefix="ab3demo")
    try:
        v = demo_worker.honest(d)
        print(canonical(v).decode())
        return 0 if v["verdict"] == "GO" else 2
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ab3")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("log"); p.add_argument("--dir", default=None)
    p.add_argument("--task", required=True); p.add_argument("--idx", default="[0]")
    p.add_argument("--action", default=""); p.add_argument("--evidence", required=True)
    p.set_defaults(fn=cmd_log)
    p = sub.add_parser("judge"); p.add_argument("--dir", default=None)
    p.add_argument("--task", required=True); p.set_defaults(fn=cmd_judge)
    p = sub.add_parser("acheck"); p.add_argument("--dir", default=None)
    p.add_argument("--stale-hours", type=float, default=24); p.set_defaults(fn=cmd_acheck)
    p = sub.add_parser("demo"); p.set_defaults(fn=cmd_demo)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
