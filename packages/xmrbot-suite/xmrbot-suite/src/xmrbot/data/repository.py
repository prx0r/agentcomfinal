from __future__ import annotations
from datetime import datetime, timezone
import json
import sqlite3
from xmrbot.core.types import NetworkSnapshot


class Repository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_network(self, snap: NetworkSnapshot) -> None:
        self.conn.execute(
            """INSERT INTO network_observations
            (timestamp,height,difficulty,target_seconds,estimated_hashrate_hs,reward_xmr,xmr_usd,mempool_transactions,fee_per_byte_atomic,source,confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (snap.timestamp.isoformat(), snap.height, snap.difficulty, snap.target_seconds,
             snap.estimated_hashrate_hs, snap.reward_xmr, snap.xmr_usd, snap.mempool_transactions,
             snap.fee_per_byte_atomic, snap.source, snap.confidence),
        )
        self.conn.commit()

    def latest_network(self) -> NetworkSnapshot | None:
        row = self.conn.execute("SELECT * FROM network_observations ORDER BY timestamp DESC, id DESC LIMIT 1").fetchone()
        return self._network(row) if row else None

    def network_history(self, limit: int = 500) -> list[NetworkSnapshot]:
        rows = self.conn.execute(
            "SELECT * FROM network_observations ORDER BY timestamp DESC, id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [self._network(r) for r in reversed(rows)]

    def add_event(self, event_type: str, importance: float, novelty: float, payload: dict) -> None:
        self.conn.execute(
            "INSERT INTO content_events(created_at,event_type,importance,novelty,payload_json) VALUES (?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), event_type, importance, novelty, json.dumps(payload)),
        )
        self.conn.commit()

    @staticmethod
    def _network(row: sqlite3.Row) -> NetworkSnapshot:
        return NetworkSnapshot(
            timestamp=row["timestamp"], height=row["height"], difficulty=row["difficulty"],
            target_seconds=row["target_seconds"], estimated_hashrate_hs=row["estimated_hashrate_hs"],
            reward_xmr=row["reward_xmr"], xmr_usd=row["xmr_usd"],
            mempool_transactions=row["mempool_transactions"], fee_per_byte_atomic=row["fee_per_byte_atomic"],
            source=row["source"], confidence=row["confidence"],
        )
