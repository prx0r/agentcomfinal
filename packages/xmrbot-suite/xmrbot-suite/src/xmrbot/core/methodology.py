from __future__ import annotations

METHODOLOGIES = {
    "estimated-network-hashrate-v1": {
        "name": "Estimated network hashrate",
        "version": "v1",
        "formula": "difficulty / target_block_seconds",
        "inputs": ["difficulty", "target_block_seconds"],
    },
    "xmr-hashprice-v1": {
        "name": "XMR hashprice",
        "version": "v1",
        "formula": "(1000 / network_hashrate_hs) * reward_xmr * (86400 / target_seconds)",
        "inputs": ["network_hashrate_hs", "reward_xmr", "target_seconds"],
    },
    "randomx-profitability-v1": {
        "name": "RandomX profitability",
        "version": "v1",
        "formula": "worker_share * daily_emission * xmr_price - power - depreciation - fees",
        "inputs": ["hashrate", "network_hashrate", "reward", "xmr_price", "power", "hardware_cost"],
    },
    "mine-or-buy-v1": {
        "name": "Mine versus buy scenario",
        "version": "v1",
        "formula": "monthly production with compounding difficulty growth versus immediate XMR purchase",
        "inputs": ["budget", "hardware_cost", "hashrate", "power", "difficulty_growth", "residual_value"],
    },
}
