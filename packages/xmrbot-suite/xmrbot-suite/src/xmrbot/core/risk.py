from __future__ import annotations
from xmrbot.core.types import RiskClass

TOOL_RISK = {
    "xmr_tools": RiskClass.R0,
    "xmr_search": RiskClass.R0,
    "xmr_network_status": RiskClass.R0,
    "xmr_mining_profitability": RiskClass.R0,
    "xmr_cpu_lookup": RiskClass.R0,
    "xmr_mine_or_buy": RiskClass.R0,
    "xmr_resource_find": RiskClass.R0,
    "xmr_node_plan": RiskClass.R0,
    "xmr_wallet_plan": RiskClass.R0,
    "xmr_machine_inspect": RiskClass.R0,
    "xmr_machine_benchmark": RiskClass.R1,
    "xmr_computer_opportunities": RiskClass.R0,
}

DISABLED_WALLET_ACTIONS = {"wallet.export_seed", "wallet.export_keys"}
