import json
import httpx
import pytest
from xmrbot.integrations.monerod import MoneroRPCClient

@pytest.mark.asyncio
async def test_monerod_snapshot_parsing():
    async def handler(request):
        if request.url.path == "/json_rpc":
            body=json.loads(request.content)
            method=body["method"]
            data={
                "get_info":{"height":3456789,"difficulty":720000000000},
                "get_last_block_header":{"block_header":{"height":3456788,"reward":600000000000,"difficulty":720000000000}},
                "get_fee_estimate":{"fee":20000},
            }[method]
            return httpx.Response(200,json={"jsonrpc":"2.0","id":"0","result":data})
        if request.url.path == "/get_transaction_pool_stats":
            return httpx.Response(200,json={"pool_stats":{"txs_total":7}})
        return httpx.Response(404)
    transport=httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        snap=await MoneroRPCClient("http://node",client=client).snapshot(xmr_usd=550)
    assert snap.height==3456789
    assert snap.estimated_hashrate_hs==6e9
    assert snap.reward_xmr==.6
    assert snap.mempool_transactions==7
    assert snap.fee_per_byte_atomic==20000
    assert snap.source=="monerod-rpc"
