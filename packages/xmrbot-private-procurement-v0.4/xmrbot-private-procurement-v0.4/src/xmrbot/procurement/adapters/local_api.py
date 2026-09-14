from __future__ import annotations
import os
import httpx
from .base import ProviderAdapter
from xmrbot.procurement.models import IntegrationMode, ProviderResult


class MoneroWalletRPCAdapter(ProviderAdapter):
    async def invoke(self, action, payload):
        url=os.getenv("MONERO_WALLET_RPC_URL","http://127.0.0.1:18088/json_rpc")
        method_map={"balance":"get_balance","create_address":"create_address","validate_address":"validate_address","transfer":"transfer"}
        method=method_map[action]
        client=self.http or httpx.AsyncClient(timeout=30); own=self.http is None
        try:
            r=await client.post(url,json={"jsonrpc":"2.0","id":"xmrbot","method":method,"params":payload}); r.raise_for_status(); data=r.json()
        finally:
            if own: await client.aclose()
        if "error" in data: raise RuntimeError(str(data["error"]))
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data.get("result",{}), source="https://docs.getmonero.org/rpc-library/wallet-rpc/", mode=IntegrationMode.LOCAL_API, live=True)


class BasicSwapAdapter(ProviderAdapter):
    async def invoke(self, action, payload):
        base=os.getenv("BASICSWAP_URL","http://127.0.0.1:12700").rstrip("/")
        password=os.getenv("BASICSWAP_PASSWORD")
        auth=("",password) if password else None
        client=self.http or httpx.AsyncClient(timeout=30); own=self.http is None
        try:
            if action == "wallets": r=await client.get(base+"/json/wallets",auth=auth)
            else: raise KeyError(action)
            r.raise_for_status(); data=r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data if isinstance(data,dict) else {"items":data}, source="https://docs.basicswapdex.com/docs/user-guides/web-ui-authentication/", mode=IntegrationMode.LOCAL_API, live=True)


class HavenoAdapter(ProviderAdapter):
    async def invoke(self, action, payload):
        # Haveno is gRPC. This Python suite ships a typed local bridge contract rather than embedding generated protobuf stubs.
        # Point XMRBOT_HAVENO_BRIDGE_URL at a thin local bridge or use the generated contract in docs/providers/haveno.md.
        base=os.getenv("XMRBOT_HAVENO_BRIDGE_URL")
        if not base: raise RuntimeError("Haveno requires local havenod + gRPC bridge; set XMRBOT_HAVENO_BRIDGE_URL")
        client=self.http or httpx.AsyncClient(timeout=30); own=self.http is None
        try:
            r=await client.post(base.rstrip("/")+"/invoke",json={"action":action,"payload":payload}); r.raise_for_status(); data=r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data, source="https://docs.haveno.exchange/users/haveno-api/", mode=IntegrationMode.LOCAL_API, live=True)
