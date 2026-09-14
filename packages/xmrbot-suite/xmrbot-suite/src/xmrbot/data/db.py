from __future__ import annotations
import sqlite3
from pathlib import Path
from xmrbot.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS network_observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  height INTEGER NOT NULL,
  difficulty REAL NOT NULL,
  target_seconds REAL NOT NULL,
  estimated_hashrate_hs REAL NOT NULL,
  reward_xmr REAL NOT NULL,
  xmr_usd REAL NOT NULL,
  mempool_transactions INTEGER NOT NULL DEFAULT 0,
  fee_per_byte_atomic INTEGER NOT NULL DEFAULT 0,
  source TEXT NOT NULL,
  confidence REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_network_timestamp ON network_observations(timestamp);

CREATE TABLE IF NOT EXISTS content_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  event_type TEXT NOT NULL,
  importance REAL NOT NULL,
  novelty REAL NOT NULL,
  payload_json TEXT NOT NULL
);
"""


def connect(path: str | None = None) -> sqlite3.Connection:
    db_path = path or settings.db_path
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
