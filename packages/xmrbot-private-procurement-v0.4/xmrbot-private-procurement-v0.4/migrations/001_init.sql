-- Production-oriented Postgres/Timescale schema. The running MVP uses equivalent SQLite tables.
CREATE TABLE IF NOT EXISTS network_observations (
  time TIMESTAMPTZ NOT NULL,
  height BIGINT NOT NULL,
  difficulty NUMERIC NOT NULL,
  target_seconds DOUBLE PRECISION NOT NULL,
  estimated_hashrate_hs DOUBLE PRECISION NOT NULL,
  reward_xmr NUMERIC NOT NULL,
  xmr_usd NUMERIC NOT NULL,
  mempool_transactions BIGINT NOT NULL DEFAULT 0,
  fee_per_byte_atomic BIGINT NOT NULL DEFAULT 0,
  source TEXT NOT NULL,
  confidence DOUBLE PRECISION NOT NULL
);
-- With TimescaleDB installed:
-- SELECT create_hypertable('network_observations', by_range('time'), if_not_exists => TRUE);
