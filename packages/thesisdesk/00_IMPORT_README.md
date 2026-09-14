# ThesisDesk

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `thesisdesk`
- **source zip:** `docs/thesisdesk.zip` (9946 bytes)
- **unpacked:** 6 files, 25702 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `thesisdesk`
- **original README(s):** `thesisdesk/README.md`

## What this is

Tiny desk UI: index.html + app.js + app.css + trades.json + RESEARCH.md. Smallest package, likely prototype for campaign frontend.

## Layout (top 2 levels)

```
  thesisdesk/README.md (1640b)
  thesisdesk/RESEARCH.md (1280b)
  thesisdesk/app.css (3429b)
  thesisdesk/app.js (6257b)
  thesisdesk/data/trades.json (11784b)
  thesisdesk/index.html (1312b)
```

## Original README excerpt

_Source: `thesisdesk/README.md`_

```markdown
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


... (+13 more lines in thesisdesk/README.md)
```

## How to use

- Raw zip stays in `docs/thesisdesk.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/thesisdesk -q` (adjust to inner dir, e.g. `packages/thesisdesk/thesisdesk`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
