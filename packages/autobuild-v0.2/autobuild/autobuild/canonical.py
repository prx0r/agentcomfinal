import json, hashlib
from typing import Any

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()

def content_id(prefix: str, value: Any, n: int = 20) -> str:
    return f"{prefix}:" + hashlib.sha256(canonical_bytes(value)).hexdigest()[:n]

def canonical_clone(value: Any) -> Any:
    return json.loads(canonical_bytes(value).decode("utf-8"))
