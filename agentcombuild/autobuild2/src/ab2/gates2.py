"""L1 authority gates, registered into the ab1 registry (new ids, per law)."""
from ab1 import gates, receipts

from . import crypto, grants


def _grant_valid(inputs):
    g = inputs.get("grant", {})
    ok, reason = grants.verify_grant(g, inputs.get("action", ""),
                                     inputs.get("facts", {}),
                                     inputs.get("now", ""))
    return ok, reason


def _grant_scope(inputs):
    # scope == valid grant for exactly this action+facts (alias with proof)
    ok, reason = grants.verify_grant(inputs.get("grant", {}),
                                     inputs.get("action", ""),
                                     inputs.get("facts", {}),
                                     inputs.get("now", ""))
    return ok, ("in-scope" if ok else reason)


def _consequential(inputs):
    needed = inputs.get("actions", [])
    by_cap = inputs.get("grants", {})
    if not needed:
        return True, "no-consequential-actions"
    for action in needed:
        entry = by_cap.get(action, {})
        ok, reason = grants.verify_grant(entry.get("grant", {}), action,
                                         entry.get("facts", {}),
                                         inputs.get("now", ""))
        if not ok:
            return False, "REFUSED:%s:%s" % (action, reason)
    return True, "all-granted"


def _receipt_signed(inputs):
    r = inputs.get("receipt", {})
    pub = inputs.get("pubkey", "")
    if not receipts.verify(r):
        return False, "receipt-invalid"
    sig = r.get("signature", "")
    if not sig or not r.get("signer") == pub:
        return False, "missing-signature"
    ok = crypto.verify_hex(pub, r["id"].encode("utf-8"), sig)
    return ok, ("signed-ok" if ok else "bad-signature")


gates.register("grant-valid-v1", "grant sig+expiry+shape", _grant_valid)
gates.register("grant-scope-v1", "capability+constraints+predicates",
               _grant_scope)
gates.register("consequential-requires-grant-v1",
               "every consequential action holds a valid grant",
               _consequential)
gates.register("receipt-signed-v1", "id recomputes AND ed25519 verifies",
               _receipt_signed)
