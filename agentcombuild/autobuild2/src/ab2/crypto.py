"""Key + signature wrappers over the vendored Ed25519. Caller holds keys."""
from . import _vendored_ed25519 as ed

PUB_HEX_LEN = 64


def keypair_from_seed_hex(seed_hex):
    """Deterministic demo/test helper. Production callers pass keys in."""
    seed = bytes.fromhex(seed_hex)
    if len(seed) != 32:
        raise ValueError("seed must be 32 bytes hex")
    pub = ed.pubkey(seed)
    return seed, pub.hex()


def sign_hex(secret: bytes, msg: bytes) -> str:
    return ed.sign(secret, msg).hex()


def verify_hex(pub_hex: str, msg: bytes, sig_hex: str) -> bool:
    try:
        pub = bytes.fromhex(pub_hex)
        sig = bytes.fromhex(sig_hex)
    except ValueError:
        return False
    if len(pub) != 32 or len(sig) != 64 or len(pub_hex) != PUB_HEX_LEN:
        return False
    try:
        return bool(ed.verify(pub, msg, sig))
    except Exception:  # noqa: BLE001 - fail closed
        return False


def address(pub_hex: str) -> str:
    import hashlib
    return hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()[:16]
