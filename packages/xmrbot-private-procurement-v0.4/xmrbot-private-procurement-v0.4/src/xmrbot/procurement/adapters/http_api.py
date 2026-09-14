from __future__ import annotations
import os
from urllib.parse import urlencode
import httpx
from .base import ProviderAdapter
from xmrbot.procurement.models import IntegrationMode, ProviderResult


class KYCnotAdapter(ProviderAdapter):
    async def invoke(self, action, payload):
        if action != "service_get": raise KeyError(action)
        key = os.getenv("KYCNOT_API_KEY")
        if not key: raise RuntimeError("KYCNOT_API_KEY is required for live KYCnot API calls")
        client = self.http or httpx.AsyncClient(timeout=20)
        own = self.http is None
        try:
            r = await client.request("QUERY", "https://kycnot.me/api/v1/service/get", headers={"Authorization":f"Bearer {key}"}, json=payload)
            r.raise_for_status()
            data = r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data, source="https://kycnot.me/docs/api", mode=IntegrationMode.NATIVE_API, live=True)


class OrbitSwapAdapter(ProviderAdapter):
    base = "https://orbitswap.io/api/v2"
    async def invoke(self, action, payload):
        client = self.http or httpx.AsyncClient(timeout=20)
        own = self.http is None
        try:
            if action == "rate":
                r = await client.get(self.base + "/rate", params=payload)
            elif action == "currencies":
                r = await client.get(self.base + "/currencies", params=payload)
            elif action == "create_transaction":
                key = os.getenv("ORBITSWAP_API_KEY")
                if not key: raise RuntimeError("ORBITSWAP_API_KEY required")
                r = await client.post(self.base + "/transactions", headers={"X-API-Key":key}, json=payload)
            elif action == "transaction_status":
                key = os.getenv("ORBITSWAP_API_KEY")
                if not key: raise RuntimeError("ORBITSWAP_API_KEY required")
                r = await client.get(self.base + f"/transactions/{payload['id']}", headers={"X-API-Key":key})
            else: raise KeyError(action)
            r.raise_for_status(); data = r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data, source="https://orbitswap.io/api-docs", mode=IntegrationMode.NATIVE_API, live=True)


class OneGweiAdapter(ProviderAdapter):
    base = "https://1gwei.dev"
    async def invoke(self, action, payload):
        client = self.http or httpx.AsyncClient(timeout=20); own = self.http is None
        try:
            if action == "quote": r = await client.get(self.base + "/api/quote", params=payload)
            elif action == "create_order": r = await client.post(self.base + "/api/orders", json=payload)
            elif action == "order_status": r = await client.get(self.base + f"/api/orders/{payload['id']}")
            else: raise KeyError(action)
            r.raise_for_status(); data = r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data, source="https://1gwei.dev/guides/agent-api-scripted-gas-top-ups", mode=IntegrationMode.NATIVE_API, live=True)


class TrocadorAnonPayAdapter(ProviderAdapter):
    base = "https://trocador.app/anonpay/"
    async def invoke(self, action, payload):
        client = self.http or httpx.AsyncClient(timeout=20); own = self.http is None
        try:
            if action == "create_invoice":
                params = dict(payload); params["direct"] = "False"
                r = await client.get(self.base, params=params)
            elif action == "status":
                r = await client.get("https://trocador.app/anonpay/status/" + payload["id"])
            else: raise KeyError(action)
            r.raise_for_status(); data = r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data, source="https://trocador.app/anonpaydocumentation", mode=IntegrationMode.NATIVE_API, live=True)


class XMRCheckoutAdapter(ProviderAdapter):
    async def invoke(self, action, payload):
        base = os.getenv("XMRCHECKOUT_URL", "http://127.0.0.1:8080").rstrip("/")
        token = os.getenv("XMRCHECKOUT_API_KEY")
        if not token: raise RuntimeError("XMRCHECKOUT_API_KEY required")
        client = self.http or httpx.AsyncClient(timeout=20); own = self.http is None
        headers={"Authorization": f"token {token}"}
        try:
            if action == "server_info": r = await client.get(base+"/api/v1/server/info", headers=headers)
            elif action == "list_webhooks": r = await client.get(base+f"/api/v1/stores/{payload['store_id']}/webhooks", headers=headers)
            else: raise KeyError(action)
            r.raise_for_status(); data=r.json()
        finally:
            if own: await client.aclose()
        return ProviderResult(provider_id=self.descriptor.id, action=action, data=data, source="https://xmrcheckout.com/docs", mode=IntegrationMode.LOCAL_API, live=True)
