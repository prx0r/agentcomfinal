# ThesisDesk

A deliberately small thesis-trading cockpit.

## Run

Because the app loads `data/trades.json`, serve the folder over a tiny local HTTP server:

```bash
cd thesisdesk
python3 -m http.server 8080
```

Open http://localhost:8080

## Included trades

1. **XMR > ZEC** — relative-value thesis. Main chart is **XMR market cap / ZEC market cap**. Parity = 1.0.
2. **NIL → $0.10** — long Nillion thesis with price chart, target, fundamentals, falsifiers and roadmap evidence.

## Philosophy

A trade is not a ticker. It is a falsifiable claim with:
- target + horizon
- conviction
- thesis
- supporting mechanisms/catalysts
- explicit falsification conditions
- levels mapped to actions
- metrics and source links
- append-only decision log

The browser stores decision logs in `localStorage`, so refreshes do not erase them.

## Add trades

Use **+ Trade** for a blank thesis tab. For a fully specified persistent trade, add an object to `data/trades.json`.

## Data

The bundled market data is intentionally static and timestamped so the initial thesis is reproducible. Current seed data comes from CoinGecko historical tables and official project sources retrieved Sep 12, 2026.

A sensible next version is a tiny server-side fetcher that writes a daily snapshot to `data/history/*.json`; avoid making the research UI depend on a fragile browser API call.

## Suggested next modules

- Daily snapshot job (prices, market caps, volume, FDV, unlocks)
- Relative-value z-score / percentile chart
- Catalyst calendar
- Source monitor/RSS
- Automatic falsifier checker
- P&L and position sizing
- Git-backed immutable thesis log
