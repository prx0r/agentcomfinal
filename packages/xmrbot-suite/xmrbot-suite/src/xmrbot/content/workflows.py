from __future__ import annotations


def workflow_for_event(event: dict) -> dict:
    event_type = event.get("event", "network_update")
    mapping = {
        "difficulty_move": ("Monero difficulty just moved — what miners should know", "/terminal", "difficulty"),
        "hashprice_move": ("Monero mining economics just changed", "/mine", "hashprice"),
        "xmr_price_move": ("What XMR's price move means for miners", "/mine", "mine-vs-buy"),
    }
    title, target, dataset = mapping.get(event_type, ("Monero network update", "/terminal", "network"))
    return {
        "question": title,
        "search_intent": event_type,
        "dataset": dataset,
        "target_url": target,
        "hook": title,
        "youtube": {"title": title, "cta": f"Run the live numbers at xmrbot.com{target}"},
        "shorts": [
            {"hook": title, "cta": f"xmrbot.com{target}"},
            {"hook": "One chart explains the move", "cta": f"xmrbot.com{target}"},
        ],
        "x_post": f"{title}. Live methodology + numbers: xmrbot.com{target}",
    }
