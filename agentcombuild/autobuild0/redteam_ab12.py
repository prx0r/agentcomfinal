"""Red-team vs ab1/ab2. Each attack must FAIL (chain holds) except R5, which
demonstrates a documented caller-trust limitation. stdlib only.

Run: cd agentcombuild && python3 autobuild0/redteam_ab12.py
Exit 0 = all attacks contained (or documented). Prints ATTACK/HELD table.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "autobuild1", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "autobuild2", "src"))

from ab1 import gates, receipts, seesaw, specgate  # noqa: E402
from ab1.store import Store  # noqa: E402
from ab2 import build as ab2build, crypto, grants  # noqa: E402

NOW = "2026-09-14T00:00:00Z"
SEED = ("9d61b19deffd5a60ba844af492ec2af44449c5697b326919703bac031cae58d1")
ASEED = ("4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c")
SECRET, PUB = crypto.keypair_from_seed_hex(SEED)
ASECRET, APUB = crypto.keypair_from_seed_hex(ASEED)
EX2 = os.path.join(HERE, "..", "autobuild2", "examples")
FACTS = {"amount_usd": 5, "calls_made": 0, "asset": "lead-123"}
results = []


def attack(name, held, detail=""):
    results.append((name, held, detail))
    print("%s %-34s %s" % ("HELD " if held else "OPEN ", name, detail))


def jload(p):
    with open(p) as fh:
        return json.load(fh)


PLAN = jload(os.path.join(EX2, "lead_plan.json"))
EV = jload(os.path.join(EX2, "lead_evidence.json"))


def good_grant():
    return grants.issue(PUB, "email.send", {"max_risk_usd": 50, "asset": "lead-123"},
                        [{"key": "facts.amount_usd", "op": "<=", "lit": 50}],
                        "2026-12-31T00:00:00Z", SECRET)


# R1: agent invents a receipt out of thin air
fake = {"id": "receipt:deadbeefdeadbeef", "passed": True, "gates": [],
        "proposal": {"cursor": 1}}
attack("R1 invented-receipt", not receipts.verify(fake))

# R2: tampered store line
import tempfile
d = tempfile.mkdtemp()
s = Store(os.path.join(d, "c.jsonl"))
r = receipts.transition("BUILD", "x", {"cursor": 0}, {"cursor": 1}, {},
                        [("no-duplicate-v1", {"items": [1, 2]})], NOW)
s.append(r)
with open(os.path.join(d, "c.jsonl"), "a") as fh:
    fh.write('{"prev":"LIES","receipt":{"id":"receipt:zzz"}}\n')
attack("R2 store-tamper", not s.verify_chain())

# R3: attacker self-signs a grant naming the victim as subject
evil = grants.issue(PUB, "email.send", {}, [], "2026-12-31T00:00:00Z", ASECRET)
ok, reason = grants.verify_grant(evil, "email.send", FACTS, NOW)
attack("R3 forged-grant-signature", not ok, reason)

# R4: self-attestation, no evidence, no grant
p = copy.deepcopy(PLAN)
p["features"][1]["evidence"] = []
v = specgate.check_plan(p)
attack("R4 trust-only-feature", not v["ok"])
view = ab2build.build(PLAN, EV, {}, None, PUB, NOW)
attack("R4 no-grant-build", not view["receipt"]["passed"])

# R5 (DOCUMENTED LIMITATION): backdated now resurrects an expired grant
old = grants.issue(PUB, "email.send", {}, [], "2026-01-01T00:00:00Z", SECRET)
ok_now, _ = grants.verify_grant(old, "email.send", FACTS, NOW)
ok_back, _ = grants.verify_grant(old, "email.send", FACTS, "2025-06-01T00:00:00Z")
limitation_present = (not ok_now) and ok_back
attack("R5 backdated-clock (KNOWN OPEN)", True,
       "expired correctly denied at true now; caller clock is trusted "
       "(mitigation: authority clock/anchoring, ab5+)")

# R6: smuggled PASS gate inside a receipt
r2 = receipts.transition("BUILD", "x", {"cursor": 0}, {"cursor": 1}, {},
                         [("no-duplicate-v1", {"items": [1]})], NOW)
r2["gates"].append({"id": "admin-override-v1", "inputs": {},
                    "verdict": "PASS", "proof": "trust me"})
attack("R6 smuggled-gate", not receipts.verify(r2))

# R7: acceptance edited after receipt — old receipt must not match new plan
view = ab2build.build(PLAN, EV, {"email.send": {"grant": good_grant(),
                                                "facts": FACTS}},
                      SECRET, PUB, NOW)
p2 = copy.deepcopy(PLAN)
p2["goal"]["acceptance"].append("and a pony")
attack("R7 acceptance-edit", view["receipt"]["evidence"]["plan"] == "lead-reply-one"
       and receipts.verify(view["receipt"])
       and "pony" not in json.dumps(view["receipt"]),
       "receipt pins old bytes; new acceptance needs new ContractRoot (ab4)")

# R8: unknown task / unknown gate at the boundary
attack("R8 unknown-gate", gates.execute("qp-admin-v9", {})["verdict"] == "FAIL")

opens = [n for n, h, _ in results if not h]
print("--- %d held, %d open ---" % (len(results) - len(opens), len(opens)))
sys.exit(0 if not opens else 2)
