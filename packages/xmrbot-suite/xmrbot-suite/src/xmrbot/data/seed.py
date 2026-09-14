from __future__ import annotations
from datetime import datetime, timezone
from xmrbot.config import settings
from xmrbot.core.types import NetworkSnapshot
from xmrbot.data.repository import Repository


def ensure_seed(repo: Repository) -> NetworkSnapshot:
    existing = repo.latest_network()
    if existing:
        return existing
    # A deterministic offline bootstrap, clearly labeled as a seed rather than live chain data.
    snap = NetworkSnapshot(
        timestamp=datetime.now(timezone.utc),
        height=0,
        difficulty=settings.network_hashrate_hs * settings.block_target_seconds,
        target_seconds=settings.block_target_seconds,
        estimated_hashrate_hs=settings.network_hashrate_hs,
        reward_xmr=settings.block_reward_xmr,
        xmr_usd=settings.xmr_usd,
        source="offline-seed-config",
        confidence=0.25,
    )
    repo.add_network(snap)
    return snap
