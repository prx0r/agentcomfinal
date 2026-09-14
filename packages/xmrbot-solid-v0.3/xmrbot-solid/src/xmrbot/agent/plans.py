from __future__ import annotations


def node_plan(*, tor: bool = True, prune: bool = False, public_rpc: bool = False) -> dict:
    flags = ["--non-interactive"]
    if prune:
        flags.append("--prune-blockchain")
    if not public_rpc:
        flags += ["--rpc-restricted-bind-ip", "127.0.0.1"]
    return {
        "risk_class": "R1-local-change",
        "requires_user_approval": True,
        "steps": [
            "Download official Monero CLI release and verify published checksums/signatures.",
            "Store blockchain in an explicitly selected data directory.",
            "Bind RPC to localhost by default; do not expose unrestricted RPC publicly.",
            "Start monerod and wait for synchronization.",
            "Verify local height against independent peers/sources.",
        ] + (["Route appropriate outbound traffic through Tor using an explicit proxy configuration."] if tor else []),
        "recommended_flags": flags,
        "tor": tor,
        "prune": prune,
        "public_rpc": public_rpc,
    }


def wallet_plan(*, hardware_wallet: bool = False) -> dict:
    return {
        "risk_class": "R2-sensitive-financial",
        "requires_user_approval": True,
        "cloud_receives_seed": False,
        "disabled_actions": ["export_seed", "export_private_spend_key"],
        "steps": [
            "Create the wallet locally using official wallet software or a supported hardware wallet.",
            "Encrypt wallet files and keep RPC bound to localhost.",
            "Display backup material only on the local device; never send it to XMRBot cloud services.",
            "Verify receive address locally before accepting funds.",
        ],
        "hardware_wallet": hardware_wallet,
    }
