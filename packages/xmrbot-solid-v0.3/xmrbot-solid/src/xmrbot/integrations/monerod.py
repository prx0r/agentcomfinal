from __future__ import annotations
from datetime import datetime, timezone
import httpx
from xmrbot.config import settings
from xmrbot.core.types import NetworkSnapshot


class MoneroRPCError(RuntimeError):
    pass


class MoneroRPCClient:
    def __init__(self, base_url: str | None = None, client: httpx.AsyncClient | None = None):
        self.base_url = (base_url or settings.monerod_url).rstrip("/")
        self._client = client

    async def _json_rpc(self, method: str, params: dict | None = None) -> dict:
        payload = {"jsonrpc": "2.0", "id": "0", "method": method}
        if params is not None:
            payload["params"] = params
        if self._client:
            response = await self._client.post(f"{self.base_url}/json_rpc", json=payload)
        else:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(f"{self.base_url}/json_rpc", json=payload)
        response.raise_for_status()
        body = response.json()
        if "error" in body:
            raise MoneroRPCError(str(body["error"]))
        return body["result"]

    async def get_info(self) -> dict:
        return await self._json_rpc("get_info")

    async def get_last_block_header(self) -> dict:
        return await self._json_rpc("get_last_block_header")

    async def get_fee_estimate(self) -> dict:
        return await self._json_rpc("get_fee_estimate")

    async def get_transaction_pool_stats(self) -> dict:
        try:
            if self._client:
                r = await self._client.get(f"{self.base_url}/get_transaction_pool_stats")
            else:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    r = await client.get(f"{self.base_url}/get_transaction_pool_stats")
            r.raise_for_status()
            return r.json()
        except Exception:
            return {}

    async def snapshot(self, *, xmr_usd: float | None = None) -> NetworkSnapshot:
        info = await self.get_info()
        header = await self.get_last_block_header()
        fee = await self.get_fee_estimate()
        pool = await self.get_transaction_pool_stats()
        block = header.get("block_header", {})
        difficulty = float(info.get("difficulty", 0) or block.get("difficulty", 0))
        target = settings.block_target_seconds
        if difficulty <= 0:
            raise MoneroRPCError("daemon returned non-positive difficulty")
        network_hashrate = difficulty / target
        reward_atomic = int(block.get("reward", int(settings.block_reward_xmr * 1e12)))
        reward_xmr = reward_atomic / 1e12
        pool_stats = pool.get("pool_stats", pool)
        return NetworkSnapshot(
            timestamp=datetime.now(timezone.utc),
            height=int(info.get("height", block.get("height", 0))),
            difficulty=difficulty,
            target_seconds=target,
            estimated_hashrate_hs=network_hashrate,
            reward_xmr=reward_xmr,
            xmr_usd=xmr_usd or settings.xmr_usd,
            mempool_transactions=int(pool_stats.get("txs_total", 0) or 0),
            fee_per_byte_atomic=int(fee.get("fee", 0) or 0),
            source="monerod-rpc",
            confidence=0.98,
        )
