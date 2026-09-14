from __future__ import annotations
from xmrbot.core.types import NetworkSnapshot


def detect_events(previous: NetworkSnapshot | None, current: NetworkSnapshot) -> list[dict]:
    if previous is None:
        return []
    events = []
    def pct(a: float, b: float) -> float:
        return 0.0 if b == 0 else (a / b - 1.0) * 100.0

    difficulty_change = pct(current.difficulty, previous.difficulty)
    hashprice_change = pct(current.hashprice_usd_per_khs_day, previous.hashprice_usd_per_khs_day)
    price_change = pct(current.xmr_usd, previous.xmr_usd)
    if abs(difficulty_change) >= 10:
        events.append({"event": "difficulty_move", "importance": min(1, abs(difficulty_change)/30), "novelty": 0.8, "change_pct": difficulty_change})
    if abs(hashprice_change) >= 10:
        events.append({"event": "hashprice_move", "importance": min(1, abs(hashprice_change)/30), "novelty": 0.9, "change_pct": hashprice_change})
    if abs(price_change) >= 10:
        events.append({"event": "xmr_price_move", "importance": min(1, abs(price_change)/30), "novelty": 0.7, "change_pct": price_change})
    return events
