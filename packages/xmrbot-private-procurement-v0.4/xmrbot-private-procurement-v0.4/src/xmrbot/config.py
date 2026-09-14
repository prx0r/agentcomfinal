from __future__ import annotations
from dataclasses import dataclass
import os


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    db_path: str = os.getenv("XMRBOT_DB_PATH", "./xmrbot.db")
    xmr_usd: float = float(os.getenv("XMRBOT_XMR_USD", "500"))
    monerod_url: str = os.getenv("XMRBOT_MONEROD_URL", "http://127.0.0.1:18081")
    monerod_enabled: bool = _bool("XMRBOT_MONEROD_ENABLED", False)
    network_hashrate_hs: float = float(os.getenv("XMRBOT_NETWORK_HASHRATE_HS", "5900000000"))
    block_reward_xmr: float = float(os.getenv("XMRBOT_BLOCK_REWARD_XMR", "0.6"))
    block_target_seconds: float = float(os.getenv("XMRBOT_BLOCK_TARGET_SECONDS", "120"))
    canonical_url: str = os.getenv("XMRBOT_CANONICAL_URL", "https://xmrbot.com").rstrip("/")
    editor_token: str = os.getenv("XMRBOT_EDITOR_TOKEN", "")
    youtube_channel_url: str = os.getenv("XMRBOT_YOUTUBE_CHANNEL_URL", "")


settings = Settings()
