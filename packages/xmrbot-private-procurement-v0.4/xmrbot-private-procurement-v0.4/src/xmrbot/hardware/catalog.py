from __future__ import annotations
import json
from importlib.resources import files
from xmrbot.core.types import CPURecord, NetworkSnapshot, ProfitabilityRequest
from xmrbot.core.economics import profitability


class HardwareCatalog:
    def __init__(self):
        path = files("xmrbot.hardware").joinpath("cpus.json")
        self._cpus = [CPURecord.model_validate(x) for x in json.loads(path.read_text())]

    def all(self) -> list[CPURecord]:
        return list(self._cpus)

    def get(self, slug: str) -> CPURecord | None:
        return next((x for x in self._cpus if x.slug == slug), None)

    def search(self, query: str) -> list[CPURecord]:
        q = query.lower().strip()
        return [x for x in self._cpus if q in f"{x.manufacturer} {x.model} {x.slug}".lower()]

    def rankings(self, net: NetworkSnapshot, electricity_usd_kwh: float = 0.10) -> list[dict]:
        rows = []
        for cpu in self._cpus:
            watts = cpu.benchmark_watts or cpu.tdp_w
            p = profitability(ProfitabilityRequest(
                hashrate_hs=cpu.benchmark_hashrate_hs, watts=watts,
                electricity_usd_kwh=electricity_usd_kwh,
                hardware_cost_usd=cpu.reference_price_usd or 0,
                amortization_months=36 if cpu.reference_price_usd else 0,
            ), net)
            rows.append({
                **cpu.model_dump(),
                "hashrate_per_watt": cpu.benchmark_hashrate_hs / watts,
                "hashrate_per_usd": None if not cpu.reference_price_usd else cpu.benchmark_hashrate_hs / cpu.reference_price_usd,
                "expected_xmr_year": p.expected_xmr_year,
                "net_usd_day": p.net_usd_day,
                "effective_cost_per_xmr_usd": p.effective_cost_per_xmr_usd,
            })
        return sorted(rows, key=lambda r: (r["hashrate_per_usd"] or 0), reverse=True)

catalog = HardwareCatalog()
