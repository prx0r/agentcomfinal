from pydantic import BaseModel, Field


class PrivacyProfile(BaseModel):
    tor_enabled: bool = True
    socks_proxy: str = "socks5://127.0.0.1:9050"
    expose_wallet_address_to_markets: bool = False
    allow_direct_network: bool = False


class Policy(BaseModel):
    minimum_net_xmr_hour: float = 0.0
    allowed_markets: set[str] = Field(default_factory=lambda: {"randomx", "mock-compute"})
    allow_untrusted_jobs: bool = False
    privacy: PrivacyProfile = Field(default_factory=PrivacyProfile)
