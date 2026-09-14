from __future__ import annotations
from hashlib import sha256
import json, uuid
from .models import ActionReceipt, ProviderAction


def make_receipt(action: ProviderAction, status: str, response: dict, grant_id: str | None = None) -> ActionReceipt:
    response_raw = json.dumps(response, sort_keys=True, separators=(",", ":"), default=str)
    rh = sha256(response_raw.encode()).hexdigest()
    material = f"{action.canonical_hash()}:{rh}:{status}:{grant_id or ''}"
    rid = sha256(material.encode()).hexdigest()
    return ActionReceipt(
        receipt_id=rid,
        provider_id=action.provider_id,
        action=action.action,
        action_hash=action.canonical_hash(),
        grant_id=grant_id,
        status=status,
        response_hash=rh,
        response_summary=response,
    )


def verify_receipt(receipt: ActionReceipt, action: ProviderAction, response: dict) -> dict:
    expected = make_receipt(action, receipt.status, response, receipt.grant_id)
    return {
        "valid": expected.receipt_id == receipt.receipt_id and expected.response_hash == receipt.response_hash,
        "receipt_id": receipt.receipt_id,
        "expected_receipt_id": expected.receipt_id,
    }
