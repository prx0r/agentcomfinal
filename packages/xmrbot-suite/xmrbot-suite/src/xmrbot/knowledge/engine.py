from __future__ import annotations
import json
import re
from importlib.resources import files


class KnowledgeEngine:
    def __init__(self):
        path = files("xmrbot.knowledge").joinpath("sources.json")
        self.docs = json.loads(path.read_text())

    @staticmethod
    def _terms(text: str) -> set[str]:
        return {x for x in re.findall(r"[a-z0-9]+", text.lower()) if len(x) > 2}

    def search(self, query: str, limit: int = 5) -> list[dict]:
        q = self._terms(query)
        scored = []
        for doc in self.docs:
            hay = self._terms(" ".join([doc["title"], doc["text"], " ".join(doc["tags"])]))
            overlap = len(q & hay)
            phrase = 2 if query.lower() in (doc["title"] + " " + doc["text"]).lower() else 0
            score = overlap + phrase
            if score:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{**doc, "score": score} for score, doc in scored[:limit]]

    def resource_find(self, task: str) -> dict:
        text = task.lower()
        rules = [
            (("wallet", "create"), "monero-wallet-rpc", "Create/manage a wallet locally through controlled wallet RPC", "R2-sensitive-financial"),
            (("node",), "monerod", "Run/query a Monero full node", "R1-local-change"),
            (("p2pool",), "P2Pool", "Decentralized pooled mining", "R1-local-change"),
            (("mine",), "XMRig + P2Pool", "Benchmark and mine RandomX without custody", "R1-local-change"),
            (("fee",), "monerod get_fee_estimate", "Query current daemon fee estimate", "R0-read"),
            (("benchmark",), "XMRig benchmark", "Measure machine RandomX hashrate", "R1-local-change"),
        ]
        for words, resource, reason, risk in rules:
            if all(w in text for w in words):
                return {"task": task, "recommended": {"resource": resource, "reason": reason, "risk": risk}, "alternatives": []}
        hits = self.search(task, 3)
        return {"task": task, "recommended": hits[0] if hits else None, "alternatives": hits[1:]}

engine = KnowledgeEngine()
