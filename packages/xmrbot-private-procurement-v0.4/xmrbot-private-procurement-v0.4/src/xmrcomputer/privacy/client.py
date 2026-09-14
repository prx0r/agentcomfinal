import httpx
from xmrcomputer.models.settings import PrivacyProfile


def build_http_client(profile: PrivacyProfile) -> httpx.AsyncClient:
    # httpx supports SOCKS when installed with httpx[socks].
    proxy = profile.socks_proxy if profile.tor_enabled else None
    return httpx.AsyncClient(proxy=proxy, timeout=20.0, headers={"User-Agent": "xmr.computer/0.1"})
