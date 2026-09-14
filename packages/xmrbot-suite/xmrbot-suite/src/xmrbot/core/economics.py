from __future__ import annotations
from xmrbot.core.types import MineOrBuyRequest, NetworkSnapshot, ProfitabilityRequest, ProfitabilityResult

DAYS_PER_MONTH = 365.0 / 12.0


def profitability(req: ProfitabilityRequest, net: NetworkSnapshot) -> ProfitabilityResult:
    price = req.xmr_usd or net.xmr_usd
    share = req.hashrate_hs / net.estimated_hashrate_hs
    xmr_day = share * net.daily_emission_xmr
    gross_usd = xmr_day * price
    electricity = (req.watts / 1000.0) * 24.0 * req.electricity_usd_kwh
    depreciation = 0.0
    if req.hardware_cost_usd and req.amortization_months:
        depreciation = req.hardware_cost_usd / (req.amortization_months * DAYS_PER_MONTH)
    fee = gross_usd * (req.pool_fee_pct / 100.0)
    net_usd = gross_usd - electricity - depreciation - fee
    production_cost = None if xmr_day <= 0 else (electricity + depreciation + fee) / xmr_day
    break_even = None if xmr_day <= 0 else (electricity + depreciation) / (xmr_day * (1 - req.pool_fee_pct / 100.0))
    return ProfitabilityResult(
        expected_xmr_day=xmr_day,
        expected_xmr_month=xmr_day * DAYS_PER_MONTH,
        expected_xmr_year=xmr_day * 365.0,
        gross_usd_day=gross_usd,
        electricity_usd_day=electricity,
        depreciation_usd_day=depreciation,
        pool_fee_usd_day=fee,
        net_usd_day=net_usd,
        effective_cost_per_xmr_usd=production_cost,
        break_even_xmr_price_usd=break_even,
        network_hashrate_hs=net.estimated_hashrate_hs,
    )


def mine_or_buy(req: MineOrBuyRequest, net: NetworkSnapshot) -> dict:
    price = req.xmr_usd or net.xmr_usd
    buy_xmr = req.budget_usd / price
    if req.hardware_cost_usd > req.budget_usd:
        return {
            "decision": "buy",
            "reason": "hardware cost exceeds budget",
            "buy_xmr": buy_xmr,
            "mine_xmr": 0.0,
            "net_mining_value_usd": 0.0,
            "methodology": "mine-or-buy-v1",
        }

    base_daily = (req.hashrate_hs / net.estimated_hashrate_hs) * net.daily_emission_xmr
    monthly_growth = 1 + req.monthly_difficulty_growth_pct / 100.0
    mined = 0.0
    electricity = 0.0
    monthly_power = (req.watts / 1000.0) * 24.0 * DAYS_PER_MONTH * req.electricity_usd_kwh
    monthly_rows = []
    for month in range(req.months):
        difficulty_factor = monthly_growth ** month
        produced = base_daily * DAYS_PER_MONTH / difficulty_factor
        mined += produced
        electricity += monthly_power
        monthly_rows.append({"month": month + 1, "xmr": produced, "difficulty_factor": difficulty_factor})

    residual = req.hardware_cost_usd * req.residual_value_pct / 100.0
    spare_cash = max(0.0, req.budget_usd - req.hardware_cost_usd)
    spare_cash_xmr = spare_cash / price
    mine_total_xmr_equiv = mined + spare_cash_xmr
    mining_value = mine_total_xmr_equiv * price + residual - electricity
    buy_value = buy_xmr * price
    decision = "mine" if mining_value > buy_value else "buy"
    return {
        "decision": decision,
        "buy_xmr": buy_xmr,
        "mine_xmr": mined,
        "spare_cash_xmr": spare_cash_xmr,
        "mine_total_xmr_equivalent": mine_total_xmr_equiv,
        "electricity_usd": electricity,
        "residual_value_usd": residual,
        "net_mining_value_usd": mining_value,
        "buy_value_usd": buy_value,
        "delta_usd": mining_value - buy_value,
        "months": req.months,
        "monthly": monthly_rows,
        "methodology": "mine-or-buy-v1",
    }
