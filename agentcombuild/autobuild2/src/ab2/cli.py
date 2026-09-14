"""ab2 CLI. JSON to stdout; exit 0 pass, 2 fail/refuse."""
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
from ab2 import build as ab2build  # noqa: E402
from ab2 import crypto, grants  # noqa: E402

DEFAULT_NOW = "2026-09-14T00:00:00Z"
DEMO_SEED_FILE = os.path.normpath(os.path.join(HERE, "..", "..", "examples",
                                               "demo_seed.hex"))


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def demo_seed():
    p = DEMO_SEED_FILE
    if not os.path.exists(p):
        p = os.path.join(os.getcwd(), "examples", "demo_seed.hex")
    with open(p) as fh:
        return fh.read().strip().split()[-1]  # last token; header lines allowed


def cmd_keygen(_args):
    import secrets as _s
    seed = _s.token_bytes(32)
    print(canonical({"pubkey": crypto.keypair_from_seed_hex(
        seed.hex())[1]}).decode())
    print("SAVE seed from env; this printout carries pubkey only.",
          file=sys.stderr)


def cmd_issue_grant(args):
    seed_hex = args.seed or demo_seed()
    secret, pub = crypto.keypair_from_seed_hex(seed_hex)
    g = grants.issue(args.subject or pub, args.capability,
                     json.loads(args.constraints or "{}"),
                     json.loads(args.predicates or "[]"),
                     args.expiry, secret)
    print(canonical(g).decode())


def _ex_dir():
    base = os.path.normpath(os.path.join(HERE, "..", "..", "examples"))
    if os.path.exists(os.path.join(base, "lead_plan.json")):
        return base
    return os.path.join(os.getcwd(), "examples")


def cmd_build(args):
    ex = _ex_dir()
    plan = load(args.plan or os.path.join(ex, "lead_plan.json"))
    ev = load(args.evidence or os.path.join(ex, "lead_evidence.json"))
    seed_hex = args.seed or demo_seed()
    secret, pub = crypto.keypair_from_seed_hex(seed_hex)
    gmap = {}
    if args.grant and args.facts:
        gmap = {args.capability: {"grant": load(args.grant),
                                  "facts": load(args.facts)}}
    view = ab2build.build(plan, ev, gmap,
                          None if args.unsigned else secret, pub,
                          args.now, args.min)
    print(canonical(view).decode())
    return 0 if view["receipt"]["passed"] else 2


def cmd_verify(args):
    r = load(args.receipt)
    print("true" if ab2build.verify_signed(r, args.pubkey) else "false")
    return 0 if ab2build.verify_signed(r, args.pubkey) else 2


def cmd_demo(_args):
    import tempfile
    ex = _ex_dir()
    seed_hex = demo_seed()
    secret, pub = crypto.keypair_from_seed_hex(seed_hex)
    plan = load(os.path.join(ex, "lead_plan.json"))
    ev = load(os.path.join(ex, "lead_evidence.json"))
    facts = {"amount_usd": 5, "calls_made": 0, "asset": "lead-123"}
    g = grants.issue(pub, "email.send", {"max_risk_usd": 50, "asset": "lead-123"},
                     [{"key": "facts.amount_usd", "op": "<=", "lit": 50}],
                     "2026-12-31T00:00:00Z", secret)
    view = ab2build.build(plan, ev, {"email.send": {"grant": g, "facts": facts}},
                          secret, pub, DEFAULT_NOW, 0.0)
    assert ab2build.verify_signed(view["receipt"], pub), "demo must verify"
    print(canonical(view).decode())
    with tempfile.NamedTemporaryFile("w", suffix=".json",
                                     delete=False) as fh:
        fh.write(canonical(view["receipt"]).decode())
        sys.stderr.write("demo receipt: %s\n" % fh.name)
    return 0 if view["receipt"]["passed"] else 2


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ab2")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("keygen"); p.set_defaults(fn=cmd_keygen)
    p = sub.add_parser("issue-grant"); p.add_argument("--seed", default=None)
    p.add_argument("--subject", default=None); p.add_argument("--capability", required=True)
    p.add_argument("--constraints", default="{}"); p.add_argument("--predicates", default="[]")
    p.add_argument("--expiry", required=True); p.set_defaults(fn=cmd_issue_grant)
    p = sub.add_parser("build"); p.add_argument("--plan", default=None)
    p.add_argument("--evidence", default=None); p.add_argument("--grant", default=None)
    p.add_argument("--facts", default=None); p.add_argument("--capability", default="email.send")
    p.add_argument("--seed", default=None); p.add_argument("--min", type=float, default=0.0)
    p.add_argument("--now", default=DEFAULT_NOW); p.add_argument("--unsigned", action="store_true")
    p.set_defaults(fn=cmd_build)
    p = sub.add_parser("verify"); p.add_argument("receipt"); p.add_argument("pubkey")
    p.set_defaults(fn=cmd_verify)
    p = sub.add_parser("demo"); p.set_defaults(fn=cmd_demo)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
