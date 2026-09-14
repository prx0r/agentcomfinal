"""Fail-closed grants (qp grants.py shape, ab2 scope).

Allowed constraint keys: max_risk_usd, max_calls, asset. Anything else = deny.
Predicates: {"key": "facts.<dotted>", "op": ==|!=|>|>=|<|<=, "lit": value}.
Unsigned / bad-sig / expired / wrong-capability = deny. No exceptions escape.
"""
from ab1.canonical import canonical, sha12

from . import crypto

ALLOWED_CONSTRAINTS = ("max_risk_usd", "max_calls", "asset")
OPS = ("==", "!=", ">", ">=", "<", "<=")


def grant_body(grant):
    return {k: v for k, v in grant.items() if k not in ("id", "signature")}


def issue(subject_pub_hex, capability, constraints, predicates, expiry,
          secret):
    body = {"subject": subject_pub_hex, "capability": capability,
            "constraints": constraints or {}, "predicates": predicates or [],
            "expiry": expiry}
    gid = "grant:" + sha12(canonical(body))
    sig = crypto.sign_hex(secret, canonical(body))
    return dict([("id", gid), ("signature", sig)] + list(body.items()))


def _resolve(key, facts, action):
    if key == "action":
        return action, True
    if key.startswith("facts."):
        cur, ok = facts, True
        for part in key[len("facts."):].split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None, False
        return cur, True
    return None, False


def _pred_ok(pred, facts, action):
    if not isinstance(pred, dict):
        return False
    if pred.get("op") not in OPS:
        return False
    val, ok = _resolve(pred.get("key", ""), facts, action)
    if not ok:
        return False
    lit = pred.get("lit")
    try:
        if pred["op"] == "==":
            return val == lit
        if pred["op"] == "!=":
            return val != lit
        if pred["op"] == ">":
            return val > lit
        if pred["op"] == ">=":
            return val >= lit
        if pred["op"] == "<":
            return val < lit
        return val <= lit
    except TypeError:
        return False


def verify_grant(grant, action, facts, now_iso):
    """Returns (ok, reason). Never raises."""
    try:
        if not isinstance(grant, dict):
            return False, "bad-shape"
        for f in ("subject", "capability", "expiry", "id", "signature"):
            if f not in grant:
                return False, "missing:%s" % f
        body = grant_body(grant)
        if grant["id"] != "grant:" + sha12(canonical(body)):
            return False, "id-mismatch"
        if not crypto.verify_hex(grant["subject"], canonical(body),
                                 grant["signature"]):
            return False, "bad-signature"
        if not (isinstance(grant["subject"], str)
                and len(grant["subject"]) == 64):
            return False, "bad-subject"
        if grant["expiry"] < now_iso:
            return False, "expired"
        if grant["capability"] != action:
            return False, "capability-mismatch"
        cons = body.get("constraints", {})
        if not isinstance(cons, dict):
            return False, "bad-constraints"
        for k in cons:
            if k not in ALLOWED_CONSTRAINTS:
                return False, "unknown-constraint:%s" % k
        facts = facts or {}
        if "max_risk_usd" in cons:
            try:
                if float(facts.get("amount_usd", 0)) > float(
                        cons["max_risk_usd"]):
                    return False, "over-risk-limit"
            except (TypeError, ValueError):
                return False, "bad-amount"
        if "max_calls" in cons:
            try:
                if int(facts.get("calls_made", 0)) + 1 > int(cons["max_calls"]):
                    return False, "over-calls-limit"
            except (TypeError, ValueError):
                return False, "bad-calls"
        if "asset" in cons and facts.get("asset") != cons["asset"]:
            return False, "asset-mismatch"
        for p in body.get("predicates", []):
            if not _pred_ok(p, facts, action):
                return False, "predicate-false"
        return True, "ok"
    except Exception:  # noqa: BLE001 - fail closed
        return False, "raised"
