"""Canonical bytes + content ids. Deterministic, stdlib only."""
import hashlib
import json


def canonical(obj):
    """Sorted keys, no whitespace, UTF-8. Same object -> same bytes, always."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha12(data: bytes) -> str:
    return sha256_hex(data)[:12]


def obj_id(prefix: str, obj) -> str:
    return prefix + ":" + sha12(canonical(obj))
