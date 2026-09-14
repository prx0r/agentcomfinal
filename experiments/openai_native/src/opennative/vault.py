"""Secrets split (brief: Vault + QP gateway). Two credential classes:

VAULT-eligible: read-only, low-consequence, revocable without loss
  (maps lookup, public data APIs, transcript reads).
QP-GATEWAY-only: anything that mutates, moves value, or asserts identity
  (send email, payments, marketplace writes, accounting mutations).

The agent never sees raw QP-gateway credentials: it calls company.* tools
and the gateway enforces grant+scope+readback itself. Pure classifier.
"""


def classify(name, capability):
    """capability: {kind: read|write, moves_value: bool, asserts_identity:
    bool, revocable: bool}. Returns VAULT|QP_GATEWAY|UNCLASSIFIED + reason.
    Unknown goes to UNCLASSIFIED (refuse), never VAULT: an unclassified
    credential must not become a Vault credential."""
    capability = capability or {}
    if capability.get("kind") not in ("read", "write"):
        return "UNCLASSIFIED", "unknown-or-missing-kind"
    if capability.get("moves_value") or capability.get("asserts_identity"):
        return "QP_GATEWAY", "value-or-identity"
    if capability.get("kind") == "write":
        return "QP_GATEWAY", "mutation"
    return "VAULT", "read-only-low-consequence"


def check_examples():
    """The brief's own examples, as law."""
    cases = {
        "maps-lookup": ({"kind": "read"}, "VAULT"),
        "company-data-api": ({"kind": "read"}, "VAULT"),
        "send-email": ({"kind": "write"}, "QP_GATEWAY"),
        "payment": ({"kind": "write", "moves_value": True}, "QP_GATEWAY"),
        "marketplace-write": ({"kind": "write"}, "QP_GATEWAY"),
        "accounting-mutation": ({"kind": "write", "moves_value": True},
                                "QP_GATEWAY"),
    }
    return {k: classify(k, cap) for k, (cap, _) in cases.items()}
