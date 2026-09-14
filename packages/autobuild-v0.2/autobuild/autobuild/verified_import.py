"""Trust-boundary object for importing knowledge from an authoritative verifier.

Autobuild cannot declare external knowledge verified. Until a concrete adapter
executes the authoritative verifier (normally /qp) and binds its canonical
receipt, this module emits only a PENDING verification request.
"""
from .canonical import digest, content_id


def make_verification_import_request(observation, claimed_receipt_ref=None):
    body={
        "observation_root":digest(observation),
        "claimed_receipt_ref":claimed_receipt_ref,
    }
    return {
        "record_type":"VERIFICATION_IMPORT_REQUEST",
        "id":content_id("verify-request",body),
        "epistemic_status":"PENDING_EXTERNAL_VERIFICATION",
        "observation":observation,
        "observation_root":body["observation_root"],
        "claimed_receipt_ref":claimed_receipt_ref,
        "required_verifier":"QP_OR_EXPLICIT_AUTHORITATIVE_ADAPTER",
        "note":"This object is not verified knowledge and must never satisfy a VERIFIED gate.",
    }


def make_verified_record(*args, **kwargs):
    raise RuntimeError(
        "autobuild cannot mint VERIFIED knowledge; use make_verification_import_request "
        "and let the authoritative /qp adapter verify and emit the canonical verified receipt"
    )
